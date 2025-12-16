import json
from difflib import SequenceMatcher
from pathlib import Path

FAQ_PATH = Path("data/faq.json")

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search_faq(user_question: str, threshold: float = 0.6):
    if not FAQ_PATH.exists():
        return None

    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        faqs = json.load(f)

    best_match = None
    best_score = 0

    for faq in faqs:
        score = similarity(user_question, faq["question"])
        if score > best_score:
            best_score = score
            best_match = faq

    if best_score >= threshold:
        return best_match["answer"]

    return None
