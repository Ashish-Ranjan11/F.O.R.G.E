import numpy as np
import joblib
import shap
import re
import string

from nltk import word_tokenize, pos_tag
from textstat import flesch_reading_ease
from sentence_transformers import SentenceTransformer

from backend.xai.parameter_reasoning import (
    stylometric_reason,
    tfidf_reason,
    ngram_reason,
    semantic_reason
)

from backend.xai.sentence_highlighter import (
    analyze_document
)

# ==========================================
# LOAD MODELS
# ==========================================

print("Loading Models...")

model = joblib.load("models/final_text_model.pkl")
tfidf = joblib.load("models/tf_idf.pkl")
ngram = joblib.load("models/n_gram.pkl")

sbert_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

explainer = shap.TreeExplainer(model)

print("Models Loaded")

# ==========================================
# STYLOMETRIC
# ==========================================

def extract_stylometric(text):

    try:

        words = word_tokenize(text)

        sentences = re.split(
            r"[.!?]",
            text
        )

        sent_lengths = [
            len(s.split())
            for s in sentences
            if s.strip() != ""
        ]

        sent_var = (
            np.var(sent_lengths)
            if len(sent_lengths) > 0
            else 0
        )

        word_freq = len(words)

        punct_count = sum(
            1 for c in text
            if c in string.punctuation
        )

        pos_tags = pos_tag(words)

        noun_count = sum(
            1 for _, t in pos_tags
            if "NN" in t
        )

        verb_count = sum(
            1 for _, t in pos_tags
            if "VB" in t
        )

        readability = flesch_reading_ease(text)

        return [
            float(sent_var),
            float(word_freq),
            float(punct_count),
            float(noun_count),
            float(verb_count),
            float(readability)
        ]

    except Exception:

        return [0, 0, 0, 0, 0, 0]

# ==========================================
# BALANCING HELPERS
# ==========================================

def normalize_to_total(scores):

    total = sum(scores.values())

    if total <= 0:

        return {
            key: 25.0
            for key in scores
        }

    return {
        key: round(
            (value / total) * 100,
            2
        )
        for key, value in scores.items()
    }


def cap_and_redistribute(scores, max_cap=40):

    capped = {}
    overflow = 0
    under_cap_keys = []

    for key, value in scores.items():

        if value > max_cap:
            capped[key] = max_cap
            overflow += value - max_cap
        else:
            capped[key] = value
            under_cap_keys.append(key)

    if overflow > 0 and under_cap_keys:

        add_each = overflow / len(under_cap_keys)

        for key in under_cap_keys:
            capped[key] += add_each

    return normalize_to_total(capped)


def get_balanced_parameter_scores(
    stylometric_val,
    tfidf_val,
    ngram_val,
    semantic_val
):

    raw_scores = {
        "stylometric": float(stylometric_val),
        "tfidf": float(tfidf_val),
        "ngram": float(ngram_val),
        "semantic": float(semantic_val)
    }

    normalized = normalize_to_total(raw_scores)

    balanced = cap_and_redistribute(
        normalized,
        max_cap=40
    )

    return balanced

# ==========================================
# MAIN PIPELINE
# ==========================================

def analyze_text(text):

    stylometric = np.array([
        extract_stylometric(text)
    ])

    tfidf_features = tfidf.transform(
        [text]
    ).toarray()

    ngram_features = ngram.transform(
        [text]
    ).toarray()

    embeddings = sbert_model.encode(
        [text]
    )

    X = np.hstack([
        stylometric,
        tfidf_features,
        ngram_features,
        embeddings
    ])

    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0]

    confidence = round(
        float(np.max(probability)) * 100,
        2
    )

    # ======================================
    # SHAP VALUES
    # ======================================

    raw_shap = explainer.shap_values(X)

    if isinstance(raw_shap, list):
        shap_values = raw_shap[0]
    else:
        shap_values = raw_shap

    shap_val = np.abs(
        shap_values[0]
    )

    total = np.sum(shap_val)

    if total == 0:
        scaled = np.zeros_like(shap_val)
    else:
        scaled = (shap_val / total) * 100

    # ======================================
    # FEATURE LENGTHS
    # ======================================

    stylometric_len = stylometric.shape[1]
    tfidf_len = tfidf_features.shape[1]
    ngram_len = ngram_features.shape[1]

    stylometric_val = np.sum(
        scaled[:stylometric_len]
    )

    tfidf_val = np.sum(
        scaled[
            stylometric_len:
            stylometric_len + tfidf_len
        ]
    )

    ngram_val = np.sum(
        scaled[
            stylometric_len + tfidf_len:
            stylometric_len + tfidf_len + ngram_len
        ]
    )

    semantic_val = np.sum(
        scaled[
            stylometric_len + tfidf_len + ngram_len:
        ]
    )

    balanced_scores = get_balanced_parameter_scores(
        stylometric_val,
        tfidf_val,
        ngram_val,
        semantic_val
    )

    # ======================================
    # REASONING
    # ======================================

    parameter_contribution = {
        "stylometric": stylometric_reason(
            float(balanced_scores["stylometric"])
        ),

        "tfidf": tfidf_reason(
            float(balanced_scores["tfidf"])
        ),

        "ngram": ngram_reason(
            float(balanced_scores["ngram"])
        ),

        "semantic": semantic_reason(
            float(balanced_scores["semantic"])
        )
    }

    # ======================================
    # SENTENCE ANALYSIS / TEXT HEATMAP
    # ======================================

    highlighted_document = analyze_document(
        text
    )

    return {
        "prediction": (
            "AI"
            if prediction == 1
            else "Human"
        ),

        "confidence": confidence,

        "risk_score": confidence,

        "risk_level": (
            "HIGH"
            if confidence >= 75
            else "MEDIUM"
            if confidence >= 45
            else "LOW"
        ),

        "parameter_contribution": parameter_contribution,

        "highlighted_document": highlighted_document,

        "full_document": highlighted_document
    }