"""
Structured logging configuration.

Provides JSON-formatted structured logging with request ID tracking
and performance measurement middleware.
"""

import logging
import sys
import time
import uuid
from contextvars import ContextVar
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Context variable for request-scoped data
request_id_var: ContextVar[str] = ContextVar("request_id", default="N/A")


class StructuredFormatter(logging.Formatter):
    """
    JSON-style structured log formatter.

    Produces log records with consistent fields including
    timestamp, level, module, message, and request ID.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a structured string."""
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_var.get("N/A"),
        }

        if record.exc_info and record.exc_info[1]:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add any extra fields
        for key in ("duration_ms", "document_id", "session_id", "endpoint"):
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        parts = [f"{k}={v}" for k, v in log_data.items()]
        return " | ".join(parts)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware that logs each HTTP request with timing information.

    Assigns a unique request ID and measures request duration.
    """

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        """Process request with logging and timing."""
        req_id = str(uuid.uuid4())[:8]
        request_id_var.set(req_id)

        logger = logging.getLogger("api")
        logger.info(
            "Request started",
            extra={"endpoint": f"{request.method} {request.url.path}"},
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            logger.info(
                "Request completed",
                extra={
                    "endpoint": f"{request.method} {request.url.path}",
                    "duration_ms": duration_ms,
                },
            )
            response.headers["X-Request-ID"] = req_id
            return response

        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                f"Request failed: {exc}",
                extra={
                    "endpoint": f"{request.method} {request.url.path}",
                    "duration_ms": duration_ms,
                },
                exc_info=True,
            )
            raise


def setup_logging(level: str = "INFO") -> None:
    """
    Configure structured logging for the application.

    Args:
        level: The logging level string (e.g., 'INFO', 'DEBUG').
    """
    formatter = StructuredFormatter()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Suppress noisy third-party loggers
    for noisy_logger in ("httpx", "httpcore", "uvicorn.access"):
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
