from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime

from app.database.database import Base

class Prediction(Base):

    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)

    engine_id = Column(Integer)

    predicted_rul = Column(Float)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )