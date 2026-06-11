import joblib
import pandas as pd
import shap

model = joblib.load("saved_models/rul_model.pkl")

explainer = shap.TreeExplainer(model)

def explain_prediction(data):

    df = pd.DataFrame([data])

    shap_values = explainer.shap_values(df)

    feature_names = df.columns.tolist()

    explanation = {}

    for i, feature in enumerate(feature_names):
        explanation[feature] = round(float(shap_values[0][i]), 2)

    top_features = dict(
        sorted(
            explanation.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]
    )

    return top_features