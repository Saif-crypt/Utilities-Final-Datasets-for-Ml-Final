import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

# ===============================
# Page Config & CSS Styling
# ===============================
st.set_page_config(page_title="Utilities Dashboard", layout="wide")

st.markdown("""
    <style>
        /* Sidebar Background Gradient with rounded corners */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #2e3959 0%, #304e7c 100%);
            color: #f9c74f;
            padding: 30px 10px 20px 10px;
            border-radius: 20px 0 0 20px;
            min-height: 100vh;
        }
        /* Sidebar menu items font and spacing */
        .nav-link {
            font-size: 20px !important;
            color: #F9FAFB !important;
            margin: 6px 0;
            border-radius: 8px !important;
        }
        /* Selected item styles */
        .nav-link.active {
            background-color: #f9c74f !important;
            color: #2e3959 !important;
        }
        /* Hover effect */
        .nav-link:hover {
            background-color: #f9c74f !important;
            color: #2e3959 !important;
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
# Stylish Sidebar with option_menu
# ===============================
with st.sidebar:
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
    selected = option_menu(
        "Main Menu",
        ["🏠 Overview", "📉 COP Trends (Plotly)", "📉 COP Trends (Matplotlib)", "⚠️ Anomalies", "📊 Correlation (Plotly)", "📊 Correlation (Seaborn)", "📈 Interactive COP Trend"],
        icons=['house', 'graph-up', 'bar-chart', 'exclamation-triangle', 'graph-up-arrow', 'heatmap', 'upload'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0px"},
            "icon": {"color": "#f9c74f", "font-size": "25px"},
            "nav-link": {"font-size": "20px", "text-align": "left", "margin": "5px 0", "--hover-color": "#f9c74f"},
            "nav-link-selected": {"background-color": "#f9c74f", "color": "#2e3959"},
        }
    )

# ===============================
# Main Title and Page Indicator
# ===============================
st.markdown('<h1 class="big-font">Utilities Monitoring Dashboard</h1>', unsafe_allow_html=True)
st.write(f"You selected **{selected}** page 🚀")

# ===============================
# Pages Implementation
# ===============================
if selected == "🏠 Overview":
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

elif selected == "📉 COP Trends (Plotly)":
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["COP"], mode="lines", name="COP", line=dict(color="#4cc9f0", width=3)))
    fig.add_trace(go.Scatter(x=df[df["Anomaly"] == -1].index, y=df[df["Anomaly"] == -1]["COP"], mode="markers", name="Anomaly",
                             marker=dict(color="red", size=12, symbol="x")))
    fig.update_layout(template="plotly_dark", title="COP vs Anomalies", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

elif selected == "📉 COP Trends (Matplotlib)":
    st.subheader("🔎 COP with Anomaly Detection (Matplotlib)")
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(df.index, df["COP"], label="COP", color="blue")
    ax1.scatter(df.index[df["Anomaly"] == -1], df["COP"][df["Anomaly"] == -1], color="red", label="Anomaly", marker="x")
    ax1.legend()
    ax1.set_title("COP vs Anomalies")
    st.pyplot(fig1)

if selected == "⚠️ Anomalies":
    anomaly_daily = df[df["Anomaly"] == -1].groupby(pd.Grouper(freq='D')).size()
    fig = px.bar(x=anomaly_daily.index, y=anomaly_daily.values,
                 labels={"x": "Date", "y": "Anomalies"},
                 color=anomaly_daily.values,
                 color_continuous_scale="oranges")
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

elif selected == "📊 Correlation (Plotly)":
    corr = df.corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
    fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

elif selected == "📊 Correlation (Seaborn)":
    st.subheader("📊 Correlation Heatmap (Seaborn)")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(df.corr(), cmap="coolwarm", annot=False, ax=ax3)
    st.pyplot(fig3)

elif selected == "📈 Interactive COP Trend":
    st.subheader("📊 Interactive COP Trend (Plotly)")
    fig4 = px.line(df.reset_index(), x="Timestamp", y=["COP", "COP_Pred"],
                   labels={"value": "COP", "Timestamp": "Time"},
                   title="Interactive COP vs Predicted COP")
    st.plotly_chart(fig4, use_container_width=True)
