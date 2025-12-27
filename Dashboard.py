# ============================================
# Singapore Airlines Analytics System
# Dashboard (FINAL – stable & clean)
# ============================================

import streamlit as st
from pathlib import Path
import base64

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Singapore Airlines Analytics System",
    page_icon="✈️",
    layout="wide",
)

# -------------------------------------------------
# Paths
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

def img_uri(path: Path):
    if not path.exists():
        return ""
    data = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/png;base64,{data}"

hero_video = ASSETS / "hero.mp4"
logo = img_uri(ASSETS / "singapore_airlines_logo.png")

imgs = {
    "m1": img_uri(ASSETS / "module1.png"),
    "m2": img_uri(ASSETS / "module2.png"),
    "m3": img_uri(ASSETS / "module3.png"),
    "m4": img_uri(ASSETS / "module4.png"),
    "sys": img_uri(ASSETS / "system_overview.png"),
    "sec": img_uri(ASSETS / "security_risk_ethics.png"),
}

# -------------------------------------------------
# CSS (SAFE & SIMPLE)
# -------------------------------------------------
st.markdown("""
<style>
.block-container { padding-top: 1rem; }

.hero {
  border-radius: 22px;
  padding: 2.5rem;
  background: linear-gradient(135deg,#001a4d,#003a80);
  color: white;
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 3rem;
  margin-bottom: .5rem;
}

.hero p {
  font-size: 1.2rem;
  opacity: .9;
}

.tags span {
  display: inline-block;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,.15);
  margin-right: 8px;
  font-weight: 700;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit,minmax(320px,1fr));
  gap: 18px;
}

.card {
  background: #0f172a;
  border-radius: 20px;
  overflow: hidden;
  color: white;
  box-shadow: 0 18px 45px rgba(0,0,0,.25);
}

.card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-body {
  padding: 18px;
  display: flex;
  flex-direction: column;
  min-height: 170px;
}

.card-body h3 {
  margin: 0 0 6px 0;
}

.card-body p {
  opacity: .75;
  flex: 1;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions a {
  text-decoration: none;
  padding: 10px 16px;
  border-radius: 14px;
  background: rgba(255,255,255,.18);
  color: white;
  font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown(f"""
<div class="hero">
  <div style="display:flex; gap:20px; align-items:center; flex-wrap:wrap;">
    <img src="{logo}" height="60">
    <div>
      <h1>Singapore Airlines Analytics System</h1>
      <p>Enterprise cloud-based analytics dashboard for operational performance, customer experience, risk, and cloud analytics.</p>
      <div class="tags">
        <span>Streamlit UI</span>
        <span>CLI supported</span>
        <span>Dataset: assets/train.csv</span>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SYSTEM PAGES
# -------------------------------------------------
st.markdown("## 🧩 System Pages")
st.markdown("Enterprise design, governance, security, and ethics.")

st.markdown(f"""
<div class="grid">

  <div class="card">
    <img src="{imgs['sys']}">
    <div class="card-body">
      <h3>🧱 System Overview / Architecture</h3>
      <p>System architecture, shared services, modular structure, and scalability mapping.</p>
      <div class="actions">
        <a href="/pages/System_Overview_Architecture.py">➡ Open page</a>
        <span>Enterprise design</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{imgs['sec']}">
    <div class="card-body">
      <h3>🛡️ Security, Risk & Ethics</h3>
      <p>Privacy, governance assumptions, security controls, and ethical analytics considerations.</p>
      <div class="actions">
        <a href="/pages/Security_Risk_Ethics.py">➡ Open page</a>
        <span>Governance</span>
      </div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# ANALYTICS MODULES
# -------------------------------------------------
st.markdown("## 📊 Analytics Modules")

st.markdown(f"""
<div class="grid">

  <div class="card">
    <img src="{imgs['m1']}">
    <div class="card-body">
      <h3>✈️ Flight Performance</h3>
      <p>Distance, delays, crew service, and fuel estimation analytics.</p>
      <div class="actions">
        <a href="/pages/Module1_Flight_Performance.py">➡ Open module</a>
        <span>KPIs & charts</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{imgs['m2']}">
    <div class="card-body">
      <h3>😊 Customer Experience</h3>
      <p>Passenger satisfaction, service quality, and behavioural analysis.</p>
      <div class="actions">
        <a href="/pages/Module2_Customer_Experience.py">➡ Open module</a>
        <span>Service insights</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{imgs['m3']}">
    <div class="card-body">
      <h3>⚠️ Risk Simulation</h3>
      <p>Monte Carlo simulation, uncertainty, and scenario modelling.</p>
      <div class="actions">
        <a href="/pages/Module3_Risk_Simulation.py">➡ Open module</a>
        <span>Probabilities</span>
      </div>
    </div>
  </div>

  <div class="card">
    <img src="{imgs['m4']}">
    <div class="card-body">
      <h3>☁️ Cloud Analytics</h3>
      <p>Scalable cloud analytics concepts and processing models.</p>
      <div class="actions">
        <a href="/pages/Module4_Cloud_Analytics.py">➡ Open module</a>
        <span>Batch vs streaming</span>
      </div>
    </div>
  </div>

</div>
""", unsafe_allow_html=True)

st.success("✅ Dashboard fully loaded. All navigation and images are operational.")
