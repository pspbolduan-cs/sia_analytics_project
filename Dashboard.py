# ============================================
# Author: Qian Zhu
# Date: 2025-12
# Singapore Airlines Analytics System
# Dashboard (Home Page) + CLI
# ============================================

import sys
import logging
import base64
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def _asset_path(rel: str) -> Path:
    return Path(__file__).parent / rel


def _guess_mime(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in [".png"]:
        return "image/png"
    if ext in [".jpg", ".jpeg"]:
        return "image/jpeg"
    if ext in [".webp"]:
        return "image/webp"
    if ext in [".mp4"]:
        return "video/mp4"
    return "application/octet-stream"


def _b64_data_uri(rel_path: str) -> str:
    path = _asset_path(rel_path)
    if not path.exists():
        return ""
    mime = _guess_mime(path)
    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{data}"


def run_streamlit_ui():
    import streamlit as st

    st.set_page_config(page_title="SIA Dashboard", page_icon="🏠", layout="wide")

    # Shared theme (safe import)
    try:
        from services.ui_service import apply_global_styles
        apply_global_styles()
    except Exception:
        pass

    # ---------- Assets (base64 so they always load on Streamlit Cloud) ----------
    hero_video_uri = _b64_data_uri("assets/hero.mp4")
    logo_uri = _b64_data_uri("assets/singapore_airlines_logo.png")

    # You can use .png or .jpg; just make sure the filenames match
    module1_uri = _b64_data_uri("assets/module1.png") or _b64_data_uri("assets/module1.jpg")
    module2_uri = _b64_data_uri("assets/module2.png") or _b64_data_uri("assets/module2.jpg")
    module3_uri = _b64_data_uri("assets/module3.png") or _b64_data_uri("assets/module3.jpg")
    module4_uri = _b64_data_uri("assets/module4.png") or _b64_data_uri("assets/module4.jpg")

    # ---------- Styles ----------
    st.markdown(
        """
        <style>
          .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1250px; }
          .heroWrap{
            position: relative;
            border-radius: 26px;
            overflow: hidden;
            background: linear-gradient(135deg, #001A4D 0%, #003A80 100%);
            box-shadow: 0 14px 40px rgba(0,0,0,0.22);
            margin-bottom: 1.6rem;
          }
          .heroVideo{
            position:absolute; inset:0;
            width:100%; height:100%;
            object-fit: cover;
            filter: contrast(1.05) saturate(1.05);
            opacity: 0.55;
          }
          .heroOverlay{
            position:absolute; inset:0;
            background: linear-gradient(135deg, rgba(0,26,77,0.90) 0%, rgba(0,58,128,0.78) 65%, rgba(0,26,77,0.92) 100%);
          }
          .heroInner{
            position: relative;
            padding: 2.2rem 2.2rem 2.0rem 2.2rem;
            display: flex;
            gap: 22px;
            align-items: flex-start;
            flex-wrap: wrap;
          }
          .logoChip{
            background: rgba(255,255,255,0.92);
            border-radius: 18px;
            padding: 12px 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.18);
            display:flex; align-items:center; justify-content:center;
          }
          .logoChip img{ height: 64px; width:auto; display:block; }
          .heroTitle{
            font-size: 3.0rem;
            font-weight: 900;
            letter-spacing: -1px;
            color: white;
            line-height: 1.05;
            margin-top: 0.1rem;
          }
          .heroSub{
            color: rgba(255,255,255,0.85);
            font-size: 1.15rem;
            margin-top: 0.65rem;
            max-width: 900px;
          }
          .tagRow{ display:flex; gap:10px; flex-wrap: wrap; margin-top: 1.2rem; }
          .tagPill{
            display:inline-flex; gap:10px; align-items:center;
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            color: rgba(255,255,255,0.92);
            font-weight: 700;
          }
          .tagDot{ width:10px; height:10px; border-radius:999px; background: rgba(255,255,255,0.75); display:inline-block; }
          .sectionTitle{
            font-size: 2.15rem;
            font-weight: 900;
            letter-spacing: -0.5px;
            color: #0B2B5B;
            margin: 0.8rem 0 0.4rem 0;
            display:flex; gap: 12px; align-items:center;
          }
          .subText{
            color: rgba(10,10,10,0.55);
            font-size: 1.05rem;
            margin-bottom: 1.0rem;
          }

          .grid{
            display:grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            margin-top: 12px;
          }
          @media (max-width: 980px){
            .grid{ grid-template-columns: 1fr; }
            .heroTitle{ font-size: 2.25rem; }
          }

          .moduleCard{
            position: relative;
            border-radius: 22px;
            overflow: hidden;
            background: #111827;
            box-shadow: 0 14px 34px rgba(0,0,0,0.18);
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
            min-height: 220px;
          }
          .moduleCard:hover{
            transform: translateY(-3px);
            box-shadow: 0 18px 42px rgba(0,0,0,0.22);
          }
          .thumb{
            width:100%;
            height: 165px;
            object-fit: cover;
            display:block;
            filter: saturate(1.05) contrast(1.05);
          }
          .moduleInner{
            padding: 16px 18px 18px 18px;
            color: white;
          }
          .moduleTitleRow{
            display:flex; gap:10px; align-items:center;
            font-size: 1.35rem;
            font-weight: 900;
            color: rgba(255,255,255,0.95);
            margin-bottom: 8px;
          }
          .moduleDesc{
            color: rgba(255,255,255,0.72);
            font-size: 1.0rem;
            line-height: 1.45;
            margin-bottom: 12px;
          }
          .ctaRow{
            display:flex; gap: 12px; align-items:center; justify-content: space-between;
            flex-wrap: wrap;
          }
          .ctaBtn{
            display:inline-flex;
            align-items:center;
            gap:10px;
            padding: 10px 14px;
            border-radius: 12px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.16);
            color: rgba(255,255,255,0.95);
            text-decoration:none;
            font-weight: 900;
          }
          .ctaBtn:hover{ background: rgba(255,255,255,0.18); }
          .ctaHint{
            color: rgba(255,255,255,0.65);
            font-weight: 700;
            font-size: 0.95rem;
          }

          .infoBox{
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(10,10,10,0.06);
            border-radius: 18px;
            padding: 16px 18px;
            box-shadow: 0 12px 28px rgba(0,0,0,0.08);
          }
          .infoBox h3{
            margin:0 0 10px 0;
            font-size: 1.25rem;
            font-weight: 900;
            color: #0B2B5B;
          }
          .infoBox ul{ margin: 0.25rem 0 0 1.2rem; color: rgba(10,10,10,0.70); }
          .infoBox li{ margin: 0.32rem 0; }

          /* If something ever gets wrapped in <pre><code>, keep it readable but do NOT show raw HTML blocks */
          pre { border-radius: 16px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- HERO ----------
    hero_html = f"""
    <div class="heroWrap">
      {"<video class='heroVideo' autoplay muted loop playsinline><source src='" + hero_video_uri + "' type='video/mp4'></video>" if hero_video_uri else ""}
      <div class="heroOverlay"></div>
      <div class="heroInner">
        <div class="logoChip">
          {"<img src='" + logo_uri + "' alt='Singapore Airlines logo' />" if logo_uri else "<div style='font-weight:900;color:#0B2B5B;'>SIA</div>"}
        </div>

        <div style="flex:1; min-width: 280px;">
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
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

    # ---------- WHAT / HOW / DATA ----------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="infoBox">
          <h3>Purpose</h3>
          <ul>
            <li>Provide a single entry point for four analytics modules (performance, customer experience, risk simulation, cloud analytics).</li>
            <li>Demonstrate interactive analytics and scenario exploration using a consistent dataset and UI theme.</li>
            <li>Support both web UI (Streamlit) and a simple CLI for quick summaries.</li>
          </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    with cols[0]:
        st.markdown(
            """
            <div class="infoBox">
              <h3>How to use</h3>
              <ul>
                <li>Start here and open a module using the cards below.</li>
                <li>Inside each module, adjust filters/sliders to explore different operational conditions.</li>
                <li>Use the “Back to Dashboard” button in modules to return quickly.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            """
            <div class="infoBox">
              <h3>Data & concepts</h3>
              <ul>
                <li><b>Dataset:</b> <code>assets/train.csv</code> (synthetic; academic use).</li>
                <li><b>Simulation:</b> controlled assumptions are used where a metric is missing.</li>
                <li><b>Cloud concepts:</b> modular pages, shared services, scalable processing patterns.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("System Architecture (quick view)", expanded=False):
        st.markdown(
            """
            **High-level flow**
            - Dashboard routes users to module pages (Streamlit multipage).
            - Modules load data via shared services (e.g., `services/data_service.py`) and apply a common theme (`services/ui_service.py`).
            - Each module focuses on a different analytics question but uses consistent UI patterns for grading clarity.

            **Suggested items to mention in your report/demo**
            - Shared services reduce duplication and improve maintainability.
            - Modular page structure supports scalability and clearer separation of concerns.
            """,
        )

    # ---------- MODULES ----------
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subText">Click <b>Open module</b> to navigate. Each module uses the same theme and dataset service.</div>',
        unsafe_allow_html=True,
    )

    def module_card(emoji: str, title: str, desc: str, hint: str, page_path: str, img_uri: str):
        # Use Streamlit multipage link if available; otherwise fallback to anchor
        try:
            import streamlit as st  # local
            if hasattr(st, "page_link"):
                link_html = f"""
                <div class="ctaRow">
                  <a class="ctaBtn" href="#" onclick="return false;">Open module →</a>
                  <span class="ctaHint">{hint}</span>
                </div>
                """
                # page_link must be rendered as a Streamlit element, not inside raw HTML
                # We'll render the card HTML, then the page_link button below it.
                card_html = f"""
                <div class="moduleCard">
                  {"<img class='thumb' src='" + img_uri + "' />" if img_uri else "<div style='height:165px;background:linear-gradient(135deg,#001A4D,#003A80);'></div>"}
                  <div class="moduleInner">
                    <div class="moduleTitleRow"><span>{emoji}</span><span>{title}</span></div>
                    <div class="moduleDesc">{desc}</div>
                    <div class="ctaRow">
                      <span class="ctaHint">{hint}</span>
                    </div>
                  </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                st.page_link(page_path, label="Open module →", icon="➡️", use_container_width=True)
                st.markdown("<div style='height:6px;'></div>", unsafe_allow_html=True)
                return
        except Exception:
            pass

        # Fallback: plain anchor navigation
        card_html = f"""
        <div class="moduleCard">
          {"<img class='thumb' src='" + img_uri + "' />" if img_uri else "<div style='height:165px;background:linear-gradient(135deg,#001A4D,#003A80);'></div>"}
          <div class="moduleInner">
            <div class="moduleTitleRow"><span>{emoji}</span><span>{title}</span></div>
            <div class="moduleDesc">{desc}</div>
            <div class="ctaRow">
              <a class="ctaBtn" href="/{page_path}" target="_self">Open module →</a>
              <span class="ctaHint">{hint}</span>
            </div>
          </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    grid_left, grid_right = st.columns(2)

    with grid_left:
        module_card(
            "✈️",
            "Flight Performance Analytics",
            "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
            "Interactive KPIs & charts",
            "pages/Module1_Flight_Performance.py",
            module1_uri,
        )
        module_card(
            "⚠️",
            "Risk & Scenario Simulation",
            "Model operational uncertainty using Monte Carlo simulation and scenario-based disruption controls.",
            "Probabilities, percentiles, worst-case outcomes",
            "pages/Module3_Risk_Simulation.py",
            module3_uri,
        )

    with grid_right:
        module_card(
            "😊",
            "Customer Experience Analytics",
            "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
            "Service quality insights",
            "pages/Module2_Customer_Experience.py",
            module2_uri,
        )
        module_card(
            "☁️",
            "Cloud Analytics",
            "Demonstrate scalable processing concepts and cloud-oriented analytics patterns.",
            "Batch vs streaming + scaling concepts",
            "pages/Module4_Cloud_Analytics.py",
            module4_uri,
        )

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    st.info("Tip: If thumbnails or video still don’t appear, confirm the filenames in /assets match what the code expects.")


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
            print("Invalid option.")
            input("Press ENTER to continue...")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].lower() == "cli":
        run_cli()
    else:
        run_streamlit_ui()
