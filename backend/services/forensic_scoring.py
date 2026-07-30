class ForensicScoringEngine:

    """
    Combines multiple forensic signals
    into one final investigation score.
    """

    def __init__(self):
        pass

    # ----------------------------------------------------

    def compute(

        self,

        frame_predictions,

        temporal_result,

        metadata

    ):

        if len(frame_predictions) == 0:

            return {

                "verdict": "Unknown",

                "confidence": 0,

                "forensic_score": 0

            }

        # ---------------------------------------

        average_model_score = (

            sum(

                frame["confidence"]

                for frame in frame_predictions

            )

            /

            len(frame_predictions)

        )

        # ---------------------------------------

        temporal_bonus = (

            temporal_result["temporal_consistency"]

            * 15

        )

        # ---------------------------------------

        evidence_bonus = (

            len(

                temporal_result["evidence"]

            )

            * 3

        )

        # ---------------------------------------

        resolution_bonus = 0

        if metadata["width"] >= 1920:

            resolution_bonus = 2

        # ---------------------------------------

        forensic_score = (

            average_model_score

            +

            temporal_bonus

            +

            evidence_bonus

            +

            resolution_bonus

        )

        forensic_score = min(

            forensic_score,

            100

        )

        verdict = (

            "Fake"

            if forensic_score >= 55

            else

            "Real"

        )

        return {

            "verdict": verdict,

            "confidence":

                round(

                    average_model_score,

                    2

                ),

            "forensic_score":

                round(

                    forensic_score,

                    2

                ),

            "average_model_score":

                round(

                    average_model_score,

                    2

                ),

            "temporal_score":

                round(

                    temporal_bonus,

                    2

                ),

            "evidence_segments":

                len(

                    temporal_result["evidence"]

                )

        }