# ============================================================
# Author: Philippe Bolduan
# Module: Cloud Analytics
# Course: CN6001 Enterprise Application & Cloud Computing
#
# Description:
# This module demonstrates cloud-style analytics patterns using a
# synthetic airline dataset (train.csv). It illustrates:
#  - Batch processing (warehouse-style KPIs)
#  - Streaming/real-time processing (chunk-based simulation)
#
# Notes:
# - The dataset is synthetic and used for academic purposes only.
# - This module supports Streamlit UI and CLI mode via Dashboard router.
#
# Key Concepts:
# - Batch vs Streaming analytics
# - Scalable processing concepts (chunking, incremental updates)
# - Simple KPI computations on large datasets
# ============================================================

import time
import pandas as pd


def _safe_apply_global_styles():
    """
    Apply shared SIA global theme if available.
    This is safe even if the module runs in CLI mode or if imports fail.
    """
    try:
        from services.ui_service import apply_global_styles
        apply_global_styles()
        return True
    except Exception:
        return False


def _inject_module_css():
    """
    Inject module-specific CSS using the same palette defined in ui_service.py.
    Ensures visual consistency with the other modules.
    """
    import streamlit as st

    PRIMARY_NAVY = "#002663"
    ACCENT_GOLD = "#FFED4D"
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

        .kpi-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 16px;
            padding: 16px 16px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
            height: 100%;
        }}
        .kpi-title {{
            color: {TEXT_GREY};
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .kpi-value {{
            color: {PRIMARY_NAVY};
            font-size: 2.2rem;
            font-weight: 800;
            line-height: 1;
        }}
        .kpi-badge {{
            display: inline-block;
            margin-top: 8px;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(255, 237, 77, 0.35);
            color: {PRIMARY_NAVY};
            font-weight: 700;
            font-size: 0.78rem;
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def _kpi_card(st, title: str, value: str, badge: str = ""):
    """Render a themed KPI card (consistent with Module 2 style)."""
    badge_html = f'<div class="kpi-badge">{badge}</div>' if badge else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            {badge_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _first_existing_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first candidate column found in df (case-safe)."""
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        cl = cand.lower()
        if cl in cols_lower:
            return cols_lower[cl]
    return None


# -----------------------------
# Batch Processing (Cloud-style job)
# -----------------------------
def batch_processing(df: pd.DataFrame) -> dict:
    """
    Simulate a batch analytics job:
    - Compute KPIs across the whole dataset (warehouse style)
    - Add short sleep to mimic cloud ETL latency (academic demo)
    """
    time.sleep(0.4)

    # ✅ Match actual train.csv column names
    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance", "flight_distance"])
    dep_delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay", "dep_delay"])
    sat_col = _first_existing_col(df, ["satisfaction", "Satisfaction"])

    total_records = int(len(df))

    avg_distance = float("nan")
    if dist_col:
        avg_distance = float(pd.to_numeric(df[dist_col], errors="coerce").dropna().mean())

    avg_dep_delay = float("nan")
    if dep_delay_col:
        avg_dep_delay = float(pd.to_numeric(df[dep_delay_col], errors="coerce").dropna().mean())

    satisfaction_rate = float("nan")
    if sat_col:
        # Your dataset uses labels like "satisfied" / "neutral or dissatisfied"
        s = df[sat_col].astype(str).str.lower()
        satisfaction_rate = float(s.str.contains("satisfied").mean() * 100.0)

    return {
        "Total Records": total_records,
        "Average Distance (km)": avg_distance,
        "Average Departure Delay (min)": avg_dep_delay,
        "Satisfaction Rate (%)": satisfaction_rate,
    }


# -----------------------------
# Streaming / Real-Time Simulation
# -----------------------------
def realtime_processing(df: pd.DataFrame, chunk_size: int):
    """
    Generator that yields dataset chunks to simulate streaming ingestion.
    This mimics near-real-time processing without needing a real stream source.
    """
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i : i + chunk_size]
        time.sleep(0.06)  # small delay to show progress clearly in UI


# -----------------------------
# Streamlit UI
# -----------------------------
def run_streamlit():
    import streamlit as st
    from services.data_service import load_data

    _safe_apply_global_styles()
    _inject_module_css()

    st.title("☁️ Cloud Analytics")
    st.markdown(
        '<div class="sia-subtext">Cloud-style analytics demonstration: batch processing vs streaming (academic simulation).</div>',
        unsafe_allow_html=True,
    )

    df = load_data()

    # Batch KPIs (full dataset summary)
    st.markdown('<div class="section-title">⭐ Batch Job KPIs</div>', unsafe_allow_html=True)
    results = batch_processing(df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        _kpi_card(st, "Total Records", f"{results['Total Records']:,}", badge="Batch ingest size")
    with c2:
        v = results["Average Distance (km)"]
        _kpi_card(st, "Avg Distance (km)", "N/A" if pd.isna(v) else f"{v:.1f}", badge="Warehouse KPI")
    with c3:
        v = results["Average Departure Delay (min)"]
        _kpi_card(st, "Avg Delay (min)", "N/A" if pd.isna(v) else f"{v:.1f}", badge="Ops KPI")
    with c4:
        v = results["Satisfaction Rate (%)"]
        _kpi_card(st, "Satisfaction Rate", "N/A" if pd.isna(v) else f"{v:.1f}%", badge="CX KPI")

    # Explanation: batch vs streaming (enterprise/cloud concept)
    st.markdown('<div class="section-title">📦 Batch vs Real-Time</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">'
        "• <b>Batch</b>: periodic ETL jobs (data lake → warehouse) for reporting<br>"
        "• <b>Streaming</b>: continuous updates for near real-time monitoring"
        "</div>",
        unsafe_allow_html=True,
    )

    # Streaming simulation
    st.markdown('<div class="section-title">🛰️ Streaming Simulation</div>', unsafe_allow_html=True)
    chunk_size = st.slider("Chunk size (records)", 50, 500, 150, step=50)

    placeholder = st.empty()
    progress = st.progress(0)

    if st.button("Start Stream"):
        processed = 0
        total = len(df)

        for chunk in realtime_processing(df, chunk_size):
            processed += len(chunk)
            pct = min(1.0, processed / total)
            progress.progress(int(pct * 100))

            # Show incremental progress updates
            placeholder.info(f"Processed {processed:,} / {total:,} records")

        placeholder.success("Streaming simulation complete ✅")


# -----------------------------
# CLI Mode
# -----------------------------
def run_cli():
    """
    CLI entry point for non-visual cloud analytics demonstration.
    Prints batch KPIs as a quick verification for the coursework requirement.
    """
    from services.data_service import load_data

    print("\n--- Cloud Analytics (CLI) ---")
    df = load_data()
    results = batch_processing(df)

    for k, v in results.items():
        if isinstance(v, float):
            print(f"{k}: {'N/A' if pd.isna(v) else f'{v:.2f}'}")
        else:
            print(f"{k}: {v}")

    print("Cloud analytics completed.")


def main(mode="streamlit"):
    if mode == "cli":
        run_cli()
    else:
        run_streamlit()


if __name__ == "__main__":
    main()
