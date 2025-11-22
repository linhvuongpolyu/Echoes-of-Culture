import streamlit as st
import os
from pathlib import Path
import sys

# Add utils directory to path
current_dir = Path(__file__).parent
frontend_dir = current_dir.parent
sys.path.append(str(frontend_dir))

from utils.star_manager import star_manager

# Page configuration - hide sidebar
st.set_page_config(
    page_title="Language",
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
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None

def get_current_region():
    return st.session_state.get('current_region', 'Hong Kong')

def get_region_language_data(region):
    """Return language data based on region"""
    language_data = {
        'Hong Kong': {
            'welcome_message': 'nei5 hou2',
            'welcome_audio': 'hk_lan.mp3',
            'correct_answer': 'nei5 hou2 (Hello)',
            'meaning': 'Hello'
        },
        'China': {
            'welcome_message': 'ni hao',
            'welcome_audio': 'cn_lan.mp3',
            'correct_answer': 'ni hao (你好 - Hello)',
            'meaning': 'Hello'
        },
        'Vietnam': {
            'welcome_message': 'Xin chào',
            'welcome_audio': 'vn_lan.mp3',
            'correct_answer': 'Xin chào (Hello)',
            'meaning': 'Hello'
        }
    }
    return language_data.get(region, language_data['Hong Kong'])

def get_listening_quiz_options(region):
    """Return multiple choice options for listening quiz"""
    quiz_options = {
        'Hong Kong': [
            'nei5 hou2 (Hello)',
            'gam1 jat6 (Today)',
            'm4 goi1 (Thank you)',
            'zou2 san4 (Good morning)'
        ],
        'China': [
            'ni hao (你好 - Hello)',
            'xie xie (谢谢 - Thank you)',
            'zai jian (再见 - Goodbye)',
            'wan an (晚安 - Good night)'
        ],
        'Vietnam': [
            'Xin chào (Hello)',
            'Cảm ơn (Thank you)',
            'Tạm biệt (Goodbye)',
            'Chúc ngủ ngon (Good night)'
        ]
    }
    return quiz_options.get(region, quiz_options['Hong Kong'])

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
    """Display progress using star_manager"""
    st.markdown("---")
    st.markdown("### 🌟 Overall Progress")
    
    # Get overall progress from star_manager
    stats = star_manager.get_overall_stats()
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

def main():
    # Initialize navigation counter to force fresh renders
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0
    
    # Get current region
    current_region = get_current_region()
    
    # Initialize language state
    initialize_language()
    
    # Get language data for the corresponding region
    lang_data = get_region_language_data(current_region)
    
    st.title(f"🗣️ {current_region} Language Listening Challenge")
    st.markdown(f"**Currently exploring:** {current_region}")
    
    # Instructions
    st.markdown("---")
    st.markdown("### 📝 Instructions")
    st.info("🎧 Listen carefully to the audio, then select what you heard from the options below. Get it right to earn 3 stars! ⭐⭐⭐")
    
    # Display audio player
    st.markdown("### 🎵 Listen to the Audio")
    audio_path = get_audio_file_path(lang_data['welcome_audio'])
    if audio_path and audio_path.exists():
        try:
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"Failed to load audio: {e}")
    else:
        st.warning(f"Audio file not found: {lang_data['welcome_audio']}")
    
    # Listening quiz
    st.markdown("---")
    st.markdown("### 🎯 What did you hear?")
    st.markdown("Select the correct phrase from the options below:")
    
    # Get quiz options for this region
    quiz_options = get_listening_quiz_options(current_region)
    
    # Use form for better user experience
    with st.form(key='language_form'):
        user_answer = st.radio(
            "Choose your answer:",
            quiz_options,
            key="language_quiz",
            index=None
        )
        
        submitted = st.form_submit_button("Submit Answer", type="primary", use_container_width=True)
    
    # Handle form submission
    if submitted:
        if user_answer:
            st.session_state.user_answer = user_answer
            st.session_state.language_submitted = True
            
            # Check if answer is correct
            if user_answer == lang_data['correct_answer']:
                st.session_state.language_stars = 3
                star_manager.update_stars(current_region, 'Language', 3)
            else:
                st.session_state.language_stars = 0
                star_manager.update_stars(current_region, 'Language', 0)
            
            st.rerun()
        else:
            st.warning("Please select an answer before submitting!")
    
    # Display results if submitted
    if st.session_state.language_submitted:
        st.markdown("---")
        st.markdown("### 📊 Quiz Results")
        
        # Check if answer was correct
        is_correct = st.session_state.user_answer == lang_data['correct_answer']
        
        if is_correct:
            st.success("🎉 **Correct!** You got it right!")
            st.markdown(f"### You earned 3 stars! ⭐⭐⭐")
            st.balloons()
        else:
            st.error("❌ **Incorrect.** That's not what you heard.")
            st.markdown(f"### You earned 0 stars! ☆☆☆")
            st.markdown(f"**Your answer:** {st.session_state.user_answer}")
            st.markdown(f"**Correct answer:** {lang_data['correct_answer']}")
        
        # Display star visualization
        stars_display = "⭐" * st.session_state.language_stars + "☆" * (3 - st.session_state.language_stars)
        st.markdown(f"### {stars_display}")
        
        # Additional info
        st.markdown("---")
        st.markdown("### 📚 About this phrase")
        st.info(f"**Meaning:** {lang_data['meaning']}\n\n**Pronunciation:** {lang_data['welcome_message']}")
        
        # Reset or navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Try Again", use_container_width=True):
                st.session_state.language_submitted = False
                st.session_state.language_stars = 0
                st.session_state.user_answer = None
                st.rerun()
        
        with col2:
            if st.button("Back to Main", use_container_width=True):
                # Increment navigation counter and clear region state
                st.session_state.nav_counter += 1
                if 'current_region' in st.session_state:
                    del st.session_state['current_region']
                st.switch_page("main_app.py")
        
        with col3:
            if st.button(f"Back to {current_region}", use_container_width=True):
                # Increment navigation counter for fresh render
                st.session_state.nav_counter += 1
                # Navigate back to corresponding page based on region
                if current_region == "Hong Kong":
                    st.switch_page("pages/1_hk.py")
                elif current_region == "China":
                    st.switch_page("pages/2_cn.py")
                elif current_region == "Vietnam":
                    st.switch_page("pages/3_vn.py")
    
    # Display current progress
    display_progress()

if __name__ == "__main__":
    main()