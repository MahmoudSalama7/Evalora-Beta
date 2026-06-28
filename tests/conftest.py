"""
Shared test fixtures and mocks.
"""

from collections.abc import AsyncIterator
from datetime import datetime, timezone
import pytest
from typing import Optional

from app.domain.interfaces.embedding_provider import EmbeddingProvider
from app.domain.interfaces.llm_provider import LLMProvider
from app.domain.interfaces.vector_repository import VectorRepository
from app.domain.interfaces.conversation_repository import ConversationRepository
from app.domain.models import Chunk, RetrievalResult, Conversation, Message, MessageRole


# ─── Mock Embedding Provider ────────────────────────────────────────

class MockEmbeddingProvider(EmbeddingProvider):
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # Return dummy 384-dimensional embeddings (unit-normalized)
        return [[1.0] + [0.0] * 383 for _ in texts]

    def embed_query(self, query: str) -> list[float]:
        return [1.0] + [0.0] * 383

    def get_dimension(self) -> int:
        return 384


# ─── Mock LLM Provider ──────────────────────────────────────────────

class MockLLMProvider(LLMProvider):
    def __init__(self, response_text: str = "Test answer.\nFOLLOW_UP: 1. Q1?\nFOLLOW_UP: 2. Q2?\nFOLLOW_UP: 3. Q3?") -> None:
        self.response_text = response_text

    async def generate(self, prompt: str, system_message: Optional[str] = None) -> str:
        return self.response_text

    async def stream(self, prompt: str, system_message: Optional[str] = None) -> AsyncIterator[str]:
        # Yield words one by one
        for word in self.response_text.split(" "):
            yield word + " "


# ─── Mock Vector Repository ─────────────────────────────────────────

class MockVectorRepository(VectorRepository):
    def __init__(self) -> None:
        self.store = {}

    def add_documents(self, document_id: str, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        self.store[document_id] = (chunks, embeddings)

    def search(self, document_id: str, query_embedding: list[float], top_k: int = 5) -> list[RetrievalResult]:
        if document_id not in self.store:
            raise KeyError(f"Document {document_id} not found")
        chunks, _ = self.store[document_id]
        return [RetrievalResult(chunk=chunk, score=0.99) for chunk in chunks[:top_k]]

    def exists(self, document_id: str) -> bool:
        return document_id in self.store

    def delete(self, document_id: str) -> None:
        if document_id not in self.store:
            raise KeyError(f"Document {document_id} not found")
        del self.store[document_id]


# ─── Mock Conversation Repository ───────────────────────────────────

class MockConversationRepository(ConversationRepository):
    def __init__(self) -> None:
        self.sessions = {}

    def create_session(self, session_id: str, document_id: str) -> Conversation:
        conv = Conversation(session_id=session_id, document_id=document_id)
        self.sessions[session_id] = conv
        return conv

    def get_session(self, session_id: str) -> Optional[Conversation]:
        return self.sessions.get(session_id)

    def add_message(self, session_id: str, message: Message) -> None:
        if session_id not in self.sessions:
            raise KeyError(f"Session {session_id} not found")
        self.sessions[session_id].messages.append(message)

    def get_history(self, session_id: str) -> list[Message]:
        if session_id not in self.sessions:
            raise KeyError(f"Session {session_id} not found")
        return self.sessions[session_id].messages

    def session_exists(self, session_id: str) -> bool:
        return session_id in self.sessions


# ─── Pytest Fixtures ───────────────────────────────────────────────

@pytest.fixture
def mock_embedding_provider():
    return MockEmbeddingProvider()


@pytest.fixture
def mock_llm_provider():
    return MockLLMProvider()


@pytest.fixture
def mock_vector_repository():
    return MockVectorRepository()


@pytest.fixture
def mock_conversation_repository():
    return MockConversationRepository()
