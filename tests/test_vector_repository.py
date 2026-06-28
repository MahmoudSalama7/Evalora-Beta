"""
Unit tests for the FAISSRepository.
"""

import pytest
from app.infrastructure.vectorstore.faiss_repository import FAISSRepository
from app.domain.models import Chunk


def test_faiss_repository_indexing_and_searching():
    """Test that FAISSRepository can index documents and search with cosine similarity."""
    repo = FAISSRepository()
    doc_id = "legal-doc-abc"
    
    # 3-dimensional normalized embeddings for simplicity
    embeddings = [
        [1.0, 0.0, 0.0],  # chunk 0: highly aligned to X-axis
        [0.0, 1.0, 0.0],  # chunk 1: highly aligned to Y-axis
        [0.0, 0.0, 1.0]   # chunk 2: highly aligned to Z-axis
    ]
    
    chunks = [
        Chunk(chunk_id="c1", document_id=doc_id, content="X-axis content", page_number=1, chunk_index=0),
        Chunk(chunk_id="c2", document_id=doc_id, content="Y-axis content", page_number=2, chunk_index=1),
        Chunk(chunk_id="c3", document_id=doc_id, content="Z-axis content", page_number=3, chunk_index=2)
    ]
    
    # Add documents to index
    repo.add_documents(doc_id, chunks, embeddings)
    assert repo.exists(doc_id) is True
    
    # Search for Y-aligned query
    query_emb = [0.1, 0.9, 0.0]  # Closest to chunk 1 (Y-axis)
    results = repo.search(doc_id, query_emb, top_k=2)
    
    assert len(results) == 2
    assert results[0].chunk.chunk_id == "c2"  # Should be the closest match
    assert results[0].score > 0.8
    
    # Delete document
    repo.delete(doc_id)
    assert repo.exists(doc_id) is False
    
    # Verify search fails for deleted document
    with pytest.raises(KeyError):
        repo.search(doc_id, query_emb)
