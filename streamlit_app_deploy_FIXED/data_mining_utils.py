import joblib
import pandas as pd

MODEL_PATH = "/content/drive/MyDrive/FinalProject_MultiAgentAI/model/rf_tuned_hiring_model.pkl"
FEATURE_COLUMNS_PATH = "/content/drive/MyDrive/FinalProject_MultiAgentAI/model/feature_columns.pkl"

_model = None
_feature_columns = None


def _load_model():
    global _model, _feature_columns
    if _model is None:
        _model = joblib.load(MODEL_PATH)
        _feature_columns = joblib.load(FEATURE_COLUMNS_PATH)
    return _model, _feature_columns


def predict_hiring_decision(features: dict):
    model, feature_columns = _load_model()
    candidate_df = pd.DataFrame([features])
    candidate_encoded = pd.get_dummies(candidate_df, columns=["Gender", "RecruitmentStrategy"])
    candidate_encoded = candidate_encoded.reindex(columns=feature_columns, fill_value=0)

    pred_label = model.predict(candidate_encoded)[0]
    pred_proba = model.predict_proba(candidate_encoded)[0][1]

    label_text = "Layak Interview" if pred_label == 1 else "Tidak Layak Interview"
    return {"label": label_text, "probability": round(float(pred_proba), 4)}
