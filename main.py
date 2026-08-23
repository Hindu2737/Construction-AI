import pandas as pd

from agents.project_agent import ProjectAgent
from agents.resource_agent import ResourceAgent
from agents.weather_agent import WeatherAgent
from agents.safety_agent import SafetyAgent
from agents.site_risk_agent import SiteRiskAgent
from agents.safety_intelligence_agent import SafetyIntelligenceAgent


# Load all trained agents
project_agent = ProjectAgent()
resource_agent = ResourceAgent()
weather_agent = WeatherAgent()
safety_agent = SafetyAgent()
site_risk_agent = SiteRiskAgent()
safety_intelligence_agent = SafetyIntelligenceAgent()


# Project model input
sample_project = {
    "Project_Type": "Tunnel",
    "Location": "Houston",
    "Planned_Cost": 12260784,
    "Actual_Cost": 15054504.05,
    "Cost_Overrun": 2793720.05,
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
    "Accident_Count": 8,
    "Safety_Risk_Score": 6.19,
    "Image_Analysis_Score": 52.99,
    "Anomaly_Detected": 0,
    "Completion_Percentage": 95.01,
}


# Read valid equipment inputs from the processed dataset.
sample_equipment = (
    pd.read_csv("datasets/resource/resource_processed.csv")
    .drop(columns=["MTTF"])
    .iloc[0]
    .to_dict()
)

# Read valid weather inputs from the processed dataset.
sample_weather = (
    pd.read_csv("datasets/weather/weather_processed.csv")
    .drop(columns=["Summary"])
    .iloc[0]
    .to_dict()
)

# Test image for Safety Agent.
image_path = (
    "datasets/contruction site safety image dataflow/"
    "css-data/test/images/"
    "000005_jpg.rf.96e9379ccae638140c4a90fc4b700a2b.jpg"
)


# Run every trained model.
project_risk = project_agent.predict_risk(sample_project)
equipment_mttf = resource_agent.predict_mttf(sample_equipment)
weather = weather_agent.predict_weather(sample_weather)
safety_report = safety_agent.inspect_image(image_path)

# Convert safety detections into worker-protection intelligence.
worker_protection_report = (
    safety_intelligence_agent.analyze_worker_protection(safety_report)
)

# Combine all four model outputs into overall site monitoring.
site_report = site_risk_agent.assess_site(
    project_risk=project_risk,
    equipment_mttf=equipment_mttf,
    weather=weather,
    safety_report=safety_report,
)


print("\n--- SITE RISK MONITORING REPORT ---")
print("Project Risk:", project_risk)
print("Equipment MTTF:", round(equipment_mttf, 2))
print("Weather:", weather)
print("Safety Status:", safety_report["status"])
print("Overall Site Risk:", site_report["site_risk_level"])
print("Risk Score:", site_report["site_risk_score"], "/ 100")

print("\nHazards:")
for hazard in site_report["hazards"]:
    print("-", hazard)

print("\nRecommended Actions:")
for action in site_report["recommended_actions"]:
    print("-", action)


print("\n--- SAFETY INTELLIGENCE & WORKER PROTECTION ---")
print(
    "Protection Level:",
    worker_protection_report["worker_protection_level"]
)
print("Safety Score:", worker_protection_report["safety_score"], "/ 100")
print("Workers Detected:", worker_protection_report["workers_detected"])

print("\nConfirmed PPE Violations:")
if worker_protection_report["confirmed_violations"]:
    for violation in worker_protection_report["confirmed_violations"]:
        print("-", violation)
else:
    print("- No confirmed PPE violations.")

print("\nWorker Protection Actions:")
if worker_protection_report["recommended_actions"]:
    for action in worker_protection_report["recommended_actions"]:
        print("-", action)
else:
    print("- Continue standard site-safety monitoring.")