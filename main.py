from agents.project_agent import ProjectAgent

agent = ProjectAgent()

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

print("Predicted Risk:", agent.predict_risk(sample_project))