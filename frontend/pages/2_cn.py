import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

def api_get(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def api_post(endpoint, data):
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def display_stars(count, max_stars=3):
    return "⭐" * count + "☆" * (max_stars - count)

def china_page():
    st.title("🇨🇳 China Knowledge Exploration")
    st.markdown("Welcome to the Chinese Culture Learning Platform!")
    
    # Get China stars data
    stars_data = api_get("/api/stars/China")
    
    if stars_data:
        stars = stars_data.get("stars", {})
        total_stars = sum(stars.values())
        st.sidebar.markdown(f"### 🌟 Current Stars: {total_stars}/12")
        
        # Show activity progress
        st.sidebar.markdown("#### Activity Progress:")
        for activity, star_count in stars.items():
            st.sidebar.markdown(f"{activity}: {display_stars(star_count)}")
    
    # Four feature sections
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🗣️ Language Imitation")
        st.markdown("Learn and imitate Mandarin pronunciation")
        if st.button("Language Imitation", key="lang_cn"):
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
        st.switch_page("main_app.py")

if __name__ == "__main__":
    china_page()