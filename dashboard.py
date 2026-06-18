import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
import os

# -------------------- CONFIG --------------------
st.set_page_config(page_title="Industrial AI Monitor", layout="wide")

# -------------------- LOAD MODEL --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "models", "machine_health_model.pkl"))

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #1F4E79;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #F4F6F7;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("<div class='big-title'>🏭 Industrial Machine Health Dashboard</div>", unsafe_allow_html=True)
st.markdown("Real-time monitoring & AI-based failure detection")
st.markdown("---")

# -------------------- INPUT SECTION --------------------
st.sidebar.header("⚙️ Sensor Inputs")

temperature = st.sidebar.slider("🌡 Temperature (°C)", 0, 120, 50)
vibration = st.sidebar.slider("📳 Vibration (mm/s)", 0, 20, 5)
pressure = st.sidebar.slider("⚡ Pressure (kPa)", 0, 300, 100)

# Additional visual parameters (not in model)
humidity = st.sidebar.slider("💧 Humidity (%)", 0, 100, 40)
rpm = st.sidebar.slider("🔄 Machine RPM", 0, 5000, 1500)
load = st.sidebar.slider("⚙️ Load (%)", 0, 100, 60)

# -------------------- MODEL INPUT --------------------
input_data = pd.DataFrame({
    'temperature': [temperature],
    'vibration': [vibration],
    'pressure': [pressure]
})

prediction = model.predict(input_data)[0]

# -------------------- METRICS --------------------
st.subheader("📊 Live Machine Metrics")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Temperature", f"{temperature}°C")
col2.metric("Vibration", f"{vibration}")
col3.metric("Pressure", f"{pressure}")
col4.metric("Humidity", f"{humidity}%")
col5.metric("RPM", rpm)
col6.metric("Load", f"{load}%")

st.markdown("---")

# -------------------- STATUS --------------------
st.subheader("🧠 AI Prediction Status")

if prediction == 1:
    st.error("🚨 High Risk of Machine Failure")
else:
    st.success("✅ Machine Operating Normally")

# -------------------- HEALTH SCORE --------------------
health_score = max(0, 100 - (temperature*0.3 + vibration*2 + pressure*0.1))

st.subheader("💚 Health Score")
st.progress(int(health_score))

st.write(f"Health Score: **{int(health_score)}%**")

# -------------------- GAUGE --------------------
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=health_score,
    title={'text': "Machine Health"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 40], 'color': "red"},
            {'range': [40, 70], 'color': "yellow"},
            {'range': [70, 100], 'color': "green"},
        ],
    }
))

st.plotly_chart(fig, use_container_width=True)

# -------------------- BAR GRAPH --------------------
st.subheader("📊 Sensor Overview")

df = pd.DataFrame({
    "Parameter": ["Temp", "Vibration", "Pressure", "Humidity", "RPM", "Load"],
    "Value": [temperature, vibration, pressure, humidity, rpm, load]
})

fig = px.bar(df, x="Parameter", y="Value", color="Parameter")
st.plotly_chart(fig, use_container_width=True)

# -------------------- TREND --------------------
st.subheader("📈 Simulated Trend")

trend_df = pd.DataFrame({
    "Temperature": [temperature-10, temperature-5, temperature],
    "Vibration": [vibration-2, vibration-1, vibration],
    "Pressure": [pressure-20, pressure-10, pressure]
})

st.line_chart(trend_df)