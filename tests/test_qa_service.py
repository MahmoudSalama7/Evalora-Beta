"""
Unit tests for the QAService.
"""

import pytest
from app.services.qa_service import QAService, SIMILARITY_THRESHOLD
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.prompt_service import PromptService
from app.services.conversation_service import ConversationService
from app.domain.models import Chunk, RetrievalResult


@pytest.mark.asyncio
async def test_qa_service_happy_path(
    mock_embedding_provider,
    mock_vector_repository,
    mock_llm_provider,
    mock_conversation_repository
):
    """Test standard QA pipeline flow when matches are found above threshold."""
    embed_svc = EmbeddingService(mock_embedding_provider)
    vector_svc = VectorStoreService(mock_vector_repository)
    prompt_svc = PromptService()
    conv_svc = ConversationService(mock_conversation_repository)
    
    qa_service = QAService(
        embedding_service=embed_svc,
        vector_store_service=vector_svc,
        prompt_service=prompt_svc,
        conversation_service=conv_svc,
        llm_provider=mock_llm_provider
    )
    
    doc_id = "doc-123"
    question = "Who are the parties?"
    
    # Pre-index mock document chunk
    chunk = Chunk(chunk_id="c1", document_id=doc_id, content="Agreement between Party A and Party B", page_number=1, chunk_index=0)
    mock_vector_repository.add_documents(doc_id, [chunk], [[1.0]*384])
    
    # Run service
    res = await qa_service.answer(document_id=doc_id, question=question)
    
    assert "Test answer" in res.answer
    assert len(res.sources) == 1
    assert res.sources[0].chunk.content == "Agreement between Party A and Party B"
    assert len(res.suggested_questions) == 3


@pytest.mark.asyncio
async def test_qa_service_below_threshold(
    mock_embedding_provider,
    mock_vector_repository,
    mock_llm_provider,
    mock_conversation_repository
):
    """Test QA pipeline returning 'not found' message when search score is below threshold."""
    embed_svc = EmbeddingService(mock_embedding_provider)
    
    # Mock search response returning very low score
    class LowScoreVectorRepository(mock_vector_repository.__class__):
        def search(self, document_id: str, query_embedding: list[float], top_k: int = 5) -> list[RetrievalResult]:
            chunks, _ = self.store[document_id]
            return [RetrievalResult(chunk=chunk, score=0.01) for chunk in chunks]
            
    low_score_repo = LowScoreVectorRepository()
    vector_svc = VectorStoreService(low_score_repo)
    prompt_svc = PromptService()
    conv_svc = ConversationService(mock_conversation_repository)
    
    qa_service = QAService(
        embedding_service=embed_svc,
        vector_store_service=vector_svc,
        prompt_service=prompt_svc,
        conversation_service=conv_svc,
        llm_provider=mock_llm_provider
    )
    
    doc_id = "doc-123"
    question = "Unrelated question?"
    
    chunk = Chunk(chunk_id="c1", document_id=doc_id, content="Agreement between Party A and Party B", page_number=1, chunk_index=0)
    low_score_repo.add_documents(doc_id, [chunk], [[1.0]*384])
    
    res = await qa_service.answer(document_id=doc_id, question=question)
    
    assert res.answer == "I couldn't find this information in the uploaded document."
    assert len(res.sources) == 0
    assert len(res.suggested_questions) == 0
