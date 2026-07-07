def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a file (PDF or image).

    Args:
        file_path (str): The path to the file from which to extract text.

    Returns:
        str: The extracted text.
    """
    extension = file_path.split(".")[-1].lower()
    
    if extension == "pdf":
        return f"Text extracted from PDF file: {file_path}"
    elif extension in ["png", "jpg", "jpeg"]:
        return f"Text extracted from image file: {file_path}"
    else:
        raise ValueError("Unsupported file type. Please provide a PDF, PNG, JPG, or JPEG file.")