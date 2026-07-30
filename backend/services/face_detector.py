import cv2
from pathlib import Path
from retinaface import RetinaFace




def detect_faces(video_id, frames):

    save_dir = FACE_DIR / video_id

    save_dir.mkdir(parents=True, exist_ok=True)

    face_results = []

    for frame in frames:

        image = cv2.imread(frame["path"])

        detections = RetinaFace.detect_faces(image)

        if not isinstance(detections, dict):
            continue

        for index, (_, detection) in enumerate(detections.items()):

            x1, y1, x2, y2 = detection["facial_area"]

            face = image[y1:y2, x1:x2]

            filename = f"face_{frame['frame_number']:04d}_{index}.jpg"

            filepath = save_dir / filename

            cv2.imwrite(str(filepath), face)

            face_results.append({

                "frame_number": frame["frame_number"],

                "timestamp": frame["timestamp"],

                "face_path": str(filepath),

                "bounding_box": [x1, y1, x2, y2],

                "confidence": float(detection["score"])

            })

    return face_results