# app/services/job_service.py
"""
Simple in‑memory Job service.
In a production system this would be backed by a database, but for now we keep
everything in process to avoid external dependencies.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

from app.domain.models_job import Job, JobStatus, KnowledgeDocument


@dataclass
class JobRecord:
    job: Job
    documents: List[KnowledgeDocument] = field(default_factory=list)


# Pre-populate sample jobs for beautiful UI display
_sample_jobs = [
    Job(
        job_id="devops-engineer-cairo",
        title="DevOps Engineer",
        seniority="Senior",
        description="We are looking for a DevOps Engineer to design, deploy, and maintain our cloud infrastructure, CI/CD pipelines, and Kubernetes clusters.",
        status=JobStatus.OPEN,
        created_at=datetime.now(timezone.utc) - timedelta(days=2),
        department="Technology Department",
        location="Cairo",
        remote_mode="Hybrid",
        applicants=148,
        ai_screened=102,
        interviewing=18,
        skills=["Docker", "Kubernetes", "AWS", "Terraform", "Python", "CI/CD", "Bash"],
        ai_match_score=84.0,
        hiring_progress=63.0,
    ),
    Job(
        job_id="senior-ai-engineer-cairo",
        title="Senior AI Engineer",
        seniority="Senior",
        description="We are looking for a Senior AI Engineer to join our team to build next-generation Agentic AI pipelines using LangGraph and MCP.",
        status=JobStatus.OPEN,
        created_at=datetime.now(timezone.utc) - timedelta(days=4),
        department="Technology Consulting",
        location="Cairo",
        remote_mode="Hybrid",
        applicants=142,
        ai_screened=24,
        interviewing=8,
        skills=["Python", "LangGraph", "Azure", "MCP", "RAG"],
        ai_match_score=92.0,
        hiring_progress=65.0,
    ),
    Job(
        job_id="lead-fullstack-developer",
        title="Lead Fullstack Developer",
        seniority="Lead",
        description="Seeking a Lead Fullstack Developer experienced in React, Node.js, and Cloud architectures to drive frontend and backend systems.",
        status=JobStatus.READY,
        created_at=datetime.now(timezone.utc) - timedelta(days=7),
        department="Product Engineering",
        location="Remote",
        remote_mode="Remote",
        applicants=89,
        ai_screened=15,
        interviewing=4,
        skills=["React", "Node.js", "TypeScript", "AWS", "Docker"],
        ai_match_score=88.0,
        hiring_progress=40.0,
    )
]


class JobService:
    """Service for creating and managing Jobs.

    It stores jobs in a module‑level dictionary ``_jobs`` keyed by ``job_id``.
    The service provides methods to create a job, retrieve it, and associate
    uploaded ``KnowledgeDocument`` objects with a job.
    """

    _jobs: Dict[str, JobRecord] = {
        j.job_id: JobRecord(job=j) for j in _sample_jobs
    }

    def create_job(
        self,
        title: str,
        seniority: str,
        description: str,
        department: str = "",
        location: str = "",
        remote_mode: str = "",
        applicants: int = 0,
        ai_screened: int = 0,
        interviewing: int = 0,
        skills: List[str] = None,
        ai_match_score: float = 0.0,
        hiring_progress: float = 0.0,
    ) -> Job:
        if skills is None:
            skills = []
        job = Job(
            title=title,
            seniority=seniority,
            description=description,
            status=JobStatus.CREATED,
            department=department,
            location=location,
            remote_mode=remote_mode,
            applicants=applicants,
            ai_screened=ai_screened,
            interviewing=interviewing,
            skills=skills,
            ai_match_score=ai_match_score,
            hiring_progress=hiring_progress,
        )
        self._jobs[job.job_id] = JobRecord(job=job)
        return job

    def get_job(self, job_id: str) -> Optional[JobRecord]:
        return self._jobs.get(job_id)

    def add_document(self, job_id: str, document: KnowledgeDocument) -> None:
        record = self.get_job(job_id)
        if not record:
            raise ValueError(f"Job {job_id} not found")
        record.documents.append(document)
        # Update job status if needed
        record.job.status = JobStatus.UPLOADING

    def set_job_ready(self, job_id: str) -> None:
        record = self.get_job(job_id)
        if record:
            record.job.status = JobStatus.READY

    def list_jobs(self) -> List[Job]:
        return [record.job for record in self._jobs.values()]
