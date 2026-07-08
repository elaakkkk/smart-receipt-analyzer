from app.services.classification_service import classify_document


def test_invoice():
    text = "This is an invoice document."
    result = classify_document(text)
    assert result == "invoice"

def test_receipt():
    text = "This is a receipt document."
    result = classify_document(text)
    assert result == "receipt"

def test_unknown():
    text = "This is an unknown document."
    result = classify_document(text)
    assert result == "unknown"  
 
def test_sans_mot():
    text = ""
    result = classify_document(text)
    assert result == "unknown"