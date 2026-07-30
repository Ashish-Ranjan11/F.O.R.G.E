from typing import List, Optional

from pydantic import BaseModel


class VideoMetadata(BaseModel):

    filename: str

    duration: float

    fps: float

    width: int

    height: int

    codec: str

    frame_count: int

    file_size_mb: float

    sha256: str


# --------------------------------------------------------


class FramePrediction(BaseModel):

    frame_number: int

    timestamp: float

    prediction: str

    confidence: float

    probability: float

    path: str


# --------------------------------------------------------


class Evidence(BaseModel):

    id: int

    timestamp: float

    confidence: float

    severity: str

    reason: str

    thumbnail: Optional[str] = None


# --------------------------------------------------------


class TimelineEvent(BaseModel):

    timestamp: float

    score: float

    status: str


# --------------------------------------------------------


class VideoAnalysisResult(BaseModel):

    verdict: str

    confidence: float

    metadata: VideoMetadata

    frame_predictions: List[FramePrediction]

    timeline: List[TimelineEvent]

    evidence: List[Evidence]