"""
Embedding service.

Provides a clean service interface for generating text embeddings.
Delegates to the EmbeddingProvider infrastructure component.
"""

import logging

from app.domain.interfaces.embedding_provider import EmbeddingProvider

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating text embeddings.

    Acts as a thin wrapper around the EmbeddingProvider,
    adding logging and error handling at the service layer.

    Args:
        embedding_provider: The concrete embedding provider to use.
    """

    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self._provider = embedding_provider

    def embed_chunks(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for document chunks.

        Args:
            texts: List of chunk text content.

        Returns:
            List of embedding vectors.
        """
        logger.info(f"Generating embeddings for {len(texts)} chunks")
        embeddings = self._provider.embed_texts(texts)
        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings

    def embed_query(self, query: str) -> list[float]:
        """
        Generate an embedding for a search query.

        Args:
            query: The search query text.

        Returns:
            The query embedding vector.
        """
        logger.debug(f"Generating query embedding for: {query[:50]}...")
        return self._provider.embed_query(query)

    def get_dimension(self) -> int:
        """Get the embedding dimensionality."""
        return self._provider.get_dimension()
