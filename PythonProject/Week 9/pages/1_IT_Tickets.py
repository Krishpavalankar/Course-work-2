import streamlit as st
import plotly.express as px
from app_db import get_table_from_csv
from ai_services import get_ai_reply  # ✅ import once, at top


# 🔐 Block page access unless logged in
if "logged_in" not in st.session_state or st.session_state.logged_in is False:
    st.error("❌ You must be logged in to view this page.")
    st.stop()


# Page config
st.set_page_config(page_title="IT Tickets Dashboard", layout="wide")
st.title("🎫 IT Ticket Management Dashboard")


# Load data
df = get_table_from_csv("it_tickets")


# Sidebar filters
st.sidebar.header("Filters")

priority = st.sidebar.selectbox(
    "Priority",
    ["All"] + sorted(df["priority"].unique()),
    key="priority_filter"
)

status = st.sidebar.selectbox(
    "Status",
    ["All"] + sorted(df["status"].unique()),
    key="status_filter"
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["category"].unique()),
    key="category_filter"
)


# Apply filters
filtered = df.copy()

if priority != "All":
    filtered = filtered[filtered["priority"] == priority]

if status != "All":
    filtered = filtered[filtered["status"] == status]

if category != "All":
    filtered = filtered[filtered["category"] == category]


# Display table
st.subheader(f"Showing {len(filtered)} ticket(s)")
st.dataframe(filtered, use_container_width=True)


# Charts
st.header("📊 Ticket Analytics")

status_count = (
    filtered.groupby("status")
    .size()
    .reset_index(name="count")
)

fig1 = px.bar(
    status_count,
    x="status",
    y="count",
    title="Tickets by Status",
    color="status"
)
st.plotly_chart(fig1, use_container_width=True)


priority_count = (
    filtered.groupby("priority")
    .size()
    .reset_index(name="count")
)

fig2 = px.pie(
    priority_count,
    names="priority",
    values="count",
    title="Priority Distribution"
)
st.plotly_chart(fig2, use_container_width=True)


# ===================== AI SECTION =====================
st.divider()
st.header("🤖 AI IT Ticket Assistant")

question = st.text_area("Ask AI about IT tickets")

if st.button("Ask AI"):
    if question.strip():
        with st.spinner("AI thinking..."):
            answer = get_ai_reply(question)  # ✅ 1 argument only
            st.success("AI Response")
            st.write(answer)
    else:
        st.warning("Please enter a question")
