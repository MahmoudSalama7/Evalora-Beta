"""
Plain text and Markdown document parser implementation.
"""

import logging
import math
from pathlib import Path

from app.domain.interfaces.parser import DocumentParser

logger = logging.getLogger(__name__)

CHARS_PER_PAGE = 3000

class TXTParser(DocumentParser):
    """
    Concrete parser for TXT and MD documents.
    """

    def parse(self, file_path: Path) -> list[tuple[int, str]]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.stat().st_size == 0:
            raise ValueError(f"File is empty: {file_path}")

        try:
            full_text = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        except Exception as exc:
            logger.error(f"Failed to read file: {file_path}, error: {exc}")
            raise ValueError(f"Invalid file format: {file_path}") from exc

        if not full_text:
            raise ValueError(f"File contains no extractable text: {file_path}")

        total_chars = len(full_text)
        estimated_pages = max(1, math.ceil(total_chars / CHARS_PER_PAGE))
        chars_per_estimated_page = math.ceil(total_chars / estimated_pages)

        pages: list[tuple[int, str]] = []
        for current_page in range(1, estimated_pages + 1):
            start = (current_page - 1) * chars_per_estimated_page
            end = current_page * chars_per_estimated_page
            page_text = full_text[start:end].strip()
            if page_text:
                pages.append((current_page, page_text))

        logger.info(f"Parsed file: {file_path.name}, ~{len(pages)} pages")
        return pages

    def supported_extensions(self) -> list[str]:
        return [".txt", ".md"]
