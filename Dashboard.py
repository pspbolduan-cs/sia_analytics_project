# ============================================
# Singapore Airlines Analytics System
# Dashboard (Home Page)
# ============================================

import streamlit as st
from pathlib import Path
import base64

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

def to_base64(path, mime):
    if not path.exists():
        return ""
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"

hero_video = to_base64(ASSETS / "hero.mp4", "video/mp4")
logo = to_base64(ASSETS / "singapore_airlines_logo.png", "image/png")

module_imgs = {
    "m1": to_base64(ASSETS / "module1.png", "image/png"),
    "m2": to_base64(ASSETS / "module2.png", "image/png"),
    "m3": to_base64(ASSETS / "module3.png", "image/png"),
    "m4": to_base64(ASSETS / "module4.png", "image/png"),
    "sys": to_base64(ASSETS / "system_overview.png", "image/png"),
    "sec": to_base64(ASSETS / "security_risk_ethics.png", "image/png"),
}

# --------------------------------------------------
# CSS
# --------------------------------------------------
st.markdown("""
<style>
.hero {
  position: relative;
  border-radius: 22px;
  overflow: hidden;
  min-height: 380px;
  margin-bottom: 2rem;
}
.hero video {
  position:absolute;
  inset:0;
  width:100%;
  height:100%;
  object-fit:cover;
  opacity:.85;
}
.heroOverlay {
  position:absolute;
  inset:0;
  background:linear-gradient(135deg,#001a4d,#003a80);
  opacity:.85;
}
.heroContent {
  position:relative;
  z-index:2;
  padding:2.5rem;
  color:white;
}
.heroContent img {
  height:60px;
  margin-bottom:1rem;
}
.tag {
  display:inline-block;
  padding:8px 14px;
  border-radius:999px;
  background:rgba(255,255,255,.15);
  margin-right:8px;
  font-weight:700;
}

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
  border-radius:20px;
  overflow:hidden;
  box-shadow:0 18px 45px rgba(0,0,0,.2);
}
.card img {
  width:100%;
  height:220px;
  object-fit:cover;
}
.cardBody {
  padding:18px;
  color:white;
}
.cardBody h3 {
  margin-bottom:6px;
}
.cardBody p {
  opacity:.75;
}
.cardFooter {
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-top:12px;
}
.cardFooter a {
  text-decoration:none;
  font-weight:900;
  background:rgba(255,255,255,.15);
  padding:10px 14px;
  border-radius:14px;
  color:white;
}
.cardFooter span {
  opacity:.7;
  font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO
# --------------------------------------------------
st.markdown(f"""
<div class="hero">
  {"<video autoplay muted loop playsinline><source src='"+hero_video+"' type='video/mp4'></video>" if hero_video else ""}
  <div class="heroOverlay"></div>
  <div class="heroContent">
    <img src="{logo}">
    <h1>Singapore Airlines Analytics System</h1>
    <p>
      Enterprise cloud-based analytics dashboard for operational performance,
      customer experience, risk scenarios, and cloud processing concepts.
    </p>
    <span class="tag">Streamlit UI</span>
    <span class="tag">CLI Supported</span>
    <span class="tag">assets/train.csv</span>
  </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# CARD HELPER
# --------------------------------------------------
def card(title, desc, img, link, btn, hint):
    return f"""
    <div class="card">
      <img src="{img}">
      <div class="cardBody">
        <h3>{title}</h3>
        <p>{desc}</p>
        <div class="cardFooter">
          <a href="/{link}" target="_self">➡️ {btn} →</a>
          <span>{hint}</span>
        </div>
      </div>
    </div>
    """

# --------------------------------------------------
# SYSTEM PAGES
# --------------------------------------------------
st.markdown("## 🧩 System Pages")
st.markdown("Enterprise architecture, governance, security & ethics.")

st.markdown(f"""
<div class="grid">
  {card(
    "System Overview / Architecture",
    "View system architecture, shared services, and cloud scalability.",
    module_imgs["sys"],
    "pages/System_Overview_Architecture.py",
    "Open page",
    "Enterprise design"
  )}
  {card(
    "Security, Risk & Ethics",
    "Review privacy, governance assumptions, and security controls.",
    module_imgs["sec"],
    "pages/Security_Risk_Ethics.py",
    "Open page",
    "Protection & ethics"
  )}
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# ANALYTICS MODULES
# --------------------------------------------------
st.markdown("## 📊 Analytics Modules")

st.markdown(f"""
<div class="grid">
  {card("Flight Performance Analytics",
        "Distance, delays, crew indicators & fuel usage.",
        module_imgs["m1"],
        "pages/Module1_Flight_Performance.py",
        "Open module",
        "KPIs & charts")}

  {card("Customer Experience Analytics",
        "Passenger satisfaction & service ratings.",
        module_imgs["m2"],
        "pages/Module2_Customer_Experience.py",
        "Open module",
        "CX insights")}

  {card("Risk & Scenario Simulation",
        "Monte Carlo risk modelling & scenarios.",
        module_imgs["m3"],
        "pages/Module3_Risk_Simulation.py",
        "Open module",
        "Probability & risk")}

  {card("Cloud Analytics",
        "Scalable analytics & cloud processing concepts.",
        module_imgs["m4"],
        "pages/Module4_Cloud_Analytics.py",
        "Open module",
        "Cloud scaling")}
</div>
""", unsafe_allow_html=True)
