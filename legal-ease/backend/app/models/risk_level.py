"""
Classifies final risk percentage into levels.
"""

from app.config import LOW_THRESHOLD, HIGH_THRESHOLD

def classify_risk(score: float) -> str:
    if score < LOW_THRESHOLD:
        return "Low Risk"
    elif score < HIGH_THRESHOLD:
        return "Moderate Risk"
    else:
        return "High Risk"