from app.risk_definitions import RISK_CATEGORIES
from app.config import ALPHA, BETA, GAMMA

def compute_risk(detected_categories, risky_sentence_count, total_sentences):

    # --------------------------
    # S1: Severity (Relative to Max Weight)
    # --------------------------
    # Instead of sum, we look at how severe the found risks are 
    # compared to the highest possible weight (usually 5).
    max_possible_weight = 5.0 
    if detected_categories:
        highest_weight_found = max(RISK_CATEGORIES[cat]["weight"] for cat in detected_categories)
        S1 = highest_weight_found / max_possible_weight
    else:
        S1 = 0

    # --------------------------
    # S2: Diversity
    # --------------------------
    M = len(RISK_CATEGORIES)
    K = len(detected_categories)
    S2 = K / M if M else 0

    # --------------------------
    # S3: Density (With a "Floor" for long docs)
    # --------------------------
    raw_density = risky_sentence_count / total_sentences if total_sentences else 0
    
    # If we found at least 2 dangerous things, don't let density drop to 0.
    # This ensures a long contract with 'hidden' traps still scores high.
    if risky_sentence_count >= 2:
        S3 = max(raw_density, 0.5) 
    else:
        S3 = raw_density

    # --------------------------
    # Final Risk Score
    # --------------------------
    final_score = (ALPHA * S1) + (BETA * S2) + (GAMMA * S3)

    # Cap the score at 100%
    risk_percentage = min(round(final_score * 100, 2), 100.0)

    return {
        "risk_percentage": risk_percentage,
        "S1_severity": round(S1, 3),
        "S2_diversity": round(S2, 3),
        "S3_density": round(S3, 3)
    }

"""
Final Risk = (α * Severity) + (β * Diversity) + (γ * Density)
Where:
- α = 0.6, β = 0.3, γ = 0.1
- Severity is based on the highest weight found.
- Density includes a floor of 0.5 for multi-risk documents.
"""