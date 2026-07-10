def classify_document(text: str) -> str:
    """
    Classify a document as receipt, invoice, or unknown using keyword scoring.
    """
    normalized_text = text.lower()

    receipt_score = calculate_score(
        normalized_text,
        [
            "ticket de vente",
            "ticket client",
            "ticket de caisse",
            "a payer",
            "à payer",
            "carte bancaire",
            "sans contact",
            "nombre de lignes",
            "merci de votre visite",
            "total promotion",
            "lidl plus",
            "cb",
        ],
    )

    invoice_score = calculate_score(
        normalized_text,
        [
            "facture",
            "invoice",
            "numéro de facture",
            "numero de facture",
            "invoice number",
            "date de facture",
            "billing address",
            "adresse de facturation",
            "tva intracommunautaire",
            "conditions de paiement",
            "montant ht",
            "montant ttc",
        ],
    )

    if receipt_score >= 2 and receipt_score >= invoice_score:
        return "receipt"

    if invoice_score >= 2 and invoice_score > receipt_score:
        return "invoice"

    return "unknown"


def calculate_score(text: str, keywords: list[str]) -> int:
    return sum(1 for keyword in keywords if keyword in text)