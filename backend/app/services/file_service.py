import os
from uuid import UUID

from fastapi import UploadFile

async def save_uploaded_file(file: UploadFile) -> str:
    """
    Save an uploaded file to the 'uploads' directory.

    Args:
        file (UploadFile): The uploaded file to be saved.

    Returns:
        str: The path where the file was saved.
    """
    # Create the 'uploads' directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    uuid = UUID()

    # Define the destination path for the uploaded file
    dest_path = os.path.join("uploads", f"{uuid.uuid4()}-{file.filename}")

    # Save the uploaded file to the destination path
    with open(dest_path, "wb") as f:
        f.write(await file.read())

    return dest_path