import re
import numpy as np
import joblib
import string

from nltk import word_tokenize, pos_tag
from textstat import flesch_reading_ease
from sentence_transformers import SentenceTransformer

# ==========================================
# LOAD MODELS
# ==========================================

model = joblib.load(
    "models/final_text_model.pkl"
)

tfidf = joblib.load(
    "models/tf_idf.pkl"
)

ngram = joblib.load(
    "models/n_gram.pkl"
)

sbert_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ==========================================
# COLOR ENGINE
# ==========================================

def classify_sentence(score):

    if score >= 85:

        return {
            "risk": "VERY HIGH",
            "color": "red"
        }

    elif score >= 60:

        return {
            "risk": "HIGH",
            "color": "orange"
        }

    elif score >= 40:

        return {
            "risk": "MEDIUM",
            "color": "yellow"
        }

    return {
        "risk": "LOW",
        "color": "green"
    }

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
            1 for _, tag in pos_tags
            if "NN" in tag
        )

        verb_count = sum(
            1 for _, tag in pos_tags
            if "VB" in tag
        )

        readability = (
            flesch_reading_ease(text)
        )

        return [
            float(sent_var),
            float(word_freq),
            float(punct_count),
            float(noun_count),
            float(verb_count),
            float(readability)
        ]

    except:

        return [0, 0, 0, 0, 0, 0]

# ==========================================
# REAL SENTENCE ANALYSIS
# ==========================================

def analyze_document(text):

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    results = []

    for sentence in sentences:

        sentence = sentence.strip()

        if len(sentence) < 5:
            continue

        try:

            # ======================================
            # FEATURES
            # ======================================

            stylometric = np.array([
                extract_stylometric(sentence)
            ])

            tfidf_features = tfidf.transform(
                [sentence]
            ).toarray()

            ngram_features = ngram.transform(
                [sentence]
            ).toarray()

            embeddings = sbert_model.encode(
                [sentence]
            )

            X = np.hstack([
                stylometric,
                tfidf_features,
                ngram_features,
                embeddings
            ])

            # ======================================
            # REAL MODEL PREDICTION
            # ======================================

            probability = model.predict_proba(X)[0]

            ai_score = round(
                float(probability[1]) * 100,
                2
            )

            classification = classify_sentence(
                ai_score
            )

            # ======================================
            # REASONING
            # ======================================

            if ai_score >= 85:

                reason = (
                    "Strong AI generation patterns detected"
                )

            elif ai_score >= 60:

                reason = (
                    "Sentence structure resembles AI-generated content"
                )

            elif ai_score >= 40:

                reason = (
                    "Moderate AI indicators detected"
                )

            else:

                reason = (
                    "Natural human-like writing detected"
                )

            # ======================================
            # SAVE
            # ======================================

            results.append({

                "sentence": sentence,

                "score": ai_score,

                "risk": classification["risk"],

                "color": classification["color"],

                "reason": reason
            })

        except Exception as e:

            print("Sentence Error:", e)

    return results