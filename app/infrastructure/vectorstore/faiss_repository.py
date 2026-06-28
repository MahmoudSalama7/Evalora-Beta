"""
FAISS vector repository implementation.

Implements the VectorRepository interface using Facebook's
FAISS library for efficient similarity search. Uses in-memory
indices per document for lightweight operation.
"""

import logging
from typing import Optional

import faiss
import numpy as np

from app.domain.interfaces.vector_repository import VectorRepository
from app.domain.models import Chunk, RetrievalResult

logger = logging.getLogger(__name__)


class FAISSRepository(VectorRepository):
    """
    Concrete vector repository using FAISS.

    Maintains separate in-memory FAISS indices per document
    for isolated similarity searches. Uses Inner Product
    (cosine similarity with normalized vectors).

    Repository Pattern: Abstracts vector storage from business logic.
    """

    def __init__(self) -> None:
        # Per-document storage: {document_id: (index, chunks)}
        self._indices: dict[str, tuple[faiss.Index, list[Chunk]]] = {}

    def add_documents(
        self,
        document_id: str,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Store document chunk embeddings in a FAISS index.

        Creates a new FAISS index for the document using
        Inner Product similarity (assumes normalized vectors).

        Args:
            document_id: Unique identifier for the document.
            chunks: List of text chunks with metadata.
            embeddings: Corresponding normalized embedding vectors.

        Raises:
            RuntimeError: If index creation fails.
        """
        if not chunks or not embeddings:
            raise ValueError("Chunks and embeddings must not be empty")

        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Mismatch: {len(chunks)} chunks vs {len(embeddings)} embeddings"
            )

        try:
            embedding_matrix = np.array(embeddings, dtype=np.float32)
            dimension = embedding_matrix.shape[1]

            # Use Inner Product for cosine similarity (vectors are normalized)
            index = faiss.IndexFlatIP(dimension)
            index.add(embedding_matrix)

            self._indices[document_id] = (index, chunks)

            logger.info(
                f"Indexed document {document_id}: "
                f"{len(chunks)} chunks, dimension={dimension}"
            )

        except Exception as exc:
            logger.error(
                f"Failed to index document {document_id}: {exc}",
                exc_info=True,
            )
            raise RuntimeError(
                f"Failed to create FAISS index: {exc}"
            ) from exc

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
            query_embedding: The normalized query embedding vector.
            top_k: Number of top results to return.

        Returns:
            List of retrieval results ordered by similarity (highest first).

        Raises:
            KeyError: If the document_id does not exist.
        """
        if document_id not in self._indices:
            raise KeyError(f"Document not found in vector store: {document_id}")

        index, chunks = self._indices[document_id]

        # Ensure we don't request more results than available
        actual_k = min(top_k, len(chunks))

        query_vector = np.array([query_embedding], dtype=np.float32)
        scores, indices = index.search(query_vector, actual_k)

        results: list[RetrievalResult] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue  # FAISS returns -1 for missing results
            results.append(
                RetrievalResult(
                    chunk=chunks[idx],
                    score=float(score),
                )
            )

        logger.debug(
            f"Search in document {document_id}: "
            f"top-{actual_k}, best_score={results[0].score if results else 'N/A'}"
        )

        return results

    def exists(self, document_id: str) -> bool:
        """Check if a document index exists."""
        return document_id in self._indices

    def delete(self, document_id: str) -> None:
        """Delete a document's index."""
        if document_id not in self._indices:
            raise KeyError(f"Document not found: {document_id}")

        del self._indices[document_id]
        logger.info(f"Deleted index for document: {document_id}")
