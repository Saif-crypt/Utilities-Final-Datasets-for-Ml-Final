import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# ===============================
# Page Config & CSS Styling
# ===============================
st.set_page_config(page_title="Utilities Dashboard", layout="wide")

st.markdown("""
    <style>
        /* Sidebar Background */
        [data-testid="stSidebar"] {
            background-color: #1f2630;
            padding: 20px 10px;
        }
        /* Sidebar Title */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #f9c74f !important;
            font-weight: bold;
            text-align: center;
        }
        /* Sidebar Links */
        section[data-testid="stSidebar"] a {
            font-size: 18px;
            font-weight: 500;
            color: #ffffff !important;
            padding: 8px 15px;
            border-radius: 8px;
            display: block;
            margin-bottom: 8px;
            background-color: #2a2f3a;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        section[data-testid="stSidebar"] a:hover {
            background-color: #f9c74f !important;
            color: #1f2630 !important;
            font-weight: bold;
            cursor: pointer;
        }
        /* Main header */
        .big-font {
            font-size: 32px !important;
            color: #f9c74f;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        /* Metric cards */
        .metric-card {
            background-color: #2a2f3a;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            color: white;
            font-size: 18px;
            margin-bottom: 15px;
        }
        .metric-card h2 {
            margin: 10px 0 0 0;
            color: #f9c74f;
        }
    </style>
""", unsafe_allow_html=True)

# ===============================
# Load and cache data
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("utilities_final.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.set_index("Timestamp")
    return df

df = load_data()

# ===============================
# Sidebar with Navigation
# ===============================
st.sidebar.markdown("## ⚡ Utilities Dashboard")
st.sidebar.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=120)
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Overview", "📉 COP Trends (Plotly)", "📉 COP Trends (Matplotlib)", "⚠️ Anomalies", "📊 Correlation (Plotly)", "📊 Correlation (Seaborn)", "📈 Interactive COP Trend"]
)

# ===============================
# Main Title and Page Indicator
# ===============================
st.markdown('<h1 class="big-font">Utilities Monitoring Dashboard</h1>', unsafe_allow_html=True)
st.write(f"You selected **{page}** page 🚀")

# ===============================
# Pages Implementation
# ===============================
if page == "🏠 Overview":
    latest_cop = df["COP"].iloc[-1]
    latest_pred = df["COP_Pred"].iloc[-1]
    anomalies_count = (df["Anomaly"] == -1).sum()
    avg_cop = df["COP"].mean()
    # KPI cards with CSS styling (from Code1)
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.markdown(f'<div class="metric-card">📌<br>Latest COP<br><h2>{latest_cop:.2f}</h2></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="metric-card">📊<br>Predicted COP<br><h2>{latest_pred:.2f}</h2></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-card">⚠️<br>Total Anomalies<br><h2>{anomalies_count}</h2></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="metric-card">📈<br>Avg COP<br><h2>{avg_cop:.2f}</h2></div>', unsafe_allow_html=True)
    # Additional KPIs in simpler metric format (Code2 style)
    st.subheader("📌 Key Performance Indicators (KPIs)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Latest COP", round(latest_cop, 2))
    col2.metric("Latest Predicted COP", round(latest_pred, 2))
    col3.metric("Total Anomalies Detected", anomalies_count)

elif page == "📉 COP Trends (Plotly)":
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["COP"], mode="lines", name="COP", line=dict(color="#4cc9f0", width=3)))
    fig.add_trace(go.Scatter(x=df[df["Anomaly"] == -1].index, y=df[df["Anomaly"] == -1]["COP"], mode="markers", name="Anomaly",
                             marker=dict(color="red", size=12, symbol="x")))
    fig.update_layout(template="plotly_dark", title="COP vs Anomalies", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

elif page == "📉 COP Trends (Matplotlib)":
    st.subheader("🔎 COP with Anomaly Detection (Matplotlib)")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df.index, df["COP"], label="COP", color="blue")
    ax1.scatter(df.index[df["Anomaly"] == -1], df["COP"][df["Anomaly"] == -1], color="red", label="Anomaly", marker="x")
    ax1.legend()
    ax1.set_title("COP vs Anomalies")
    st.pyplot(fig1)

elif page == "⚠️ Anomalies":
    anomaly_daily = df[df["Anomaly"] == -1].groupby(df.index.date).size()
    fig = px.bar(x=anomaly_daily.index, y=anomaly_daily.values,
                 labels={"x": "Date", "y": "Anomalies"},
                 color=anomaly_daily.values,
                 color_continuous_scale="oranges")
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Correlation (Plotly)":
    corr = df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

elif page == "📊 Correlation (Seaborn)":
    st.subheader("📊 Correlation Heatmap (Seaborn)")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.corr(), cmap="coolwarm", annot=False, ax=ax3)
    st.pyplot(fig3)

elif page == "📈 Interactive COP Trend":
    st.subheader("📊 Interactive COP Trend (Plotly)")
    fig4 = px.line(df.reset_index(), x="Timestamp", y=["COP", "COP_Pred"],
                   labels={"value": "COP", "Timestamp": "Time"},
                   title="Interactive COP vs Predicted COP")
    st.plotly_chart(fig4, use_container_width=True)
