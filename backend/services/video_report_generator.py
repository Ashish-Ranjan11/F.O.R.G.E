from datetime import datetime


class VideoReportGenerator:

    def __init__(self):
        pass

    # -----------------------------------------------------

    def executive_summary(

        self,

        forensic_result,

        summary

    ):

        return {

            "prediction":

                forensic_result["verdict"],

            "confidence":

                forensic_result["confidence"],

            "forensic_score":

                forensic_result["forensic_score"],

            "frames_processed":

                summary["frames_extracted"],

            "faces_detected":

                summary["faces_detected"],

            "feature_vectors":

                summary["feature_vectors"],

            "overall_risk":

                "HIGH"

                if forensic_result["verdict"] == "Fake"

                else "LOW"

        }

    # -----------------------------------------------------

    def statistics(

        self,

        metadata,

        summary,

        forensic_result

    ):

        return {

            "duration":

                metadata.get("duration"),

            "fps":

                metadata.get("fps"),

            "resolution":

                metadata.get("resolution"),

            "frames_processed":

                summary["frames_extracted"],

            "faces_detected":

                summary["faces_detected"],

            "audio_status":

                summary["audio_status"],

            "evidence_segments":

                forensic_result["evidence_segments"],

            "temporal_score":

                forensic_result["temporal_score"]

        }

    # -----------------------------------------------------

    def build_complete_report(

        self,

        video_id,

        metadata,

        forensic_result,

        parameter_reasoning,

        timeline,

        visualizations,

        summary

    ):

        report = {

            "report_info": {

                "generated_at":

                    datetime.now().strftime(

                        "%Y-%m-%d %H:%M:%S"

                    ),

                "framework":

                    "FORGE",

                "report_type":

                    "Video Investigation Report",

                "video_id":

                    video_id

            },

            "prediction":

                forensic_result,

            "metadata":

                metadata,

            "parameter_reasoning":

                parameter_reasoning,

            "timeline":

                timeline,

            "visualizations":

                visualizations,

            "summary":

                summary

        }

        report["executive_summary"] = (

            self.executive_summary(

                forensic_result,

                summary

            )

        )

        report["statistics"] = (

            self.statistics(

                metadata,

                summary,

                forensic_result

            )

        )

        return report