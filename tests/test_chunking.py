"""
Unit tests for the chunking logic.
"""

from app.config import Settings
from app.services.document_service import DocumentService


def test_create_chunks(mock_embedding_provider, mock_vector_repository, mock_llm_provider):
    """Test that page text is correctly chunked and page number is preserved."""
    settings = Settings(
        chunk_size=100,
        chunk_overlap=20,
    )
    
    # We instantiate DocumentService with mocked dependencies
    from app.services.embedding_service import EmbeddingService
    from app.services.vector_store_service import VectorStoreService
    from app.services.prompt_service import PromptService

    embed_svc = EmbeddingService(mock_embedding_provider)
    vector_svc = VectorStoreService(mock_vector_repository)
    prompt_svc = PromptService()

    doc_service = DocumentService(
        settings=settings,
        embedding_service=embed_svc,
        vector_store_service=vector_svc,
        llm_provider=mock_llm_provider,
        prompt_service=prompt_svc
    )

    pages = [
        (1, "This is page one content. It has some text that will be split because we configured a small chunk size."),
        (2, "This is page two. More text to process for this document chunker.")
    ]

    chunks = doc_service._create_chunks("doc-123", pages)

    assert len(chunks) > 0
    assert all(chunk.document_id == "doc-123" for chunk in chunks)
    
    # Check page preservation
    page_1_chunks = [c for c in chunks if c.page_number == 1]
    page_2_chunks = [c for c in chunks if c.page_number == 2]
    
    assert len(page_1_chunks) > 0
    assert len(page_2_chunks) > 0
    
    # Check indexing order
    assert chunks[0].chunk_index == 0
    assert chunks[1].chunk_index == 1
    assert chunks[-1].chunk_index == len(chunks) - 1
