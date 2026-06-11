from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import Prediction

router = APIRouter()

@router.get("/history")
def get_history(
    db: Session = Depends(get_db)
):

    predictions = db.query(Prediction).all()

    return predictions