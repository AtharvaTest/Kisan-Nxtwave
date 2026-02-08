def explain(signals: dict, risk_level: str) -> dict:
    reasons = []
    if signals.get("exif_missing"):
        reasons.append({"title": "Missing metadata", "detail": "EXIF metadata absent.", "severity": "MEDIUM"})
    if signals.get("ela_mean", 0) > 0.35:
        reasons.append({"title": "Compression anomalies", "detail": "ELA suggests uneven recompression.", "severity": "HIGH"})
    if signals.get("noise_inconsistency", 0) > 0.4:
        reasons.append({"title": "Noise inconsistency", "detail": "Patch noise profile mismatch.", "severity": "MEDIUM"})
    if signals.get("video_frame_inconsistency", 0) > 0.4:
        reasons.append({"title": "Temporal anomalies", "detail": "Frame-level changes abrupt over time.", "severity": "MEDIUM"})
    if signals.get("audio_spectral_anomaly", 0) > 0.4:
        reasons.append({"title": "Spectral irregularities", "detail": "Audio frequency structure shows discontinuity.", "severity": "HIGH"})
    reasons = reasons[:6]
    rec = "FLAG" if risk_level != "LOW" else "ACCEPT"
    return {
        "summary": f"{risk_level} risk indication based on forensic signals.",
        "reasons": reasons or [{"title": "No major anomalies", "detail": "Signals remain in expected range.", "severity": "LOW"}],
        "limitations": [
            "Low-quality media increases uncertainty.",
            "This system does not prove real-world truth.",
            "Domain expert review is required for legal interpretation.",
        ],
        "recommended_action": rec,
    }
