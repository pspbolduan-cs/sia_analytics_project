# ============================================================
# Author: Philippe Bolduan
# Module: Risk & Scenario Simulation
# Course: CN6001 Enterprise Application & Cloud Computing
#
# Description:
# This module models operational uncertainty using simulation and
# scenario-based risk modelling. Because real airline operational
# data is confidential, a synthetic dataset (train.csv) is used for
# academic demonstration purposes.
# ============================================================

import numpy as np
import pandas as pd


def _safe_apply_global_styles():
    """Apply shared UI theme if available (safe for CLI too)."""
    try:
        from services.ui_service import apply_global_styles
        apply_global_styles()
        return True
    except Exception:
        return False


def _inject_module_css():
    """Inject module-specific UI styles using the same palette as ui_service.py."""
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
            padding: 16px;
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_back_links():
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


def _kpi_card(st, title: str, value: str, badge: str = ""):
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
    cols_lower = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand in df.columns:
            return cand
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    return None


def simulate_delay_monte_carlo(mean_delay, std_delay, n, crisis_multiplier):
    delays = np.random.normal(mean_delay, std_delay, n)
    delays = np.clip(delays, 0, None)
    return delays * crisis_multiplier


def delay_risk_kpis(delays, threshold):
    return {
        "expected": np.mean(delays),
        "p_over": np.mean(delays > threshold) * 100,
        "p95": np.percentile(delays, 95),
        "p99": np.percentile(delays, 99),
        "worst": np.max(delays),
    }


def simulate_fuel_price_paths(start_price, days, annual_vol, annual_drift, n_paths):
    dt = 1 / 365
    prices = np.zeros((days + 1, n_paths))
    prices[0] = start_price

    for t in range(1, days + 1):
        z = np.random.normal(0, 1, n_paths)
        prices[t] = prices[t - 1] * np.exp(
            (annual_drift - 0.5 * annual_vol**2) * dt + annual_vol * np.sqrt(dt) * z
        )

    df = pd.DataFrame(prices)
    df.index.name = "Day"
    return df


def run_streamlit():
    import streamlit as st
    from services.data_service import load_data

    _safe_apply_global_styles()
    _inject_module_css()
    _render_back_links()

    st.title("⚠️ Risk & Scenario Simulation")
    st.markdown(
        '<div class="sia-subtext">This module models operational uncertainty using simulation and scenario-based risk modelling.</div>',
        unsafe_allow_html=True,
    )

    df = load_data()

    delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepDelay"])
    dist_col = _first_existing_col(df, ["Flight Distance", "Distance"])

    if delay_col is None:
        st.error("No departure delay column found.")
        return

    delays_raw = pd.to_numeric(df[delay_col], errors="coerce").dropna()
    mean_delay = delays_raw.mean()
    std_delay = delays_raw.std() if delays_raw.std() > 0 else 10

    st.markdown('<div class="section-title">🎛️ Scenario Controls</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    sims = c1.slider("Monte Carlo simulations", 2000, 50000, 12000, step=2000)
    threshold = c2.slider("Delay risk threshold (min)", 15, 180, 60, step=5)
    crisis_mult = c3.slider("Crisis multiplier", 1.0, 2.5, 1.15, step=0.05)

    delays = simulate_delay_monte_carlo(mean_delay, std_delay, sims, crisis_mult)
    kpis = delay_risk_kpis(delays, threshold)

    st.markdown('<div class="section-title">⭐ Key Risk Indicators</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    _kpi_card(k1, "Expected Delay (min)", f"{kpis['expected']:.1f}")
    _kpi_card(k2, f"P(Delay > {threshold}m)", f"{kpis['p_over']:.1f}%")
    _kpi_card(k3, "95th Percentile", f"{kpis['p95']:.1f}")
    _kpi_card(k4, "Worst Case", f"{kpis['worst']:.1f}")

    st.markdown('<div class="section-title">📊 Simulated Delay Distribution</div>', unsafe_allow_html=True)
    st.bar_chart(pd.Series(delays).value_counts().sort_index())

    st.markdown('<div class="section-title">🛢️ Fuel Price Volatility</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    start_price = f1.number_input("Starting fuel price (USD)", 20.0, 250.0, 85.0)
    days = f2.slider("Days to simulate", 30, 365, 180, step=15)
    vol = f3.slider("Annual volatility", 0.05, 0.8, 0.35, step=0.05)

    fuel_paths = simulate_fuel_price_paths(start_price, days, vol, 0.03, 18)
    st.line_chart(fuel_paths)

    if dist_col:
        st.markdown('<div class="section-title">🧭 Distance vs Delay</div>', unsafe_allow_html=True)
        tmp = pd.DataFrame({
            "distance": pd.to_numeric(df[dist_col], errors="coerce"),
            "delay": pd.to_numeric(df[delay_col], errors="coerce"),
        }).dropna()
        tmp["bucket"] = pd.cut(tmp["distance"], bins=8)
        st.line_chart(tmp.groupby("bucket")["delay"].mean())


def run_cli():
    print("CLI mode not implemented for this module.")


def main(mode="streamlit"):
    if mode == "cli":
        run_cli()
    else:
        run_streamlit()


if __name__ == "__main__":
    main()
