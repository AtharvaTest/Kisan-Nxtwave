from app.analysis.video.frame_extract import extract_frames

def run_video_pipeline(evidence: dict):
    frames = extract_frames(evidence)
    signals = {
        "exif_missing": False,
        "ela_mean": 0.21,
        "noise_inconsistency": 0.19,
        "video_frame_inconsistency": 0.46,
        "audio_spectral_anomaly": 0.0,
    }
    return signals, {"ela_heatmap_key": None, "frames_sample_keys": frames}
