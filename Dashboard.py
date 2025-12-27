# ============================================
# Author: Qian Zhu
# Date: 2025-12
# Singapore Airlines Analytics System
# Dashboard (Home Page)
# ============================================

import sys
import base64
from pathlib import Path
import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Singapore Airlines Analytics System",
    page_icon="🏠",
    layout="wide"
)

# --------------------------------------------------
# OPTIONAL GLOBAL STYLES
# --------------------------------------------------
try:
    from services.ui_service import apply_global_styles
    apply_global_styles()
except Exception:
    pass

# --------------------------------------------------
# PATHS
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

def img_uri(path):
    if not path.exists():
        return ""
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()

def video_uri(path):
    if not path.exists():
        return ""
    return "data:video/mp4;base64," + base64.b64encode(path.read_bytes()).decode()

# Assets
HERO_VIDEO = video_uri(ASSETS / "hero.mp4")
LOGO = img_uri(ASSETS / "singapore_airlines_logo.png")

MODULE_IMGS = {
    "m1": img_uri(ASSETS / "module1.png"),
    "m2": img_uri(ASSETS / "module2.png"),
    "m3": img_uri(ASSETS / "module3.png"),
    "m4": img_uri(ASSETS / "module4.png"),
    "sys": img_uri(ASSETS / "system_overview.png"),
    "sec": img_uri(ASSETS / "security_risk_ethics.png"),
}

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
.block-container { padding-top: 1.2rem; }

.hero {
  position: relative;
  border-radius: 26px;
  overflow: hidden;
  min-height: 380px;
  box-shadow: 0 20px 50px rgba(0,0,0,.25);
}
.hero video {
  position:absolute;
  width:100%;
  height:100%;
  object-fit:cover;
}
.hero::after {
  content:"";
  position:absolute;
  inset:0;
  background:linear-gradient(135deg,#001a4d 0%,#003a80cc 50%,#001a4d 100%);
}
.heroInner {
  position:relative;
  z-index:2;
  padding:2.2rem;
  color:white;
  display:flex;
  gap:20px;
  flex-wrap:wrap;
}
.logo {
  background:white;
  padding:12px;
  border-radius:16px;
}
.logo img { height:64px; }

.sectionTitle {
  font-size:2.2rem;
  font-weight:900;
  margin:1.6rem 0 .4rem;
}
.sectionSub { opacity:.65; margin-bottom:1rem; }

.grid {
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:18px;
}
@media(max-width:900px){
  .grid{grid-template-columns:1fr;}
}

.card {
  background:#0f172a;
  border-radius:22px;
  overflow:hidden;
  box-shadow:0 18px 45px rgba(0,0,0,.2);
}
.card img {
  width:100%;
  height:220px;
  object-fit:cover;
}
.cardBody {
  padding:16px;
  color:white;
}
.cardFooter {
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-top:12px;
}
.cardFooter a {
  background:rgba(255,255,255,.14);
  padding:10px 14px;
  border-radius:14px;
  text-decoration:none;
  color:white;
  font-weight:800;
}
.cardFooter span { opacity:.7; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown(f"""
<div class="hero">
  {"<video autoplay muted loop playsinline><source src='"+HERO_VIDEO+"' type='video/mp4'></video>" if HERO_VIDEO else ""}
  <div class="heroInner">
    <div class="logo"><img src="{LOGO}"></div>
    <div>
      <h1>Singapore Airlines Analytics System</h1>
      <p style="max-width:900px;opacity:.85;font-size:1.15rem">
        Enterprise cloud-based analytics dashboard for operational performance,
        customer experience, risk scenarios, and cloud processing concepts.
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SYSTEM PAGES
# --------------------------------------------------
st.markdown('<div class="sectionTitle">🧩 System Pages</div>', unsafe_allow_html=True)
st.markdown('<div class="sectionSub">Enterprise architecture, governance, security & ethics.</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="grid">

  <div class="card">
    <img src="{MODULE_IMGS['sys']}">
    <div class="cardBody">
      <h3>System Overview / Architecture</h3>
      <p>View system architecture, shared services, page structure and scalability.</p>
      <div class="cardFooter">
        <a href="/pages/System_Overview_Architecture.py">➡️ Open page →</a>
        <span>Enterprise design</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{MODULE_IMGS['sec']}">
    <div class="cardBody">
      <h3>Security, Risk & Ethics</h3>
      <p>Review privacy protections, governance assumptions and ethical analytics.</p>
      <div class="cardFooter">
        <a href="/pages/Security_Risk_Ethics.py">➡️ Open page →</a>
        <span>Governance</span>
      </div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ANALYTICS MODULES
# --------------------------------------------------
st.markdown('<div class="sectionTitle">📊 Analytics Modules</div>', unsafe_allow_html=True)
st.markdown('<div class="sectionSub">Click Open module → to explore analytics.</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="grid">

  <div class="card">
    <img src="{MODULE_IMGS['m1']}">
    <div class="cardBody">
      <h3>Flight Performance Analytics</h3>
      <p>Distance, delays, crew metrics and estimated fuel usage.</p>
      <div class="cardFooter">
        <a href="/pages/Module1_Flight_Performance.py">➡️ Open module →</a>
        <span>KPIs & charts</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{MODULE_IMGS['m2']}">
    <div class="cardBody">
      <h3>Customer Experience Analytics</h3>
      <p>Passenger satisfaction, service ratings and behaviour.</p>
      <div class="cardFooter">
        <a href="/pages/Module2_Customer_Experience.py">➡️ Open module →</a>
        <span>Insights</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{MODULE_IMGS['m3']}">
    <div class="cardBody">
      <h3>Risk & Scenario Simulation</h3>
      <p>Monte Carlo simulations and operational risk modelling.</p>
      <div class="cardFooter">
        <a href="/pages/Module3_Risk_Simulation.py">➡️ Open module →</a>
        <span>Probabilities</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{MODULE_IMGS['m4']}">
    <div class="cardBody">
      <h3>Cloud Analytics</h3>
      <p>Batch vs streaming analytics and scalability concepts.</p>
      <div class="cardFooter">
        <a href="/pages/Module4_Cloud_Analytics.py">➡️ Open module →</a>
        <span>Cloud patterns</span>
      </div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)
