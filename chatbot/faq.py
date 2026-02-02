import json
import os
from rapidfuzz import process, fuzz

_FAQ = []

def load_faq():
    global _FAQ
    if _FAQ:
        return _FAQ

    # Project root is one folder above chatbot/
    base_dir = os.path.dirname(os.path.dirname(__file__))
    faq_path = os.path.join(base_dir, "data", "faq.json")

    with open(faq_path, "r", encoding="utf-8") as f:
        _FAQ = json.load(f)

    return _FAQ


def find_faq_answer(user_text, threshold=75):
    if not user_text:
        return None

    faq = load_faq()

    pairs = []
    for item in faq:
        for phrasing in item["q"]:
            pairs.append((phrasing, item["a"]))

    choices = [p for p, _ in pairs]

    match = process.extractOne(
        user_text.lower().strip(),
        choices,
        scorer=fuzz.WRatio
    )

    if not match:
        return None

    _, score, index = match
    if score < threshold:
        return None

    return pairs[index][1]
