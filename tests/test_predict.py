from fastapi.testclient import TestClient
from src.predict import app
client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_predict_route_valid_input():
    payload = {
        "kiln_temperature": 3000,
        "mill_vibration": 600,
        "motor_current": 90,
        "feed_rate": 60,
        "gas_pressure": 100
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_route_invalid_input():
    payload = {
        "kiln_temperature": "high",
        "mill_vibration": 600,
        "motor_current": 90,
        "feed_rate": 60,
        "gas_pressure": 100
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
