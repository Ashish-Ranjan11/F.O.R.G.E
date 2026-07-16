from __future__ import annotations

import hashlib
import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import (
    FastAPI,
    File,
    Form,
    UploadFile,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.services.analytics_engine import (
    get_analytics,
    update_analytics,
)
from backend.services.audio_pipeline import process_audio
from backend.services.docx_processor import process_docx
from backend.services.forensic_pipeline import analyze_text
from backend.services.image_pipeline import process_image
from backend.services.pdf_processor import process_pdf
from backend.services.report_generator import generate_pdf_report


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

UPLOAD_DIR = PROJECT_ROOT / "uploads"
AUDIO_UPLOAD_DIR = UPLOAD_DIR / "audio"

BACKEND_UPLOAD_DIR = PROJECT_ROOT / "backend" / "uploads"

REPORT_DIR = PROJECT_ROOT / "reports"

AUDIO_VISUAL_DIR = (
    PROJECT_ROOT
    / "backend"
    / "audio_visuals"
)

WAVEFORM_DIR = AUDIO_VISUAL_DIR / "waveforms"
SPECTROGRAM_DIR = AUDIO_VISUAL_DIR / "spectrograms"
AUDIO_HEATMAP_DIR = AUDIO_VISUAL_DIR / "heatmaps"


for directory in (
    UPLOAD_DIR,
    AUDIO_UPLOAD_DIR,
    BACKEND_UPLOAD_DIR,
    REPORT_DIR,
    WAVEFORM_DIR,
    SPECTROGRAM_DIR,
    AUDIO_HEATMAP_DIR,
):
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="FORGE API",
    description=(
        "Multimodal explainable AI platform for "
        "text, image and audio forensic analysis."
    ),
    version="2.0.0",
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/uploads",
    StaticFiles(
        directory=str(
            UPLOAD_DIR
        )
    ),
    name="uploads",
)

app.mount(
    "/backend-uploads",
    StaticFiles(
        directory=str(
            BACKEND_UPLOAD_DIR
        )
    ),
    name="backend_uploads",
)

app.mount(
    "/reports",
    StaticFiles(
        directory=str(
            REPORT_DIR
        )
    ),
    name="reports",
)

app.mount(
    "/audio-visuals",
    StaticFiles(
        directory=str(
            AUDIO_VISUAL_DIR
        )
    ),
    name="audio_visuals",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# CONSTANTS
# =========================================================

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

AUDIO_EXTENSIONS = {
    ".wav",
    ".flac",
    ".mp3",
    ".m4a",
}

TEXT_EXTENSIONS = {
    ".txt",
    ".docx",
    ".pdf",
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def utc_timestamp() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


def generate_case_id(
    modality: str,
) -> str:
    prefix = {
        "text": "TXT",
        "image": "IMG",
        "audio": "AUD",
    }.get(
        modality,
        "GEN",
    )

    date_part = datetime.now(
        timezone.utc
    ).strftime(
        "%Y%m%d"
    )

    random_part = (
        uuid.uuid4()
        .hex[:8]
        .upper()
    )

    return (
        f"FORGE-{prefix}-"
        f"{date_part}-"
        f"{random_part}"
    )


def sanitize_filename(
    filename: str,
) -> str:
    safe_name = os.path.basename(
        filename
    )

    safe_name = safe_name.replace(
        " ",
        "_",
    )

    return (
        f"{uuid.uuid4().hex}_"
        f"{safe_name}"
    )


def calculate_sha256(
    file_path: Path,
) -> str:
    digest = hashlib.sha256()

    with file_path.open(
        "rb"
    ) as handle:
        for chunk in iter(
            lambda: handle.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(
                chunk
            )

    return digest.hexdigest()


def save_uploaded_file(
    uploaded_file: UploadFile,
    destination: Path,
) -> None:
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with destination.open(
        "wb"
    ) as buffer:
        shutil.copyfileobj(
            uploaded_file.file,
            buffer,
        )


def build_evidence_metadata(
    *,
    file_path: Optional[Path],
    original_filename: Optional[str],
    modality: str,
    mime_type: Optional[str] = None,
) -> Dict[str, Any]:
    evidence: Dict[str, Any] = {
        "original_filename": (
            original_filename
            or "direct_text_input"
        ),
        "modality": modality,
        "mime_type": (
            mime_type
            or "text/plain"
        ),
        "analysis_timestamp_utc": (
            utc_timestamp()
        ),
        "size_bytes": None,
        "sha256": None,
    }

    if (
        file_path
        and file_path.exists()
    ):
        evidence[
            "size_bytes"
        ] = file_path.stat().st_size

        evidence[
            "sha256"
        ] = calculate_sha256(
            file_path
        )

    return evidence


def normalize_probability(
    value: Any,
) -> float:
    try:
        number = float(
            value
        )
    except (
        TypeError,
        ValueError,
    ):
        return 0.0

    if 0 <= number <= 1:
        number *= 100

    return round(
        max(
            0.0,
            min(
                100.0,
                number,
            ),
        ),
        2,
    )


def attach_standard_contract(
    *,
    result: Dict[str, Any],
    modality: str,
    case_id: str,
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    fake_probability = (
        result.get(
            "raw_ai_probability"
        )
        or result.get(
            "raw_probability_fake"
        )
        or result.get(
            "risk_score"
        )
        or 0
    )

    real_probability = (
        result.get(
            "raw_human_probability"
        )
        or result.get(
            "raw_probability_real"
        )
    )

    fake_probability = (
        normalize_probability(
            fake_probability
        )
    )

    if real_probability is None:
        real_probability = (
            100 - fake_probability
        )

    real_probability = (
        normalize_probability(
            real_probability
        )
    )

    result[
        "case_id"
    ] = case_id

    result[
        "evidence"
    ] = evidence

    result[
        "modality"
    ] = modality

    result[
        "file_type"
    ] = modality

    result[
        "probabilities"
    ] = {
        "ai": fake_probability,
        "human": real_probability,
    }

    result[
        "analysis_version"
    ] = "FORGE-XAI-2.0"

    confidence = normalize_probability(
        result.get(
            "confidence",
            0,
        )
    )

    if confidence >= 90:
        decision_strength = (
            "VERY STRONG"
        )
    elif confidence >= 75:
        decision_strength = (
            "STRONG"
        )
    elif confidence >= 60:
        decision_strength = (
            "MODERATE"
        )
    else:
        decision_strength = (
            "LIMITED"
        )

    result[
        "decision_strength"
    ] = decision_strength

    return result


def create_report(
    result: Dict[str, Any],
) -> None:
    case_id = result.get(
        "case_id",
        generate_case_id(
            result.get(
                "modality",
                "general",
            )
        ),
    )

    report_name = (
        f"{case_id}_"
        f"{datetime.now(timezone.utc).strftime('%H%M%S')}"
        f".pdf"
    )

    report_path = (
        REPORT_DIR
        / report_name
    )

    try:
        generate_pdf_report(
            result,
            str(
                report_path
            ),
        )

        result[
            "pdf_report"
        ] = (
            f"/reports/"
            f"{report_name}"
        )

    except Exception as error:
        result[
            "pdf_report_error"
        ] = str(
            error
        )


def update_module_analytics(
    modality: str,
    result: Dict[str, Any],
) -> None:
    if result.get(
        "error"
    ):
        return

    update_analytics(
        modality,
        result.get(
            "prediction",
            "UNKNOWN",
        ),
        result.get(
            "confidence",
            0,
        ),
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def home():
    return {
        "message": (
            "FORGE Backend Running"
        ),
        "version": "2.0.0",
        "status": "online",
        "modules": {
            "text": "available",
            "image": "available",
            "audio": "available",
        },
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "FORGE API",
        "timestamp": utc_timestamp(),
    }


# =========================================================
# MAIN ANALYZE ENDPOINT
# =========================================================

@app.post("/analyze")
async def analyze(
    file: Optional[
        UploadFile
    ] = File(
        default=None
    ),
    text: str = Form(
        default=""
    ),
):
    try:
        result: Optional[
            Dict[str, Any]
        ] = None

        modality = "text"
        file_path: Optional[
            Path
        ] = None

        original_filename: Optional[
            str
        ] = None

        mime_type: Optional[
            str
        ] = None

        uploaded_public_url: Optional[
            str
        ] = None

        # -------------------------------------------------
        # DIRECT TEXT INPUT
        # -------------------------------------------------

        if text.strip():
            modality = "text"

            result = analyze_text(
                text.strip()
            )

        # -------------------------------------------------
        # UPLOADED FILE
        # -------------------------------------------------

        elif file is not None:
            if not file.filename:
                return {
                    "error": (
                        "Empty filename"
                    )
                }

            original_filename = (
                file.filename
            )

            mime_type = (
                file.content_type
            )

            extension = (
                Path(
                    original_filename
                )
                .suffix
                .lower()
            )

            stored_filename = (
                sanitize_filename(
                    original_filename
                )
            )

            # ---------------------------------------------
            # IMAGE
            # ---------------------------------------------

            if extension in IMAGE_EXTENSIONS:
                modality = "image"

                file_path = (
                    UPLOAD_DIR
                    / stored_filename
                )

                save_uploaded_file(
                    file,
                    file_path,
                )

                result = process_image(
                    str(
                        file_path
                    )
                )

                uploaded_public_url = (
                    f"/uploads/"
                    f"{stored_filename}"
                )

            # ---------------------------------------------
            # AUDIO
            # ---------------------------------------------

            elif extension in AUDIO_EXTENSIONS:
                modality = "audio"

                file_path = (
                    AUDIO_UPLOAD_DIR
                    / stored_filename
                )

                save_uploaded_file(
                    file,
                    file_path,
                )

                result = process_audio(
                    str(
                        file_path
                    )
                )

                uploaded_public_url = (
                    f"/uploads/audio/"
                    f"{stored_filename}"
                )

            # ---------------------------------------------
            # DOCX
            # ---------------------------------------------

            elif extension == ".docx":
                modality = "text"

                file_path = (
                    UPLOAD_DIR
                    / stored_filename
                )

                save_uploaded_file(
                    file,
                    file_path,
                )

                result = process_docx(
                    str(
                        file_path
                    )
                )

                uploaded_public_url = (
                    f"/uploads/"
                    f"{stored_filename}"
                )

            # ---------------------------------------------
            # PDF
            # ---------------------------------------------

            elif extension == ".pdf":
                modality = "text"

                file_path = (
                    UPLOAD_DIR
                    / stored_filename
                )

                save_uploaded_file(
                    file,
                    file_path,
                )

                result = process_pdf(
                    str(
                        file_path
                    )
                )

                uploaded_public_url = (
                    f"/uploads/"
                    f"{stored_filename}"
                )

            # ---------------------------------------------
            # TXT
            # ---------------------------------------------

            elif extension == ".txt":
                modality = "text"

                file_path = (
                    UPLOAD_DIR
                    / stored_filename
                )

                save_uploaded_file(
                    file,
                    file_path,
                )

                text_content = (
                    file_path.read_text(
                        encoding="utf-8",
                        errors="ignore",
                    )
                )

                result = analyze_text(
                    text_content
                )

                uploaded_public_url = (
                    f"/uploads/"
                    f"{stored_filename}"
                )

            else:
                return {
                    "error": (
                        "Unsupported file type: "
                        f"{extension}"
                    )
                }

        else:
            return {
                "error": (
                    "No input provided"
                )
            }

        if result is None:
            return {
                "error": (
                    "Analysis failed"
                )
            }

        if result.get(
            "error"
        ):
            return result

        case_id = generate_case_id(
            modality
        )

        evidence = (
            build_evidence_metadata(
                file_path=file_path,
                original_filename=(
                    original_filename
                ),
                modality=modality,
                mime_type=mime_type,
            )
        )

        result = attach_standard_contract(
            result=result,
            modality=modality,
            case_id=case_id,
            evidence=evidence,
        )

        if uploaded_public_url:
            result[
                "uploaded_file"
            ] = uploaded_public_url

        update_module_analytics(
            modality,
            result,
        )

        create_report(
            result
        )

        return result

    except Exception as error:
        return {
            "error": str(
                error
            )
        }


# =========================================================
# DIRECT IMAGE ENDPOINT
# =========================================================

@app.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...)
):
    try:
        if not file.filename:
            return {
                "error": (
                    "Empty filename"
                )
            }

        extension = (
            Path(
                file.filename
            )
            .suffix
            .lower()
        )

        if extension not in IMAGE_EXTENSIONS:
            return {
                "error": (
                    "Only PNG, JPG, JPEG "
                    "and WEBP image files "
                    "are supported."
                )
            }

        stored_filename = (
            sanitize_filename(
                file.filename
            )
        )

        file_path = (
            UPLOAD_DIR
            / stored_filename
        )

        save_uploaded_file(
            file,
            file_path,
        )

        result = process_image(
            str(
                file_path
            )
        )

        if result.get(
            "error"
        ):
            return result

        case_id = generate_case_id(
            "image"
        )

        evidence = (
            build_evidence_metadata(
                file_path=file_path,
                original_filename=(
                    file.filename
                ),
                modality="image",
                mime_type=(
                    file.content_type
                ),
            )
        )

        result = attach_standard_contract(
            result=result,
            modality="image",
            case_id=case_id,
            evidence=evidence,
        )

        result[
            "uploaded_file"
        ] = (
            f"/uploads/"
            f"{stored_filename}"
        )

        update_module_analytics(
            "image",
            result,
        )

        create_report(
            result
        )

        return result

    except Exception as error:
        return {
            "error": str(
                error
            )
        }


# =========================================================
# DIRECT AUDIO ENDPOINT
# =========================================================

@app.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...)
):
    try:
        if not file.filename:
            return {
                "error": (
                    "Empty filename"
                )
            }

        extension = (
            Path(
                file.filename
            )
            .suffix
            .lower()
        )

        if extension not in AUDIO_EXTENSIONS:
            return {
                "error": (
                    "Only WAV, FLAC, MP3 "
                    "and M4A audio files "
                    "are supported."
                )
            }

        stored_filename = (
            sanitize_filename(
                file.filename
            )
        )

        file_path = (
            AUDIO_UPLOAD_DIR
            / stored_filename
        )

        save_uploaded_file(
            file,
            file_path,
        )

        result = process_audio(
            str(
                file_path
            )
        )

        if result.get(
            "error"
        ):
            return result

        case_id = generate_case_id(
            "audio"
        )

        evidence = (
            build_evidence_metadata(
                file_path=file_path,
                original_filename=(
                    file.filename
                ),
                modality="audio",
                mime_type=(
                    file.content_type
                ),
            )
        )

        result = attach_standard_contract(
            result=result,
            modality="audio",
            case_id=case_id,
            evidence=evidence,
        )

        result[
            "uploaded_file"
        ] = (
            f"/uploads/audio/"
            f"{stored_filename}"
        )

        update_module_analytics(
            "audio",
            result,
        )

        create_report(
            result
        )

        return result

    except Exception as error:
        return {
            "error": str(
                error
            )
        }


# =========================================================
# ANALYTICS
# =========================================================

@app.get("/analytics")
def analytics():
    return get_analytics()