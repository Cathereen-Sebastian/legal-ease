"""
API Routes for Legal Risk Analysis
"""

from fastapi import APIRouter, UploadFile, File
from app.services.pdf_service import extract_text_from_pdf
from app.services.nlp_service import extract_sentences
from app.services.clause_detector import detect_clauses
from app.services.risk_scorer import compute_risk
from app.models.risk_level import classify_risk

router = APIRouter()


@router.post("/analyze-text/")
async def analyze_text(text: str):

    sentences = extract_sentences(text)

    detected_categories, risky_clauses, risky_count = detect_clauses(sentences)

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
        "risky_clauses": risky_clauses
    }


@router.post("/analyze-pdf/")
async def analyze_pdf(file: UploadFile = File(...)):

    text = extract_text_from_pdf(file.file)
    sentences = extract_sentences(text)

    detected_categories, risky_clauses, risky_count = detect_clauses(sentences)

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
        "risky_clauses": risky_clauses
    }