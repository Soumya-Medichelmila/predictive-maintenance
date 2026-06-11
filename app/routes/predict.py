from fastapi import APIRouter

from app.schemas.predict_schema import PredictionRequest
from app.services.model_service import predict_rul

router = APIRouter()

@router.post("/predict")
def predict(request: PredictionRequest):

    result = predict_rul(request.dict())

    return {
        "predicted_rul": result
    }