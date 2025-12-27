# ============================================================
# Author: Charles (updated by Philippe Bolduan)
# Date: 2025-12
# Module 1 – Flight Performance Analytics
# Course: CN6001 Enterprise Application & Cloud Computing
#
# Description:
# This module provides:
# - Streamlit UI for visual analytics
# - CLI mode for summary-based analytics
#
# Fuel consumption is synthetically estimated based on
# flight distance due to the absence of real fuel data.
# ============================================================

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from services.data_service import load_data


# ============================================================
# Helpers / Shared UI
# ============================================================
def _safe_apply_global_styles() -> bool:
    """Apply shared theme if available (safe for CLI too)."""
    try:
        from services.ui_service import apply_global_styles

        apply_global_styles()
        return True
    except Exception:
        return False


def _inject_module_css() -> None:
    """Module CSS + floating back button (hover dashboard style)."""
    import streamlit as st

    PRIMARY_NAVY = "#002663"
    BACKGROUND_CREAM = "#F5F3EE"
    TEXT_GREY = "#555555"
    CARD_BG = "#FFFFFF"
    CARD_BORDER = "#E5E7EB"

    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {BACKGROUND_CREAM}; }}
        h1, h2, h3 {{ color: {PRIMARY_NAVY}; }}

        .sia-subtext {{
            color: {TEXT_GREY};
            font-size: 1rem;
            margin-top: -6px;
        }}

        .section-title {{
            margin-top: 14px;
            margin-bottom: 2px;
            font-size: 1.25rem;
            font-weight: 800;
            color: {PRIMARY_NAVY};
        }}
        .hint {{
            color: {TEXT_GREY};
            font-size: 0.92rem;
        }}

        /* Floating back button ONLY (matches other modules) */
        .sia-back-float {{
            position: fixed;
            top: 90px;
            right: 18px;
            z-index: 999999;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255,255,255,0.94);
            border: 1px solid rgba(0,0,0,0.10);
            box-shadow: 0 10px 28px rgba(0,0,0,0.14);
            backdrop-filter: blur(6px);
        }}
        .sia-back-float a {{
            text-decoration: none;
            font-weight: 800;
            color: {PRIMARY_NAVY};
            font-size: 0.98rem;
        }}
        .sia-back-float a:hover {{
            text-decoration: underline;
        }}

        /* Make matplotlib plots breathe a bit */
        .stPlotlyChart, .stPyplot {{
            background: transparent !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_back_hover_only() -> None:
    """Render ONLY the floating back-to-dashboard link."""
    import streamlit as st

    st.markdown(
        """
        <div class="sia-back-float">
            🏠 <a href="./" target="_self">Back to Dashboard</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _first_existing_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return first existing column name (case-safe)."""
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        cl = cand.lower()
        if cl in cols_lower:
            return cols_lower[cl]
    return None


def _kpi_cards(st, items: list[tuple[str, str, str]]) -> None:
    """
    Lightweight KPI cards (works even if ui_service.render_kpi_cards is missing).
    items: [(title, value, badge), ...]
    """
    PRIMARY_NAVY = "#002663"
    TEXT_GREY = "#555555"

    st.markdown(
        """
        <style>
        .kpiGrid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
        @media (max-width: 1200px){ .kpiGrid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 700px){ .kpiGrid { grid-template-columns: 1fr; } }
        .kpiCard{
            background: white;
            border: 1px solid rgba(0,0,0,0.06);
            border-radius: 16px;
            padding: 14px 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }
        .kpiTitle{ color: rgba(0,0,0,0.55); font-size: 0.90rem; font-weight: 700; }
        .kpiValue{ color: """
        + PRIMARY_NAVY
        + """;
            font-size: 2.0rem; font-weight: 900; line-height: 1.1; margin-top: 6px;
        }
        .kpiBadge{
            display:inline-block; margin-top: 8px;
            padding: 4px 10px; border-radius: 999px;
            background: rgba(255,237,77,0.35);
            color: """
        + PRIMARY_NAVY
        + """;
            font-weight: 800; font-size: 0.78rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    cards = []
    for title, value, badge in items:
        badge_html = f'<div class="kpiBadge">{badge}</div>' if badge else ""
        cards.append(
            f"""
            <div class="kpiCard">
                <div class="kpiTitle">{title}</div>
                <div class="kpiValue">{value}</div>
                {badge_html}
            </div>
            """
        )

    st.markdown(f'<div class="kpiGrid">{"".join(cards)}</div>', unsafe_allow_html=True)


# ============================================================
# SHARED LOGIC — DATA PREPARATION
# ============================================================
def prepare_flight_data() -> pd.DataFrame | None:
    """
    Load dataset and simulate fuel consumption.
    Shared by both UI and CLI to ensure consistency.
    """
    df = load_data()
    if df is None or df.empty:
        return None

    # Find the distance column robustly
    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    if dist_col is None:
        return None

    # Simulate fuel consumption (academic estimation)
    BASE_FUEL_RATE = 0.05  # kg per km
    rng = np.random.default_rng(42)
    distance = pd.to_numeric(df[dist_col], errors="coerce")

    df["Estimated Fuel Consumption (kg)"] = (
        distance * BASE_FUEL_RATE * rng.uniform(0.9, 1.1, size=len(df))
    )

    return df


# ============================================================
# STREAMLIT UI VERSION
# ============================================================
def run_flight_performance_ui():
    import streamlit as st

    st.set_page_config(page_title="Flight Performance Analytics", page_icon="✈️", layout="wide")

    _safe_apply_global_styles()
    _inject_module_css()
    _render_back_hover_only()

    st.title("✈️ Flight Performance Analytics")
    st.markdown(
        """
        <div class="sia-subtext">
        This module analyses operational flight performance: distance patterns, delay trends,
        crew service indicators, and <b>estimated fuel consumption</b> (simulated for academic use).
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # -------------------------------
    # LOAD & PREPARE DATA
    # -------------------------------
    df = prepare_flight_data()
    if df is None:
        st.error("❌ Unable to load dataset or required columns (e.g., Flight Distance) are missing.")
        st.stop()

    # Robust columns
    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    dep_delay_col = _first_existing_col(
        df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay", "departure_delay", "dep_delay"]
    )
    arr_delay_col = _first_existing_col(
        df, ["Arrival Delay in Minutes", "ArrivalDelay", "ArrDelay", "arrival_delay", "arr_delay"]
    )

    # -------------------------------
    # FILTERS
    # -------------------------------
    st.markdown('<div class="section-title">🎛️ Filters</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    # Distance filter
    dist_series = pd.to_numeric(df[dist_col], errors="coerce").dropna()
    dmin = float(dist_series.min()) if not dist_series.empty else 0.0
    dmax = float(dist_series.max()) if not dist_series.empty else 1.0

    with c1:
        dist_range = st.slider("Flight distance range (km)", float(dmin), float(dmax), (float(dmin), float(dmax)))
    with c2:
        sample_n = st.slider("Sample size for scatter plots", 1000, min(50000, len(df)), min(8000, len(df)), step=1000)
    with c3:
        bins = st.slider("Histogram bins", 10, 60, 30, step=5)

    # Filter df by distance range
    df_f = df.copy()
    df_f["_dist_num"] = pd.to_numeric(df_f[dist_col], errors="coerce")
    df_f = df_f[df_f["_dist_num"].between(dist_range[0], dist_range[1], inclusive="both")].dropna(subset=["_dist_num"])

    if df_f.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    # -------------------------------
    # KPI SECTION
    # -------------------------------
    total_flights = int(len(df_f))
    avg_distance = float(df_f["_dist_num"].mean())

    avg_dep_delay = None
    if dep_delay_col:
        s = pd.to_numeric(df_f[dep_delay_col], errors="coerce")
        avg_dep_delay = float(s.mean()) if s.notna().any() else None

    avg_arr_delay = None
    if arr_delay_col:
        s = pd.to_numeric(df_f[arr_delay_col], errors="coerce")
        avg_arr_delay = float(s.mean()) if s.notna().any() else None

    fuel_s = pd.to_numeric(df_f["Estimated Fuel Consumption (kg)"], errors="coerce")
    avg_fuel = float(fuel_s.mean()) if fuel_s.notna().any() else 0.0

    kpis = [
        ("Total Flights", f"{total_flights:,}", "Filtered subset"),
        ("Avg Distance (km)", f"{avg_distance:.1f}", "Distance KPI"),
        ("Avg Fuel (kg)", f"{avg_fuel:.1f}", "Simulated"),
        ("Avg Arrival Delay (min)", f"{avg_arr_delay:.1f}" if avg_arr_delay is not None else "N/A", "Operational"),
    ]
    _kpi_cards(st, kpis)

    st.divider()

    # -------------------------------
    # FLIGHT DISTANCE DISTRIBUTION
    # -------------------------------
    st.markdown('<div class="section-title">📈 Flight Distance Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Histogram of flight distance for the selected range.</div>', unsafe_allow_html=True)

    fig1, ax1 = plt.subplots()
    ax1.hist(df_f["_dist_num"], bins=bins)
    ax1.set_xlabel("Flight Distance (km)")
    ax1.set_ylabel("Number of Flights")
    st.pyplot(fig1, clear_figure=True)

    st.divider()

    # -------------------------------
    # DELAY ANALYSIS
    # -------------------------------
    st.markdown('<div class="section-title">⏱ Delay vs Flight Distance</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Scatter plot (sampled for performance).</div>', unsafe_allow_html=True)

    sample_df = df_f.sample(n=min(sample_n, len(df_f)), random_state=42)

    if arr_delay_col:
        arr = pd.to_numeric(sample_df[arr_delay_col], errors="coerce")
        fig2, ax2 = plt.subplots()
        ax2.scatter(sample_df["_dist_num"], arr, alpha=0.25)
        ax2.set_xlabel("Flight Distance (km)")
        ax2.set_ylabel("Arrival Delay (minutes)")
        st.pyplot(fig2, clear_figure=True)
    else:
        st.info("Arrival delay column not found in dataset. Skipping delay scatter plot.")

    st.divider()

    # -------------------------------
    # FUEL CONSUMPTION ANALYSIS
    # -------------------------------
    st.markdown('<div class="section-title">⛽ Estimated Fuel vs Flight Distance</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Fuel is simulated from distance (academic estimation).</div>', unsafe_allow_html=True)

    fuel = pd.to_numeric(sample_df["Estimated Fuel Consumption (kg)"], errors="coerce")
    fig3, ax3 = plt.subplots()
    ax3.scatter(sample_df["_dist_num"], fuel, alpha=0.30)
    ax3.set_xlabel("Flight Distance (km)")
    ax3.set_ylabel("Estimated Fuel Consumption (kg)")
    st.pyplot(fig3, clear_figure=True)

    st.divider()

    # -------------------------------
    # CREW PERFORMANCE
    # -------------------------------
    st.markdown('<div class="section-title">👨‍✈️ Crew Service Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Average rating (1–5) across available service columns.</div>', unsafe_allow_html=True)

    crew_cols = ["On-board service", "Inflight service", "Checkin service"]
    available = [c for c in crew_cols if c in df_f.columns]

    if available:
        crew_avg = df_f[available].apply(pd.to_numeric, errors="coerce").mean().sort_values()

        fig4, ax4 = plt.subplots()
        crew_avg.plot(kind="barh", ax=ax4)
        ax4.set_xlabel("Average Rating (1–5)")
        st.pyplot(fig4, clear_figure=True)
    else:
        st.warning("Crew service columns not found in dataset.")


# ============================================================
# CLI VERSION
# ============================================================
def run_flight_performance_cli():
    """
    Command-line interface for Flight Performance Analytics.
    Provides summary statistics without visualizations.
    """

    print("\n=======================================")
    print("  FLIGHT PERFORMANCE ANALYTICS (CLI)   ")
    print("=======================================\n")

    df = prepare_flight_data()
    if df is None:
        print("❌ ERROR: Unable to load dataset or required columns missing (e.g., Flight Distance).")
        input("Press ENTER to return...")
        return

    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    dep_delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay"])
    arr_delay_col = _first_existing_col(df, ["Arrival Delay in Minutes", "ArrivalDelay", "ArrDelay"])

    dist = pd.to_numeric(df[dist_col], errors="coerce")
    fuel = pd.to_numeric(df["Estimated Fuel Consumption (kg)"], errors="coerce")

    print(f"✈️ Total Flights        : {len(df):,}")
    print(f"📏 Avg Distance (km)    : {float(dist.mean()):.1f}")

    if dep_delay_col:
        dep = pd.to_numeric(df[dep_delay_col], errors="coerce")
        print(f"⏱ Avg Departure Delay  : {float(dep.mean()):.1f} min")
    else:
        print("⏱ Avg Departure Delay  : N/A (column missing)")

    if arr_delay_col:
        arr = pd.to_numeric(df[arr_delay_col], errors="coerce")
        print(f"🛬 Avg Arrival Delay    : {float(arr.mean()):.1f} min")
    else:
        print("🛬 Avg Arrival Delay    : N/A (column missing)")

    print(f"⛽ Avg Fuel Consumption : {float(fuel.mean()):.1f} kg")

    crew_cols = ["On-board service", "Inflight service", "Checkin service"]
    available = [c for c in crew_cols if c in df.columns]

    if available:
        print("\n👨‍✈️ Crew Service Ratings:")
        for col in available:
            s = pd.to_numeric(df[col], errors="coerce")
            if s.notna().any():
                print(f" - {col}: {float(s.mean()):.2f}")
            else:
                print(f" - {col}: N/A")

    print("\n✔ Flight Performance CLI completed.")
    input("\nPress ENTER to return to main menu...")


# ============================================================
# AUTO-RUN STREAMLIT WHEN OPENED AS PAGE
# ============================================================
try:
    import streamlit as st

    if st.runtime.exists():
        run_flight_performance_ui()
except Exception:
    pass
