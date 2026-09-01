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
from agents.compliance_agent import ComplianceAgent
from agents.insurance_agent import InsuranceIntelligenceAgent


st.set_page_config(
    page_title="ConstructAI | Site safety intelligence",
    page_icon=":material/construction:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_agents():
    """Load all trained models only once while the app is running."""
    return {
        "project": ProjectAgent(),
        "resource": ResourceAgent(),
        "weather": WeatherAgent(),
        "safety": SafetyAgent(),
        "site_risk": SiteRiskAgent(),
        "safety_intelligence": SafetyIntelligenceAgent(),
        "compliance": ComplianceAgent(),
        "insurance": InsuranceIntelligenceAgent(),
    }


@st.cache_data
def load_source_data():
    """Load datasets used as valid input templates for the ML models."""
    project_df = pd.read_csv(
        "datasets/project_management/project_processed.csv"
    )

    equipment_df = pd.read_csv(
        "datasets/resource/resource_processed.csv"
    )

    weather_df = pd.read_csv(
        "datasets/weather/weather_processed.csv"
    )

    return project_df, equipment_df, weather_df


def status_color(value):
    """Return a Streamlit badge color based on a status label."""
    text = str(value).lower()

    if (
        "high" in text
        or "unsafe" in text
        or "non-compliant" in text
    ):
        return "red"

    if (
        "medium" in text
        or "attention" in text
        or "partial" in text
    ):
        return "orange"

    return "green"


def run_analysis(
    agents,
    sample_project,
    sample_equipment,
    sample_weather,
    uploaded_image,
):
    """Run every AI agent and return one complete site assessment."""
    image_suffix = Path(uploaded_image.name).suffix.lower()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=image_suffix,
    ) as temp_file:
        temp_file.write(uploaded_image.getbuffer())
        temporary_image_path = Path(temp_file.name)

    try:
        project_risk = agents["project"].predict_risk(sample_project)

        equipment_mttf = agents["resource"].predict_mttf(
            sample_equipment
        )

        weather_prediction = agents["weather"].predict_weather(
            sample_weather
        )

        safety_report = agents["safety"].inspect_image(
            str(temporary_image_path)
        )

        worker_protection_report = (
            agents["safety_intelligence"].analyze_worker_protection(
                safety_report
            )
        )

        site_report = agents["site_risk"].assess_site(
            project_risk=project_risk,
            equipment_mttf=equipment_mttf,
            weather=weather_prediction,
            safety_report=safety_report,
        )

        compliance_report = agents["compliance"].assess_compliance(
            safety_report=safety_report,
            worker_protection_report=worker_protection_report,
        )

        insurance_report = agents["insurance"].assess_insurance_risk(
            site_report=site_report,
            compliance_report=compliance_report,
            equipment_mttf=equipment_mttf,
        )

        return {
            "project_risk": project_risk,
            "equipment_mttf": equipment_mttf,
            "weather_prediction": weather_prediction,
            "safety_report": safety_report,
            "worker_protection_report": worker_protection_report,
            "site_report": site_report,
            "compliance_report": compliance_report,
            "insurance_report": insurance_report,
            "image_name": uploaded_image.name,
            "image_bytes": uploaded_image.getvalue(),
        }

    finally:
        temporary_image_path.unlink(missing_ok=True)


# ---------------------------------------------------------
# Load application resources
# ---------------------------------------------------------

st.session_state.setdefault("analysis_result", None)

agents = load_agents()
project_df, equipment_df, weather_df = load_source_data()

project_template = (
    project_df
    .drop(columns=["Risk_Level"])
    .iloc[0]
    .to_dict()
)

equipment_template = (
    equipment_df
    .drop(columns=["MTTF"])
    .iloc[0]
    .to_dict()
)

weather_template = (
    weather_df
    .drop(columns=["Summary"])
    .iloc[0]
    .to_dict()
)

project_types = sorted(
    project_df["Project_Type"].dropna().unique()
)

locations = sorted(
    project_df["Location"].dropna().unique()
)

weather_conditions = sorted(
    project_df["Weather_Condition"].dropna().unique()
)


# ---------------------------------------------------------
# Sidebar: project input and compact result summaries
# ---------------------------------------------------------

with st.sidebar:
    st.title("ConstructAI")
    st.caption("Construction safety intelligence dashboard")

    st.header(":material/tune: Project details")

    project_type = st.selectbox(
        "Project type",
        options=project_types,
        index=project_types.index(project_template["Project_Type"]),
    )

    location = st.selectbox(
        "Location",
        options=locations,
        index=locations.index(project_template["Location"]),
    )

    weather_condition = st.selectbox(
        "Current site weather",
        options=weather_conditions,
        index=weather_conditions.index(
            project_template["Weather_Condition"]
        ),
    )

    planned_cost = st.number_input(
        "Planned cost",
        min_value=0.0,
        value=float(project_template["Planned_Cost"]),
        step=10000.0,
    )

    actual_cost = st.number_input(
        "Current cost",
        min_value=0.0,
        value=float(project_template["Actual_Cost"]),
        step=10000.0,
    )

    accident_count = st.number_input(
        "Recent accidents",
        min_value=0,
        value=int(project_template["Accident_Count"]),
        step=1,
    )

    st.caption(
        "Upload the construction-site image in the main workspace."
    )

    if st.session_state["analysis_result"] is not None:
        result = st.session_state["analysis_result"]

        st.header(":material/summarize: Latest results")

        st.badge(
            f"Site risk: {result['site_report']['site_risk_level']}",
            color=status_color(result["site_report"]["site_risk_level"]),
        )

        st.badge(
            f"Safety: {result['safety_report']['status']}",
            color=status_color(result["safety_report"]["status"]),
        )

        st.badge(
            f"Compliance: {result['compliance_report']['compliance_status']}",
            color=status_color(
                result["compliance_report"]["compliance_status"]
            ),
        )

        st.badge(
            f"Insurance: {result['insurance_report']['insurance_risk_level']}",
            color=status_color(
                result["insurance_report"]["insurance_risk_level"]
            ),
        )

        st.space("small")

        with st.expander(
            "Project and equipment",
            icon=":material/engineering:",
        ):
            st.metric("Project risk", result["project_risk"])
            st.metric(
                "Equipment MTTF",
                f"{result['equipment_mttf']:.1f}",
            )
            st.metric(
                "Weather prediction",
                result["weather_prediction"],
            )

        with st.expander(
            "Safety result",
            icon=":material/health_and_safety:",
        ):
            st.metric(
                "Safety score",
                f"{result['worker_protection_report']['safety_score']} / 100",
            )
            st.metric(
                "Workers detected",
                result["worker_protection_report"]["workers_detected"],
            )

        with st.expander(
            "Compliance and insurance",
            icon=":material/gavel:",
        ):
            st.metric(
                "Compliance score",
                f"{result['compliance_report']['compliance_score']} / 100",
            )
            st.metric(
                "Insurance score",
                f"{result['insurance_report']['insurance_risk_score']} / 100",
            )

    st.space("small")
    st.caption("ConstructAI • AI-assisted internal risk-support tool")


# ---------------------------------------------------------
# Main header / app bar
# ---------------------------------------------------------

header_left, header_right = st.columns([4, 1], vertical_alignment="center")

with header_left:
    st.title(":material/construction: Construction site intelligence")
    st.caption(
        "Analyze project risk, equipment reliability, worker protection, "
        "compliance, and insurance risk from one site assessment."
    )

with header_right:
    with st.container(horizontal_alignment="right"):
        st.badge(
            "AI monitoring active",
            icon=":material/monitoring:",
            color="blue",
        )


# ---------------------------------------------------------
# Main image-upload panel
# ---------------------------------------------------------

st.space("small")

with st.container(border=True):
    upload_left, upload_right = st.columns(
        [2, 1],
        vertical_alignment="center",
    )

    with upload_left:
        st.subheader(":material/upload: Upload a construction-site image")
        st.caption(
            "Use a JPG or PNG image containing workers, PPE, machinery, "
            "vehicles, or safety cones."
        )

        uploaded_image = st.file_uploader(
            "Choose a site image",
            type=["jpg", "jpeg", "png"],
            key="main_image_upload",
        )

    with upload_right:
        st.subheader("Ready to analyze")
        st.write(
            "ConstructAI combines project, equipment, weather, image safety, "
            "compliance, and insurance intelligence."
        )

        analyze_site = st.button(
            "Analyze site safety",
            type="primary",
            icon=":material/analytics:",
            width="stretch",
        )


# ---------------------------------------------------------
# Run AI analysis only when the user selects the button
# ---------------------------------------------------------

if analyze_site:
    if uploaded_image is None:
        st.warning(
            "Upload a construction-site image before starting analysis.",
            icon=":material/upload:",
        )
    else:
        sample_project = project_template.copy()

        sample_project.update({
            "Project_Type": project_type,
            "Location": location,
            "Weather_Condition": weather_condition,
            "Planned_Cost": planned_cost,
            "Actual_Cost": actual_cost,
            "Cost_Overrun": actual_cost - planned_cost,
            "Accident_Count": accident_count,
        })

        with st.status(
            "Running Construction AI agents...",
            expanded=True,
        ) as status:
            st.write("Analyzing project risk...")
            st.write("Checking equipment maintenance risk...")
            st.write("Predicting weather conditions...")
            st.write("Inspecting PPE and visual safety hazards...")
            st.write("Creating compliance and insurance intelligence...")

            st.session_state["analysis_result"] = run_analysis(
                agents=agents,
                sample_project=sample_project,
                sample_equipment=equipment_template.copy(),
                sample_weather=weather_template.copy(),
                uploaded_image=uploaded_image,
            )

            status.update(
                label="Site assessment complete",
                state="complete",
                expanded=False,
            )

        st.toast(
            "Site assessment completed.",
            icon=":material/check_circle:",
        )


# ---------------------------------------------------------
# Main dashboard results
# ---------------------------------------------------------

result = st.session_state["analysis_result"]

if result is None:
    with st.container(border=True):
        st.header("Start a new site assessment")
        st.write(
            "Enter project details in the sidebar, upload a construction-site "
            "image above, and select **Analyze site safety**."
        )

        st.caption(
            "The system combines Project Risk, Equipment MTTF, Weather, "
            "YOLO PPE Detection, Compliance, and Insurance Intelligence."
        )

    st.stop()


# ---------------------------------------------------------
# Milestone 1: Site risk monitoring
# ---------------------------------------------------------

st.header(":material/monitoring: Site risk monitoring")

with st.container(horizontal=True):
    st.metric(
        "Overall site risk",
        result["site_report"]["site_risk_level"],
        border=True,
    )

    st.metric(
        "Site-risk score",
        f"{result['site_report']['site_risk_score']} / 100",
        border=True,
    )

    st.metric(
        "Project risk",
        result["project_risk"],
        border=True,
    )

    st.metric(
        "Equipment MTTF",
        f"{result['equipment_mttf']:.1f}",
        border=True,
    )

if result["site_report"]["site_risk_level"] == "High":
    st.error(
        "High site risk detected. Review the hazards and recommended "
        "actions before continuing affected work.",
        icon=":material/error:",
    )
elif result["site_report"]["site_risk_level"] == "Medium":
    st.warning(
        "Medium site risk detected. Monitor the site and resolve "
        "the listed issues.",
        icon=":material/warning:",
    )
else:
    st.success(
        "Low site risk detected. Continue normal site monitoring.",
        icon=":material/check_circle:",
    )

hazards_column, actions_column = st.columns(2)

with hazards_column:
    with st.container(border=True):
        st.subheader("Detected hazards")

        if result["site_report"]["hazards"]:
            for hazard in result["site_report"]["hazards"]:
                st.write(f":material/warning: {hazard}")
        else:
            st.success("No site-level hazards found.")

with actions_column:
    with st.container(border=True):
        st.subheader("Recommended actions")

        if result["site_report"]["recommended_actions"]:
            for action in result["site_report"]["recommended_actions"]:
                st.write(f":material/check_circle: {action}")
        else:
            st.success("Continue standard site monitoring.")


# ---------------------------------------------------------
# Milestone 2: Safety and worker protection
# ---------------------------------------------------------

st.header(":material/health_and_safety: Safety intelligence & worker protection")

image_column, safety_column = st.columns([1.3, 1])

with image_column:
    with st.container(border=True):
        st.subheader("Uploaded site image")

        st.image(
            result["image_bytes"],
            caption=result["image_name"],
            width="stretch",
        )

with safety_column:
    with st.container(border=True):
        st.subheader("Worker protection status")

        st.metric(
            "Safety status",
            result["safety_report"]["status"],
        )

        st.metric(
            "Worker protection level",
            result["worker_protection_report"]["worker_protection_level"],
        )

        st.metric(
            "Safety score",
            f"{result['worker_protection_report']['safety_score']} / 100",
        )

        st.metric(
            "Workers detected",
            result["worker_protection_report"]["workers_detected"],
        )

with st.container(border=True):
    st.subheader("Objects detected in image")

    safety_detections = result["safety_report"]["detections"]

    if safety_detections:
        st.dataframe(
            pd.DataFrame(safety_detections),
            hide_index=True,
            width="stretch",
        )
    else:
        st.info(
            "No trained construction-safety classes were confidently detected. "
            "Use an image containing workers, PPE, machinery, vehicles, "
            "or safety cones.",
            icon=":material/info:",
        )

ppe_column, protection_column = st.columns(2)

with ppe_column:
    with st.container(border=True):
        st.subheader("Confirmed PPE violations")

        violations = result["worker_protection_report"][
            "confirmed_violations"
        ]

        if violations:
            for violation in violations:
                st.error(
                    violation,
                    icon=":material/report:",
                )
        else:
            st.success(
                "No confirmed PPE violations found.",
                icon=":material/check_circle:",
            )

with protection_column:
    with st.container(border=True):
        st.subheader("Worker protection actions")

        protection_actions = result["worker_protection_report"][
            "recommended_actions"
        ]

        if protection_actions:
            for action in protection_actions:
                st.write(f":material/check_circle: {action}")
        else:
            st.success("Continue standard worker-protection monitoring.")


# ---------------------------------------------------------
# Milestone 3: Compliance and insurance intelligence
# ---------------------------------------------------------

st.header(":material/gavel: Compliance & insurance intelligence")

with st.container(horizontal=True):
    st.metric(
        "Compliance status",
        result["compliance_report"]["compliance_status"],
        border=True,
    )

    st.metric(
        "Compliance score",
        f"{result['compliance_report']['compliance_score']} / 100",
        border=True,
    )

    st.metric(
        "Insurance risk level",
        result["insurance_report"]["insurance_risk_level"],
        border=True,
    )

    st.metric(
        "Insurance risk score",
        f"{result['insurance_report']['insurance_risk_score']} / 100",
        border=True,
    )

compliance_status = result["compliance_report"]["compliance_status"]

if compliance_status == "Non-Compliant":
    st.error(
        "Non-compliant site condition. Resolve listed violations before "
        "affected work continues.",
        icon=":material/gavel:",
    )
elif compliance_status == "Partially Compliant":
    st.warning(
        "Partially compliant. Complete corrective actions and perform "
        "a follow-up inspection.",
        icon=":material/warning:",
    )
else:
    st.success(
        "No confirmed compliance violations found.",
        icon=":material/check_circle:",
    )

with st.container(border=True):
    st.subheader("Compliance findings")

    compliance_findings = result["compliance_report"]["findings"]

    if compliance_findings:
        compliance_dataframe = pd.DataFrame(compliance_findings)

        st.dataframe(
            compliance_dataframe[
                ["violation", "severity", "requirement", "action"]
            ],
            hide_index=True,
            width="stretch",
        )
    else:
        st.success("No confirmed compliance findings.")

with st.container(border=True):
    st.subheader("Insurance-risk recommendation")

    st.info(
        result["insurance_report"]["recommendation"],
        icon=":material/analytics:",
    )

    st.caption(result["insurance_report"]["note"])