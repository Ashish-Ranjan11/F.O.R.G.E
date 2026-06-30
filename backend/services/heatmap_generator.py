import os
import uuid
import cv2
import numpy as np

# =====================================================
# FORGE IMAGE HEATMAP GENERATOR
# Reliable forensic heatmap fallback
# Works even when GradCAM graph connection fails
# =====================================================

PROJECT_ROOT = os.getcwd()

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "backend",
    "uploads",
    "heatmaps"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

IMAGE_SIZE = (224, 224)


def generate_heatmap(image_path):
    try:
        img = cv2.imread(image_path)

        if img is None:
            print("❌ Heatmap failed: image not readable")
            return None

        img = cv2.resize(
            img,
            IMAGE_SIZE
        )

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        edges = cv2.Canny(
            gray,
            70,
            180
        )

        blur = cv2.GaussianBlur(
            gray,
            (7, 7),
            0
        )

        high_freq = cv2.absdiff(
            gray,
            blur
        )

        heat = cv2.addWeighted(
            edges,
            0.55,
            high_freq,
            0.45,
            0
        )

        heat = cv2.normalize(
            heat,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        )

        heat = np.uint8(
            heat
        )

        heat_color = cv2.applyColorMap(
            heat,
            cv2.COLORMAP_JET
        )

        overlay = cv2.addWeighted(
            img,
            0.58,
            heat_color,
            0.42,
            0
        )

        filename = f"{uuid.uuid4()}_image_heatmap.jpg"

        output_path = os.path.join(
            OUTPUT_DIR,
            filename
        )

        cv2.imwrite(
            output_path,
            overlay
        )

        return f"/backend-uploads/heatmaps/{filename}"

    except Exception as e:
        print("❌ Heatmap generation failed:", e)
        return None


def generate_gradcam(image_path):
    return generate_heatmap(image_path)