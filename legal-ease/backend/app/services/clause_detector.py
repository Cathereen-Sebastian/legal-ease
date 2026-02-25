import torch
from sentence_transformers import SentenceTransformer, util
from app.risk_definitions import RISK_CATEGORIES
from app.models.risk_clause import RiskClause
from app.config import SIMILARITY_THRESHOLD

# -----------------------------
# 1. Load Model Once
# -----------------------------
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# 2. Precompute Template Embeddings
# -----------------------------
TEMPLATE_EMBEDDINGS = {}
for category, data in RISK_CATEGORIES.items():
    templates = data.get("semantic_templates", [])
    if templates:
        TEMPLATE_EMBEDDINGS[category] = embedding_model.encode(templates, convert_to_tensor=True)

# -----------------------------
# 3. Negation & Protective Logic
# -----------------------------
STRONG_SAFE_PHRASES = [
    "under no circumstances", "at no time", "strictly prohibit",
    "strictly refrain", "not our practice", "do not restrict",
    "will not monetize", "never sell"
]

NEGATION_WORDS = ["not", "never", "no", "won't", "don't", "cannot", "prohibit", "refrain"]

PROTECTIVE_PREFIXES = ["we do not", "we will not", "we shall not", "we never"]

def is_protective_sentence(sentence: str) -> bool:
    s_low = sentence.lower().strip()

    # Certain phrases override risk
    if "no liability" in s_low or "not liable" in s_low:
        return False  # This is risky, so never mark safe

    if any(phrase in s_low for phrase in STRONG_SAFE_PHRASES):
        return True

    if any(s_low.startswith(p) for p in PROTECTIVE_PREFIXES):
        return True

    return False

def is_keyword_negated(sentence: str, keyword: str) -> bool:
    s_low = sentence.lower()
    kw_index = s_low.find(keyword.lower())

    if kw_index == -1:
        return False

    # Look at words before the keyword
    context_before = s_low[:kw_index].split()
    return any(neg in context_before for neg in NEGATION_WORDS)

# -----------------------------
# 4. Main Detection Function
# -----------------------------
def detect_clauses(sentences):
    detected_categories = set()
    risky_clauses = []
    risky_sentence_count = 0

    if not sentences:
        return detected_categories, risky_clauses, risky_sentence_count

    # Batch encode sentences
    all_embeddings = embedding_model.encode(sentences, convert_to_tensor=True, show_progress_bar=False)

    for i, sentence in enumerate(sentences):
        lower_sentence = sentence.lower().strip()
        sentence_embedding = all_embeddings[i]
        sentence_is_risky = False

        # Step 1: Skip protective sentences
        if is_protective_sentence(lower_sentence):
            continue

        for category, data in RISK_CATEGORIES.items():
            category_detected = False

            # Step 2: Keyword Match with Negation Check
            for keyword in data["keywords"]:
                if keyword.lower() in lower_sentence:
                    if not is_keyword_negated(lower_sentence, keyword):
                        category_detected = True
                        break

            # Step 3: Semantic Match
            if not category_detected and category in TEMPLATE_EMBEDDINGS:
                similarities = util.cos_sim(sentence_embedding, TEMPLATE_EMBEDDINGS[category])
                if torch.max(similarities).item() >= SIMILARITY_THRESHOLD:
                    category_detected = True

            if category_detected:
                detected_categories.add(category)
                sentence_is_risky = True
                risky_clauses.append(
                    RiskClause(
                        sentence=sentence,
                        category=category,
                        explanation=data["explanation"]
                    )
                )

        if sentence_is_risky:
            risky_sentence_count += 1

    return detected_categories, risky_clauses, risky_sentence_count