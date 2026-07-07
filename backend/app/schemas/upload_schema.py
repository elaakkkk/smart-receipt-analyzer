from pydantic import BaseModel


class UploadReceiptResponse(BaseModel):
    """
    Response model for the upload receipt endpoint.
    """
    filename: str
    content_type: str
    saved_path: str
    message: str