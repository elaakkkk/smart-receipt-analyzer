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

    items = extract_items(extracted_text)
    total_amount = extract_total_amount(extracted_text)
    items_total = calculate_raw_items_total(items)

    structured_data = {
        "merchant_name": extract_merchant_name(extracted_text),
        "purchase_date": extract_purchase_date(extracted_text),
        "total_amount": total_amount,
        "discount_amount": extract_discount_amount(items_total, total_amount),
        "currency": extract_currency(extracted_text),
        "category_totals": calculate_category_totals_from_items(items),
        "items": items,
    }

    return ExtractedReceiptData(**structured_data)


# -------------------------------------------------------------------
# Merchant
# -------------------------------------------------------------------

def extract_merchant_name(text: str) -> str | None:
    lower_text = normalize_ocr_text(text.lower())

    merchant_patterns = [
        ("LIDL", ["lidl"]),
        ("LECLERC", ["e.leclerc", "e leclerc", "leclerc"]),
        ("SUPER U", ["super u", "magasin u", "commercants autrement", "commercantes autrement", "carte u"]),
        ("CARREFOUR", ["carrefour"]),
        ("MONOPRIX", ["monoprix"]),
        ("AUCHAN", ["auchan"]),
        ("INTERMARCHE", ["intermarche"]),
        ("CASINO", ["casino"]),
        ("FRANPRIX", ["franprix"]),
        ("ACTION", ["action"]),
    ]

    for merchant, keywords in merchant_patterns:
        if any(keyword in lower_text for keyword in keywords):
            return merchant

    lines = get_clean_lines(text)

    for line in lines[:8]:
        if len(line) >= 3 and not contains_amount(line):
            return line

    return None


# -------------------------------------------------------------------
# Date / Total / Currency
# -------------------------------------------------------------------

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

    priority_patterns = [
        r"total\s+\d+\s+articles?\s+(\d+[,.]\d{2})",
        r"total\s*\[\d+\]\s*articles?\s+(\d+[,.]\d{2})",
        r"(?:a payer|à payer)\s+(\d+[,.]\d{2})",
        r"cb\s+sans\s+contact\s+(\d+[,.]\d{2})",
        r"montant\s*=\s*(\d+[,.]\d{2})",
        r"carte\s+(\d+[,.]\d{2})",
    ]

    for pattern in priority_patterns:
        match = re.search(pattern, normalized_text)

        if match:
            return parse_amount(match.group(1))

    candidate_lines = []

    for line in get_clean_lines(normalized_text):
        lower_line = line.lower()

        if any(
            ignored in lower_line
            for ignored in [
                "sous - total",
                "sous-total",
                "total tva",
                "tva ht ttc",
                "mont.tva",
                "total ht",
                "cumul disponible",
                "solde",
                "bon achat",
            ]
        ):
            continue

        candidate_lines.append(line)

    amounts = []

    for line in candidate_lines:
        amounts.extend(re.findall(r"\b\d+[,.]\d{2}\b", line))

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


# -------------------------------------------------------------------
# Items extraction
# -------------------------------------------------------------------

def extract_items(text: str) -> list[dict]:
    normalized_text = normalize_ocr_text(text)
    lines = get_clean_lines(normalized_text)

    items: list[dict] = []

    ignored_keywords = [
        "ticket",
        "article p.u",
        "ttc tva",
        "reduction",
        "lidl plus",
    ]

    for index, line in enumerate(lines):
        lower_line = normalize_ocr_text(line.lower())

        if is_quantity_detail_line(line):
            continue

        if is_section_header(line):
            continue

        if should_stop_item_extraction(lower_line):
            break

        if any(keyword in lower_line for keyword in ignored_keywords):
            continue

        if is_tax_line(line):
            continue

        item = (
            parse_lidl_item_line(line)
            or parse_super_u_item_line(line, lines, index)
            or parse_leclerc_item_line(line)
        )

        if not item:
            continue

        item["category"] = categorize_item(item["name"])
        items.append(item)

    return items


def parse_lidl_item_line(line: str) -> dict | None:
    pattern = re.compile(
        r"^(?P<name>.+?)\s+"
        r"(?P<unit_price>\d+[,.]\d{2})\s+"
        r"(?P<quantity>\d+(?:[,.]\d+)?)\s+"
        r"(?P<total_price>\d+[,.]\d{2})"
    )

    match = pattern.search(line)

    if not match:
        return None

    name = clean_item_name(match.group("name"))
    unit_price = parse_amount(match.group("unit_price"))
    quantity = parse_quantity(match.group("quantity"))
    total_price = parse_amount(match.group("total_price"))

    unit_price, total_price = fix_item_prices(unit_price, quantity, total_price)

    if not name or total_price is None:
        return None

    if should_ignore_product_name(name):
        return None

    return {
        "name": name,
        "unit_price": unit_price,
        "quantity": quantity,
        "total_price": total_price,
    }


def parse_super_u_item_line(
    line: str,
    lines: list[str],
    index: int
) -> dict | None:
    """
    Super U format examples:
    CROUTONS ROND.FRIT.NAT.U 2X90G 1,12 € 11
    EQUILIDEJ CROUS.CHOC.BJORG500G 4,00 € Il
    M&M'S MINIS POCH.360G FAM.PACK 4,99 € Ill
    """

    product_pattern = re.compile(
        r"^(?P<name>.+?)\s+"
        r"(?P<total_price>\d+[,.]\d{2})\s*(?:eur|€)?\s*"
        r"(?P<tax_code>[0-9ilIL]{1,3})?$",
        re.IGNORECASE
    )

    match = product_pattern.search(line)

    if not match:
        return None

    name = clean_item_name(match.group("name"))
    total_price = parse_amount(match.group("total_price"))

    if not name or total_price is None:
        return None

    if should_ignore_product_name(name):
        return None

    quantity = 1.0
    unit_price = total_price

    if index + 1 < len(lines):
        next_line = normalize_ocr_text(lines[index + 1].lower())

        quantity_match = re.search(
            r"^(?P<quantity>\d+(?:[,.]\d+)?)\s*x+\s*(?P<unit_price>\d+[,.]\d{2})\s*(?:eur)?$",
            next_line
        )

        if quantity_match:
            quantity = parse_quantity(quantity_match.group("quantity")) or 1.0
            unit_price = parse_amount(quantity_match.group("unit_price")) or total_price

    unit_price, total_price = fix_item_prices(unit_price, quantity, total_price)

    return {
        "name": name,
        "unit_price": unit_price,
        "quantity": quantity,
        "total_price": total_price,
    }


def parse_leclerc_item_line(line: str) -> dict | None:
    """
    Leclerc format examples:
    THE SAVEUR VANIL.MIEL,TWINI, 30 2.77.2
    RUTABAGA VRAC 1.10 2
    CAROTTE 0.57 2
    """

    pattern = re.compile(
        r"^(?P<name>.+?)\s+"
        r"(?P<total_price>\d+[,.]\d{2})(?:[,.]?\d+)?$"
    )

    match = pattern.search(line)

    if not match:
        return None

    name = clean_item_name(match.group("name"))
    total_price = parse_amount(match.group("total_price"))

    if not name or total_price is None:
        return None

    if should_ignore_product_name(name):
        return None

    if re.search(r"\d{8,}", name):
        return None

    return {
        "name": name,
        "unit_price": total_price,
        "quantity": 1.0,
        "total_price": total_price,
    }


# -------------------------------------------------------------------
# Item filters / helpers
# -------------------------------------------------------------------

def is_quantity_detail_line(line: str) -> bool:
    """
    Ignore lines like:
    1 x 1,12 EUR
    1 xX 1,05 EUR
    """

    normalized_line = normalize_ocr_text(line.lower()).strip()

    return bool(
        re.match(
            r"^\d+(?:[,.]\d+)?\s*x+\s*\d+[,.]\d{2}\s*(?:eur)?$",
            normalized_line
        )
    )


def is_section_header(line: str) -> bool:
    normalized_line = normalize_ocr_text(line.lower()).strip()

    section_headers = [
        "epicerie",
        "fraiche decoupe",
        "fruits et legumes",
        "papet rdc",
        "aides a la cuisine",
        "biscuits sucres",
        "cereales et poudres chocolat",
        "chocolats snacking",
        "fruits",
        "laits et derives",
        "legumes",
        "potages",
        "sacherie",
        "surgele sale",
        "surgele sucre",
    ]

    return (
        normalized_line in section_headers
        or normalized_line.startswith(">>")
        or normalized_line.startswith("***")
    )


def should_stop_item_extraction(lower_line: str) -> bool:
    normalized_line = normalize_ocr_text(lower_line).strip()

    stop_prefixes = [
        "nombre de lignes",
        "nombre de lignes d'article",
        "total ",
        "total [",
        "sous - total",
        "sous-total",
        "cb sans contact",
        "carte bancaire",
        "bon achat carte",
        "vos avantages",
        "echange",
        "echanges",
        "siret",
        "code magasin",
        "no carte",
        "votre solde",
        "ticket a conserver",
    ]

    stop_contains = [
        "a payer",
        "total eligible",
        "total eligibles",
        "tva ht ttc",
        "taux mont",
        "avec lidl plus",
    ]

    return (
        any(normalized_line.startswith(prefix) for prefix in stop_prefixes)
        or any(keyword in normalized_line for keyword in stop_contains)
    )


def should_ignore_product_name(name: str) -> bool:
    lower_name = normalize_ocr_text(name.lower()).strip()

    ignored = [
        "total",
        "sous total",
        "total tva",
        "dont articles",
        "cb sans contact",
        "tva ht ttc",
        "votre solde",
        "code magasin",
        "no carte",
        "siret",
        "date heure",
        "telephone",
        "magasin",
        "france",
        "tva",
        "vente",
    ]

    if any(keyword in lower_name for keyword in ignored):
        return True

    if is_quantity_detail_line(name):
        return True

    if is_section_header(name):
        return True

    if len(name.strip()) < 3:
        return True

    return False


def is_tax_line(line: str) -> bool:
    return bool(
        re.match(
            r"^[A-Z]\s+\d+[,.]\d+%\s+\d+[,.]\d{2}\s+\d+[,.]\d{2}\s+\d+[,.]\d{2}",
            line.strip()
        )
    )


def clean_item_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r"^[>\-\*\s]+", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()


# -------------------------------------------------------------------
# Calculations
# -------------------------------------------------------------------

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


def extract_discount_amount(
    items_total: float | None,
    total_amount: float | None
) -> float | None:
    if items_total is None or total_amount is None:
        return None

    discount = round(items_total - total_amount, 2)

    # avoid false discounts caused by OCR/parser noise
    if discount <= 0:
        return None

    # if the difference is too large, it is probably an extraction error
    if total_amount > 0 and discount > total_amount * 0.35:
        return None

    return discount


def calculate_raw_items_total(items: list[dict]) -> float:
    total = sum(
        item.get("total_price") or 0
        for item in items
    )

    return round(total, 2)


def calculate_category_totals_from_items(items: list[dict]) -> dict[str, float]:
    category_totals: dict[str, float] = {}

    for item in items:
        category = item.get("category") or "other"
        total_price = item.get("total_price") or 0

        category_totals[category] = round(
            category_totals.get(category, 0) + total_price,
            2
        )

    return category_totals


# -------------------------------------------------------------------
# Generic helpers
# -------------------------------------------------------------------

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


def parse_quantity(value: str) -> float | None:
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
        .replace("é", "e")
        .replace("É", "E")
        .replace("è", "e")
        .replace("È", "E")
        .replace("ê", "e")
        .replace("Ê", "E")
        .replace("ç", "c")
        .replace("Ç", "C")
        .replace("’", "'")
        .replace("montant\n", "montant ")
        .replace("a payer\n", "a payer ")
    )