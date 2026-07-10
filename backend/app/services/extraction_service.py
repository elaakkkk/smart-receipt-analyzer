import re
from datetime import datetime

from app.services.item_categorization_service import categorize_item
from app.schemas.receipt_schema import ExtractedReceiptData


def extract_structured_data(
    extracted_text: str,
    document_type: str
) -> ExtractedReceiptData:
    """
    Extract structured receipt data from OCR text.
    """

    structured_data = {
        "merchant_name": extract_merchant_name(extracted_text),
        "purchase_date": extract_purchase_date(extracted_text),
        "total_amount": extract_total_amount(extracted_text),
        "currency": extract_currency(extracted_text),
        "items": extract_items(extracted_text),
    }

    return ExtractedReceiptData(**structured_data)


def extract_merchant_name(text: str) -> str | None:
    lines = get_clean_lines(text)

    merchant_keywords = [
        "lidl",
        "carrefour",
        "monoprix",
        "auchan",
        "leclerc",
        "intermarché",
        "intermarche",
        "casino",
        "franprix",
        "u express",
        "super u",
    ]

    lower_text = text.lower()

    for keyword in merchant_keywords:
        if keyword in lower_text:
            return keyword.upper()

    for line in lines[:8]:
        if len(line) >= 3 and not contains_amount(line):
            return line

    return None


def extract_purchase_date(text: str) -> str | None:
    normalized_text = normalize_ocr_text(text)

    patterns = [
        r"\b(\d{1,2})[\/\.-](\d{1,2})[\/\.-](\d{4})\b",
        r"\b(\d{1,2})[\/\.-](\d{1,2})[\/\.-](\d{2})\b",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, normalized_text)

        for match in matches:
            day = int(match[0])
            month = int(match[1])
            year = int(match[2])

            if year < 100:
                year += 2000

            try:
                parsed_date = datetime(year, month, day)
                return parsed_date.date().isoformat()
            except ValueError:
                continue

    return None


def extract_total_amount(text: str) -> float | None:
    normalized_text = normalize_ocr_text(text.lower())

    total_patterns = [
        r"a payer\s+(\d+[,.]\d{2})",
        r"montant\s+(\d+[,.]\d{2})",
        r"total\s+(?:ttc)?\s*(\d+[,.]\d{2})",
        r"carte\s+(\d+[,.]\d{2})",
    ]

    for pattern in total_patterns:
        match = re.search(pattern, normalized_text)

        if match:
            return parse_amount(match.group(1))

    amounts = re.findall(r"\b\d+[,.]\d{2}\b", normalized_text)

    parsed_amounts = [
        amount
        for amount in (parse_amount(value) for value in amounts)
        if amount is not None
    ]

    if not parsed_amounts:
        return None

    return max(parsed_amounts)


def extract_currency(text: str) -> str:
    upper_text = text.upper()

    if "EUR" in upper_text or "€" in upper_text:
        return "EUR"

    if "USD" in upper_text or "$" in upper_text:
        return "USD"

    return "EUR"


def get_clean_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


def contains_amount(text: str) -> bool:
    return bool(re.search(r"\d+[,.]\d{2}", text))


def parse_amount(value: str) -> float | None:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None


def normalize_ocr_text(text: str) -> str:
    return (
        text
        .replace("@", "0")
        .replace("€", " eur ")
        .replace("à", "a")
        .replace("À", "A")
        .replace("montant\n", "montant ")
        .replace("a payer\n", "a payer ")
        .replace("à payer\n", "à payer ")
    )

def extract_items(text: str) -> list[dict]:
    normalized_text = normalize_ocr_text(text)
    lines = get_clean_lines(normalized_text)

    items = []

    ignored_keywords = [
        "ticket",
        "article",
        "nombre de lignes",
        "reduction",
        "réduction",
        "lidl plus",
        "a payer",
        "total",
        "carte",
        "tva",
        "montant",
        "siret",
        "code ape",
        "merci",
        "garantie",
        "factures",
        "coupon",
        "coupons",
        "points",
        "achat effectué",
        "supermarché",
        "supermarche",
    ]

    stop_keywords = [
        "nombre de lignes",
        "a payer",
        "total eligible",
        "total éligible",
        "carte",
        "va taux",
        "taux mont",
        "total promotion",
        "avec lidl plus",
        "siret",
    ]

    item_pattern = re.compile(
        r"^(?P<name>.+?)\s+"
        r"(?P<unit_price>\d+[,.]\d{2})\s+"
        r"(?P<quantity>\d+(?:[,.]\d+)?)\s+"
        r"(?P<total_price>\d+[,.]\d{2})"
    )

    for line in lines:
        lower_line = line.lower()

        if any(keyword in lower_line for keyword in stop_keywords):
            break

        if any(keyword in lower_line for keyword in ignored_keywords):
            continue

        if is_tax_line(line):
            continue

        match = item_pattern.search(line)

        if not match:
            continue

        name = match.group("name").strip()
        unit_price = parse_amount(match.group("unit_price"))
        quantity = parse_quantity(match.group("quantity"))
        total_price = parse_amount(match.group("total_price"))

        unit_price, total_price = fix_item_prices(
            unit_price=unit_price,
            quantity=quantity,
            total_price=total_price,
        )

        if not name or total_price is None:
            continue

        items.append(
            {
                "name": name,
                "unit_price": unit_price,
                "quantity": quantity,
                "total_price": total_price,
                "category": categorize_item(name)
            }
        )

    return items

def parse_quantity(value: str) -> float | None:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None

def is_tax_line(line: str) -> bool:
    return bool(
        re.match(
            r"^[A-Z]\s+\d+[,.]\d+%\s+\d+[,.]\d{2}\s+\d+[,.]\d{2}\s+\d+[,.]\d{2}",
            line.strip()
        )
    )

def fix_item_prices(
    unit_price: float | None,
    quantity: float | None,
    total_price: float | None
) -> tuple[float | None, float | None]:
    if unit_price is None or quantity is None or total_price is None:
        return unit_price, total_price

    expected_total = round(unit_price * quantity, 2)

    if expected_total == total_price:
        return unit_price, total_price

    if quantity == 1 and unit_price != total_price:
        unit_price = total_price
        return unit_price, total_price

    corrected_unit_price = round(total_price / quantity, 2)

    if corrected_unit_price > 0:
        unit_price = corrected_unit_price

    return unit_price, total_price