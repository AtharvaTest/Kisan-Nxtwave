from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    job_id: str


class AnalysisOut(BaseModel):
    _id: str
    evidence_id: str
    risk_score: int
    risk_level: str
    confidence: float
    uncertainty: float
    signals: dict
    explanations: dict
    artifacts: dict
    created_at: str
