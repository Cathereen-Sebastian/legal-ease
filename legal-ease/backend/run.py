import sys
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. SETUP THE PATH
# This ensures that even if you move the project, Python finds the 'app' folder
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. THE IMPORT
# Because it's app >> services >> risk_scorer
try:
    from app.services.risk_scorer import compute_risk
    print("✅ Connection established: Backend logic loaded.")
except ImportError as e:
    print(f"❌ Path Error: Could not find the risk_scorer. {e}")
    sys.exit(1)

app = FastAPI()

# 3. CORS (Security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. THE API ENDPOINT
@app.post("/analyze")
async def analyze_document(payload: dict):
    # This is what your Frontend will talk to
    text_data = payload.get("text", "")
    
    # For now, we use your compute_risk function with sample numbers
    # Once your NLP logic is fully integrated, replace these variables
    sample_categories = ["Liability", "Privacy"]
    sample_risky_count = 3
    sample_total_sentences = 20
    
    result = compute_risk(sample_categories, sample_risky_count, sample_total_sentences)
    return result

if __name__ == "__main__":
    print("🚀 FastAPI is starting on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)