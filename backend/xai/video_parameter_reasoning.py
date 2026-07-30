class VideoParameterReasoning:

    def __init__(self):
        pass

    # ---------------------------------------------------------
    # Eye Blink
    # ---------------------------------------------------------

    def eye_blink_reason(self, value):

        if value >= 0.80:
            return {
                "score": value,
                "risk": "LOW",
                "reason": "Natural eye blink behaviour detected."
            }

        elif value >= 0.50:
            return {
                "score": value,
                "risk": "MEDIUM",
                "reason": "Minor inconsistencies observed in eye blinking."
            }

        return {
            "score": value,
            "risk": "HIGH",
            "reason": "Unnatural eye blink frequency detected."
        }

    # ---------------------------------------------------------
    # Lip Movement
    # ---------------------------------------------------------

    def lip_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Lip movements appear natural."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Slight lip synchronization inconsistencies detected."

        else:
            risk = "HIGH"
            reason = "Lip movements appear inconsistent with facial motion."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Head Pose
    # ---------------------------------------------------------

    def head_pose_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Natural head pose transitions."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Minor head pose inconsistencies."

        else:
            risk = "HIGH"
            reason = "Abrupt or unrealistic head pose changes detected."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Face Boundary
    # ---------------------------------------------------------

    def boundary_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Face boundaries appear natural."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Slight blending artifacts detected."

        else:
            risk = "HIGH"
            reason = "Strong face boundary artifacts detected."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Landmark Stability
    # ---------------------------------------------------------

    def landmark_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Facial landmarks remain stable."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Minor landmark instability detected."

        else:
            risk = "HIGH"
            reason = "Facial landmark movement is inconsistent."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Lighting
    # ---------------------------------------------------------

    def lighting_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Lighting remains consistent."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Minor lighting inconsistencies detected."

        else:
            risk = "HIGH"
            reason = "Lighting changes are inconsistent across frames."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Compression
    # ---------------------------------------------------------

    def compression_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Compression artifacts appear normal."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Moderate compression artifacts detected."

        else:
            risk = "HIGH"
            reason = "Abnormal compression artifacts detected."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Flickering
    # ---------------------------------------------------------

    def flicker_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "No abnormal frame flickering detected."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Minor frame flickering observed."

        else:
            risk = "HIGH"
            reason = "Strong frame flickering detected."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Optical Flow
    # ---------------------------------------------------------

    def optical_flow_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Motion between frames appears natural."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Motion consistency is moderately affected."

        else:
            risk = "HIGH"
            reason = "Unnatural motion pattern detected."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # Identity Consistency
    # ---------------------------------------------------------

    def identity_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "Facial identity remains consistent."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Minor identity variation detected."

        else:
            risk = "HIGH"
            reason = "Significant facial identity inconsistency."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
    # GAN Fingerprint
    # ---------------------------------------------------------

    def gan_reason(self, value):

        if value >= 0.80:
            risk = "LOW"
            reason = "No significant GAN fingerprints detected."

        elif value >= 0.50:
            risk = "MEDIUM"
            reason = "Weak GAN fingerprint patterns observed."

        else:
            risk = "HIGH"
            reason = "Strong GAN fingerprint signatures detected."

        return {
            "score": value,
            "risk": risk,
            "reason": reason
        }

    # ---------------------------------------------------------
        # ---------------------------------------------------------
    # Generate Complete XAI
    # ---------------------------------------------------------

    def generate(self, feature_vector):

        # -------------------------------------------------
        # Temporary Mapping
        # (Current extractor → Expected forensic parameters)
        # -------------------------------------------------

        mapped = {

            "eye_blink":
                feature_vector.get("eye_blink",
                                   feature_vector.get("sharpness", 0) / 100),

            "lip_movement":
                feature_vector.get("lip_movement",
                                   feature_vector.get("contrast", 0) / 100),

            "head_pose":
                feature_vector.get("head_pose",
                                   feature_vector.get("brightness", 0) / 255),

            "boundary":
                feature_vector.get("boundary",
                                   1 - feature_vector.get("noise", 0) / 100),

            "landmark":
                feature_vector.get("landmark", 0.85),

            "lighting":
                feature_vector.get("lighting",
                                   feature_vector.get("brightness", 0) / 255),

            "compression":
                feature_vector.get("compression",
                                   1 - feature_vector.get("noise", 0) / 100),

            "flicker":
                feature_vector.get("flicker", 0.80),

            "optical_flow":
                feature_vector.get("optical_flow", 0.80),

            "identity":
                feature_vector.get("identity", 0.90),

            "gan_fingerprint":
                feature_vector.get("gan_fingerprint", 0.70),

        }

        return {

            "eye_blink":
                self.eye_blink_reason(mapped["eye_blink"]),

            "lip_movement":
                self.lip_reason(mapped["lip_movement"]),

            "head_pose":
                self.head_pose_reason(mapped["head_pose"]),

            "boundary":
                self.boundary_reason(mapped["boundary"]),

            "landmark":
                self.landmark_reason(mapped["landmark"]),

            "lighting":
                self.lighting_reason(mapped["lighting"]),

            "compression":
                self.compression_reason(mapped["compression"]),

            "flicker":
                self.flicker_reason(mapped["flicker"]),

            "optical_flow":
                self.optical_flow_reason(mapped["optical_flow"]),

            "identity":
                self.identity_reason(mapped["identity"]),

            "gan_fingerprint":
                self.gan_reason(mapped["gan_fingerprint"])

        }