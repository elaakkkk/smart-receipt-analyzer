from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class ExtractedReceiptData(BaseModel):
    merchant_name: str
    purchase_date: str | None = None
    total_amount: float | None = None
    currency: str | None = "EUR"
    items: list = Field(default_factory=list)

class ValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

class ReceiptListItem(BaseModel):
    id: int
    original_filename: str
    content_type: str
    saved_path: str
    document_type: str | None 
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)  # Enable ORM mode for SQLAlchemy models

class ReceiptDetail(ReceiptListItem):
    extracted_text: str | None
    structured_data: dict | None   
    validation_result: dict | None
class DeleteReceiptResponse(BaseModel):
    receipt_id: int
    message: str