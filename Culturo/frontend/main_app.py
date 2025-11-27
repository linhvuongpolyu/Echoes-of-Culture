import streamlit as st
import base64
import os
from pathlib import Path
import sys

# Add utils to path
sys.path.append(str(Path(__file__).parent))
from utils.star_manager import star_manager

# Build absolute path to logo
logo_path = Path(__file__).parent.parent / "assets" / "images" / "logo.png"

# Page configuration - show sidebar
st.set_page_config(
    page_title="Culturo",
    page_icon=str(logo_path),  # Convert Path object to string for absolute path
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styles with simple sidebar
st.markdown("""
    <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-straight/css/uicons-regular-straight.css'>
    <link rel='stylesheet' href='https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css'>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.0.0/css/flag-icons.min.css'>
    <style>
        /* Hide page navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Style the sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
        }
        
        /* Style main content background */
        .main {
            background-color: #EFF8FF !important;
        }
        
        .stApp {
            background-color: #EFF8FF !important;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #EFF8FF !important;
        }
        
        /* Adjust main content area padding */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
            background-color: #EFF8FF !important;
        }
        /* Adjust title and content width */
        .main .block-container > div {
            max-width: 100%;
        }
        
        /* Custom styles for new layout */
        .main-header {
            background: linear-gradient(135deg, #a8e6cf 0%, #88d8c0 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: #2c3e50;
        }
        
        .stats-container {
            display: flex;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            flex: 1;
            color: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .countries-container {
            display: flex;
            gap: 1.5rem;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        
        .country-card {
            flex: 1;
            min-width: 300px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            overflow: hidden;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .country-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }
        
        .country-header {
            padding: 1rem;
            font-weight: bold;
            font-size: 1.2rem;
            border-bottom: 1px solid #eee;
        }
        
        .china-header {
            background: #dc3545;
            color: white;
        }
        
        .vietnam-header {
            background: #dc3545;
            color: white;
        }
        
        .hongkong-header {
            background: #dc3545;
            color: white;
        }
        
        .country-map {
            padding: 1rem;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .country-stats {
            padding: 0.5rem;
            font-size: 0.9rem;
            color: #666;
        }
        
        .explore-button {
            background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-weight: bold;
            margin: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .explore-button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(233, 30, 99, 0.4);
        }
        
        /* Style for Discover expander */
        [data-testid="stExpander"] > div:first-child {
            border-radius: 16px !important;
            text-align: left !important;
            font-weight: 900 !important;
            margin: 4px !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        
        [data-testid="stExpander"] > div:first-child > div {
            border-radius: 16px !important;
        }
        
        /* Style primary buttons to pink color */
        button[kind="primary"] {
            background-color: #C11574 !important;
            border-color: #C11574 !important;
        }
        
        button[kind="primary"]:hover {
            background-color: #a00f5d !important;
            border-color: #a00f5d !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Star data is now managed by star_manager utility - no initialization needed

def get_image_base64(image_path):
    """Convert image to base64 encoding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Failed to load image {image_path}: {e}")
        return None


# Main page
def main():
    # Initialize navigation counter to force fresh renders
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0
    
    # Clear current_region when on main page to prevent navigation issues
    if 'current_region' in st.session_state:
        del st.session_state['current_region']
    
    # Check query parameters first - using st.query_params API
    region_param = st.query_params.get("region", None)
    
    if region_param:
        if region_param == "hk":
            st.switch_page("pages/1_hk.py")
        elif region_param == "cn":
            st.switch_page("pages/2_cn.py")
        elif region_param == "vn":
            st.switch_page("pages/3_vn.py")
    
    # Sidebar content matching the design
    with st.sidebar:
        # Culturo logo image
        logo_img_path = Path(__file__).parent.parent / "assets" / "images" / "Cultoro.jpg"
        if os.path.exists(logo_img_path):
            st.image(str(logo_img_path), width=200)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1rem 0;">
                <h3>🌍 Culturo</h3>
                <p style="font-size: 0.8rem; color: #666; margin: 0;">Discover culture all the world!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # General section (highlighted as current page)
        st.markdown("""
        <div style="background-color: #004DA0; color: white; padding: 8px 16px; margin: 4px; border-radius: 16px; font-weight: bold; width: 100%; box-sizing: border-box; display: flex; align-items: center; gap: 8px;">
            <i class="fi fi-rs-apps"></i>
            <span>General</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Discover section with expandable menu
        with st.expander("Discover", expanded=False):
            if st.button("Viet Nam", key="nav_vietnam", width="stretch"):
                st.switch_page("pages/3_vn.py")
            if st.button("China", key="nav_china", width="stretch"):
                st.switch_page("pages/2_cn.py")
            if st.button("Hong Kong", key="nav_hongkong", width="stretch"):
                st.switch_page("pages/1_hk.py")
    
    # Combined Header and Statistics Section
    stats = star_manager.get_overall_stats()
    total_stars = stats['total_stars']
    explored_countries = len([region for region in ['china', 'vietnam', 'hongkong'] if stats.get(f'{region}_stars', 0) > 0])
    
    # Header text at top of page
    st.markdown("""
        <div style="margin-top: -2rem; margin-bottom: 0.5rem;">
            <h1 style="margin: 0; font-size: 2rem; font-weight: bold; color: #2c3e50; line-height: 1;">Hello,</h1>
            <p style="margin-top: 0; margin-bottom: 0; font-size: 1rem; color: #2c3e50; line-height: 1;">Let's enjoy and discover with us!</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Statistics boxes using Streamlit columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div style="background: white; padding: 0.6rem 1rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; font-size: 1rem; color: #666; font-weight: bold;">⭐ Total Stars</h3>
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #333;">{total_stars}/36</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style="background: white; padding: 0.6rem 1rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; font-size: 1rem; color: #666; font-weight: bold;">🌍 Countries Explored</h3>
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #333;">{explored_countries}/3</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Countries Section
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get paths to map images
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    assets_dir = os.path.join(project_root, "assets", "map")
    
    cn_map_path = os.path.join(assets_dir, "China.png")
    vn_map_path = os.path.join(assets_dir, "Vietnam.png")
    hk_map_path = os.path.join(assets_dir, "Hong Kong.png")
    
    # Create 3 columns for countries
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Vietnam Card
        vietnam_stars = stats.get('vietnam_stars', 0)
        vn_img_base64 = get_image_base64(vn_map_path) if os.path.exists(vn_map_path) else None
        
        st.markdown(f"""
            <div style="background: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); padding: 1rem; margin-bottom: 0.5rem; min-height: 280px;">
                <!-- Header with flag, name, and stars -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span class="fi fi-vn" style="font-size: 1.3rem;"></span>
                        <span style="font-weight: bold; font-size: 1.1rem;">VIET NAM</span>
                    </div>
                    <span style="font-size: 0.9rem; color: #666;">{vietnam_stars}/12</span>
                </div>
                <!-- Map image -->
                <div style="text-align: center; padding: 0.5rem 0;">
                    {'<img src="data:image/png;base64,' + vn_img_base64 + '" style="width: 240px; max-width: 100%;" />' if vn_img_base64 else '<div style="height: 150px; display: flex; align-items: center; justify-content: center; background: #f0f0f0; border-radius: 10px;">Vietnam Map</div>'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Explore button outside white container
        if st.button("Explore Viet Nam", key="explore_vietnam", width="stretch", type="primary"):
            st.switch_page("pages/3_vn.py")
    
    with col2:
        # China Card
        china_stars = stats.get('china_stars', 0)
        cn_img_base64 = get_image_base64(cn_map_path) if os.path.exists(cn_map_path) else None
        
        st.markdown(f"""
            <div style="background: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); padding: 1rem; margin-bottom: 0.5rem; min-height: 280px;">
                <!-- Header with flag, name, and stars -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span class="fi fi-cn" style="font-size: 1.3rem;"></span>
                        <span style="font-weight: bold; font-size: 1.1rem;">CHINA</span>
                    </div>
                    <span style="font-size: 0.9rem; color: #666;">{china_stars}/12</span>
                </div>
                <!-- Map image -->
                <div style="text-align: center; padding: 0.5rem 0;">
                    {'<img src="data:image/png;base64,' + cn_img_base64 + '" style="width: 240px; max-width: 100%;" />' if cn_img_base64 else '<div style="height: 150px; display: flex; align-items: center; justify-content: center; background: #f0f0f0; border-radius: 10px;">China Map</div>'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Explore button outside white container
        if st.button("Explore China", key="explore_china", width="stretch", type="primary"):
            st.switch_page("pages/2_cn.py")
    
    with col3:
        # Hong Kong Card
        hongkong_stars = stats.get('hongkong_stars', 0)
        hk_img_base64 = get_image_base64(hk_map_path) if os.path.exists(hk_map_path) else None
        
        st.markdown(f"""
            <div style="background: white; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); padding: 1rem; margin-bottom: 0.5rem; min-height: 280px;">
                <!-- Header with flag, name, and stars -->
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span class="fi fi-hk" style="font-size: 1.3rem;"></span>
                        <span style="font-weight: bold; font-size: 1.1rem;">HONG KONG</span>
                    </div>
                    <span style="font-size: 0.9rem; color: #666;">{hongkong_stars}/12</span>
                </div>
                <!-- Map image -->
                <div style="text-align: center; padding: 0.5rem 0;">
                    {'<img src="data:image/png;base64,' + hk_img_base64 + '" style="width: 240px; max-width: 100%;" />' if hk_img_base64 else '<div style="height: 150px; display: flex; align-items: center; justify-content: center; background: #f0f0f0; border-radius: 10px;">Hong Kong Map</div>'}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Explore button outside white container
        if st.button("Explore Hong Kong", key="explore_hongkong", width="stretch", type="primary"):
            st.switch_page("pages/1_hk.py")
    

if __name__ == "__main__":
    main()