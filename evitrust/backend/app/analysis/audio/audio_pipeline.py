from app.analysis.audio.spectral_check import spectral_anomaly

def run_audio_pipeline(_: dict):
    signals = {
        "exif_missing": False,
        "ela_mean": 0.0,
        "noise_inconsistency": 0.0,
        "video_frame_inconsistency": 0.0,
        "audio_spectral_anomaly": spectral_anomaly(b""),
    }
    return signals, {"ela_heatmap_key": None, "frames_sample_keys": []}
