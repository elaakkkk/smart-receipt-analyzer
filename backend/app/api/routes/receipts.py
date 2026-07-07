from fastapi import APIRouter, UploadFile, File

from app.services.file_service import save_uploaded_file
from app.schemas.upload_schema import UploadReceiptResponse
from app.services.validation_service import validate_uploaded_file
from app.services.ocr_service import extract_text_from_file
from app.services.classification_service import classify_document

router = APIRouter()
@router.post("/upload", response_model=UploadReceiptResponse)
async def upload_receipt(file : UploadFile = File(...)) -> UploadReceiptResponse:
    validate_uploaded_file(file)
    dest_path = await save_uploaded_file(file)
    extracted_text = extract_text_from_file(dest_path)
    document_type = classify_document(extracted_text)

    return UploadReceiptResponse(
        filename=file.filename,
        content_type=file.content_type,
        saved_path=dest_path,
        extracted_text=extracted_text,
        document_type=document_type,
        message="File uploaded and saved successfully and text extracted and classified.",
    )