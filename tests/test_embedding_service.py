"""
Unit tests for the EmbeddingService.
"""

from app.services.embedding_service import EmbeddingService


def test_embedding_service_methods(mock_embedding_provider):
    """Test that embedding service forwards queries and texts correctly."""
    service = EmbeddingService(embedding_provider=mock_embedding_provider)
    
    # Test dimension retrieval
    assert service.get_dimension() == 384
    
    # Test batch embedding
    texts = ["hello", "world"]
    embeddings = service.embed_chunks(texts)
    assert len(embeddings) == 2
    assert len(embeddings[0]) == 384
    
    # Test single query embedding
    query_emb = service.embed_query("search text")
    assert len(query_emb) == 384
