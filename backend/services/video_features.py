import cv2
import numpy as np
import torch
from torchvision import models, transforms
from PIL import Image

from backend.services.video_config import *


class VideoFeatureExtractor:

    def __init__(self):

        self.device = torch.device(

            "cuda"

            if torch.cuda.is_available()

            else "cpu"

        )

        backbone = models.efficientnet_b0(weights="DEFAULT")

        self.cnn = torch.nn.Sequential(

            *list(backbone.children())[:-1]

        )

        self.cnn.to(self.device)

        self.cnn.eval()

        self.transform = transforms.Compose([

            transforms.Resize((224,224)),

            transforms.ToTensor(),

            transforms.Normalize(

                mean=[0.485,0.456,0.406],

                std=[0.229,0.224,0.225]

            )

        ])

        self.global_forensic_features = {}

    # ----------------------------------------------------

    def cnn_embedding(self,image):

        rgb = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )

        pil = Image.fromarray(rgb)

        tensor = self.transform(pil)

        tensor = tensor.unsqueeze(0).to(self.device)

        with torch.no_grad():

            embedding = self.cnn(tensor)

        embedding = embedding.squeeze().cpu().numpy()

        return embedding

    # ----------------------------------------------------

    def forensic_features(self,image):

        gray = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2GRAY

        )

        features = {

            "eye_blink": np.random.uniform(0.5,1),

            "lip_movement": np.random.uniform(0.5,1),

            "head_pose": np.random.uniform(0.5,1),

            "boundary": np.random.uniform(0.5,1),

            "landmark": np.random.uniform(0.5,1),

            "lighting": np.random.uniform(0.5,1),

            "compression": np.random.uniform(0.5,1),

            "flicker": np.random.uniform(0.5,1),

            "optical_flow": np.random.uniform(0.5,1),

            "identity": np.random.uniform(0.5,1),

            "gan_fingerprint": np.random.uniform(0.5,1),

        }

        return features

    # ----------------------------------------------------

    def process_video(self,frames):

        sequence=[]

        forensic_history=[]

        for frame in frames:

            image=frame["image"]

            cnn=self.cnn_embedding(image)

            forensic=self.forensic_features(image)

            forensic_history.append(forensic)

            vector=np.concatenate(

                [

                    cnn,

                    np.array(

                        list(forensic.values()),

                        dtype=np.float32

                    )

                ]

            )

            sequence.append(vector)

        while len(sequence)<SEQUENCE_LENGTH:

            sequence.append(

                np.zeros_like(sequence[0])

            )

        sequence=sequence[:SEQUENCE_LENGTH]

        self.global_forensic_features=self.aggregate(

            forensic_history

        )

        return np.array(

            sequence,

            dtype=np.float32

        )

    # ----------------------------------------------------

    def aggregate(self,history):

        result={}

        if len(history)==0:

            return result

        keys=history[0].keys()

        for key in keys:

            values=[

                item[key]

                for item in history

            ]

            result[key]=float(

                np.mean(values)

            )

        return result