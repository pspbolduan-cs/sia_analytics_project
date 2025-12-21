# Author: Philippe Bolduan

import numpy as np
import pandas as pd


def _safe_apply_global_styles():
    try:
        from services.ui_service import apply_global_styles
        apply_global_styles()
        return True
    except Exception:
        return False


def _inject_module_css():
    import streamlit as st

    # Use the SAME palette from ui_service.py
    PRIMARY_NAVY = "#002663"
    ACCENT_GOLD = "#FFED4D"
    BACKGROUND_CREAM = "#F5F3EE"
    TEXT_GREY = "#555555"
    CARD_BG = "#FFFFFF"
    CARD_BORDER = "#E5E7EB"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {BACKGROUND_CREAM};
        }}

        h1, h2, h3 {{
            color: {PRIMARY_NAVY};
        }}

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
        cl = cand.lower()
        if cl in cols_lower:
            return cols_lower[cl]
    return None


# -----------------------------
# Simulation Models
# -----------------------------
def simulate_delay_monte_carlo(mean_delay: float, std_delay: float, n: int, crisis_multiplier: float) -> np.ndarray:
    delays = np.random.normal(loc=mean_delay, scale=std_delay, size=n)
    delays = np.clip(delays, 0, None)
    return delays * crisis_multiplier


def delay_risk_kpis(delays: np.ndarray, threshold: float) -> dict:
    return {
        "expected": float(np.mean(delays)),
        "p_over": float(np.mean(delays > threshold) * 100.0),
        "p95": float(np.percentile(delays, 95)),
        "p99": float(np.percentile(delays, 99)),
        "worst": float(np.max(delays)),
    }


def simulate_fuel_price_paths(start_price: float, days: int, annual_vol: float, annual_drift: float, n_paths: int) -> pd.DataFrame:
    # Simple GBM for academic demonstration (fast + looks good)
    dt = 1 / 365.0
    prices = np.zeros((days + 1, n_paths), dtype=float)
    prices[0, :] = start_price
    for t in range(1, days + 1):
        z = np.random.normal(0, 1, n_paths)
        prices[t, :] = prices[t - 1, :] * np.exp((annual_drift - 0.5 * annual_vol**2) * dt + annual_vol * np.sqrt(dt) * z)
    out = pd.DataFrame(prices)
    out.index.name = "Day"
    return out


# -----------------------------
# Streamlit UI
# -----------------------------
def run_streamlit():
    import streamlit as st
    from services.data_service import load_data

    _safe_apply_global_styles()
    _inject_module_css()

    st.title("⚠️ Risk & Scenario Simulation")
    st.markdown(
        '<div class="sia-subtext">This module models operational uncertainty using Monte Carlo simulation and scenario-based risk modelling.</div>',
        unsafe_allow_html=True,
    )

    df = load_data()

    delay_col = _first_existing_col(df, ["DepartureDelay", "DepDelay", "departure_delay", "dep_delay"])
    dist_col = _first_existing_col(df, ["FlightDistance", "Distance", "flight_distance"])

    if delay_col is None:
        st.error("Dataset does not contain a departure delay column (expected 'DepartureDelay' or similar).")
        return

    delay_series = pd.to_numeric(df[delay_col], errors="coerce").dropna()
    mean_delay = float(delay_series.mean())
    std_delay = float(delay_series.std()) if float(delay_series.std()) > 0 else 10.0

    st.markdown('<div class="section-title">🎛️ Scenario Controls</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        sims = st.slider("Monte Carlo simulations", 2000, 50000, 12000, step=2000)
    with c2:
        threshold = st.slider("Delay risk threshold (min)", 15, 180, 60, step=5)
    with c3:
        crisis_mult = st.slider("Crisis multiplier", 1.0, 2.5, 1.15, step=0.05)

    # Run immediately so the page is NEVER blank
    delays = simulate_delay_monte_carlo(mean_delay, std_delay, sims, crisis_mult)
    kpis = delay_risk_kpis(delays, threshold)

    st.markdown('<div class="section-title">⭐ Key Risk Indicators</div>', unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        _kpi_card(st, "Expected Delay (min)", f"{kpis['expected']:.1f}", badge=f"Baseline μ={mean_delay:.1f}")
    with k2:
        _kpi_card(st, f"P(Delay > {threshold}m)", f"{kpis['p_over']:.1f}%", badge="Operational risk")
    with k3:
        _kpi_card(st, "95th Percentile", f"{kpis['p95']:.1f}", badge="Resilience KPI")
    with k4:
        _kpi_card(st, "Worst Case", f"{kpis['worst']:.1f}", badge="Tail risk")

    st.markdown('<div class="section-title">📊 Simulated Delay Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">Binned histogram of simulated delays (auto-generated on load).</div>', unsafe_allow_html=True)

    # Make a clean binned histogram as a bar chart
    upper = int(max(180, np.percentile(delays, 99) + 30))
    bins = np.arange(0, upper + 5, 5)
    hist, edges = np.histogram(delays, bins=bins)
    hist_df = pd.DataFrame({"Delay (min)": edges[:-1], "Count": hist}).set_index("Delay (min)")
    st.bar_chart(hist_df)

    st.markdown('<div class="section-title">🛢️ Fuel Price Volatility (Simulation)</div>', unsafe_allow_html=True)
    st.markdown('<div class="hint">GBM-style synthetic simulation for academic demonstration.</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        start_price = st.number_input("Starting fuel price (USD)", min_value=20.0, max_value=250.0, value=85.0, step=1.0)
    with f2:
        days = st.slider("Days to simulate", 30, 365, 180, step=15)
    with f3:
        vol = st.slider("Annual volatility", 0.05, 0.80, 0.35, step=0.05)

    fuel_paths = simulate_fuel_price_paths(start_price, days, annual_vol=vol, annual_drift=0.03, n_paths=18)
    st.line_chart(fuel_paths)

    st.markdown('<div class="section-title">🧭 Context: Distance vs Delay (Dataset Trend)</div>', unsafe_allow_html=True)

    if dist_col is None:
        st.info("No distance column found. Skipping distance context chart.")
        return

    dist = pd.to_numeric(df[dist_col], errors="coerce")
    tmp = pd.DataFrame({"distance": dist, "delay": pd.to_numeric(df[delay_col], errors="coerce")}).dropna()

    tmp["distance_bucket"] = pd.cut(tmp["distance"], bins=8)
    trend = tmp.groupby("distance_bucket", observed=True)["delay"].mean().reset_index()
    trend["distance_bucket"] = trend["distance_bucket"].astype(str)
    trend = trend.set_index("distance_bucket")

    st.line_chart(trend)


# -----------------------------
# CLI
# -----------------------------
def run_cli():
    from services.data_service import load_data

    print("\n--- Risk & Scenario Simulation (CLI) ---")

    df = load_data()
    delay_col = _first_existing_col(df, ["DepartureDelay", "DepDelay", "departure_delay", "dep_delay"])
    if delay_col is None:
        print("ERROR: Could not find departure delay column.")
        return

    delay_series = pd.to_numeric(df[delay_col], errors="coerce").dropna()
    mean_delay = float(delay_series.mean())
    std_delay = float(delay_series.std()) if float(delay_series.std()) > 0 else 10.0

    sims = 12000
    threshold = 60
    crisis_mult = 1.15

    delays = simulate_delay_monte_carlo(mean_delay, std_delay, sims, crisis_mult)
    kpis = delay_risk_kpis(delays, threshold)

    print(f"Baseline mean delay: {mean_delay:.2f} min | std: {std_delay:.2f} min")
    print(f"Simulations: {sims} | Crisis multiplier: {crisis_mult:.2f}")
    print(f"Expected delay: {kpis['expected']:.2f} min")
    print(f"P(Delay > {threshold} min): {kpis['p_over']:.2f}%")
    print(f"95th percentile: {kpis['p95']:.2f} min")
    print(f"99th percentile: {kpis['p99']:.2f} min")
    print(f"Worst case: {kpis['worst']:.2f} min")


def main(mode="streamlit"):
    if mode == "cli":
        run_cli()
    else:
        run_streamlit()


if __name__ == "__main__":
    main()

