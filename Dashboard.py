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
    import streamlit as st
    from services.ui_service import apply_global_styles

    st.set_page_config(
        page_title="SIA Dashboard",
        page_icon="🏠",
        layout="wide",
    )

    apply_global_styles()

    # HERO (Video background)
    st.markdown(
        """
        <div style="
            position:relative;
            width:100%;
            height:420px;
            overflow:hidden;
            border-radius:20px;
            margin-bottom:2.5rem;
            box-shadow:0 10px 30px rgba(0,0,0,0.30);
        ">

            <video autoplay muted loop playsinline
                style="
                    position:absolute;
                    inset:0;
                    width:100%;
                    height:100%;
                    object-fit:cover;
                ">
                <source src="assets/hero.mp4" type="video/mp4">
            </video>

            <div style="
                position:absolute;
                inset:0;
                background:linear-gradient(
                    135deg,
                    rgba(0,26,77,0.88) 0%,
                    rgba(0,58,128,0.78) 100%
                );
            "></div>

            <div style="
                position:relative;
                z-index:2;
                padding:3.8rem;
            ">
                <h1 style="
                    font-size:3.4rem;
                    font-weight:900;
                    letter-spacing:-1px;
                    margin:0 0 0.6rem 0;
                    color:white;
                ">
                    Singapore Airlines Analytics System
                </h1>

                <p style="
                    color:#E5E7EB;
                    font-size:1.2rem;
                    margin:0;
                ">
                    Enterprise Cloud-Based Analytics Dashboard
                </p>
            </div>

            <div style="
                position:absolute;
                right:40px;
                bottom:-120px;
                width:320px;
                height:320px;
                background:rgba(255,255,255,0.08);
                border-radius:999px;
            "></div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h2>📊 Analytics Modules</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    def module_card(title, desc, link):
        st.markdown(
            f"""
            <a href="/{link}" target="_self" style="text-decoration:none;">
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
            "Flight distance, delays, crew performance, and estimated fuel usage.",
            "pages/Module1_Flight_Performance.py",
        )

        module_card(
            "⚠️ Risk & Scenario Simulation",
            "Risk simulation and disruption scenario modelling.",
            "pages/Module3_Risk_Simulation.py",
        )

    with col2:
        module_card(
            "😊 Customer Experience Analytics",
            "Passenger satisfaction, service quality, and inflight experience.",
            "pages/Module2_Customer_Experience.py",
        )

        module_card(
            "☁️ Cloud Analytics",
            "Cloud-style processing demonstration and scalable analytics concepts.",
            "pages/Module4_Cloud_Analytics.py",
        )

    st.info("Use the sidebar or click any module card to navigate.")


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
            print("\n[CLI] Risk Simulation module is visualization-focused.")
            print("Please use Streamlit UI for full functionality.")
            input("\nPress ENTER to return to menu...")

        elif choice == "4":
            print("\n[CLI] Cloud Analytics module is visualization-focused.")
            print("Please use Streamlit UI for full functionality.")
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
