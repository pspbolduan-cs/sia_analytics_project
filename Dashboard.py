# ============================================
# Author: Qian Zhu
# Date: 2025-12
# Singapore Airlines Analytics System
# Dashboard (Home Page) + CLI
# ============================================

import sys
import logging
from pathlib import Path
from textwrap import dedent

logging.basicConfig(level=logging.INFO)


# =============================================================
# STREAMLIT UI MODE
# =============================================================
def run_streamlit_ui():
    import streamlit as st
    import base64

    # Optional global styles (won't crash if missing)
    try:
        from services.ui_service import apply_global_styles
    except Exception:
        apply_global_styles = None

    st.set_page_config(page_title="SIA Dashboard", page_icon="🏠", layout="wide")

    if apply_global_styles:
        try:
            apply_global_styles()
        except Exception:
            pass

    # ---------------------------------------------------
    # ABSOLUTE ASSET PATHS
    # ---------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent
    ASSETS_DIR = BASE_DIR / "assets"

    HERO_VIDEO_PATH = ASSETS_DIR / "hero.mp4"
    LOGO_PATH = ASSETS_DIR / "singapore_airlines_logo.png"

    MODULE_1_PATH = ASSETS_DIR / "module1.png"
    MODULE_2_PATH = ASSETS_DIR / "module2.png"
    MODULE_3_PATH = ASSETS_DIR / "module3.png"
    MODULE_4_PATH = ASSETS_DIR / "module4.png"

    # ✅ NEW SYSTEM PAGE THUMBNAILS
    SYSTEM_OVERVIEW_IMG = ASSETS_DIR / "system_overview.png"
    SECURITY_RISK_ETHICS_IMG = ASSETS_DIR / "security_risk_ethics.png"

    def _mime_for_image(p: Path) -> str:
        s = p.suffix.lower()
        if s == ".png":
            return "image/png"
        if s in [".jpg", ".jpeg"]:
            return "image/jpeg"
        if s == ".webp":
            return "image/webp"
        return "image/png"

    def _to_data_uri(p: Path, mime: str) -> str:
        if not p.exists():
            return ""
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{b64}"

    hero_video_uri = _to_data_uri(HERO_VIDEO_PATH, "video/mp4")
    logo_uri = _to_data_uri(LOGO_PATH, _mime_for_image(LOGO_PATH))

    m1_uri = _to_data_uri(MODULE_1_PATH, _mime_for_image(MODULE_1_PATH))
    m2_uri = _to_data_uri(MODULE_2_PATH, _mime_for_image(MODULE_2_PATH))
    m3_uri = _to_data_uri(MODULE_3_PATH, _mime_for_image(MODULE_3_PATH))
    m4_uri = _to_data_uri(MODULE_4_PATH, _mime_for_image(MODULE_4_PATH))

    sys_overview_uri = _to_data_uri(SYSTEM_OVERVIEW_IMG, _mime_for_image(SYSTEM_OVERVIEW_IMG))
    sec_risk_uri = _to_data_uri(SECURITY_RISK_ETHICS_IMG, _mime_for_image(SECURITY_RISK_ETHICS_IMG))

    # ---------------------------------------------------
    # NAVIGATION (Streamlit multipage-safe)
    # ---------------------------------------------------
    def go_page(page_file: str):
        """
        Navigate to a Streamlit multipage file inside /pages.
        Uses st.switch_page when available; otherwise falls back to st.page_link UI.
        """
        try:
            st.switch_page(f"pages/{page_file}")
        except Exception:
            st.warning("Navigation not supported in this Streamlit version. Use the left sidebar to open the page.")

    # ---------------------------------------------------
    # CSS
    # ---------------------------------------------------
    st.markdown(
        dedent(
            """
            <style>
              .block-container { padding-top: 1.2rem !important; }

              /* HERO */
              .heroWrap{
                position: relative;
                border-radius: 26px;
                overflow: hidden;
                margin-bottom: 2.2rem;
                box-shadow: 0 18px 45px rgba(0,0,0,0.22);
                border: 1px solid rgba(255,255,255,0.10);
                min-height: 390px;
              }
              .heroVideo{
                position:absolute; inset:0;
                width:100%; height:100%;
                object-fit:cover;
                opacity:0.85;
                z-index:0;
              }
              .heroOverlay{
                position:absolute; inset:0;
                background: linear-gradient(135deg,
                  rgba(0,26,77,0.92) 0%,
                  rgba(0,58,128,0.70) 45%,
                  rgba(0,26,77,0.92) 100%);
                z-index:1;
              }
              .heroInner{
                position:relative;
                z-index:2;
                padding: 2.2rem 2.4rem;
                display:flex;
                gap: 22px;
                align-items:flex-start;
                flex-wrap: wrap;
              }
              .logoChip{
                background: rgba(255,255,255,0.92);
                border-radius: 18px;
                padding: 12px 14px;
                box-shadow: 0 12px 35px rgba(0,0,0,0.18);
                border: 1px solid rgba(255,255,255,0.45);
                display:flex;
                align-items:center;
                justify-content:center;
              }
              .logoChip img{ height: 64px; width:auto; display:block; }

              .tagRow{ display:flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
              .tagPill{
                display:inline-flex; align-items:center; gap:8px;
                padding: 9px 12px;
                border-radius: 999px;
                background: rgba(255,255,255,0.14);
                border: 1px solid rgba(255,255,255,0.22);
                color: rgba(255,255,255,0.92);
                font-weight: 800;
                font-size: 0.95rem;
                backdrop-filter: blur(6px);
              }
              .tagDot{ width: 10px; height: 10px; border-radius: 999px; background: rgba(255,255,255,0.75); display:inline-block; }
              .kbd{
                padding: 2px 8px;
                border-radius: 10px;
                background: rgba(0,0,0,0.22);
                border: 1px solid rgba(255,255,255,0.16);
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
                font-weight: 800;
              }

              .sectionTitle{
                font-size: 2.2rem;
                font-weight: 950;
                letter-spacing: -0.5px;
                margin: 0 0 0.3rem 0;
                color: #0b2c5f;
              }
              .sectionSub{
                color: rgba(0,0,0,0.60);
                font-size: 1.05rem;
                margin-bottom: 1.1rem;
              }

              .cardGrid{
                display:grid;
                grid-template-columns: 1fr 1fr;
                gap: 18px;
              }
              @media (max-width: 980px){
                .cardGrid{ grid-template-columns: 1fr; }
              }

              .moduleCard{
                background: #0f172a;
                border-radius: 22px;
                overflow:hidden;
                border: 1px solid rgba(255,255,255,0.10);
                box-shadow: 0 18px 45px rgba(0,0,0,0.18);
              }
              .thumbWrap{
                height: 210px;
                width: 100%;
                position: relative;
                overflow: hidden;
              }
              .thumbWrap img{
                width:100%;
                height:100%;
                object-fit: cover;
                display:block;
              }
              .thumbShade{
                position:absolute;
                inset:0;
                background: linear-gradient(180deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.25) 100%);
              }

              .moduleInner{
                padding: 16px 18px 18px 18px;
                color: rgba(255,255,255,0.92);
              }
              .moduleTitleRow{
                display:flex;
                align-items:center;
                gap: 10px;
                font-size: 1.28rem;
                font-weight: 950;
                margin-bottom: 6px;
              }
              .moduleDesc{
                color: rgba(255,255,255,0.74);
                font-size: 1.02rem;
                line-height: 1.45;
                margin-bottom: 14px;
              }

              /* Make Streamlit buttons look like your CTA */
              div[data-testid="stButton"] > button{
                width: 100%;
                border-radius: 14px !important;
                padding: 12px 14px !important;
                font-weight: 900 !important;
                border: 1px solid rgba(255,255,255,0.20) !important;
                background: rgba(255,255,255,0.14) !important;
                color: rgba(255,255,255,0.95) !important;
              }
              div[data-testid="stButton"] > button:hover{
                background: rgba(255,255,255,0.18) !important;
              }

              .hintRight{
                text-align:right;
                color: rgba(255,255,255,0.70);
                font-weight: 800;
                padding-top: 12px;
              }

              .infoCard{
                background: #ffffff;
                border-radius: 18px;
                padding: 16px 18px;
                border: 1px solid rgba(0,0,0,0.06);
                box-shadow: 0 12px 35px rgba(0,0,0,0.08);
                margin-top: 18px;
              }
              .infoCard h3{
                margin: 0 0 8px 0;
                font-size: 1.25rem;
                font-weight: 950;
                color: #0b2c5f;
              }
              .infoCard ul{
                margin: 0;
                padding-left: 18px;
                color: rgba(0,0,0,0.70);
                font-size: 1.02rem;
                line-height: 1.55;
              }
            </style>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # HERO
    # ---------------------------------------------------
    video_block = ""
    if hero_video_uri:
        video_block = dedent(
            f"""
            <video class="heroVideo" autoplay muted loop playsinline>
              <source src="{hero_video_uri}" type="video/mp4" />
            </video>
            """
        )

    logo_block = ""
    if logo_uri:
        logo_block = dedent(
            f"""
            <div class="logoChip">
              <img src="{logo_uri}" alt="Singapore Airlines logo">
            </div>
            """
        )

    st.markdown(
        dedent(
            f"""
            <div class="heroWrap">
              {video_block}
              <div class="heroOverlay"></div>

              <div class="heroInner">
                {logo_block}

                <div style="flex:1; min-width: 280px;">
                  <div style="
                    font-size:3.1rem;
                    font-weight:950;
                    letter-spacing:-1px;
                    color:#ffffff;
                    line-height:1.05;
                    margin:0.15rem 0 0.55rem 0;
                  ">
                    Singapore Airlines Analytics System
                  </div>

                  <div style="
                    color:rgba(255,255,255,0.88);
                    font-size:1.18rem;
                    max-width:980px;
                    margin:0 0 1.05rem 0;
                  ">
                    Enterprise cloud-based analytics dashboard for operational performance, customer experience,
                    risk scenarios, and cloud processing concepts.
                  </div>

                  <div class="tagRow">
                    <span class="tagPill"><span class="tagDot"></span>Streamlit UI</span>
                    <span class="tagPill"><span class="tagDot"></span>CLI supported</span>
                    <span class="tagPill"><span class="tagDot"></span>Synthetic dataset: <span class="kbd">assets/train.csv</span></span>
                  </div>

                  {"<div style='margin-top:12px; color:rgba(255,255,255,0.90); font-weight:900;'>⚠️ Video not found: <span class='kbd'>assets/hero.mp4</span></div>" if not hero_video_uri else ""}
                  {"<div style='margin-top:8px; color:rgba(255,255,255,0.90); font-weight:900;'>⚠️ Logo not found: <span class='kbd'>assets/singapore_airlines_logo.png</span></div>" if not logo_uri else ""}
                </div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # WHAT THIS DASHBOARD DOES
    # ---------------------------------------------------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">A single entry point that explains the system and links to analytics modules built on the same dataset + shared services.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="infoCard">
              <h3>How to use</h3>
              <ul>
                <li>Start here and open a module using <b>Open module</b>.</li>
                <li>Each module offers interactive controls (filters/sliders) + charts.</li>
                <li>Risk Simulation explains uncertainty (probability, percentiles, worst-case).</li>
                <li>Cloud Analytics demonstrates scalable processing concepts (batch vs streaming).</li>
              </ul>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="infoCard">
              <h3>Data & concepts</h3>
              <ul>
                <li><b>Dataset:</b> synthetic <span class="kbd">assets/train.csv</span> (academic use).</li>
                <li><b>Assumptions:</b> controlled simulation is used where metrics are missing.</li>
                <li><b>Architecture:</b> modular pages + shared services (data / UI helpers).</li>
                <li><b>UI + CLI:</b> web UI for visuals + menu-driven CLI for quick summaries.</li>
              </ul>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # SYSTEM PAGES (NEW)
    # ---------------------------------------------------
    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sectionTitle">🧩 System Pages</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">These pages strengthen enterprise design + governance criteria (architecture, security, risk & ethics).</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="cardGrid">', unsafe_allow_html=True)

    # Card 1
    st.markdown(
        dedent(
            f"""
            <div class="moduleCard">
              <div class="thumbWrap">
                {f"<img src='{sys_overview_uri}' alt='System Overview / Architecture'>" if sys_overview_uri else ""}
                <div class="thumbShade"></div>
              </div>
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">🏗️</span><span>System Overview / Architecture</span></div>
                <div class="moduleDesc">View the system architecture, shared services, page structure, and cloud scalability mapping.</div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
    c1a, c1b = st.columns([1.1, 1])
    with c1a:
        if st.button("➡️ Open page →", key="open_sys_overview"):
            go_page("System_Overview_Architecture.py")
    with c1b:
        st.markdown('<div class="hintRight">Enterprise design + scalability</div>', unsafe_allow_html=True)

    # spacing between cards in grid visually
    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # Card 2
    st.markdown(
        dedent(
            f"""
            <div class="moduleCard">
              <div class="thumbWrap">
                {f"<img src='{sec_risk_uri}' alt='Security, Risk & Ethics'>" if sec_risk_uri else ""}
                <div class="thumbShade"></div>
              </div>
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">🛡️</span><span>Security, Risk & Ethics</span></div>
                <div class="moduleDesc">Review privacy protections, governance assumptions, security controls, and ethical analytics considerations.</div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
    c2a, c2b = st.columns([1.1, 1])
    with c2a:
        if st.button("➡️ Open page →", key="open_security_risk"):
            go_page("Security_Risk_Ethics.py")
    with c2b:
        st.markdown('<div class="hintRight">LO6: protection + governance</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # ANALYTICS MODULES
    # ---------------------------------------------------
    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Click <b>Open module →</b> to navigate. Each module uses the same theme and dataset service.</div>',
        unsafe_allow_html=True,
    )

    # Module 1
    st.markdown(
        dedent(
            f"""
            <div class="moduleCard">
              <div class="thumbWrap">
                {f"<img src='{m1_uri}' alt='Flight Performance'>" if m1_uri else ""}
                <div class="thumbShade"></div>
              </div>
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">✈️</span><span>Flight Performance Analytics</span></div>
                <div class="moduleDesc">Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.</div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
    m1a, m1b = st.columns([1.1, 1])
    with m1a:
        if st.button("➡️ Open module →", key="open_m1"):
            go_page("Module1_Flight_Performance.py")
    with m1b:
        st.markdown('<div class="hintRight">Interactive KPIs & charts</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # Module 2
    st.markdown(
        dedent(
            f"""
            <div class="moduleCard">
              <div class="thumbWrap">
                {f"<img src='{m2_uri}' alt='Customer Experience'>" if m2_uri else ""}
                <div class="thumbShade"></div>
              </div>
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">😊</span><span>Customer Experience Analytics</span></div>
                <div class="moduleDesc">Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.</div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
    m2a, m2b = st.columns([1.1, 1])
    with m2a:
        if st.button("➡️ Open module →", key="open_m2"):
            go_page("Module2_Customer_Experience.py")
    with m2b:
        st.markdown('<div class="hintRight">Service quality insights</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # Module 3
    st.markdown(
        dedent(
            f"""
            <div class="moduleCard">
              <div class="thumbWrap">
                {f"<img src='{m3_uri}' alt='Risk Simulation'>" if m3_uri else ""}
                <div class="thumbShade"></div>
              </div>
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">⚠️</span><span>Risk & Scenario Simulation</span></div>
                <div class="moduleDesc">Model operational uncertainty using Monte Carlo simulation and scenario-based disruption controls.</div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
    m3a, m3b = st.columns([1.1, 1])
    with m3a:
        if st.button("➡️ Open module →", key="open_m3"):
            go_page("Module3_Risk_Simulation.py")
    with m3b:
        st.markdown('<div class="hintRight">Probabilities, percentiles, worst-case</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    # Module 4
    st.markdown(
        dedent(
            f"""
            <div class="moduleCard">
              <div class="thumbWrap">
                {f"<img src='{m4_uri}' alt='Cloud Analytics'>" if m4_uri else ""}
                <div class="thumbShade"></div>
              </div>
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">☁️</span><span>Cloud Analytics</span></div>
                <div class="moduleDesc">Demonstrate scalable processing concepts and cloud-oriented analytics patterns.</div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
    m4a, m4b = st.columns([1.1, 1])
    with m4a:
        if st.button("➡️ Open module →", key="open_m4"):
            go_page("Module4_Cloud_Analytics.py")
    with m4b:
        st.markdown('<div class="hintRight">Batch vs streaming + scaling</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    st.info("Tip: If an image/video is missing, confirm the filename and that it sits inside the /assets folder.")


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
            print("\n[CLI] Cloud Analytics module demonstrates cloud execution.")
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
