"""
Sentence Transformer embedding provider implementation.

Uses the sentence-transformers library to generate dense
vector embeddings for text chunks and queries.
"""

import logging
from typing import Optional

from sentence_transformers import SentenceTransformer

from app.domain.interfaces.embedding_provider import EmbeddingProvider

logger = logging.getLogger(__name__)


class SentenceTransformerEmbeddings(EmbeddingProvider):
    """
    Concrete embedding provider using Sentence Transformers.

    Loads a pre-trained model (default: BAAI/bge-small-en-v1.5)
    and generates embeddings for document chunks and queries.

    Note: BGE models use a query prefix 'Represent this sentence: '
    for better retrieval performance.

    Args:
        model_name: The Hugging Face model identifier.
    """

    QUERY_PREFIX = "Represent this sentence: "

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5") -> None:
        logger.info(f"Loading embedding model: {model_name}")
        self._model: Optional[SentenceTransformer] = None
        self._model_name = model_name
        self._dimension: Optional[int] = None

    def _ensure_loaded(self) -> SentenceTransformer:
        """Lazy-load the model on first use."""
        if self._model is None:
            self._model = SentenceTransformer(self._model_name)
            # Determine dimension from a test embedding
            test_embedding = self._model.encode(["test"])
            self._dimension = test_embedding.shape[1]
            logger.info(
                f"Embedding model loaded: {self._model_name}, "
                f"dimension={self._dimension}"
            )
        return self._model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a batch of document texts.

        Args:
            texts: List of text strings to embed.

        Returns:
            List of embedding vectors.

        Raises:
            RuntimeError: If embedding generation fails.
        """
        if not texts:
            return []

        try:
            model = self._ensure_loaded()
            embeddings = model.encode(
                texts,
                show_progress_bar=False,
                normalize_embeddings=True,
                batch_size=32,
            )
            return embeddings.tolist()

        except Exception as exc:
            logger.error(f"Embedding generation failed: {exc}", exc_info=True)
            raise RuntimeError(f"Failed to generate embeddings: {exc}") from exc

    def embed_query(self, query: str) -> list[float]:
        """
        Generate an embedding for a search query.

        Uses a query prefix for BGE models to improve retrieval.

        Args:
            query: The query text to embed.

        Returns:
            The embedding vector.

        Raises:
            RuntimeError: If embedding generation fails.
        """
        try:
            model = self._ensure_loaded()
            prefixed_query = f"{self.QUERY_PREFIX}{query}"
            embedding = model.encode(
                [prefixed_query],
                show_progress_bar=False,
                normalize_embeddings=True,
            )
            return embedding[0].tolist()

        except Exception as exc:
            logger.error(f"Query embedding failed: {exc}", exc_info=True)
            raise RuntimeError(f"Failed to embed query: {exc}") from exc

    def get_dimension(self) -> int:
        """
        Return the dimensionality of the embeddings.

        Returns:
            The number of dimensions in the embedding vectors.
        """
        self._ensure_loaded()
        assert self._dimension is not None
        return self._dimension
