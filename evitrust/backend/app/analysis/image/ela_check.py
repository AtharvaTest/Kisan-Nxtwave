from app.services.storage_service import storage_service

def run_ela_check(evidence: dict) -> tuple[dict, dict]:
    heatmap_key = f"{evidence['case_id']}/{evidence['_id']}/artifacts/ela.png"
    storage_service.upload_bytes(heatmap_key, b"placeholder-ela", "image/png")
    return {"ela_mean": 0.42}, {"ela_heatmap_key": heatmap_key}
