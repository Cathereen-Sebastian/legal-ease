from sentence_transformers import SentenceTransformer, util
import torch
import re

from app.risk_definitions import RISK_CATEGORIES
from app.models.risk_clause import RiskClause
from app.config import SIMILARITY_THRESHOLD


# --------------------------
# Load embedding model once
# --------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------
# Normalize text
# (Fix curly apostrophes)
# --------------------------
def normalize_text(text: str) -> str:
    return text.lower().replace("’", "'").strip()


# --------------------------
# Negation words
# --------------------------
NEGATION_WORDS = [
    "not", "never", "no", "without",
    "do not", "does not", "did not",
    "will not", "shall not",
    "cannot", "can't", "won't",
    "isn't", "aren't", "wasn't", "weren't"
]


# --------------------------
# Protective sentence filter
# --------------------------
SAFE_PATTERNS = [
    "we don't sell",
    "we do not sell",
    "we don't share",
    "we do not share",
    "we never sell",
    "we never share",
    "we do not disclose",
    "we don't disclose",
    "we will not sell",
    "we will not share"
]


def is_protective_sentence(sentence: str) -> bool:

    sentence = normalize_text(sentence)

    return any(pattern in sentence for pattern in SAFE_PATTERNS)


# --------------------------
# Check if sentence contains negation
# --------------------------
def contains_negation(sentence: str) -> bool:

    sentence = normalize_text(sentence)

    for word in NEGATION_WORDS:
        if word in sentence:
            return True

    return False


# --------------------------
# Check if keyword is negated
# --------------------------
def keyword_is_negated(sentence: str, keyword: str) -> bool:

    sentence = normalize_text(sentence)

    pattern = rf"(not|never|no|without|do not|does not|did not|will not|shall not)\s+\w*\s*{re.escape(keyword)}"

    return re.search(pattern, sentence) is not None


# --------------------------
# Precompute template embeddings
# --------------------------
TEMPLATE_EMBEDDINGS = {}

for category, data in RISK_CATEGORIES.items():

    templates = data.get("semantic_templates", [])

    if templates:

        TEMPLATE_EMBEDDINGS[category] = embedding_model.encode(
            templates,
            convert_to_tensor=True
        )


# --------------------------
# Main clause detection
# --------------------------
def detect_clauses(sentences):

    detected_categories = set()
    risky_clauses = []
    risky_sentence_count = 0

    if not sentences:
        return detected_categories, risky_clauses, risky_sentence_count


    # Encode sentences once (fast)
    sentence_embeddings = embedding_model.encode(
        sentences,
        convert_to_tensor=True
    )


    for i, sentence in enumerate(sentences):

        sentence_lower = normalize_text(sentence)
        sentence_embedding = sentence_embeddings[i]

        # --------------------------
        # Skip protective statements
        # --------------------------
        if is_protective_sentence(sentence_lower):
            continue


        for category, data in RISK_CATEGORIES.items():

            detected = False


            # --------------------------
            # LEVEL 1: Keyword Match
            # --------------------------
            for keyword in data["keywords"]:

                if keyword in sentence_lower:

                    # Skip if negated
                    if keyword_is_negated(sentence_lower, keyword):
                        continue

                    detected = True
                    break


            # --------------------------
            # LEVEL 2: Semantic Match
            # --------------------------
            if not detected and category in TEMPLATE_EMBEDDINGS:

                # Skip semantic detection if negation exists
                if contains_negation(sentence_lower):
                    continue

                similarities = util.cos_sim(
                    sentence_embedding,
                    TEMPLATE_EMBEDDINGS[category]
                )

                if torch.max(similarities).item() >= SIMILARITY_THRESHOLD:
                    detected = True


            # --------------------------
            # Save detected clause
            # --------------------------
            if detected:

                detected_categories.add(category)

                risky_sentence_count += 1

                risky_clauses.append(
                    RiskClause(
                        sentence=sentence,
                        category=category,
                        explanation=data["explanation"]
                    )
                )

                break


    return detected_categories, risky_clauses, risky_sentence_count