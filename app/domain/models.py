"""
Domain models for the QA Assistant.

These are pure Python data classes that represent the core business
entities. They have no dependencies on frameworks or infrastructure.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
import uuid


class MessageRole(str, Enum):
    """Role of a message in a conversation."""
    HUMAN = "human"
    ASSISTANT = "assistant"


@dataclass
class Chunk:
    """
    A chunk of text extracted from a document.

    Attributes:
        chunk_id: Unique identifier for this chunk.
        document_id: ID of the parent document.
        content: The text content of the chunk.
        page_number: The page number this chunk originated from.
        chunk_index: Sequential index of this chunk within the document.
        metadata: Additional metadata about the chunk.
    """
    chunk_id: str
    document_id: str
    content: str
    page_number: int
    chunk_index: int
    metadata: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.chunk_id:
            self.chunk_id = str(uuid.uuid4())


@dataclass
class Document:
    """
    Represents an uploaded document.

    Attributes:
        document_id: Unique identifier for this document.
        filename: Original filename of the uploaded document.
        page_count: Number of pages in the document.
        chunk_count: Number of chunks generated from the document.
        upload_time: Timestamp when the document was uploaded.
        summary: Auto-generated summary of the document.
    """
    document_id: str
    filename: str
    page_count: int = 0
    chunk_count: int = 0
    upload_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    summary: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.document_id:
            self.document_id = str(uuid.uuid4())


@dataclass
class Message:
    """
    A single message in a conversation.

    Attributes:
        role: The role of the message sender (human or assistant).
        content: The text content of the message.
        timestamp: When the message was created.
    """
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Conversation:
    """
    A conversation session linked to a document.

    Attributes:
        session_id: Unique identifier for this conversation.
        document_id: ID of the document being discussed.
        messages: Ordered list of messages in the conversation.
        created_at: When the conversation was started.
    """
    session_id: str
    document_id: str
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class RetrievalResult:
    """
    A chunk retrieved from the vector store with its similarity score.

    Attributes:
        chunk: The retrieved text chunk.
        score: Similarity score (lower is more similar for L2 distance).
    """
    chunk: Chunk
    score: float


@dataclass
class AnswerResult:
    """
    The result of a question-answering operation.

    Attributes:
        answer: The generated answer text.
        sources: List of source chunks used to generate the answer.
        suggested_questions: Follow-up questions the user might ask.
    """
    answer: str
    sources: list[RetrievalResult] = field(default_factory=list)
    suggested_questions: list[str] = field(default_factory=list)
