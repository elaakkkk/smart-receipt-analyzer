from app.schemas.receipt_schema import ExtractedReceiptData


def calculate_category_totals(
    structured_data: ExtractedReceiptData
) -> dict[str, float]:
    category_totals: dict[str, float] = {}

    for item in structured_data.items:
        category = item.category or "other"
        total_price = item.total_price or 0

        category_totals[category] = round(
            category_totals.get(category, 0) + total_price,
            2
        )

    return category_totals


def calculate_items_total(structured_data: ExtractedReceiptData) -> float:
    total = sum(
        item.total_price or 0
        for item in structured_data.items
    )

    return round(total, 2)


def calculate_items_count(structured_data: ExtractedReceiptData) -> int:
    return len(structured_data.items)