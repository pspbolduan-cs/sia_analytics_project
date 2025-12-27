# ============================================================
# Author: Ruitao He (updated by Philippe Bolduan)
# Last Updated: 2025-12
# Module 2: Customer Experience Analytics
# Course: CN6001 Enterprise Application & Cloud Computing
#
# Improvements:
# - Uses shared services.data_service.load_data (consistent with other modules)
# - Adds the floating "Back to Dashboard" hover button (same as other modules)
# - Removes seaborn dependency + palette issues (clean, consistent Matplotlib)
# - Robust column detection + safe numeric conversion
# - Cleaner layout: filters + KPIs + charts
# ============================================================

from __future__ import annotations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# Helpers
# ============================================================
def _safe_apply_global_styles() -> bool:
    """Apply shared UI theme if available (safe for CLI too)."""
    try:
        from services.ui_service import apply_global_styles

        apply_global_styles()
        return True
    except Exception:
        return False


def _load_data() -> pd.DataFrame | None:
    """
    Prefer the project's shared data_service.load_data().
    Falls back to reading assets/train.csv if needed.
    """
    try:
        from services.data_service import load_data

        df = load_data()
        if df is not None and not df.empty:
            return df
    except Exception:
        pass

    try:
        df = pd.read_csv("assets/train.csv")
        df = df.loc[:, ~df.columns.str.contains("unnamed", case=False)]
        return df
    except Exception:
        return None


def _first_existing_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first matching column name in df from candidates (case-safe)."""
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
    Strip indentation so HTML always renders.
    """
    cleaned = "\n".join(line.lstrip() for line in html.splitlines()).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def _inject_module_css(st) -> None:
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

        /* Floating back button ONLY */
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
        .kpiGrid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }}
        @media (max-width: 900px){{ .kpiGrid {{ grid-template-columns: 1fr; }} }}

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
    _render_html(
        st,
        """
        <div class="sia-back-float">
            🏠 <a href="./" target="_self">Back to Dashboard</a>
        </div>
        """,
    )


def _kpi_cards(st, items: list[tuple[str, str, str]]) -> None:
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


def _standardize_satisfaction(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a robust satisfaction_score (1–5) from whatever satisfaction labels exist.
    Falls back to neutral=3.
    """
    sat_col = _first_existing_col(df, ["satisfaction", "Satisfaction", "satisfied"])
    if sat_col is None:
        df["satisfaction_score"] = 3.0
        df["satisfaction_label"] = "neutral"
        return df

    raw = df[sat_col].astype(str).str.strip().str.lower()

    # Map common labels
    satisfaction_map = {
        "very dissatisfied": 1,
        "dissatisfied": 2,
        "neutral": 3,
        "neutral or dissatisfied": 3,
        "neutral or satisfied": 4,
        "satisfied": 4,
        "very satisfied": 5,
    }

    score = raw.map(satisfaction_map)

    # If some datasets are 0/1 or numeric-like
    numeric = pd.to_numeric(raw, errors="coerce")
    score = score.fillna(numeric)

    # Clamp / fill
    score = score.clip(lower=1, upper=5).fillna(3)

    df["satisfaction_score"] = score.astype(float)

    # Create a label too (nice for summaries)
    def label_from_score(x: float) -> str:
        if x <= 2:
            return "dissatisfied"
        if x == 3:
            return "neutral"
        return "satisfied"

    df["satisfaction_label"] = df["satisfaction_score"].apply(label_from_score)
    return df


def _safe_numeric_series(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


# ============================================================
# STREAMLIT UI
# ============================================================
def run_customer_experience_ui():
    import streamlit as st

    st.set_page_config(page_title="Customer Experience Analytics", page_icon="😊", layout="wide")

    _safe_apply_global_styles()
    _inject_module_css(st)
    _render_back_hover_only(st)

    st.title("😊 Customer Experience Analytics")
    _render_html(
        st,
        """
        <div class="sia-subtext">
        Explore passenger satisfaction, service ratings, and behavioural indicators across the customer journey.
        </div>
        """,
    )

    df = _load_data()
    if df is None or df.empty:
        st.error("❌ Unable to load dataset (expected assets/train.csv).")
        st.stop()

    df = _standardize_satisfaction(df)

    # Detect distance column (for filtering)
    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    if dist_col:
        df["_dist_num"] = _safe_numeric_series(df, dist_col)
    else:
        df["_dist_num"] = np.nan

    # ------------------------------------------------------------
    # Filters
    # ------------------------------------------------------------
    _render_html(st, '<div class="section-title">🎛️ Filters</div>')
    c1, c2, c3 = st.columns(3)

    with c1:
        # Satisfaction filter
        sat_min = st.slider("Minimum satisfaction score", 1, 5, 1, step=1)

    with c2:
        # Optional distance filter
        if dist_col and df["_dist_num"].notna().any():
            dmin = float(df["_dist_num"].min())
            dmax = float(df["_dist_num"].max())
            dist_range = st.slider("Flight distance range (km)", dmin, dmax, (dmin, dmax))
        else:
            dist_range = None
            st.info("Distance column not found — distance filter disabled.")

    with c3:
        bins = st.slider("Histogram bins", 5, 25, 10, step=1)

    df_f = df[df["satisfaction_score"] >= sat_min].copy()
    if dist_range is not None:
        df_f = df_f[df_f["_dist_num"].between(dist_range[0], dist_range[1], inclusive="both")]

    if df_f.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    # ------------------------------------------------------------
    # KPI Summary
    # ------------------------------------------------------------
    avg_score = float(df_f["satisfaction_score"].mean())
    total_passengers = int(len(df_f))
    satisfied_rate = float((df_f["satisfaction_label"] == "satisfied").mean() * 100.0)

    _kpi_cards(
        st,
        [
            ("⭐ Average Satisfaction", f"{avg_score:.2f}", "Filtered subset"),
            ("👥 Passengers Included", f"{total_passengers:,}", "After filters"),
            ("✅ Satisfied Rate", f"{satisfied_rate:.1f}%", "Score ≥ 4"),
            ("📌 Min Score Filter", f"{sat_min}", "Satisfaction threshold"),
        ],
    )

    st.divider()

    # ============================================================
    # Chart 1 — Satisfaction Distribution
    # ============================================================
    _render_html(st, '<div class="section-title">📊 Satisfaction Score Distribution</div>')
    _render_html(st, '<div class="hint">Histogram of satisfaction scores (1–5) for filtered passengers.</div>')

    fig1, ax1 = plt.subplots(figsize=(8, 4))
    ax1.hist(df_f["satisfaction_score"], bins=np.arange(0.5, 5.6, (5 / bins)))
    ax1.set_xlabel("Satisfaction Score (1–5)")
    ax1.set_ylabel("Passenger Count")
    ax1.set_title("Distribution of Satisfaction Scores")
    ax1.grid(False)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    st.pyplot(fig1, clear_figure=True)

    st.divider()

    # ============================================================
    # Chart 2 — Satisfaction vs Flight Distance (if available)
    # ============================================================
    _render_html(st, '<div class="section-title">🧭 Satisfaction vs Flight Distance</div>')
    _render_html(st, '<div class="hint">How satisfaction varies with distance (binned mean delay-style trend).</div>')

    if dist_col and df_f["_dist_num"].notna().any():
        # Bin distance and plot mean satisfaction per bin (cleaner than huge scatter)
        tmp = df_f[["_dist_num", "satisfaction_score"]].dropna()
        if tmp["_dist_num"].nunique() > 2:
            tmp["distance_bucket"] = pd.cut(tmp["_dist_num"], bins=8)
            trend = tmp.groupby("distance_bucket", observed=True)["satisfaction_score"].mean().reset_index()
            trend["distance_bucket"] = trend["distance_bucket"].astype(str)

            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.plot(trend["distance_bucket"], trend["satisfaction_score"], marker="o")
            ax2.set_xlabel("Flight Distance Bucket (km)")
            ax2.set_ylabel("Avg Satisfaction (1–5)")
            ax2.set_title("Average Satisfaction by Flight Distance")
            ax2.tick_params(axis="x", rotation=25)
            ax2.grid(False)
            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            st.pyplot(fig2, clear_figure=True)
        else:
            st.info("Not enough distance variation to build a distance trend chart.")
    else:
        st.info("Flight distance column not available. Skipping distance chart.")

    st.divider()

    # ============================================================
    # Chart 3 — Average Inflight Service Ratings
    # ============================================================
    _render_html(st, '<div class="section-title">🔥 Average Inflight Service Ratings</div>')
    _render_html(st, '<div class="hint">Average (1–5) across service attributes that exist in the dataset.</div>')

    service_cols = [
        "Inflight wifi service",
        "Departure/Arrival time convenient",
        "Ease of Online booking",
        "Gate location",
        "Food and drink",
        "Online boarding",
        "Seat comfort",
        "Inflight entertainment",
        "On-board service",
        "Leg room service",
        "Baggage handling",
        "Checkin service",
        "Inflight service",
        "Cleanliness",
    ]

    available_services = [c for c in service_cols if c in df_f.columns]
    if not available_services:
        st.warning("No service rating columns found in dataset.")
        return

    scores = df_f[available_services].apply(pd.to_numeric, errors="coerce").mean().sort_values()

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.barh(scores.index.astype(str), scores.values)
    ax3.set_xlabel("Average Rating (1–5)")
    ax3.set_ylabel("Service Category")
    ax3.set_title("Passenger Evaluation of Service Attributes")
    ax3.grid(False)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    st.pyplot(fig3, clear_figure=True)


# ============================================================
# CLI Version
# ============================================================
def run_customer_experience_cli():
    print("\n=======================================")
    print("  CUSTOMER EXPERIENCE ANALYTICS (CLI)  ")
    print("=======================================\n")

    df = _load_data()
    if df is None or df.empty:
        print("❌ ERROR: Dataset not found.")
        input("Press ENTER to return...")
        return

    df = _standardize_satisfaction(df)

    avg_score = float(df["satisfaction_score"].mean())
    satisfied_rate = float((df["satisfaction_label"] == "satisfied").mean() * 100.0)

    print(f"⭐ Average Satisfaction Score: {avg_score:.2f}")
    print(f"✅ Satisfied Rate (score ≥ 4): {satisfied_rate:.1f}%")
    print("\n📊 Satisfaction Distribution (labels):")
    print(df["satisfaction_label"].value_counts())

    print("\n✔ Analysis Completed.")
    input("Press ENTER to return...")


# ============================================================
# Auto-run Streamlit if page is opened directly
# ============================================================
try:
    import streamlit as st

    if st.runtime.exists():
        run_customer_experience_ui()
except Exception:
    pass
