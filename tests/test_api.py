"""
Integration/API tests for Document QA Assistant routes.
"""

import json
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api.dependencies import get_document_service, get_qa_service, get_conversation_service
from app.domain.models import Document, AnswerResult, RetrievalResult, Chunk, Conversation, Message, MessageRole


# ─── Mock Services for API Injection ──────────────────────────────

class MockDocumentService:
    async def upload(self, filename: str, file_content: bytes) -> Document:
        if filename == "corrupt.pdf":
            raise ValueError("Corrupted or invalid PDF file")
        return Document(
            document_id="mock-doc-id",
            filename=filename,
            page_count=3,
            chunk_count=10,
            summary="This is a mock summary of the document."
        )


class MockQAService:
    async def answer(self, document_id: str, question: str, session_id: str = None) -> AnswerResult:
        if document_id == "invalid-doc":
            raise KeyError("Document not found")
        return AnswerResult(
            answer="This is a mock answer from the assistant.",
            sources=[
                RetrievalResult(
                    chunk=Chunk(chunk_id="c1", document_id=document_id, content="Mock source chunk content", page_number=2, chunk_index=1),
                    score=0.95
                )
            ],
            suggested_questions=["Follow up 1?", "Follow up 2?"]
        )

    async def answer_stream(self, document_id: str, question: str, session_id: str = None):
        if document_id == "invalid-doc":
            yield {"type": "error", "data": "Document not found: invalid-doc"}
            return
        
        yield {
            "type": "sources",
            "data": [{"page": 2, "chunk": 1, "score": 0.95, "preview": "Mock source..."}]
        }
        yield {"type": "token", "data": "This is a "}
        yield {"type": "token", "data": "mock streamed answer."}
        yield {"type": "follow_ups", "data": ["Follow up 1?", "Follow up 2?"]}
        yield {"type": "done", "data": {"session_id": session_id or "mock-session-id"}}


class MockConversationService:
    def get_session(self, session_id: str) -> Conversation:
        if session_id == "invalid-session":
            return None
        from datetime import datetime, timezone
        conv = Conversation(session_id=session_id, document_id="mock-doc-id")
        conv.messages = [
            Message(role=MessageRole.HUMAN, content="Hi", timestamp=datetime.now(timezone.utc)),
            Message(role=MessageRole.ASSISTANT, content="Hello", timestamp=datetime.now(timezone.utc))
        ]
        return conv


@pytest.fixture(autouse=True)
def setup_dependency_overrides():
    """Setup mock service injection overrides before each test."""
    app.dependency_overrides[get_document_service] = lambda: MockDocumentService()
    app.dependency_overrides[get_qa_service] = lambda: MockQAService()
    app.dependency_overrides[get_conversation_service] = lambda: MockConversationService()
    yield
    app.dependency_overrides.clear()


# ─── API Routes Unit Tests ────────────────────────────────────────

def test_health_endpoint():
    """Test health check route."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}


def test_upload_pdf_endpoint():
    """Test POST /upload with PDF file."""
    client = TestClient(app)
    files = {"file": ("contract.pdf", b"%PDF-1.4 mock pdf data", "application/pdf")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["document_id"] == "mock-doc-id"
    assert res_data["filename"] == "contract.pdf"
    assert res_data["pages"] == 3
    assert "mock summary" in res_data["summary"]


def test_upload_unsupported_file():
    """Test POST /upload with unsupported file extension."""
    client = TestClient(app)
    files = {"file": ("image.png", b"fake image bytes", "image/png")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_upload_corrupt_file():
    """Test POST /upload handling corrupted files gracefully."""
    client = TestClient(app)
    files = {"file": ("corrupt.pdf", b"%PDF-1.4 corrupt", "application/pdf")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "Corrupted or invalid PDF" in response.json()["detail"]


def test_chat_endpoint_happy():
    """Test POST /chat happy path."""
    client = TestClient(app)
    payload = {"document_id": "mock-doc-id", "question": "Who are contracting parties?"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    res_data = response.json()
    assert "mock answer" in res_data["answer"]
    assert len(res_data["sources"]) == 1
    assert res_data["sources"][0]["page"] == 2
    assert len(res_data["suggested_questions"]) == 2


def test_chat_endpoint_missing_doc():
    """Test POST /chat when document ID doesn't exist."""
    client = TestClient(app)
    payload = {"document_id": "invalid-doc", "question": "Who are contracting parties?"}
    response = client.post("/chat", json=payload)
    assert response.status_code == 404
    assert "Document not found" in response.json()["detail"]


def test_chat_endpoint_empty_question():
    """Test POST /chat with empty question validation."""
    client = TestClient(app)
    payload = {"document_id": "mock-doc-id", "question": "   "}
    response = client.post("/chat", json=payload)
    assert response.status_code == 400


def test_chat_stream_endpoint():
    """Test POST /chat/stream SSE endpoint."""
    client = TestClient(app)
    payload = {"document_id": "mock-doc-id", "question": "Summarize the agreement."}
    response = client.post("/chat/stream", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    
    # Parse SSE stream output
    lines = response.text.split("\n")
    events = [line for line in lines if line.startswith("event:") or line.startswith("data:")]
    
    assert "event: sources" in events[0]
    assert "event: token" in events[2]
    assert "data: This is a " in events[3]
    assert "event: follow_ups" in events[6]
    assert "event: done" in events[8]


def test_get_history_happy():
    """Test GET /history/{session_id} retrieval."""
    client = TestClient(app)
    response = client.get("/history/session-123")
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["session_id"] == "session-123"
    assert len(res_data["messages"]) == 2
    assert res_data["messages"][0]["role"] == "human"
    assert res_data["messages"][1]["role"] == "assistant"


def test_get_history_missing():
    """Test GET /history/{session_id} when session ID does not exist."""
    client = TestClient(app)
    response = client.get("/history/invalid-session")
    assert response.status_code == 404
    assert "Session not found" in response.json()["detail"]
