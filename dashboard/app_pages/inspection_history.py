import json
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.database import get_inspection_count, get_recent_inspections


def load_json_list(value):
    """Safely convert JSON database text into a Python list."""
    if not value:
        return []

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return []


st.title(":material/history: Inspection history")
st.caption(
    "Review previously saved Construction AI site assessments, "
    "risk scores, compliance findings, and uploaded inspection images."
)

inspections = get_recent_inspections(limit=200)

if not inspections:
    with st.container(border=True):
        st.info(
            "No saved inspections yet. Go to **Site assessment**, upload "
            "a construction-site image, and select **Analyze site safety**.",
            icon=":material/info:",
        )

    st.stop()

inspections_df = pd.DataFrame(inspections)

# Convert database timestamps into readable date/time values.
inspections_df["created_at"] = pd.to_datetime(
    inspections_df["created_at"],
    errors="coerce",
)

# ---------------------------------------------------------
# History overview metrics
# ---------------------------------------------------------

total_inspections = get_inspection_count()

high_risk_count = len(
    inspections_df[
        inspections_df["site_risk_level"] == "High"
    ]
)

unsafe_count = len(
    inspections_df[
        inspections_df["safety_status"] == "Unsafe"
    ]
)

non_compliant_count = len(
    inspections_df[
        inspections_df["compliance_status"] == "Non-Compliant"
    ]
)

st.header(":material/analytics: Inspection overview")

with st.container(horizontal=True):
    st.metric(
        "Saved inspections",
        total_inspections,
        border=True,
    )

    st.metric(
        "High-risk inspections",
        high_risk_count,
        border=True,
    )

    st.metric(
        "Unsafe inspections",
        unsafe_count,
        border=True,
    )

    st.metric(
        "Non-compliant inspections",
        non_compliant_count,
        border=True,
    )


# ---------------------------------------------------------
# Filters
# ---------------------------------------------------------

st.header(":material/filter_list: Filter inspections")

filter_left, filter_right, filter_third = st.columns(3)

with filter_left:
    risk_filter = st.selectbox(
        "Site-risk level",
        options=["All", "Low", "Medium", "High"],
    )

with filter_right:
    safety_filter = st.selectbox(
        "Safety status",
        options=["All", "Safe", "Unsafe"],
    )

with filter_third:
    compliance_filter = st.selectbox(
        "Compliance status",
        options=[
            "All",
            "Compliant",
            "Partially Compliant",
            "Non-Compliant",
        ],
    )

filtered_df = inspections_df.copy()

if risk_filter != "All":
    filtered_df = filtered_df[
        filtered_df["site_risk_level"] == risk_filter
    ]

if safety_filter != "All":
    filtered_df = filtered_df[
        filtered_df["safety_status"] == safety_filter
    ]

if compliance_filter != "All":
    filtered_df = filtered_df[
        filtered_df["compliance_status"] == compliance_filter
    ]


# ---------------------------------------------------------
# Inspection table
# ---------------------------------------------------------

st.header(":material/table_chart: Saved inspection records")

display_df = filtered_df[
    [
        "id",
        "created_at",
        "project_type",
        "location",
        "site_risk_level",
        "site_risk_score",
        "safety_status",
        "compliance_status",
        "insurance_risk_level",
    ]
].copy()

display_df = display_df.rename(
    columns={
        "id": "Inspection ID",
        "created_at": "Date and time",
        "project_type": "Project type",
        "location": "Location",
        "site_risk_level": "Site risk",
        "site_risk_score": "Risk score",
        "safety_status": "Safety status",
        "compliance_status": "Compliance status",
        "insurance_risk_level": "Insurance risk",
    }
)

st.dataframe(
    display_df,
    hide_index=True,
    width="stretch",
    column_config={
        "Risk score": st.column_config.ProgressColumn(
            "Risk score",
            min_value=0,
            max_value=100,
            format="%d / 100",
        ),
        "Date and time": st.column_config.DatetimeColumn(
            "Date and time",
            format="DD MMM YYYY, HH:mm",
        ),
    },
)


# ---------------------------------------------------------
# Selected inspection detail view
# ---------------------------------------------------------

st.header(":material/visibility: Inspection details")

if filtered_df.empty:
    st.warning(
        "No saved inspections match the selected filters.",
        icon=":material/filter_alt_off:",
    )

    st.stop()

inspection_options = {
    (
        f"#{row['id']} • {row['project_type']} • "
        f"{row['location']} • {row['created_at'].strftime('%d %b %Y, %H:%M')}"
    ): row["id"]
    for _, row in filtered_df.iterrows()
}

selected_label = st.selectbox(
    "Select a saved inspection",
    options=list(inspection_options.keys()),
)

selected_id = inspection_options[selected_label]

selected_record = filtered_df[
    filtered_df["id"] == selected_id
].iloc[0].to_dict()

selected_hazards = load_json_list(
    selected_record["hazards"]
)

selected_actions = load_json_list(
    selected_record["recommended_actions"]
)

selected_violations = load_json_list(
    selected_record["ppe_violations"]
)

detail_left, detail_right = st.columns([1.1, 1])

with detail_left:
    with st.container(border=True):
        st.subheader("Saved inspection image")

        image_path = Path(selected_record["image_path"])

        if image_path.exists():
            st.image(
                str(image_path),
                caption=selected_record["image_filename"],
                width="stretch",
            )
        else:
            st.warning(
                "The saved inspection image file could not be found.",
                icon=":material/image_not_supported:",
            )

with detail_right:
    with st.container(border=True):
        st.subheader("Risk and compliance summary")

        st.metric(
            "Overall site risk",
            selected_record["site_risk_level"],
        )

        st.metric(
            "Site-risk score",
            f"{selected_record['site_risk_score']} / 100",
        )

        st.metric(
            "Safety status",
            selected_record["safety_status"],
        )

        st.metric(
            "Compliance status",
            selected_record["compliance_status"],
        )

        st.metric(
            "Insurance risk",
            selected_record["insurance_risk_level"],
        )

        st.metric(
            "Equipment MTTF",
            f"{selected_record['equipment_mttf']:.1f}",
        )


hazards_column, violations_column = st.columns(2)

with hazards_column:
    with st.container(border=True):
        st.subheader("Detected hazards")

        if selected_hazards:
            for hazard in selected_hazards:
                st.write(f":material/warning: {hazard}")
        else:
            st.success("No saved hazards for this inspection.")

with violations_column:
    with st.container(border=True):
        st.subheader("Confirmed PPE violations")

        if selected_violations:
            for violation in selected_violations:
                st.error(
                    violation,
                    icon=":material/report:",
                )
        else:
            st.success("No confirmed PPE violations.")


with st.container(border=True):
    st.subheader("Recommended actions")

    if selected_actions:
        for action in selected_actions:
            st.write(f":material/check_circle: {action}")
    else:
        st.success("No actions were recorded for this inspection.")
        