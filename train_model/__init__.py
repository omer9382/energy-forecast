import logging
import azure.functions as func
from repository.cosmos_repo import CosmosRepo
from models.DataLoader import DataLoader
from models.FE import FE
from models.LinearRegression import LinearRegression

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Python Timer trigger function started training.')

    cosmosclient = CosmosRepo()
    items = cosmosclient.obtain_all()

    dl = DataLoader(items=items)
    df = dl.transform_into_df()

    # 1. Transform data (FE handles datetime and numeric conversion)
    fe = FE(df)
    df_transformed = fe.transform()

    # 2. Define features used for training
    features = [
        "hours", "day_of_week", "month", "is_weekend",
        "lag_1", "lag_24", "lag_168", "rolling_24"
    ]

    # 3. Create and train model
    lrmodel = LinearRegression(df=df_transformed, feature_cols=features)
    w, b, std, mean = lrmodel.compute_cost()

    # 4. Prepare JSON-serializable item
    # We use .tolist() to convert NumPy arrays to standard Python lists
    item = {
        "id": "model_state",
        "w": w.tolist() if hasattr(w, "tolist") else w,
        "b": float(b),
        "std": std.tolist() if hasattr(std, "tolist") else std,
        "mean": mean.tolist() if hasattr(mean, "tolist") else mean
    }

    # 5. Write to Cosmos DB
    cosmosclient.write_to_state(item)
    logging.info('Model trained and saved successfully to Cosmos DB.')