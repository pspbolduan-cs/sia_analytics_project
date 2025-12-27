# ============================================
# Author: Qian Zhu
# Singapore Airlines Analytics System
# Dashboard (Home Page) + CLI
# Course: CN6001 Enterprise Application & Cloud Computing
# ============================================

import sys
import logging

logging.basicConfig(level=logging.INFO)


# =============================================================
# STREAMLIT UI MODE
# =============================================================
def run_streamlit_ui():
    import streamlit as st
    from services.ui_service import apply_global_styles

    st.set_page_config(
        page_title="Singapore Airlines Analytics System",
        page_icon="✈️",
        layout="wide"
    )

    apply_global_styles()

    # =====================================================
    # HERO SECTION WITH VIDEO BACKGROUND
    # =====================================================
    st.markdown(
        """
        <div style="
            position:relative;
            width:100%;
            height:420px;
            overflow:hidden;
            border-radius:22px;
            margin-bottom:3rem;
            box-shadow:0 12px 35px rgba(0,0,0,0.35);
        ">

            <!-- Video Background -->
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

            <!-- Overlay -->
            <div style="
                position:absolute;
                inset:0;
                background:linear-gradient(
                    135deg,
                    rgba(0,26,77,0.88) 0%,
                    rgba(0,58,128,0.80) 100%
                );
            "></div>

            <!-- Text Content -->
            <div style="
                position:relative;
                z-index:2;
                padding:3.8rem;
            ">
                <h1 style="
                    font-size:3.4rem;
                    font-weight:900;
                    letter-spacing:-1px;
                    color:white;
                    margin-bottom:0.6rem;
                ">
                    Singapore Airlines Analytics System
                </h1>

                <p style="
                    font-size:1.2rem;
                    color:#E5E7EB;
                    max-width:720px;
                ">
                    Enterprise Cloud-Based Analytics Dashboard
                </p>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # MODULE SECTION
    # =====================================================
    st.markdown(
        """
        <h2 style="
            font-size:2.2rem;
            font-weight:800;
            color:#002663;
            margin-bottom:1.8rem;
        ">
            📊 Analytics Modules
        </h2>
        """,
        unsafe_allow_html=True
    )

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
            "Operational risk modelling and scenario-based simulations.",
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
            "Cloud-style batch and streaming analytics demonstrations.",
            "pages/Module4_Cloud_Analytics.py"
        )

    st.info("Use the sidebar or click a module card to navigate.")


# =============================================================
# CLI MODE
# =============================================================
def run_cli():
    from pages.Module1_Flight_Performance import run_flight_performance_cli
    from pages.Module2_Customer_Experience import run_customer_experience_cli

    print("===========================================")
    print(" Singapore Airlines Analytics System (CLI)")
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
            print("\nRisk & Scenario Simulation is visualization-focused.")
            input("Press ENTER to return to menu...")

        elif choice == "4":
            print("\nCloud Analytics is visualization-focused.")
            input("Press ENTER to return to menu...")

        elif choice == "5":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")
            input("Press ENTER to continue...")


# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
