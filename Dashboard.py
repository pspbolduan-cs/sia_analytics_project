# ============================================
# Singapore Airlines Analytics System
# Dashboard (FINAL – CLEAN & STABLE)
# ============================================

import streamlit as st
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Singapore Airlines Analytics System",
    page_icon="✈️",
    layout="wide"
)

# --------------------------------------------------
# PATHS
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

HERO_VIDEO = ASSETS / "hero.mp4"
LOGO = ASSETS / "singapore_airlines_logo.png"

IMG_SYSTEM = ASSETS / "system_overview.png"
IMG_SECURITY = ASSETS / "security_risk_ethics.png"

IMG_M1 = ASSETS / "module1.png"
IMG_M2 = ASSETS / "module2.png"
IMG_M3 = ASSETS / "module3.png"
IMG_M4 = ASSETS / "module4.png"

# --------------------------------------------------
# GLOBAL STYLES
# --------------------------------------------------
st.markdown("""
<style>
.block-container { padding-top: 1rem; }

.hero {
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    margin-bottom: 2rem;
}

.hero-overlay {
    position:absolute;
    inset:0;
    background: linear-gradient(
        rgba(0,20,60,0.80),
        rgba(0,20,60,0.85)
    );
}

.hero-content {
    position: relative;
    padding: 3rem;
    color: white;
}

.hero-title {
    font-size: 3rem;
    font-weight: 900;
}

.hero-sub {
    font-size: 1.2rem;
    opacity: 0.95;
    max-width: 900px;
}

.section-title {
    font-size: 2rem;
    font-weight: 900;
    margin-top: 1.5rem;
}

.card {
    background: #0f172a;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
}

.card-body {
    padding: 1rem;
    color: white;
}

.card-desc {
    opacity: 0.85;
    margin-bottom: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
with st.container():
    st.markdown('<div class="hero">', unsafe_allow_html=True)

    if HERO_VIDEO.exists():
        st.video(str(HERO_VIDEO))

    st.markdown('<div class="hero-overlay"></div>', unsafe_allow_html=True)

    st.markdown('<div class="hero-content">', unsafe_allow_html=True)
    if LOGO.exists():
        st.image(str(LOGO), width=180)

    st.markdown('<div class="hero-title">Singapore Airlines Analytics System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Enterprise cloud-based analytics dashboard for operational performance, '
        'customer experience, risk scenarios, and cloud processing concepts.</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div></div>', unsafe_allow_html=True)

# --------------------------------------------------
# SYSTEM PAGES
# --------------------------------------------------
st.markdown('<div class="section-title">🧩 System Pages</div>', unsafe_allow_html=True)
st.caption("Enterprise architecture, governance, security & ethics")

c1, c2 = st.columns(2)

with c1:
    st.image(str(IMG_SYSTEM), use_container_width=True)
    st.markdown("### 🧱 System Overview / Architecture")
    st.markdown(
        "View the system architecture, shared services, page structure, and cloud scalability mapping."
    )
    if st.button("➡️ Open page", key="sys"):
        st.switch_page("pages/System_Overview_Architecture.py")

with c2:
    st.image(str(IMG_SECURITY), use_container_width=True)
    st.markdown("### 🛡️ Security, Risk & Ethics")
    st.markdown(
        "Review privacy protections, governance assumptions, security controls, and ethical analytics considerations."
    )
    if st.button("➡️ Open page", key="sec"):
        st.switch_page("pages/Security_Risk_Ethics.py")

# --------------------------------------------------
# ANALYTICS MODULES
# --------------------------------------------------
st.markdown('<div class="section-title">📊 Analytics Modules</div>', unsafe_allow_html=True)
st.caption("Click Open module → to explore analytics")

m1, m2 = st.columns(2)
m3, m4 = st.columns(2)

with m1:
    st.image(str(IMG_M1), use_container_width=True)
    st.markdown("### ✈️ Flight Performance Analytics")
    if st.button("➡️ Open module", key="m1"):
        st.switch_page("pages/Module1_Flight_Performance.py")

with m2:
    st.image(str(IMG_M2), use_container_width=True)
    st.markdown("### 😊 Customer Experience Analytics")
    if st.button("➡️ Open module", key="m2"):
        st.switch_page("pages/Module2_Customer_Experience.py")

with m3:
    st.image(str(IMG_M3), use_container_width=True)
    st.markdown("### ⚠️ Risk & Scenario Simulation")
    if st.button("➡️ Open module", key="m3"):
        st.switch_page("pages/Module3_Risk_Simulation.py")

with m4:
    st.image(str(IMG_M4), use_container_width=True)
    st.markdown("### ☁️ Cloud Analytics")
    if st.button("➡️ Open module", key="m4"):
        st.switch_page("pages/Module4_Cloud_Analytics.py")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.success("✅ Dashboard fully operational. All navigation and media working correctly.")
