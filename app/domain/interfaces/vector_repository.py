"""
Abstract vector repository interface.

Defines the contract for vector database operations,
implementing the Repository Pattern to decouple the
vector store implementation from business logic.
"""

from abc import ABC, abstractmethod

from app.domain.models import Chunk, RetrievalResult


class VectorRepository(ABC):
    """
    Abstract base class for vector storage repositories.

    Provides CRUD-like operations for managing document
    embeddings and performing similarity searches.
    """

    @abstractmethod
    def add_documents(
        self,
        document_id: str,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Store document chunk embeddings in the vector store.

        Args:
            document_id: Unique identifier for the document.
            chunks: List of text chunks with metadata.
            embeddings: Corresponding embedding vectors.

        Raises:
            RuntimeError: If storing embeddings fails.
        """
        ...

    @abstractmethod
    def search(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Search for the most similar chunks to a query.

        Args:
            document_id: ID of the document to search within.
            query_embedding: The query embedding vector.
            top_k: Number of top results to return.

        Returns:
            List of retrieval results ordered by similarity.

        Raises:
            KeyError: If the document_id does not exist.
            RuntimeError: If the search operation fails.
        """
        ...

    @abstractmethod
    def exists(self, document_id: str) -> bool:
        """
        Check if a document index exists.

        Args:
            document_id: The document ID to check.

        Returns:
            True if the document's index exists.
        """
        ...

    @abstractmethod
    def delete(self, document_id: str) -> None:
        """
        Delete a document's index from the vector store.

        Args:
            document_id: The document ID to delete.

        Raises:
            KeyError: If the document_id does not exist.
        """
        ...
