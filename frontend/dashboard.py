import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Business Operations Intelligence", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")
API = os.getenv("API_BASE_URL", "http://localhost:8000")

st.title("📊 Business Operations Intelligence")
st.caption("One view of revenue, expenses, workforce performance and operational bottlenecks.")

def get(path, default=None):
    try:
        response = requests.get(f"{API}{path}", timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Cannot reach API at {API}. Start FastAPI first. Details: {exc}")
        return default

def money(value):
    return f"₹{value:,.0f}"

with st.sidebar:
    st.header("Controls")
    st.write("Data source: local SQLite demo database")
    horizon = st.slider("Forecast horizon (days)", 7, 90, 30)
    if st.button("Refresh dashboard", use_container_width=True):
        st.cache_data.clear()
    st.divider()
    st.caption("Demo data is synthetic. Validate all alerts before acting.")

metrics = get("/api/overview")
if not metrics:
    st.stop()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total revenue", money(metrics["total_revenue"]))
c2.metric("Total expenses", money(metrics["total_expenses"]))
c3.metric("Net after expenses", money(metrics["net_after_expenses"]))
c4.metric("Delayed tasks", f'{metrics["delayed_tasks"]} ({metrics["delay_rate_pct"]}%)')

st.divider()
left,right = st.columns([1.35,1])
with left:
    st.subheader("Revenue by month and department")
    trend = get("/api/revenue-trend", [])
    if trend:
        df = pd.DataFrame(trend)
        fig = px.bar(df, x="month", y="revenue", color="department", barmode="group",
                     title="Monthly revenue")
        fig.update_layout(legend_title_text="Department", xaxis_title="", yaxis_title="Revenue (₹)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No revenue records found. Run `python -m app.seed`.")
with right:
    st.subheader("Department performance")
    departments = get("/api/department-performance", [])
    if departments:
        ddf = pd.DataFrame(departments)
        fig = px.bar(ddf, x="department", y="revenue", title="Revenue by department",
                     hover_data=["expenses","employee_target_attainment_pct","employees"])
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(ddf, use_container_width=True, hide_index=True)

st.divider()
left,right = st.columns(2)
with left:
    st.subheader("Revenue forecast")
    forecast = get(f"/api/revenue-forecast?horizon={horizon}", {})
    if forecast.get("history") and forecast.get("forecast"):
        hist = pd.DataFrame(forecast["history"])
        fut = pd.DataFrame(forecast["forecast"])
        hist["series"] = "Actual"
        fut["series"] = "Forecast"
        chart = pd.concat([hist.rename(columns={"date":"day"}), fut.rename(columns={"date":"day"})])
        fig = px.line(chart, x="day", y="revenue", color="series", title="Daily revenue and baseline forecast")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(forecast.get("note",""))
    else:
        st.info(forecast.get("note","Forecast unavailable"))
with right:
    st.subheader("Workflow bottlenecks")
    bottlenecks = get("/api/bottlenecks", [])
    if bottlenecks:
        bdf = pd.DataFrame(bottlenecks)
        fig = px.bar(bdf, x="stage", y="avg_duration_hours", color="is_bottleneck",
                     title="Average time by workflow stage",
                     labels={"avg_duration_hours":"Average hours","is_bottleneck":"Bottleneck"})
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(bdf, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Expense anomaly review")
anomalies = get("/api/expense-anomalies", [])
if anomalies:
    adf = pd.DataFrame(anomalies)
    st.warning(f"{len(adf)} expense records were flagged for review. A statistical anomaly is not proof of fraud.")
    st.dataframe(adf, use_container_width=True, hide_index=True)
else:
    st.success("No expense anomalies flagged.")

st.divider()
st.subheader("AI management report")
question = st.text_input("What should the management report focus on?",
                         "What are the biggest operational risks and the top three actions for next month?")
if st.button("Generate management report", type="primary"):
    with st.spinner("Analyzing SQL metrics, anomalies and workflow bottlenecks..."):
        try:
            res = requests.post(f"{API}/api/management-report",
                                json={"question":question}, timeout=90)
            res.raise_for_status()
            report = res.json()["report"]
            st.markdown(report)
            st.download_button("Download report (.md)", report, file_name="management_report.md")
        except requests.RequestException as exc:
            st.error(f"Report generation failed: {exc}")

st.caption("Built with Streamlit • FastAPI • SQLAlchemy • SQLite • scikit-learn • Plotly • optional Groq")
