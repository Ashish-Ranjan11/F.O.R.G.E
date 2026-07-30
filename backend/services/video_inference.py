import torch
import numpy as np

from backend.models import VideoForgeryModel
from backend.services.video_config import *


class VideoInferenceEngine:

    def __init__(self):

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else "cpu"

        )

        self.model = VideoForgeryModel()

        checkpoint = torch.load(

            MODEL_PATH,

            map_location=self.device

        )

        if isinstance(checkpoint, dict):

            if "model_state_dict" in checkpoint:

                self.model.load_state_dict(

                    checkpoint["model_state_dict"]

                )

            else:

                self.model.load_state_dict(checkpoint)

        else:

            self.model = checkpoint

        self.model.to(self.device)

        self.model.eval()

    # --------------------------------------------------

    @torch.no_grad()

    def predict_video(

        self,

        feature_sequence

    ):

        """
        feature_sequence

        Shape:

        (sequence_length,total_feature_size)

        """

        if isinstance(feature_sequence, np.ndarray):

            feature_sequence = torch.tensor(

                feature_sequence,

                dtype=torch.float32

            )

        if feature_sequence.ndim == 2:

            feature_sequence = feature_sequence.unsqueeze(0)

        feature_sequence = feature_sequence.to(self.device)

        probability, attention = self.model(

            feature_sequence

        )

        confidence = float(

            probability.squeeze().cpu().numpy()

        )

        prediction = (

            "Fake"

            if confidence >= 0.5

            else "Real"

        )

        return {

            "prediction": prediction,

            "confidence": round(

                confidence * 100,

                2

            ),

            "probability": confidence,

            "attention": attention.squeeze().cpu().tolist()

        }