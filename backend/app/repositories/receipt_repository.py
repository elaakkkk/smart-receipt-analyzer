from sqlalchemy.orm import Session

from app.models.receipt import Receipt


def create_receipt(
    db: Session,
    original_filename: str,
    content_type: str,
    saved_path: str,
    extracted_text: str,
    document_type: str,
    structured_data: dict,
    validation_result: dict,
) -> Receipt:
    """
    Create a new receipt in the database.
    """
    db_receipt = Receipt(
        original_filename=original_filename,
        content_type=content_type,
        saved_path=saved_path,
        extracted_text=extracted_text,
        document_type=document_type,
        structured_data=structured_data,
        validation_result=validation_result,
    )

    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)

    return db_receipt

def get_receipts(db: Session, limit: int = 50):
    """
    Retrieve a list of receipts from the database.
    """
    return (
        db.query(Receipt)
        .order_by(Receipt.created_at.desc())
        .limit(limit)
        .all()
    )

def get_receipt_by_id(db: Session, receipt_id: int):
    """
    Retrieve a receipt by its ID from the database.
    """
    return db.query(Receipt).filter(Receipt.id == receipt_id).first()