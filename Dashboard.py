# ============================================
# Author: Qian Zhu
# Date: 2025-12
# Singapore Airlines Analytics System
# Dashboard (Home Page) + CLI
# ============================================

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)


# =========================
# Helpers
# =========================
def _read_file_bytes(path: str) -> bytes:
    p = Path(path)
    if not p.exists():
        return b""
    return p.read_bytes()


def _video_data_uri(mp4_path: str) -> str:
    """
    Returns a data: URI for MP4 to make background video reliable on Streamlit Cloud.
    If the file is missing, returns an empty string.
    """
    import base64

    data = _read_file_bytes(mp4_path)
    if not data:
        return ""
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:video/mp4;base64,{b64}"


# =============================================================
# STREAMLIT UI MODE
# =============================================================
def run_streamlit_ui():
    import streamlit as st

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

    # -------------------------
    # CSS
    # -------------------------
    st.markdown(
        """
        <style>
          /* Reduce top padding */
          .block-container { padding-top: 1.2rem; }

          /* Remove any accidental code formatting look inside our sections */
          pre, code { font-family: inherit !important; }

          /* HERO */
          .heroWrap{
            position: relative;
            border-radius: 26px;
            overflow: hidden;
            margin-bottom: 2.2rem;
            box-shadow: 0 18px 45px rgba(0,0,0,0.22);
            border: 1px solid rgba(255,255,255,0.10);
            min-height: 360px;
          }
          .heroVideo{
            position:absolute;
            inset:0;
            width:100%;
            height:100%;
            object-fit:cover;
            opacity: 0.80;
            filter: saturate(1.05) contrast(1.05);
            transform: scale(1.03);
          }
          .heroOverlay{
            position:absolute;
            inset:0;
            background: linear-gradient(135deg, rgba(0,26,77,0.88) 0%, rgba(0,58,128,0.72) 45%, rgba(0,26,77,0.88) 100%);
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
          .logoChip img{
            height: 64px;
            width:auto;
            display:block;
          }
          .heroTitle{
            font-size: 3.1rem;
            font-weight: 950;
            letter-spacing: -1px;
            color: #ffffff;
            line-height: 1.05;
            margin: 0.15rem 0 0.55rem 0;
          }
          .heroSub{
            color: rgba(255,255,255,0.88);
            font-size: 1.18rem;
            max-width: 980px;
            margin: 0 0 1.05rem 0;
          }

          .tagRow{
            display:flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 8px;
          }
          .tagPill{
            display:inline-flex;
            align-items:center;
            gap: 8px;
            padding: 9px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.22);
            color: rgba(255,255,255,0.92);
            font-weight: 700;
            font-size: 0.95rem;
            backdrop-filter: blur(6px);
          }
          .tagDot{
            width: 10px;
            height: 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.75);
            display:inline-block;
          }
          .kbd{
            padding: 2px 8px;
            border-radius: 10px;
            background: rgba(0,0,0,0.22);
            border: 1px solid rgba(255,255,255,0.16);
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-weight: 700;
          }

          /* Sections */
          .sectionTitle{
            font-size: 2.35rem;
            font-weight: 950;
            color: #0B2A4A;
            margin: 0.4rem 0 0.65rem 0;
            letter-spacing: -0.5px;
            display:flex;
            align-items:center;
            gap: 10px;
          }
          .sectionSub{
            color: #6B7280;
            margin: 0 0 1.25rem 0;
            font-size: 1.05rem;
          }

          /* Cards grid */
          .grid{
            display:grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
          }
          @media (max-width: 1000px){
            .grid{ grid-template-columns: 1fr; }
            .heroTitle{ font-size: 2.3rem; }
          }

          .moduleCard{
            border-radius: 22px;
            overflow: hidden;
            background: #0B1220;
            border: 1px solid rgba(255,255,255,0.10);
            box-shadow: 0 12px 34px rgba(0,0,0,0.18);
            transition: transform 120ms ease, box-shadow 120ms ease;
          }
          .moduleCard:hover{
            transform: translateY(-2px);
            box-shadow: 0 18px 48px rgba(0,0,0,0.24);
          }

          .thumb{
            width: 100%;
            height: 190px;
            object-fit: cover;
            display:block;
          }

          .moduleInner{
            padding: 18px 18px 16px 18px;
          }
          .moduleTitleRow{
            display:flex;
            align-items:center;
            gap: 10px;
            color: #fff;
            font-size: 1.45rem;
            font-weight: 900;
            margin: 0 0 8px 0;
          }
          .moduleDesc{
            color: rgba(255,255,255,0.80);
            font-size: 1.02rem;
            line-height: 1.45;
            margin: 0 0 14px 0;
            min-height: 2.7em;
          }
          .ctaRow{
            display:flex;
            align-items:center;
            justify-content: space-between;
            gap: 10px;
            margin-top: 6px;
          }
          .ctaHint{
            color: rgba(255,255,255,0.70);
            font-weight: 700;
            font-size: 0.98rem;
          }
          .ctaBtn{
            display:inline-flex;
            align-items:center;
            gap: 10px;
            padding: 10px 14px;
            border-radius: 14px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.20);
            color: white;
            font-weight: 900;
            text-decoration: none;
          }
          .ctaBtn:hover{
            background: rgba(255,255,255,0.18);
          }

          /* Info cards */
          .infoWrap{
            display:grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
            margin-top: 10px;
          }
          @media (max-width: 1000px){
            .infoWrap{ grid-template-columns: 1fr; }
          }
          .infoCard{
            background: rgba(255,255,255,0.80);
            border: 1px solid rgba(15,23,42,0.08);
            border-radius: 18px;
            padding: 18px 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
          }
          .infoCard h3{
            margin: 0 0 8px 0;
            font-size: 1.25rem;
            font-weight: 950;
            color: #0B2A4A;
          }
          .infoCard ul{
            margin: 0;
            padding-left: 1.05rem;
            color: #334155;
            font-size: 1.02rem;
            line-height: 1.55;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------
    # Paths
    # -------------------------
    hero_video_path = "assets/hero.mp4"
    logo_path = "assets/singapore_airlines_logo.png"

    module_images = {
        "module1": "assets/module1.png",
        "module2": "assets/module2.png",
        "module3": "assets/module3.png",
        "module4": "assets/module4.png",
    }

    # -------------------------
    # HERO (video background)
    # -------------------------
    video_uri = _video_data_uri(hero_video_path)

    video_html = ""
    if video_uri:
        video_html = f"""
          <video class="heroVideo" autoplay muted loop playsinline>
            <source src="{video_uri}" type="video/mp4">
          </video>
        """

    hero_html = f"""
      <div class="heroWrap">
        {video_html}
        <div class="heroOverlay"></div>

        <div class="heroInner">
          <div class="logoChip">
            <img src="{logo_path}" alt="Singapore Airlines logo">
          </div>

          <div style="flex:1; min-width: 280px;">
            <div class="heroTitle">Singapore Airlines Analytics System</div>
            <div class="heroSub">
              Enterprise cloud-based analytics dashboard for operational performance, customer experience,
              risk scenarios, and cloud processing concepts.
            </div>

            <div class="tagRow">
              <span class="tagPill"><span class="tagDot"></span>Streamlit UI</span>
              <span class="tagPill"><span class="tagDot"></span>CLI supported</span>
              <span class="tagPill"><span class="tagDot"></span>Synthetic dataset: <span class="kbd">assets/train.csv</span></span>
            </div>
          </div>
        </div>
      </div>
    """

    st.markdown(hero_html, unsafe_allow_html=True)

    # -------------------------
    # What this dashboard does
    # -------------------------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">A single entry-point that lets you explore four analytics modules built on a shared theme, layout, and dataset.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="infoWrap">
          <div class="infoCard">
            <h3>How to use</h3>
            <ul>
              <li>Start here and open a module using the “Open module” buttons below.</li>
              <li>Use sliders/filters inside modules to test different operational conditions.</li>
              <li>Each module shows KPIs plus charts that support the insights.</li>
            </ul>
          </div>
          <div class="infoCard">
            <h3>Data & concepts</h3>
            <ul>
              <li><b>Dataset:</b> synthetic <span class="kbd">assets/train.csv</span> for academic demonstration.</li>
              <li><b>Risk module:</b> probabilities, percentiles, worst-case outcomes (Monte Carlo).</li>
              <li><b>Cloud module:</b> batch vs streaming + scalability patterns.</li>
              <li><b>Shared UI:</b> consistent theme across pages for a coherent system.</li>
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------
    # Modules
    # -------------------------
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Open a module to explore its KPIs, visualisations, and controls.</div>',
        unsafe_allow_html=True,
    )

    # Use Streamlit's multipage linking if available; fallback to basic anchors.
    def page_link_html(page_path: str, label: str) -> str:
        # Streamlit multipage typically supports st.page_link; HTML anchor fallback keeps the UI usable.
        return f'<a class="ctaBtn" href="/{page_path}" target="_self">Open module →</a>'

    # If st.page_link exists, we can render a normal button-like link below each card with Streamlit.
    can_page_link = hasattr(st, "page_link")

    def module_card(img_src: str, icon: str, title: str, desc: str, hint: str, page_path: str):
        st.markdown(
            f"""
            <div class="moduleCard">
              <img class="thumb" src="{img_src}" alt="{title}">
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">{icon}</span><span>{title}</span></div>
                <div class="moduleDesc">{desc}</div>
                <div class="ctaRow">
                  <div class="ctaHint">{hint}</div>
                  {"<!-- button placeholder -->" if can_page_link else page_link_html(page_path, "Open module →")}
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if can_page_link:
            # Button aligned with the card layout: render just below the HTML card in the same column.
            # Use an empty label in HTML and place the Streamlit page link right after.
            st.page_link(page_path, label="Open module →", icon="➡️")

    col1, col2 = st.columns(2)

    with col1:
        module_card(
            module_images["module1"],
            "✈️",
            "Flight Performance Analytics",
            "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
            "Interactive KPIs & charts",
            "pages/Module1_Flight_Performance.py",
        )
        module_card(
            module_images["module3"],
            "⚠️",
            "Risk & Scenario Simulation",
            "Model operational uncertainty using Monte Carlo simulation and scenario-based disruption controls.",
            "Probabilities, percentiles, worst-case outcomes",
            "pages/Module3_Risk_Simulation.py",
        )

    with col2:
        module_card(
            module_images["module2"],
            "😊",
            "Customer Experience Analytics",
            "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
            "Service quality insights",
            "pages/Module2_Customer_Experience.py",
        )
        module_card(
            module_images["module4"],
            "☁️",
            "Cloud Analytics",
            "Demonstrate scalable processing concepts and cloud-oriented analytics patterns.",
            "Batch vs streaming + scaling concepts",
            "pages/Module4_Cloud_Analytics.py",
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
    # Usage: python3 Dashboard.py cli
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    # Usage: streamlit run Dashboard.py
    else:
        run_streamlit_ui()
