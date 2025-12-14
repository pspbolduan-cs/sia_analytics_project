# ============================================================
# Author: Charles
# Description: Flight Performance Analytics module
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# -------------------------------
# LOAD DATASET
# -------------------------------
df = pd.read_csv("assets/train.csv")

# -------------------------------
# PAGE TITLE
# -------------------------------
st.title("✈️ Flight Performance Analytics")

# =========================
# KEY PERFORMANCE INDICATORS
# =========================
st.subheader("📊 Key Performance Indicators")

total_flights = len(df)
avg_distance = df["Flight Distance"].mean()
avg_departure_delay = df["Departure Delay in Minutes"].mean()
avg_arrival_delay = df["Arrival Delay in Minutes"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("✈️ Total Flights", total_flights)
col2.metric("📏 Avg Flight Distance", f"{avg_distance:.1f} km")
col3.metric("⏱ Avg Departure Delay", f"{avg_departure_delay:.1f} min")
col4.metric("🛬 Avg Arrival Delay", f"{avg_arrival_delay:.1f} min")

# =========================
# FLIGHT DISTANCE DISTRIBUTION
# =========================
st.subheader("📈 Flight Distance Distribution")

fig1, ax1 = plt.subplots()
ax1.hist(df["Flight Distance"], bins=30)
ax1.set_xlabel("Flight Distance")
ax1.set_ylabel("Number of Flights")

st.pyplot(fig1)

# =========================
# DELAY ANALYSIS
# =========================
st.subheader("⏱ Delay Analysis")

fig2, ax2 = plt.subplots()
ax2.scatter(df["Flight Distance"], df["Arrival Delay in Minutes"], alpha=0.3)
ax2.set_xlabel("Flight Distance")
ax2.set_ylabel("Arrival Delay (Minutes)")

st.pyplot(fig2)

# =========================
# CREW PERFORMANCE
# =========================
st.subheader("👨‍✈️ Crew Performance (Service Ratings)")

crew_columns = [
    "On-board service",
    "Inflight service",
    "Checkin service"
]

crew_avg = df[crew_columns].mean()

fig3, ax3 = plt.subplots()
crew_avg.plot(kind="bar", ax=ax3)
ax3.set_ylabel("Average Rating")

st.pyplot(fig3)

# =========================
# DESCRIPTION
# =========================
st.write("""
This module analyzes operational performance metrics such as:
- Flight distance and delays  
- Arrival and departure efficiency  
- Crew service performance  
""")



