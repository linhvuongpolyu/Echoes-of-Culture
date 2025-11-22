import streamlit as st
import base64
import os
from pathlib import Path

# Page configuration - hide sidebar
st.set_page_config(
    page_title="Area Knowledge Exploration",
    page_icon="🌍",
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

# Initialize star data
def initialize_stars():
    if 'stars' not in st.session_state:
        st.session_state.stars = {
            'Hong Kong': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
            'China': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
            'Vietnam': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
        }

def get_image_base64(image_path):
    """Convert image to base64 encoding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Failed to load image {image_path}: {e}")
        return None

# Create interactive map
def create_interactive_map():
    """Create interactive map"""
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
        // 使用查询参数方法进行页面跳转
        window.parent.location.search = '?region=' + region;
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

# Display star progress
def display_stars(count, max_stars=3):
    """Display star progress"""
    stars = "⭐" * count + "☆" * (max_stars - count)
    return stars

# Main page
def main():
    # 首先检查查询参数 - 使用新的 st.query_params API
    region_param = st.query_params.get("region", [None])[0]
    
    if region_param:
        if region_param == "hk":
            st.switch_page("pages/1_hk.py")
        elif region_param == "cn":
            st.switch_page("pages/2_cn.py")
        elif region_param == "vn":
            st.switch_page("pages/3_vn.py")
    
    # Initialize star data
    initialize_stars()
    
    # Display overall statistics - using session state data
    total_stars = sum(sum(city_stars.values()) for city_stars in st.session_state.stars.values())
    st.markdown(f"### 🌟 Total Stars: {total_stars}/36")
    
    # Create interactive map
    st.markdown("---")
    st.markdown("### 🗺️ Click on a region on the map to start exploring")
    
    # Create map
    map_html = create_interactive_map()
    
    # Display map
    if map_html:
        st.components.v1.html(map_html, height=700)
    else:
        # If map creation fails, show alternative buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🇭🇰 Explore Hong Kong", width=True, key="hk_map_btn"):
                st.switch_page("pages/1_hk.py")
        
        with col2:
            if st.button("🇨🇳 Explore China", width=True, key="cn_map_btn"):
                st.switch_page("pages/2_cn.py")
        
        with col3:
            if st.button("🇻🇳 Explore Vietnam", width=True, key="vn_map_btn"):
                st.switch_page("pages/3_vn.py")
    
    # Handle region selection
    st.markdown("---")
    st.markdown("### Select Region:")
    
    # Use radio buttons as region selector
    selected_region = st.radio(
        "Choose a region to explore:",
        ["Hong Kong", "China", "Vietnam"],
        horizontal=True,
        key="region_radio"
    )
    
    # Confirm button
    if st.button(f"Explore {selected_region}", type="primary", width=True):
        if selected_region == "Hong Kong":
            st.switch_page("pages/1_hk.py")
        elif selected_region == "China":
            st.switch_page("pages/2_cn.py")
        elif selected_region == "Vietnam":
            st.switch_page("pages/3_vn.py")
    
    # Debug information - showing asset paths
    st.sidebar.markdown("### Debug Information")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)
    assets_dir = os.path.join(project_root, "assets", "map")
    st.sidebar.write(f"Project Root Directory: {project_root}")
    st.sidebar.write(f"Assets Directory: {assets_dir}")

if __name__ == "__main__":
    main()