import re

card_names = [
    "Active Cash Visa Card",
    "Autograph Journey Visa Card",
    "Autograph Visa Card",
    "Reflect Visa Card",
    "Attune World Elite Mastercard",
    "Bilt World Elite Mastercard",
    "One Key Mastercard",
    "One Key+ Mastercard",
    "Choices Privileges World Elite Mastercard",
    "Choices Privileges Select World Elite Mastercard",
    "Signify Business Cash Card"
]

def identify_card_from_query(query):
    for card in card_names:
        if re.search(rf"\b{re.escape(card)}\b", query, re.IGNORECASE):
            return card, card_names
    return None, card_names