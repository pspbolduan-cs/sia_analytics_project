# ============================================================
# Author: Philippe Bolduan
# Page: Security, Risk & Ethics
# Course: CN6001 Enterprise Application & Cloud Computing
#
# Purpose:
# - Explicitly cover LO6 (risk, security, protection)
# - Distinguish operational risk from data/security risk
# - Explain privacy and governance assumptions
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

          .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-top: 14px;
          }}
          @media (max-width: 980px) {{
            .grid {{ grid-template-columns: 1fr; }}
          }}

          .card {{
            background: #ffffff;
            border-radius: 18px;
            padding: 16px 18px;
            border: 1px solid rgba(0,0,0,0.06);
            box-shadow: 0 12px 35px rgba(0,0,0,0.08);
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

          .pill {{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding: 7px 10px;
            border-radius: 999px;
            background: rgba(0,38,99,0.08);
            border: 1px solid rgba(0,38,99,0.14);
            color: {PRIMARY_NAVY};
            font-weight: 900;
            margin-right: 8px;
            margin-bottom: 8px;
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


def run():
    st.set_page_config(page_title="Security, Risk & Ethics", page_icon="🛡️", layout="wide")

    _safe_apply_global_styles()
    _inject_css()
    _render_back_hover_only()

    st.title("🛡️ Security, Risk & Ethics")
    _render_html(
        """
        <div class="sia-subtext">
          This page explicitly addresses protection, governance, and ethical analytics considerations (LO6).
          It also clarifies the difference between operational risk (simulated) and security risk (data protection).
        </div>
        """
    )

    _render_html(
        """
        <div style="margin-top:10px;">
          <span class="pill">✅ Synthetic data</span>
          <span class="pill">🔐 Privacy-first</span>
          <span class="pill">🧭 Governance</span>
          <span class="pill">⚖️ Ethical analytics</span>
        </div>
        """
    )

    _render_html(
        """
        <div class="grid">
          <div class="card">
            <h3>Privacy & data handling</h3>
            <ul>
              <li><b>No PII:</b> the project uses a synthetic dataset (<b>assets/train.csv</b>) for academic demonstration.</li>
              <li><b>Read-only analytics:</b> the system is designed for analysis and reporting, not altering source data.</li>
              <li><b>Minimization:</b> only required columns are processed for each module’s charts and KPIs.</li>
              <li><b>Retention:</b> no long-term storage of user inputs; controls affect live visualizations only.</li>
            </ul>
          </div>

          <div class="card">
            <h3>Security controls (assumptions)</h3>
            <ul>
              <li><b>Access control:</b> in real deployment, restrict access via authentication (SSO / IAM).</li>
              <li><b>Secure storage:</b> encrypt at rest (object storage / managed DB), and encrypt in transit (TLS).</li>
              <li><b>Integrity:</b> validate schema + handle missing values to prevent incorrect reporting.</li>
              <li><b>Least privilege:</b> analytics services should read only what they need.</li>
            </ul>
          </div>
        </div>
        """
    )

    _render_html(
        """
        <div class="grid" style="margin-top:16px;">
          <div class="card">
            <h3>Risk categories (important distinction)</h3>
            <ul>
              <li><b>Operational risk:</b> delays, disruptions, and uncertainty (covered by the Risk Simulation module).</li>
              <li><b>Data risk:</b> bias, missing values, noisy metrics, and misleading trends if not validated.</li>
              <li><b>Security risk:</b> unauthorized access, leakage, tampering, and availability issues.</li>
            </ul>
            <p>
              This system models <b>operational risk</b> using simulation, while documenting <b>data + security risk</b>
              using enterprise protection assumptions.
            </p>
          </div>

          <div class="card">
            <h3>Ethical analytics & transparency</h3>
            <ul>
              <li><b>Decision support:</b> the dashboard supports human decisions; it does not automate critical actions.</li>
              <li><b>Transparency:</b> simulated values (e.g., fuel or disruption multipliers) are clearly labelled.</li>
              <li><b>Fair interpretation:</b> avoid overgeneralization; context matters (route, seasonality, operations).</li>
              <li><b>Accountability:</b> results should be reviewed by stakeholders before operational policy changes.</li>
            </ul>
          </div>
        </div>
        """
    )

    with st.expander("Suggested report paragraph (copy/paste)"):
        st.write(
            """
In this project, protection and governance requirements are addressed through privacy-first data handling and clear
enterprise security assumptions. The system uses a synthetic dataset (train.csv) that contains no personally
identifiable information (PII), supporting ethical academic use. In a real airline deployment, the application would
be protected through authentication/authorization (IAM or SSO), encryption in transit (TLS), encryption at rest, and
least-privilege permissions. The project also distinguishes operational risk (modelled via simulation) from data risk
(missing values, bias) and security risk (unauthorized access or tampering). Finally, the dashboard is designed as a
decision-support tool with transparent assumptions, ensuring outputs are interpreted responsibly.
"""
        )


run()
