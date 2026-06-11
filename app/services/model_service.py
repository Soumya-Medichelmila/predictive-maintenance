import joblib
import pandas as pd

model = joblib.load("saved_models/rul_model.pkl")


def predict_rul(data):
    df = pd.DataFrame([data])

    prediction = model.predict(df)[0]

    return round(float(prediction), 2)