"""
Abstract embedding provider interface.

Defines the contract for text embedding services, allowing
different embedding models to be swapped without changing
the service layer.
"""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Abstract base class for embedding providers.

    Concrete implementations generate dense vector representations
    of text using models like Sentence Transformers.
    """

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors, one per input text.

        Raises:
            RuntimeError: If embedding generation fails.
        """
        ...

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """
        Generate an embedding for a single query string.

        Some models use different encoding for queries vs documents.

        Args:
            query: The query text to embed.

        Returns:
            The embedding vector for the query.

        Raises:
            RuntimeError: If embedding generation fails.
        """
        ...

    @abstractmethod
    def get_dimension(self) -> int:
        """
        Return the dimensionality of the embeddings.

        Returns:
            The number of dimensions in the embedding vectors.
        """
        ...
