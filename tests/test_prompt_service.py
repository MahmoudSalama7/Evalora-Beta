"""
Unit tests for the PromptService.
"""

from app.domain.models import Chunk, RetrievalResult, Message, MessageRole
from app.services.prompt_service import PromptService


def test_build_qa_prompt():
    """Test that prompt constructs context and history correctly."""
    service = PromptService()
    
    chunks = [
        RetrievalResult(
            chunk=Chunk(chunk_id="c1", document_id="doc1", content="Termination requires 30 days notice.", page_number=4, chunk_index=0),
            score=0.9
        )
    ]
    
    history = [
        Message(role=MessageRole.HUMAN, content="Hi"),
        Message(role=MessageRole.ASSISTANT, content="Hello. How can I help you?")
    ]
    
    sys_prompt, user_prompt = service.build_qa_prompt(
        question="How is termination handled?",
        retrieved_chunks=chunks,
        conversation_history=history
    )
    
    # Assert system prompt contains grounding rules
    assert "Answer ONLY using the provided document context" in sys_prompt
    
    # Assert user prompt contains question, context, and history
    assert "Termination requires 30 days notice." in user_prompt
    assert "Page 4" in user_prompt
    assert "User: Hi" in user_prompt
    assert "Assistant: Hello" in user_prompt
    assert "How is termination handled?" in user_prompt


def test_parse_follow_up_questions():
    """Test that parser extracts follow-up questions from response block."""
    service = PromptService()
    
    raw_response = (
        "The agreement is governed by New York law.\n"
        "FOLLOW_UP: 1. Which court has jurisdiction?\n"
        "FOLLOW_UP: 2. What is the governing law?\n"
        "FOLLOW_UP: 3. Are there arbitration clauses?"
    )
    
    clean_ans, follow_ups = service.parse_follow_up_questions(raw_response)
    
    assert clean_ans == "The agreement is governed by New York law."
    assert len(follow_ups) == 3
    assert follow_ups[0] == "Which court has jurisdiction?"
    assert follow_ups[1] == "What is the governing law?"
    assert follow_ups[2] == "Are there arbitration clauses?"
