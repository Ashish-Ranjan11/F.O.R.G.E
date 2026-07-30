class TimelineBuilder:

    def build(self, frame_predictions):

        timeline = []

        for prediction in frame_predictions:

            timeline.append(

                {

                    "timestamp":

                        prediction["timestamp"],

                    "score":

                        prediction["confidence"],

                    "status":

                        prediction["prediction"]

                }

            )

        return timeline