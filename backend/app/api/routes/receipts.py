from fastapi import APIRouter, UploadFile, File

from app.services.file_service import save_uploaded_file
from app.schemas.upload_schema import UploadReceiptResponse
from app.services.validation_service import validate_uploaded_file

router = APIRouter()
@router.post("/upload", response_model=UploadReceiptResponse)
async def upload_receipt(file : UploadFile = File(...)) -> UploadReceiptResponse:
    validate_uploaded_file(file)
    dest_path = await save_uploaded_file(file)
    
    return UploadReceiptResponse(
        filename=file.filename,
        content_type=file.content_type,
        saved_path=dest_path,
        message="File uploaded and saved successfully"
    )