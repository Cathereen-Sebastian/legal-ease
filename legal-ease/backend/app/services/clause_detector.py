import torch
from sentence_transformers import SentenceTransformer, util
from app.risk_definitions import RISK_CATEGORIES
from app.models.risk_clause import RiskClause
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
    "do not",
    "does not",
    "never",
    "without your consent",
    "only with your permission",
    "minimal",
    "optional",
    "you can disable",
    "you may disable",
    "retain ownership",
    "remains your property",
    "no automatic charges",
    "no recurring charges",
    "not track",
    "not share",
    "not sell",
    "only required",
    "only necessary",
    "at any time through settings",
    "retain full ownership",
    "delete your account",
    "remove content at any time"
]


def is_protective_sentence(sentence: str) -> bool:
    s = sentence.lower()

    for indicator in SAFE_INDICATORS:
        if indicator in s:
            return True

    return False


# -----------------------------
# 4. Keyword Negation Check
# -----------------------------
NEGATION_WORDS = [
    "not",
    "never",
    "no",
    "without",
    "cannot",
    "won't",
    "don't"
]


def keyword_is_negated(sentence: str, keyword: str) -> bool:
    s = sentence.lower()

    index = s.find(keyword.lower())

    if index == -1:
        return False

    context = s[max(0, index - 40): index + 40]

    for neg in NEGATION_WORDS:
        if neg in context:
            return True

    return False


# -----------------------------
# 5. Main Clause Detection
# -----------------------------
def detect_clauses(sentences):

    detected_categories = set()
    risky_clauses = []
    risky_sentence_count = 0

    if not sentences:
        return detected_categories, risky_clauses, risky_sentence_count

    # Encode all sentences once
    sentence_embeddings = embedding_model.encode(
        sentences,
        convert_to_tensor=True,
        show_progress_bar=False
    )

    for i, sentence in enumerate(sentences):

        sentence_lower = sentence.lower().strip()
        sentence_embedding = sentence_embeddings[i]

        sentence_marked_risky = False

        # -----------------------------
        # Skip clearly protective sentences
        # -----------------------------
        if is_protective_sentence(sentence_lower):
            continue

        for category, data in RISK_CATEGORIES.items():

            category_detected = False

            # -----------------------------
            # 1. Keyword Matching
            # -----------------------------
            for keyword in data["keywords"]:

                if keyword.lower() in sentence_lower:

                    if not keyword_is_negated(sentence_lower, keyword):
                        category_detected = True
                        break

            # -----------------------------
            # 2. Semantic Matching
            # -----------------------------
            if not category_detected and category in TEMPLATE_EMBEDDINGS:

                similarities = util.cos_sim(
                    sentence_embedding,
                    TEMPLATE_EMBEDDINGS[category]
                )

                if torch.max(similarities).item() >= SIMILARITY_THRESHOLD:
                    category_detected = True

            # -----------------------------
            # 3. Add Risk Clause
            # -----------------------------
            if category_detected:

                detected_categories.add(category)

                risky_clauses.append(
                    RiskClause(
                        sentence=sentence,
                        category=category,
                        explanation=data["explanation"]
                    )
                )

                sentence_marked_risky = True

        if sentence_marked_risky:
            risky_sentence_count += 1

    return detected_categories, risky_clauses, risky_sentence_count