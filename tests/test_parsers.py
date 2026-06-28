"""
Unit tests for parsers and the ParserFactory.
"""

from pathlib import Path
import pytest

from app.infrastructure.parsers.parser_factory import ParserFactory, UnsupportedFileTypeError
from app.infrastructure.parsers.pdf_parser import PDFParser
from app.infrastructure.parsers.docx_parser import DOCXParser


def test_parser_factory_resolution():
    """Test that the factory returns correct parsers based on extension."""
    pdf_parser = ParserFactory.get_parser("document.pdf")
    assert isinstance(pdf_parser, PDFParser)
    assert ".pdf" in pdf_parser.supported_extensions()

    docx_parser = ParserFactory.get_parser("contract.DOCX")
    assert isinstance(docx_parser, DOCXParser)
    assert ".docx" in docx_parser.supported_extensions()


def test_parser_factory_unsupported():
    """Test factory raising UnsupportedFileTypeError for unknown formats."""
    with pytest.raises(UnsupportedFileTypeError) as exc:
        ParserFactory.get_parser("image.png")
    assert "Unsupported file type: '.png'" in str(exc.value)


def test_pdf_parser_missing_file():
    """Test PDFParser raising FileNotFoundError for missing files."""
    parser = PDFParser()
    with pytest.raises(FileNotFoundError):
        parser.parse(Path("non_existent_file.pdf"))


def test_docx_parser_missing_file():
    """Test DOCXParser raising FileNotFoundError for missing files."""
    parser = DOCXParser()
    with pytest.raises(FileNotFoundError):
        parser.parse(Path("non_existent_file.docx"))


def test_custom_parser_registration():
    """Test that new parsers can be dynamically registered in the factory."""
    from app.domain.interfaces.parser import DocumentParser

    class TextParser(DocumentParser):
        def parse(self, file_path: Path) -> list[tuple[int, str]]:
            return [(1, file_path.read_text())]
        def supported_extensions(self) -> list[str]:
            return [".txt"]

    ParserFactory.register_parser(".txt", TextParser())
    
    assert ".txt" in ParserFactory.supported_extensions()
    txt_parser = ParserFactory.get_parser("notes.txt")
    assert isinstance(txt_parser, TextParser)
