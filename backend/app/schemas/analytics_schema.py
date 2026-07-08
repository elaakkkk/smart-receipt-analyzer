from pydantic import BaseModel


class AnalyticsSummaryResponse(BaseModel):
    total_receipts: int
    valid_receipts: int
    invalid_receipts: int
    unknown_documents: int
    receipt_documents: int
    invoice_documents: int

class DocumentTypesStatsResponse(BaseModel):
    unknown: int
    receipt: int
    invoice: int