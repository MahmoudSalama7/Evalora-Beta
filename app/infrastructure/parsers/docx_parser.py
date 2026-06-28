"""
DOCX document parser implementation.

Uses python-docx to extract text content from Word documents,
mapping paragraphs to approximate pages.
"""

import logging
import math
from pathlib import Path

from docx import Document as DocxDocument
from docx.opc.exceptions import PackageNotFoundError

from app.domain.interfaces.parser import DocumentParser

logger = logging.getLogger(__name__)

# Average characters per page for page estimation
CHARS_PER_PAGE = 3000


class DOCXParser(DocumentParser):
    """
    Concrete parser for DOCX documents.

    Extracts text from Word documents paragraph-by-paragraph,
    estimating page boundaries based on character count.
    """

    def parse(self, file_path: Path) -> list[tuple[int, str]]:
        """
        Parse a DOCX file and extract text with page estimates.

        Args:
            file_path: Path to the DOCX file.

        Returns:
            List of (page_number, text_content) tuples.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the DOCX is empty or corrupted.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"DOCX file not found: {file_path}")

        if file_path.stat().st_size == 0:
            raise ValueError(f"DOCX file is empty: {file_path}")

        try:
            doc = DocxDocument(str(file_path))
        except PackageNotFoundError as exc:
            logger.error(f"Failed to open DOCX: {file_path}, error: {exc}")
            raise ValueError(
                f"Corrupted or invalid DOCX file: {file_path}"
            ) from exc
        except Exception as exc:
            logger.error(f"Failed to open DOCX: {file_path}, error: {exc}")
            raise ValueError(
                f"Corrupted or invalid DOCX file: {file_path}"
            ) from exc

        # Collect all paragraph text
        all_text = []
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                all_text.append(text)

        if not all_text:
            raise ValueError(
                f"DOCX contains no extractable text: {file_path}"
            )

        # Group paragraphs into estimated pages
        full_text = "\n".join(all_text)
        total_chars = len(full_text)
        estimated_pages = max(1, math.ceil(total_chars / CHARS_PER_PAGE))

        pages: list[tuple[int, str]] = []
        chars_per_estimated_page = math.ceil(total_chars / estimated_pages)

        current_page = 1
        current_text: list[str] = []
        current_char_count = 0

        for paragraph_text in all_text:
            current_text.append(paragraph_text)
            current_char_count += len(paragraph_text)

            if current_char_count >= chars_per_estimated_page:
                pages.append((current_page, "\n".join(current_text)))
                current_page += 1
                current_text = []
                current_char_count = 0

        # Add remaining text
        if current_text:
            pages.append((current_page, "\n".join(current_text)))

        logger.info(
            f"Parsed DOCX: {file_path.name}, "
            f"~{estimated_pages} estimated pages, "
            f"{len(all_text)} paragraphs"
        )

        return pages

    def supported_extensions(self) -> list[str]:
        """Return supported file extensions."""
        return [".docx"]
