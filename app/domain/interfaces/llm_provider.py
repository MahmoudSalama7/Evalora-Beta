"""
Abstract LLM provider interface.

Defines the contract for language model providers, enabling
the Strategy Pattern to swap between different LLM backends
(e.g., Groq, OpenAI, Ollama) without changing business logic.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    Concrete implementations must support both synchronous generation
    and asynchronous streaming.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
    ) -> str:
        """
        Generate a complete response from the LLM.

        Args:
            prompt: The user prompt to send to the LLM.
            system_message: Optional system-level instructions.

        Returns:
            The complete generated text response.

        Raises:
            RuntimeError: If the LLM request fails.
        """
        ...

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        system_message: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """
        Stream a response from the LLM token by token.

        Args:
            prompt: The user prompt to send to the LLM.
            system_message: Optional system-level instructions.

        Yields:
            Individual tokens or text chunks as they are generated.

        Raises:
            RuntimeError: If the LLM request fails.
        """
        ...
