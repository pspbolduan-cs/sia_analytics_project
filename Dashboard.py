def run_streamlit_ui():
    import streamlit as st
    from pathlib import Path
    import base64

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
    # ✅ ABSOLUTE ASSET PATHS (this is the main fix)
    # ---------------------------------------------------
    BASE_DIR = Path(__file__).resolve().parent
    ASSETS_DIR = BASE_DIR / "assets"

    HERO_VIDEO_PATH = ASSETS_DIR / "hero.mp4"
    LOGO_PATH = ASSETS_DIR / "singapore_airlines_logo.png"

    MODULE_1_PATH = ASSETS_DIR / "module1.png"
    MODULE_2_PATH = ASSETS_DIR / "module2.png"
    MODULE_3_PATH = ASSETS_DIR / "module3.png"
    MODULE_4_PATH = ASSETS_DIR / "module4.png"

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

    hero_video_uri = _to_data_uri(HERO_VIDEO_PATH, "video/mp4")
    logo_uri = _to_data_uri(LOGO_PATH, _mime_for_image(LOGO_PATH))

    m1_uri = _to_data_uri(MODULE_1_PATH, _mime_for_image(MODULE_1_PATH))
    m2_uri = _to_data_uri(MODULE_2_PATH, _mime_for_image(MODULE_2_PATH))
    m3_uri = _to_data_uri(MODULE_3_PATH, _mime_for_image(MODULE_3_PATH))
    m4_uri = _to_data_uri(MODULE_4_PATH, _mime_for_image(MODULE_4_PATH))

    # ---------------------------------------------------
    # Optional: quick debug (remove later)
    # ---------------------------------------------------
    # st.caption(f"hero.mp4 exists: {HERO_VIDEO_PATH.exists()} | logo exists: {LOGO_PATH.exists()}")

    # ---------------------------------------------------
    # CSS (keep yours; this includes the key hero layering)
    # ---------------------------------------------------
    st.markdown(
        """
        <style>
          .heroWrap{
            position: relative;
            border-radius: 26px;
            overflow: hidden;
            margin-bottom: 2.2rem;
            box-shadow: 0 18px 45px rgba(0,0,0,0.22);
            border: 1px solid rgba(255,255,255,0.10);
            min-height: 380px;
          }
          .heroVideo{
            position:absolute; inset:0;
            width:100%; height:100%;
            object-fit:cover;
            opacity:0.85;
            z-index:0;
          }
          .heroOverlay{
            position:absolute; inset:0;
            background: linear-gradient(135deg,
              rgba(0,26,77,0.92) 0%,
              rgba(0,58,128,0.72) 45%,
              rgba(0,26,77,0.92) 100%);
            z-index:1;
          }
          .heroInner{
            position:relative;
            z-index:2;
            padding: 2.2rem 2.4rem;
            display:flex;
            gap: 22px;
            align-items:flex-start;
            flex-wrap: wrap;
          }
          .logoChip{
            background: rgba(255,255,255,0.92);
            border-radius: 18px;
            padding: 12px 14px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.18);
            border: 1px solid rgba(255,255,255,0.45);
            display:flex;
            align-items:center;
            justify-content:center;
          }
          .logoChip img{ height: 64px; width:auto; display:block; }

          .tagRow{ display:flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
          .tagPill{
            display:inline-flex; align-items:center; gap:8px;
            padding: 9px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.22);
            color: rgba(255,255,255,0.92);
            font-weight: 800;
            font-size: 0.95rem;
            backdrop-filter: blur(6px);
          }
          .tagDot{ width: 10px; height: 10px; border-radius: 999px; background: rgba(255,255,255,0.75); display:inline-block; }
          .kbd{
            padding: 2px 8px;
            border-radius: 10px;
            background: rgba(0,0,0,0.22);
            border: 1px solid rgba(255,255,255,0.16);
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-weight: 800;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------------
    # ✅ HERO (title + logo forced visible, no “code showing”)
    # ---------------------------------------------------
    video_block = ""
    if hero_video_uri:
        video_block = f"""
        <video class="heroVideo" autoplay muted loop playsinline>
          <source src="{hero_video_uri}" type="video/mp4" />
        </video>
        """

    logo_block = ""
    if logo_uri:
        logo_block = f"""
        <div class="logoChip">
          <img src="{logo_uri}" alt="Singapore Airlines logo">
        </div>
        """

    st.markdown(
        f"""
        <div class="heroWrap">
          {video_block}
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

              {"<div style='margin-top:12px; color:rgba(255,255,255,0.85); font-weight:800;'>⚠️ hero.mp4 not found at <span class='kbd'>assets/hero.mp4</span></div>" if not hero_video_uri else ""}
              {"<div style='margin-top:8px; color:rgba(255,255,255,0.85); font-weight:800;'>⚠️ logo not found at <span class='kbd'>assets/singapore_airlines_logo.png</span></div>" if not logo_uri else ""}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ✅ Keep the rest of your page below (modules, etc.)
    # Use m1_uri, m2_uri, m3_uri, m4_uri for your cards.
