import datetime

from app.schemas.receipt_schema import ExtractedReceiptData

def extract_structured_data(extracted_text: str, document_type: str) -> ExtractedReceiptData:
    """
    Extract structured data from the extracted text of a receipt.

    Args:
        extracted_text (str): The text extracted from the receipt.
        document_type (str): The type of the document.

    Returns:
        ExtractedReceiptData: An instance of ExtractedReceiptData containing the structured data.
    """
    if document_type == "receipt":
        structured_data = {
            "merchant_name": "Unknown merchant",
            "total_amount": None,
            "purchase_date": datetime.now().strftime("%Y-%m-%d"),
            "currency": "EUR",
            "items": []
        }
    else :
        structured_data = {
            "merchant_name": "Unknown merchant",
            "total_amount": None,
            "purchase_date": None,
            "currency": "EUR",
            "items": []
        }
    return ExtractedReceiptData(**structured_data)