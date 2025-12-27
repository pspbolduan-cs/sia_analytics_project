# ============================================
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
    import streamlit.components.v1 as components
    from pathlib import Path
    import base64

    # Optional global styles (safe)
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
    # PATHS
    # ---------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent
    ASSETS_DIR = BASE_DIR / "assets"

    PATHS = {
        "hero_mp4": ASSETS_DIR / "hero.mp4",
        "logo": ASSETS_DIR / "singapore_airlines_logo.png",
        "m1": ASSETS_DIR / "module1.png",
        "m2": ASSETS_DIR / "module2.png",
        "m3": ASSETS_DIR / "module3.png",
        "m4": ASSETS_DIR / "module4.png",
        "sys_overview": ASSETS_DIR / "system_overview.png",
        "sys_security": ASSETS_DIR / "security_risk_ethics.png",
    }

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

    def _to_video_uri(p: Path) -> str:
        if not p.exists():
            return ""
        b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
        return f"data:video/mp4;base64,{b64}"

    # Data URIs
    hero_video_uri = _to_video_uri(PATHS["hero_mp4"])
    logo_uri = _to_data_uri(PATHS["logo"], _mime_for_image(PATHS["logo"]))

    m1_uri = _to_data_uri(PATHS["m1"], _mime_for_image(PATHS["m1"]))
    m2_uri = _to_data_uri(PATHS["m2"], _mime_for_image(PATHS["m2"]))
    m3_uri = _to_data_uri(PATHS["m3"], _mime_for_image(PATHS["m3"]))
    m4_uri = _to_data_uri(PATHS["m4"], _mime_for_image(PATHS["m4"]))

    sys1_uri = _to_data_uri(PATHS["sys_overview"], _mime_for_image(PATHS["sys_overview"]))
    sys2_uri = _to_data_uri(PATHS["sys_security"], _mime_for_image(PATHS["sys_security"]))

    # ---------------------------------------------------
    # OPTIONAL DEBUG (sidebar)
    # ---------------------------------------------------
    with st.sidebar.expander("🛠 Debug (assets)", expanded=False):
        missing = [k for k, p in PATHS.items() if not p.exists()]
        st.write("Assets folder:", str(ASSETS_DIR))
        if missing:
            st.error("Missing files:")
            for k in missing:
                st.write(f"- {k}: {PATHS[k].name}")
        else:
            st.success("All assets found ✅")

    # ---------------------------------------------------
    # HTML/CSS (render via components.html so it NEVER escapes)
    # ---------------------------------------------------
    def card(title, emoji, desc, hint, href_path, img_uri, cta_text):
        img_html = f"<img src='{img_uri}' alt='{title}'>" if img_uri else ""
        return f"""
        <div class="moduleCard">
          <div class="thumbWrap">
            {img_html}
            <div class="thumbShade"></div>
          </div>

          <div class="moduleInner">
            <div class="moduleTitleRow">
              <span style="font-size:1.35rem;">{emoji}</span><span>{title}</span>
            </div>
            <div class="moduleDesc">{desc}</div>

            <div class="ctaRow">
              <a class="ctaBtn" href="/{href_path}" target="_self">➡️ {cta_text} →</a>
              <span class="ctaHint">{hint}</span>
            </div>
          </div>
        </div>
        """

    hero_video_block = (
        f"""
        <video class="heroVideo" autoplay muted loop playsinline>
          <source src="{hero_video_uri}" type="video/mp4" />
        </video>
        """
        if hero_video_uri
        else ""
    )

    logo_block = (
        f"""
        <div class="logoChip">
          <img src="{logo_uri}" alt="Singapore Airlines logo">
        </div>
        """
        if logo_uri
        else ""
    )

    html = f"""
    <style>
      .block-container {{ padding-top: 1.2rem !important; }}

      .heroWrap{{
        position: relative;
        border-radius: 26px;
        overflow: hidden;
        margin-bottom: 26px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.22);
        border: 1px solid rgba(255,255,255,0.10);
        min-height: 350px;
      }}
      .heroVideo{{
        position:absolute; inset:0;
        width:100%; height:100%;
        object-fit:cover;
        opacity:0.85;
        z-index:0;
      }}
      .heroOverlay{{
        position:absolute; inset:0;
        background: linear-gradient(135deg,
          rgba(0,26,77,0.92) 0%,
          rgba(0,58,128,0.70) 45%,
          rgba(0,26,77,0.92) 100%);
        z-index:1;
      }}
      .heroInner{{
        position:relative;
        z-index:2;
        padding: 2.2rem 2.4rem;
        display:flex;
        gap: 22px;
        align-items:flex-start;
        flex-wrap: wrap;
      }}
      .logoChip{{
        background: rgba(255,255,255,0.92);
        border-radius: 18px;
        padding: 12px 14px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.18);
        border: 1px solid rgba(255,255,255,0.45);
        display:flex;
        align-items:center;
        justify-content:center;
      }}
      .logoChip img{{ height: 64px; width:auto; display:block; }}

      .tagRow{{ display:flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }}
      .tagPill{{
        display:inline-flex; align-items:center; gap:8px;
        padding: 9px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.22);
        color: rgba(255,255,255,0.92);
        font-weight: 800;
        font-size: 0.95rem;
        backdrop-filter: blur(6px);
      }}
      .tagDot{{ width: 10px; height: 10px; border-radius: 999px; background: rgba(255,255,255,0.75); display:inline-block; }}
      .kbd{{
        padding: 2px 8px;
        border-radius: 10px;
        background: rgba(0,0,0,0.22);
        border: 1px solid rgba(255,255,255,0.16);
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-weight: 800;
      }}

      .sectionTitle{{
        font-size: 2.2rem;
        font-weight: 950;
        letter-spacing: -0.5px;
        margin: 0 0 0.3rem 0;
        color: #0b2c5f;
      }}
      .sectionSub{{
        color: rgba(0,0,0,0.60);
        font-size: 1.05rem;
        margin-bottom: 1.1rem;
      }}

      .moduleGrid{{
        display:grid;
        grid-template-columns: 1fr 1fr;
        gap: 18px;
      }}
      @media (max-width: 980px){{
        .moduleGrid{{ grid-template-columns: 1fr; }}
      }}

      .moduleCard{{
        background: #0f172a;
        border-radius: 22px;
        overflow:hidden;
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 18px 45px rgba(0,0,0,0.18);
        transition: transform .15s ease, box-shadow .15s ease;
      }}
      .moduleCard:hover{{
        transform: translateY(-2px);
        box-shadow: 0 22px 55px rgba(0,0,0,0.22);
      }}

      .thumbWrap{{
        height: 220px;
        width: 100%;
        position: relative;
        overflow: hidden;
        background: #0b1224;
      }}
      .thumbWrap img{{
        width:100%;
        height:100%;
        object-fit: cover;
        display:block;
      }}
      .thumbShade{{
        position:absolute;
        inset:0;
        background: linear-gradient(180deg, rgba(0,0,0,0.05) 0%, rgba(0,0,0,0.25) 100%);
      }}

      .moduleInner{{
        padding: 16px 18px 16px 18px;
        color: rgba(255,255,255,0.92);
      }}
      .moduleTitleRow{{
        display:flex;
        align-items:center;
        gap: 10px;
        font-size: 1.28rem;
        font-weight: 950;
        margin-bottom: 6px;
      }}
      .moduleDesc{{
        color: rgba(255,255,255,0.74);
        font-size: 1.02rem;
        line-height: 1.45;
        margin-bottom: 12px;
      }}
      .ctaRow{{
        display:flex;
        align-items:center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
      }}
      .ctaBtn{{
        display:inline-flex;
        align-items:center;
        gap: 10px;
        padding: 10px 14px;
        border-radius: 14px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.20);
        color: rgba(255,255,255,0.95);
        font-weight: 900;
        text-decoration: none;
      }}
      .ctaBtn:hover{{ background: rgba(255,255,255,0.18); }}
      .ctaHint{{ color: rgba(255,255,255,0.70); font-weight: 800; }}

      .infoCard{{
        background: #ffffff;
        border-radius: 18px;
        padding: 16px 18px;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 12px 35px rgba(0,0,0,0.08);
        margin-top: 18px;
      }}
      .infoCard h3{{
        margin: 0 0 8px 0;
        font-size: 1.25rem;
        font-weight: 950;
        color: #0b2c5f;
      }}
      .infoCard ul{{
        margin: 0;
        padding-left: 18px;
        color: rgba(0,0,0,0.70);
        font-size: 1.02rem;
        line-height: 1.55;
      }}
    </style>

    <div class="heroWrap">
      {hero_video_block}
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

          {"" if hero_video_uri else "<div style='margin-top:12px; color:rgba(255,255,255,0.90); font-weight:900;'>⚠️ Missing <span class='kbd'>assets/hero.mp4</span></div>"}
          {"" if logo_uri else "<div style='margin-top:8px; color:rgba(255,255,255,0.90); font-weight:900;'>⚠️ Missing <span class='kbd'>assets/singapore_airlines_logo.png</span></div>"}
        </div>
      </div>
    </div>

    <div class="sectionTitle">📌 What this dashboard does</div>
    <div class="sectionSub">A single entry point that explains the system and links to analytics modules + system governance pages.</div>

    <div class="infoCard">
      <h3>How to use</h3>
      <ul>
        <li>Start here and open a module using <b>Open module</b>.</li>
        <li>Each analytics module offers interactive controls + charts.</li>
        <li>Risk Simulation explains uncertainty (probability, percentiles, worst-case).</li>
        <li>Cloud Analytics demonstrates scalable processing concepts (batch vs streaming).</li>
      </ul>
    </div>

    <div class="infoCard">
      <h3>Data & concepts</h3>
      <ul>
        <li><b>Dataset:</b> synthetic <span class="kbd">assets/train.csv</span> (academic use).</li>
        <li><b>Architecture:</b> modular pages + shared services (data / UI helpers).</li>
        <li><b>Governance:</b> dedicated pages cover architecture + security/risk/ethics.</li>
        <li><b>UI + CLI:</b> web UI for visuals + menu-driven CLI for quick summaries.</li>
      </ul>
    </div>

    <div style="height:18px;"></div>
    <div class="sectionTitle">🧩 System Pages</div>
    <div class="sectionSub">These pages strengthen enterprise design + governance criteria (architecture, security, risk & ethics).</div>

    <div class="moduleGrid">
      {card(
        "System Overview / Architecture",
        "🏗️",
        "View the system architecture, shared services, page structure, and cloud scalability mapping.",
        "Enterprise design + scalability",
        "pages/System_Overview_Architecture.py",
        sys1_uri,
        "Open page"
      )}

      {card(
        "Security, Risk & Ethics",
        "🛡️",
        "Review privacy protections, governance assumptions, security controls, and ethical analytics considerations.",
        "LO6: protection + governance",
        "pages/Security_Risk_Ethics.py",
        sys2_uri,
        "Open page"
      )}
    </div>

    <div style="height:18px;"></div>
    <div class="sectionTitle">📊 Analytics Modules</div>
    <div class="sectionSub">Click <b>Open module →</b> to navigate. Each module uses the same theme and dataset service.</div>

    <div class="moduleGrid">
      {card(
        "Flight Performance Analytics",
        "✈️",
        "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
        "Interactive KPIs & charts",
        "pages/Module1_Flight_Performance.py",
        m1_uri,
        "Open module"
      )}

      {card(
        "Customer Experience Analytics",
        "😊",
        "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
        "Service quality insights",
        "pages/Module2_Customer_Experience.py",
        m2_uri,
        "Open module"
      )}

      {card(
        "Risk & Scenario Simulation",
        "⚠️",
        "Model operational uncertainty using Monte Carlo simulation and scenario-based disruption controls.",
        "Probabilities, percentiles, worst-case outcomes",
        "pages/Module3_Risk_Simulation.py",
        m3_uri,
        "Open module"
      )}

      {card(
        "Cloud Analytics",
        "☁️",
        "Demonstrate scalable processing concepts and cloud-oriented analytics patterns.",
        "Batch vs streaming + scaling concepts",
        "pages/Module4_Cloud_Analytics.py",
        m4_uri,
        "Open module"
      )}
    </div>
    """

    # IMPORTANT:
    # Use components.html so Streamlit does NOT escape HTML (prevents the "code block" issue)
    components.html(html, height=2050, scrolling=True)


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
