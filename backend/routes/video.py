import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.video_utils import (
    generate_video_id,
    ensure_directories,
    validate_video,
    UPLOAD_DIR,
)

from backend.services.video_pipeline import process_video

router = APIRouter(
    prefix="/video",
    tags=["Video Forensics"],
)

ensure_directories()


@router.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):

    # -----------------------------
    # Validate
    # -----------------------------

    if not validate_video(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Unsupported video format.",
        )

    # -----------------------------
    # Generate unique ID
    # -----------------------------

    video_id = generate_video_id()

    extension = Path(file.filename).suffix.lower()

    save_path = (
        UPLOAD_DIR /
        f"{video_id}{extension}"
    )

    # -----------------------------
    # Save uploaded file
    # -----------------------------

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # Process video
    # -----------------------------

    try:

        result = process_video(
            str(save_path),
            video_id,
        )

        return {
            "success": True,
            "message": "Video processed successfully.",
            "data": result,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )