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

    # ---------- Helper: ensure assets exist ----------
    def _asset_exists(path: str) -> bool:
        try:
            import os
            return os.path.exists(path)
        except Exception:
            return False

    # ---------- Dashboard CSS ----------
    st.markdown(
        """
        <style>
        .heroWrap{
          position:relative;
          height:420px;
          border-radius:26px;
          overflow:hidden;
          margin: 8px 0 44px 0;
          box-shadow: 0 18px 45px rgba(0,0,0,0.28);
        }
        .heroVideo{
          width:100%;
          height:100%;
          object-fit:cover;
          display:block;
          transform: scale(1.02);
          filter:saturate(1.05) contrast(1.02);
        }
        .heroOverlay{
          position:absolute;
          inset:0;
          background: linear-gradient(135deg, rgba(0,26,77,0.88) 0%, rgba(0,58,128,0.74) 100%);
        }
        .heroInner{
          position:absolute;
          inset:0;
          padding: 44px 44px;
          color: white;
          display:flex;
          flex-direction:column;
          justify-content:center;
        }
        .logoChip{
          background: rgba(255,255,255,0.92);
          border-radius: 18px;
          padding: 10px 12px;
          display:inline-flex;
          align-items:center;
          gap: 10px;
          width: fit-content;
          box-shadow: 0 10px 30px rgba(0,0,0,0.18);
          margin-bottom: 18px;
        }
        .heroTitle{
          font-size: 3.1rem;
          font-weight: 950;
          letter-spacing: -1px;
          margin: 0 0 8px 0;
          line-height: 1.05;
          text-shadow: 0 8px 30px rgba(0,0,0,0.35);
        }
        .heroSub{
          font-size: 1.15rem;
          color: rgba(255,255,255,0.92);
          max-width: 980px;
          margin: 0 0 18px 0;
          line-height: 1.35;
        }
        .tagRow{
          display:flex;
          gap: 10px;
          flex-wrap: wrap;
          margin-top: 6px;
        }
        .tagPill{
          display:inline-flex;
          align-items:center;
          gap: 8px;
          padding: 8px 12px;
          border-radius: 999px;
          background: rgba(255,255,255,0.14);
          border: 1px solid rgba(255,255,255,0.22);
          color: rgba(255,255,255,0.92);
          font-weight: 700;
          font-size: 0.92rem;
        }
        .tagDot{
          width:10px;
          height:10px;
          border-radius: 999px;
          background: rgba(255,237,77,0.95);
          box-shadow: 0 0 0 3px rgba(255,237,77,0.18);
        }

        .sectionTitle{
          font-size: 2.2rem;
          font-weight: 950;
          color: #0b2b5f;
          margin: 8px 0 12px 0;
          display:flex;
          align-items:center;
          gap: 12px;
        }
        .sectionHint{
          color:#5b6472;
          font-size: 1.02rem;
          margin-bottom: 16px;
        }

        .moduleGrid{
          display:grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 18px;
          margin-top: 12px;
        }
        @media (max-width: 980px){
          .moduleGrid{ grid-template-columns: 1fr; }
          .heroWrap{ height: 460px; }
          .heroInner{ padding: 34px 22px; }
          .heroTitle{ font-size: 2.4rem; }
        }

        .moduleCard{
          background: rgba(255,255,255,0.96);
          border: 1px solid rgba(17,24,39,0.08);
          border-radius: 22px;
          overflow:hidden;
          box-shadow: 0 10px 30px rgba(0,0,0,0.08);
          transition: transform 160ms ease, box-shadow 160ms ease;
        }
        .moduleCard:hover{
          transform: translateY(-2px);
          box-shadow: 0 18px 45px rgba(0,0,0,0.14);
        }
        .thumb{
          width:100%;
          height:180px;
          object-fit: cover;
          display:block;
          filter: saturate(1.05) contrast(1.02);
        }
        .moduleInner{
          padding: 18px 18px 16px 18px;
        }
        .moduleTitleRow{
          display:flex;
          align-items:center;
          gap: 10px;
          font-size: 1.35rem;
          font-weight: 950;
          color: #0b2b5f;
          margin-bottom: 8px;
        }
        .moduleDesc{
          color:#5b6472;
          font-size: 1.02rem;
          line-height: 1.35;
          margin-bottom: 12px;
        }
        .ctaRow{
          display:flex;
          align-items:center;
          justify-content: space-between;
          gap: 12px;
          flex-wrap: wrap;
        }
        .ctaBtn{
          display:inline-flex;
          align-items:center;
          gap: 10px;
          padding: 10px 14px;
          border-radius: 999px;
          background: #0b2b5f;
          color: white;
          font-weight: 900;
          text-decoration: none;
          border: 1px solid rgba(0,0,0,0.06);
        }
        .ctaBtn:hover{ opacity: 0.96; }
        .ctaHint{
          color:#0b2b5f;
          background: rgba(255,237,77,0.28);
          border: 1px solid rgba(255,237,77,0.40);
          font-weight: 900;
          border-radius: 999px;
          padding: 8px 12px;
          font-size: 0.9rem;
        }

        .infoGrid{
          display:grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 18px;
          margin-top: 18px;
          margin-bottom: 6px;
        }
        @media (max-width: 980px){
          .infoGrid{ grid-template-columns: 1fr; }
        }
        .infoCard{
          background: rgba(255,255,255,0.96);
          border: 1px solid rgba(17,24,39,0.08);
          border-radius: 22px;
          padding: 18px;
          box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        }
        .infoCard h3{
          margin: 0 0 10px 0;
          color:#0b2b5f;
          font-size: 1.35rem;
          font-weight: 950;
        }
        .infoCard ul{
          margin: 0;
          padding-left: 18px;
          color:#5b6472;
          font-size: 1.02rem;
          line-height: 1.55;
        }
        code.badge{
          background: rgba(17,24,39,0.92);
          color: #D1FAE5;
          padding: 2px 8px;
          border-radius: 8px;
          font-weight: 900;
          font-size: 0.95rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- HERO (video if exists, else gradient image fallback) ----------
    hero_video_path = "assets/hero.mp4"
    logo_path = "assets/singapore_airlines_logo.png"

    if _asset_exists(hero_video_path):
        hero_bg = f"""
        <video autoplay muted loop playsinline class="heroVideo">
          <source src="{hero_video_path}" type="video/mp4">
        </video>
        """
    else:
        hero_bg = """
        <div style="position:absolute; inset:0; background: radial-gradient(circle at 20% 20%, rgba(255,255,255,0.10), rgba(255,255,255,0.0) 45%),
                                     linear-gradient(135deg, #001A4D 0%, #003A80 100%);">
        </div>
        """

    logo_html = ""
    if _asset_exists(logo_path):
        logo_html = f'<div class="logoChip"><img src="{logo_path}" style="height:64px; width:auto;" alt="Singapore Airlines logo"></div>'

    st.markdown(
        f"""
        <div class="heroWrap">
          {hero_bg}
          <div class="heroOverlay"></div>

          <div class="heroInner">
            {logo_html}

            <div class="heroTitle">Singapore Airlines Analytics System</div>
            <div class="heroSub">
              Enterprise cloud-based analytics dashboard for operational performance, customer experience,
              risk scenarios, and cloud processing concepts.
            </div>

            <div class="tagRow">
              <span class="tagPill"><span class="tagDot"></span>Streamlit UI</span>
              <span class="tagPill"><span class="tagDot"></span>CLI Supported</span>
              <span class="tagPill"><span class="tagDot"></span>Synthetic Dataset (train.csv)</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- What this dashboard does ----------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionHint">Open a module to explore analytics, simulations, and cloud processing concepts using a shared dataset and consistent UI theme.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="infoGrid">
          <div class="infoCard">
            <h3>How to use</h3>
            <ul>
              <li>Start on this dashboard and open a module using the cards below.</li>
              <li>Use sliders/filters inside modules to explore different operating conditions.</li>
              <li>Risk Simulation demonstrates uncertainty (probabilities, percentiles, worst-case outcomes).</li>
              <li>Cloud Analytics explains how analytics workloads run at scale (batch vs streaming).</li>
            </ul>
          </div>

          <div class="infoCard">
            <h3>Data & concepts</h3>
            <ul>
              <li><strong>Dataset:</strong> synthetic <code class="badge">assets/train.csv</code> (academic use only).</li>
              <li><strong>Assumptions:</strong> when a metric is missing (e.g., fuel cost), controlled simulation is used.</li>
              <li><strong>Cloud concepts:</strong> modular pages, shared services, scalable processing patterns.</li>
              <li><strong>UI/CLI:</strong> Streamlit web UI plus a menu-driven CLI for quick summaries.</li>
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- Modules ----------
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown('<div class="sectionHint">Click “Open module” to navigate. Each module uses the same theme and dataset service.</div>', unsafe_allow_html=True)

    # Update these if your asset filenames differ:
    module_assets = {
        "module1": "assets/module1.jpg",
        "module2": "assets/module2.jpg",
        "module3": "assets/module3.jpg",
        "module4": "assets/module4.jpg",
    }

    def module_card_html(icon, title, desc, hint, page_path, thumb_path):
        thumb_html = ""
        if _asset_exists(thumb_path):
            thumb_html = f'<img class="thumb" src="{thumb_path}" alt="{title} thumbnail">'
        else:
            thumb_html = """
            <div style="height:180px; background:linear-gradient(135deg,#001A4D,#003A80);"></div>
            """

        return f"""
        <div class="moduleCard">
          {thumb_html}
          <div class="moduleInner">
            <div class="moduleTitleRow"><span style="font-size:1.35rem;">{icon}</span><span>{title}</span></div>
            <div class="moduleDesc">{desc}</div>
            <div class="ctaRow">
              <a class="ctaBtn" href="/{page_path}" target="_self">Open module →</a>
              <span class="ctaHint">{hint}</span>
            </div>
          </div>
        </div>
        """

    modules_html = """
    <div class="moduleGrid">
    """ + \
    module_card_html(
        "✈️",
        "Flight Performance Analytics",
        "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
        "Interactive KPIs & charts",
        "pages/Module1_Flight_Performance.py",
        module_assets["module1"]
    ) + \
    module_card_html(
        "😊",
        "Customer Experience Analytics",
        "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
        "Service quality insights",
        "pages/Module2_Customer_Experience.py",
        module_assets["module2"]
    ) + \
    module_card_html(
        "⚠️",
        "Risk & Scenario Simulation",
        "Model operational uncertainty using simulation and disruption scenarios to quantify delay risk and volatility.",
        "Risk simulation & percentiles",
        "pages/Module3_Risk_Simulation.py",
        module_assets["module3"]
    ) + \
    module_card_html(
        "☁️",
        "Cloud Analytics",
        "Demonstrate scalable processing concepts and cloud execution patterns, including batch vs streaming analytics.",
        "Scalable processing concepts",
        "pages/Module4_Cloud_Analytics.py",
        module_assets["module4"]
    ) + \
    """
    </div>
    """

    st.markdown(modules_html, unsafe_allow_html=True)

    st.info("Tip: Use the sidebar at any time to jump between pages.")


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
            print("\n[CLI] Risk Simulation is visualization-focused.")
            print("Please use Streamlit UI for full functionality.")
            input("\nPress ENTER to return to menu...")

        elif choice == "4":
            print("\n[CLI] Cloud Analytics demonstrates cloud execution patterns.")
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
    # CLI MODE
    # Usage: python3 Dashboard.py cli
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    # STREAMLIT UI MODE
    # Usage: streamlit run Dashboard.py
    else:
        run_streamlit_ui()
