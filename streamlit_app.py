import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px

st.set_page_config(page_title="Machine Anomaly Detection", layout="wide",page_icon="⚙️")

st.title("Machine Anomaly Detection Dashboard")
st.markdown("This dashboard allows you to input machine data and get real-time anomaly detection results using a pre-trained model.")
st.sidebar.header("Input Machine Data")
kiln_temperature = st.sidebar.number_input("Kiln Temperature (°C)", value=100)
mill_vibration = st.sidebar.number_input("Mill Vibration (mm/s)", value=5)
motor_current = st.sidebar.number_input("Motor Current (A)", value=10)
feed_rate = st.sidebar.number_input("Feed Rate (kg/h)", value=50)
gas_pressure = st.sidebar.number_input("Gas Pressure (kPa)", value=4)

payload = {
    "kiln_temperature": kiln_temperature,
    "mill_vibration": mill_vibration,
    "motor_current": motor_current,
    "feed_rate": feed_rate,
    "gas_pressure": gas_pressure
}

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["timestamp", "prediction", "anomaly_score","Alert","result"])
    
def show_alert(prediction, alert):
    if "Huge anomaly detected!" in alert_message.lower():
        color="#ff4b4b"
    elif "Anomaly detected!" in alert_message.lower():
        color="#ffcc00"
    else:
        color="#4caf50"
    st.markdown(f"""
    <div style="
        background-color: {color};
        padding: 10px;
        border-radius: 5px;
        color: white;
        font-weight: bold;
        text-align: center;
    ">
        {prediction}-{alert_message}
    </div>
    """, unsafe_allow_html=True
    )


if st.button("Detect Anomaly"):
    try:
        url = st.secrets["API_URL"] 
        response = requests.post(url, json=payload)
        data = response.json()
        prediction = data.get("prediction", "")
        anomaly_score = data.get("Anomaly Score", 0)
        alert_message = data.get("Recommendation", "")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_row=pd.DataFrame({
            "timestamp": [timestamp],
            "prediction": [prediction],
            "anomaly_score": [anomaly_score],
            "Alert": [alert_message],
            "result": [data.get("prediction", "")]
        })
        st.session_state.history = pd.concat([st.session_state.history, new_row], ignore_index=True)
        show_alert(prediction, alert_message)
        st.metric(label="Anomaly Score", value=f"{anomaly_score:.2f}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")

col1,col2=st.columns([2,3])
with col1:
    st.subheader("Anomaly Detection History")
    if not st.session_state.history.empty:
        fig = px.line(st.session_state.history, x="timestamp", y="anomaly_score", title="Anomaly Score Over Time")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data to display yet. Please input machine data and detect anomalies.")
with col2:
    st.subheader("Detailed History")
    if not st.session_state.history.empty:
        st.dataframe(st.session_state.history[["timestamp", "prediction", "anomaly_score","Alert"]])
    else:
        st.info("No data to display yet. Please input machine data and detect anomalies.")


st.markdown("---")
st.markdown("Created by Justus Omari Kwache - Anomaly Detection System for Industrial Machines")