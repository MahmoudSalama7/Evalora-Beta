from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List

from app.api.dependencies import get_job_service, get_document_service
from app.api.schemas import (
    JobCreateRequest,
    JobResponse,
    JobListResponse,
    UploadResponse,
    ErrorResponse,
)
from app.services.job_service import JobService
from app.services.document_service import DocumentService

router = APIRouter(tags=["Jobs"])

@router.get("/jobs/", response_model=JobListResponse, responses={200: {"description": "List jobs"}})
async def list_jobs(job_service: JobService = Depends(get_job_service)):
    jobs = job_service.list_jobs()
    job_responses: List[JobResponse] = []
    for job in jobs:
        job_responses.append(
            JobResponse(
                job_id=job.job_id,
                title=job.title,
                seniority=job.seniority,
                description=job.description,
                status=job.status,
                created_at=job.created_at.isoformat(),
            )
        )
    return JobListResponse(jobs=job_responses)

@router.post(
    "/jobs/",
    response_model=JobResponse,
    status_code=201,
    responses={
        201: {"description": "Job created"},
        400: {"model": ErrorResponse, "description": "Bad request"},
    },
)
async def create_job(
    payload: JobCreateRequest,
    job_service: JobService = Depends(get_job_service),
):
    if not payload.title or not payload.seniority or not payload.description:
        raise HTTPException(status_code=400, detail="Missing required fields")
    job = job_service.create_job(
        title=payload.title, seniority=payload.seniority, description=payload.description
    )
    return JobResponse(
        job_id=job.job_id,
        title=job.title,
        seniority=job.seniority,
        description=job.description,
        status=job.status,
        created_at=job.created_at.isoformat(),
    )

@router.post(
    "/jobs/{job_id}/upload",
    response_model=UploadResponse,
    responses={
        200: {"description": "Resources uploaded"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        404: {"model": ErrorResponse, "description": "Job not found"},
    },
)
async def upload_job_resources(
    job_id: str,
    files: List[UploadFile] = File(...),
    job_service: JobService = Depends(get_job_service),
    document_service: DocumentService = Depends(get_document_service),
):
    # Ensure job exists
    job_record = job_service.get_job(job_id)
    if not job_record:
        raise HTTPException(status_code=404, detail="Job not found")
    # Process each uploaded file
    uploaded_documents = []
    for file in files:
        content = await file.read()
        doc = await document_service.upload(filename=file.filename, file_content=content)
        job_service.add_document(job_id, doc)
        uploaded_documents.append(doc)
    # Return last uploaded document info (or first if multiple)
    # For simplicity, return info of the first uploaded document
    if not uploaded_documents:
        raise HTTPException(status_code=400, detail="No files uploaded")
    doc = uploaded_documents[0]
    return UploadResponse(
        document_id=doc.document_id,
        filename=doc.filename,
        pages=doc.page_count,
        chunks=doc.chunk_count,
        summary=doc.summary,
    )
