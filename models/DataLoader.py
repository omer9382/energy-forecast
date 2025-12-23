import pandas as pd
class DataLoader():
    def __init__(self,items = None):
     self.items = items

    def transform_into_df(self):
        df = pd.DataFrame(self.items)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        return df