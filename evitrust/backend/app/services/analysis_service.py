from datetime import datetime, timezone
from app.repositories.evidence_repo import evidence_repo
from app.repositories.analysis_repo import analysis_repo
from app.services.scoring_service import score
from app.services.explain_service import explain
from app.analysis.image.image_pipeline import run_image_pipeline
from app.analysis.video.video_pipeline import run_video_pipeline
from app.analysis.audio.audio_pipeline import run_audio_pipeline

class AnalysisService:
    def analyze_evidence(self, evidence: dict):
        if evidence["type"] == "IMAGE":
            signals, artifacts = run_image_pipeline(evidence)
        elif evidence["type"] == "VIDEO":
            signals, artifacts = run_video_pipeline(evidence)
        else:
            signals, artifacts = run_audio_pipeline(evidence)
        risk_score, risk_level, confidence, uncertainty = score(signals)
        explanations = explain(signals, risk_level)
        doc = {
            "_id": evidence["_id"] + "-analysis",
            "evidence_id": evidence["_id"],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence": confidence,
            "uncertainty": uncertainty,
            "signals": signals,
            "explanations": explanations,
            "artifacts": artifacts,
        }
        evidence_repo.update_status(evidence["_id"], "ANALYZED")
        return analysis_repo.create(doc)

analysis_service = AnalysisService()
