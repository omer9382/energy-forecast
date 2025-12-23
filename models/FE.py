import pandas as pd

class FE:
    def __init__(self,df):
        self.df = df
        self.df["Timestamp"] = pd.to_datetime(self.df["Timestamp"])
        self.df["Load"] = pd.to_numeric(self.df["Load"], errors='coerce')
    def transform(self):
        x = self.df["Timestamp"]
        y = self.df["Load"]


        self.df["hours"] = x.dt.hour
        self.df["day_of_week"] = x.dt.dayofweek
        self.df["month"] = x.dt.month
        self.df["is_weekend"] = (self.df["day_of_week"] >= 5).astype(int)
        self.df["lag_1"] = y.shift(1)
        self.df["lag_24"] = y.shift(24)    # same hour yesterday
        self.df["lag_168"] = y.shift(168)
        self.df["rolling_24"]=y.rolling(window=24).mean()
        self.df = self.df.dropna().copy()
        return self.df

    def transform_for_days(self):
        x=self.df["Timestamp"]
        y=self.df["Load"]
        self.df["day_of_week"] = x.dt.dayofweek
        self.df["month"] = x.dt.month
        self.df["is_weekend"] = (self.df["day_of_week"] >= 5).astype(int)
        self.df["lag_1"] = y.shift(1)
        self.df["lag_7"] = y.shift(7)
        self.df["lag_30"] = y.shift(30)
        self.df["rolling_7"] = y.rolling(7).mean()
        self.df["rolling_30"] = y.rolling(30).mean()
        self.df = self.df.dropna().copy()

        return self.df
