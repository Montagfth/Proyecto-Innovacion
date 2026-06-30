from fastapi import APIRouter, Request, Response, Query
from prediction.predict_models import PredictRequest

router = APIRouter()

@router.get("/")
async def get_prediction(order: PredictRequest = Query()):
 return "oal"