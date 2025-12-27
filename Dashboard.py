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
    import base64
    from pathlib import Path

    import streamlit as st
    import streamlit.components.v1 as components
    from services.ui_service import apply_global_styles

    st.set_page_config(page_title="SIA Dashboard", page_icon="🏠", layout="wide")

    apply_global_styles()

    @st.cache_data(show_spinner=False)
    def _file_to_base64(path: str) -> str | None:
        p = Path(path)
        if not p.exists():
            return None
        data = p.read_bytes()
        return base64.b64encode(data).decode("utf-8")

    video_b64 = _file_to_base64("assets/hero.mp4")
    logo_b64 = _file_to_base64("assets/singapore_airlines_logo.png")

    logo_html = ""
    if logo_b64:
        logo_html = f"""
        <img src="data:image/png;base64,{logo_b64}"
             style="height:76px; width:auto; border-radius:12px; background:rgba(255,255,255,0.92); padding:10px 14px;" />
        """

    if video_b64:
        hero_html = f"""
        <div style="
            position: relative;
            border-radius: 24px;
            overflow: hidden;
            height: 340px;
            box-shadow: 0 14px 40px rgba(0,0,0,0.25);
            margin-bottom: 2.2rem;
        ">
            <video autoplay muted loop playsinline
                style="
                    position:absolute;
                    inset:0;
                    width:100%;
                    height:100%;
                    object-fit:cover;
                    filter: saturate(1.05) contrast(1.05);
                ">
                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
            </video>

            <div style="
                position:absolute;
                inset:0;
                background: linear-gradient(135deg,
                    rgba(0,26,77,0.88) 0%,
                    rgba(0,58,128,0.76) 55%,
                    rgba(0,26,77,0.82) 100%);
            "></div>

            <div style="
                position:absolute;
                inset:0;
                padding: 2.4rem 2.6rem;
                display:flex;
                flex-direction:column;
                justify-content:center;
                gap: 0.65rem;
            ">
                <div style="display:flex; align-items:center; gap:14px; margin-bottom: 0.6rem;">
                    {logo_html}
                </div>

                <div style="
                    font-size: 3.1rem;
                    font-weight: 900;
                    letter-spacing: -1px;
                    color: #FFFFFF;
                    line-height: 1.05;
                ">
                    Singapore Airlines Analytics System
                </div>

                <div style="
                    color: rgba(255,255,255,0.88);
                    font-size: 1.15rem;
                    max-width: 920px;
                ">
                    Enterprise cloud-based analytics dashboard for operational performance, customer experience, risk scenarios, and cloud processing concepts.
                </div>

                <div style="
                    margin-top: 0.85rem;
                    display:flex;
                    gap: 10px;
                    flex-wrap: wrap;
                ">
                    <span style="
                        display:inline-block;
                        padding: 8px 12px;
                        border-radius: 999px;
                        background: rgba(255,237,77,0.22);
                        color: #FFED4D;
                        font-weight: 800;
                        font-size: 0.9rem;
                        border: 1px solid rgba(255,237,77,0.25);
                    ">Streamlit UI</span>

                    <span style="
                        display:inline-block;
                        padding: 8px 12px;
                        border-radius: 999px;
                        background: rgba(255,255,255,0.12);
                        color: rgba(255,255,255,0.88);
                        font-weight: 700;
                        font-size: 0.9rem;
                        border: 1px solid rgba(255,255,255,0.14);
                    ">CLI Supported</span>

                    <span style="
                        display:inline-block;
                        padding: 8px 12px;
                        border-radius: 999px;
                        background: rgba(255,255,255,0.12);
                        color: rgba(255,255,255,0.88);
                        font-weight: 700;
                        font-size: 0.9rem;
                        border: 1px solid rgba(255,255,255,0.14);
                    ">Synthetic Dataset (train.csv)</span>
                </div>
            </div>
        </div>
        """
        components.html(hero_html, height=360)
    else:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #001A4D 0%, #003A80 100%);
                padding: 3.4rem;
                border-radius: 24px;
                margin-bottom: 2.2rem;
                box-shadow: 0 14px 40px rgba(0,0,0,0.25);
            ">
                <h1 style="
                    font-size: 3.1rem;
                    font-weight: 900;
                    letter-spacing: -1px;
                    margin: 0 0 0.5rem 0;
                    color: white;
                    line-height: 1.05;
                ">
                    Singapore Airlines Analytics System
                </h1>
                <p style="
                    color: rgba(255,255,255,0.85);
                    font-size: 1.15rem;
                    margin: 0;
                ">
                    Enterprise cloud-based analytics dashboard
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<h2 style='margin-top:0.5rem;'>📊 Analytics Modules</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    def module_card(title: str, desc: str, page_path: str):
        st.markdown(
            f"""
            <a href="/{page_path}" target="_self" style="text-decoration:none;">
                <div class="sia-card">
                    <div class="sia-card-title">{title}</div>
                    <div class="sia-card-desc">{desc}</div>
                </div>
            </a>
            """,
            unsafe_allow_html=True,
        )

    with col1:
        module_card(
            "✈️ Flight Performance Analytics",
            "Flight distance distribution, delay patterns, crew/service indicators, and estimated fuel usage.",
            "pages/Module1_Flight_Performance.py",
        )
        module_card(
            "⚠️ Risk & Scenario Simulation",
            "Operational uncertainty modelling using simulation and disruption scenarios.",
            "pages/Module3_Risk_Simulation.py",
        )

    with col2:
        module_card(
            "😊 Customer Experience Analytics",
            "Passenger satisfaction, service ratings, and experience insights.",
            "pages/Module2_Customer_Experience.py",
        )
        module_card(
            "☁️ Cloud Analytics",
            "Batch vs streaming concepts and scalable processing demonstrations.",
            "pages/Module4_Cloud_Analytics.py",
        )

    st.info("Use the sidebar or click a module card to navigate.")


def run_cli():
    from pages.Module1_Flight_Performance import run_flight_performance_cli
    from pages.Module2_Customer_Experience import run_customer_experience_cli

    print("===========================================")
    print("   Singapore Airlines Analytics System CLI")
    print("===========================================")

    while True:
        print("\n1. Flight Performance Analytics")
        print("2. Customer Experience Analytics")
        print("3. Risk & Scenario Simulation")
        print("4. Cloud Analytics")
        print("5. Exit\n")

        choice = input("Enter option (1–5): ").strip()

        if choice == "1":
            run_flight_performance_cli()
        elif choice == "2":
            run_customer_experience_cli()
        elif choice == "3":
            print("\n[CLI] Risk Simulation is visualization-focused.")
            print("Use the Streamlit UI for full functionality.")
            input("\nPress ENTER to return to menu...")
        elif choice == "4":
            print("\n[CLI] Cloud Analytics is visualization-focused.")
            print("Use the Streamlit UI for full functionality.")
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
