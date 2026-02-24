from sentence_transformers import SentenceTransformer, util
import torch
from app.risk_definitions import RISK_CATEGORIES
from app.models.risk_clause import RiskClause
from app.config import SIMILARITY_THRESHOLD

# Load model once on startup
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Precompute template embeddings
TEMPLATE_EMBEDDINGS = {}
for category, data in RISK_CATEGORIES.items():
    templates = data.get("semantic_templates", [])
    if templates:
        TEMPLATE_EMBEDDINGS[category] = embedding_model.encode(templates, convert_to_tensor=True)

def detect_clauses(sentences):
    detected_categories = set()
    risky_clauses = []
    risky_sentence_count = 0

    if not sentences:
        return detected_categories, risky_clauses, risky_sentence_count

    # Optimization: Batch encode all sentences at once
    all_embeddings = embedding_model.encode(sentences, convert_to_tensor=True)

    for i, sentence in enumerate(sentences):
        lower_sentence = sentence.lower()
        sentence_embedding = all_embeddings[i]
        detected = False

        for category, data in RISK_CATEGORIES.items():
            # Level-1: Keyword Match
            for keyword in data["keywords"]:
                if keyword in lower_sentence:
                    detected = True
                    break

            # Level-3: Semantic Match
            if not detected and category in TEMPLATE_EMBEDDINGS:
                similarities = util.cos_sim(sentence_embedding, TEMPLATE_EMBEDDINGS[category])
                if torch.max(similarities).item() >= SIMILARITY_THRESHOLD:
                    detected = True

            if detected:
                detected_categories.add(category)
                risky_sentence_count += 1
                risky_clauses.append(RiskClause(
                    sentence=sentence,
                    category=category,
                    explanation=data["explanation"]
                ))
                break 

    return detected_categories, risky_clauses, risky_sentence_count