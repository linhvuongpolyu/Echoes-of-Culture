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

# Page configuration - hide sidebar
st.set_page_config(
    page_title="Culturo",
    page_icon=str(logo_path),  # Convert Path object to string for absolute path
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Completely hide sidebar CSS
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        /* Adjust main content area padding */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }
        /* Adjust title and content width */
        .main .block-container > div {
            max-width: 100%;
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

# Note: The HTML-based interactive map has been replaced with simple Streamlit buttons
# to avoid iframe nesting issues during navigation. The function below is kept for reference
# but is no longer used.

# Create interactive map (DEPRECATED - causes iframe nesting issues)
def create_interactive_map_deprecated():
    """Create interactive map - DEPRECATED: Use native Streamlit buttons instead"""
    # Image paths - locate assets directory from frontend directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)  # Up to project root
    assets_dir = os.path.join(project_root, "assets", "map")
    
    bg_path = os.path.join(assets_dir, "obg.png")
    hk_path = os.path.join(assets_dir, "ohk.png")
    cn_path = os.path.join(assets_dir, "ocn.png")
    vn_path = os.path.join(assets_dir, "ovn.png")
    
    # Get base64 encoding of images
    bg_b64 = get_image_base64(bg_path)
    hk_b64 = get_image_base64(hk_path)
    cn_b64 = get_image_base64(cn_path)
    vn_b64 = get_image_base64(vn_path)
    
    if not all([bg_b64, hk_b64, cn_b64, vn_b64]):
        st.error("Failed to load map images, please check the image paths")
        return None
    
    # CSS styles and JavaScript - modified size settings
    map_html = f"""
    <style>
    .map-container {{
        position: relative;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto;
        border: 2px solid #ddd;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .base-map {{
        width: 100%;
        height: auto;
        display: block;
    }}
    
    .region-icon {{
        position: absolute;
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 10;
        border-radius: 50%;
        border: 3px solid transparent;
    }}
    
    .region-icon:hover {{
        transform: scale(1.2);
        border-color: #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
    }}
    
    .region-icon:active {{
        transform: scale(1.1);
    }}
    
    #hk-icon {{
        top: 60%;
        left: 75%;
        width: 300px;
    }}
    
    #cn-icon {{
        top: 10%;
        left: 33%;
        width: 600px;
    }}
    
    #vn-icon {{
        top: 65%;
        left: 50%;
        width: 300px;
    }}
    
    .tooltip {{
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 14px;
        white-space: nowrap;
        z-index: 100;
        display: none;
        pointer-events: none;
    }}
    
    .region-name {{
        position: absolute;
        color: white;
        font-weight: bold;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        z-index: 5;
        pointer-events: none;
        font-size: 18px;
    }}
    
    #hk-name {{
        top: 45%;
        left: 75%;
    }}
    
    #cn-name {{
        top: 55%;
        left: 60%;
    }}
    
    #vn-name {{
        top: 70%;
        left: 70%;
    }}
    </style>
    
    <div class="map-container">
        <img src="data:image/png;base64,{bg_b64}" class="base-map" alt="Map Background">
        
        <img id="hk-icon" class="region-icon" 
             src="data:image/png;base64,{hk_b64}" 
             alt="Hong Kong"
             onclick="handleRegionClick('hk')"
             onmouseover="showTooltip(this, 'Explore Hong Kong')"
             onmouseout="hideTooltip()">
             
        <img id="cn-icon" class="region-icon" 
             src="data:image/png;base64,{cn_b64}" 
             alt="China"
             onclick="handleRegionClick('cn')"
             onmouseover="showTooltip(this, 'Explore China')"
             onmouseout="hideTooltip()">
             
        <img id="vn-icon" class="region-icon" 
             src="data:image/png;base64,{vn_b64}" 
             alt="Vietnam"
             onclick="handleRegionClick('vn')"
             onmouseover="showTooltip(this, 'Explore Vietnam')"
             onmouseout="hideTooltip()">
             
        <div id="hk-name" class="region-name">Hong Kong</div>
        <div id="cn-name" class="region-name">China</div>
        <div id="vn-name" class="region-name">Vietnam</div>
             
        <div id="tooltip" class="tooltip"></div>
    </div>
    
    <script>
    function handleRegionClick(region) {{
        // Use query parameters for page navigation
        try {{
            // Try to update parent window location
            if (window.parent && window.parent !== window) {{
                window.parent.location.href = window.parent.location.pathname + '?region=' + region;
            }} else {{
                window.location.href = window.location.pathname + '?region=' + region;
            }}
        }} catch (e) {{
            // Fallback: try direct navigation
            console.error('Navigation error:', e);
            window.location.href = '/?region=' + region;
        }}
    }}
    
    function showTooltip(element, text) {{
        const tooltip = document.getElementById('tooltip');
        tooltip.textContent = text;
        tooltip.style.display = 'block';
        
        // Update tooltip position
        const rect = element.getBoundingClientRect();
        const container = element.closest('.map-container');
        const containerRect = container.getBoundingClientRect();
        
        tooltip.style.left = (rect.left - containerRect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = (rect.top - containerRect.top - 35) + 'px';
    }}
    
    function hideTooltip() {{
        document.getElementById('tooltip').style.display = 'none';
    }}
    </script>
    """
    
    return map_html

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
    
    # Display overall statistics - using star_manager
    stats = star_manager.get_overall_stats()
    total_stars = stats['total_stars']
    st.markdown(f"### 🌟 Total Stars: {total_stars}/36")
    
    # Create interactive map
    st.markdown("---")
    st.markdown("### 🗺️ Click on a region on the map to start exploring")
    
    # Display clickable map regions
    st.markdown("### Click on a region to explore:")
    
    # Get paths to map images
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    assets_dir = os.path.join(project_root, "assets", "map")
    
    hk_map_path = os.path.join(assets_dir, "hk.png")
    cn_map_path = os.path.join(assets_dir, "cn.png")
    vn_map_path = os.path.join(assets_dir, "vn.png")
    
    # Create 3 columns for each region with clickable containers
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🇭🇰 Hong Kong")
        # Use button as the clickable element - image shown for context
        if os.path.exists(hk_map_path):
            st.image(hk_map_path, width='stretch')
        if st.button("👉 Click Here to Explore Hong Kong", key="hk_map_btn", width='stretch', type="primary"):
            st.switch_page("pages/1_hk.py")
    
    with col2:
        st.markdown("#### 🇨🇳 China")
        if os.path.exists(cn_map_path):
            st.image(cn_map_path, width='stretch')
        if st.button("👉 Click Here to Explore China", key="cn_map_btn", width='stretch', type="primary"):
            st.switch_page("pages/2_cn.py")
    
    with col3:
        st.markdown("#### 🇻🇳 Vietnam")
        if os.path.exists(vn_map_path):
            st.image(vn_map_path, width='stretch')
        if st.button("👉 Click Here to Explore Vietnam", key="vn_map_btn", width='stretch', type="primary"):
            st.switch_page("pages/3_vn.py")
    

if __name__ == "__main__":
    main()