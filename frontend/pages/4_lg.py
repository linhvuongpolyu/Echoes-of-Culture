import streamlit as st
import os
from pathlib import Path
import sys

# Add utils directory to path
current_dir = Path(__file__).parent
frontend_dir = current_dir.parent
sys.path.append(str(frontend_dir))

try:
    from utils.api_client import star_client
    API_AVAILABLE = True
except ImportError as e:
    st.error(f"Cannot import API client: {e}")
    API_AVAILABLE = False

# Page configuration - hide sidebar
st.set_page_config(
    page_title="Language Imitation",
    page_icon="🗣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS to completely hide sidebar
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        /* Adjust main content area spacing */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

def initialize_language():
    if 'language_submitted' not in st.session_state:
        st.session_state.language_submitted = False
    if 'language_stars' not in st.session_state:
        st.session_state.language_stars = 0

def get_current_region():
    return st.session_state.get('current_region', 'Hong Kong')

def get_region_language_data(region):
    """Return language data based on region"""
    language_data = {
        'Hong Kong': {
            'welcome_message': 'nei5 hou2',
            'welcome_audio': 'hk_lan.mp3'
        },
        'China': {
            'welcome_message': 'ni hao',
            'welcome_audio': 'cn_lan.mp3'
        },
        'Vietnam': {
            'welcome_message': 'Xin chào',
            'welcome_audio': 'vn_lan.mp3'
        }
    }
    return language_data.get(region, language_data['Hong Kong'])

def get_audio_file_path(audio_filename):
    """Get the full path of audio file"""
    project_root = Path(__file__).parent.parent.parent
    audio_path = project_root / "assets" / "languages" / audio_filename
    return audio_path if audio_path.exists() else None

def play_audio(audio_filename):
    """Play audio file"""
    audio_path = get_audio_file_path(audio_filename)
    if audio_path and audio_path.exists():
        try:
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            return True
        except Exception as e:
            st.error(f"Failed to play audio: {e}")
            return False
    else:
        st.warning(f"Audio file not found: {audio_filename}")
        return False

def display_progress():
    """Fetch and display progress from backend API"""
    st.markdown("---")
    st.markdown("### 🌟 Overall Progress")
    
    if not API_AVAILABLE:
        st.warning("⚠️ Backend API is not available, unable to display progress information")
        st.info("Please ensure the backend service is running: `cd backend && python api_server.py`")
        return
    
    # Get overall progress
    result = star_client.get_overall_stats()
    if result and result.get('success'):
        stats = result['data']
        all_stars = stats['all_stars']
        total_stars = stats['total_stars']
        max_total_stars = stats['max_total_stars']
        
        # Display overall progress
        st.markdown(f"### Total Progress: {total_stars}/{max_total_stars} Stars")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            hk_stars = all_stars.get('Hong Kong', {})
            hk_total = sum(hk_stars.values())
            st.markdown(f"#### 🇭🇰 Hong Kong: {hk_total}/12")
            for activity, stars in hk_stars.items():
                stars_display = "⭐" * stars + "☆" * (3 - stars)
                st.markdown(f"**{activity}:** {stars_display}")
        
        with col2:
            cn_stars = all_stars.get('China', {})
            cn_total = sum(cn_stars.values())
            st.markdown(f"#### 🇨🇳 China: {cn_total}/12")
            for activity, stars in cn_stars.items():
                stars_display = "⭐" * stars + "☆" * (3 - stars)
                st.markdown(f"**{activity}:** {stars_display}")
        
        with col3:
            vn_stars = all_stars.get('Vietnam', {})
            vn_total = sum(vn_stars.values())
            st.markdown(f"#### 🇻🇳 Vietnam: {vn_total}/12")
            for activity, stars in vn_stars.items():
                stars_display = "⭐" * stars + "☆" * (3 - stars)
                st.markdown(f"**{activity}:** {stars_display}")
        
        # Progress bar
        progress = total_stars / max_total_stars
        st.progress(progress)
        st.markdown(f"**Overall Completion: {progress:.1%}**")
        
    else:
        st.error("❌ Cannot fetch star data from backend")
        st.info("Please check if the backend service is running")

def main():
    # Get current region
    current_region = get_current_region()
    
    # Initialize language state
    initialize_language()
    
    # Get language data for the corresponding region
    lang_data = get_region_language_data(current_region)
    
    st.title(f"🗣️ {current_region} Language Imitation")
    st.markdown(f"**Currently exploring:** {current_region}")
    
    # Display welcome message and play welcome audio
    st.markdown(f"### {lang_data['welcome_message']}")
    
    # Welcome audio play button
    if st.button("🎵 Play Audio", key="welcome_audio"):
        play_audio(lang_data['welcome_audio'])
    
    # Imitation practice area
    st.markdown("### 🎤 Practice Imitation")
    
    # Use form for better user experience
    with st.form(key='language_form'):
        user_input = st.text_area(
            "Enter your imitation here:", 
            height=100, 
            placeholder="Please enter your imitation pronunciation...",
            key="language_input",
            help="Listen carefully to the original audio, then try to imitate and enter your pronunciation"
        )
        
        submitted = st.form_submit_button("Submit Imitation", type="primary", width=True)
    
    # Handle form submission
    if submitted:
        if user_input.strip():
            st.session_state.language_submitted = True
            
            # Save stars to backend API
            if API_AVAILABLE:
                result = star_client.update_stars(current_region, 'Language Imitation', 3)
                if result and result.get('success'):
                    st.success("✅ Stars saved to backend system!")
                    st.session_state.language_stars = 3
                else:
                    st.error("❌ Failed to save stars to backend")
                    st.session_state.language_stars = 3  # Still show success to user
            else:
                st.warning("⚠️ API unavailable, stars not saved")
                st.session_state.language_stars = 3
            
            st.rerun()
        else:
            st.warning("Please enter your imitation pronunciation first")
    
    # Display results if submitted
    if st.session_state.language_submitted:
        st.markdown("---")
        st.markdown("### 📊 Practice Results")
        
        st.markdown(f"### You earned {st.session_state.language_stars} out of 3 stars! ⭐")
        
        # Display star visualization
        stars_display = "⭐" * st.session_state.language_stars + "☆" * (3 - st.session_state.language_stars)
        st.markdown(f"### {stars_display}")
        
        st.markdown("🎉 Congratulations! You completed the language imitation practice!")
        
        # Reset or navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Practice Again", width=True):
                st.session_state.language_submitted = False
                st.session_state.language_stars = 0
                st.rerun()
        
        with col2:
            if st.button("Back to Main", width=True):
                st.switch_page("main_app.py")
        
        with col3:
            if st.button(f"Back to {current_region}", width=True):
                # Navigate back to corresponding page based on region
                if current_region == "Hong Kong":
                    st.switch_page("pages/1_hk.py")
                elif current_region == "China":
                    st.switch_page("pages/2_cn.py")
                elif current_region == "Vietnam":
                    st.switch_page("pages/3_vn.py")
    
    # Display current progress from backend
    display_progress()
    
    # API status indication
    if not API_AVAILABLE:
        st.markdown("---")
        st.markdown("### 🔧 System Status")
        st.error("Backend API is not available")
        st.info("To enable star tracking, please start the backend server:")
        st.code("cd backend && python api_server.py")

if __name__ == "__main__":
    main()