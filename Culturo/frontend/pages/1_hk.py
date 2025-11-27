import streamlit as st
import sys
import os
from pathlib import Path
import mimetypes
import base64
from PIL import Image

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.star_manager import star_manager

# Page icon logo (keep original logo.png for tab icon)
page_logo_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.png"
logo_icon = str(page_logo_path) if page_logo_path.exists() else "🇭🇰"

# Sidebar logo (use provided Cultoro.jpg)
sidebar_logo_path = Path(__file__).parent.parent.parent / "assets" / "images" / "Cultoro.jpg"

st.set_page_config(
    page_title="Hong Kong - Culturo",
    page_icon=logo_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS (borrowed from 3_vn.py for consistency)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display:none; }
        [data-testid="stSidebar"] { background:#FFFFFF !important; }
        html, body, .stApp { background: linear-gradient(90deg, #F6F6DB 0%, #FFFFFF 100%) !important; min-height:100vh !important; }
        .main, .block-container, .stApp > header, [data-testid="stHeader"] { background:transparent !important; }
        .hk-header { display:flex; align-items:center; gap:6px; }
        .stColumns > div { padding-left:0 !important; padding-right:0 !important; }
        .stColumns { gap:6px !important; }
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { display:none !important; }
        button[data-testid="baseButton-primary"] { margin-top:0 !important; }
        button[kind="primary"] {
            border-radius:999px !important;
            background:linear-gradient(90deg, rgba(244,235,255,1) 0%, rgba(254,241,246,1) 100%) !important;
            color:#7C3AED !important;
            border:2px solid #E9D5FF !important;
            box-shadow:0 2px 0 rgba(124,58,237,0.15) inset, 0 4px 12px rgba(124,58,237,0.12) !important;
            font-weight:600 !important;
        }
        button[kind="primary"]:hover { filter:brightness(1.02) !important; box-shadow:0 2px 0 rgba(124,58,237,0.18) inset, 0 6px 16px rgba(124,58,237,0.18) !important; }
    </style>
""", unsafe_allow_html=True)

def load_icon(*keywords):
    icon_dir = Path(__file__).parent.parent.parent / "assets" / "icons"
    if not icon_dir.exists():
        return ""
    for f in icon_dir.iterdir():
        name = f.name.lower()
        if any(k in name for k in keywords):
            data = f.read_bytes()
            mime = mimetypes.guess_type(f.name)[0] or 'image/png'
            b64 = base64.b64encode(data).decode()
            return f"data:{mime};base64,{b64}"
    return ""

animals_icon = load_icon('pig','animal')
language_icon = load_icon('translation','language','translate')
arts_icon = load_icon('theater','art','mask')
food_icon = load_icon('ramen','noodle','food')

def hong_kong_page():
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0

    # Sidebar
    with st.sidebar:
        if sidebar_logo_path.exists():
            st.image(str(sidebar_logo_path), width=200)
        else:
            st.markdown("""
            <div style="text-align:center; padding:1rem 0;">
                <h3>🌍 Culturo</h3>
                <p style="font-size:0.8rem; color:#666; margin:0;">Discover culture all the world!</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("← General", key="sidebar_general_hk", width="stretch"):
            st.session_state.nav_counter += 1
            if 'current_region' in st.session_state: del st.session_state['current_region']
            st.switch_page("main_app.py")

        with st.expander("Discover", expanded=True):
            if st.button("Hong Kong", key="nav_hk", width="stretch", disabled=True):
                pass
            if st.button("China", key="nav_china_from_hk", width="stretch"):
                st.switch_page("pages/2_cn.py")
            if st.button("Viet Nam", key="nav_vn_from_hk", width="stretch"):
                st.switch_page("pages/3_vn.py")

    # Header
    left, right = st.columns([0.1, 0.9])
    with left:
        back_clicked = st.button("←\nBack", key="back_btn_hk", use_container_width=True)
    with right:
        st.markdown("""
            <div class="hk-header">
                <img src="https://flagcdn.com/w80/hk.png" width="50" height="33" style="border-radius:3px;" />
                <div style="display:flex; flex-direction:column;">
                    <h2 style="margin:0; padding:0; color:#E53935; font-size:1.6rem; font-weight:600; line-height:1;">Hong Kong</h2>
                    <p style="margin:0; padding:0; color:#666; font-size:0.9rem; line-height:1;">Choose an activity to explore!</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if back_clicked:
        st.session_state.nav_counter += 1
        if 'current_region' in st.session_state: del st.session_state['current_region']
        st.switch_page("main_app.py")

    st.markdown("<br>", unsafe_allow_html=True)

    stars = star_manager.get_stars("Hong Kong")

    # Layout: left cards, right map
    col_left, col_right = st.columns([1,1.2])
    with col_left:
        c1, c2 = st.columns(2)
        with c1:
            count = stars.get('Draw Animals', 0)
            st.markdown(f"""
                <div style=\"background:white; border-radius:15px; padding:1.2rem; box-shadow:0 2px 8px rgba(0,0,0,0.08); min-height:180px;\">
                    <div style=\"display:flex; flex-direction:column; align-items:center; gap:0; text-align:center;\">
                        <img src=\"{animals_icon}\" width=\"72\" height=\"72\" style=\"margin:0; display:block; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.12));\" />
                        <h3 style=\"margin:0; font-size:1.25rem; color:#2c3e50; font-weight:700; line-height:1;\">Animals</h3>
                        <p style=\"margin:0; font-size:1rem; color:#666; line-height:1;\">Drawing ⭐ {count}/3</p>
                        <div style=\"color:#ddd; font-size:1rem; margin:0;\">{'⭐'*count}{'☆'*(3-count)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="hk_animals_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Hong Kong"; st.switch_page("pages/5_draw.py")
        with c2:
            count = stars.get('Language', 0)
            st.markdown(f"""
                <div style=\"background:white; border-radius:15px; padding:1.2rem; box-shadow:0 2px 8px rgba(0,0,0,0.08); min-height:180px;\">
                    <div style=\"display:flex; flex-direction:column; align-items:center; gap:0; text-align:center;\">
                        <img src=\"{language_icon}\" width=\"72\" height=\"72\" style=\"margin:0; display:block; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.12));\" />
                        <h3 style=\"margin:0; font-size:1.25rem; color:#2c3e50; font-weight:700; line-height:1;\">Language</h3>
                        <p style=\"margin:0; font-size:1rem; color:#666; line-height:1;\">Quiz ⭐ {count}/3</p>
                        <div style=\"color:#ddd; font-size:1rem; margin:0;\">{'⭐'*count}{'☆'*(3-count)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="hk_language_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Hong Kong"; st.switch_page("pages/4_lg.py")
        c3, c4 = st.columns(2)
        with c3:
            count = stars.get('Performance', 0)
            st.markdown(f"""
                <div style=\"background:white; border-radius:15px; padding:1.2rem; box-shadow:0 2px 8px rgba(0,0,0,0.08); min-height:180px;\">
                    <div style=\"display:flex; flex-direction:column; align-items:center; gap:0; text-align:center;\">\n                        <img src=\"{arts_icon}\" width=\"72\" height=\"72\" style=\"margin:0; display:block; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.12));\" />\n                        <h3 style=\"margin:0; font-size:1.25rem; color:#2c3e50; font-weight:700; line-height:1;\">Arts</h3>\n                        <p style=\"margin:0; font-size:1rem; color:#666; line-height:1;\">Video & Quiz ⭐ {count}/3</p>\n                        <div style=\"color:#ddd; font-size:1rem; margin:0;\">{'⭐'*count}{'☆'*(3-count)}</div>\n                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="hk_arts_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Hong Kong"; st.switch_page("pages/7_per.py")
        with c4:
            count = stars.get('Food', 0)
            st.markdown(f"""
                <div style=\"background:white; border-radius:15px; padding:1.2rem; box-shadow:0 2px 8px rgba(0,0,0,0.08); min-height:180px;\">
                    <div style=\"display:flex; flex-direction:column; align-items:center; gap:0; text-align:center;\">\n                        <img src=\"{food_icon}\" width=\"72\" height=\"72\" style=\"margin:0; display:block; filter:drop-shadow(0 2px 4px rgba(0,0,0,0.12));\" />\n                        <h3 style=\"margin:0; font-size:1.25rem; color:#2c3e50; font-weight:700; line-height:1;\">Food</h3>\n                        <p style=\"margin:0; font-size:1rem; color:#666; line-height:1;\">Quiz ⭐ {count}/3</p>\n                        <div style=\"color:#ddd; font-size:1rem; margin:0;\">{'⭐'*count}{'☆'*(3-count)}</div>\n                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="hk_food_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Hong Kong"; st.switch_page("pages/6_food.py")

    with col_right:
        # Map similar to Vietnam page
        target_height = 520
        map_path = Path(__file__).parent.parent.parent / "assets" / "pages" / "Hongkong_main.png"
        chosen = None
        if os.path.exists(map_path):
            chosen = map_path
        else:
            for name in ["Hongkong.png", "Hong Kong.png", "hongkong_map.png"]:
                alt = Path(__file__).parent.parent.parent / "assets" / "pages" / name
                if os.path.exists(alt):
                    chosen = alt
                    break
        if chosen:
            try:
                img = Image.open(chosen)
                w, h = img.size
                if h > target_height:
                    new_w = int(w * (target_height / h))
                    img = img.resize((new_w, target_height), Image.LANCZOS)
                st.image(img, width="content")
            except Exception:
                st.image(str(chosen), width="content")
        else:
            st.markdown("""
                <div style="background:#f0f0f0; border-radius:15px; padding:3rem; text-align:center; min-height:400px; display:flex; align-items:center; justify-content:center;">
                    <p style="color:#999;">Hong Kong Map</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    hong_kong_page()
