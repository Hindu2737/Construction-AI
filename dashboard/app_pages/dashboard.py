import streamlit as st

from main import run_analysis
from reporting.risk_summary import create_risk_summary
from reporting.recommendations import generate_recommendations
from reporting.pdf_generator import generate_pdf_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ConstructAI | Executive Dashboard",
    page_icon="🏗️",
    layout="wide",
)


# ============================================================
# PAGE HEADER
# ============================================================

st.title("🏗️ ConstructAI Executive Dashboard")
st.caption(
    "Agentic Construction Risk Intelligence Platform"
)

st.markdown(
    """
    Monitor project risk, site safety, worker protection,
    equipment reliability, weather conditions, compliance,
    and insurance risk from one dashboard.
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "dashboard_analysis_result" not in st.session_state:
    st.session_state["dashboard_analysis_result"] = None


# ============================================================
# ANALYSIS FUNCTION
# ============================================================

@st.cache_data(ttl=300)
def get_analysis_results():
    """
    Runs the complete Construction-AI analysis pipeline.

    The actual agent execution is handled by main.py.
    """

    return run_analysis()


# ============================================================
# RUN ANALYSIS
# ============================================================

try:

    if st.session_state["dashboard_analysis_result"] is None:

        with st.spinner(
            "Running Construction-AI intelligence agents..."
        ):
            results = get_analysis_results()

        st.session_state[
            "dashboard_analysis_result"
        ] = results

    else:

        results = st.session_state[
            "dashboard_analysis_result"
        ]


except Exception as e:

    st.error(
        "Unable to run the Construction-AI analysis pipeline."
    )

    st.exception(e)

    st.stop()


# ============================================================
# SAFETY CHECK
# ============================================================

if not isinstance(results, dict):

    st.error(
        "The analysis pipeline did not return a valid result."
    )

    st.stop()


# ============================================================
# CREATE RISK SUMMARY
# ============================================================

try:

    summary = create_risk_summary(results)

except Exception as e:

    st.error(
        "Unable to create the risk summary."
    )

    st.exception(e)

    st.stop()


# ============================================================
# EXTRACT REPORTS SAFELY
# ============================================================

project_risk = results.get(
    "project_risk",
    "Unknown",
)

equipment_mttf = results.get(
    "equipment_mttf",
    0,
)

weather_prediction = results.get(
    "weather_prediction",
    results.get(
        "weather",
        "Unknown",
    ),
)

safety_report = results.get(
    "safety_report",
    {},
)

worker_protection_report = results.get(
    "worker_protection_report",
    {},
)

site_report = results.get(
    "site_report",
    {},
)

compliance_report = results.get(
    "compliance_report",
    {},
)

insurance_report = results.get(
    "insurance_report",
    {},
)


# ============================================================
# RISK VALUES
# ============================================================

site_risk_score = site_report.get(
    "site_risk_score",
    0,
)

site_risk_level = site_report.get(
    "site_risk_level",
    "Unknown",
)


# SafetyIntelligenceAgent produces a SAFETY PROTECTION score.
# Higher = better.
# Therefore risk = 100 - protection score.

safety_protection_score = worker_protection_report.get(
    "safety_score",
    100,
)

try:
    safety_protection_score = float(
        safety_protection_score
    )
except (
    TypeError,
    ValueError,
):
    safety_protection_score = 100


safety_risk_score = max(
    0,
    min(
        100,
        100 - safety_protection_score,
    ),
)


# ============================================================
# DISPLAY OVERALL RISK
# ============================================================

st.markdown("---")

st.subheader("🎯 Overall Risk Overview")


overall_scores = [
    site_risk_score,
    safety_risk_score,
]

insurance_score = insurance_report.get(
    "insurance_risk_score",
    0,
)

try:
    insurance_score = float(
        insurance_score
    )
except (
    TypeError,
    ValueError,
):
    insurance_score = 0

overall_scores.append(
    insurance_score
)

overall_risk_score = round(
    sum(overall_scores) / len(overall_scores)
)


if overall_risk_score >= 70:

    overall_risk_level = "High"

elif overall_risk_score >= 40:

    overall_risk_level = "Medium"

else:

    overall_risk_level = "Low"


# ============================================================
# TOP METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Overall Risk",
        f"{overall_risk_score}/100",
        overall_risk_level,
    )


with col2:

    st.metric(
        "Project Risk",
        str(project_risk),
    )


with col3:

    st.metric(
        "Site Risk",
        f"{site_risk_score}/100",
        site_risk_level,
    )


with col4:

    st.metric(
        "Safety Risk",
        f"{int(safety_risk_score)}/100",
    )


# ============================================================
# SECONDARY METRICS
# ============================================================

st.markdown("### 📊 Operational Intelligence")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Weather",
        str(weather_prediction),
    )


with col2:

    try:
        mttf_display = f"{float(equipment_mttf):.1f}"

    except (
        TypeError,
        ValueError,
    ):
        mttf_display = "N/A"

    st.metric(
        "Equipment MTTF",
        mttf_display,
    )


with col3:

    compliance_status = compliance_report.get(
        "compliance_status",
        "Unknown",
    )

    compliance_score = compliance_report.get(
        "compliance_score",
        0,
    )

    st.metric(
        "Compliance",
        str(compliance_status),
        f"{compliance_score}/100",
    )


with col4:

    insurance_level = insurance_report.get(
        "insurance_risk_level",
        "Unknown",
    )

    st.metric(
        "Insurance Risk",
        str(insurance_level),
    )


# ============================================================
# RISK BREAKDOWN
# ============================================================

st.markdown("---")

st.subheader("📈 Risk Breakdown")


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("#### 🏗️ Site Risk")

    st.progress(
        int(
            max(
                0,
                min(
                    100,
                    site_risk_score,
                ),
            )
        )
    )

    st.write(
        f"**Level:** {site_risk_level}"
    )

    st.write(
        f"**Score:** {site_risk_score}/100"
    )


with col2:

    st.markdown("#### 🦺 Worker Safety Risk")

    st.progress(
        int(safety_risk_score)
    )

    protection_level = worker_protection_report.get(
        "worker_protection_level",
        "Unknown",
    )

    st.write(
        f"**Protection Level:** {protection_level}"
    )

    st.write(
        f"**Risk Score:** {int(safety_risk_score)}/100"
    )


with col3:

    st.markdown("#### 🛡️ Insurance Risk")

    st.progress(
        int(
            max(
                0,
                min(
                    100,
                    insurance_score,
                ),
            )
        )
    )

    st.write(
        f"**Level:** {insurance_level}"
    )

    st.write(
        f"**Score:** {int(insurance_score)}/100"
    )


# ============================================================
# ALERTS
# ============================================================

st.markdown("---")

st.subheader("🚨 Active Risk Alerts")


alerts = []


# Project risk alert
if str(project_risk).lower() == "high":

    alerts.append(
        "🔴 High project risk detected."
    )

elif str(project_risk).lower() == "medium":

    alerts.append(
        "🟠 Medium project risk detected."
    )


# Site risk alert
if site_risk_score >= 60:

    alerts.append(
        "🔴 Site risk is high. Additional inspection is recommended."
    )

elif site_risk_score >= 30:

    alerts.append(
        "🟠 Site risk requires attention."
    )


# Safety alert
violations = worker_protection_report.get(
    "confirmed_violations",
    [],
)

if violations:

    for violation in violations:

        alerts.append(
            f"🔴 Worker safety violation detected: {violation}"
        )


# Weather alert
bad_weather = {
    "Rain",
    "Light Rain",
    "Heavy Rain",
    "Windy",
    "Overcast",
}

if weather_prediction in bad_weather:

    alerts.append(
        f"🟠 Weather-related risk detected: "
        f"{weather_prediction}"
    )


# Equipment alert
try:

    mttf_value = float(
        equipment_mttf
    )

    if mttf_value < 100:

        alerts.append(
            "🔴 Equipment may fail soon. Immediate inspection recommended."
        )

    elif mttf_value < 300:

        alerts.append(
            "🟠 Equipment maintenance should be scheduled."
        )

except (
    TypeError,
    ValueError,
):
    pass


# Compliance alert
if compliance_status != "Compliant":

    alerts.append(
        f"🔴 Compliance status: {compliance_status}"
    )


# Insurance alert
if insurance_level == "High":

    alerts.append(
        "🔴 High insurance risk indicator detected."
    )


if alerts:

    for alert in alerts:

        st.warning(alert)

else:

    st.success(
        "✅ No major risk alerts detected."
    )


# ============================================================
# HAZARDS & FINDINGS
# ============================================================

st.markdown("---")

col1, col2 = st.columns(2)


with col1:

    st.subheader("⚠️ Site Hazards")

    hazards = site_report.get(
        "hazards",
        [],
    )

    if hazards:

        for hazard in hazards:

            st.warning(
                hazard
            )

    else:

        st.success(
            "No site hazards identified."
        )


with col2:

    st.subheader("🦺 Safety Findings")

    if violations:

        for violation in violations:

            st.error(
                violation
            )

    else:

        st.success(
            "No confirmed PPE violations."
        )


# ============================================================
# RECOMMENDED ACTIONS
# ============================================================

st.markdown("---")

st.subheader("💡 Recommended Actions")


recommended_actions = []


# Site actions
recommended_actions.extend(
    site_report.get(
        "recommended_actions",
        [],
    )
)


# Worker protection actions
recommended_actions.extend(
    worker_protection_report.get(
        "recommended_actions",
        [],
    )
)


# Compliance actions
recommended_actions.extend(
    compliance_report.get(
        "recommended_actions",
        [],
    )
)


# Insurance recommendation
insurance_recommendation = insurance_report.get(
    "recommendation"
)

if insurance_recommendation:

    recommended_actions.append(
        insurance_recommendation
    )


# Remove duplicates
recommended_actions = list(
    dict.fromkeys(
        recommended_actions
    )
)


if recommended_actions:

    for index, action in enumerate(
        recommended_actions,
        start=1,
    ):

        st.write(
            f"**{index}.** {action}"
        )

else:

    st.success(
        "Continue routine monitoring and preventive safety controls."
    )


# ============================================================
# COMPLIANCE & INSURANCE
# ============================================================

st.markdown("---")

st.subheader("🛡️ Compliance & Insurance Intelligence")


col1, col2 = st.columns(2)


with col1:

    st.markdown("### Compliance")

    st.write(
        f"**Status:** {compliance_status}"
    )

    st.write(
        f"**Score:** {compliance_score}/100"
    )

    findings = compliance_report.get(
        "findings",
        [],
    )

    if findings:

        for finding in findings:

            violation = finding.get(
                "violation",
                "Unknown",
            )

            severity = finding.get(
                "severity",
                "Unknown",
            )

            requirement = finding.get(
                "requirement",
                "",
            )

            action = finding.get(
                "action",
                "",
            )

            st.markdown(
                f"""
                **{violation}**

                - Severity: `{severity}`
                - Requirement: {requirement}
                - Action: {action}
                """
            )

    else:

        st.success(
            "No compliance findings."
        )


with col2:

    st.markdown("### Insurance Risk")

    st.write(
        f"**Risk Level:** {insurance_level}"
    )

    st.write(
        f"**Risk Score:** {int(insurance_score)}/100"
    )

    recommendation = insurance_report.get(
        "recommendation",
        "No recommendation available.",
    )

    st.info(
        recommendation
    )

    note = insurance_report.get(
        "note"
    )

    if note:

        st.caption(
            note
        )


# ============================================================
# SAFETY INTELLIGENCE
# ============================================================

st.markdown("---")

st.subheader("🧠 Safety Intelligence")


col1, col2, col3 = st.columns(3)


with col1:

    workers_detected = worker_protection_report.get(
        "workers_detected",
        0,
    )

    st.metric(
        "Workers Detected",
        workers_detected,
    )


with col2:

    st.metric(
        "Confirmed Violations",
        len(violations),
    )


with col3:

    st.metric(
        "Protection Score",
        f"{int(safety_protection_score)}/100",
    )


# ============================================================
# SAFETY DETECTIONS
# ============================================================

detections = safety_report.get(
    "detections",
    [],
)

if detections:

    with st.expander(
        "🔍 View Computer Vision Detections"
    ):

        for detection in detections:

            label = detection.get(
                "label",
                "Unknown",
            )

            confidence = detection.get(
                "confidence",
                0,
            )

            st.write(
                f"**{label}** — "
                f"{float(confidence) * 100:.1f}% confidence"
            )


# ============================================================
# REPORTING INTELLIGENCE
# ============================================================

st.markdown("---")

st.subheader("📄 Reporting Intelligence")

st.write(
    """
    Generate an enterprise-style Construction-AI
    risk intelligence report containing the executive
    summary, risk scores, safety findings, compliance
    findings, insurance intelligence and recommended
    actions.
    """
)


# ============================================================
# GENERATE PDF REPORT
# ============================================================

if st.button(
    "📄 Generate Risk Report",
    use_container_width=True,
):

    with st.spinner(
        "Generating Construction-AI risk report..."
    ):

        try:

            # Generate recommendations
            recommendations = generate_recommendations(
                results
            )

            # Generate PDF
            pdf_file = generate_pdf_report(
                summary=summary,
                results=results,
                recommendations=recommendations,
            )

            st.success(
                "✅ Risk report generated successfully."
            )

            st.download_button(
                label="⬇️ Download Risk Report",
                data=pdf_file.getvalue(),
                file_name=(
                    "ConstructAI_Risk_Intelligence_Report.pdf"
                ),
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as e:

            st.error(
                "❌ Unable to generate the risk report."
            )

            st.exception(e)


# ============================================================
# AGENT STATUS
# ============================================================

st.markdown("---")

st.subheader("🤖 Agent Status")


agents = [
    (
        "Project Agent",
        "Project risk prediction",
    ),
    (
        "Resource Agent",
        "Equipment reliability / MTTF",
    ),
    (
        "Weather Agent",
        "Weather risk prediction",
    ),
    (
        "Safety Agent",
        "Computer vision PPE detection",
    ),
    (
        "Safety Intelligence Agent",
        "Worker protection intelligence",
    ),
    (
        "Site Risk Agent",
        "Site-level risk assessment",
    ),
    (
        "Compliance Agent",
        "Safety compliance assessment",
    ),
    (
        "Insurance Intelligence Agent",
        "Insurance risk intelligence",
    ),
]


for agent_name, description in agents:

    col1, col2, col3 = st.columns(
        [2, 5, 1]
    )

    with col1:

        st.write(
            f"**{agent_name}**"
        )

    with col2:

        st.write(
            description
        )

    with col3:

        st.success(
            "Active"
        )


# ============================================================
# DETAILED AGENT OUTPUT
# ============================================================

st.markdown("---")

st.subheader("🔎 Detailed Agent Output")


with st.expander(
    "Project Agent"
):

    st.json(
        {
            "project_risk": project_risk
        }
    )


with st.expander(
    "Resource Agent"
):

    st.json(
        {
            "equipment_mttf": equipment_mttf
        }
    )


with st.expander(
    "Weather Agent"
):

    st.json(
        {
            "weather_prediction": weather_prediction
        }
    )


with st.expander(
    "Safety Agent"
):

    st.json(
        safety_report
    )


with st.expander(
    "Safety Intelligence Agent"
):

    st.json(
        worker_protection_report
    )


with st.expander(
    "Site Risk Agent"
):

    st.json(
        site_report
    )


with st.expander(
    "Compliance Agent"
):

    st.json(
        compliance_report
    )


with st.expander(
    "Insurance Intelligence Agent"
):

    st.json(
        insurance_report
    )


# ============================================================
# REFRESH
# ============================================================

st.markdown("---")

if st.button(
    "🔄 Refresh Analysis",
    use_container_width=True,
):

    st.cache_data.clear()

    st.session_state[
        "dashboard_analysis_result"
    ] = None

    st.rerun()