# ============================================
# Author: Qian Zhu
# Date: 2025-12
# Singapore Airlines Analytics System
# Dashboard (Home Page) + CLI
# ============================================

import sys
import logging

logging.basicConfig(level=logging.INFO)


def run_streamlit_ui():
    import os
    import base64
    import pandas as pd
    import streamlit as st

    from services.ui_service import apply_global_styles
    from services.data_service import load_data

    st.set_page_config(
        page_title="SIA Dashboard",
        page_icon="✈️",
        layout="wide",
    )

    apply_global_styles()

    def first_existing_col(df, candidates):
        cols_lower = {c.lower(): c for c in df.columns}
        for cand in candidates:
            if cand in df.columns:
                return cand
            cl = cand.lower()
            if cl in cols_lower:
                return cols_lower[cl]
        return None

    def kpi_card(title: str, value: str, sub: str = ""):
        st.markdown(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 16px;
                padding: 16px;
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

    def module_card(title, desc, page_path):
        # Streamlit multipage apps typically work with /<page_name> routing,
        # but keeping your current approach for consistency.
        st.markdown(
            f"""
            <a href="/{page_path}" target="_self" style="text-decoration:none;">
                <div class="sia-card" style="padding:18px 18px;">
                    <div class="sia-card-title" style="margin-bottom:6px;">{title}</div>
                    <div class="sia-card-desc">{desc}</div>
                    <div style="margin-top:12px;font-weight:800;color:#002663;">Open ➜</div>
                </div>
            </a>
            """,
            unsafe_allow_html=True,
        )

    def video_to_base64(path: str) -> str | None:
        if not os.path.exists(path):
            return None
        try:
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        except Exception:
            return None

    # Optional assets
    logo_path = os.path.join("assets", "singapore_airlines_logo.png")

    # Optional hero video (add your own file)
    # Put it in: assets/hero.mp4
    hero_video_path = os.path.join("assets", "hero.mp4")
    hero_video_b64 = video_to_base64(hero_video_path)

    # HERO
    left, right = st.columns([1, 3], vertical_alignment="center")

    with left:
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)

    with right:
        if hero_video_b64:
            st.markdown(
                f"""
                <div style="
                    position: relative;
                    border-radius: 22px;
                    overflow: hidden;
                    margin-bottom: 1.6rem;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
                    min-height: 250px;
                ">
                    <video autoplay muted loop playsinline
                        style="
                            position:absolute;
                            top:0; left:0;
                            width:100%;
                            height:100%;
                            object-fit:cover;
                            filter: brightness(0.55);
                        ">
                        <source src="data:video/mp4;base64,{hero_video_b64}" type="video/mp4">
                    </video>

                    <div style="
                        position: relative;
                        z-index: 2;
                        padding: 3.0rem;
                    ">
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
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
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

    # Overview KPIs
    df = load_data()

    delay_col = first_existing_col(df, ["Departure Delay in Minutes", "DepartureDelay", "DepDelay"])
    dist_col = first_existing_col(df, ["Flight Distance", "FlightDistance", "Distance"])
    sat_col = first_existing_col(df, ["satisfaction", "Satisfaction", "satisfied"])

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

    r1, r2, r3, r4 = st.columns(4)
    with r1:
        kpi_card("Records", f"{total_rows:,}", "Rows in train.csv")
    with r2:
        kpi_card("Columns", f"{total_cols}", "Dataset schema size")
    with r3:
        kpi_card("Missing cells", f"{missing_cells:,}", "Data quality check")
    with r4:
        if sat_rate is not None:
            kpi_card("Satisfied rate", f"{sat_rate:.1f}%", "Based on satisfaction label")
        else:
            kpi_card("Satisfied rate", "N/A", "Column not found")

    r5, r6 = st.columns(2)
    with r5:
        if avg_delay is not None:
            kpi_card("Avg departure delay", f"{avg_delay:.1f} min", f"Column: {delay_col}")
        else:
            kpi_card("Avg departure delay", "N/A", "Delay column not found")
    with r6:
        if avg_dist is not None:
            kpi_card("Avg flight distance", f"{avg_dist:,.0f} km", f"Column: {dist_col}")
        else:
            kpi_card("Avg flight distance", "N/A", "Distance column not found")

    # Modules
    st.markdown("<h2 style='margin-top:1.8rem;'>📊 Analytics Modules</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        module_card(
            "✈️ Flight Performance Analytics",
            "Flight distance, delays, crew performance, and estimated fuel usage.",
            "pages/Module1_Flight_Performance.py",
        )
        module_card(
            "⚠️ Risk & Scenario Simulation",
            "Scenario controls, risk indicators, delay distribution, and volatility simulation.",
            "pages/Module3_Risk_Simulation.py",
        )

    with col2:
        module_card(
            "😊 Customer Experience Analytics",
            "Passenger satisfaction, service quality, and inflight experience insights.",
            "pages/Module2_Customer_Experience.py",
        )
        module_card(
            "☁️ Cloud Analytics",
            "Ingestion metrics, batch processing, and streaming-style simulation.",
            "pages/Module4_Cloud_Analytics.py",
        )

    st.info("Use the sidebar or click any module card to navigate.")


def run_cli():
    print("===========================================")
    print("   Singapore Airlines Analytics System CLI")
    print("===========================================")

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


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
