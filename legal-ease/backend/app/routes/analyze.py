# app/routes/analyze.py

from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.nlp_service import extract_sentences
from app.services.clause_detector import detect_clauses
from app.services.risk_scorer import compute_risk
from app.models.risk_level import classify_risk
from app.services.mandatory_permissions import get_mandatory_permissions, PERMISSION_EXPLANATIONS

router = APIRouter()

def adjust_clauses(risky_clauses, app_type: str):
    """
    Adjust clauses based on mandatory permissions:
    - Mandatory permissions → informational + friendly explanation
    - Others → risky + warning
    """
    mandatory = get_mandatory_permissions(app_type)
    adjusted = []

    for clause in risky_clauses:
        clause_dict = clause.__dict__.copy()
        if clause.category in mandatory:
            clause_dict["type"] = "informational"
            explanation = PERMISSION_EXPLANATIONS.get(clause.category, "")
            clause_dict["message"] = f"{explanation} (Expected for {app_type.replace('_',' ').title()} apps)"
        else:
            clause_dict["type"] = "risky"
            clause_dict["message"] = f"Warning: {clause.explanation}"

        adjusted.append(clause_dict)

    return adjusted

# ---------------- Text Analysis ----------------
@router.post("/analyze-text/")
async def analyze_text(text: str, app_type: str = "generic"):

    sentences = extract_sentences(text)
    detected_categories, risky_clauses, risky_count = detect_clauses(sentences)
    adjusted_clauses = adjust_clauses(risky_clauses, app_type)

    risk_data = compute_risk(
        detected_categories,
        risky_count,
        len(sentences)
    )

    risk_level = classify_risk(risk_data["risk_percentage"])

    return {
        **risk_data,
        "risk_level": risk_level,
        "detected_categories": list(detected_categories),
        "risky_clauses": adjusted_clauses,
        "app_type": app_type
    }

# ---------------- PDF Analysis ----------------
@router.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...), app_type: str = "generic"):

    text = extract_text_from_pdf(file.file)
    sentences = extract_sentences(text)
    detected_categories, risky_clauses, risky_count = detect_clauses(sentences)
    adjusted_clauses = adjust_clauses(risky_clauses, app_type)

    risk_data = compute_risk(
        detected_categories,
        risky_count,
        len(sentences)
    )

    risk_level = classify_risk(risk_data["risk_percentage"])

    return {
        **risk_data,
        "risk_level": risk_level,
        "detected_categories": list(detected_categories),
        "risky_clauses": adjusted_clauses,
        "app_type": app_type
    }