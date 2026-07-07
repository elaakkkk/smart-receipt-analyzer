from fastapi import HTTPException, UploadFile


def validate_uploaded_file(file: UploadFile) -> str:
    """
    Validate the uploaded file.

    Args:
        file (UploadFile): The uploaded file to be validated.

    Raises:
        HTTPException: If the file is not uploaded or has an invalid type.
    """
    allowed_extensions = ["pdf", "png", "jpg", "jpeg"]

    if file is None or file.filename == "":
        raise HTTPException(status_code=400, detail="No file uploaded. Please upload a PDF, PNG, JPG, or JPEG file.")
    
    extension = file.filename.split(".")[-1].lower()
    if extension == "":
        raise HTTPException(status_code=400, detail="File has no extension. Please upload a PDF, PNG, JPG, or JPEG file.")
    
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF, PNG, JPG, or JPEG file.")

    return extension