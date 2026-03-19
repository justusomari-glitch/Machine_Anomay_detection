import pandas as pd
import joblib
from src.schema import AnomalyDetectionRequest
from fastapi import FastAPI

app = FastAPI(title="Anomaly Detection API")
# Load the trained model
model = joblib.load('anomaly_model.pkl')   

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict")
def predict(data: AnomalyDetectionRequest):
    input_dict =data.model_dump()
    input_df = pd.DataFrame([input_dict])
    prediction = model.predict(input_df)
    score = model.decision_function(input_df)
    if prediction[0] == -1:
        if score[0] < -0.13:
            result= "Huge anomaly detected!"
            alert= "Machine is in critical condition. Immediate attention required!"
        else:
            result= "Anomaly detected!"
            alert= "Machine is in poor condition. Schedule maintenance soon."
    else:
        result= "No anomaly detected."
        alert= "Machine is in good condition."
    return {"prediction": result,
            "Recommendation": alert,
            "Anomaly Score": round(float(score[0]), 2)}
