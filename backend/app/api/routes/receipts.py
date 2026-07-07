from fastapi import APIRouter, HTTPException, UploadFile, File

from app.services.file_service import save_uploaded_file

router = APIRouter()
@router.post("/upload")
async def upload_receipt(file : UploadFile = File(...)) -> dict[str, str]:
    allowed_extensions = ["pdf", "png", "jpg", "jpeg"]
    
    if(file is None):
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a PDF, PNG, JPG, or JPEG file.")
    if(file.filename.split(".")[-1].lower() not in allowed_extensions):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF, PNG, JPG, or JPEG file.")
    
    dest_path = await save_uploaded_file(file)
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": dest_path,
        "message": "File uploaded and saved successfully"
    }