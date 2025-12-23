
import azure.functions as func
import logging
from models.DataLoader import DataLoader
from repository.cosmos_repo import CosmosRepo
from models.LinearRegression import LinearRegression
from models.FE import FE
def main(mytimer:func.TimerRequest):
   comsos_repo = CosmosRepo()
   items = comsos_repo.obtain_all()
   dl = DataLoader(items=items)
   df = dl.transform_into_df()
   fe = FE(df)
   transformed = fe.transform_for_days()
   daily_features = [
      "day_of_week", # Captures weekly seasonality (e.g., Mondays vs. Sundays)
      "month",       # Captures annual seasonality (e.g., Summer vs. Winter load)
      "is_weekend",   # Critical for load forecasting (commercial vs. residential)
      "lag_1",       # Yesterday's load (Daily Lag 1)
      "lag_7",       # Same day last week (Daily Lag 7)
      "lag_30",      # Same day last month (Daily Lag 30)
      "rolling_7"    # Average load over the last week (Trend)
   ]
   lr = LinearRegression(transformed,daily_features)
   w, b, std, mean = lr.compute_cost()
   item = {
      "id": "model_state",
      "w": w.tolist() if hasattr(w, "tolist") else w,
      "b": float(b),
      "std": std.tolist() if hasattr(std, "tolist") else std,
      "mean": mean.tolist() if hasattr(mean, "tolist") else mean
   }
   comsos_repo.write_to_state_days(item)
   logging.info('Model trained and saved successfully to Cosmos DB.')



