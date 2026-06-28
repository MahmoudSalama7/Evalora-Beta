"""
Abstract document parser interface.

Defines the contract that all document parsers (PDF, DOCX, etc.)
must implement. Used by the Factory Pattern to select the
appropriate parser at runtime.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class DocumentParser(ABC):
    """
    Abstract base class for document parsers.

    All concrete parsers must implement the `parse` method to extract
    text content from a document file, returning a list of tuples
    containing (page_number, text_content).
    """

    @abstractmethod
    def parse(self, file_path: Path) -> list[tuple[int, str]]:
        """
        Parse a document and extract text content.

        Args:
            file_path: Path to the document file.

        Returns:
            A list of tuples where each tuple contains:
                - page_number (int): 1-indexed page number.
                - text_content (str): Extracted text from that page.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or corrupted.
        """
        ...

    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """
        Return the file extensions supported by this parser.

        Returns:
            A list of lowercase file extensions (e.g., ['.pdf']).
        """
        ...
