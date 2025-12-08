# services/ui_service.py

import matplotlib.pyplot as plt

# ============================================
# GLOBAL THEME CONFIGURATION
# ============================================

PRIMARY_COLOR = "#013A63"   # Deep navy blue
ACCENT_COLOR = "#FFD700"    # Gold
LIGHT_BG = "#F6F6F6"
CARD_BG = "white"


def apply_global_styles():
    """
    Inject global CSS styling for all Streamlit pages.
    This function is only executed in Streamlit mode.
    """
    import streamlit as st  # Imported locally to avoid CLI warnings

    st.markdown(
        f"""
        <style>
            .block-container {{
                padding: 2rem 4rem !important;
            }}

            h1, h2, h3, h4 {{
                color: {PRIMARY_COLOR};
                font-weight: 700;
            }}

            .kpi-card {{
                background: {CARD_BG};
                padding: 1.2rem;
                border-radius: 12px;
                border: 1px solid #ddd;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                text-align: center;
            }}

            .kpi-value {{
                font-size: 2rem;
                font-weight: 700;
                color: {PRIMARY_COLOR};
            }}

            .kpi-label {{
                font-size: 0.9rem;
                color: #666;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title: str, icon: str = "📌"):
    """
    Render a formatted section title with an icon and divider.
    """
    import streamlit as st
    st.markdown(f"### {icon} {title}")
    st.markdown("---")


def render_kpi_cards(metrics: dict):
    """
    Render KPI cards in a horizontal layout.
    Example input:
        {
            "Average Score": "4.2",
            "Total Passengers": "12000"
        }
    """
    import streamlit as st

    cols = st.columns(len(metrics))
    for idx, (label, value) in enumerate(metrics.items()):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_chart(fig, use_full_width: bool = False):
    """
    Display a chart with consistent formatting and layout.
    """
    import streamlit as st

    fig.tight_layout()
    st.pyplot(fig, clear_figure=True, use_container_width=use_full_width)
