# app/routes/analyze.py

from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

from app.services.pdf_service import extract_text_from_pdf
from app.services.nlp_service import extract_sentences
from app.services.clause_detector import detect_clauses
from app.services.risk_scorer import compute_risk
from app.models.risk_level import classify_risk

# ---- Import mandatory permissions ----
from app.services.mandatory_permissions import MANDATORY_PERMISSIONS, PERMISSION_EXPLANATIONS
router = APIRouter()

# -------- REQUEST MODEL --------
class TextInput(BaseModel):
    text: str
    category: str | None = None  # app type


# -------- SUMMARY GENERATOR --------
def generate_summary(detected_categories, risk_level, risky_clauses):
    if not risky_clauses:
        return "This document appears mostly safe. No major risky clauses were detected."

    categories = ", ".join(detected_categories)

    summary = f"This document has a {risk_level.lower()} level of legal risk. "
    summary += f"It contains clauses related to {categories}. "
    summary += "These clauses may affect your rights, limit liability, or allow data sharing. "
    summary += "You should review these sections carefully before accepting the agreement."

    return summary


# -------- UTILITY: Get mandatory permissions --------
def get_mandatory_permissions(app_type: str):
    perms = MANDATORY_PERMISSIONS.get(app_type, [])
    # Include friendly explanation for each permission
    return {perm: PERMISSION_EXPLANATIONS.get(perm, "No description available") for perm in perms}


# -------- TEXT ANALYSIS --------
@router.post("/analyze-text/")
async def analyze_text(input_data: TextInput):
    text = input_data.text
    app_type = input_data.category or "other"

    sentences = extract_sentences(text)
    detected_categories, risky_clauses, risky_count = detect_clauses(sentences)

    # Compute overall document risk
    risk_data = compute_risk(detected_categories, risky_count, len(sentences))
    overall_risk_level = classify_risk(risk_data["risk_percentage"])

    # Compute risk per clause
    per_clause_clauses = []
    for c in risky_clauses:
        clause_risk_score = compute_risk([c.category], 1, 1)["risk_percentage"]
        clause_risk_level = classify_risk(clause_risk_score).lower()
        per_clause_clauses.append({
            "category": c.category,
            "clause": c.sentence,
            "note": c.explanation,
            "risk_level": clause_risk_level
        })

    summary = generate_summary(detected_categories, overall_risk_level, risky_clauses)

    # ---- Add mandatory permissions ----
    mandatory_permissions = get_mandatory_permissions(app_type)

    return {
        **risk_data,
        "risk_level": overall_risk_level,
        "summary": summary,
        "detected_categories": list(detected_categories),
        "risky_clauses": per_clause_clauses,
        "mandatory_permissions": mandatory_permissions
    }


# -------- PDF ANALYSIS --------
@router.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...), app_type: str = Form("other")):
    text = extract_text_from_pdf(file.file)
    sentences = extract_sentences(text)
    detected_categories, risky_clauses, risky_count = detect_clauses(sentences)

    # Compute overall document risk
    risk_data = compute_risk(detected_categories, risky_count, len(sentences))
    overall_risk_level = classify_risk(risk_data["risk_percentage"])

    # Compute risk per clause
    per_clause_clauses = []
    for c in risky_clauses:
        clause_risk_score = compute_risk([c.category], 1, 1)["risk_percentage"]
        clause_risk_level = classify_risk(clause_risk_score).lower()
        per_clause_clauses.append({
            "category": c.category,
            "clause": c.sentence,
            "note": c.explanation,
            "risk_level": clause_risk_level
        })

    summary = generate_summary(detected_categories, overall_risk_level, risky_clauses)

    # ---- Add mandatory permissions ----
    mandatory_permissions = get_mandatory_permissions(app_type)

    return {
        **risk_data,
        "risk_level": overall_risk_level,
        "summary": summary,
        "detected_categories": list(detected_categories),
        "risky_clauses": per_clause_clauses,
        "mandatory_permissions": mandatory_permissions
    }