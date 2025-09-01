import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# Load Data
# ===============================
st.set_page_config(page_title="Utilities Dashboard", layout="wide")

df = pd.read_csv("utilities_3compressors_final.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sidebar
st.sidebar.title("⚡ Navigation")
page = st.sidebar.radio("Go to", ["Overview", "COP Trends", "Anomalies", "Correlation"])

# ===============================
# KPI Cards
# ===============================
if page == "Overview":
    st.title("⚡ Utilities Monitoring Dashboard")
    st.markdown("Real-time COP monitoring, anomalies, and KPIs")

    latest_cop = df["COP"].iloc[-1]
    latest_pred = df["COP_Pred"].iloc[-1]
    anomalies_count = (df["Anomaly"] == -1).sum()
    avg_cop = df["COP"].mean()

    # KPI Cards (3 columns)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("📌 Latest COP", f"{latest_cop:.2f}")
    kpi2.metric("📊 Predicted COP", f"{latest_pred:.2f}")
    kpi3.metric("⚠️ Total Anomalies", anomalies_count)
    kpi4.metric("📈 Avg COP", f"{avg_cop:.2f}")

# ===============================
# COP Trends
# ===============================
if page == "COP Trends":
    st.header("📉 COP Trends with Anomaly Detection")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["COP"], 
                             mode="lines", name="COP", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df[df["Anomaly"]==-1]["Timestamp"], 
                             y=df[df["Anomaly"]==-1]["COP"], 
                             mode="markers", name="Anomaly", marker=dict(color="red", size=10, symbol="x")))
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# Anomaly Summary
# ===============================
if page == "Anomalies":
    st.header("⚠️ Anomaly Summary")
    anomaly_daily = df[df["Anomaly"]==-1].groupby(df["Timestamp"].dt.date).size()

    fig = px.bar(x=anomaly_daily.index, y=anomaly_daily.values, labels={"x":"Date", "y":"Anomalies"})
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# Correlation
# ===============================
if page == "Correlation":
    st.header("📊 Correlation Heatmap")
    corr = df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
    st.plotly_chart(fig, use_container_width=True)
