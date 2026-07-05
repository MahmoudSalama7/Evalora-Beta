"""
Document service.

Orchestrates the document upload pipeline: file saving, parsing,
chunking, embedding, indexing, and auto-summarization.
"""

import logging
import os
import uuid
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import Settings
from app.domain.interfaces.llm_provider import LLMProvider
from app.domain.models import Chunk, Document
from app.infrastructure.parsers.parser_factory import ParserFactory
from app.services.embedding_service import EmbeddingService
from app.services.prompt_service import PromptService
from app.services.vector_store_service import VectorStoreService

logger = logging.getLogger(__name__)


class DocumentService:
    """
    Service for document upload and processing.

    Orchestrates the complete document ingestion pipeline:
    1. Save uploaded file to disk
    2. Parse text content (PDF/DOCX)
    3. Split into chunks with overlap
    4. Generate embeddings
    5. Index in vector store
    6. Generate auto-summary

    Args:
        settings: Application configuration.
        embedding_service: Service for generating embeddings.
        vector_store_service: Service for vector storage.
        llm_provider: LLM for generating document summaries.
        prompt_service: Service for building prompts.
    """

    def __init__(
        self,
        settings: Settings,
        embedding_service: EmbeddingService,
        vector_store_service: VectorStoreService,
        llm_provider: LLMProvider,
        prompt_service: PromptService,
    ) -> None:
        self._settings = settings
        self._embedding_service = embedding_service
        self._vector_store_service = vector_store_service
        self._llm_provider = llm_provider
        self._prompt_service = prompt_service
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        # Ensure upload directory exists
        os.makedirs(settings.upload_dir, exist_ok=True)

    async def upload(
        self,
        filename: str,
        file_content: bytes,
        job_id: str | None = None,
    ) -> Document:
        """
        Process and index an uploaded document.

        Args:
            filename: Original filename.
            file_content: Raw file bytes.
            job_id: Optional parent job ID to also index against for job-level RAG.

        Returns:
            Document object with metadata and auto-summary.

        Raises:
            ValueError: If the file is empty or unsupported.
        """
        if not file_content:
            raise ValueError("File is empty")

        document_id = str(uuid.uuid4())
        logger.info(
            f"Processing upload: {filename}, doc_id={document_id}",
            extra={"document_id": document_id},
        )

        # Step 1: Save file to disk
        file_path = self._save_file(document_id, filename, file_content)

        # Step 2: Parse document
        parser = ParserFactory.get_parser(filename)
        pages = parser.parse(file_path)
        page_count = len(pages)

        logger.info(
            f"Parsed {page_count} pages from {filename}",
            extra={"document_id": document_id},
        )

        # Step 3: Chunk the text
        chunks = self._create_chunks(document_id, pages)

        logger.info(
            f"Created {len(chunks)} chunks",
            extra={"document_id": document_id},
        )

        # Step 4: Generate embeddings
        chunk_texts = [chunk.content for chunk in chunks]
        embeddings = self._embedding_service.embed_chunks(chunk_texts)

        # Step 5: Index in vector store
        self._vector_store_service.index_document(
            document_id, chunks, embeddings
        )
        if job_id:
            # Also index under the job_id for unified RAG retrieve
            self._vector_store_service.index_document(
                job_id, chunks, embeddings
            )

        # Step 6: Generate auto-summary
        summary = await self._generate_summary(pages)

        document = Document(
            document_id=document_id,
            filename=filename,
            page_count=page_count,
            chunk_count=len(chunks),
            summary=summary,
        )

        logger.info(
            f"Upload complete: {filename}, "
            f"{page_count} pages, {len(chunks)} chunks",
            extra={"document_id": document_id},
        )

        return document

    def _save_file(
        self,
        document_id: str,
        filename: str,
        content: bytes,
    ) -> Path:
        """Save uploaded file to the upload directory."""
        # Create document-specific subdirectory
        doc_dir = Path(self._settings.upload_dir) / document_id
        os.makedirs(doc_dir, exist_ok=True)

        file_path = doc_dir / filename
        file_path.write_bytes(content)

        logger.debug(f"Saved file: {file_path}")
        return file_path

    def _create_chunks(
        self,
        document_id: str,
        pages: list[tuple[int, str]],
    ) -> list[Chunk]:
        """
        Split parsed pages into overlapping chunks.

        Preserves page metadata for each chunk.
        """
        chunks: list[Chunk] = []
        chunk_index = 0

        for page_number, page_text in pages:
            # Split page text into chunks
            page_chunks = self._text_splitter.split_text(page_text)

            for chunk_text in page_chunks:
                chunk = Chunk(
                    chunk_id=str(uuid.uuid4()),
                    document_id=document_id,
                    content=chunk_text,
                    page_number=page_number,
                    chunk_index=chunk_index,
                    metadata={
                        "page": page_number,
                        "chunk": chunk_index,
                    },
                )
                chunks.append(chunk)
                chunk_index += 1

        return chunks

    async def _generate_summary(
        self,
        pages: list[tuple[int, str]],
    ) -> str:
        """Generate an auto-summary of the document."""
        try:
            # Combine first few pages for summary
            combined_text = "\n\n".join(
                text for _, text in pages[:5]
            )

            system_msg, user_prompt = self._prompt_service.build_summary_prompt(
                combined_text
            )
            summary = await self._llm_provider.generate(
                prompt=user_prompt,
                system_message=system_msg,
            )
            return summary.strip()

        except Exception as exc:
            logger.warning(f"Failed to generate summary: {exc}")
            return "Summary generation failed. You can still ask questions about this document."
