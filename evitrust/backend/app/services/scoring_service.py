def score(signals: dict) -> tuple[int, str, float, float]:
    total = 0
    total += 10 if signals.get("exif_missing") else 0
    total += int(min(max(signals.get("ela_mean", 0), 0), 1) * 25)
    total += int(min(max(signals.get("noise_inconsistency", 0), 0), 1) * 25)
    total += int(min(max(signals.get("video_frame_inconsistency", 0), 0), 1) * 25)
    total += int(min(max(signals.get("audio_spectral_anomaly", 0), 0), 1) * 25)
    total = min(100, max(0, total))
    level = "LOW" if total <= 33 else "MEDIUM" if total <= 66 else "HIGH"
    present = sum(1 for k,v in signals.items() if v)
    confidence = round(min(0.95, 0.35 + present * 0.1), 2)
    uncertainty = round(max(0.05, 1 - confidence), 2)
    return total, level, confidence, uncertainty
