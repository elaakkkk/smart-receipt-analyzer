import pytest
from fastapi import HTTPException

from app.services.validation_service import validate_uploaded_file


class FakeUploadFile:
    def __init__(self, filename: str):
        self.filename = filename


def test_valid_png_file():
    file = FakeUploadFile("ticket.png")
    result = validate_uploaded_file(file)
    assert result == "png"


def test_valid_pdf_file():
    file = FakeUploadFile("document.pdf")
    result = validate_uploaded_file(file)
    assert result == "pdf"


def test_invalid_txt_file():
    file = FakeUploadFile("bad.txt")

    with pytest.raises(HTTPException):
        validate_uploaded_file(file)


def test_empty_filename():
    file = FakeUploadFile("")

    with pytest.raises(HTTPException):
        validate_uploaded_file(file)