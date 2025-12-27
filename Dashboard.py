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
    import streamlit as st
    from services.ui_service import apply_global_styles

    st.set_page_config(
        page_title="SIA Dashboard",
        page_icon="🏠",
        layout="wide"
    )

    apply_global_styles()

    # ---------- Theme helpers ----------
    PRIMARY_NAVY = "#001A4D"
    SECONDARY_NAVY = "#003A80"
    GOLD = "#FFED4D"
    BG = "#F5F3EE"

    st.markdown(
        f"""
        <style>
            .stApp {{
                background-color: {BG};
            }}

            .section-h2 {{
                font-size: 2.2rem;
                font-weight: 900;
                color: {PRIMARY_NAVY};
                margin: 0.3rem 0 1.1rem 0;
                letter-spacing: -0.5px;
            }}

            .muted {{
                color: rgba(0,0,0,0.65);
                font-size: 1.05rem;
                line-height: 1.6;
            }}

            .pill {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 8px 14px;
                border-radius: 999px;
                background: rgba(255,255,255,0.16);
                border: 1px solid rgba(255,255,255,0.18);
                color: rgba(255,255,255,0.92);
                font-weight: 700;
                font-size: 0.95rem;
                backdrop-filter: blur(8px);
            }}

            .pill.gold {{
                background: rgba(255, 237, 77, 0.18);
                border: 1px solid rgba(255, 237, 77, 0.28);
                color: rgba(255,255,255,0.95);
            }}

            .grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 18px;
                margin-top: 6px;
            }}

            .cardLink {{
                text-decoration: none !important;
                color: inherit !important;
            }}

            .moduleCard {{
                position: relative;
                border-radius: 22px;
                overflow: hidden;
                min-height: 210px;
                box-shadow: 0 12px 40px rgba(0,0,0,0.12);
                border: 1px solid rgba(0,0,0,0.06);
                background: #ffffff;
                transition: transform 140ms ease, box-shadow 140ms ease;
            }}

            .moduleCard:hover {{
                transform: translateY(-2px);
                box-shadow: 0 16px 55px rgba(0,0,0,0.16);
            }}

            .moduleBg {{
                position: absolute;
                inset: 0;
                background-size: cover;
                background-position: center;
                filter: saturate(1.05);
                transform: scale(1.02);
            }}

            .moduleOverlay {{
                position: absolute;
                inset: 0;
                background: linear-gradient(
                    135deg,
                    rgba(0, 26, 77, 0.88) 0%,
                    rgba(0, 58, 128, 0.72) 55%,
                    rgba(0, 26, 77, 0.40) 100%
                );
            }}

            .moduleInner {{
                position: relative;
                padding: 18px 18px 16px 18px;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }}

            .moduleTitleRow {{
                display: flex;
                align-items: center;
                gap: 10px;
                color: white;
                font-weight: 900;
                font-size: 1.35rem;
                letter-spacing: -0.4px;
            }}

            .moduleDesc {{
                margin-top: 10px;
                color: rgba(255,255,255,0.88);
                font-size: 1.02rem;
                line-height: 1.55;
                max-width: 92%;
            }}

            .ctaRow {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-top: 14px;
            }}

            .ctaBtn {{
                display: inline-flex;
                align-items: center;
                gap: 10px;
                padding: 10px 14px;
                border-radius: 12px;
                background: rgba(255,255,255,0.16);
                border: 1px solid rgba(255,255,255,0.22);
                color: rgba(255,255,255,0.95);
                font-weight: 800;
                font-size: 0.98rem;
                backdrop-filter: blur(10px);
            }}

            .ctaHint {{
                color: rgba(255,255,255,0.78);
                font-size: 0.95rem;
                font-weight: 700;
            }}

            .infoGrid {{
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 14px;
                margin-top: 10px;
            }}

            .infoCard {{
                background: rgba(255,255,255,0.90);
                border: 1px solid rgba(0,0,0,0.06);
                border-radius: 18px;
                padding: 14px 14px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.06);
            }}

            .infoTitle {{
                font-weight: 900;
                color: {PRIMARY_NAVY};
                font-size: 1.08rem;
                margin-bottom: 6px;
            }}

            .infoText {{
                color: rgba(0,0,0,0.70);
                font-size: 0.98rem;
                line-height: 1.55;
            }}

            .footer {{
                margin-top: 26px;
                padding: 16px 0 6px 0;
                color: rgba(0,0,0,0.55);
                font-size: 0.95rem;
            }}

            @media (max-width: 980px) {{
                .grid {{
                    grid-template-columns: 1fr;
                }}
                .infoGrid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # ======================
    # HERO SECTION
    # ======================
    st.markdown(
        """
        <div style="
            position: relative;
            background: linear-gradient(135deg, #001A4D 0%, #003A80 100%);
            padding: 3.2rem;
            border-radius: 22px;
            margin-bottom: 1.6rem;
            box-shadow: 0 14px 45px rgba(0,0,0,0.25);
            overflow: hidden;
        ">
            <div style="
                position:absolute;
                right: -120px;
                top: -120px;
                width: 340px;
                height: 340px;
                background: rgba(255,255,255,0.08);
                border-radius: 999px;
            "></div>

            <div style="
                position:absolute;
                right: 40px;
                bottom: -140px;
                width: 340px;
                height: 340px;
                background: rgba(255,255,255,0.06);
                border-radius: 999px;
            "></div>

            <div style="display:flex; align-items:flex-start; gap:18px; flex-wrap:wrap;">
                <div style="
                    background: rgba(255,255,255,0.92);
                    border-radius: 16px;
                    padding: 10px 12px;
                    display:flex;
                    align-items:center;
                    gap:12px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
                ">
                    <img src="assets/singapore_airlines_logo.png" style="height:64px; width:auto;" />
                </div>

                <div style="flex: 1; min-width: 280px;">
                    <h1 style="
                        font-size: 3.15rem;
                        font-weight: 950;
                        letter-spacing: -1px;
                        margin: 0 0 0.65rem 0;
                        color: white;
                        line-height: 1.05;
                    ">
                        Singapore Airlines Analytics System
                    </h1>

                    <p style="
                        color: rgba(255,255,255,0.88);
                        font-size: 1.15rem;
                        margin: 0 0 1.25rem 0;
                        max-width: 980px;
                        line-height: 1.6;
                    ">
                        Enterprise cloud-based analytics dashboard for operational performance, customer experience,
                        risk scenarios, and cloud processing concepts.
                    </p>

                    <div style="display:flex; gap:10px; flex-wrap:wrap;">
                        <span class="pill gold">✅ Streamlit UI</span>
                        <span class="pill">🧾 CLI Supported</span>
                        <span class="pill">📦 Synthetic Dataset (train.csv)</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================
    # QUICK ORIENTATION (NEW SECTION)
    # ======================
    st.markdown('<div class="section-h2">What you can do here</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="muted" style="max-width: 1050px; margin-bottom: 0.6rem;">
            This system demonstrates how an airline can use analytics to understand performance, customer experience,
            operational risk, and cloud-style processing. Each module focuses on a different business question and
            produces charts, KPIs, and decision support insights.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="infoGrid">
            <div class="infoCard">
                <div class="infoTitle">Operational performance</div>
                <div class="infoText">Delay patterns, distance trends, crew/service indicators, and estimated fuel analytics.</div>
            </div>
            <div class="infoCard">
                <div class="infoTitle">Customer experience</div>
                <div class="infoText">Satisfaction distribution, service ratings, and areas for service improvement.</div>
            </div>
            <div class="infoCard">
                <div class="infoTitle">Risk + cloud concepts</div>
                <div class="infoText">Disruption simulation, uncertainty modelling, batch vs streaming processing demonstrations.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================
    # ANALYTICS MODULES (UPGRADED CARDS WITH IMAGES)
    # ======================
    st.markdown('<div class="section-h2" style="margin-top: 22px;">📊 Analytics Modules</div>', unsafe_allow_html=True)

    def module_card(icon, title, desc, link, image_path):
        st.markdown(
            f"""
            <a class="cardLink" href="/{link}" target="_self">
                <div class="moduleCard">
                    <div class="moduleBg" style="background-image:url('{image_path}');"></div>
                    <div class="moduleOverlay"></div>

                    <div class="moduleInner">
                        <div>
                            <div class="moduleTitleRow">
                                <span style="font-size:1.35rem;">{icon}</span>
                                <span>{title}</span>
                            </div>
                            <div class="moduleDesc">{desc}</div>
                        </div>

                        <div class="ctaRow">
                            <span class="ctaBtn">Open module →</span>
                            <span class="ctaHint">Interactive KPIs & charts</span>
                        </div>
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="grid">', unsafe_allow_html=True)

    module_card(
        "✈️",
        "Flight Performance Analytics",
        "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage patterns.",
        "pages/Module1_Flight_Performance.py",
        "assets/card_flight.jpg",
    )

    module_card(
        "😊",
        "Customer Experience Analytics",
        "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
        "pages/Module2_Customer_Experience.py",
        "assets/card_customer.jpg",
    )

    module_card(
        "⚠️",
        "Risk & Scenario Simulation",
        "Model operational uncertainty with disruption scenarios and simulated delay risk indicators.",
        "pages/Module3_Risk_Simulation.py",
        "assets/card_risk.jpg",
    )

    module_card(
        "☁️",
        "Cloud Analytics",
        "Demonstrate batch vs streaming concepts and scalable analytics patterns used in cloud environments.",
        "pages/Module4_Cloud_Analytics.py",
        "assets/card_cloud.jpg",
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ======================
    # HOW IT WORKS (NEW SECTION)
    # ======================
    st.markdown('<div class="section-h2" style="margin-top: 22px;">How the system works</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="infoGrid">
            <div class="infoCard">
                <div class="infoTitle">1) Data ingestion</div>
                <div class="infoText">Load the synthetic dataset (train.csv) and prepare key fields for analysis.</div>
            </div>
            <div class="infoCard">
                <div class="infoTitle">2) Processing</div>
                <div class="infoText">Compute KPIs, group trends, and run simulations where real data is unavailable.</div>
            </div>
            <div class="infoCard">
                <div class="infoTitle">3) Visualisation</div>
                <div class="infoText">Present results via charts and KPI cards for interpretation and decision support.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================
    # DATASET & ASSUMPTIONS (NEW SECTION)
    # ======================
    st.markdown('<div class="section-h2" style="margin-top: 22px;">Dataset and assumptions</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="muted" style="max-width: 1050px;">
            Real airline operational datasets are confidential. This project uses a synthetic dataset to demonstrate an end-to-end analytics pipeline.
            When specific operational metrics are unavailable, controlled simulations are used and clearly labelled within modules.
        </div>
        """,
        unsafe_allow_html=True
    )

    # Optional: show a tiny dataset snapshot if services.data_service exists
    try:
        from services.data_service import load_data
        df = load_data()
        with st.expander("View dataset snapshot"):
            st.dataframe(df.head(10), use_container_width=True)
    except Exception:
        pass

    # ======================
    # FOOTER (NEW SECTION)
    # ======================
    st.markdown(
        """
        <div class="footer">
            Developed for CN6001 Enterprise Application & Cloud Computing (academic prototype).
        </div>
        """,
        unsafe_allow_html=True
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


# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
