from backend.services.fake_image_detector import analyze_image
from backend.services.heatmap_generator import generate_heatmap


def process_image(image_path):
    try:
        result = analyze_image(image_path)

        if "error" in result:
            return result

        heatmap_path = generate_heatmap(image_path)

        result["heatmap"] = heatmap_path
        result["file_type"] = "image"
        result["modality"] = "image"

        return result

    except Exception as e:
        return {
            "error": str(e)
        }