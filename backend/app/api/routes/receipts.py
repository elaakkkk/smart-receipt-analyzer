from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.repositories.receipt_repository import create_receipt,get_receipts 

from app.services.file_service import save_uploaded_file
from app.schemas.upload_schema import UploadReceiptResponse
from app.services.validation_service import validate_uploaded_file
from app.services.ocr_service import extract_text_from_file
from app.services.classification_service import classify_document
from app.services.extraction_service import extract_structured_data
from app.services.business_validation_service import validate_extracted_data
from app.schemas.receipt_schema import ReceiptListItem

router = APIRouter()
@router.post("/upload", response_model=UploadReceiptResponse)
async def upload_receipt(file : UploadFile = File(...), db: Session = Depends(get_db)) -> UploadReceiptResponse:
    validate_uploaded_file(file)
    dest_path = await save_uploaded_file(file)
    extracted_text = extract_text_from_file(dest_path)
    document_type = classify_document(extracted_text)
    structured_data = extract_structured_data(extracted_text, document_type)
    validation_result = validate_extracted_data(structured_data)
    created_receipt = create_receipt(
        db=db,
        original_filename=file.filename,
        content_type=file.content_type,
        saved_path=dest_path,
        extracted_text=extracted_text,
        document_type=document_type,
        structured_data=structured_data.model_dump(),
        validation_result=validation_result.model_dump()
    )

    return UploadReceiptResponse(
        receipt_id=created_receipt.id,
        filename=file.filename,
        content_type=file.content_type,
        saved_path=dest_path,
        extracted_text=extracted_text,
        document_type=document_type,
        structured_data=structured_data,
        validation_result=validation_result,
        message="File uploaded, processed, structured, validated and saved successfully.",
    )

@router.get("/", response_model=list[ReceiptListItem])
def list_receipts(db: Session = Depends(get_db), limit: int = 50):
    """
    Retrieve a list of receipts from the database.
    """
    receipts = get_receipts(db, limit=limit)
    return receipts