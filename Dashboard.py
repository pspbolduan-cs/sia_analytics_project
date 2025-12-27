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


# -------------------------
# Base64 helpers (reliable assets on Streamlit Cloud)
# -------------------------
def _read_bytes(path: str) -> bytes:
    p = Path(path)
    return p.read_bytes() if p.exists() else b""


def _data_uri(path: str, mime: str) -> str:
    import base64

    data = _read_bytes(path)
    if not data:
        return ""
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def _guess_image_mime(path: str) -> str:
    p = path.lower()
    if p.endswith(".png"):
        return "image/png"
    if p.endswith(".jpg") or p.endswith(".jpeg"):
        return "image/jpeg"
    if p.endswith(".webp"):
        return "image/webp"
    return "image/png"


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
    # Asset paths (must match your repo)
    # -------------------------
    HERO_VIDEO = "assets/hero.mp4"
    LOGO = "assets/singapore_airlines_logo.png"

    MODULE_1 = "assets/module1.png"
    MODULE_2 = "assets/module2.png"
    MODULE_3 = "assets/module3.png"
    MODULE_4 = "assets/module4.png"

    # -------------------------
    # Embed assets as data URIs
    # -------------------------
    hero_video_uri = _data_uri(HERO_VIDEO, "video/mp4")
    logo_uri = _data_uri(LOGO, _guess_image_mime(LOGO))

    m1_uri = _data_uri(MODULE_1, _guess_image_mime(MODULE_1))
    m2_uri = _data_uri(MODULE_2, _guess_image_mime(MODULE_2))
    m3_uri = _data_uri(MODULE_3, _guess_image_mime(MODULE_3))
    m4_uri = _data_uri(MODULE_4, _guess_image_mime(MODULE_4))

    # -------------------------
    # CSS
    # -------------------------
    st.markdown(
        """
        <style>
          .block-container { padding-top: 1.2rem; }

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
            opacity: 0.82;
            filter: saturate(1.05) contrast(1.05);
            transform: scale(1.03);
          }
          .heroOverlay{
            position:absolute;
            inset:0;
            background: linear-gradient(135deg, rgba(0,26,77,0.90) 0%, rgba(0,58,128,0.72) 45%, rgba(0,26,77,0.90) 100%);
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
            font-weight: 800;
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
            font-weight: 800;
          }

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

          /* IMPORTANT: image fills full header */
          .thumb{
            width: 100%;
            height: 210px;
            object-fit: cover;
            display:block;
          }

          .moduleInner{ padding: 18px 18px 16px 18px; }
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
            font-weight: 800;
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
          .ctaBtn:hover{ background: rgba(255,255,255,0.18); }

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
            background: rgba(255,255,255,0.86);
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

          .warn{
            margin-top: 0.6rem;
            color: rgba(255,255,255,0.80);
            font-weight: 700;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -------------------------
    # HERO (video + overlay + content)
    # -------------------------
    if not hero_video_uri:
        video_html = ""
        video_note = '<div class="warn">⚠️ hero.mp4 not found at <span class="kbd">assets/hero.mp4</span></div>'
    else:
        video_html = f"""
            <video class="heroVideo" autoplay muted loop playsinline>
              <source src="{hero_video_uri}" type="video/mp4" />
            </video>
        """
        video_note = ""

    if not logo_uri:
        logo_html = '<div class="logoChip"><div class="warn">⚠️ Logo missing</div></div>'
    else:
        logo_html = f"""
            <div class="logoChip">
              <img src="{logo_uri}" alt="Singapore Airlines logo">
            </div>
        """

    hero_html = f"""
      <div class="heroWrap">
        {video_html}
        <div class="heroOverlay"></div>
        <div class="heroInner">
          {logo_html}
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
            {video_note}
          </div>
        </div>
      </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # -------------------------
    # Info sections
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
              <li>Each module shows KPIs plus charts to support the insights.</li>
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
    # Modules grid (images fill header)
    # -------------------------
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sectionSub">Open a module to explore its KPIs, visualisations, and controls.</div>',
        unsafe_allow_html=True,
    )

    # Streamlit multipage link helper:
    can_page_link = hasattr(st, "page_link")

    def open_link_html(page_path: str) -> str:
        return f'<a class="ctaBtn" href="/{page_path}" target="_self">Open module →</a>'

    def module_card(img_uri: str, icon: str, title: str, desc: str, hint: str, page_path: str):
        # Fallback if image missing
        if not img_uri:
            img_tag = '<div style="height:210px;background:linear-gradient(135deg,#001A4D,#003A80)"></div>'
        else:
            img_tag = f'<img class="thumb" src="{img_uri}" alt="{title}">'

        st.markdown(
            f"""
            <div class="moduleCard">
              {img_tag}
              <div class="moduleInner">
                <div class="moduleTitleRow"><span style="font-size:1.35rem;">{icon}</span><span>{title}</span></div>
                <div class="moduleDesc">{desc}</div>
                <div class="ctaRow">
                  <div class="ctaHint">{hint}</div>
                  {"<!-- streamlit link below -->" if can_page_link else open_link_html(page_path)}
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if can_page_link:
            st.page_link(page_path, label="Open module →", icon="➡️")

    col1, col2 = st.columns(2)

    with col1:
        module_card(
            m1_uri, "✈️", "Flight Performance Analytics",
            "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
            "Interactive KPIs & charts",
            "pages/Module1_Flight_Performance.py",
        )
        module_card(
            m3_uri, "⚠️", "Risk & Scenario Simulation",
            "Model operational uncertainty using Monte Carlo simulation and scenario-based disruption controls.",
            "Probabilities, percentiles, worst-case outcomes",
            "pages/Module3_Risk_Simulation.py",
        )

    with col2:
        module_card(
            m2_uri, "😊", "Customer Experience Analytics",
            "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
            "Service quality insights",
            "pages/Module2_Customer_Experience.py",
        )
        module_card(
            m4_uri, "☁️", "Cloud Analytics",
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
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
