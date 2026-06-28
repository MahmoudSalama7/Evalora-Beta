"""
Vector store service.

Provides a clean service interface for vector storage operations.
Delegates to the VectorRepository infrastructure component.
"""

import logging

from app.domain.interfaces.vector_repository import VectorRepository
from app.domain.models import Chunk, RetrievalResult

logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Service for managing vector storage operations.

    Wraps the VectorRepository with service-level concerns
    like logging, validation, and configuration.

    Args:
        vector_repository: The concrete vector repository to use.
        top_k: Default number of results to return in searches.
    """

    def __init__(
        self,
        vector_repository: VectorRepository,
        top_k: int = 5,
    ) -> None:
        self._repository = vector_repository
        self._top_k = top_k

    def index_document(
        self,
        document_id: str,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Index a document's chunks in the vector store.

        Args:
            document_id: Unique document identifier.
            chunks: The document's text chunks.
            embeddings: Corresponding embedding vectors.
        """
        logger.info(
            f"Indexing document {document_id}: {len(chunks)} chunks"
        )
        self._repository.add_documents(document_id, chunks, embeddings)

    def search(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int | None = None,
    ) -> list[RetrievalResult]:
        """
        Search for similar chunks in a document.

        Args:
            document_id: The document to search within.
            query_embedding: The query embedding vector.
            top_k: Override default number of results.

        Returns:
            List of retrieval results with similarity scores.
        """
        k = top_k or self._top_k
        logger.debug(f"Searching document {document_id}, top-{k}")
        return self._repository.search(document_id, query_embedding, k)

    def document_exists(self, document_id: str) -> bool:
        """Check if a document has been indexed."""
        return self._repository.exists(document_id)

    def delete_document(self, document_id: str) -> None:
        """Delete a document's index."""
        self._repository.delete(document_id)
        logger.info(f"Deleted vector index for document: {document_id}")
