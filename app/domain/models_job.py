# Knowledge‑Based Interview Engine Domain Models

"""
Domain models for the Evalora Knowledge‑Based Interview Engine.
These replace the previous legal‑specific models and are scoped to a *Job*.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import uuid
from typing import List, Optional, Dict


class JobStatus(str, Enum):
    """Current processing state of a Job."""
    CREATED = "created"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"
    DRAFT = "Draft"
    OPEN = "Open"
    PAUSED = "Paused"
    CLOSED = "Closed"
    FILLED = "Filled"


@dataclass
class Job:
    """A recruitment job that owns its own knowledge base."""
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    seniority: str = ""
    description: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: JobStatus = JobStatus.CREATED
    # optional fields for future extensions
    metadata: Dict[str, str] = field(default_factory=dict)
    # new fields for UI
    department: str = ""
    location: str = ""
    remote_mode: str = ""
    applicants: int = 0
    ai_screened: int = 0
    interviewing: int = 0
    skills: List[str] = field(default_factory=list)
    ai_match_score: float = 0.0
    hiring_progress: float = 0.0


@dataclass
class KnowledgeChunk:
    """A chunk of text extracted from a resource belonging to a Job."""
    chunk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str = ""
    document_id: str = ""
    content: str = ""
    page_number: int = 0
    chunk_index: int = 0
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class KnowledgeDocument:
    """A resource uploaded for a specific Job."""
    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str = ""
    filename: str = ""
    page_count: int = 0
    chunk_count: int = 0
    upload_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    summary: Optional[str] = None


@dataclass
class InterviewQuestion:
    question_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    interview_id: str = ""
    content: str = ""


@dataclass
class Interview:
    interview_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    questions: List[InterviewQuestion] = field(default_factory=list)


@dataclass
class EvaluationResult:
    """Result of evaluating a candidate answer against the knowledge base."""
    score: float = 0.0
    feedback: str = ""
    sources: List[KnowledgeChunk] = field(default_factory=list)

