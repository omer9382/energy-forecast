import numpy as np
import pandas as pd

class LinearRegression:
    def __init__(self, df=None, feature_cols=None, iters=2000):
        self.b = 0.0
        self.w = None
        self.df_original = df.copy() if df is not None else None
        self.df = df.dropna().copy() if df is not None else None

        self.feature_cols = feature_cols if feature_cols else [
            "hours", "day_of_week", "month", "is_weekend",
            "lag_1", "lag_24", "lag_168", "rolling_24"
        ]
        self.iters = iters
        self.X_mean = None
        self.X_std = None

    def compute_cost(self):
        X_df = self.df[self.feature_cols].apply(pd.to_numeric, errors='coerce').fillna(0.0)
        y_series = pd.to_numeric(self.df["Load"], errors='coerce').fillna(0.0)
        X_matrix = X_df.values.astype(np.float64)
        y_matrix = y_series.values.astype(np.float64)

        self.X_mean = X_matrix.mean(axis=0)
        self.X_std = X_matrix.std(axis=0)
        X_norm = (X_matrix - self.X_mean) / (self.X_std + 1e-8)

        m, n = X_norm.shape
        self.w = np.random.uniform(-0.01, 0.01, size=n)
        lr = 0.1

        for i in range(self.iters):
            y_hat = X_norm.dot(self.w) + self.b
            error = y_hat - y_matrix
            dw = (1/m) * X_norm.T.dot(error)
            db = (1/m) * np.sum(error)
            self.w -= lr * dw
            self.b -= lr * db
        return self.w, self.b, self.X_std, self.X_mean

    def load(self, w, b, std, mean):
        self.w = np.array(w)
        self.b = float(b)
        self.X_std = np.array(std)
        self.X_mean = np.array(mean)

    def predict(self, X):
        ts = pd.to_datetime(X[0])
        data = {
            "hours": ts.hour,
            "day_of_week": ts.dayofweek,
            "month": ts.month,
            "is_weekend": int(ts.dayofweek >= 5)
        }
        df_hist = self.df_original.set_index("Timestamp")
        lags = {
            "lag_1": ts - pd.Timedelta(hours=1),
            "lag_24": ts - pd.Timedelta(hours=24),
            "lag_168": ts - pd.Timedelta(hours=168)
        }
        for name, delta_ts in lags.items():
            if delta_ts in df_hist.index:
                val = df_hist.loc[delta_ts, "Load"]
                data[name] = float(val.mean() if isinstance(val, pd.Series) else val)
            else:
                data[name] = 0.0

        lag_24_ts = lags["lag_24"]
        if lag_24_ts in df_hist.index:
            data["rolling_24"] = df_hist["Load"].loc[lag_24_ts - pd.Timedelta(hours=23) : lag_24_ts].mean()
        else:
            data["rolling_24"] = data.get("lag_24", 0.0)

        x_row = np.array([data.get(col, 0.0) for col in self.feature_cols], dtype=np.float64)
        x_row = (x_row - self.X_mean) / (self.X_std + 1e-8)
        return float(x_row.dot(self.w) + self.b)

    def predict_for_days(self, X):
        ts = pd.to_datetime(X[0])
        data = {
            "day_of_week": ts.dayofweek,
            "month": ts.month,
            "is_weekend": int(ts.dayofweek >= 5)
        }
        df_hist = self.df_original.set_index("Timestamp")
        lags = {
            "lag_1": ts - pd.Timedelta(days=1),
            "lag_7": ts - pd.Timedelta(days=7),
            "lag_30": ts - pd.Timedelta(days=30)
        }
        for name, delta_ts in lags.items():
            if delta_ts in df_hist.index:
                val = df_hist.loc[delta_ts, "Load"]
                data[name] = float(val.mean() if isinstance(val, pd.Series) else val)
            else:
                data[name] = 0.0

        lag_7_ts = lags["lag_7"]
        if lag_7_ts in df_hist.index:
            data["rolling_7"] = df_hist.loc[ts - pd.Timedelta(days=7):ts - pd.Timedelta(days=1), "Load"].mean()
        else:
            data["rolling_7"] = data.get("lag_7", 0.0)

        x_row = np.array([data.get(col, 0.0) for col in self.feature_cols], dtype=np.float64)
        x_row = (x_row - self.X_mean) / (self.X_std + 1e-8)
        return float(x_row.dot(self.w) + self.b)

    def forecast(self, n_hours=1):
        preds = []
        current_ts = pd.to_datetime(self.df_original["Timestamp"].iloc[-1])
        for _ in range(n_hours):
            next_ts = current_ts + pd.Timedelta(hours=1)
            pred = self.predict([next_ts])
            preds.append((next_ts, pred))
            new_row = pd.DataFrame({"Timestamp": [next_ts], "Load": [pred]})
            self.df_original = pd.concat([self.df_original, new_row], ignore_index=True)
            current_ts = next_ts
        return preds

    def forecast_days(self, n_days=1):
        preds = []
        current_ts = pd.to_datetime(self.df_original["Timestamp"].iloc[-1])
        for _ in range(n_days):
            next_ts = current_ts + pd.Timedelta(days=1)
            pred = self.predict_for_days([next_ts])
            preds.append((next_ts, pred))
            new_row = pd.DataFrame({"Timestamp": [next_ts], "Load": [pred]})
            self.df_original = pd.concat([self.df_original, new_row], ignore_index=True)
            current_ts = next_ts
        return preds