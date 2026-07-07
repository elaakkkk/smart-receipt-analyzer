def classify_document(text: str) -> str:
    """
    Classifies the document based on its text content.

    Args:
        text (str): The text extracted from the document.

    Returns:
        str: The classification label for the document.
    """
    # Placeholder logic for classification
    if "facture" in text.lower() or "invoice" in text.lower():
        return "invoice"
    elif "total" in text.lower() or "receipt" in text.lower():
        return "receipt"
    else:
        return "unknown"