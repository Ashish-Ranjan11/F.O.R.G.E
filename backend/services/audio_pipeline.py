from backend.services.audio_detector import analyze_audio_model
from backend.services.audio_xai import build_audio_xai
from backend.services.audio_visualizer import generate_audio_visuals


def process_audio(file_path):
    model_result = analyze_audio_model(file_path)

    if "error" in model_result:
        return model_result

    raw_params = model_result["raw_parameters"]
    fake_probability = model_result["raw_probability_fake"]

    parameter_contribution, suspicious_segments = build_audio_xai(
        raw_params,
        model_result["confidence"],
        fake_probability
    )

    visuals = generate_audio_visuals(file_path)

    result = {
        "modality": "audio",
        "prediction": model_result["prediction"],
        "confidence": model_result["confidence"],
        "risk_level": model_result["risk_level"],
        "risk_score": model_result["risk_score"],
        "recommendation": (
            "Suspicious synthetic audio patterns detected. Additional forensic review advised."
            if model_result["prediction"] == "FAKE"
            else
            "Audio appears natural, but manual review is recommended for high-stakes use."
        ),
        "parameter_contribution": parameter_contribution,
        "suspicious_segments": suspicious_segments,
        "waveform": visuals["waveform"],
        "spectrogram": visuals["spectrogram"],
        "audio_heatmap": visuals["audio_heatmap"],
        "raw_probability_real": model_result["raw_probability_real"],
        "raw_probability_fake": model_result["raw_probability_fake"]
    }

    return result