# app/services/clause_detector.py

import torch
from sentence_transformers import SentenceTransformer, util
from app.models.risk_clause import RiskClause
from app.risk_definitions import RISK_CATEGORIES
from app.config import SIMILARITY_THRESHOLD

# -----------------------------
# 1. Load NLP Model
# -----------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# 2. Precompute Risk Template Embeddings
# -----------------------------
TEMPLATE_EMBEDDINGS = {}
for category, data in RISK_CATEGORIES.items():
    templates = data.get("semantic_templates", [])
    if templates:
        TEMPLATE_EMBEDDINGS[category] = embedding_model.encode(
            templates,
            convert_to_tensor=True
        )

# -----------------------------
# 3. Safety / Protective Detection
# -----------------------------
SAFE_INDICATORS = [
    "do not", "does not", "never", "without your consent",
    "only with your permission", "minimal", "optional",
    "you can disable", "you may disable", "retain ownership",
    "remains your property", "no automatic charges",
    "no recurring charges", "not track", "not share",
    "not sell", "only required", "only necessary",
    "at any time through settings", "retain full ownership",
    "delete your account", "remove content at any time"
]

def is_protective_sentence(sentence: str) -> bool:
    s = sentence.lower()
    return any(indicator in s for indicator in SAFE_INDICATORS)

# -----------------------------
# 4. Keyword Negation Check
# -----------------------------
NEGATION_WORDS = ["not", "never", "no", "without", "cannot", "won't", "don't"]

def keyword_is_negated(sentence: str, keyword: str) -> bool:
    s = sentence.lower()
    index = s.find(keyword.lower())
    if index == -1:
        return False
    context = s[max(0, index - 40): index + 40]
    return any(neg in context for neg in NEGATION_WORDS)

# -----------------------------
# 5. Permission Category Mapping
# -----------------------------
PERMISSION_KEYWORDS = {
    "camera": ["camera", "photo", "video", "take pictures", "record video"],
    "microphone": ["microphone", "voice", "audio", "call", "record"],
    "contacts": ["contact", "friends list", "address book"],
    "location": ["location", "gps", "position", "map", "current location"],
    "storage": ["storage", "files", "offline data", "save data", "device storage"],
    "usage_data": ["usage data", "analytics", "app usage", "search history", "behavioral data"]
}

def map_clause_to_permission(sentence: str):
    sentence_lower = sentence.lower()
    # Special mapping for anonymized data sharing
    if "share anonymized data" in sentence_lower:
        return "data_sharing"
    for category, keywords in PERMISSION_KEYWORDS.items():
        if any(keyword in sentence_lower for keyword in keywords):
            return category
    return None

# -----------------------------
# 6. Main Clause Detection
# -----------------------------
def detect_clauses(sentences):
    detected_categories = set()
    risky_clauses = []

    if not sentences:
        return detected_categories, risky_clauses, 0

    sentence_embeddings = embedding_model.encode(
        sentences,
        convert_to_tensor=True,
        show_progress_bar=False
    )

    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower().strip()
        sentence_embedding = sentence_embeddings[i]
        sentence_marked_risky = False

        if is_protective_sentence(sentence_lower):
            continue

        for category, data in RISK_CATEGORIES.items():
            category_detected = False

            # Keyword check
            for keyword in data.get("keywords", []):
                if keyword.lower() in sentence_lower and not keyword_is_negated(sentence_lower, keyword):
                    category_detected = True
                    break

            # Semantic similarity check
            if not category_detected and category in TEMPLATE_EMBEDDINGS:
                similarities = util.cos_sim(sentence_embedding, TEMPLATE_EMBEDDINGS[category])
                if torch.max(similarities).item() >= SIMILARITY_THRESHOLD:
                    category_detected = True

            if category_detected:
                # Map to real permission or special case
                permission_category = map_clause_to_permission(sentence) or category
                detected_categories.add(permission_category)

                risky_clauses.append(
                    RiskClause(
                        sentence=sentence,
                        category=permission_category,
                        explanation=data.get(
                            "explanation", f"This clause allows access to {permission_category} data."
                        )
                    )
                )
                sentence_marked_risky = True

    # -----------------------------
    # Deduplicate clauses by sentence
    # -----------------------------
    unique_clauses = []
    seen_sentences = set()
    for clause in risky_clauses:
        if clause.sentence not in seen_sentences:
            unique_clauses.append(clause)
            seen_sentences.add(clause.sentence)

    return detected_categories, unique_clauses, len(unique_clauses)