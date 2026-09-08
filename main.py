import pandas as pd

from agents.project_agent import ProjectAgent
from agents.resource_agent import ResourceAgent
from agents.weather_agent import WeatherAgent
from agents.safety_agent import SafetyAgent
from agents.site_risk_agent import SiteRiskAgent
from agents.safety_intelligence_agent import SafetyIntelligenceAgent
from agents.compliance_agent import ComplianceAgent
from agents.insurance_agent import InsuranceIntelligenceAgent


# ============================================================
# LOAD ALL AGENTS
# ============================================================

project_agent = ProjectAgent()
resource_agent = ResourceAgent()
weather_agent = WeatherAgent()
safety_agent = SafetyAgent()
site_risk_agent = SiteRiskAgent()
safety_intelligence_agent = SafetyIntelligenceAgent()
compliance_agent = ComplianceAgent()
insurance_agent = InsuranceIntelligenceAgent()


# ============================================================
# DEFAULT PROJECT INPUT
# ============================================================

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


# ============================================================
# MAIN ANALYSIS FUNCTION
# ============================================================

def run_analysis(
    project_data=None,
    equipment_data=None,
    weather_data=None,
    image_path=None,
):
    """
    Runs the complete Construction-AI intelligence pipeline.

    Returns:
        dict containing all agent outputs.
    """

    # --------------------------------------------------------
    # Use default project data if none is provided
    # --------------------------------------------------------

    if project_data is None:
        project_data = sample_project


    # --------------------------------------------------------
    # Load equipment data
    # --------------------------------------------------------

    if equipment_data is None:

        equipment_data = (
            pd.read_csv(
                "datasets/resource/resource_processed.csv"
            )
            .drop(columns=["MTTF"])
            .iloc[0]
            .to_dict()
        )


    # --------------------------------------------------------
    # Load weather data
    # --------------------------------------------------------

    if weather_data is None:

        weather_data = (
            pd.read_csv(
                "datasets/weather/weather_processed.csv"
            )
            .drop(columns=["Summary"])
            .iloc[0]
            .to_dict()
        )


    # --------------------------------------------------------
    # Default safety image
    # --------------------------------------------------------

    if image_path is None:

        image_path = (
            "datasets/contruction site safety image dataflow/"
            "css-data/test/images/"
            "000005_jpg.rf.96e9379ccae638140c4a90fc4b700a2b.jpg"
        )


    # ========================================================
    # 1. PROJECT AGENT
    # ========================================================

    project_risk = project_agent.predict_risk(
        project_data
    )


    # ========================================================
    # 2. RESOURCE AGENT
    # ========================================================

    equipment_mttf = resource_agent.predict_mttf(
        equipment_data
    )


    # ========================================================
    # 3. WEATHER AGENT
    # ========================================================

    weather = weather_agent.predict_weather(
        weather_data
    )


    # ========================================================
    # 4. SAFETY / YOLO AGENT
    # ========================================================

    safety_report = safety_agent.inspect_image(
        image_path
    )


    # ========================================================
    # 5. SAFETY INTELLIGENCE
    # ========================================================

    worker_protection_report = (
        safety_intelligence_agent.analyze_worker_protection(
            safety_report
        )
    )


    # ========================================================
    # 6. SITE RISK
    # ========================================================

    site_report = site_risk_agent.assess_site(
        project_risk=project_risk,
        equipment_mttf=equipment_mttf,
        weather=weather,
        safety_report=safety_report,
    )


    # ========================================================
    # 7. COMPLIANCE
    # ========================================================

    compliance_report = (
        compliance_agent.assess_compliance(
            safety_report=safety_report,
            worker_protection_report=worker_protection_report,
        )
    )


    # ========================================================
    # 8. INSURANCE INTELLIGENCE
    # ========================================================

    insurance_report = (
        insurance_agent.assess_insurance_risk(
            site_report=site_report,
            compliance_report=compliance_report,
            equipment_mttf=equipment_mttf,
        )
    )


    # ========================================================
    # RETURN EVERYTHING
    # ========================================================

    return {
    "project_risk": project_risk,
    "equipment_mttf": float(equipment_mttf),

    # Keep the existing key used by site_assessment.py
    "weather_prediction": weather,

    # Also keep this for the new dashboard/reporting layer
    "weather": weather,

    "safety_report": safety_report,

    "worker_protection_report":
        worker_protection_report,

    "site_report":
        site_report,

    "compliance_report":
        compliance_report,

    "insurance_report":
        insurance_report,
    }


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    results = run_analysis()

    print("\n========================================")
    print("   CONSTRUCTION-AI ANALYSIS")
    print("========================================")

    print("\n--- PROJECT ---")
    print(
        "Project Risk:",
        results["project_risk"]
    )

    print("\n--- RESOURCE ---")
    print(
        "Equipment MTTF:",
        round(results["equipment_mttf"], 2)
    )

    print("\n--- WEATHER ---")
    print(
        "Weather:",
        results["weather"]
    )

    print("\n--- SAFETY ---")

    safety = results["safety_report"]

    print(
        "Safety Status:",
        safety["status"]
    )

    print(
        "Detections:",
        len(safety["detections"])
    )

    print(
        "Violations:",
        len(safety["violations"])
    )

    print("\n--- WORKER PROTECTION ---")

    protection = results[
        "worker_protection_report"
    ]

    print(
        "Protection Level:",
        protection["worker_protection_level"]
    )

    print(
        "Safety Score:",
        protection["safety_score"],
        "/ 100"
    )

    print(
        "Workers Detected:",
        protection["workers_detected"]
    )

    print("\n--- SITE RISK ---")

    site = results["site_report"]

    print(
        "Site Risk:",
        site["site_risk_level"]
    )

    print(
        "Site Risk Score:",
        site["site_risk_score"],
        "/ 100"
    )

    print("\nHazards:")

    for hazard in site["hazards"]:
        print("-", hazard)


    print("\n--- COMPLIANCE ---")

    compliance = results[
        "compliance_report"
    ]

    print(
        "Compliance:",
        compliance["compliance_status"]
    )

    print(
        "Compliance Score:",
        compliance["compliance_score"],
        "/ 100"
    )


    print("\n--- INSURANCE ---")

    insurance = results[
        "insurance_report"
    ]

    print(
        "Insurance Risk:",
        insurance["insurance_risk_level"]
    )

    print(
        "Insurance Score:",
        insurance["insurance_risk_score"],
        "/ 100"
    )

    print(
        "Recommendation:",
        insurance["recommendation"]
    )