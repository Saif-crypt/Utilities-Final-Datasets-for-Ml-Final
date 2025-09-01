import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ============================================
# 📌 Load Data
# ============================================
st.set_page_config(page_title="Utilities Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("utilities_final.csv")
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df = df.set_index("Timestamp")
    return df

df = load_data()
st.sidebar.success("✅ Data Loaded: {} rows".format(df.shape[0]))

# ============================================
# 📊 Dashboard Title
# ============================================
st.title("⚡ Utilities Monitoring Dashboard")
st.markdown("Real-time **COP monitoring, anomaly detection, and KPIs**")

# ============================================
# 📊 1. COP with Anomaly Detection
# ============================================
st.subheader("🔎 COP with Anomaly Detection")

fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(df.index, df["COP"], label="COP", color="blue")
ax1.scatter(df.index[df["Anomaly"] == -1],
            df["COP"][df["Anomaly"] == -1],
            color="red", label="Anomaly", marker="x")
ax1.legend()
ax1.set_title("COP vs Anomalies")
st.pyplot(fig1)

# ============================================
# 📊 2. Actual vs Predicted COP
# ============================================
st.subheader("📈 Actual vs Predicted COP")

fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(df.index, df["COP"], label="Actual COP", color="blue")
ax2.plot(df.index, df["COP_Pred"], label="Predicted COP", color="orange")
ax2.legend()
ax2.set_title("Actual vs Predicted COP")
st.pyplot(fig2)

# ============================================
# 📊 3. Correlation Heatmap
# ============================================
st.subheader("📊 Correlation Heatmap")

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(df.corr(), cmap="coolwarm", annot=False, ax=ax3)
st.pyplot(fig3)

# ============================================
# 📌 4. KPI Section
# ============================================
st.subheader("📌 Key Performance Indicators (KPIs)")

latest_cop = df["COP"].iloc[-1]
latest_pred = df["COP_Pred"].iloc[-1]
anomalies_count = (df["Anomaly"] == -1).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Latest COP", round(latest_cop, 2))
col2.metric("Latest Predicted COP", round(latest_pred, 2))
col3.metric("Total Anomalies Detected", anomalies_count)

# ============================================
# 📊 5. Interactive Plot with Plotly
# ============================================
st.subheader("📊 Interactive COP Trend (Plotly)")

fig4 = px.line(df.reset_index(), x="Timestamp", y=["COP", "COP_Pred"],
               labels={"value": "COP", "Timestamp": "Time"},
               title="Interactive COP vs Predicted COP")
st.plotly_chart(fig4, use_container_width=True)
