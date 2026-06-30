import pandas as pd
import numpy as np
import re
import joblib
import os
from sentence_analyzer import SentenceAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


# =====================================================
# 1. LOAD DATASETS
# =====================================================

print("\nLoading datasets...\n")




# =====================================================
#

# =====================================================
# 3. FIX COLUMN NAMES


# =====================================================
# 10. TEXT CLEANING FUNCTION
# =====================================================

def clean_text(text):

    text = str(text).lower()

    # remove URLs
    text = re.sub(r"http\S+", "", text)

    # remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# 11. APPLY CLEANING
# =====================================================

print("\nCleaning text...")

df["clean_text"] = df[TEXT_COLUMN].apply(clean_text)


# =====================================================
# 12. TF-IDF FEATURE EXTRACTION
# =====================================================

print("\nExtracting TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words='english'
)

X = vectorizer.fit_transform(df["clean_text"])

y = df["label"]


# =====================================================
# 13. TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =====================================================
# 14. TRAIN MODEL
# =====================================================

print("\nTraining model...")

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)


# =====================================================
# 15. MAKE PREDICTIONS
# =====================================================

print("\nMaking predictions...")

predictions = model.predict(X_test)


# =====================================================
# 16. EVALUATE MODEL
# =====================================================

accuracy = accuracy_score(y_test, predictions)

print("\n===================================")
print("MODEL ACCURACY:")
print(accuracy)
print("===================================")

print("\nCLASSIFICATION REPORT:\n")

print(classification_report(y_test, predictions))


# =====================================================
# 17. CREATE MODELS FOLDER
# =====================================================

print("\nSaving model...")

# remove file named models if it exists
if os.path.isfile("models"):
    os.remove("models")

# create models folder
os.makedirs("models", exist_ok=True)


# =====================================================
# 18. SAVE MODEL & VECTORIZER
# =====================================================

joblib.dump(model, "models/forgery_detector.pkl")

joblib.dump(vectorizer, "models/vectorizer.pkl")

print("\nModel saved successfully!")


# =====================================================
# 19. LIVE TEXT TESTING
# =====================================================

print("\n===================================")
print("LIVE TEXT TESTING")
print("Type 'exit' to stop")
print("===================================")

while True:

    user_input = input("\nEnter text: ")

    if user_input.lower() == "exit":
        print("\nExiting...")
        break

    # clean input
    cleaned_input = clean_text(user_input)

    # convert to vector
    vector_input = vectorizer.transform([cleaned_input])

    # prediction
    prediction = model.predict(vector_input)[0]

    # probabilities
    probabilities = model.predict_proba(vector_input)[0]

    human_probability = probabilities[0]
    ai_probability = probabilities[1]

    # determine label
    if prediction == 1:
        label = "AI-GENERATED / FORGED"
    else:
        label = "HUMAN-WRITTEN"

    # confidence interpretation
    if ai_probability > 0.90:
        confidence = "VERY HIGH"

    elif ai_probability > 0.75:
        confidence = "HIGH"

    elif ai_probability > 0.60:
        confidence = "MODERATE"

    else:
        confidence = "LOW"

    # print results
    print("\n========== RESULT ==========")

    print(f"Prediction: {label}")

    print(f"AI Probability: {ai_probability:.4f}")

    print(f"Human Probability: {human_probability:.4f}")

    print(f"Confidence Level: {confidence}")

    # interpretation
    if prediction == 1:

        if ai_probability > 0.90:
            print("Interpretation: Text strongly resembles AI-generated writing.")

        elif ai_probability > 0.75:
            print("Interpretation: Text shows significant AI-generated characteristics.")

        elif ai_probability > 0.60:
            print("Interpretation: Text contains moderate AI-like writing patterns.")

        else:
            print("Interpretation: Weak AI-generated indicators detected.")

    else:

        if human_probability > 0.90:
            print("Interpretation: Text strongly resembles human-written content.")

        else:
            print("Interpretation: Text appears more human-written than AI-generated.")

    print("============================")
