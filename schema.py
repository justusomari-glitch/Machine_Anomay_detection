import joblib
from pydantic import BaseModel

anomaly_model = joblib.load('anomaly_model.pkl')
print("Model loaded successfully.")
print("Model type:", type(anomaly_model))
print("features in model:", anomaly_model.feature_names_in_)

class AnomalyDetectionRequest(BaseModel):
        kiln_temperature: float
        mill_vibration: float
        motor_current: float
        feed_rate: float
        gas_pressure: float








    