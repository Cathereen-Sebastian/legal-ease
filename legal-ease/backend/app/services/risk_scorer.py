from app.risk_definitions import RISK_CATEGORIES
from app.config import ALPHA, BETA, GAMMA

def compute_risk(detected_categories, risky_sentence_count, total_sentences):

    # --------------------------
    # S1: Severity (Relative to Max Weight)
    # --------------------------
    max_possible_weight = 5.0
    # Only consider categories that exist in RISK_CATEGORIES
    valid_weights = [RISK_CATEGORIES[cat]["weight"] for cat in detected_categories if cat in RISK_CATEGORIES]
    S1 = max(valid_weights) / max_possible_weight if valid_weights else 0

    # --------------------------
    # S2: Diversity
    # --------------------------
    M = len(RISK_CATEGORIES)
    K = len([cat for cat in detected_categories if cat in RISK_CATEGORIES])
    S2 = K / M if M else 0

    # --------------------------
    # S3: Density (With a "Floor" for long docs)
    # --------------------------
    raw_density = risky_sentence_count / total_sentences if total_sentences else 0
    if risky_sentence_count >= 2:
        S3 = max(raw_density, 0.5)
    else:
        S3 = raw_density

    # --------------------------
    # Final Risk Score
    # --------------------------
    final_score = (ALPHA * S1) + (BETA * S2) + (GAMMA * S3)
    risk_percentage = min(round(final_score * 100, 2), 100.0)

    return {
        "risk_percentage": risk_percentage,
        "S1_severity": round(S1, 3),
        "S2_diversity": round(S2, 3),
        "S3_density": round(S3, 3)
    }