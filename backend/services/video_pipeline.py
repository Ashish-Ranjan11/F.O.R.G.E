from pathlib import Path

from backend.services.metadata_pipeline import MetadataPipeline
from backend.services.frame_extractor import extract_frames
from backend.services.face_detector import detect_faces

from backend.services.video_features import VideoFeatureExtractor
from backend.services.video_inference import VideoInferenceEngine

from backend.services.audio_extractor import extract_audio

from backend.services.temporal_analysis import TemporalAnalyzer
from backend.services.forensic_scoring import ForensicScoringEngine

from backend.services.timeline_builder import TimelineBuilder
from backend.services.evidence_builder import EvidenceBuilder

from backend.services.video_visualizer import VideoVisualizer
from backend.services.video_report_generator import VideoReportGenerator

from backend.xai.video_parameter_reasoning import VideoParameterReasoning


def process_video(
    video_path: str,
    video_id: str,
    sample_rate: float = 2.0,
):

    path = Path(video_path)

    if not path.exists():
        raise FileNotFoundError(video_path)

    print("=" * 80)
    print("F.O.R.G.E VIDEO INVESTIGATION")
    print("=" * 80)

    ###########################################################
    ## STEP 1
    ###########################################################

    metadata = MetadataPipeline().extract(str(path))

    ###########################################################
    ## STEP 2
    ###########################################################

    frames = extract_frames(
        video_path=str(path),
        video_id=video_id,
        sample_rate=sample_rate,
    )

    if len(frames) == 0:
        raise RuntimeError("No frames extracted.")

    ###########################################################
    ## STEP 3
    ###########################################################

    faces = detect_faces(
        video_id,
        frames,
    )

    ###########################################################
    ## STEP 4
    ###########################################################

    extractor = VideoFeatureExtractor()

    feature_sequence = extractor.process_video(frames)

    ###########################################################
    ## STEP 5
    ###########################################################

    inference = VideoInferenceEngine()

    prediction = inference.predict_video(
        feature_sequence
    )

    ###########################################################
    ## STEP 6
    ###########################################################

    reasoning_engine = VideoParameterReasoning()

    parameter_reasoning = reasoning_engine.generate(
        extractor.global_forensic_features
    )

    ###########################################################
    ## STEP 7
    ###########################################################

    temporal = TemporalAnalyzer()

    temporal_result = temporal.analyze(
        frames,
        prediction
    )

    ###########################################################
    ## STEP 8
    ###########################################################

    scorer = ForensicScoringEngine()

    forensic_result = scorer.compute(
        prediction,
        temporal_result,
        metadata.dict()
    )

    ###########################################################
    ## STEP 9
    ###########################################################

    timeline = TimelineBuilder().build(
        temporal_result
    )

    evidence = EvidenceBuilder().build(
        temporal_result["evidence"],
        Path(frames[0]["path"]).parent,
    )

    ###########################################################
    ## STEP 10
    ###########################################################

    audio = extract_audio(
        str(path)
    )

    ###########################################################
    ## STEP 11
    ###########################################################

    visualizer = VideoVisualizer()

    visualizations = visualizer.visualize(
        video_id,
        frames,
        faces,
        timeline,
    )

    ###########################################################
    ## SUMMARY
    ###########################################################

    summary = {

        "frames_extracted": len(frames),

        "faces_detected": len(faces),

        "feature_vectors": len(feature_sequence),

        "audio_status":

            "success"

            if audio

            else

            "not_available",

        "prediction":

            forensic_result["verdict"],

        "confidence":

            forensic_result["confidence"],

    }

    ###########################################################
    ## REPORT
    ###########################################################

    report = VideoReportGenerator().build_complete_report(

        video_id,

        metadata.dict(),

        forensic_result,

        parameter_reasoning,

        timeline,

        visualizations,

        summary,

    )

    print("=" * 80)
    print("VIDEO ANALYSIS COMPLETED")
    print("=" * 80)

    return {

        "status": "completed",

        "video_id": video_id,

        "prediction": forensic_result,

        "metadata": metadata,

        "frames": frames,

        "faces": faces,

        "feature_sequence": feature_sequence,

        "parameter_reasoning": parameter_reasoning,

        "timeline": timeline,

        "evidence": evidence,

        "audio": audio,

        "visualizations": visualizations,

        "report": report,

    }