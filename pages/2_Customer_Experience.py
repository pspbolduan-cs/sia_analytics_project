# ============================================================
# Author: Ruitao He
# Last Updated: 2025-12-08
# Description:
# Customer Experience Analytics Dashboard 
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# ============================================================
# GLOBAL PLOT SETTINGS (Smaller Size + High DPI)
# ============================================================
mpl.rcParams['figure.figsize'] = (6, 3)   # Compact charts
mpl.rcParams['figure.dpi'] = 150          # High clarity
sns.set(style="whitegrid")

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Experience Analytics",
    page_icon="😊",
    layout="wide"
)

# ============================================================
# TITLE & INTRODUCTION
# ============================================================
st.title("😊 Customer Experience Analytics Dashboard")

st.markdown("""
This dashboard provides insights into **passenger experience and satisfaction**, covering:

- ⭐ Satisfaction distribution  
- 🧭 Flight distance influence  
- 🛫 Inflight service components  
- 🔥 Numerical feature correlations  
""")

st.divider()

# ============================================================
# LOAD DATASET
# ============================================================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("assets/train.csv")
    except:
        st.error("❌ ERROR: train.csv missing in /assets/")
        return None

df = load_data()
if df is None:
    st.stop()

# Drop unnamed placeholder columns
df = df.loc[:, ~df.columns.str.contains("unnamed", case=False)]

# ============================================================
# SATISFACTION → NUMERIC SCORE
# ============================================================
df["satisfaction"] = df["satisfaction"].astype(str).str.lower()

satisfaction_map = {
    "very dissatisfied": 1,
    "dissatisfied": 2,
    "neutral or dissatisfied": 3,
    "neutral": 3,
    "neutral or satisfied": 4,
    "satisfied": 4,
    "very satisfied": 5
}

df["satisfaction_score"] = df["satisfaction"].map(satisfaction_map)
df["satisfaction_score"].fillna(3, inplace=True)

# ============================================================
# KPI SUMMARY
# ============================================================
st.subheader("📌 Key Customer Experience Metrics")

col1, col2 = st.columns(2)

col1.metric("⭐ Average Satisfaction Score", f"{df['satisfaction_score'].mean():.2f}")
col2.metric("🧑‍🤝‍🧑 Total Passengers", f"{len(df)}")

st.divider()

# ============================================================
# SATISFACTION DISTRIBUTION (BAR CHART)
# ============================================================
st.subheader("📊 Satisfaction Score Distribution")

score_counts = df["satisfaction_score"].value_counts().sort_index()

fig, ax = plt.subplots()

# Bar chart
ax.bar(score_counts.index, score_counts.values, color="#4A90E2")

# Remove double horizontal gridlines entirely
ax.grid(False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_linewidth(0.6)
ax.spines["bottom"].set_linewidth(0.6)

ax.set_title("Satisfaction Score Distribution", fontsize=14)
ax.set_xlabel("Satisfaction Score (1–5)")
ax.set_ylabel("Passenger Count")

st.pyplot(fig, clear_figure=True)

st.divider()

# ============================================================
# FLIGHT DISTANCE EFFECT
# ============================================================
st.subheader("🧭 Impact of Flight Distance on Satisfaction")

min_d = int(df["Flight Distance"].min())
max_d = int(df["Flight Distance"].max())

distance_threshold = st.slider(
    "Select minimum flight distance (km):",
    min_d,
    max_d,
    value=min_d + (max_d - min_d) // 3,
    step=100
)

filtered = df[df["Flight Distance"] >= distance_threshold]
st.write(f"Displaying **{len(filtered)} passengers** with distance ≥ **{distance_threshold} km**")

fd_counts = filtered["satisfaction_score"].value_counts().sort_index()

fig2, ax2 = plt.subplots()

ax2.bar(fd_counts.index, fd_counts.values, color="#4A90E2")

# Remove gridlines & ensure single clean axes
ax2.grid(False)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_linewidth(0.6)
ax2.spines["bottom"].set_linewidth(0.6)

ax2.set_title(f"Satisfaction (Distance ≥ {distance_threshold} km)", fontsize=14)
ax2.set_xlabel("Satisfaction Score")
ax2.set_ylabel("Passenger Count")

st.pyplot(fig2, clear_figure=True)

st.divider()

# ============================================================
# CORRELATION HEATMAP (COMPACT + CLEAN)
# ============================================================
st.subheader("🔥 Numerical Feature Correlation Heatmap")

num_df = df.select_dtypes(include=["int64", "float64"])

if not num_df.empty:

    fig3, ax3 = plt.subplots(figsize=(10, 6), dpi=150)

    sns.heatmap(
        num_df.corr(),
        cmap="coolwarm",
        ax=ax3,
        linewidths=0.3,
        linecolor="gray",
        cbar_kws={"shrink": 0.7}
    )

    ax3.set_title("Numeric Feature Correlations", fontsize=16, fontweight="bold")
    plt.xticks(rotation=45, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=9)

    st.pyplot(fig3, clear_figure=True)

else:
    st.warning("⚠️ No numerical features available for correlation heatmap.")

st.divider()

# ============================================================
# RETURN TO MAIN PAGE
# ============================================================
st.page_link("main.py", label="⬅️ Return to Main Dashboard", icon="🏠")
