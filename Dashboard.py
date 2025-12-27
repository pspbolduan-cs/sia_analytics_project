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
    from services.ui_service import apply_global_styles

    st.set_page_config(
        page_title="SIA Dashboard",
        page_icon="🏠",
        layout="wide",
    )

    apply_global_styles()

    # ----------------------
    # Helpers
    # ----------------------
    def _render_html(html: str):
        st.markdown(html, unsafe_allow_html=True)

    def _page_link(page_path: str, label: str, icon: str = ""):
        """
        Prefer Streamlit-native navigation when available.
        Falls back to a normal link if page_link isn't supported.
        """
        try:
            st.page_link(page_path, label=label, icon=icon)
        except Exception:
            page_name = page_path.split("/")[-1].replace(".py", "")
            _render_html(f'<a href="/{page_name}" target="_self" class="plainLink">{icon} {label}</a>')

    # ----------------------
    # CSS (dashboard-only)
    # ----------------------
    _render_html(
        """
        <style>
            .plainLink { text-decoration: none; color: inherit; font-weight: 700; }

            .heroWrap {
                position: relative;
                border-radius: 24px;
                overflow: hidden;
                margin-bottom: 2.2rem;
                box-shadow: 0 18px 50px rgba(0,0,0,0.24);
                border: 1px solid rgba(255,255,255,0.12);
            }
            .heroInner {
                position: relative;
                padding: 3.2rem 3.0rem 2.7rem 3.0rem;
                z-index: 2;
            }
            .heroVideo {
                position: absolute;
                inset: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
                opacity: 0.55;
                z-index: 0;
                filter: contrast(1.05) saturate(1.05);
            }
            .heroOverlay {
                position: absolute;
                inset: 0;
                background: linear-gradient(135deg,
                    rgba(0,26,77,0.92) 0%,
                    rgba(0,58,128,0.78) 60%,
                    rgba(0,26,77,0.86) 100%
                );
                z-index: 1;
            }
            .heroTitle {
                font-size: 3.15rem;
                font-weight: 950;
                letter-spacing: -1px;
                margin: 0 0 0.35rem 0;
                color: #FFFFFF;
                line-height: 1.05;
            }
            .heroSub {
                color: rgba(255,255,255,0.88);
                font-size: 1.15rem;
                margin: 0;
                max-width: 70ch;
            }
            .tagRow { display:flex; gap: 12px; flex-wrap: wrap; margin-top: 1.25rem; }
            .tagPill {
                display:inline-flex; align-items:center; gap:10px;
                padding: 10px 14px;
                border-radius: 999px;
                background: rgba(255,255,255,0.14);
                color: rgba(255,255,255,0.92);
                border: 1px solid rgba(255,255,255,0.16);
                font-weight: 800;
                letter-spacing: 0.2px;
            }
            .tagDot {
                width: 10px; height: 10px; border-radius: 999px;
                background: rgba(255,237,77,0.95);
                box-shadow: 0 0 18px rgba(255,237,77,0.55);
            }
            .logoChip {
                display:inline-flex;
                align-items:center;
                gap:12px;
                background: rgba(255,255,255,0.92);
                border-radius: 16px;
                padding: 10px 12px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.18);
                margin-bottom: 18px;
            }
            .logoChip img { height: 56px; width: auto; }

            .sectionH2 {
                margin-top: 0.5rem;
                margin-bottom: 0.8rem;
                font-size: 2.25rem;
                font-weight: 950;
                color: #002663;
                letter-spacing: -0.6px;
            }
            .sectionNote {
                color: #5B5B5B;
                font-size: 1.02rem;
                margin-top: -6px;
                margin-bottom: 16px;
            }

            .gridWrap {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 18px;
                margin-top: 14px;
            }
            @media (max-width: 980px) {
                .gridWrap { grid-template-columns: 1fr; }
                .heroInner { padding: 2.4rem 1.6rem 2.1rem 1.6rem; }
                .heroTitle { font-size: 2.45rem; }
            }

            .moduleCard {
                background: rgba(255,255,255,0.96);
                border-radius: 22px;
                border: 1px solid #E5E7EB;
                box-shadow: 0 10px 30px rgba(0,0,0,0.08);
                overflow: hidden;
                transition: transform .12s ease, box-shadow .12s ease;
            }
            .moduleCard:hover {
                transform: translateY(-2px);
                box-shadow: 0 18px 44px rgba(0,0,0,0.12);
            }
            .moduleInner {
                padding: 18px 18px 16px 18px;
            }
            .moduleTitleRow {
                display:flex;
                align-items:center;
                gap: 12px;
                font-size: 1.35rem;
                font-weight: 950;
                color: #002663;
                margin-bottom: 10px;
            }
            .moduleDesc {
                color: #5B5B5B;
                font-size: 1.02rem;
                line-height: 1.45;
                margin-bottom: 14px;
                min-height: 44px;
            }
            .ctaRow {
                display:flex;
                align-items:center;
                justify-content: space-between;
                gap: 12px;
                flex-wrap: wrap;
            }
            .ctaBtn {
                display:inline-flex;
                align-items:center;
                gap: 10px;
                padding: 10px 14px;
                border-radius: 14px;
                background: #002663;
                color: #FFFFFF;
                font-weight: 900;
                text-decoration: none;
                border: 1px solid rgba(255,255,255,0.12);
            }
            .ctaHint {
                color: #6B7280;
                font-weight: 700;
                font-size: 0.95rem;
            }

            .thumb {
                height: 140px;
                width: 100%;
                object-fit: cover;
                display: block;
                filter: contrast(1.02) saturate(1.02);
            }

            .infoGrid {
                display: grid;
                grid-template-columns: 1.15fr 0.85fr;
                gap: 18px;
                margin-top: 18px;
            }
            @media (max-width: 980px) {
                .infoGrid { grid-template-columns: 1fr; }
            }

            .panel {
                background: rgba(255,255,255,0.96);
                border-radius: 22px;
                border: 1px solid #E5E7EB;
                box-shadow: 0 10px 30px rgba(0,0,0,0.08);
                padding: 18px;
            }
            .panelH3 {
                margin: 0 0 10px 0;
                font-size: 1.35rem;
                font-weight: 950;
                color: #002663;
                letter-spacing: -0.2px;
            }
            .bullets {
                margin: 0;
                padding-left: 18px;
                color: #4B5563;
                line-height: 1.55;
                font-size: 1.0rem;
            }
            .kpiRow {
                display:grid;
                grid-template-columns: repeat(3, minmax(0,1fr));
                gap: 12px;
                margin-top: 10px;
            }
            @media (max-width: 980px) {
                .kpiRow { grid-template-columns: 1fr; }
            }
            .kpi {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                padding: 14px 14px;
                box-shadow: 0 8px 22px rgba(0,0,0,0.06);
            }
            .kpiLabel { color:#6B7280; font-weight:800; font-size: 0.92rem; margin-bottom: 6px; }
            .kpiValue { color:#002663; font-weight:950; font-size: 1.65rem; line-height: 1.1; }
            .kpiSub { color:#6B7280; font-weight:700; font-size: 0.92rem; margin-top: 6px; }

            .footer {
                margin-top: 26px;
                padding: 10px 2px;
                color: #6B7280;
                font-size: 0.95rem;
            }
        </style>
        """
    )

    # =============================================================
    # HERO (video background)
    # =============================================================
    hero_video_src = "assets/hero.mp4"
    logo_src = "assets/singapore_airlines_logo.png"

    _render_html(
        f"""
        <div class="heroWrap">
            <video class="heroVideo" autoplay muted loop playsinline>
                <source src="{hero_video_src}" type="video/mp4">
            </video>
            <div class="heroOverlay"></div>

            <div class="heroInner">
                <div class="logoChip">
                    <img src="{logo_src}" alt="Singapore Airlines logo">
                </div>

                <div class="heroTitle">Singapore Airlines Analytics System</div>
                <p class="heroSub">
                    Enterprise cloud-based analytics dashboard for operational performance, customer experience,
                    risk scenarios, and cloud processing concepts.
                </p>

                <div class="tagRow">
                    <span class="tagPill"><span class="tagDot"></span>Streamlit UI</span>
                    <span class="tagPill"><span class="tagDot"></span>CLI Supported</span>
                    <span class="tagPill"><span class="tagDot"></span>Synthetic Dataset (train.csv)</span>
                </div>
            </div>
        </div>
        """
    )

    # =============================================================
    # QUICK CONTEXT (so it’s obvious what the app does)
    # =============================================================
    _render_html('<div class="sectionH2">What this dashboard does</div>')
    _render_html(
        """
        <div class="sectionNote">
            This system demonstrates an end-to-end analytics pipeline for an airline using a synthetic dataset.
            You can explore performance metrics, customer experience indicators, operational risk simulations, and cloud processing concepts.
        </div>
        """
    )

    # Optional: small KPI row using the dataset (safe + fast)
    try:
        import pandas as pd
        from services.data_service import load_data

        df = load_data()
        rows = int(df.shape[0])

        # These column names vary across datasets, so we check safely.
        def first_col(candidates):
            cols_lower = {c.lower(): c for c in df.columns}
            for c in candidates:
                if c in df.columns:
                    return c
                if c.lower() in cols_lower:
                    return cols_lower[c.lower()]
            return None

        delay_col = first_col(["Departure Delay in Minutes", "DepDelay", "DepartureDelay", "departure_delay"])
        sat_col = first_col(["satisfaction", "Satisfaction", "satisfied", "Satisfaction label"])
        dist_col = first_col(["Flight Distance", "Distance", "flight_distance", "FlightDistance"])

        avg_delay = None
        if delay_col:
            s = pd.to_numeric(df[delay_col], errors="coerce").dropna()
            if len(s) > 0:
                avg_delay = float(s.mean())

        long_haul = None
        if dist_col:
            d = pd.to_numeric(df[dist_col], errors="coerce").dropna()
            if len(d) > 0:
                long_haul = float((d >= 3000).mean() * 100.0)

        sat_rate = None
        if sat_col:
            sc = df[sat_col].astype(str).str.lower()
            sat_rate = float(sc.isin(["satisfied", "yes", "1", "true"]).mean() * 100.0)

        _render_html(
            """
            <div class="kpiRow">
                <div class="kpi">
                    <div class="kpiLabel">Dataset size</div>
                    <div class="kpiValue">{rows}</div>
                    <div class="kpiSub">rows in train.csv</div>
                </div>
                <div class="kpi">
                    <div class="kpiLabel">Average departure delay</div>
                    <div class="kpiValue">{avg_delay}</div>
                    <div class="kpiSub">minutes (from dataset)</div>
                </div>
                <div class="kpi">
                    <div class="kpiLabel">Long-haul share</div>
                    <div class="kpiValue">{long_haul}</div>
                    <div class="kpiSub">distance ≥ 3000 km</div>
                </div>
            </div>
            """.format(
                rows=f"{rows:,}",
                avg_delay=f"{avg_delay:.1f}" if avg_delay is not None else "—",
                long_haul=f"{long_haul:.1f}%" if long_haul is not None else "—",
            )
        )
    except Exception:
        pass

    # =============================================================
    # MODULES (with images)
    # Put these 4 images into: assets/
    # - assets/module1.jpg
    # - assets/module2.jpg
    # - assets/module3.jpg
    # - assets/module4.jpg
    # =============================================================
    _render_html('<div class="sectionH2">Analytics Modules</div>')
    _render_html('<div class="sectionNote">Open any module to explore interactive KPIs, charts, and scenarios.</div>')

    modules = [
        {
            "title": "Flight Performance Analytics",
            "icon": "✈️",
            "desc": "Explore distance distribution, delay trends, crew/service indicators, and estimated fuel usage.",
            "page": "pages/Module1_Flight_Performance.py",
            "thumb": "assets/module1.jpg",
            "hint": "Operational KPIs & charts",
        },
        {
            "title": "Customer Experience Analytics",
            "icon": "😊",
            "desc": "Analyse satisfaction outcomes, service ratings, and behavioural indicators affecting passenger experience.",
            "page": "pages/Module2_Customer_Experience.py",
            "thumb": "assets/module2.jpg",
            "hint": "Service quality insights",
        },
        {
            "title": "Risk & Scenario Simulation",
            "icon": "⚠️",
            "desc": "Model operational uncertainty using delay-risk simulation and disruption scenarios with interactive controls.",
            "page": "pages/Module3_Risk_Simulation.py",
            "thumb": "assets/module3.jpg",
            "hint": "Simulation & resilience KPIs",
        },
        {
            "title": "Cloud Analytics",
            "icon": "☁️",
            "desc": "Demonstrate cloud processing concepts such as batch vs streaming and scalable execution patterns.",
            "page": "pages/Module4_Cloud_Analytics.py",
            "thumb": "assets/module4.jpg",
            "hint": "Batch/streaming concepts",
        },
    ]

    cards_html = ['<div class="gridWrap">']
    for m in modules:
        # Card header + image
        cards_html.append(
            f"""
            <div class="moduleCard">
                <img class="thumb" src="{m['thumb']}" alt="{m['title']} thumbnail">
                <div class="moduleInner">
                    <div class="moduleTitleRow">
                        <span style="font-size:1.35rem;">{m['icon']}</span>
                        <span>{m['title']}</span>
                    </div>
                    <div class="moduleDesc">{m['desc']}</div>
                    <div class="ctaRow">
                        <span class="ctaHint">{m['hint']}</span>
                        <span id="{m['page'].replace('/','_')}"></span>
                    </div>
                </div>
            </div>
            """
        )
    cards_html.append("</div>")
    _render_html("".join(cards_html))

    # After HTML cards, render real Streamlit buttons/links in the same order
    # (Streamlit elements can't be embedded directly inside the HTML card reliably)
    # So we show a clean row of buttons under the grid.
    c1, c2, c3, c4 = st.columns(4)
    cols = [c1, c2, c3, c4]
    for col, m in zip(cols, modules):
        with col:
            _page_link(m["page"], "Open module →", icon=m["icon"])

    # =============================================================
    # EXTRA SECTIONS THAT HELP MARKS + CLARITY
    # =============================================================
    _render_html('<div class="infoGrid">')

    # Left: project summary / how to use
    _render_html(
        """
        <div class="panel">
            <div class="panelH3">How to use</div>
            <ul class="bullets">
                <li>Start on this dashboard and open a module using the buttons above.</li>
                <li>Use sliders/filters inside modules to explore different operational conditions.</li>
                <li>Risk Simulation demonstrates uncertainty (probabilities, percentiles, worst-case outcomes).</li>
                <li>Cloud Analytics explains how analytics workloads run at scale (batch vs streaming).</li>
            </ul>
        </div>
        """
    )

    # Right: dataset + assumptions + cloud concepts
    _render_html(
        """
        <div class="panel">
            <div class="panelH3">Data & concepts</div>
            <ul class="bullets">
                <li><b>Dataset:</b> synthetic <code>assets/train.csv</code> (academic use only).</li>
                <li><b>Assumptions:</b> when a metric is missing (e.g., fuel cost), controlled simulation is used.</li>
                <li><b>Cloud concepts:</b> modular pages, shared services, scalable processing patterns, batch vs streaming.</li>
                <li><b>UI/CLI:</b> Streamlit web UI plus a menu-driven CLI for quick summaries.</li>
            </ul>
        </div>
        """
    )

    _render_html("</div>")

    # =============================================================
    # OPTIONAL: Architecture snapshot (simple + readable)
    # =============================================================
    with st.expander("System Architecture (quick view)", expanded=False):
        st.markdown(
            """
**Structure**
- `Dashboard.py` – entry point (UI + CLI)
- `pages/` – modules (Flight / Customer / Risk / Cloud)
- `services/` – shared styling + data loading helpers
- `assets/` – dataset + branding + media

**Why this matters**
- Clear separation of concerns (UI vs services vs modules)
- Easy for team collaboration and extension
            """
        )

    # =============================================================
    # Footer
    # =============================================================
    _render_html(
        """
        <div class="footer">
            CN6001 Enterprise Application & Cloud Computing — Coursework Project (Academic Demonstration).
        </div>
        """
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
            print("\n[CLI] Risk Simulation is visualization-focused.")
            print("Use Streamlit UI for full functionality.")
            input("\nPress ENTER to return to menu...")

        elif choice == "4":
            print("\n[CLI] Cloud Analytics is concept + visualization-focused.")
            print("Use Streamlit UI for full functionality.")
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
