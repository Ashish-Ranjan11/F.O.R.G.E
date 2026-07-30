from pathlib import Path
import cv2
import matplotlib.pyplot as plt

from .video_utils import VISUAL_DIR


class VideoVisualizer:

    def __init__(self):

        self.frame_output = VISUAL_DIR / "annotated_frames"
        self.timeline_output = VISUAL_DIR / "timelines"

        self.frame_output.mkdir(parents=True, exist_ok=True)
        self.timeline_output.mkdir(parents=True, exist_ok=True)

    # -------------------------------------------------------
    # Draw Face Bounding Boxes
    # -------------------------------------------------------

    def annotate_frames(self, video_id, frames, faces):

        save_dir = self.frame_output / video_id
        save_dir.mkdir(parents=True, exist_ok=True)

        face_lookup = {}

        for face in faces:

            face_lookup.setdefault(
                face["frame_number"],
                []
            ).append(face)

        annotated = []

        for frame in frames:

            image = cv2.imread(frame["path"])

            if image is None:
                continue

            current_faces = face_lookup.get(
                frame["frame_number"],
                []
            )

            for face in current_faces:

                x1, y1, x2, y2 = face["bounding_box"]

                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    image,
                    f"{face['confidence']:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

            output = save_dir / Path(frame["path"]).name

            cv2.imwrite(
                str(output),
                image
            )

            annotated.append(str(output))

        return annotated

    # -------------------------------------------------------
    # Timeline Graph
    # -------------------------------------------------------

    def generate_timeline_plot(
        self,
        video_id,
        timeline
    ):

        output_file = (
            self.timeline_output /
            f"{video_id}_timeline.png"
        )

        if len(timeline) == 0:
            return None

        x = []
        y = []

        for item in timeline:

            x.append(item["timestamp"])

            y.append(item.get("score", 0))

        plt.figure(figsize=(12,4))

        plt.plot(
            x,
            y,
            linewidth=2
        )

        plt.title(
            "Video Investigation Timeline"
        )

        plt.xlabel("Time (seconds)")

        plt.ylabel("Suspicion Score")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            output_file,
            dpi=200
        )

        plt.close()

        return str(output_file)

    # -------------------------------------------------------
    # Summary
    # -------------------------------------------------------

    def visualize(
        self,
        video_id,
        frames,
        faces,
        timeline
    ):

        annotated = self.annotate_frames(
            video_id,
            frames,
            faces
        )

        timeline_plot = self.generate_timeline_plot(
            video_id,
            timeline
        )

        return {

            "annotated_frames": annotated,

            "timeline_plot": timeline_plot

        }