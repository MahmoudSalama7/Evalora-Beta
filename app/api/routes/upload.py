"""
Upload API route.

Handles document file uploads, delegating all business
logic to the DocumentService.
"""

import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.dependencies import get_document_service
from app.api.schemas import ErrorResponse, UploadResponse
from app.infrastructure.parsers.parser_factory import (
    ParserFactory,
    UnsupportedFileTypeError,
)
from app.services.document_service import DocumentService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Documents"])


@router.post(
    "/upload",
    response_model=UploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
    summary="Upload a document",
    description="Upload a PDF or DOCX file for question answering.",
)
async def upload_document(
    file: UploadFile = File(..., description="PDF or DOCX file to upload"),
    document_service: DocumentService = Depends(get_document_service),
) -> UploadResponse:
    """
    Upload and process a document file.

    Accepts PDF and DOCX files. The document is parsed, chunked,
    embedded, indexed, and an auto-summary is generated.

    Returns a unique document_id for subsequent queries.
    """
    # Validate filename exists
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    # Validate file extension
    try:
        ParserFactory.get_parser(file.filename)
    except UnsupportedFileTypeError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    # Read file content
    content = await file.read()
    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    # Process upload
    try:
        document = await document_service.upload(
            filename=file.filename,
            file_content=content,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.error(f"Upload failed: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the document.",
        )

    return UploadResponse(
        document_id=document.document_id,
        filename=document.filename,
        pages=document.page_count,
        chunks=document.chunk_count,
        summary=document.summary,
    )
