from agents.project_agent import ProjectAgent
from agents.resource_agent import ResourceAgent
from agents.weather_agent import WeatherAgent

project_agent = ProjectAgent()
resource_agent = ResourceAgent()
weather_agent = WeatherAgent()

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

sample_equipment = {
    "ProductType": "L12",
    "Humidity": 65.0,
    "Temperature": 28.0,
    "Age": 5,
    "Quantity": 40000,
}

sample_weather = {
    "Precip Type": "rain",
    "Temperature (C)": 18.0,
    "Apparent Temperature (C)": 17.5,
    "Humidity": 0.80,
    "Wind Speed (km/h)": 15.0,
    "Wind Bearing (degrees)": 200.0,
    "Visibility (km)": 8.0,
    "Pressure (millibars)": 1012.0,
    "Hour": 14,
    "Month": 8,
    "Day_Of_Week": 2,
}

print("Predicted Project Risk:", project_agent.predict_risk(sample_project))
print("Predicted Equipment MTTF:", resource_agent.predict_mttf(sample_equipment))
print("Predicted Weather:", weather_agent.predict_weather(sample_weather))