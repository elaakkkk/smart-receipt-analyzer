from app.schemas.receipt_schema import ExtractedReceiptData
from app.services.business_validation_service import validate_extracted_data


def test_données_valid():
    structured_data = ExtractedReceiptData(
        merchant_name="Test Merchant",
        total_amount=100.0,
        currency="USD",
        items=[{"name": "Item 1", "price": 50.0}, {"name": "Item 2", "price": 50.0}],
    )
    result = validate_extracted_data(structured_data)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert len(result.warnings) == 0

def test_total_amount_missing():
    structured_data = ExtractedReceiptData(
        merchant_name="Test Merchant",
        total_amount=None,
        currency="USD",
        items=[{"name": "Item 1", "price": 50.0}],
    )
    result = validate_extracted_data(structured_data)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert len(result.warnings) == 1
    assert "Total amount is missing or invalid." in result.warnings

def test_items_vide():
    structured_data = ExtractedReceiptData(
        merchant_name="Test Merchant",
        total_amount=100.0,
        currency="USD",
        items=[],
    )
    result = validate_extracted_data(structured_data)
    assert result.is_valid is True
    assert len(result.errors) == 0
    assert len(result.warnings) == 1
    assert "No items were extracted." in result.warnings

def test_total_amount_negatif():
    structured_data = ExtractedReceiptData(
        merchant_name="Test Merchant",
        total_amount=-50.0,
        currency="USD",
        items=[{"name": "Item 1", "price": -50.0}],
    )
    result = validate_extracted_data(structured_data)
    assert result.is_valid is False
    assert len(result.errors) == 1
    assert "Total amount must be greater than zero." in result.errors
    assert len(result.warnings) == 0

def test_currency_non_reconnue():
    structured_data = ExtractedReceiptData(
        merchant_name="Test Merchant",
        total_amount=100.0,
        currency=None,
        items=[{"name": "Item 1", "price": 100.0}],
    )
    result = validate_extracted_data(structured_data)
    assert result.is_valid is False
    assert len(result.errors) == 1
    assert "Currency is missing or invalid." in result.errors
    assert len(result.warnings) == 0