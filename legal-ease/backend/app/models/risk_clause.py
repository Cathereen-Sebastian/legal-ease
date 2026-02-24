"""
Represents a detected risky clause.
"""

from pydantic import BaseModel

class RiskClause(BaseModel):
    sentence: str
    category: str
    explanation: str