from pydantic import BaseModel

class RiskClause(BaseModel):
    sentence: str
    category: str
    explanation: str
    type: str = "risky"      # default is "risky"
    message: str = ""         # optional message