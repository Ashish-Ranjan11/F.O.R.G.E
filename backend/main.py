from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form
)

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import os
import uuid
import shutil

from backend.services.docx_processor import process_docx
from backend.services.pdf_processor import process_pdf
from backend.services.forensic_pipeline import analyze_text
from backend.services.image_pipeline import process_image
from backend.services.report_generator import generate_pdf_report
from backend.services.audio_pipeline import process_audio

from backend.services.analytics_engine import (
    get_analytics,
    update_analytics
)

# ==========================================
# APP INIT
# ==========================================

app = FastAPI(
    title="DeepFakeConnect API"
)

# ==========================================
# DIRECTORIES
# ==========================================

os.makedirs(
    "uploads",
    exist_ok=True
)

os.makedirs(
    "uploads/audio",
    exist_ok=True
)

os.makedirs(
    "reports",
    exist_ok=True
)

os.makedirs(
    "backend/uploads",
    exist_ok=True
)

os.makedirs(
    "backend/audio_visuals/waveforms",
    exist_ok=True
)

os.makedirs(
    "backend/audio_visuals/spectrograms",
    exist_ok=True
)

os.makedirs(
    "backend/audio_visuals/heatmaps",
    exist_ok=True
)

# ==========================================
# STATIC FILES
# ==========================================

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.mount(
    "/backend-uploads",
    StaticFiles(directory="backend/uploads"),
    name="backend_uploads"
)

app.mount(
    "/reports",
    StaticFiles(directory="reports"),
    name="reports"
)

app.mount(
    "/audio-visuals",
    StaticFiles(directory="backend/audio_visuals"),
    name="audio_visuals"
)

# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def home():

    return {
        "message": "DeepFakeConnect Backend Running"
    }

# ==========================================
# MAIN ANALYZE ENDPOINT
# TEXT + IMAGE + AUDIO
# ==========================================

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(None),
    text: str = Form("")
):

    try:

        result = None
        file_type = "text"
        file_path = None

        # ==================================
        # TEXTBOX INPUT
        # ==================================

        if text and text.strip():

            result = analyze_text(
                text
            )

            file_type = "text"

            update_analytics(
                "text",
                result.get(
                    "prediction",
                    "UNKNOWN"
                ),
                result.get(
                    "confidence",
                    0
                )
            )

        # ==================================
        # FILE INPUT
        # ==================================

        elif file:

            if not file.filename:

                return {
                    "error": "Empty filename"
                }

            original_filename = file.filename

            filename = (
                f"{uuid.uuid4()}_{original_filename}"
            )

            extension = os.path.splitext(
                original_filename
            )[1].lower()

            # ==============================
            # AUDIO FILES
            # ==============================

            if extension in [
                ".wav",
                ".flac",
                ".mp3",
                ".m4a"
            ]:

                file_type = "audio"

                file_path = os.path.join(
                    "uploads",
                    "audio",
                    filename
                )

                with open(
                    file_path,
                    "wb"
                ) as buffer:

                    shutil.copyfileobj(
                        file.file,
                        buffer
                    )

                result = process_audio(
                    file_path
                )

                update_analytics(
                    "audio",
                    result.get(
                        "prediction",
                        "UNKNOWN"
                    ),
                    result.get(
                        "confidence",
                        0
                    )
                )

                result["uploaded_file"] = (
                    f"/uploads/audio/{filename}"
                )

                result["file_type"] = file_type

            # ==============================
            # IMAGE FILES
            # ==============================

            elif extension in [
                ".png",
                ".jpg",
                ".jpeg"
            ]:

                file_type = "image"

                file_path = os.path.join(
                    "uploads",
                    filename
                )

                with open(
                    file_path,
                    "wb"
                ) as buffer:

                    shutil.copyfileobj(
                        file.file,
                        buffer
                    )

                result = process_image(
                    file_path
                )

                update_analytics(
                    "image",
                    result.get(
                        "prediction",
                        "UNKNOWN"
                    ),
                    result.get(
                        "confidence",
                        0
                    )
                )

                result["uploaded_file"] = (
                    f"/uploads/{filename}"
                )

                result["file_type"] = file_type

            # ==============================
            # DOCX FILE
            # ==============================

            elif extension == ".docx":

                file_type = "text"

                file_path = os.path.join(
                    "uploads",
                    filename
                )

                with open(
                    file_path,
                    "wb"
                ) as buffer:

                    shutil.copyfileobj(
                        file.file,
                        buffer
                    )

                result = process_docx(
                    file_path
                )

                update_analytics(
                    "text",
                    result.get(
                        "prediction",
                        "UNKNOWN"
                    ),
                    result.get(
                        "confidence",
                        0
                    )
                )

                result["uploaded_file"] = (
                    f"/uploads/{filename}"
                )

                result["file_type"] = file_type

            # ==============================
            # PDF FILE
            # ==============================

            elif extension == ".pdf":

                file_type = "text"

                file_path = os.path.join(
                    "uploads",
                    filename
                )

                with open(
                    file_path,
                    "wb"
                ) as buffer:

                    shutil.copyfileobj(
                        file.file,
                        buffer
                    )

                result = process_pdf(
                    file_path
                )

                update_analytics(
                    "text",
                    result.get(
                        "prediction",
                        "UNKNOWN"
                    ),
                    result.get(
                        "confidence",
                        0
                    )
                )

                result["uploaded_file"] = (
                    f"/uploads/{filename}"
                )

                result["file_type"] = file_type

            # ==============================
            # TXT FILE
            # ==============================

            elif extension == ".txt":

                file_type = "text"

                file_path = os.path.join(
                    "uploads",
                    filename
                )

                with open(
                    file_path,
                    "wb"
                ) as buffer:

                    shutil.copyfileobj(
                        file.file,
                        buffer
                    )

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as txt_file:

                    text_content = txt_file.read()

                result = analyze_text(
                    text_content
                )

                update_analytics(
                    "text",
                    result.get(
                        "prediction",
                        "UNKNOWN"
                    ),
                    result.get(
                        "confidence",
                        0
                    )
                )

                result["uploaded_file"] = (
                    f"/uploads/{filename}"
                )

                result["file_type"] = file_type

            # ==============================
            # UNSUPPORTED
            # ==============================

            else:

                return {
                    "error": f"Unsupported file type: {extension}"
                }

        # ==================================
        # NO INPUT
        # ==================================

        else:

            return {
                "error": "No input provided"
            }

        # ==================================
        # GENERATE PDF REPORT
        # ==================================

        if result is None:

            return {
                "error": "Analysis failed"
            }

        report_name = (
            f"{uuid.uuid4()}.pdf"
        )

        report_path = os.path.join(
            "reports",
            report_name
        )

        try:

            generate_pdf_report(
                result,
                report_path
            )

            result["pdf_report"] = (
                f"/reports/{report_name}"
            )

        except Exception as report_error:

            result["pdf_report_error"] = str(
                report_error
            )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }

# ==========================================
# DIRECT AUDIO ENDPOINT
# ==========================================

@app.post("/upload-audio")
async def upload_audio(
    file: UploadFile = File(...)
):

    try:

        if not file.filename:

            return {
                "error": "Empty filename"
            }

        original_filename = file.filename

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        if extension not in [
            ".wav",
            ".flac",
            ".mp3",
            ".m4a"
        ]:

            return {
                "error": "Only audio files are allowed"
            }

        filename = (
            f"{uuid.uuid4()}_{original_filename}"
        )

        audio_path = os.path.join(
            "uploads",
            "audio",
            filename
        )

        with open(
            audio_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = process_audio(
            audio_path
        )

        update_analytics(
            "audio",
            result.get(
                "prediction",
                "UNKNOWN"
            ),
            result.get(
                "confidence",
                0
            )
        )

        result["uploaded_file"] = (
            f"/uploads/audio/{filename}"
        )

        result["file_type"] = "audio"

        report_name = (
            f"{uuid.uuid4()}.pdf"
        )

        report_path = os.path.join(
            "reports",
            report_name
        )

        try:

            generate_pdf_report(
                result,
                report_path
            )

            result["pdf_report"] = (
                f"/reports/{report_name}"
            )

        except Exception as report_error:

            result["pdf_report_error"] = str(
                report_error
            )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }

# ==========================================
# DIRECT IMAGE ENDPOINT
# ==========================================

@app.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...)
):

    try:

        if not file.filename:

            return {
                "error": "Empty filename"
            }

        original_filename = file.filename

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        if extension not in [
            ".png",
            ".jpg",
            ".jpeg"
        ]:

            return {
                "error": "Only image files are allowed"
            }

        filename = (
            f"{uuid.uuid4()}_{original_filename}"
        )

        file_path = os.path.join(
            "uploads",
            filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = process_image(
            file_path
        )

        update_analytics(
            "image",
            result.get(
                "prediction",
                "UNKNOWN"
            ),
            result.get(
                "confidence",
                0
            )
        )

        result["uploaded_file"] = (
            f"/uploads/{filename}"
        )

        result["file_type"] = "image"

        return result

    except Exception as e:

        return {
            "error": str(e)
        }

# ==========================================
# ANALYTICS ENDPOINT
# ==========================================

@app.get("/analytics")
def analytics():

    return get_analytics()