import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ConstructAI | Site Safety Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

if "dashboard_analysis_result" not in st.session_state:
    st.session_state["dashboard_analysis_result"] = None

if "last_saved_inspection_id" not in st.session_state:
    st.session_state["last_saved_inspection_id"] = None


# IMPORTANT:
# Do NOT create live_monitoring_state here.
# live_monitoring.py creates its own MonitoringState object.


# ============================================================
# NAVIGATION
# ============================================================

page = st.navigation(
    [
        st.Page(
            "app_pages/site_assessment.py",
            title="Site Assessment",
            icon=":material/health_and_safety:",
        ),

        st.Page(
            "app_pages/dashboard.py",
            title="Executive Dashboard",
            icon=":material/dashboard:",
        ),

        st.Page(
            "app_pages/live_monitoring.py",
            title="Live Monitoring",
            icon=":material/videocam:",
        ),

        st.Page(
            "app_pages/inspection_history.py",
            title="Inspection History",
            icon=":material/history:",
        ),
    ],
    position="top",
)


# ============================================================
# RUN PAGE
# ============================================================

page.run()