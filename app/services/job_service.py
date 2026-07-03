# app/services/job_service.py
"""
Simple in‑memory Job service.
In a production system this would be backed by a database, but for now we keep
everything in process to avoid external dependencies.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.domain.models_job import Job, JobStatus, KnowledgeDocument


@dataclass
class JobRecord:
    job: Job
    documents: List[KnowledgeDocument] = field(default_factory=list)


class JobService:
    """Service for creating and managing Jobs.

    It stores jobs in a module‑level dictionary ``_jobs`` keyed by ``job_id``.
    The service provides methods to create a job, retrieve it, and associate
    uploaded ``KnowledgeDocument`` objects with a job.
    """

    _jobs: Dict[str, JobRecord] = {}

    def create_job(self, title: str, seniority: str, description: str) -> Job:
        job = Job(title=title, seniority=seniority, description=description, status=JobStatus.CREATED)
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
