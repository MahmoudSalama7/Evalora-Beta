"""
Groq LLM provider implementation.

Implements the LLMProvider interface using the Groq API,
which provides fast inference for open-source models
like LLaMA and Mixtral.
"""

import logging
import time
from collections.abc import AsyncIterator
from typing import Optional

from groq import AsyncGroq

from app.domain.interfaces.llm_provider import LLMProvider

logger = logging.getLogger(__name__)


class GroqProvider(LLMProvider):
    """
    Concrete LLM provider using Groq's inference API.

    Implements the Strategy Pattern, allowing the LLM backend
    to be swapped without changing business logic.

    Args:
        api_key: Groq API key for authentication.
        model: Model identifier (e.g., 'llama-3.3-70b-versatile').
        temperature: Sampling temperature (0.0 to 1.0).
        max_tokens: Maximum tokens in the response.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.3-70b-versatile",
        temperature: float = 0.1,
        max_tokens: int = 2048,
    ) -> None:
        self._client = AsyncGroq(api_key=api_key)
        self._model = model
        self._temperature = temperature
        self._max_tokens = max_tokens

    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
    ) -> str:
        """
        Generate a complete response from Groq.

        Args:
            prompt: The user prompt.
            system_message: Optional system instructions.

        Returns:
            The complete generated text.

        Raises:
            RuntimeError: If the API request fails.
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        start_time = time.perf_counter()

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )

            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(
                f"LLM generation completed",
                extra={"duration_ms": duration_ms},
            )

            content = response.choices[0].message.content
            return content if content else ""

        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                f"LLM generation failed after {duration_ms}ms: {exc}",
                exc_info=True,
            )
            raise RuntimeError(f"LLM generation failed: {exc}") from exc

    async def stream(
        self,
        prompt: str,
        system_message: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """
        Stream a response from Groq token by token.

        Args:
            prompt: The user prompt.
            system_message: Optional system instructions.

        Yields:
            Individual tokens as they are generated.

        Raises:
            RuntimeError: If the API request fails.
        """
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        start_time = time.perf_counter()

        try:
            stream = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(
                f"LLM streaming completed",
                extra={"duration_ms": duration_ms},
            )

        except Exception as exc:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            logger.error(
                f"LLM streaming failed after {duration_ms}ms: {exc}",
                exc_info=True,
            )
            raise RuntimeError(f"LLM streaming failed: {exc}") from exc
