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
    from pathlib import Path

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
    # ASSET PATHS (Streamlit Cloud safe)
    # ---------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent
    ASSETS_DIR = BASE_DIR / "assets"

    HERO_VIDEO_PATH = ASSETS_DIR / "hero.mp4"
    LOGO_PATH = ASSETS_DIR / "singapore_airlines_logo.png"

    MODULE_1_PATH = ASSETS_DIR / "module1.png"
    MODULE_2_PATH = ASSETS_DIR / "module2.png"
    MODULE_3_PATH = ASSETS_DIR / "module3.png"
    MODULE_4_PATH = ASSETS_DIR / "module4.png"

    SYSTEM_OVERVIEW_PATH = ASSETS_DIR / "system_overview.png"
    SECURITY_RISK_ETHICS_PATH = ASSETS_DIR / "security_risk_ethics.png"

    def _exists(p: Path) -> bool:
        try:
            return p.exists() and p.is_file()
        except Exception:
            return False

    # ---------------------------------------------------
    # CSS (hero + module cards + clean layout)
    # NOTE: Buttons/links are Streamlit widgets (NOT HTML <a>),
    # so navigation works on Streamlit Cloud in the SAME TAB.
    # ---------------------------------------------------
    st.markdown(
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
          }
          .heroInner{
            padding: 1.2rem 1.3rem;
          }

          /* Cards */
          .cardShell{
            background: #0f172a;
            border-radius: 22px;
            overflow:hidden;
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 18px 45px rgba(0,0,0,0.18);
            margin-bottom: 18px;
          }
          .cardTop{
            height: 210px;
            overflow:hidden;
            background: rgba(255,255,255,0.06);
          }
          .cardTop img{
            width:100%;
            height:100%;
            object-fit: cover;
            display:block;
          }
          .cardBody{
            padding: 14px 16px 16px 16px;
            color: rgba(255,255,255,0.92);
          }
          .cardTitle{
            display:flex;
            align-items:center;
            gap: 10px;
            font-size: 1.28rem;
            font-weight: 950;
            margin-bottom: 6px;
          }
          .cardDesc{
            color: rgba(255,255,255,0.74);
            font-size: 1.02rem;
            line-height: 1.45;
            margin-bottom: 12px;
          }
          .cardHint{
            color: rgba(255,255,255,0.70);
            font-weight: 800;
            white-space: nowrap;
            font-size: 0.98rem;
          }

          /* Typography */
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

          /* Info cards */
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

          /* Make Streamlit buttons look like CTA */
          div.stButton > button {
            width: 100%;
            border-radius: 14px !important;
            padding: 10px 14px !important;
            font-weight: 900 !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # HERO (video + logo + title always visible)
    # Use Streamlit native st.video/st.image (Cloud-safe)
    # ---------------------------------------------------
    with st.container():
        st.markdown('<div class="heroWrap"><div class="heroInner">', unsafe_allow_html=True)

        top_left, top_right = st.columns([1, 3], vertical_alignment="top")

        with top_left:
            if _exists(LOGO_PATH):
                st.image(str(LOGO_PATH), width=140)
            else:
                st.warning("Logo not found: assets/singapore_airlines_logo.png")

        with top_right:
            st.markdown(
                """
                <div style="
                  font-size:3.1rem;
                  font-weight:950;
                  letter-spacing:-1px;
                  color:#0b2c5f;
                  line-height:1.05;
                  margin:0.15rem 0 0.55rem 0;
                ">
                  Singapore Airlines Analytics System
                </div>
                <div style="
                  color:rgba(0,0,0,0.70);
                  font-size:1.18rem;
                  max-width:980px;
                  margin:0 0 0.25rem 0;
                ">
                  Enterprise cloud-based analytics dashboard for operational performance, customer experience,
                  risk scenarios, and cloud processing concepts.
                </div>
                """,
                unsafe_allow_html=True,
            )

        if _exists(HERO_VIDEO_PATH):
            st.video(str(HERO_VIDEO_PATH), autoplay=True, loop=True, muted=True)
        else:
            st.warning("Video not found: assets/hero.mp4")

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # WHAT THIS DASHBOARD DOES
    # ---------------------------------------------------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">A single entry point that explains the system and links to analytics modules and enterprise system pages.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="infoCard">
          <h3>How to use</h3>
          <ul>
            <li>Open a module using <b>Open module</b> or open a governance page using <b>Open page</b>.</li>
            <li>Each module offers interactive controls (filters/sliders) + charts.</li>
            <li>Risk Simulation explains uncertainty (probability, percentiles, worst-case).</li>
            <li>Cloud Analytics demonstrates scalable processing concepts (batch vs streaming).</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="infoCard">
          <h3>Data & concepts</h3>
          <ul>
            <li><b>Dataset:</b> synthetic <span style="font-weight:900;">assets/train.csv</span> (academic use).</li>
            <li><b>Architecture:</b> modular pages + shared services (data / UI helpers).</li>
            <li><b>UI + CLI:</b> web UI for visuals + menu-driven CLI for quick summaries.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # Navigation helpers (SAME TAB)
    # IMPORTANT:
    # - Streamlit multipage navigation should use st.switch_page("pages/YourPage.py")
    # - This works on Streamlit Cloud and keeps everything in the same tab.
    # ---------------------------------------------------
    def go(page_py: str):
        """Safely navigate to a Streamlit multipage file path."""
        try:
            st.switch_page(page_py)
        except Exception:
            st.error(
                f"Navigation failed. Make sure this file exists: {page_py}\n"
                "Also ensure you are running as a Streamlit multipage app (pages/ folder)."
            )

    def render_card(title, emoji, desc, hint, page_py, img_path: Path, btn_label: str, key: str):
        # Card shell (HTML) + content (Streamlit widgets)
        st.markdown('<div class="cardShell">', unsafe_allow_html=True)

        # Image header (HTML so it fills the full card width/height)
        if _exists(img_path):
            img_bytes = img_path.read_bytes()
            st.markdown('<div class="cardTop">', unsafe_allow_html=True)
            st.image(img_bytes, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown('<div class="cardTop"></div>', unsafe_allow_html=True)

        st.markdown('<div class="cardBody">', unsafe_allow_html=True)
        st.markdown(f'<div class="cardTitle"><span style="font-size:1.35rem;">{emoji}</span><span>{title}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="cardDesc">{desc}</div>', unsafe_allow_html=True)

        # Button row (Streamlit widgets)
        btn_col, hint_col = st.columns([1.25, 1], vertical_alignment="center")
        with btn_col:
            if st.button(f"➡️ {btn_label} →", key=key, use_container_width=True):
                go(page_py)
        with hint_col:
            st.markdown(f'<div class="cardHint">{hint}</div>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # SYSTEM PAGES
    # ---------------------------------------------------
    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sectionTitle">🧩 System Pages</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">These pages strengthen enterprise design + governance (architecture, security, risk & ethics).</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        render_card(
            title="System Overview / Architecture",
            emoji="🧱",
            desc="View the system architecture, shared services, page structure, and cloud scalability mapping.",
            hint="Enterprise design + scalability",
            page_py="pages/System_Overview_Architecture.py",
            img_path=SYSTEM_OVERVIEW_PATH,
            btn_label="Open page",
            key="open_system_overview",
        )
    with c2:
        render_card(
            title="Security, Risk & Ethics",
            emoji="🛡️",
            desc="Review privacy protections, governance assumptions, security controls, and ethical analytics considerations.",
            hint="Protection + governance",
            page_py="pages/Security_Risk_Ethics.py",
            img_path=SECURITY_RISK_ETHICS_PATH,
            btn_label="Open page",
            key="open_security_risk_ethics",
        )

    # ---------------------------------------------------
    # ANALYTICS MODULES
    # ---------------------------------------------------
    st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Click <b>Open module →</b> to navigate. Each module uses the same theme and dataset service.</div>',
        unsafe_allow_html=True,
    )

    r1c1, r1c2 = st.columns(2, gap="large")
    with r1c1:
        render_card(
            title="Flight Performance Analytics",
            emoji="✈️",
            desc="Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
            hint="Interactive KPIs & charts",
            page_py="pages/Module1_Flight_Performance.py",
            img_path=MODULE_1_PATH,
            btn_label="Open module",
            key="open_module_1",
        )
    with r1c2:
        render_card(
            title="Customer Experience Analytics",
            emoji="😊",
            desc="Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
            hint="Service quality insights",
            page_py="pages/Module2_Customer_Experience.py",
            img_path=MODULE_2_PATH,
            btn_label="Open module",
            key="open_module_2",
        )

    r2c1, r2c2 = st.columns(2, gap="large")
    with r2c1:
        render_card(
            title="Risk & Scenario Simulation",
            emoji="⚠️",
            desc="Model operational uncertainty using Monte Carlo simulation and scenario-based disruption controls.",
            hint="Probabilities, percentiles, worst-case",
            page_py="pages/Module3_Risk_Simulation.py",
            img_path=MODULE_3_PATH,
            btn_label="Open module",
            key="open_module_3",
        )
    with r2c2:
        render_card(
            title="Cloud Analytics",
            emoji="☁️",
            desc="Demonstrate scalable processing concepts and cloud-oriented analytics patterns.",
            hint="Batch vs streaming + scaling",
            page_py="pages/Module4_Cloud_Analytics.py",
            img_path=MODULE_4_PATH,
            btn_label="Open module",
            key="open_module_4",
        )

    st.info(
        "Tip: If an image/video is missing on Streamlit Cloud, confirm the filename EXACTLY and that it’s inside /assets "
        "(including correct capitalization)."
    )


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
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
