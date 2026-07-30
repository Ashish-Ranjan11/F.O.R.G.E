from pathlib import Path

# --------------------------------------------------
# Backend Root
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

# --------------------------------------------------
# Model
# --------------------------------------------------

MODEL_PATH = BASE_DIR / "models" / "video_model.pth"

# Change this if your model filename is different.

# --------------------------------------------------
# Video
# --------------------------------------------------

SEQUENCE_LENGTH = 30

IMAGE_SIZE = (224, 224)

FRAME_SAMPLE_RATE = 2

# --------------------------------------------------
# CNN Feature Size
# --------------------------------------------------

CNN_FEATURE_SIZE = 1280

# --------------------------------------------------
# Number of handcrafted forensic features
# --------------------------------------------------

FORENSIC_FEATURES = 11

# --------------------------------------------------
# Total feature vector
# --------------------------------------------------

TOTAL_FEATURE_SIZE = CNN_FEATURE_SIZE + FORENSIC_FEATURES