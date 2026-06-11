from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.predict_schema import PredictionRequest
from app.services.model_service import predict_rul

from app.database.dependencies import get_db
from app.database.models import Prediction

router = APIRouter()

@router.post("/predict")
def predict(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):

    result = predict_rul(request.dict())

    prediction = Prediction(
        engine_id=request.engine_id,
        predicted_rul=result
    )

    db.add(prediction)
    db.commit()

    return {
        "predicted_rul": result
    }