import streamlit as st
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.star_manager import star_manager

def china_page():
    # Initialize navigation counter to force fresh renders
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0
    
    st.title("🇨🇳 China Knowledge Exploration")
    st.markdown("Welcome to the Chinese Culture Learning Platform!")
    
    # Get China stars data from star_manager
    stars = star_manager.get_stars("China")
    total_stars = star_manager.get_total_stars("China")
    
    st.sidebar.markdown(f"### 🌟 Current Stars: {total_stars}/12")
    
    # Show activity progress
    st.sidebar.markdown("#### Activity Progress:")
    for activity, star_count in stars.items():
        st.sidebar.markdown(f"{activity}: {star_manager.display_stars(star_count)}")
    
    # Four feature sections
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🗣️ Language")
        st.markdown("Learn Mandarin pronunciation")
        if st.button("Language", key="lang_cn"):
            st.session_state.current_region = "China"
            st.switch_page("pages/4_lg.py")
    
    with col2:
        st.markdown("### 🎨 Draw animals")
        st.markdown("Draw animals characteristic of China")
        if st.button("Draw Animals", key="draw_cn"):
            st.session_state.current_region = "China"
            st.switch_page("pages/5_draw.py")
    
    with col3:
        st.markdown("### 📺 Food Culture")
        st.markdown("Watch the video and answer questions")
        if st.button("Food Culture Quiz", key="food_cn"):
            st.session_state.current_region = "China"
            st.switch_page("pages/6_food.py")
    
    with col4:
        st.markdown("### 📹 Performance Culture")
        st.markdown("Watch the video and answer questions")
        if st.button("Performance Culture Quiz", key="per_cn"):
            st.session_state.current_region = "China"
            st.switch_page("pages/7_per.py")
    
    # Back to Main button
    if st.button("Back to Main"):
        # Increment navigation counter and clear region state
        st.session_state.nav_counter += 1
        if 'current_region' in st.session_state:
            del st.session_state['current_region']
        st.switch_page("main_app.py")

if __name__ == "__main__":
    china_page()
