from fastapi import FastAPI

from app.routes.predict import router as predict_router
from app.routes.history import router as history_router
#from app.routes.explain import router as explain_router

app = FastAPI(
    title="Predictive Maintenance API"
)

app.include_router(predict_router)
#app.include_router(explain_router)
app.include_router(history_router)


@app.get("/")
def home():
    return {
        "message": "Predictive Maintenance API Running"
    }