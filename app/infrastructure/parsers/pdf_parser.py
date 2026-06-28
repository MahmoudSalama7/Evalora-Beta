"""
PDF document parser implementation.

Uses PyMuPDF (fitz) to extract text content from PDF files,
preserving page-level metadata.
"""

import logging
from pathlib import Path

import fitz  # PyMuPDF

from app.domain.interfaces.parser import DocumentParser

logger = logging.getLogger(__name__)


class PDFParser(DocumentParser):
    """
    Concrete parser for PDF documents.

    Extracts text page-by-page using PyMuPDF, with robust
    error handling for corrupted or empty files.
    """

    def parse(self, file_path: Path) -> list[tuple[int, str]]:
        """
        Parse a PDF file and extract text by page.

        Args:
            file_path: Path to the PDF file.

        Returns:
            List of (page_number, text_content) tuples.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the PDF is empty or corrupted.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        if file_path.stat().st_size == 0:
            raise ValueError(f"PDF file is empty: {file_path}")

        try:
            doc = fitz.open(str(file_path))
        except Exception as exc:
            logger.error(f"Failed to open PDF: {file_path}, error: {exc}")
            raise ValueError(f"Corrupted or invalid PDF file: {file_path}") from exc

        pages: list[tuple[int, str]] = []

        try:
            if doc.page_count == 0:
                raise ValueError(f"PDF contains no pages: {file_path}")

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                text = page.get_text("text").strip()
                if text:
                    pages.append((page_num + 1, text))  # 1-indexed

            if not pages:
                raise ValueError(
                    f"PDF contains no extractable text: {file_path}"
                )

            logger.info(
                f"Parsed PDF: {file_path.name}, "
                f"{doc.page_count} pages, {len(pages)} with text"
            )
        finally:
            doc.close()

        return pages

    def supported_extensions(self) -> list[str]:
        """Return supported file extensions."""
        return [".pdf"]
