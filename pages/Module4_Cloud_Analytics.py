# ============================================================
# Author: Philippe Bolduan
# Module: Cloud Analytics
# Course: CN6001 Enterprise Application & Cloud Computing
#
# Description:
# This module demonstrates cloud-style analytics patterns using the
# project dataset (train.csv). It focuses on practical concepts:
# caching, batch processing, and a lightweight streaming simulation.
# ============================================================

from __future__ import annotations

import time
from typing import Optional

import numpy as np
import pandas as pd


# -----------------------------
# Helpers
# -----------------------------
def _safe_apply_global_styles() -> bool:
    try:
        from services.ui_service import apply_global_styles
        apply_global_styles()
        return True
    except Exception:
        return False


def _first_existing_col(df: pd.DataFrame, candidates: list[str]) -> Optional[str]:
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        cl = cand.lower()
        if cl in cols_lower:
            return cols_lower[cl]
    return None


def _inject_module_css() -> None:
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

        .back-row {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 6px 0 14px 0;
            font-size: 1rem;
        }}
        .back-row a {{
            text-decoration: none;
            font-weight: 700;
            color: {PRIMARY_NAVY};
        }}
        .back-row a:hover {{
            text-decoration: underline;
        }}

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
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_back_links() -> None:
    import streamlit as st

    st.markdown(
        """
        <div class="back-row">
            🏠 <a href="./" target="_self">Back to Dashboard</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sia-back-float">
            🏠 <a href="./" target="_self">Back to Dashboard</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _kpi_card(st, title: str, value: str, badge: str = "") -> None:
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


def _bytes_to_mb(x: int) -> float:
    return float(x) / (1024.0 * 1024.0)


def _df_memory_bytes(df: pd.DataFrame) -> int:
    return int(df.memory_usage(deep=True).sum())


# -----------------------------
# Cloud-style patterns
# -----------------------------
def _batch_aggregate(df: pd.DataFrame, batch_size: int) -> pd.DataFrame:
    """
    Simple batch processing pattern:
    - process the dataset in chunks
    - emit per-batch KPIs
    """
    n = len(df)
    out = []
    start = 0
    batch_id = 1

    delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay"])
    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance"])
    sat_col = _first_existing_col(df, ["satisfaction", "Satisfaction", "satisfied"])

    while start < n:
        end = min(start + batch_size, n)
        chunk = df.iloc[start:end]

        rows = len(chunk)
        missing = int(chunk.isna().sum().sum())

        avg_delay = None
        if delay_col:
            s = pd.to_numeric(chunk[delay_col], errors="coerce")
            avg_delay = float(s.mean()) if s.notna().any() else None

        avg_dist = None
        if dist_col:
            s = pd.to_numeric(chunk[dist_col], errors="coerce")
            avg_dist = float(s.mean()) if s.notna().any() else None

        sat_rate = None
        if sat_col:
            # handle "satisfied"/"neutral or dissatisfied" or 0/1
            v = chunk[sat_col]
            if v.dtype == object:
                sat_rate = float((v.astype(str).str.lower().str.contains("satisf")).mean() * 100.0)
            else:
                vv = pd.to_numeric(v, errors="coerce")
                if vv.notna().any():
                    # assume 1 indicates satisfied if binary-like
                    sat_rate = float((vv > 0).mean() * 100.0)

        out.append(
            {
                "Batch": batch_id,
                "Rows": rows,
                "Missing Cells": missing,
                "Avg Departure Delay": avg_delay,
                "Avg Flight Distance": avg_dist,
                "Satisfaction Rate %": sat_rate,
            }
        )

        start = end
        batch_id += 1

    return pd.DataFrame(out)


def _streaming_simulation(df: pd.DataFrame, window_size: int, steps: int, seed: int) -> pd.DataFrame:
    """
    Lightweight streaming-like simulation:
    - sample a rolling window from the dataset
    - compute metrics per step
    """
    rng = np.random.default_rng(seed)
    n = len(df)
    if n == 0:
        return pd.DataFrame()

    delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay"])
    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance"])

    rows = []
    for t in range(1, steps + 1):
        start = int(rng.integers(0, max(1, n)))
        end = min(n, start + window_size)
        window = df.iloc[start:end]

        avg_delay = None
        if delay_col:
            s = pd.to_numeric(window[delay_col], errors="coerce")
            avg_delay = float(s.mean()) if s.notna().any() else None

        avg_dist = None
        if dist_col:
            s = pd.to_numeric(window[dist_col], errors="coerce")
            avg_dist = float(s.mean()) if s.notna().any() else None

        rows.append({"Step": t, "Window Rows": len(window), "Avg Delay": avg_delay, "Avg Distance": avg_dist})

    return pd.DataFrame(rows)


# -----------------------------
# Streamlit UI
# -----------------------------
def run_streamlit() -> None:
    import streamlit as st
    from services.data_service import load_data

    _safe_apply_global_styles()
    _inject_module_css()
    _render_back_links()

    st.title("☁️ Cloud Analytics")
    st.markdown(
        '<div class="sia-subtext">Cloud-oriented patterns: cached ingestion, batch processing, and a lightweight streaming simulation.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">📥 Data Ingestion</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">This section demonstrates an ingestion step and basic dataset health indicators.</div>',
        unsafe_allow_html=True,
    )

    # timing load (cloud-style: show latency and caching behavior)
    t0 = time.perf_counter()
    df = load_data()
    load_ms = (time.perf_counter() - t0) * 1000.0

    total_rows = int(len(df))
    total_cols = int(df.shape[1])
    missing_cells = int(df.isna().sum().sum())
    mem_mb = _bytes_to_mb(_df_memory_bytes(df))

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        _kpi_card(st, "Rows", f"{total_rows:,}", "Dataset size")
    with k2:
        _kpi_card(st, "Columns", f"{total_cols}", "Schema width")
    with k3:
        _kpi_card(st, "Missing Cells", f"{missing_cells:,}", "Data quality")
    with k4:
        _kpi_card(st, "Load Time", f"{load_ms:.0f} ms", "Ingestion latency")

    with st.expander("Preview sample records"):
        st.dataframe(df.head(20), use_container_width=True)

    st.markdown('<div class="section-title">🧱 Batch Processing</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">Process data in chunks and compute per-batch metrics.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        batch_size = st.slider("Batch size (rows)", 1000, 50000, 10000, step=1000)
    with c2:
        show_table = st.checkbox("Show batch table", value=True)

    batch_df = _batch_aggregate(df, batch_size=batch_size)

    # chart: rows per batch
    chart_df = batch_df[["Batch", "Rows"]].set_index("Batch")
    st.bar_chart(chart_df)

    # chart: avg delay per batch (if available)
    if batch_df["Avg Departure Delay"].notna().any():
        delay_chart = batch_df[["Batch", "Avg Departure Delay"]].set_index("Batch")
        st.line_chart(delay_chart)

    if show_table:
        st.dataframe(batch_df, use_container_width=True)

    st.markdown('<div class="section-title">📡 Streaming Simulation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hint">A lightweight simulation that computes metrics on a rolling window, similar to near real-time dashboards.</div>',
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns(3)
    with s1:
        window_size = st.slider("Window size (rows)", 200, 20000, 4000, step=200)
    with s2:
        steps = st.slider("Steps", 5, 60, 20, step=5)
    with s3:
        seed = st.number_input("Seed", min_value=1, max_value=999999, value=2025, step=1)

    stream_df = _streaming_simulation(df, window_size=window_size, steps=steps, seed=int(seed))
    if len(stream_df) == 0:
        st.info("No data available for streaming simulation.")
    else:
        st.line_chart(stream_df.set_index("Step")[["Avg Delay"]].dropna())
        if stream_df["Avg Distance"].notna().any():
            st.line_chart(stream_df.set_index("Step")[["Avg Distance"]].dropna())

        with st.expander("Show streaming metrics table"):
            st.dataframe(stream_df, use_container_width=True)

    st.markdown('<div class="section-title">⚖️ Batch vs Real-time</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hint">
        <b>Batch</b> is efficient for scheduled reporting and heavy aggregation jobs.
        <br/>
        <b>Real-time</b> supports rapid monitoring and quick operational response, often using rolling windows or event streams.
        <br/><br/>
        This module demonstrates both patterns using the same dataset and metrics.
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# CLI
# -----------------------------
def run_cli() -> None:
    from services.data_service import load_data

    print("\n--- Cloud Analytics (CLI) ---")

    t0 = time.perf_counter()
    df = load_data()
    load_ms = (time.perf_counter() - t0) * 1000.0

    total_rows = int(len(df))
    total_cols = int(df.shape[1])
    missing_cells = int(df.isna().sum().sum())
    mem_mb = _bytes_to_mb(_df_memory_bytes(df))

    print(f"Rows: {total_rows:,}")
    print(f"Columns: {total_cols}")
    print(f"Missing cells: {missing_cells:,}")
    print(f"Estimated memory: {mem_mb:.2f} MB")
    print(f"Load time: {load_ms:.0f} ms")

    batch_size = 10000
    batch_df = _batch_aggregate(df, batch_size=batch_size)

    print(f"\nBatch processing (batch_size={batch_size}):")
    print(f"Total batches: {len(batch_df)}")
    print(f"Rows processed: {int(batch_df['Rows'].sum()):,}")

    if batch_df["Avg Departure Delay"].notna().any():
        avg_delay_overall = float(pd.to_numeric(df[_first_existing_col(df, ['Departure Delay in Minutes','DepartureDelay','DepDelay'])], errors="coerce").mean())
        print(f"Overall avg departure delay: {avg_delay_overall:.2f} min")

    # small streaming summary
    stream_df = _streaming_simulation(df, window_size=4000, steps=10, seed=2025)
    if len(stream_df) > 0 and stream_df["Avg Delay"].notna().any():
        print(f"Streaming avg delay (10 steps): mean={float(stream_df['Avg Delay'].mean()):.2f} min")


def main(mode: str = "streamlit") -> None:
    if mode == "cli":
        run_cli()
    else:
        run_streamlit()


if __name__ == "__main__":
    main()
