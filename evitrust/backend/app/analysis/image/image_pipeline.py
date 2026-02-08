from app.analysis.image.exif_check import run_exif_check
from app.analysis.image.ela_check import run_ela_check
from app.analysis.image.noise_check import run_noise_check

def run_image_pipeline(evidence: dict):
    signals = {}
    signals.update(run_exif_check(b""))
    ela, artifacts = run_ela_check(evidence)
    signals.update(ela)
    signals.update(run_noise_check(b""))
    signals.setdefault("video_frame_inconsistency", 0.0)
    signals.setdefault("audio_spectral_anomaly", 0.0)
    return signals, {**artifacts, "frames_sample_keys": []}
