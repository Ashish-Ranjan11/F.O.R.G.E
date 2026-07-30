import cv2
from pathlib import Path

from .video_utils import FRAME_DIR


def extract_frames(
    video_path,
    video_id,
    sample_rate=2,
):

    save_dir = FRAME_DIR / video_id

    save_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    interval = max(int(fps / sample_rate), 1)

    frames = []

    frame_idx = 0

    saved = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_idx % interval == 0:

            filename = f"frame_{saved:04d}.jpg"

            filepath = save_dir / filename

            cv2.imwrite(str(filepath), frame)

            frames.append(

    {

        "frame_number": saved,

        "timestamp": round(frame_idx / fps, 2),

        "path": str(filepath),

        "image": frame.copy(),

        "height": frame.shape[0],

        "width": frame.shape[1],

    }

)
            

            saved += 1

        frame_idx += 1

    cap.release()

    return frames