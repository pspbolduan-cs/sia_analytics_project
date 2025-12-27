# ============================================================
# Author: Philippe Bolduan
# Page: System Overview / Architecture
# Course: CN6001 Enterprise Application & Cloud Computing
#
# Purpose:
# - Strengthen enterprise design / architecture marks
# - Explain modular layout, shared services, scalability mapping
# ============================================================

from __future__ import annotations

import streamlit as st


def _safe_apply_global_styles() -> bool:
    try:
        from services.ui_service import apply_global_styles
        apply_global_styles()
        return True
    except Exception:
        return False


def _render_html(html: str) -> None:
    cleaned = "\n".join(line.lstrip() for line in html.splitlines()).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def _inject_css() -> None:
    PRIMARY_NAVY = "#002663"
    BACKGROUND_CREAM = "#F5F3EE"
    TEXT_GREY = "#555555"

    _render_html(
        f"""
        <style>
          .stApp {{ background-color: {BACKGROUND_CREAM}; }}
          h1, h2, h3 {{ color: {PRIMARY_NAVY}; }}

          .sia-subtext {{
              color: {TEXT_GREY};
              font-size: 1rem;
              margin-top: -6px;
          }}

          .card {{
            background: #ffffff;
            border-radius: 18px;
            padding: 16px 18px;
            border: 1px solid rgba(0,0,0,0.06);
            box-shadow: 0 12px 35px rgba(0,0,0,0.08);
            margin-top: 14px;
          }}
          .card h3 {{
            margin: 0 0 8px 0;
            font-size: 1.15rem;
            font-weight: 950;
            color: {PRIMARY_NAVY};
          }}
          .card p, .card li {{
            color: rgba(0,0,0,0.70);
            font-size: 1.02rem;
            line-height: 1.55;
          }}
          .kbd {{
            padding: 2px 8px;
            border-radius: 10px;
            background: rgba(0,0,0,0.06);
            border: 1px solid rgba(0,0,0,0.08);
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-weight: 800;
          }}

          /* Floating back button */
          .sia-back-float {{
              position: fixed;
              top: 90px;
              right: 18px;
              z-index: 999999;
              display: inline-flex;
              align-items: center;
              gap: 10px;
              padding: 10px 14px;
              border-radius: 999px;
              background: rgba(255,255,255,0.94);
              border: 1px solid rgba(0,0,0,0.10);
              box-shadow: 0 10px 28px rgba(0,0,0,0.14);
              backdrop-filter: blur(6px);
          }}
          .sia-back-float a {{
              text-decoration: none;
              font-weight: 800;
              color: {PRIMARY_NAVY};
              font-size: 0.98rem;
          }}
          .sia-back-float a:hover {{ text-decoration: underline; }}

          /* Diagram container */
          .diagramWrap {{
            background: linear-gradient(135deg, rgba(0,38,99,0.10), rgba(0,38,99,0.02));
            border: 1px solid rgba(0,0,0,0.06);
            border-radius: 18px;
            padding: 14px;
            margin-top: 14px;
          }}
        </style>
        """
    )


def _render_back_hover_only() -> None:
    _render_html(
        """
        <div class="sia-back-float">
            🏠 <a href="./" target="_self">Back to Dashboard</a>
        </div>
        """
    )


def _architecture_svg() -> str:
    # Inline SVG so you don't need any extra assets.
    return """
    <div class="diagramWrap">
      <svg width="100%" height="320" viewBox="0 0 1100 320" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <style>
            .box{ fill:#ffffff; stroke:rgba(0,0,0,0.12); stroke-width:2; rx:18; }
            .title{ font: 900 22px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill:#002663; }
            .txt{ font: 700 16px ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto; fill:rgba(0,0,0,0.68); }
            .arrow{ stroke:rgba(0,0,0,0.35); stroke-width:3; marker-end:url(#m); }
          </style>
          <marker id="m" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
            <path d="M0,0 L12,6 L0,12 Z" fill="rgba(0,0,0,0.35)" />
          </marker>
        </defs>

        <!-- Boxes -->
        <rect class="box" x="30"  y="40"  width="240" height="110" rx="18"/>
        <text class="title" x="60" y="78">User</text>
        <text class="txt"   x="60" y="110">Browser / CLI</text>

        <rect class="box" x="310" y="40"  width="300" height="110" rx="18"/>
        <text class="title" x="340" y="78">Dashboard</text>
        <text class="txt"   x="340" y="110">Navigation + overview</text>

        <rect class="box" x="650" y="40"  width="420" height="110" rx="18"/>
        <text class="title" x="680" y="78">Shared Services</text>
        <text class="txt"   x="680" y="110">data_service + ui_service</text>

        <rect class="box" x="310" y="190" width="760" height="110" rx="18"/>
        <text class="title" x="340" y="228">Pages</text>
        <text class="txt"   x="340" y="258">System Overview • Security/Risk/Ethics • Modules 1–4</text>

        <rect class="box" x="30"  y="190" width="240" height="110" rx="18"/>
        <text class="title" x="60" y="228">Dataset</text>
        <text class="txt"   x="60" y="258">assets/train.csv</text>

        <!-- Arrows -->
        <line class="arrow" x1="270" y1="95" x2="310" y2="95"/>
        <line class="arrow" x1="610" y1="95" x2="650" y2="95"/>
        <line class="arrow" x1="820" y1="150" x2="820" y2="190"/>
        <line class="arrow" x1="270" y1="245" x2="310" y2="245"/>
      </svg>

      <div style="margin-top:10px; color:rgba(0,0,0,0.68); font-weight:700;">
        Architecture summary: a <b>dashboard</b> routes users to pages, which rely on <b>shared services</b> for consistent
        data ingestion and styling. All modules use the same <span class="kbd">assets/train.csv</span> dataset.
      </div>
    </div>
    """


def run():
    st.set_page_config(page_title="System Overview / Architecture", page_icon="🏗️", layout="wide")

    _safe_apply_global_styles()
    _inject_css()
    _render_back_hover_only()

    st.title("🏗️ System Overview / Architecture")
    _render_html(
        """
        <div class="sia-subtext">
          This page explains the enterprise-style architecture of the Singapore Airlines Analytics System:
          modular pages, shared services, and cloud scalability mapping.
        </div>
        """
    )

    _render_html(_architecture_svg())

    _render_html(
        """
        <div class="card">
          <h3>Core components</h3>
          <ul>
            <li><b>Dashboard:</b> single entry point, navigation hub, and system overview.</li>
            <li><b>Pages (Modules 1–4):</b> analytics functions with interactive UI + charts.</li>
            <li><b>System Pages:</b> governance-friendly pages (architecture + security/ethics).</li>
            <li><b>Shared Services:</b> reusable functions for <span class="kbd">load_data()</span> and global UI theme.</li>
            <li><b>Dataset:</b> synthetic <span class="kbd">assets/train.csv</span> (academic use).</li>
          </ul>
        </div>
        """
    )

    _render_html(
        """
        <div class="card">
          <h3>Scalability mapping (cloud-ready)</h3>
          <ul>
            <li><b>Storage upgrade:</b> replace CSV with object storage (e.g., S3 / Blob Storage).</li>
            <li><b>Batch analytics:</b> run aggregation jobs on schedule (serverless / container jobs).</li>
            <li><b>Streaming analytics:</b> near real-time ingestion using event streams (simulated in Module 4).</li>
            <li><b>Observability:</b> measure load/compute time and monitor performance trends.</li>
          </ul>
        </div>
        """
    )

    with st.expander("Folder structure (recommended)"):
        st.code(
            """project_root/
  Dashboard.py
  assets/
    train.csv
    hero.mp4
    singapore_airlines_logo.png
    module1.png module2.png module3.png module4.png
  pages/
    System_Overview_Architecture.py
    Security_Risk_Ethics.py
    Module1_Flight_Performance.py
    Module2_Customer_Experience.py
    Module3_Risk_Simulation.py
    Module4_Cloud_Analytics.py
  services/
    data_service.py
    ui_service.py
""",
            language="text",
        )


# Streamlit runs the script top-to-bottom
run()
