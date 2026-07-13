from collections import defaultdict
from datetime import datetime

from app.models.receipt import Receipt


def get_merchant_spending(receipts: list[Receipt]) -> list[dict]:
    merchant_data: dict[str, dict] = {}

    for receipt in receipts:
        data = receipt.structured_data or {}

        merchant_name = data.get("merchant_name") or receipt.document_type or "Unknown"
        total_amount = data.get("total_amount") or 0

        if merchant_name not in merchant_data:
            merchant_data[merchant_name] = {
                "merchant_name": merchant_name,
                "total_spent": 0,
                "receipt_count": 0,
            }

        merchant_data[merchant_name]["total_spent"] += total_amount
        merchant_data[merchant_name]["receipt_count"] += 1

    result = list(merchant_data.values())

    for item in result:
        item["total_spent"] = round(item["total_spent"], 2)

    return sorted(result, key=lambda item: item["total_spent"], reverse=True)


def get_monthly_spending(receipts: list[Receipt]) -> list[dict]:
    monthly_data: dict[str, dict] = {}

    for receipt in receipts:
        data = receipt.structured_data or {}
        total_amount = data.get("total_amount") or 0

        month = extract_month(data, receipt)

        if month not in monthly_data:
            monthly_data[month] = {
                "month": month,
                "total_spent": 0,
                "receipt_count": 0,
            }

        monthly_data[month]["total_spent"] += total_amount
        monthly_data[month]["receipt_count"] += 1

    result = list(monthly_data.values())

    for item in result:
        item["total_spent"] = round(item["total_spent"], 2)

    return sorted(result, key=lambda item: item["month"])


def get_top_products(receipts: list[Receipt], limit: int = 10) -> list[dict]:
    product_data: dict[str, dict] = {}

    for receipt in receipts:
        data = receipt.structured_data or {}
        items = data.get("items") or []

        for item in items:
            product_name = item.get("name") or "Unknown product"
            total_price = item.get("total_price") or 0
            quantity = item.get("quantity") or 1

            normalized_name = product_name.strip().lower()

            if normalized_name not in product_data:
                product_data[normalized_name] = {
                    "product_name": product_name,
                    "total_spent": 0,
                    "quantity": 0,
                }

            product_data[normalized_name]["total_spent"] += total_price
            product_data[normalized_name]["quantity"] += quantity

    result = list(product_data.values())

    for item in result:
        item["total_spent"] = round(item["total_spent"], 2)
        item["quantity"] = round(item["quantity"], 2)

    return sorted(result, key=lambda item: item["total_spent"], reverse=True)[:limit]


def get_category_spending(receipts: list[Receipt]) -> list[dict]:
    category_data: defaultdict[str, float] = defaultdict(float)

    for receipt in receipts:
        data = receipt.structured_data or {}
        items = data.get("items") or []

        for item in items:
            category = item.get("category") or "other"
            total_price = item.get("total_price") or 0

            category_data[category] += total_price

    result = [
        {
            "category": category,
            "total_spent": round(total_spent, 2),
        }
        for category, total_spent in category_data.items()
    ]

    return sorted(result, key=lambda item: item["total_spent"], reverse=True)


def extract_month(data: dict, receipt: Receipt) -> str:
    purchase_date = data.get("purchase_date")

    if purchase_date:
        try:
            parsed_date = datetime.fromisoformat(purchase_date)
            return parsed_date.strftime("%Y-%m")
        except ValueError:
            pass

    return receipt.created_at.strftime("%Y-%m")