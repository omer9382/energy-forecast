import json
import logging
import azure.functions as func
from models.FE import FE
from models.DataLoader import DataLoader
from repository.cosmos_repo import CosmosRepo
from models.LinearRegression import LinearRegression
from models.serializer import Serializer
def main(req:func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    n_hours = req_body['hours']
    repoclient = CosmosRepo()
    items = repoclient.obtain_all()
    df = DataLoader(items)
    transformed_data = df.transform_into_df()
    fe = FE(transformed_data)
    df = fe.transform()
    lrmodel = LinearRegression(df)
    read_from_model = repoclient.get_model_state()[0]
    lrmodel.load(read_from_model["w"],read_from_model["b"],read_from_model["std"],read_from_model["mean"])
    new_preds = lrmodel.forecast(n_hours)
    serializer = Serializer(new_preds)
    spreds = serializer.serialize()
    j_dump = json.dumps(spreds)
    return func.HttpResponse(
        json.dumps(j_dump),
        status_code=200,
        mimetype="application/json"
    )



