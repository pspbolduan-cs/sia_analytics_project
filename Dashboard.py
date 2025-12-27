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

    def exists(p: Path) -> bool:
        try:
            return p.exists() and p.is_file()
        except Exception:
            return False

    # ---------------------------------------------------
    # CLEAN PROFESSIONAL THEME CSS
    # (no broken HTML wrappers — only skinning Streamlit blocks)
    # ---------------------------------------------------
    st.markdown(
        """
        <style>
          /* Page spacing */
          .block-container { padding-top: 1.2rem !important; padding-bottom: 2.5rem !important; }
          [data-testid="stAppViewContainer"] {
            background: #f5f6fa;
          }

          /* Remove extra top whitespace under header */
          header { background: transparent !important; }
          [data-testid="stHeader"] { background: transparent !important; }

          /* Hero panel */
          .heroPanel{
            background: linear-gradient(135deg, rgba(12, 37, 78, 0.95), rgba(9, 72, 150, 0.92));
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 22px;
            padding: 22px 22px 18px 22px;
            box-shadow: 0 18px 55px rgba(15, 23, 42, 0.18);
            margin-bottom: 18px;
          }
          .heroTitle{
            color:#ffffff;
            font-weight: 950;
            letter-spacing: -0.7px;
            font-size: 3.0rem;
            line-height: 1.05;
            margin: 0;
          }
          .heroSub{
            color: rgba(255,255,255,0.85);
            font-size: 1.12rem;
            margin-top: 8px;
            max-width: 980px;
          }
          .pillRow{ display:flex; flex-wrap:wrap; gap:10px; margin-top: 12px; }
          .pill{
            display:inline-flex; align-items:center; gap:8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.20);
            color: rgba(255,255,255,0.92);
            font-weight: 850;
            font-size: 0.95rem;
            backdrop-filter: blur(6px);
          }
          .dot{ width: 10px; height: 10px; border-radius: 999px; background: rgba(255,255,255,0.75); display:inline-block; }

          /* Section titles */
          .sectionTitle{
            font-size: 2.0rem;
            font-weight: 950;
            letter-spacing: -0.4px;
            margin: 16px 0 4px 0;
            color: #0b2c5f;
          }
          .sectionSub{
            color: rgba(15, 23, 42, 0.65);
            font-size: 1.05rem;
            margin-bottom: 12px;
          }

          /* Card skin (Streamlit container border wrapper) */
          div[data-testid="stVerticalBlockBorderWrapper"]{
            border-radius: 18px !important;
            border: 1px solid rgba(15, 23, 42, 0.10) !important;
            background: #ffffff !important;
            box-shadow: 0 14px 38px rgba(15, 23, 42, 0.08) !important;
          }

          /* Make images inside cards rounded */
          [data-testid="stImage"] img{
            border-radius: 14px !important;
          }

          /* CTA buttons */
          div.stButton > button{
            border-radius: 14px !important;
            padding: 10px 14px !important;
            font-weight: 900 !important;
            border: 1px solid rgba(12, 37, 78, 0.18) !important;
            background: linear-gradient(135deg, #0b2c5f, #0a4aa1) !important;
            color: #ffffff !important;
          }
          div.stButton > button:hover{
            filter: brightness(1.04);
          }

          /* Small meta text */
          .meta{
            color: rgba(15, 23, 42, 0.60);
            font-weight: 800;
            font-size: 0.95rem;
            margin-top: 6px;
          }

          /* Reduce video chrome spacing */
          [data-testid="stVideo"]{
            border-radius: 16px;
            overflow: hidden;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # Navigation (same tab)
    # ---------------------------------------------------
    def go(page_py: str):
        try:
            st.switch_page(page_py)
        except Exception:
            st.error(
                f"Navigation failed.\n\n"
                f"Missing file: `{page_py}`\n"
                f"Make sure it exists inside the `/pages` folder with the EXACT same name (case-sensitive)."
            )

    # ---------------------------------------------------
    # HERO (clean + professional)
    # ---------------------------------------------------
    st.markdown('<div class="heroPanel">', unsafe_allow_html=True)

    left, right = st.columns([1, 4], vertical_alignment="center")
    with left:
        if exists(LOGO_PATH):
            st.image(str(LOGO_PATH), width=110)
        else:
            st.caption("Logo missing: assets/singapore_airlines_logo.png")

    with right:
        st.markdown('<p class="heroTitle">Singapore Airlines Analytics System</p>', unsafe_allow_html=True)
        st.markdown(
            '<div class="heroSub">Enterprise cloud-based analytics dashboard for operational performance, '
            'customer experience, risk scenarios, and cloud processing concepts.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="pillRow">
              <span class="pill"><span class="dot"></span> Streamlit UI</span>
              <span class="pill"><span class="dot"></span> CLI supported</span>
              <span class="pill"><span class="dot"></span> Dataset: assets/train.csv</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if exists(HERO_VIDEO_PATH):
        st.video(str(HERO_VIDEO_PATH), autoplay=True, loop=True, muted=True)
    else:
        st.warning("Video not found: assets/hero.mp4")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # Info cards
    # ---------------------------------------------------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">A single entry point that explains the system and links to analytics modules and enterprise system pages.</div>',
        unsafe_allow_html=True,
    )

    a, b = st.columns(2, gap="large")
    with a:
        with st.container(border=True):
            st.subheader("How to use")
            st.write(
                "- Open a module using **Open module** or a governance page using **Open page**.\n"
                "- Each module includes interactive controls + charts.\n"
                "- Risk Simulation explains uncertainty (probability, percentiles, worst-case).\n"
                "- Cloud Analytics demonstrates scalable processing concepts."
            )

    with b:
        with st.container(border=True):
            st.subheader("Data & concepts")
            st.write(
                "- **Dataset:** synthetic `assets/train.csv` (academic use)\n"
                "- **Architecture:** modular pages + shared services (data / UI helpers)\n"
                "- **UI + CLI:** web dashboard + menu-driven CLI summaries"
            )

    # ---------------------------------------------------
    # Card renderer (pure Streamlit — GOOD design, no broken HTML)
    # ---------------------------------------------------
    def render_card(title, emoji, desc, hint, page_py, img_path: Path, btn_label: str, key: str):
        with st.container(border=True):
            if exists(img_path):
                st.image(str(img_path), use_container_width=True)
            else:
                st.info(f"Missing image: {img_path.name}")

            st.markdown(f"### {emoji} {title}")
            st.write(desc)
            st.markdown(f'<div class="meta">{hint}</div>', unsafe_allow_html=True)

            if st.button(f"➡️ {btn_label}", key=key, use_container_width=True):
                go(page_py)

    # ---------------------------------------------------
    # System Pages
    # ---------------------------------------------------
    st.markdown('<div class="sectionTitle">🧩 System Pages</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Enterprise design + governance pages (architecture, security, risk & ethics).</div>',
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
    # Analytics Modules
    # ---------------------------------------------------
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Click <b>Open module</b> to navigate. Each module uses the same theme and dataset service.</div>',
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
        "If an image/video is missing on Streamlit Cloud: verify filename + capitalization and confirm it’s inside `/assets`."
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
