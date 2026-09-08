import streamlit as st


st.set_page_config(
    page_title="ConstructAI | Site safety intelligence",
    page_icon=":material/construction:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.session_state.setdefault("analysis_result", None)
st.session_state.setdefault("last_saved_inspection_id", None)

page = st.navigation(
    [
        st.Page(
            "app_pages/dashboard.py",
            title="Executive Dashboard",
            icon=":material/dashboard:",
        ),
        st.Page(
            "app_pages/site_assessment.py",
            title="Site assessment",
            icon=":material/health_and_safety:",
        ),
        st.Page(
            "app_pages/inspection_history.py",
            title="Inspection history",
            icon=":material/history:",
        ),
    ],
    position="top",
)

page.run()