"""
Pydantic schemas for API request/response validation.

These DTOs define the contract between the API layer and
external clients. They are separate from domain models.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Upload Schemas ────────────────────────────────────────────────

class UploadResponse(BaseModel):
    """Response returned after a successful document upload."""

    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    pages: int = Field(..., description="Number of pages in the document")
    chunks: int = Field(..., description="Number of chunks created")
    summary: Optional[str] = Field(None, description="Auto-generated document summary")


# ─── Chat Schemas ──────────────────────────────────────────────────

class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    document_id: str = Field(..., description="ID of the document to query")
    question: str = Field(..., min_length=1, description="The question to ask")
    session_id: Optional[str] = Field(
        None, description="Optional session ID for conversation continuity"
    )


class SourceInfo(BaseModel):
    """Information about a source chunk used in an answer."""

    page: int = Field(..., description="Page number")
    chunk: int = Field(..., description="Chunk index")
    score: float = Field(..., description="Similarity score")
    preview: str = Field("", description="Text preview of the chunk")


class ChatResponse(BaseModel):
    """Response returned from the chat endpoint."""

    answer: str = Field(..., description="The generated answer")
    sources: list[SourceInfo] = Field(
        default_factory=list, description="Source chunks used"
    )
    suggested_questions: list[str] = Field(
        default_factory=list, description="Suggested follow-up questions"
    )
    session_id: Optional[str] = Field(
        None, description="Session ID for conversation continuity"
    )


# ─── History Schemas ───────────────────────────────────────────────

class MessageSchema(BaseModel):
    """A single message in a conversation."""

    role: str = Field(..., description="Message role (human/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="When the message was sent")


class HistoryResponse(BaseModel):
    """Response returned from the history endpoint."""

    session_id: str = Field(..., description="Session identifier")
    document_id: str = Field(..., description="Associated document ID")
    messages: list[MessageSchema] = Field(
        default_factory=list, description="Conversation messages"
    )


# ─── Error Schemas ─────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    """Standard error response."""

    detail: str = Field(..., description="Error description")
    error_code: str = Field("UNKNOWN_ERROR", description="Machine-readable error code")
