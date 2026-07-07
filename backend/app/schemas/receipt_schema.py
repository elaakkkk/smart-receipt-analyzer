from pydantic import BaseModel, Field


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