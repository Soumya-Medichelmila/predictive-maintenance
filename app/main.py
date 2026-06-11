from fastapi import FastAPI

from app.routes.predict import router as predict_router
from app.routes.history import router as history_router

from app.database.database import Base, engine
from app.database.models import Prediction

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Predictive Maintenance API"
)

app.include_router(predict_router)
app.include_router(history_router)

@app.get("/")
def home():
    return {
        "message": "Predictive Maintenance API Running"
    }