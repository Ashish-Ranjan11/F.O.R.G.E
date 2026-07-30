from services.video_schemas import Evidence, TimelineEvent


class TemporalAnalyzer:
    """
    Performs temporal consistency analysis over frame predictions.
    Builds:
        • Timeline
        • Evidence Segments
        • Temporal Statistics
    """

    def __init__(
        self,
        fake_threshold=60,
        min_consecutive_frames=3
    ):
        self.fake_threshold = fake_threshold
        self.min_frames = min_consecutive_frames

    # ----------------------------------------------------

    def analyze(self, frame_predictions):

        evidence = []
        timeline = []

        start = None
        consecutive = 0
        current_segment = []

        fake_frames = 0
        real_frames = 0

        confidences = []
        switches = 0
        previous_prediction = None

        for prediction in frame_predictions:

            confidence = prediction["confidence"]

            confidences.append(confidence)

            is_fake = confidence >= self.fake_threshold

            label = "Fake" if is_fake else "Real"

            if is_fake:
                fake_frames += 1
            else:
                real_frames += 1

            # ---------------- Timeline ----------------

            timeline.append(

                TimelineEvent(

                    timestamp=prediction["timestamp"],

                    status=label,

                    confidence=confidence

                )

            )

            # ---------------- Prediction Switch ----------------

            if previous_prediction is not None:

                if previous_prediction != label:
                    switches += 1

            previous_prediction = label

            # ---------------- Consecutive Fake Frames ----------------

            if is_fake:

                if start is None:
                    start = prediction["timestamp"]

                consecutive += 1

                current_segment.append(prediction)

            else:

                if consecutive >= self.min_frames:

                    evidence.append(

                        self._build_segment(

                            start,

                            current_segment[-1]["timestamp"],

                            current_segment

                        )

                    )

                start = None
                consecutive = 0
                current_segment = []

        # ----------------------------------------------------

        if consecutive >= self.min_frames:

            evidence.append(

                self._build_segment(

                    start,

                    current_segment[-1]["timestamp"],

                    current_segment

                )

            )

        # ----------------------------------------------------

        average_confidence = (

            sum(confidences) / len(confidences)

            if confidences else 0

        )

        temporal_consistency = (

            1 -

            (switches / max(len(frame_predictions) - 1, 1))

        )

        # ----------------------------------------------------

        return {

            "timeline": timeline,

            "evidence": evidence,

            "average_confidence":

                round(average_confidence, 2),

            "prediction_switches":

                switches,

            "temporal_consistency":

                round(temporal_consistency, 3),

            "fake_frames":

                fake_frames,

            "real_frames":

                real_frames

        }

    # ----------------------------------------------------

    def _build_segment(

        self,

        start,

        end,

        frames

    ):

        avg_confidence = (

            sum(

                f["confidence"]

                for f in frames

            ) / len(frames)

        )

        return Evidence(

            timestamp=f"{start} → {end}",

            confidence=round(

                avg_confidence,

                2

            ),

            reason=f"{len(frames)} consecutive suspicious frames detected.",

            frame_path=frames[0].get("frame_path")

            if frames else None

        )