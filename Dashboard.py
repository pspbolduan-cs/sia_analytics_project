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
    # ASSET PATHS
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

    def file_to_data_uri(p: Path, mime: str) -> str:
        """
        Background video requires a browser-accessible URL.
        Streamlit doesn't serve /assets files directly, so we embed as a base64 data URI.
        Keep hero.mp4 short/small (ideal <= ~12–20MB).
        """
        if not exists(p):
            return ""
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{b64}"

    hero_video_uri = file_to_data_uri(HERO_VIDEO_PATH, "video/mp4")

    # ---------------------------------------------------
    # CLEAN, CONSISTENT DESIGN SYSTEM
    # ---------------------------------------------------
    st.markdown(
        """
        <style>
          /* App background + spacing */
          [data-testid="stAppViewContainer"]{
            background: radial-gradient(1200px 700px at 15% 5%, rgba(14, 65, 140, 0.08), transparent 55%),
                        radial-gradient(1000px 600px at 90% 10%, rgba(245, 158, 11, 0.08), transparent 55%),
                        #f6f7fb;
          }
          .block-container{
            padding-top: 1.2rem !important;
            padding-bottom: 3rem !important;
            max-width: 1200px;
          }
          header, [data-testid="stHeader"]{ background: transparent !important; }

          /* Typography */
          .h1{
            font-size: 3.05rem;
            font-weight: 950;
            letter-spacing: -0.9px;
            line-height: 1.05;
            margin: 0;
          }
          .sub{
            font-size: 1.12rem;
            color: rgba(255,255,255,0.86);
            margin-top: 10px;
            max-width: 980px;
            line-height: 1.5;
          }
          .sectionTitle{
            font-size: 2.0rem;
            font-weight: 950;
            letter-spacing: -0.5px;
            margin: 18px 0 6px 0;
            color: #0b2c5f;
          }
          .sectionSub{
            color: rgba(15, 23, 42, 0.65);
            font-size: 1.05rem;
            margin-bottom: 12px;
            line-height: 1.5;
          }

          /* Hero */
          .heroWrap{
            position: relative;
            border-radius: 26px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(15, 23, 42, 0.18);
            border: 1px solid rgba(255,255,255,0.16);
            margin-bottom: 18px;
            min-height: 380px;
          }
          .heroVideo{
            position:absolute;
            inset:0;
            width:100%;
            height:100%;
            object-fit: cover;
            transform: scale(1.02);
            filter: saturate(1.05) contrast(1.02);
            z-index: 0;
          }
          .heroOverlay{
            position:absolute;
            inset:0;
            background:
              linear-gradient(135deg,
                rgba(9, 20, 43, 0.86) 0%,
                rgba(10, 58, 128, 0.62) 45%,
                rgba(9, 20, 43, 0.88) 100%);
            z-index: 1;
          }
          .heroInner{
            position: relative;
            z-index: 2;
            padding: 26px 26px 20px 26px;
            display:flex;
            flex-direction: column;
            gap: 16px;
          }
          .heroTopRow{
            display:flex;
            align-items:flex-start;
            justify-content: space-between;
            gap: 18px;
            flex-wrap: wrap;
          }
          .logoChip{
            background: rgba(255,255,255,0.92);
            border-radius: 18px;
            padding: 10px 12px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.20);
            border: 1px solid rgba(255,255,255,0.45);
            display:flex;
            align-items:center;
            justify-content:center;
            flex: 0 0 auto;
          }
          .logoChip img{ height: 56px; width:auto; display:block; }

          /* Pills */
          .pillRow{
            display:flex;
            flex-wrap:wrap;
            gap: 10px;
            margin-top: 4px;
          }
          .pill{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.20);
            color: rgba(255,255,255,0.92);
            font-weight: 850;
            font-size: 0.95rem;
            backdrop-filter: blur(6px);
          }
          .dot{
            width: 10px;
            height: 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.80);
            display:inline-block;
          }

          /* Cards */
          .card{
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(15, 23, 42, 0.10);
            border-radius: 20px;
            box-shadow: 0 14px 38px rgba(15, 23, 42, 0.08);
            overflow:hidden;
          }
          .cardBody{
            padding: 14px 16px 16px 16px;
          }
          .cardTitle{
            font-size: 1.25rem;
            font-weight: 950;
            color: #0b2c5f;
            margin: 6px 0 6px 0;
            display:flex;
            gap: 10px;
            align-items:center;
          }
          .cardDesc{
            color: rgba(15, 23, 42, 0.70);
            font-size: 1.02rem;
            line-height: 1.5;
            margin-bottom: 10px;
          }
          .cardMeta{
            color: rgba(15, 23, 42, 0.55);
            font-weight: 850;
            font-size: 0.95rem;
            margin-top: 6px;
          }

          /* Make Streamlit image nicely rounded within cards */
          [data-testid="stImage"] img{
            border-radius: 14px !important;
          }

          /* CTA buttons */
          div.stButton > button{
            border-radius: 14px !important;
            padding: 10px 14px !important;
            font-weight: 900 !important;
            border: 1px solid rgba(12, 37, 78, 0.16) !important;
            background: linear-gradient(135deg, #0b2c5f, #0a4aa1) !important;
            color: #ffffff !important;
          }
          div.stButton > button:hover{
            filter: brightness(1.06);
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
                f"Navigation failed.\n\nMissing file: `{page_py}`\n"
                "Make sure it exists inside `/pages` and the filename matches EXACTLY (case-sensitive)."
            )

    # ---------------------------------------------------
    # HERO (VIDEO BACKGROUND BEHIND TITLE)
    # ---------------------------------------------------
    logo_html = ""
    if exists(LOGO_PATH):
        # Use st.image for reliability, but we want it inside hero HTML.
        # So embed logo as base64 too (small file, safe).
        logo_uri = file_to_data_uri(LOGO_PATH, "image/png")
        if logo_uri:
            logo_html = f"""
            <div class="logoChip">
              <img src="{logo_uri}" alt="Singapore Airlines Logo" />
            </div>
            """

    video_html = ""
    if hero_video_uri:
        video_html = f"""
        <video class="heroVideo" autoplay muted loop playsinline>
          <source src="{hero_video_uri}" type="video/mp4">
        </video>
        """

    st.markdown(
        f"""
        <div class="heroWrap">
          {video_html}
          <div class="heroOverlay"></div>

          <div class="heroInner">
            <div class="heroTopRow">
              {logo_html}
              <div style="flex:1; min-width: 280px;">
                <div class="h1" style="color:#ffffff;">Singapore Airlines Analytics System</div>
                <div class="sub">
                  Enterprise cloud-based analytics dashboard for operational performance, customer experience,
                  risk scenarios, and cloud processing concepts.
                </div>

                <div class="pillRow">
                  <span class="pill"><span class="dot"></span> Streamlit UI</span>
                  <span class="pill"><span class="dot"></span> CLI supported</span>
                  <span class="pill"><span class="dot"></span> Dataset: assets/train.csv</span>
                </div>

                {"<div style='margin-top:12px; color:rgba(255,255,255,0.92); font-weight:900;'>⚠️ Video missing: assets/hero.mp4</div>" if not hero_video_uri else ""}
                {"<div style='margin-top:8px; color:rgba(255,255,255,0.92); font-weight:900;'>⚠️ Logo missing: assets/singapore_airlines_logo.png</div>" if not logo_html else ""}
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # Small intro area
    # ---------------------------------------------------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">A single entry point linking system pages (governance) and analytics modules (interactive dashboards).</div>',
        unsafe_allow_html=True,
    )

    i1, i2 = st.columns(2, gap="large")
    with i1:
        st.markdown('<div class="card"><div class="cardBody">', unsafe_allow_html=True)
        st.markdown('<div class="cardTitle">🧭 How to use</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="cardDesc">
              • Open a module using <b>Open module</b> or a governance page using <b>Open page</b>.<br>
              • Each module has interactive controls + charts.<br>
              • Risk Simulation explains uncertainty (probability, percentiles, worst-case).<br>
              • Cloud Analytics demonstrates scalable processing concepts.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div></div>", unsafe_allow_html=True)

    with i2:
        st.markdown('<div class="card"><div class="cardBody">', unsafe_allow_html=True)
        st.markdown('<div class="cardTitle">🗂️ Data & concepts</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="cardDesc">
              • <b>Dataset:</b> synthetic <code>assets/train.csv</code> (academic use).<br>
              • <b>Architecture:</b> modular pages + shared services (data / UI helpers).<br>
              • <b>UI + CLI:</b> dashboard for visuals + CLI for quick summaries.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div></div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # Card renderer (clean + consistent)
    # ---------------------------------------------------
    def render_card(title, emoji, desc, hint, page_py, img_path: Path, btn_label: str, key: str):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if exists(img_path):
            st.image(str(img_path), use_container_width=True)
        else:
            st.info(f"Missing image: {img_path.name}")

        st.markdown('<div class="cardBody">', unsafe_allow_html=True)
        st.markdown(f'<div class="cardTitle">{emoji} {title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="cardDesc">{desc}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="cardMeta">{hint}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Button below body for consistent alignment
        if st.button(f"➡️ {btn_label}", key=key, use_container_width=True):
            go(page_py)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------
    # SYSTEM PAGES
    # ---------------------------------------------------
    st.markdown('<div class="sectionTitle">🧩 System Pages</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Enterprise design + governance pages (architecture, security, risk & ethics).</div>',
        unsafe_allow_html=True,
    )

    s1, s2 = st.columns(2, gap="large")
    with s1:
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

    with s2:
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
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Click <b>Open module</b> to navigate. Each module follows the same clean theme.</div>',
        unsafe_allow_html=True,
    )

    m1, m2 = st.columns(2, gap="large")
    with m1:
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
    with m2:
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

    m3, m4 = st.columns(2, gap="large")
    with m3:
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
    with m4:
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
        "If video doesn’t show: keep assets/hero.mp4 small (short loop). If images don’t show: verify filenames + capitalization."
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
