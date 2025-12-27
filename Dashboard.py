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
    import streamlit.components.v1 as components

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
    # ASSETS
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

    def to_data_uri(p: Path, mime: str) -> str:
        """Used only for HERO html background video/logo."""
        if not exists(p):
            return ""
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        return f"data:{mime};base64,{b64}"

    hero_video_uri = to_data_uri(HERO_VIDEO_PATH, "video/mp4")  # keep hero.mp4 small
    logo_uri = to_data_uri(LOGO_PATH, "image/png")

    # ---------------------------------------------------
    # GLOBAL CLEAN DESIGN SYSTEM (square cards / boxes)
    # ---------------------------------------------------
    st.markdown(
        """
        <style>
          /* Background + page width */
          [data-testid="stAppViewContainer"]{
            background:
              radial-gradient(1100px 700px at 15% 5%, rgba(14, 65, 140, 0.10), transparent 55%),
              radial-gradient(1000px 700px at 90% 10%, rgba(245, 158, 11, 0.08), transparent 55%),
              #F6F7FB;
          }
          .block-container{
            max-width: 1180px;
            padding-top: 1.1rem !important;
            padding-bottom: 2.6rem !important;
          }
          header, [data-testid="stHeader"]{ background: transparent !important; }

          /* Section typography */
          .secTitle{
            font-size: 1.9rem;
            font-weight: 950;
            letter-spacing: -0.4px;
            color: #0B2C5F;
            margin: 14px 0 4px 0;
          }
          .secSub{
            color: rgba(15, 23, 42, 0.65);
            font-size: 1.05rem;
            line-height: 1.5;
            margin-bottom: 14px;
          }

          /* Box/card styling for bordered containers */
          div[data-testid="stVerticalBlockBorderWrapper"]{
            background: #FFFFFF !important;
            border: 1px solid rgba(15, 23, 42, 0.10) !important;
            border-radius: 14px !important;     /* more “square” */
            box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08) !important;
          }

          /* Reduce padding inconsistencies */
          div[data-testid="stVerticalBlockBorderWrapper"] > div{
            padding-top: 12px !important;
            padding-bottom: 12px !important;
          }

          /* Images inside cards: square-ish */
          [data-testid="stImage"] img{
            border-radius: 10px !important;
          }

          /* Buttons: clean CTA */
          div.stButton > button{
            width: 100%;
            border-radius: 10px !important;
            padding: 10px 14px !important;
            font-weight: 900 !important;
            border: 1px solid rgba(12, 37, 78, 0.16) !important;
            background: linear-gradient(135deg, #0B2C5F, #0A4AA1) !important;
            color: #FFFFFF !important;
          }
          div.stButton > button:hover{
            filter: brightness(1.06);
          }

          /* Small meta text */
          .meta{
            color: rgba(15, 23, 42, 0.60);
            font-weight: 800;
            font-size: 0.95rem;
            margin-top: 6px;
          }

          /* Make markdown lists tighter in boxes */
          .tight ul { margin-top: 0.3rem; margin-bottom: 0.3rem; }
          .tight li { margin-bottom: 0.25rem; }
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
    # HERO (Background video behind title) — use components.html so HTML never prints as text
    # ---------------------------------------------------
    hero_height = 380

    # Clean fallbacks (if missing video/logo)
    video_tag = ""
    if hero_video_uri:
        video_tag = f"""
        <video class="bg" autoplay muted loop playsinline>
          <source src="{hero_video_uri}" type="video/mp4">
        </video>
        """
    else:
        video_tag = """<div class="bg-fallback"></div>"""

    logo_tag = ""
    if logo_uri:
        logo_tag = f"""<img class="logo" src="{logo_uri}" alt="SIA Logo" />"""

    hero_html = f"""
    <div class="hero">
      {video_tag}
      <div class="overlay"></div>
      <div class="content">
        <div class="top">
          {logo_tag}
          <div class="text">
            <div class="title">Singapore Airlines Analytics System</div>
            <div class="subtitle">
              Enterprise cloud-based analytics dashboard for operational performance, customer experience,
              risk scenarios, and cloud processing concepts.
            </div>
            <div class="pills">
              <span class="pill"><span class="dot"></span> Streamlit UI</span>
              <span class="pill"><span class="dot"></span> CLI supported</span>
              <span class="pill"><span class="dot"></span> Dataset: assets/train.csv</span>
            </div>
          </div>
        </div>
        <div class="note">
          {("" if hero_video_uri else "⚠️ Missing video: assets/hero.mp4")}
          {("" if logo_uri else (" &nbsp; • &nbsp; ⚠️ Missing logo: assets/singapore_airlines_logo.png"))}
        </div>
      </div>
    </div>

    <style>
      .hero {{
        position: relative;
        height: {hero_height}px;
        width: 100%;
        border-radius: 16px;                 /* more “box” */
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.16);
        box-shadow: 0 18px 50px rgba(15,23,42,0.18);
        background: #0b2c5f;
      }}
      .bg {{
        position:absolute; inset:0;
        width:100%; height:100%;
        object-fit: cover;
        transform: scale(1.02);
        filter: saturate(1.05) contrast(1.03);
      }}
      .bg-fallback {{
        position:absolute; inset:0;
        background: radial-gradient(800px 400px at 20% 20%, rgba(255,255,255,0.10), transparent 60%),
                    linear-gradient(135deg, rgba(7, 18, 40, 0.96), rgba(10, 58, 128, 0.86));
      }}
      .overlay {{
        position:absolute; inset:0;
        background: linear-gradient(135deg,
          rgba(9, 18, 38, 0.88) 0%,
          rgba(10, 58, 128, 0.60) 45%,
          rgba(9, 18, 38, 0.90) 100%);
      }}
      .content {{
        position: relative;
        height: 100%;
        padding: 22px 22px 18px 22px;
        display:flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 12px;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      }}
      .top {{
        display:flex;
        gap: 16px;
        align-items:flex-start;
      }}
      .logo {{
        height: 56px;
        width:auto;
        background: rgba(255,255,255,0.92);
        border-radius: 12px;
        padding: 10px 12px;
        border: 1px solid rgba(255,255,255,0.35);
        box-shadow: 0 10px 30px rgba(0,0,0,0.22);
      }}
      .text {{ flex: 1; min-width: 240px; }}
      .title {{
        color: #fff;
        font-weight: 950;
        letter-spacing: -0.8px;
        font-size: 44px;
        line-height: 1.05;
      }}
      .subtitle {{
        margin-top: 10px;
        color: rgba(255,255,255,0.86);
        font-size: 16.8px;
        line-height: 1.55;
        max-width: 980px;
      }}
      .pills {{
        display:flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
      }}
      .pill {{
        display:inline-flex;
        align-items:center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.20);
        color: rgba(255,255,255,0.92);
        font-weight: 850;
        font-size: 13.8px;
        backdrop-filter: blur(6px);
      }}
      .dot {{
        width: 10px; height: 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.82);
        display:inline-block;
      }}
      .note {{
        color: rgba(255,255,255,0.80);
        font-weight: 800;
        font-size: 13px;
        opacity: 0.95;
      }}
      @media (max-width: 980px) {{
        .title {{ font-size: 34px; }}
        .hero {{ height: 420px; }}
      }}
    </style>
    """

    components.html(hero_html, height=hero_height + 10)

    # ---------------------------------------------------
    # SECTIONS
    # ---------------------------------------------------
    st.markdown('<div class="secTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="secSub">A single entry point linking system pages (governance) and analytics modules (interactive dashboards).</div>',
        unsafe_allow_html=True,
    )

    a, b = st.columns(2, gap="large")
    with a:
        with st.container(border=True):
            st.markdown("#### 🧭 How to use")
            st.markdown(
                """
                <div class="tight">
                <ul>
                  <li>Open a module using <b>Open module</b> or a governance page using <b>Open page</b>.</li>
                  <li>Each module includes interactive controls + charts.</li>
                  <li>Risk Simulation explains uncertainty (probability, percentiles, worst-case).</li>
                  <li>Cloud Analytics demonstrates scalable processing concepts.</li>
                </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with b:
        with st.container(border=True):
            st.markdown("#### 🗂️ Data & concepts")
            st.markdown(
                """
                <div class="tight">
                <ul>
                  <li><b>Dataset:</b> synthetic <code>assets/train.csv</code> (academic use).</li>
                  <li><b>Architecture:</b> modular pages + shared services (data / UI helpers).</li>
                  <li><b>UI + CLI:</b> dashboard for visuals + CLI for quick summaries.</li>
                </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------------------------------------------------
    # CLEAN CARD RENDERER (square box style)
    # ---------------------------------------------------
    def render_card(title, emoji, desc, hint, page_py, img_path: Path, btn_label: str, key: str):
        with st.container(border=True):
            if exists(img_path):
                st.image(str(img_path), use_container_width=True)
            else:
                st.info(f"Missing image: {img_path.name}")

            st.markdown(f"#### {emoji} {title}")
            st.write(desc)
            st.markdown(f'<div class="meta">{hint}</div>', unsafe_allow_html=True)

            if st.button(f"➡️ {btn_label}", key=key, use_container_width=True):
                go(page_py)

    # ---------------------------------------------------
    # SYSTEM PAGES
    # ---------------------------------------------------
    st.markdown('<div class="secTitle">🧩 System Pages</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="secSub">Enterprise design + governance pages (architecture, security, risk & ethics).</div>',
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
    st.markdown('<div class="secTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="secSub">Click <b>Open module</b> to navigate. Each module follows the same clean boxed layout.</div>',
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
        "If the hero video loads slowly: keep `assets/hero.mp4` as a short loop (small file). "
        "If images don’t show: verify filename capitalization inside `/assets`."
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
