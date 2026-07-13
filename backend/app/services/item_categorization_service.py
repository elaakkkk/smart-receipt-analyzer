import re
import unicodedata


def categorize_item(item_name: str) -> str:
    name = normalize_item_name(item_name)

    phrase_rules = [
        ("pet_food", [
            "pinky snack",
            "pour chien",
            "mr goodlad",
            "mr. goodlad",
            "canard",
            "bacon boeuf",
        ]),
        ("protein", [
            "protein pancakes",
            "proteine bites",
            "gummies proteines",
            "barre proteinee",
            "proteine",
            "proteinee",
            "protein",
        ]),
        ("cosmetics", [
            "scrub",
            "body scrub",
            "blush",
            "pinceau",
            "baume",
            "gommage",
            "levres",
            "masque visage",
            "hair booster",
            "gel douche",
            "soin du corps",
            "chev miel",
            "bbume",
            "huile",
        ]),
        ("health", [
            "patch chauffant",
            "thermofect",
            "douleurs",
            "innovit",
            "biotiques",
            "gommes peau",
        ]),
        ("household", [
            "sac de transport",
            "sacs a laniere",
            "sachets congelateur",
            "sac kraft",
            "sac caisse",
            "dumil",
        ]),
        ("snack_sweet", [
            "petit beurre",
            "m&m",
            "m m",
            "minis poch",
            "nutella",
            "milka",
            "twix",
            "haribo",
            "popcorn",
            "croky",
            "baileys creams",
            "flipz",
            "pain d epices",
            "chocolat",
            "choco",
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
            "pancakes",
            "gommes",
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
            "pad thai",
            "noodle bowl",
            "sauce algerienne",
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