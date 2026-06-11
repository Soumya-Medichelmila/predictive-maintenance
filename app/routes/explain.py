from fastapi import APIRouter

from app.schemas.predict_schema import PredictionRequest
from app.services.explain_service import explain_prediction

router = APIRouter()

@router.post("/explain")
def explain(request: PredictionRequest):

    result = explain_prediction(request.dict())

    return {
        "top_factors": result
    }