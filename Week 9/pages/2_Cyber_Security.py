import streamlit as st
import plotly.express as px
from app_db import get_table_from_csv
from ai_services import get_ai_reply  # ✅ import once


# 🔐 Block page access unless logged in
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("❌ You must be logged in to view this page.")
    st.stop()


# Page config
st.set_page_config(page_title="Cyber Security Dashboard", layout="wide")
st.title("🛡 Cyber Security Incidents Dashboard")


# Load data
df = get_table_from_csv("cyber_incidents")


# Sidebar filters
st.sidebar.header("Filters")

incident_type = st.sidebar.selectbox(
    "Incident Type", ["All"] + sorted(df["incident_type"].unique())
)

severity = st.sidebar.selectbox(
    "Severity", ["All"] + sorted(df["severity"].unique())
)

status = st.sidebar.selectbox(
    "Status", ["All"] + sorted(df["status"].unique())
)


# Apply filters
filtered = df.copy()

if incident_type != "All":
    filtered = filtered[filtered["incident_type"] == incident_type]

if severity != "All":
    filtered = filtered[filtered["severity"] == severity]

if status != "All":
    filtered = filtered[filtered["status"] == status]


# Display data
st.subheader(f"Showing {len(filtered)} incident(s)")
st.dataframe(filtered, use_container_width=True)


# Charts
st.header("📊 Incident Trends")

count_by_type = (
    filtered.groupby("incident_type")
    .size()
    .reset_index(name="count")
)

fig1 = px.bar(
    count_by_type,
    x="incident_type",
    y="count",
    title="Incidents by Type",
    color="incident_type"
)
st.plotly_chart(fig1, use_container_width=True)


severity_count = (
    filtered.groupby("severity")
    .size()
    .reset_index(name="count")
)

fig2 = px.pie(
    severity_count,
    names="severity",
    values="count",
    title="Severity Breakdown"
)
st.plotly_chart(fig2, use_container_width=True)


# ===================== AI SECTION =====================
st.divider()
st.header("🛡️ AI Cyber Security Assistant")

security_question = st.text_area(
    "Ask AI about threats, severity trends, or response priorities"
)

if st.button("Ask Security AI"):
    if security_question.strip():
        with st.spinner("AI thinking..."):
            ai_response = get_ai_reply(security_question)  # ✅ ONE ARGUMENT ONLY
            st.success("AI Recommendation")
            st.write(ai_response)
    else:
        st.warning("Please enter a question")
