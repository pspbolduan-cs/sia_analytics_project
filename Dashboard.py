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
    import base64
    import streamlit as st
    from services.ui_service import apply_global_styles

    st.set_page_config(
        page_title="SIA Dashboard",
        page_icon="🏠",
        layout="wide"
    )

    apply_global_styles()

    def video_to_base64(path: str) -> str | None:
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    hero_video_path = os.path.join("assets", "hero.mp4")
    hero_video_b64 = video_to_base64(hero_video_path)

    # ======================
    # HERO SECTION
    # ======================
    if hero_video_b64:
        st.markdown(
            f"""
            <div style="
                position: relative;
                height: 340px;
                border-radius: 22px;
                overflow: hidden;
                margin-bottom: 2.2rem;
                box-shadow: 0 12px 35px rgba(0,0,0,0.35);
            ">

                <div style="position:absolute; inset:0;">
                    <video autoplay muted loop playsinline
                        style="
                            width:100%;
                            height:100%;
                            object-fit:cover;
                        ">
                        <source src="data:video/mp4;base64,{hero_video_b64}" type="video/mp4">
                    </video>

                    <div style="
                        position:absolute;
                        inset:0;
                        background: linear-gradient(
                            135deg,
                            rgba(0,26,77,0.65),
                            rgba(0,58,128,0.55)
                        );
                    "></div>
                </div>

                <div style="
                    position: relative;
                    z-index: 2;
                    padding: 3rem;
                    color: white;
                ">
                    <h1 style="
                        font-size: 3.1rem;
                        font-weight: 900;
                        margin-bottom: 0.6rem;
                        letter-spacing: -0.5px;
                        color: white;
                    ">
                        Singapore Airlines Analytics System
                    </h1>

                    <p style="
                        font-size: 1.15rem;
                        color: #F3F4F6;
                        margin-top: 0;
                        max-width: 900px;
                    ">
                        Enterprise Cloud-Based Analytics Dashboard
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #001A4D 0%, #003A80 100%);
                padding: 3.8rem;
                border-radius: 20px;
                margin-bottom: 2.5rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            ">
                <h1 style="
                    font-size: 3.4rem;
                    font-weight: 900;
                    letter-spacing: -1px;
                    margin-bottom: 0.5rem;
                    color: white;
                ">
                    Singapore Airlines Analytics System
                </h1>
                <p style="
                    color: #F3F4F6;
                    font-size: 1.2rem;
                    margin-top: 0.5rem;
                ">
                    Enterprise Cloud-Based Analytics Dashboard
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ======================
    # MODULES
    # ======================
    st.markdown("<h2>📊 Analytics Modules</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    def module_card(title: str, desc: str, link: str):
        st.markdown(
            f"""
            <a href="/{link}" target="_self" style="text-decoration:none;">
                <div class="sia-card">
                    <div class="sia-card-title">{title}</div>
                    <div class="sia-card-desc">{desc}</div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

    with col1:
        module_card(
            "✈️ Flight Performance Analytics",
            "Flight distance, delays, crew performance, and estimated fuel usage.",
            "pages/Module1_Flight_Performance.py"
        )
        module_card(
            "⚠️ Risk & Scenario Simulation",
            "Simulations and operational risk forecasting.",
            "pages/Module3_Risk_Simulation.py"
        )

    with col2:
        module_card(
            "😊 Customer Experience Analytics",
            "Passenger satisfaction, service quality, and inflight experience.",
            "pages/Module2_Customer_Experience.py"
        )
        module_card(
            "☁️ Cloud Analytics",
            "Cloud-based data loading and scalability demonstrations.",
            "pages/Module4_Cloud_Analytics.py"
        )

    st.info("Use the sidebar or click any module card to navigate.")


# =============================================================
# CLI MODE
# =============================================================
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
            print("\n[CLI] Risk Simulation is best viewed in Streamlit UI.")
            input("\nPress ENTER to return to menu...")

        elif choice == "4":
            print("\n[CLI] Cloud Analytics is best viewed in Streamlit UI.")
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
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
