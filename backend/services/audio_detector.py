import os
import numpy as np
import librosa
import tensorflow as tf

from spafe.features.lfcc import lfcc
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "audio_fusion_cnn_bilstm_model.h5"
)

SCALER_MEAN_PATH = os.path.join(BASE_DIR, "models", "scaler_mean.npy")
SCALER_SCALE_PATH = os.path.join(BASE_DIR, "models", "scaler_scale.npy")

SAMPLE_RATE = 16000
MAX_FRAMES = 100
NUM_CEPS = 20
NUM_FILTERS = 70
THRESHOLD = 0.5

PARAMETER_NAMES = [
    "spectral_centroid_mean",
    "spectral_centroid_std",
    "spectral_bandwidth_mean",
    "spectral_bandwidth_std",
    "spectral_rolloff_mean",
    "spectral_rolloff_std",
    "spectral_flatness_mean",
    "spectral_flatness_std",
    "zero_crossing_rate_mean",
    "zero_crossing_rate_std",
    "rms_energy_mean",
    "rms_energy_std",
    "entropy",
    "variance",
    "pitch_mean",
    "pitch_std",
    "pitch_range",
    "pause_ratio",
    "amplitude_discontinuity",
    "phase_variance",
    "phase_discontinuity",
    "noise_floor",
    "energy_variation",
    "tempo",
    "chroma_mean",
    "chroma_std",
    "audio_duration"
]

try:
    audio_model = load_model(MODEL_PATH, compile=False)
    print("✅ Audio Fusion CNN-BiLSTM Model Loaded")
except Exception as e:
    print("❌ Audio Model Loading Failed:", e)
    audio_model = None

try:
    SCALER_MEAN = np.load(SCALER_MEAN_PATH)
    SCALER_SCALE = np.load(SCALER_SCALE_PATH)
    SCALER_SCALE = np.where(SCALER_SCALE == 0, 1, SCALER_SCALE)
    print("✅ Audio parameter scaler loaded")
except Exception:
    SCALER_MEAN = np.zeros(27)
    SCALER_SCALE = np.ones(27)
    print("⚠️ Audio scaler not found. Using default scaler.")


def safe_mean(x):
    return float(np.mean(x)) if len(x) > 0 else 0.0


def safe_std(x):
    return float(np.std(x)) if len(x) > 0 else 0.0


def calculate_entropy(signal):
    hist, _ = np.histogram(signal, bins=50, density=True)
    hist = hist + 1e-8
    return float(-np.sum(hist * np.log2(hist)))


def load_audio(file_path):
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)

    if len(audio) == 0:
        raise ValueError("Empty audio file")

    return audio


def extract_lfcc_features(audio):
    features = lfcc(
        sig=audio,
        fs=SAMPLE_RATE,
        num_ceps=NUM_CEPS,
        nfilts=NUM_FILTERS
    )

    if features.shape[0] < MAX_FRAMES:
        pad_len = MAX_FRAMES - features.shape[0]
        features = np.pad(features, ((0, pad_len), (0, 0)), mode="constant")
    else:
        features = features[:MAX_FRAMES, :]

    features = features.astype(np.float32)
    features = np.expand_dims(features, axis=0)
    features = np.expand_dims(features, axis=-1)

    return features


def extract_audio_parameters(audio):
    try:
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=SAMPLE_RATE)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=SAMPLE_RATE)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=SAMPLE_RATE)[0]
        spectral_flatness = librosa.feature.spectral_flatness(y=audio)[0]

        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        rms = librosa.feature.rms(y=audio)[0]

        entropy = calculate_entropy(audio)
        variance = float(np.var(audio))

        try:
            pitch = librosa.yin(audio, fmin=50, fmax=500, sr=SAMPLE_RATE)
            pitch = pitch[np.isfinite(pitch)]
            pitch_mean = safe_mean(pitch)
            pitch_std = safe_std(pitch)
            pitch_range = float(np.max(pitch) - np.min(pitch)) if len(pitch) > 0 else 0.0
        except Exception:
            pitch_mean = 0.0
            pitch_std = 0.0
            pitch_range = 0.0

        pause_ratio = float(np.mean(np.abs(audio) < 0.02))

        amplitude_diff = np.diff(audio)
        amplitude_discontinuity = float(np.mean(np.abs(amplitude_diff)))

        stft = librosa.stft(audio)
        phase = np.angle(stft)

        phase_variance = float(np.var(phase))
        phase_discontinuity = float(np.mean(np.abs(np.diff(phase, axis=1))))

        noise_floor = float(np.percentile(np.abs(audio), 10))
        energy_variation = safe_std(rms)

        try:
            tempo, _ = librosa.beat.beat_track(y=audio, sr=SAMPLE_RATE)
            tempo = float(tempo)
        except Exception:
            tempo = 0.0

        chroma = librosa.feature.chroma_stft(y=audio, sr=SAMPLE_RATE)

        parameters = [
            safe_mean(spectral_centroid),
            safe_std(spectral_centroid),
            safe_mean(spectral_bandwidth),
            safe_std(spectral_bandwidth),
            safe_mean(spectral_rolloff),
            safe_std(spectral_rolloff),
            safe_mean(spectral_flatness),
            safe_std(spectral_flatness),
            safe_mean(zcr),
            safe_std(zcr),
            safe_mean(rms),
            safe_std(rms),
            entropy,
            variance,
            pitch_mean,
            pitch_std,
            pitch_range,
            pause_ratio,
            amplitude_discontinuity,
            phase_variance,
            phase_discontinuity,
            noise_floor,
            energy_variation,
            tempo,
            float(np.mean(chroma)),
            float(np.std(chroma)),
            float(len(audio) / SAMPLE_RATE)
        ]

        return np.array(parameters, dtype=np.float32)

    except Exception as e:
        print("Audio parameter extraction error:", e)
        return np.zeros(27, dtype=np.float32)


def scale_parameters(params):
    scaled = (params - SCALER_MEAN) / SCALER_SCALE
    return scaled.astype(np.float32).reshape(1, -1)


def risk_level(score):
    if score >= 75:
        return "HIGH"
    if score >= 45:
        return "MEDIUM"
    return "LOW"


def analyze_audio_model(file_path):
    if audio_model is None:
        return {
            "error": "Audio model not loaded"
        }

    audio = load_audio(file_path)

    lfcc_features = extract_lfcc_features(audio)
    raw_parameters = extract_audio_parameters(audio)
    scaled_parameters = scale_parameters(raw_parameters)

    probability_real = float(
        audio_model.predict(
            [lfcc_features, scaled_parameters],
            verbose=0
        )[0][0]
    )
    probability_fake = 1 - probability_real

    print("=" * 50)
    print("DEBUG AUDIO MODEL")
    print("Probability Real:", probability_real)
    print("Probability Fake:", probability_fake)
    print("Raw Parameters Shape:", raw_parameters.shape)
    print("Scaled Parameters Shape:", scaled_parameters.shape)
    print("First 5 Raw Params:", raw_parameters[:5])
    print("First 5 Scaled Params:", scaled_parameters.flatten()[:5])
    print("=" * 50)

    if probability_real >= THRESHOLD:
        prediction = "REAL"
        confidence = probability_real * 100
    else:
        prediction = "FAKE"
        confidence = probability_fake * 100
    return {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "raw_probability_real": round(probability_real, 4),
        "raw_probability_fake": round(probability_fake, 4),
        "risk_level": risk_level(probability_fake * 100),
        "risk_score": round(probability_fake * 100, 2),
        "raw_parameters": raw_parameters,
        "scaled_parameters": scaled_parameters.flatten(),
        "parameter_names": PARAMETER_NAMES
    }