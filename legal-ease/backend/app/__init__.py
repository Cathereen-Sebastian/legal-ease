"""
Initializes FastAPI application and registers routes.
Includes CORS middleware for frontend communication.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router

app = FastAPI(title="Legal-Ease Risk Analyzer")

# Enable CORS (for HTML/JS frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze_router)