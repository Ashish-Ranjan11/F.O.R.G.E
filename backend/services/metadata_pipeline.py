import os
import cv2

from backend.services.video_utils import sha256
from backend.services.video_schemas import VideoMetadata


class MetadataPipeline:

    def extract(self, video_path: str):

        cap = cv2.VideoCapture(video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        duration = frame_count / fps if fps else 0

        cap.release()

        return VideoMetadata(

            filename=os.path.basename(video_path),

            duration=duration,

            fps=fps,

            width=width,

            height=height,

            codec="Unknown",

            frame_count=frame_count,

            file_size_mb=round(
                os.path.getsize(video_path) / (1024 * 1024),
                2
            ),

            sha256=sha256(video_path)
        )