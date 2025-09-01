import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# Page Config
# ===============================
st.set_page_config(page_title="Utilities Dashboard", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
        /* Background & Fonts */
        body {
            background-color: #0e1117;
            color: #fafafa;
        }
        .big-font {
            font-size:30px !important;
            font-weight: bold;
            color: #f9c74f;
        }
        .metric-card {
            background-color: #1f2630;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.4);
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# Load Data
# ===============================
df = pd.read_csv("utilities_3compressors_final.csv")
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sidebar
st.sidebar.title("⚡ Navigation")
page = st.sidebar.radio("Go to", ["Overview", "COP Trends", "Anomalies", "Correlation"])

# ===============================
# KPI Cards (Overview Page)
# ===============================
if page == "Overview":
    st.markdown("<p class='big-font'>⚡ Utilities Monitoring Dashboard</p>", unsafe_allow_html=True)
    st.write("Real-time COP monitoring, anomaly detection, and KPIs")

    latest_cop = df["COP"].iloc[-1]
    latest_pred = df["COP_Pred"].iloc[-1]
    anomalies_count = (df["Anomaly"] == -1).sum()
    avg_cop = df["COP"].mean()

    # KPI Cards Layout
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(f"<div class='metric-card'>📌<br>Latest COP<br><h2>{latest_cop:.2f}</h2></div>", unsafe_allow_html=True)

    with kpi2:
        st.markdown(f"<div class='metric-card'>📊<br>Predicted COP<br><h2>{latest_pred:.2f}</h2></div>", unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"<div class='metric-card'>⚠️<br>Total Anomalies<br><h2>{anomalies_count}</h2></div>", unsafe_allow_html=True)

    with kpi4:
        st.markdown(f"<div class='metric-card'>📈<br>Avg COP<br><h2>{avg_cop:.2f}</h2></div>", unsafe_allow_html=True)

# ===============================
# COP Trends Page
# ===============================
if page == "COP Trends":
    st.markdown("<p class='big-font'>📉 COP Trends with Anomaly Detection</p>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["COP"], 
                             mode="lines", name="COP", line=dict(color="#4cc9f0", width=3)))
    fig.add_trace(go.Scatter(x=df[df["Anomaly"]==-1]["Timestamp"], 
                             y=df[df["Anomaly"]==-1]["COP"], 
                             mode="markers", name="Anomaly", 
                             marker=dict(color="red", size=12, symbol="x")))

    fig.update_layout(template="plotly_dark", title="COP vs Anomalies")
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# Anomaly Summary
# ===============================
if page == "Anomalies":
    st.markdown("<p class='big-font'>⚠️ Anomaly Summary</p>", unsafe_allow_html=True)

    anomaly_daily = df[df["Anomaly"]==-1].groupby(df["Timestamp"].dt.date).size()

    fig = px.bar(x=anomaly_daily.index, y=anomaly_daily.values,
                 labels={"x":"Date", "y":"Anomalies"},
                 color=anomaly_daily.values,
                 color_continuous_scale="oranges")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# ===============================
# Correlation Heatmap
# ===============================
if page == "Correlation":
    st.markdown("<p class='big-font'>📊 Correlation Heatmap</p>", unsafe_allow_html=True)

    corr = df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
