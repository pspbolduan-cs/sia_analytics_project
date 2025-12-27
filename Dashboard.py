import sys
import logging
from pathlib import Path
import base64

logging.basicConfig(level=logging.INFO)


ASSET_DIR = Path(__file__).parent / "assets"


def _b64_file(path: Path) -> str:
    """Return base64 string for a local file. Empty string if missing."""
    try:
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception:
        return ""


def run_streamlit_ui():
    import streamlit as st

    st.set_page_config(page_title="SIA Dashboard", page_icon="🏠", layout="wide")

    # Apply shared theme if available
    try:
        from services.ui_service import apply_global_styles

        apply_global_styles()
    except Exception:
        pass

    # Assets (base64 so it works on Streamlit Cloud)
    logo_b64 = _b64_file(ASSET_DIR / "singapore_airlines_logo.png")
    hero_mp4_b64 = _b64_file(ASSET_DIR / "hero.mp4")

    m1_b64 = _b64_file(ASSET_DIR / "module1.png")
    m2_b64 = _b64_file(ASSET_DIR / "module2.png")
    m3_b64 = _b64_file(ASSET_DIR / "module3.png")
    m4_b64 = _b64_file(ASSET_DIR / "module4.png")

    # -----------------------------
    # Global CSS
    # -----------------------------
    st.markdown(
        """
        <style>
          :root{
            --bg: #F6F3EE;
            --ink: #0B1B33;
            --muted: #5B6677;
            --card: #0F1624;
            --card2: rgba(15,22,36,0.92);
            --stroke: rgba(255,255,255,0.10);
            --shadow: 0 16px 40px rgba(0,0,0,0.18);
            --r: 24px;
          }

          .block-container { padding-top: 1.25rem; }

          .heroWrap{
            position: relative;
            border-radius: 28px;
            overflow: hidden;
            box-shadow: var(--shadow);
            margin-bottom: 26px;
          }

          .heroMedia{
            position:absolute;
            inset:0;
            z-index:0;
            background: linear-gradient(135deg, #001A4D 0%, #003A80 55%, #0A3D7A 100%);
          }

          .heroOverlay{
            position:absolute;
            inset:0;
            z-index:1;
            background: linear-gradient(135deg,
              rgba(0,26,77,0.90) 0%,
              rgba(0,58,128,0.78) 55%,
              rgba(0,26,77,0.86) 100%);
          }

          .heroInner{
            position: relative;
            z-index: 2;
            padding: 40px 42px;
            display:flex;
            gap: 22px;
            flex-wrap: wrap;
            align-items:flex-start;
          }

          .logoChip{
            background: rgba(255,255,255,0.92);
            border-radius: 18px;
            padding: 10px 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.18);
            display:flex;
            align-items:center;
            justify-content:center;
          }
          .logoChip img{ height:64px; width:auto; display:block; }

          .heroTitle{
            font-size: 3.15rem;
            font-weight: 950;
            letter-spacing: -1px;
            margin: 0;
            color: #FFFFFF;
            line-height: 1.05;
          }

          .heroSub{
            margin-top: 10px;
            max-width: 880px;
            font-size: 1.12rem;
            color: rgba(255,255,255,0.85);
          }

          .tagRow{
            margin-top: 18px;
            display:flex;
            flex-wrap:wrap;
            gap: 10px;
          }
          .tagPill{
            display:inline-flex;
            gap:10px;
            align-items:center;
            padding: 10px 14px;
            border-radius: 999px;
            background: rgba(255,255,255,0.10);
            border: 1px solid rgba(255,255,255,0.14);
            color: rgba(255,255,255,0.86);
            font-weight: 600;
            backdrop-filter: blur(8px);
          }
          .tagDot{
            width:10px; height:10px; border-radius:999px;
            background: rgba(255,255,255,0.80);
            display:inline-block;
          }

          .sectionTitle{
            font-size: 2.35rem;
            font-weight: 900;
            color: #0B2A57;
            margin-top: 8px;
            margin-bottom: 10px;
            display:flex;
            align-items:center;
            gap: 12px;
          }

          .sectionSub{
            color: var(--muted);
            font-size: 1.05rem;
            margin-bottom: 18px;
          }

          .grid{
            display:grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
          }
          @media (max-width: 900px){
            .grid{ grid-template-columns: 1fr; }
          }

          .moduleCard{
            border-radius: var(--r);
            overflow:hidden;
            background: var(--card);
            box-shadow: var(--shadow);
            border: 1px solid rgba(255,255,255,0.06);
          }

          .thumb{
            width: 100%;
            height: 190px;
            object-fit: cover;
            display:block;
            filter: saturate(1.05) contrast(1.03);
          }

          .moduleInner{
            padding: 18px 20px 18px 20px;
          }

          .moduleTitleRow{
            display:flex;
            align-items:center;
            gap: 12px;
            color: #FFFFFF;
            font-weight: 900;
            font-size: 1.35rem;
            margin-bottom: 8px;
          }

          .moduleDesc{
            color: rgba(255,255,255,0.78);
            font-size: 1.02rem;
            line-height: 1.45;
            margin-bottom: 14px;
          }

          .ctaRow{
            display:flex;
            align-items:center;
            justify-content: space-between;
            gap: 12px;
            padding-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.08);
          }

          .ctaHint{
            color: rgba(255,255,255,0.68);
            font-weight: 650;
            font-size: 0.98rem;
          }

          .ctaBtn{
            display:inline-flex;
            align-items:center;
            gap: 10px;
            padding: 10px 14px;
            border-radius: 12px;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.14);
            color: rgba(255,255,255,0.92);
            text-decoration:none;
            font-weight: 800;
            transition: all .15s ease-in-out;
            white-space:nowrap;
          }
          .ctaBtn:hover{
            background: rgba(255,255,255,0.18);
            transform: translateY(-1px);
          }

          .infoGrid{
            display:grid;
            grid-template-columns: 1.2fr 1fr;
            gap: 18px;
            margin-top: 4px;
            margin-bottom: 6px;
          }
          @media (max-width: 900px){
            .infoGrid{ grid-template-columns: 1fr; }
          }

          .infoCard{
            background: #FFFFFF;
            border-radius: 18px;
            border: 1px solid rgba(11,42,87,0.10);
            padding: 18px 18px;
            box-shadow: 0 10px 26px rgba(0,0,0,0.08);
          }

          .infoCard h3{
            margin: 0 0 10px 0;
            color: #0B2A57;
            font-size: 1.35rem;
            font-weight: 900;
          }

          .infoCard ul{
            margin: 0;
            padding-left: 1.25rem;
            color: #344155;
            font-size: 1.02rem;
            line-height: 1.55;
          }

          .kbd{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            background: rgba(11,42,87,0.08);
            border: 1px solid rgba(11,42,87,0.12);
            padding: 2px 8px;
            border-radius: 10px;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # HERO (video background)
    # -----------------------------
    if hero_mp4_b64:
        hero_media_html = f"""
        <div class="heroMedia">
          <video autoplay muted loop playsinline
            style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; opacity:0.55;">
            <source src="data:video/mp4;base64,{hero_mp4_b64}" type="video/mp4">
          </video>
        </div>
        """
    else:
        hero_media_html = '<div class="heroMedia"></div>'

    logo_html = (
        f'<img src="data:image/png;base64,{logo_b64}" alt="Singapore Airlines logo"/>'
        if logo_b64
        else '<div style="height:64px; width:220px; display:flex; align-items:center; justify-content:center; color:#0B2A57; font-weight:900;">SIA</div>'
    )

    st.markdown(
        f"""
        <div class="heroWrap">
          {hero_media_html}
          <div class="heroOverlay"></div>
          <div class="heroInner">
            <div class="logoChip">{logo_html}</div>
            <div style="flex:1; min-width:280px;">
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
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # What this dashboard does
    # -----------------------------
    st.markdown('<div class="sectionTitle">📌 What this dashboard does</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="infoGrid">
          <div class="infoCard">
            <h3>Purpose</h3>
            <ul>
              <li>Provide a single entry-point to four analytics modules.</li>
              <li>Show operational insights (performance, experience, risk) using a consistent UI theme.</li>
              <li>Demonstrate cloud analytics concepts (scaling patterns, batch vs streaming ideas).</li>
            </ul>
          </div>
          <div class="infoCard">
            <h3>How to use</h3>
            <ul>
              <li>Open any module below and explore filters and KPIs.</li>
              <li>Use the module “Back to Dashboard” link to return here.</li>
              <li>Results use the same dataset/service layer across pages.</li>
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # Module cards
    # -----------------------------
    st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
    st.markdown('<div class="sectionSub">Click <b>Open module</b> to navigate.</div>', unsafe_allow_html=True)

    def module_card(img_b64: str, icon: str, title: str, desc: str, hint: str, page_path: str):
        img_html = (
            f'<img class="thumb" src="data:image/png;base64,{img_b64}" alt="{title}"/>'
            if img_b64
            else '<div style="height:190px; background: linear-gradient(135deg,#001A4D,#003A80);"></div>'
        )

        # Use st.switch_page when available (more reliable), else fall back to link
        can_switch = hasattr(st, "switch_page")

        if can_switch:
            # Render card + separate button row using HTML + Streamlit button
            st.markdown(
                f"""
                <div class="moduleCard">
                  {img_html}
                  <div class="moduleInner">
                    <div class="moduleTitleRow"><span style="font-size:1.35rem;">{icon}</span><span>{title}</span></div>
                    <div class="moduleDesc">{desc}</div>
                    <div class="ctaRow">
                      <div class="ctaHint">{hint}</div>
                      <div style="opacity:0.7; font-weight:800;">Open module →</div>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            # Button below the card to trigger navigation
            if st.button("Open module →", key=f"btn_{page_path}"):
                st.switch_page(page_path)
        else:
            # Link-based fallback
            st.markdown(
                f"""
                <div class="moduleCard">
                  {img_html}
                  <div class="moduleInner">
                    <div class="moduleTitleRow"><span style="font-size:1.35rem;">{icon}</span><span>{title}</span></div>
                    <div class="moduleDesc">{desc}</div>
                    <div class="ctaRow">
                      <div class="ctaHint">{hint}</div>
                      <a class="ctaBtn" href="/{page_path}" target="_self">Open module →</a>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    c1, c2 = st.columns(2)
    with c1:
        module_card(
            m1_b64,
            "✈️",
            "Flight Performance Analytics",
            "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
            "Interactive KPIs & charts",
            "pages/Module1_Flight_Performance.py",
        )
    with c2:
        module_card(
            m2_b64,
            "😊",
            "Customer Experience Analytics",
            "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
            "Service quality insights",
            "pages/Module2_Customer_Experience.py",
        )

    c3, c4 = st.columns(2)
    with c3:
        module_card(
            m3_b64,
            "⚠️",
            "Risk & Scenario Simulation",
            "Model operational uncertainty using Monte Carlo simulation and scenario-based disruption controls.",
            "Probabilities, percentiles, worst-case outcomes",
            "pages/Module3_Risk_Simulation.py",
        )
    with c4:
        module_card(
            m4_b64,
            "☁️",
            "Cloud Analytics",
            "Demonstrate scalable processing concepts and cloud-oriented analytics patterns.",
            "Batch vs streaming + scaling concepts",
            "pages/Module4_Cloud_Analytics.py",
        )

    # -----------------------------
    # Quick view section (optional)
    # -----------------------------
    with st.expander("System architecture (quick view)"):
        st.markdown(
            """
            - **Dashboard (this page):** navigation + context.
            - **Modules:** four pages in `/pages/` with shared UI theme.
            - **Dataset:** `assets/train.csv` (synthetic academic dataset).
            - **Services:** shared helpers in `/services/` for loading data and UI styling.
            """
        )


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
            print("\nRisk & Scenario Simulation is UI-focused. Use Streamlit for full functionality.")
            input("\nPress ENTER to return to menu...")
        elif choice == "4":
            print("\nCloud Analytics is UI-focused. Use Streamlit for full functionality.")
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
