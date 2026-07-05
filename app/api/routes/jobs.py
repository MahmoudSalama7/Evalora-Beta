from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List

from app.api.dependencies import get_job_service, get_document_service, get_llm_provider
from app.api.schemas import (
    JobCreateRequest,
    JobResponse,
    JobListResponse,
    UploadResponse,
    ErrorResponse,
)
from app.services.job_service import JobService
from app.services.document_service import DocumentService
from app.domain.interfaces.llm_provider import LLMProvider
import logging

logger = logging.getLogger(__name__)

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
                department=job.department,
                location=job.location,
                remote_mode=job.remote_mode,
                applicants=job.applicants,
                ai_screened=job.ai_screened,
                interviewing=job.interviewing,
                skills=job.skills,
                ai_match_score=job.ai_match_score,
                hiring_progress=job.hiring_progress,
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
    llm_provider: LLMProvider = Depends(get_llm_provider),
):
    if not payload.title or not payload.seniority or not payload.description:
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Extract skills using LLM from job description
    extracted_skills = []
    try:
        system_prompt = (
            "You are an expert HR assistant. Your task is to extract a list of professional skills, "
            "technologies, programming languages, tools, or methodologies from the job title and description. "
            "Return ONLY a clean comma-separated list of skills (e.g. Python, Docker, Kubernetes, React). "
            "Do not include any explanation, conversational text, introduction, or list numbering. "
            "Limit to at most 10 of the most relevant skills."
        )
        user_prompt = f"Job Title: {payload.title}\nJob Description: {payload.description}"
        llm_response = await llm_provider.generate(
            prompt=user_prompt,
            system_message=system_prompt,
        )
        if llm_response:
            # Parse skills: split by comma, strip whitespace, remove empty ones
            extracted_skills = [
                s.strip()
                for s in llm_response.split(",")
                if s.strip()
            ]
    except Exception as exc:
        # Gracefully handle extraction failures so job creation still succeeds
        logger.warning(f"LLM skill extraction failed: {exc}")

    # Merge manually provided skills with LLM-extracted ones (preserving order, removing duplicates)
    final_skills = list(payload.skills) if payload.skills else []
    seen = set(s.lower() for s in final_skills)
    for skill in extracted_skills:
        if skill.lower() not in seen:
            final_skills.append(skill)
            seen.add(skill.lower())

    job = job_service.create_job(
        title=payload.title,
        seniority=payload.seniority,
        description=payload.description,
        department=payload.department,
        location=payload.location,
        remote_mode=payload.remote_mode,
        applicants=payload.applicants,
        ai_screened=payload.ai_screened,
        interviewing=payload.interviewing,
        skills=final_skills,
        ai_match_score=payload.ai_match_score,
        hiring_progress=payload.hiring_progress,
    )
    return JobResponse(
        job_id=job.job_id,
        title=job.title,
        seniority=job.seniority,
        description=job.description,
        status=job.status,
        created_at=job.created_at.isoformat(),
        department=job.department,
        location=job.location,
        remote_mode=job.remote_mode,
        applicants=job.applicants,
        ai_screened=job.ai_screened,
        interviewing=job.interviewing,
        skills=job.skills,
        ai_match_score=job.ai_match_score,
        hiring_progress=job.hiring_progress,
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
        doc = await document_service.upload(
            filename=file.filename,
            file_content=content,
            job_id=job_id
        )
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


@router.get(
    "/jobs/{job_id}/documents",
    response_model=List[UploadResponse],
    responses={
        200: {"description": "List of resources for the job"},
        404: {"model": ErrorResponse, "description": "Job not found"},
    },
)
async def list_job_documents(
    job_id: str,
    job_service: JobService = Depends(get_job_service),
):
    record = job_service.get_job(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="Job not found")
    return [
        UploadResponse(
            document_id=doc.document_id,
            filename=doc.filename,
            pages=doc.page_count,
            chunks=doc.chunk_count,
            summary=doc.summary,
        )
        for doc in record.documents
    ]

