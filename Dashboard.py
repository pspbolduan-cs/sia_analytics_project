# ============================================
# Author: Qian Zhu
# Date: 2025-12
# Singapore Airlines Analytics System
# Dashboard (Home Page) + CLI
# ============================================

import sys
import logging

logging.basicConfig(level=logging.INFO)


# =============================================================
# STREAMLIT UI MODE
# =============================================================
def run_streamlit_ui():
    import os
    import streamlit as st

    from services.ui_service import apply_global_styles
    from services.data_service import load_data

    st.set_page_config(
        page_title="SIA Dashboard",
        page_icon="✈️",
        layout="wide",
    )

    apply_global_styles()

    # ---------- helpers ----------
    def _first_existing_col(df, candidates):
        cols_lower = {c.lower(): c for c in df.columns}
        for cand in candidates:
            if cand in df.columns:
                return cand
            cl = cand.lower()
            if cl in cols_lower:
                return cols_lower[cl]
        return None

    def _kpi(title: str, value: str, sub: str = ""):
        st.markdown(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 16px 16px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.06);
                height: 100%;
            ">
                <div style="color:#555555;font-size:0.9rem;font-weight:600;margin-bottom:6px;">{title}</div>
                <div style="color:#002663;font-size:2.2rem;font-weight:800;line-height:1;">{value}</div>
                {f'<div style="margin-top:8px;color:#555555;font-size:0.9rem;">{sub}</div>' if sub else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _page_link(label: str, page_path: str, desc: str):
        """
        Uses Streamlit page links when available, otherwise falls back to anchor links.
        """
        # Streamlit page_link exists in newer versions; keep a safe fallback.
        if hasattr(st, "page_link"):
            st.markdown(
                f"""
                <div class="sia-card" style="padding:18px 18px;">
                    <div class="sia-card-title" style="margin-bottom:6px;">{label}</div>
                    <div class="sia-card-desc" style="margin-bottom:14px;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.page_link(page_path, label="Open", icon="➡️")
        else:
            # Fallback: works well in Streamlit Cloud for multipage apps
            st.markdown(
                f"""
                <a href="/{page_path}" target="_self" style="text-decoration:none;">
                    <div class="sia-card" style="padding:18px 18px;">
                        <div class="sia-card-title" style="margin-bottom:6px;">{label}</div>
                        <div class="sia-card-desc">{desc}</div>
                        <div style="margin-top:12px;font-weight:800;color:#002663;">Open ➜</div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True,
            )

    # ---------- top bar / branding ----------
    logo_path = os.path.join("assets", "singapore_airlines_logo.png")
    has_logo = os.path.exists(logo_path)

    left, right = st.columns([1, 3])
    with left:
        if has_logo:
            st.image(logo_path, use_container_width=True)
    with right:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #001A4D 0%, #003A80 100%);
                padding: 3.0rem;
                border-radius: 22px;
                margin-bottom: 1.6rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.25);
                position: relative;
                overflow: hidden;
            ">
                <div style="
                    position:absolute;
                    right:-80px;
                    top:-80px;
                    width:260px;
                    height:260px;
                    background: rgba(255, 237, 77, 0.18);
                    border-radius: 999px;
                "></div>

                <div style="
                    position:absolute;
                    right:40px;
                    bottom:-120px;
                    width:320px;
                    height:320px;
                    background: rgba(255,255,255,0.08);
                    border-radius: 999px;
                "></div>

                <h1 style="
                    font-size: 3.0rem;
                    font-weight: 900;
                    letter-spacing: -1px;
                    margin: 0 0 0.4rem 0;
                    color: white;
                ">
                    Singapore Airlines Analytics System
                </h1>

                <p style="
                    color: #E5E7EB;
                    font-size: 1.15rem;
                    margin: 0;
                ">
                    Enterprise cloud-based analytics dashboard
                </p>

                <div style="
                    margin-top: 1.2rem;
                    color: #E5E7EB;
                    font-size: 0.95rem;
                ">
                    CN6001 • Streamlit UI + CLI • Synthetic dataset (train.csv)
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------- quick dataset health ----------
    df = load_data()

    delay_col = _first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay"])
    dist_col = _first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance"])
    sat_col = _first_existing_col(df, ["satisfaction", "Satisfaction", "satisfied"])

    total_rows = len(df)
    total_cols = df.shape[1]
    missing_cells = int(df.isna().sum().sum())

    avg_delay = None
    if delay_col:
        s = pd.to_numeric(df[delay_col], errors="coerce")
        if s.notna().any():
            avg_delay = float(s.mean())

    avg_dist = None
    if dist_col:
        s = pd.to_numeric(df[dist_col], errors="coerce")
        if s.notna().any():
            avg_dist = float(s.mean())

    sat_rate = None
    if sat_col:
        v = df[sat_col]
        if v.dtype == object:
            sat_rate = float((v.astype(str).str.lower().str.contains("satisf")).mean() * 100.0)
        else:
            vv = pd.to_numeric(v, errors="coerce")
            if vv.notna().any():
                sat_rate = float((vv > 0).mean() * 100.0)

    st.markdown("<h2 style='margin-top:0.2rem;'>📌 Overview</h2>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        _kpi("Records", f"{total_rows:,}", "Rows in train.csv")
    with k2:
        _kpi("Columns", f"{total_cols}", "Dataset schema size")
    with k3:
        _kpi("Missing cells", f"{missing_cells:,}", "Data quality check")
    with k4:
        if sat_rate is not None:
            _kpi("Satisfied rate", f"{sat_rate:.1f}%", "Based on satisfaction label")
        else:
            _kpi("Satisfied rate", "N/A", "Column not found")

    k5, k6 = st.columns(2)
    with k5:
        if avg_delay is not None:
            _kpi("Avg departure delay", f"{avg_delay:.1f} min", f"Column: {delay_col}")
        else:
            _kpi("Avg departure delay", "N/A", "Delay column not found")
    with k6:
        if avg_dist is not None:
            _kpi("Avg flight distance", f"{avg_dist:,.0f} km", f"Column: {dist_col}")
        else:
            _kpi("Avg flight distance", "N/A", "Distance column not found")

    # ---------- modules ----------
    st.markdown("<h2 style='margin-top:1.8rem;'>📊 Analytics Modules</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        _page_link(
            "✈️ Flight Performance Analytics",
            "pages/Module1_Flight_Performance.py",
            "Flight distance, delays, crew performance, and estimated fuel usage.",
        )
        _page_link(
            "⚠️ Risk & Scenario Simulation",
            "pages/Module3_Risk_Simulation.py",
            "Scenario controls, risk indicators, delay distribution, and volatility simulation.",
        )

    with col2:
        _page_link(
            "😊 Customer Experience Analytics",
            "pages/Module2_Customer_Experience.py",
            "Passenger satisfaction, service quality, and inflight experience insights.",
        )
        _page_link(
            "☁️ Cloud Analytics",
            "pages/Module4_Cloud_Analytics.py",
            "Ingestion metrics, batch processing, and streaming-style analytics simulation.",
        )

    st.info("Tip: Use the sidebar or click a module card to navigate.")


# =============================================================
# CLI MODE
# =============================================================
def run_cli():
    print("===========================================")
    print("   Singapore Airlines Analytics System CLI")
    print("===========================================")

    # Lazy imports so CLI starts even if Streamlit-only dependencies exist elsewhere
    try:
        from pages.Module1_Flight_Performance import run_cli as run_flight_cli
    except Exception:
        run_flight_cli = None

    try:
        from pages.Module2_Customer_Experience import run_cli as run_customer_cli
    except Exception:
        run_customer_cli = None

    try:
        from pages.Module3_Risk_Simulation import run_cli as run_risk_cli
    except Exception:
        run_risk_cli = None

    try:
        from pages.Module4_Cloud_Analytics import run_cli as run_cloud_cli
    except Exception:
        run_cloud_cli = None

    while True:
        print("\n1. Flight Performance Analytics")
        print("2. Customer Experience Analytics")
        print("3. Risk & Scenario Simulation")
        print("4. Cloud Analytics")
        print("5. Exit\n")

        choice = input("Enter option (1–5): ").strip()

        if choice == "1":
            if run_flight_cli:
                run_flight_cli()
            else:
                print("Module 1 CLI not available.")
                input("\nPress ENTER to return to menu...")

        elif choice == "2":
            if run_customer_cli:
                run_customer_cli()
            else:
                print("Module 2 CLI not available.")
                input("\nPress ENTER to return to menu...")

        elif choice == "3":
            if run_risk_cli:
                run_risk_cli()
            else:
                print("Module 3 CLI not available.")
                input("\nPress ENTER to return to menu...")

        elif choice == "4":
            if run_cloud_cli:
                run_cloud_cli()
            else:
                print("Module 4 CLI not available.")
                input("\nPress ENTER to return to menu...")

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("❌ Invalid option.")
            input("Press ENTER to continue...")


# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == "__main__":
    # CLI MODE: python Dashboard.py cli
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    # STREAMLIT UI MODE: streamlit run Dashboard.py
    else:
        # Keep imports local to avoid CLI issues on some systems
        import pandas as pd  # noqa: F401
        run_streamlit_ui()
