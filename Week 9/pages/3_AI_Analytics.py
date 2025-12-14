import sys
import os

# -------------------------------------------------
# Fix Python paths (KEEP EXACTLY THIS)
# -------------------------------------------------
sys.path.append(os.path.abspath("Week10"))     # ai_services.py
sys.path.append(os.path.abspath("Week 9"))     # ✅ app_db.py (folder has a space)

from ai_services import get_ai_reply           # ✅ correct import
from app_db import get_table_from_csv

import streamlit as st
import plotly.express as px


# -------------------------------------------------
# Auth check
# -------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ You must be logged in to view this page.")
    st.stop()


# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(page_title="AI Analytics", layout="wide")
st.title("🤖 AI Analytics Dashboard")


# -------------------------------------------------
# Load data
# -------------------------------------------------
inc = get_table_from_csv("cyber_incidents")
ds = get_table_from_csv("datasets_metadata")
tickets = get_table_from_csv("it_tickets")


# -------------------------------------------------
# Cyber Analytics
# -------------------------------------------------
st.header("📈 Cyber Incident Analytics")

count_by_type = inc.groupby("incident_type").size().reset_index(name="count")
fig1 = px.bar(
    count_by_type,
    x="incident_type",
    y="count",
    title="Incident Type Frequency",
    color="incident_type"
)
st.plotly_chart(fig1, use_container_width=True)

severity_count = inc.groupby("severity").size().reset_index(name="count")
fig2 = px.pie(
    severity_count,
    names="severity",
    values="count",
    title="Severity Breakdown"
)
st.plotly_chart(fig2, use_container_width=True)


# -------------------------------------------------
# Dataset Analytics
# -------------------------------------------------
st.header("🗄 Dataset Insights")

fig3 = px.histogram(
    ds,
    x="file_size_mb",
    nbins=30,
    title="Dataset File Size Distribution (MB)"
)
st.plotly_chart(fig3, use_container_width=True)

category_count = ds.groupby("category").size().reset_index(name="count")
fig4 = px.bar(
    category_count,
    x="category",
    y="count",
    title="Datasets by Category",
    color="category"
)
st.plotly_chart(fig4, use_container_width=True)


# -------------------------------------------------
# Ticket Analytics
# -------------------------------------------------
st.header("🎫 Ticket Analytics")

tickets_status = tickets.groupby("status").size().reset_index(name="count")
fig5 = px.bar(
    tickets_status,
    x="status",
    y="count",
    title="Tickets by Status",
    color="status"
)
st.plotly_chart(fig5, use_container_width=True)

priority_count = tickets.groupby("priority").size().reset_index(name="count")
fig6 = px.pie(
    priority_count,
    names="priority",
    values="count",
    title="Priority Breakdown"
)
st.plotly_chart(fig6, use_container_width=True)


# -------------------------------------------------
# AI SECTION (1 argument only)
# -------------------------------------------------
st.divider()
st.header("📊 AI Analytics Insights")

analytics_question = st.text_area(
    "Ask AI to analyze dashboard trends:",
    placeholder="What trends do you see in ticket priority?"
)

if st.button("Ask Analytics AI"):
    if analytics_question.strip():
        with st.spinner("AI analyzing trends..."):
            ai_reply = get_ai_reply(analytics_question)   # ✅ one argument only
        st.success("AI Insight")
        st.write(ai_reply)
    else:
        st.warning("Please enter a question.")
