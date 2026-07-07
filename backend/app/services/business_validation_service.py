from app.schemas.receipt_schema import ExtractedReceiptData, ValidationResult


def validate_extracted_data(structured_data: ExtractedReceiptData) -> ValidationResult:
    """
    Validate the extracted structured data.

    Args:
        structured_data (ExtractedReceiptData): The extracted structured data to be validated.

    Returns:
        ValidationResult: The result of the validation.
    """
    errors = []
    warnings = []

    if not structured_data.merchant_name:
        errors.append("Merchant name is missing or invalid.")

    if structured_data.total_amount is None:
        warnings.append("Total amount is missing or invalid.")

    if structured_data.total_amount is not None and structured_data.total_amount <= 0:
        errors.append("Total amount must be greater than zero.")

    if structured_data.currency is None or structured_data.currency == "":
        errors.append(f"Currency '{structured_data.currency}' is not recognized. Defaulting to 'EUR'.")
    
    if not structured_data.items:
        warnings.append("No items were extracted.")

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        warnings=warnings
    )