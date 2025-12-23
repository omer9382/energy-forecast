
class Serializer:
    def __init__(self,preds):
        self.preds = preds

    def serialize(self):
        spreds = []
        for timestamp,prediction in self.preds:
            timestamp_str = timestamp.isoformat()

            spreds.append(
                {
                    "timestamp":timestamp_str,
                    "prediction":float(prediction)
                }
            )
        return spreds


