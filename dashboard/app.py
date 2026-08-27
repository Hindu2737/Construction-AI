from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st

from agents.project_agent import ProjectAgent
from agents.resource_agent import ResourceAgent
from agents.weather_agent import WeatherAgent
from agents.safety_agent import SafetyAgent
from agents.site_risk_agent import SiteRiskAgent
from agents.safety_intelligence_agent import SafetyIntelligenceAgent


st.set_page_config(
    page_title="Agentic AI for Safety Monitoring with Construction Risk Analytics",
    page_icon="🏗️",
    layout="wide",
)


@st.cache_resource
def load_agents():
    return {
        "project": ProjectAgent(),
        "resource": ResourceAgent(),
        "weather": WeatherAgent(),
        "safety": SafetyAgent(),
        "site_risk": SiteRiskAgent(),
        "safety_intelligence": SafetyIntelligenceAgent(),
    }


@st.cache_data
def load_data():
    equipment_df = pd.read_csv("datasets/resource/resource_processed.csv")
    weather_df = pd.read_csv("datasets/weather/weather_processed.csv")
    return equipment_df, weather_df


agents = load_agents()
equipment_df, weather_df = load_data()

st.title("🏗️ Agentic AI for Safety Monitoring with Construction Risk Analytics")
st.write(
    "Predict project risk, equipment maintenance risk, weather conditions, "
    "and worker PPE violations from a construction-site image."
)

st.sidebar.header("Project Details")

project_type = st.sidebar.selectbox(
    "Project Type",
    ["Tunnel", "Building", "Bridge", "Dam", "Road"],
)

location = st.sidebar.selectbox(
    "Location",
    ["Houston", "New York", "Chicago", "Los Angeles", "Miami"],
)

planned_cost = st.sidebar.number_input(
    "Planned Cost",
    min_value=0.0,
    value=12260784.0,
)

actual_cost = st.sidebar.number_input(
    "Actual Cost",
    min_value=0.0,
    value=15054504.05,
)

accident_count = st.sidebar.number_input(
    "Accident Count",
    min_value=0,
    value=8,
)

uploaded_image = st.file_uploader(
    "Upload a construction-site image for PPE and hazard inspection",
    type=["jpg", "jpeg", "png"],
)

analyze_button = st.button("Analyze Site Risk", type="primary")

if analyze_button:
    if uploaded_image is None:
        st.warning("Please upload a construction-site image first.")
        st.stop()

    # Values required by the trained Project Risk model
    sample_project = {
        "Project_Type": project_type,
        "Location": location,
        "Planned_Cost": planned_cost,
        "Actual_Cost": actual_cost,
        "Cost_Overrun": actual_cost - planned_cost,
        "Planned_Duration": 699,
        "Actual_Duration": 814,
        "Schedule_Deviation": 115,
        "Vibration_Level": 1.53,
        "Crack_Width": 2.81,
        "Load_Bearing_Capacity": 471.2,
        "Temperature": 18.54,
        "Humidity": 49.88,
        "Weather_Condition": "Snowy",
        "Air_Quality_Index": 210,
        "Energy_Consumption": 25202.99,
        "Material_Usage": 244.84,
        "Labor_Hours": 6602,
        "Equipment_Utilization": 76.3,
        "Accident_Count": accident_count,
        "Safety_Risk_Score": 6.19,
        "Image_Analysis_Score": 52.99,
        "Anomaly_Detected": 0,
        "Completion_Percentage": 95.01,
    }

    # Valid feature examples from the datasets
    sample_equipment = (
        equipment_df.drop(columns=["MTTF"]).iloc[0].to_dict()
    )

    sample_weather = (
        weather_df.drop(columns=["Summary"]).iloc[0].to_dict()
    )

    suffix = Path(uploaded_image.name).suffix

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(uploaded_image.getbuffer())
        image_path = temp_file.name

    with st.spinner("Running all AI agents..."):
        project_risk = agents["project"].predict_risk(sample_project)
        equipment_mttf = agents["resource"].predict_mttf(sample_equipment)
        weather = agents["weather"].predict_weather(sample_weather)
        safety_report = agents["safety"].inspect_image(image_path)

        worker_report = agents["safety_intelligence"].analyze_worker_protection(
            safety_report
        )

        site_report = agents["site_risk"].assess_site(
            project_risk=project_risk,
            equipment_mttf=equipment_mttf,
            weather=weather,
            safety_report=safety_report,
        )

    st.divider()
    st.header("Site Risk Monitoring")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Project Risk", project_risk)
    col2.metric("Equipment MTTF", f"{equipment_mttf:.1f}")
    col3.metric("Weather", weather)
    col4.metric("Overall Risk Score", f"{site_report['site_risk_score']} / 100")

    if site_report["site_risk_level"] == "High":
        st.error(f"Overall Site Risk: {site_report['site_risk_level']}")
    elif site_report["site_risk_level"] == "Medium":
        st.warning(f"Overall Site Risk: {site_report['site_risk_level']}")
    else:
        st.success(f"Overall Site Risk: {site_report['site_risk_level']}")

    st.subheader("Detected Hazards")
    for hazard in site_report["hazards"]:
        st.write(f"• {hazard}")

    st.subheader("Recommended Actions")
    for action in site_report["recommended_actions"]:
        st.write(f"• {action}")

    st.divider()
    st.header("Safety Intelligence & Worker Protection")

    left, right = st.columns(2)
    left.image(uploaded_image, caption="Uploaded Site Image", use_container_width=True)
    right.metric(
        "Worker Protection Level",
        worker_report["worker_protection_level"],
    )
    right.metric("Safety Score", f"{worker_report['safety_score']} / 100")
    right.metric("Workers Detected", worker_report["workers_detected"])

    st.subheader("Confirmed PPE Violations")
    if worker_report["confirmed_violations"]:
        for violation in worker_report["confirmed_violations"]:
            st.error(f"• {violation}")
    else:
        st.success("No confirmed PPE violations found.")

    st.subheader("Worker Protection Actions")
    if worker_report["recommended_actions"]:
        for action in worker_report["recommended_actions"]:
            st.write(f"• {action}")
    else:
        st.success("Continue standard site-safety monitoring.")

    with st.expander("View all YOLO detections"):
        st.dataframe(pd.DataFrame(safety_report["detections"]))

