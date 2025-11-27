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

# Build absolute path to logo (reuse app logo like main_app)
logo_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.png"
logo_icon = str(logo_path) if logo_path.exists() else "🇻🇳"  # fallback if missing

# Page configuration (replace flag with logo)
st.set_page_config(
    page_title="Vietnam - Culturo",
    page_icon=logo_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styles
st.markdown("""
    <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-straight/css/uicons-regular-straight.css'>
    <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css'>
    <style>
        /* Hide page navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Sidebar styling - keep solid white */
        [data-testid="stSidebar"] {
            background: #FFFFFF !important;
        }
        
        /* Page background: soft gradient on root */
        html, body, .stApp {
            background: linear-gradient(90deg, #BFEFE6 0%, #FFFFFF 100%) !important;
            background-attachment: fixed !important;
            min-height: 100vh !important;
        }
        /* Make inner containers transparent so gradient shows through */
        .main, .block-container, .stApp > header, [data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* Expander styling */
        [data-testid="stExpander"] > div:first-child {
            border-radius: 16px !important;
            text-align: left !important;
            font-weight: 900 !important;
            margin: 4px !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        
        /* Header row tweaks */
        .vn-header { display: flex; align-items: center; gap: 6px; }
        /* Reduce default column inner padding to bring items closer */
        .stColumns > div { padding-left: 0 !important; padding-right: 0 !important; }
        /* Reduce gutter between header columns */
        .stColumns { gap: 6px !important; }
        
        /* Hide heading anchor/link icon next to titles */
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { display: none !important; }

        /* Tighten spacing between cards and their action buttons */
        .element-container:has(div[style*="background: white"]) + .element-container { margin-top: 6px !important; }
        button[data-testid="baseButton-primary"] { margin-top: 0 !important; }

        /* Stylish pill button to match reference (soft purple gradient) */
        button[kind="primary"] {
            border-radius: 999px !important;
            background: linear-gradient(90deg, rgba(244,235,255,1) 0%, rgba(254,241,246,1) 100%) !important;
            color: #7C3AED !important; /* vivid purple text */
            border: 2px solid #E9D5FF !important; /* light lavender border */
            box-shadow: 0 2px 0 rgba(124,58,237,0.15) inset, 0 4px 12px rgba(124,58,237,0.12) !important;
            font-weight: 600 !important;
        }
        button[kind="primary"]:hover {
            filter: brightness(1.02) !important;
            box-shadow: 0 2px 0 rgba(124,58,237,0.18) inset, 0 6px 16px rgba(124,58,237,0.18) !important;
        }
        .stColumns > div { padding-left: 0 !important; padding-right: 0 !important; }
    </style>
    """, unsafe_allow_html=True)

def vietnam_page():
    # Initialize navigation counter to force fresh renders
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0

    # Helper: load base64 data URI for icon by keywords
    icon_dir = Path(__file__).parent.parent.parent / "assets" / "icons"
    def load_icon(*keywords):
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
    
    # Sidebar content
    with st.sidebar:
        # Logo
        logo_img_path = Path(__file__).parent.parent.parent / "assets" / "images" / "Cultoro.jpg"
        if os.path.exists(logo_img_path):
            st.image(str(logo_img_path), width=200)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h3>🌍 Culturo</h3>
                <p style="font-size: 0.8rem; color: #666; margin: 0;">Discover culture all the world!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # General section
        if st.button("← General", key="sidebar_general", width="stretch"):
            st.session_state.nav_counter += 1
            if 'current_region' in st.session_state:
                del st.session_state['current_region']
            st.switch_page("main_app.py")
        
        # Discover section with expander
        with st.expander("Discover", expanded=True):
            if st.button("Viet Nam", key="nav_vietnam", width="stretch", disabled=True):
                pass  # Current page
            if st.button("China", key="nav_china", width="stretch", disabled=False):
                st.switch_page("pages/2_cn.py")
            if st.button("Hong Kong", key="nav_hongkong", width="stretch", disabled=False):
                st.switch_page("pages/1_hk.py")
    
    # Header: Back button and flag/title in the same row (restore flag per request)
    header_left, header_right = st.columns([0.1, 0.9])
    with header_left:
        back_clicked = st.button("←\nBack", key="back_btn", use_container_width=True)
    with header_right:
        st.markdown("""
            <div class="vn-header">
                <img src="https://flagcdn.com/w80/vn.png" width="50" height="33" style="border-radius: 3px;" />
                <div style="display: flex; flex-direction: column;">
                    <h2 style="margin: 0; padding: 0; color: #E53935; font-size: 1.6rem; font-weight: 600; line-height: 1;">Viet Nam</h2>
                    <p style="margin: 0; padding: 0; color: #666; font-size: 0.9rem; line-height: 1;">Choose an activity to explore!</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    if back_clicked:
        st.session_state.nav_counter += 1
        if 'current_region' in st.session_state:
            del st.session_state['current_region']
        st.switch_page("main_app.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get Vietnam stars data from star_manager
    stars = star_manager.get_stars("Vietnam")
    total_stars = star_manager.get_total_stars("Vietnam")
    
    # Main layout: Activities grid on left, map on right
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        # Row 1
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            # Animals card
            animals_stars = stars.get('Draw Animals', 0)
            st.markdown(f"""
                <div style="background: white; border-radius: 15px; padding: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); min-height: 180px;">
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 0; text-align: center;">
                        <img src="{animals_icon}" alt="Animals" width="72" height="72" style="margin:0; display:block; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12));" />
                        <h3 style="margin: 0; font-size: 1.25rem; color: #2c3e50; font-weight: 700; line-height: 1;">Animals</h3>
                        <p style="margin: 0; font-size: 1rem; color: #666; line-height: 1;">Drawing ⭐ {animals_stars}/3</p>
                        <div style="color: #ddd; font-size: 1rem; margin: 0;">{'⭐' * animals_stars}{'☆' * (3 - animals_stars)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="animals_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Vietnam"
                st.switch_page("pages/5_draw.py")
        
        with row1_col2:
            # Language card
            language_stars = stars.get('Language', 0)
            st.markdown(f"""
                <div style="background: white; border-radius: 15px; padding: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); min-height: 180px;">
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 0; text-align: center;">
                        <img src="{language_icon}" alt="Language" width="72" height="72" style="margin:0; display:block; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12));" />
                        <h3 style="margin: 0; font-size: 1.25rem; color: #2c3e50; font-weight: 700; line-height: 1;">Language</h3>
                        <p style="margin: 0; font-size: 1rem; color: #666; line-height: 1;">Quiz ⭐ {language_stars}/3</p>
                        <div style="color: #ddd; font-size: 1rem; margin: 0;">{'⭐' * language_stars}{'☆' * (3 - language_stars)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="language_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Vietnam"
                st.switch_page("pages/4_lg.py")
        
        # Row 2
        row2_col1, row2_col2 = st.columns(2)
        
        with row2_col1:
            # Arts card
            arts_stars = stars.get('Performance', 0)
            st.markdown(f"""
                <div style="background: white; border-radius: 15px; padding: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); min-height: 180px;">
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 0; text-align: center;">
                        <img src="{arts_icon}" alt="Arts" width="72" height="72" style="margin:0; display:block; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12));" />
                        <h3 style="margin: 0; font-size: 1.25rem; color: #2c3e50; font-weight: 700; line-height: 1;">Arts</h3>
                        <p style="margin: 0; font-size: 1rem; color: #666; line-height: 1;">Video & Quiz ⭐ {arts_stars}/3</p>
                        <div style="color: #ddd; font-size: 1rem; margin: 0;">{'⭐' * arts_stars}{'☆' * (3 - arts_stars)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="arts_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Vietnam"
                st.switch_page("pages/7_per.py")
        
        with row2_col2:
            # Food card
            food_stars = stars.get('Food', 0)
            st.markdown(f"""
                <div style="background: white; border-radius: 15px; padding: 1.2rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); min-height: 180px;">
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 0; text-align: center;">
                        <img src="{food_icon}" alt="Food" width="72" height="72" style="margin:0; display:block; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.12));" />
                        <h3 style="margin: 0; font-size: 1.25rem; color: #2c3e50; font-weight: 700; line-height: 1;">Food</h3>
                        <p style="margin: 0; font-size: 1rem; color: #666; line-height: 1;">Quiz ⭐ {food_stars}/3</p>
                        <div style="color: #ddd; font-size: 1rem; margin: 0;">{'⭐' * food_stars}{'☆' * (3 - food_stars)}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Click to start 🚀", key="food_btn", width="stretch", type="primary"):
                st.session_state.current_region = "Vietnam"
                st.switch_page("pages/6_food.py")
    
    with col_right:
        # Map image scaled to fit one page (reduce height to avoid scroll)
        target_height = 520  # adjust if still scrolling; reduce further if needed
        map_path = Path(__file__).parent.parent.parent / "assets" / "pages" / "Vietnam_main.png"
        chosen = None
        if os.path.exists(map_path):
            chosen = map_path
        else:
            for name in ["Vietnam.png", "vn.png", "vietnam_map.png"]:
                alt_path = Path(__file__).parent.parent.parent / "assets" / "pages" / name
                if os.path.exists(alt_path):
                    chosen = alt_path
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
                <div style="background: #f0f0f0; border-radius: 15px; padding: 3rem; text-align: center; min-height: 400px; display: flex; align-items: center; justify-content: center;">
                    <p style="color: #999;">Vietnam Map</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    vietnam_page()
