from sqlalchemy.orm import Session

from app.models.receipt import Receipt
from app.schemas.analytics_schema import AnalyticsSummaryResponse, DocumentTypesStatsResponse, ValidationStatsResponse


def get_analytics_summary(db: Session) -> AnalyticsSummaryResponse:
    """
    Retrieve analytics summary from the database.
    """
    receipts = db.query(Receipt).all()

    total_receipts = len(receipts)

    valid_receipts = 0
    invalid_receipts = 0
    unknown_documents = 0
    receipt_documents = 0
    invoice_documents = 0

    for receipt in receipts:
        validation_result = receipt.validation_result or {}
        is_valid = validation_result.get("is_valid")

        if is_valid is True:
            valid_receipts += 1
        elif is_valid is False:
            invalid_receipts += 1

        if receipt.document_type == "unknown":
            unknown_documents += 1
        elif receipt.document_type == "receipt":
            receipt_documents += 1
        elif receipt.document_type == "invoice":
            invoice_documents += 1

    return AnalyticsSummaryResponse(
        total_receipts=total_receipts,
        valid_receipts=valid_receipts,
        invalid_receipts=invalid_receipts,
        unknown_documents=unknown_documents,
        receipt_documents=receipt_documents,
        invoice_documents=invoice_documents,
    )

def get_document_types_stats(db: Session) -> DocumentTypesStatsResponse:
    """
    Retrieve document types statistics from the database.
    """
    receipts = db.query(Receipt).all()

    unknown_count = 0
    receipt_count = 0
    invoice_count = 0

    for receipt in receipts:
        if receipt.document_type == "unknown":
            unknown_count += 1
        elif receipt.document_type == "receipt":
            receipt_count += 1
        elif receipt.document_type == "invoice":
            invoice_count += 1

    return DocumentTypesStatsResponse(
        unknown=unknown_count,
        receipt=receipt_count,
        invoice=invoice_count,
    )

def get_validation_stats(db: Session) -> ValidationStatsResponse:
    """
    Retrieve validation statistics from the database.
    """
    receipts = db.query(Receipt).all()

    valid_count = 0
    invalid_count = 0
    with_warnings_count = 0
    without_warnings_count = 0

    for receipt in receipts:
        validation_result = receipt.validation_result or {}
        is_valid = validation_result.get("is_valid")
        warnings = validation_result.get("warnings", [])

        if is_valid is True:
            valid_count += 1
        elif is_valid is False:
            invalid_count += 1

        if len(warnings) > 0:
            with_warnings_count += 1
        else:
            without_warnings_count += 1

    return ValidationStatsResponse(
        valid=valid_count,
        invalid=invalid_count,
        with_warnings=with_warnings_count,
        without_warnings=without_warnings_count,
    )