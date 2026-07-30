from pathlib import Path
import hashlib
import uuid
import shutil

# ==========================================================
# Backend Root
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

# ==========================================================
# Upload Directories
# ==========================================================

UPLOAD_DIR = BASE_DIR / "uploads"

VIDEO_DIR = UPLOAD_DIR / "videos"

FRAME_DIR = VIDEO_DIR / "frames"

AUDIO_DIR = VIDEO_DIR / "audio"

VISUAL_DIR = BASE_DIR / "video_visuals"

REPORT_DIR = BASE_DIR / "reports"

TEMP_DIR = BASE_DIR / "temp"

# ==========================================================
# Create Required Directories
# ==========================================================

for directory in [

    UPLOAD_DIR,

    VIDEO_DIR,

    FRAME_DIR,

    AUDIO_DIR,

    VISUAL_DIR,

    REPORT_DIR,

    TEMP_DIR,

]:
    directory.mkdir(parents=True, exist_ok=True)

# ==========================================================
# SHA256 Hash
# ==========================================================

def sha256(file_path: str):

    hasher = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            chunk = f.read(8192)

            if not chunk:
                break

            hasher.update(chunk)

    return hasher.hexdigest()

# ==========================================================
# Unique Video ID
# ==========================================================

def generate_video_id():

    return uuid.uuid4().hex

# ==========================================================
# Copy Uploaded Video
# ==========================================================

def save_video(source_path: str, video_id: str):

    extension = Path(source_path).suffix

    destination = VIDEO_DIR / f"{video_id}{extension}"

    shutil.copy(source_path, destination)

    return str(destination)

# ==========================================================
# Cleanup Temporary Files
# ==========================================================

def cleanup_video(video_id: str):

    frame_folder = FRAME_DIR / video_id

    if frame_folder.exists():

        shutil.rmtree(frame_folder, ignore_errors=True)

    audio_file = AUDIO_DIR / f"{video_id}.wav"

    if audio_file.exists():

        audio_file.unlink(missing_ok=True)