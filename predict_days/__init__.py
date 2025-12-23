import json
import logging
import azure.functions as func

# Import all necessary local modules
from models.FE import FE
from models.DataLoader import DataLoader
from repository.cosmos_repo import CosmosRepo
from models.LinearRegression import LinearRegression
from models.serializer import Serializer

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP Trigger function for predicting electric usage over a number of days.
    This function uses the V1/V3 Azure Functions programming model.
    """

    # ----------------------------------------------------------------------
    # 1. Input Parsing and Validation
    # ----------------------------------------------------------------------
    cosmosclient = CosmosRepo()
    daily_features = [
        "day_of_week", # Captures weekly seasonality (e.g., Mondays vs. Sundays)
        "month",       # Captures annual seasonality (e.g., Summer vs. Winter load)
        "is_weekend",   # Critical for load forecasting (commercial vs. residential)
        "lag_1",       # Yesterday's load (Daily Lag 1)
        "lag_7",       # Same day last week (Daily Lag 7)
        "lag_30",      # Same day last month (Daily Lag 30)
        "rolling_7"    # Average load over the last week (Trend)
    ]
    try:
        # Get JSON body from the request
        req_json = req.get_json()
    except ValueError:
        # Log a warning for bad request format
        logging.warning("Request body is not valid JSON.")
        return func.HttpResponse(
            "Please pass a valid JSON object in the request body",
            status_code=400
        )

    # Validate the required 'days' input
    try:
        days_value = req_json.get('days')
        if days_value is None:
            raise KeyError("'days' field is missing")

        # Ensure it's an integer for the forecast model
        n_days = int(days_value)
    except KeyError as e:
        return func.HttpResponse(
            f"Required field missing: {str(e)}",
            status_code=400
        )
    except ValueError:
        return func.HttpResponse(
            "Value for 'days' must be an integer",
            status_code=400
        )

    # ----------------------------------------------------------------------
    # 2. Model Execution and Forecasting
    # ----------------------------------------------------------------------

    try:
        items = cosmosclient.obtain_all()
        df = DataLoader(items)
        transformed_data = df.transform_into_df()
        fe = FE(transformed_data)
        df = fe.transform()
        lrmodel = LinearRegression(df,daily_features)

        # Safely access the model state
        read_from_model = list(cosmosclient.get_model_state_days())[0]

        lrmodel.load(
            read_from_model["w"],
            read_from_model["b"],
            read_from_model["std"],
            read_from_model["mean"]
        )

        # Prediction
        new_preds = lrmodel.forecast_days(n_days)

        # Serialization for final output format
        serializer = Serializer(new_preds)
        spreds = serializer.serialize()

        # Final JSON preparation
        pred_json = json.dumps(spreds)

        # 3. Success Response
        return func.HttpResponse(
            body=pred_json,
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        # Log the error for debugging in Azure Functions logs
        logging.error(f"Prediction failed with an unhandled exception: {e}", exc_info=True)
        return func.HttpResponse(
            f"Internal server error: A prediction or data retrieval step failed: {str(e)}",
            status_code=500
        )