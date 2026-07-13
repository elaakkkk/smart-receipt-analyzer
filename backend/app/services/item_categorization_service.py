import re
import unicodedata


def categorize_item(item_name: str) -> str:
    name = normalize_item_name(item_name)

    phrase_rules = [
        ("snack_sweet", [
            "petit beurre",
            "m&m",
            "m m",
            "minis poch",
            "nutella",
            "chocolat",
            "choc",
            "biscuit",
            "biscuits",
            "cookie",
            "cookies",
            "muesli",
            "cereales",
            "equilidej",
            "ben j",
            "b&j",
            "pot choc",
        ]),
        ("fruit", [
            "kiwi",
            "myrtille",
            "mangue",
            "citron vert",
            "salade de fruits",
            "fruits hiver",
            "barquette 4 fruits",
        ]),
        ("vegetable_herb", [
            "laitue",
            "iceberg",
            "poireaux",
            "rutabaga",
            "carotte",
            "tomate",
            "concombre",
            "brocoli",
            "courgette",
            "poivron",
            "oignon",
            "aneth",
            "persil",
            "basilic",
            "menthe",
        ]),
        ("dairy", [
            "cr uht",
            "uht ent",
            "lait ",
            "yaourt",
            "yogurt",
            "fromage",
            "fromages",
            "creme",
            "beurre doux",
        ]),
        ("carbohydrate", [
            "spaghetti",
            "pates",
            "riz",
            "pain",
            "baguette",
            "frites",
            "pdt",
            "pomme de terre",
            "croutons",
        ]),
        ("prepared_food", [
            "pizza",
            "sandwich",
            "quiche",
            "lasagne",
            "burger",
            "wrap",
            "veloute",
            "potage",
            "soupe",
        ]),
        ("household", [
            "sac kraft",
            "sac caisse",
            "papier",
            "sopalin",
            "mouchoir",
            "savon",
            "lessive",
        ]),
        ("beverage", [
            "the",
            "cafe",
            "nescafe",
            "nesc",
            "jus",
            "soda",
            "eau",
        ]),
        ("stationery", [
            "roller",
            "effac",
            "recharge",
            "recharges",
        ]),
    ]

    for category, phrases in phrase_rules:
        if any(phrase in name for phrase in phrases):
            return category

    return "other"


def normalize_item_name(name: str) -> str:
    name = name.lower()
    name = unicodedata.normalize("NFKD", name)
    name = "".join(char for char in name if not unicodedata.combining(char))
    name = name.replace("œ", "oe")
    name = name.replace("'", " ")
    name = name.replace(".", " ")
    name = name.replace("-", " ")
    name = name.replace("&", " & ")
    name = re.sub(r"\s+", " ", name)
    return name.strip()