from pathlib import Path

# -------------------------------------------------------
# Video Engine Configuration
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
FRAME_DIR = BASE_DIR / "frames"
HEATMAP_DIR = BASE_DIR / "heatmaps"
REPORT_DIR = BASE_DIR / "reports"
TEMP_DIR = BASE_DIR / "temp"

MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "video_model.pth"

FRAME_EXTRACTION_RATE = 1          # 1 frame/sec
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16

FAKE_THRESHOLD = 0.60
HIGH_RISK_THRESHOLD = 0.85

SUPPORTED_FORMATS = [
    ".mp4",
    ".avi",
    ".mov",
    ".mkv"
]

for folder in [
    UPLOAD_DIR,
    FRAME_DIR,
    HEATMAP_DIR,
    REPORT_DIR,
    TEMP_DIR,
    MODEL_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)