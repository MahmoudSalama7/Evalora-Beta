"""
FastAPI application factory.

Configures the FastAPI application with middleware, routes,
static file serving, and startup/shutdown lifecycle events.
"""

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import chat, history, upload, jobs
from app.config import get_settings
from app.utils.logging import RequestLoggingMiddleware, setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle manager.

    Handles startup initialization and shutdown cleanup.
    """
    settings = get_settings()

    # Setup logging
    setup_logging(settings.log_level)
    logger.info("Starting QA Assistant application")

    # Create data directories
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.faiss_index_dir, exist_ok=True)

    logger.info("Application started successfully")

    yield

    logger.info("Application shutting down")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    # Initialize logging early
    setup_logging(settings.log_level)

    app = FastAPI(
        title="Document QA Assistant",
        description=(
            "AI-powered Question Answering Assistant for legal documents. "
            "Upload PDF or DOCX files and ask questions using RAG."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )

    # ─── Middleware ────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestLoggingMiddleware)

    # ─── Routes ───────────────────────────────────────────────────
    app.include_router(upload.router)
    app.include_router(jobs.router)
    app.include_router(chat.router)
    app.include_router(history.router)

    # ─── Static Files (Frontend — Vite Build) ────────────────────
    frontend_dist_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "frontend", "dist"
    )
    frontend_assets_dir = os.path.join(frontend_dist_dir, "assets")

    if os.path.isdir(frontend_assets_dir):
        app.mount(
            "/assets",
            StaticFiles(directory=frontend_assets_dir),
            name="assets",
        )

    # ─── Health Check ─────────────────────────────────────────────
    @app.get("/health", tags=["System"])
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": "1.0.0"}

    # ─── SPA Catch-All → Serve index.html for client-side routing ─
    from fastapi.responses import FileResponse

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        """
        Serve the React SPA.

        For any route not matched by API endpoints, return index.html
        so React Router can handle client-side navigation.
        """
        # Check if a specific static file exists in dist/
        file_path = os.path.join(frontend_dist_dir, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)

        # Otherwise, serve index.html for SPA routing
        index_path = os.path.join(frontend_dist_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Evalora AI API", "docs": "/docs"}

    return app


# Create the application instance
app = create_app()
