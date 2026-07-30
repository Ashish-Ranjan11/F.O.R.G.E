import os


class EvidenceBuilder:

    def build(

        self,

        evidence_segments,

        frame_directory

    ):

        report = []

        for idx, segment in enumerate(evidence_segments):

            frame_name = f"frame_{idx:04}.jpg"

            frame_path = os.path.join(

                frame_directory,

                frame_name

            )

            report.append(

                {

                    "id": idx + 1,

                    "timestamp":

                        segment.timestamp,

                    "confidence":

                        round(

                            segment.confidence,

                            2

                        ),

                    "severity":

                        (

                            "HIGH"

                            if segment.confidence >= 90

                            else

                            "MEDIUM"

                            if segment.confidence >= 70

                            else

                            "LOW"

                        ),

                    "reason":

                        segment.reason,

                    "thumbnail":

                        frame_path

                        if os.path.exists(frame_path)

                        else None

                }

            )

        return report