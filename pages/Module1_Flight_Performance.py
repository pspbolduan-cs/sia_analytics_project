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


def _render_html(st, html: str) -> None:
    """
    Streamlit Markdown turns lines with 4+ leading spaces into CODE.
    This strips indentation so HTML always renders properly.
    """
    cleaned = "\n".join(line.lstrip() for line in html.splitlines()).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def _inject_module_css(st) -> None:
    """Module CSS + floating back button (hover dashboard style)."""
    PRIMARY_NAVY = "#002663"
    BACKGROUND_CREAM = "#F5F3EE"
    TEXT_GREY = "#555555"

    _render_html(
        st,
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

        /* KPI cards */
        .kpiGrid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}
        @media (max-width: 1200px){{ .kpiGrid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (max-width: 700px){{ .kpiGrid {{ grid-template-columns: 1fr; }} }}

        .kpiCard{{
            background: white;
            border: 1px solid rgba(0,0,0,0.06);
            border-radius: 16px;
            padding: 14px 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }}
        .kpiTitle{{ color: rgba(0,0,0,0.55); font-size: 0.90rem; font-weight: 700; }}
        .kpiValue{{
            color: {PRIMARY_NAVY};
            font-size: 2.0rem; font-weight: 900; line-height: 1.1; margin-top: 6px;
        }}
        .kpiBadge{{
            display:inline-block; margin-top: 8px;
            padding: 4px 10px; border-radius: 999px;
            background: rgba(255,237,77,0.35);
            color: {PRIMARY_NAVY};
            font-weight: 800; font-size: 0.78rem;
        }}
        </style>
        """,
    )


def _render_back_hover_only(st) -> None:
    """Render ONLY the floating back-to-dashboard link."""
    _render_html(
        st,
        """
        <div class="sia-back-float">
            🏠 <a href="./" target="_self">Back to Dashboard</a>
        </div>
        """,
    )


def _kpi_cards(st, items: list[tuple[str, str, str]]) -> None:
    """Render KPI cards (HTML)."""
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

    _render_html(st, f'<div class="kpiGrid">{"".join(cards)}</div>')


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

    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    if dist_col is None:
        return None

    # Simulate fuel consumption (academic estimation)
    BASE_FUEL_RATE = 0.05  # kg per km
    rng = np.random.default_rng(42)
    distance = pd.to_numeric(df[dist_col], errors="coerce")

    df["Estimated Fuel Consumption (kg)"] = distance * BASE_FUEL_RATE * rng.uniform(0.9, 1.1, size=len(df))
    return df


# ============================================================
# STREAMLIT UI VERSION
# ============================================================
def run_flight_performance_ui():
    import streamlit as st

    st.set_page_config(page_title="Flight Performance Analytics", page_icon="✈️", layout="wide")

    _safe_apply_global_styles()
    _inject_module_css(st)
    _render_back_hover_only(st)

    st.title("✈️ Flight Performance Analytics")
    _render_html(
        st,
        """
        <div class="sia-subtext">
        Operational flight performance analytics: distance patterns, delay trends,
        crew service indicators, and <b>estimated fuel consumption</b> (simulated for academic use).
        </div>
        """,
    )

    # -------------------------------
    # LOAD & PREPARE DATA
    # -------------------------------
    df = prepare_flight_data()
    if df is None:
        st.error("❌ Unable to load dataset or required columns (e.g., Flight Distance) are missing.")
        st.stop()

    # ✅ Total flights should be total rows from dataset
    total_flights_all = int(len(df))

    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    dep_delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay", "departure_delay", "dep_delay"])
    arr_delay_col = _first_existing_col(df, ["Arrival Delay in Minutes", "ArrivalDelay", "ArrDelay", "arrival_delay", "arr_delay"])

    # -------------------------------
    # FILTERS
    # -------------------------------
    _render_html(st, '<div class="section-title">🎛️ Filters</div>')

    dist_series = pd.to_numeric(df[dist_col], errors="coerce").dropna()
    if dist_series.empty:
        st.error("Distance column exists but contains no numeric values.")
        st.stop()

    dmin = float(dist_series.min())
    dmax = float(dist_series.max())

    c1, c2, c3 = st.columns(3)
    with c1:
        dist_range = st.slider("Flight distance range (km)", dmin, dmax, (dmin, dmax))
    with c2:
        sample_n = st.slider(
            "Sample size for scatter plots",
            1000,
            min(50000, total_flights_all),
            min(8000, total_flights_all),
            step=1000,
        )
    with c3:
        bins = st.slider("Histogram bins", 10, 60, 30, step=5)

    # Filter by distance (only affects filtered KPIs / charts)
    df_f = df.copy()
    df_f["_dist_num"] = pd.to_numeric(df_f[dist_col], errors="coerce")
    df_f = df_f[df_f["_dist_num"].between(dist_range[0], dist_range[1], inclusive="both")].dropna(subset=["_dist_num"])
    total_flights_filtered = int(len(df_f))

    if df_f.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    # -------------------------------
    # KPI SECTION (FIXED RENDERING)
    # -------------------------------
    avg_distance = float(df_f["_dist_num"].mean())

    fuel_s = pd.to_numeric(df_f["Estimated Fuel Consumption (kg)"], errors="coerce")
    avg_fuel = float(fuel_s.mean()) if fuel_s.notna().any() else 0.0

    kpis = [
        ("Total Flights", f"{total_flights_all:,}", "Entire dataset"),
        ("Flights in Filter", f"{total_flights_filtered:,}", "After distance filter"),
        ("Avg Distance (km)", f"{avg_distance:.1f}", "Filtered subset"),
        ("Avg Fuel (kg)", f"{avg_fuel:.1f}", "Simulated"),
    ]
    _kpi_cards(st, kpis)

    st.divider()

    # -------------------------------
    # FLIGHT DISTANCE DISTRIBUTION
    # -------------------------------
    _render_html(st, '<div class="section-title">📈 Flight Distance Distribution</div>')
    _render_html(st, '<div class="hint">Histogram of flight distance for the selected range.</div>')

    fig1, ax1 = plt.subplots()
    ax1.hist(df_f["_dist_num"], bins=bins)
    ax1.set_xlabel("Flight Distance (km)")
    ax1.set_ylabel("Number of Flights")
    st.pyplot(fig1, clear_figure=True)

    st.divider()

    # -------------------------------
    # DELAY ANALYSIS
    # -------------------------------
    _render_html(st, '<div class="section-title">⏱ Arrival Delay vs Flight Distance</div>')
    _render_html(st, '<div class="hint">Scatter plot (sampled for performance).</div>')

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
    _render_html(st, '<div class="section-title">⛽ Estimated Fuel vs Flight Distance</div>')
    _render_html(st, '<div class="hint">Fuel is simulated from distance (academic estimation).</div>')

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
    _render_html(st, '<div class="section-title">👨‍✈️ Crew Service Performance</div>')
    _render_html(st, '<div class="hint">Average rating (1–5) across available service columns.</div>')

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
    """Command-line interface for Flight Performance Analytics (summary only)."""

    print("\n=======================================")
    print("  FLIGHT PERFORMANCE ANALYTICS (CLI)   ")
    print("=======================================\n")

    df = prepare_flight_data()
    if df is None:
        print("❌ ERROR: Unable to load dataset or required columns missing (e.g., Flight Distance).")
        input("Press ENTER to return...")
        return

    total_flights_all = int(len(df))

    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    dep_delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay"])
    arr_delay_col = _first_existing_col(df, ["Arrival Delay in Minutes", "ArrivalDelay", "ArrDelay"])

    dist = pd.to_numeric(df[dist_col], errors="coerce")
    fuel = pd.to_numeric(df["Estimated Fuel Consumption (kg)"], errors="coerce")

    print(f"✈️ Total Flights        : {total_flights_all:,}")
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
            print(f" - {col}: {float(s.mean()):.2f}" if s.notna().any() else f" - {col}: N/A")

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
