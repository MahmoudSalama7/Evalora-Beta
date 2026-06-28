"""
Parser factory for document parsing.

Implements the Factory Pattern to automatically select the
appropriate parser based on the file extension.
"""

import logging
from pathlib import Path

from app.domain.interfaces.parser import DocumentParser
from app.infrastructure.parsers.docx_parser import DOCXParser
from app.infrastructure.parsers.pdf_parser import PDFParser

logger = logging.getLogger(__name__)


class UnsupportedFileTypeError(ValueError):
    """Raised when a file type is not supported by any parser."""

    def __init__(self, extension: str) -> None:
        self.extension = extension
        super().__init__(
            f"Unsupported file type: '{extension}'. "
            f"Supported types: .pdf, .docx"
        )


class ParserFactory:
    """
    Factory for creating document parsers.

    Automatically selects the correct parser implementation
    based on the file extension. Follows the Factory Pattern.

    Usage:
        parser = ParserFactory.get_parser("document.pdf")
        pages = parser.parse(Path("document.pdf"))
    """

    _parsers: dict[str, DocumentParser] = {
        ".pdf": PDFParser(),
        ".docx": DOCXParser(),
    }

    @classmethod
    def get_parser(cls, filename: str) -> DocumentParser:
        """
        Get the appropriate parser for a given filename.

        Args:
            filename: The name of the file to parse.

        Returns:
            A DocumentParser instance for the file type.

        Raises:
            UnsupportedFileTypeError: If the file extension is not supported.
        """
        extension = Path(filename).suffix.lower()

        parser = cls._parsers.get(extension)
        if parser is None:
            logger.warning(f"Unsupported file type requested: {extension}")
            raise UnsupportedFileTypeError(extension)

        logger.debug(f"Selected parser for '{extension}': {type(parser).__name__}")
        return parser

    @classmethod
    def supported_extensions(cls) -> list[str]:
        """
        Get all supported file extensions.

        Returns:
            List of supported file extensions.
        """
        return list(cls._parsers.keys())

    @classmethod
    def register_parser(cls, extension: str, parser: DocumentParser) -> None:
        """
        Register a new parser for a file extension.

        Enables extensibility — new parsers can be added
        without modifying existing code.

        Args:
            extension: The file extension (e.g., '.txt').
            parser: The parser instance to register.
        """
        cls._parsers[extension.lower()] = parser
        logger.info(f"Registered parser for '{extension}': {type(parser).__name__}")
