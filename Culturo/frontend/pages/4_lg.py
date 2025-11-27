import streamlit as st
import os
from pathlib import Path
import sys

# Add utils directory to path
current_dir = Path(__file__).parent
frontend_dir = current_dir.parent
sys.path.append(str(frontend_dir))

from utils.star_manager import star_manager

# Build absolute path to logo
logo_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.png"
logo_icon = str(logo_path) if logo_path.exists() else "🗣️"

# Page configuration
st.set_page_config(
    page_title="Language - Culturo",
    page_icon=logo_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styles
st.markdown("""
    <style>
        /* Hide page navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        
        /* Sidebar styling - solid white */
        [data-testid="stSidebar"] {
            background: #FFFFFF !important;
        }
        
        /* Page background: solid color */
        html, body, .stApp {
            background: #EFF8FF !important;
            background-attachment: fixed !important;
            min-height: 100vh !important;
        }
        /* Make inner containers transparent so background shows through */
        .main, .block-container, .stApp > header, [data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* Header row tweaks */
        .vn-header { display: flex; align-items: center; gap: 6px; }
        /* Reduce default column inner padding to bring items closer */
        .stColumns > div { padding-left: 0 !important; padding-right: 0 !important; }
        /* Reduce gutter between header columns */
        .stColumns { gap: 6px !important; }
        
        /* Hide heading anchor/link icon next to titles */
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { display: none !important; }
        
        /* Form container - white background */
        div[data-testid="stForm"] {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
            border: 1px solid #E0E0E0 !important;
            padding: 1rem !important;
        }
        
        /* (Removed per-page button color override to use global theme) */
    </style>
    """, unsafe_allow_html=True)

def initialize_language():
    if 'language_submitted' not in st.session_state:
        st.session_state.language_submitted = False
    if 'language_stars' not in st.session_state:
        st.session_state.language_stars = 0
    if 'user_answer' not in st.session_state:
        st.session_state.user_answer = None

def reset_language_state():
    st.session_state.language_submitted = False
    st.session_state.language_stars = 0
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

def get_region_image_path(region):
    """Get the image path for the region"""
    project_root = Path(__file__).parent.parent.parent
    image_files = {
        'Hong Kong': 'hk_lg.png',
        'China': 'cn_lg.png',
        'Vietnam': 'vn_lg.png'
    }
    image_filename = image_files.get(region, 'hk_lg.png')
    image_path = project_root / "assets" / "languages" / "image" / image_filename
    return image_path if image_path.exists() else None

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
    
    # Check if region changed and reset language state if needed
    if 'last_language_region' not in st.session_state:
        st.session_state.last_language_region = current_region
    elif st.session_state.last_language_region != current_region:
        reset_language_state()
        st.session_state.last_language_region = current_region
    
    # Initialize language state
    initialize_language()
    
    # Get language data for the corresponding region
    lang_data = get_region_language_data(current_region)
    
    # Get current stars for language activity
    current_stars = star_manager.get_stars(current_region).get('Language', 0)
    
    # Header: Back button, title, and stars in the same row
    header_left, header_middle, header_right = st.columns([0.1, 0.75, 0.15])
    with header_left:
        back_clicked = st.button("←\nBack", key="back_btn_lang", width='stretch')
    with header_middle:
        # Get flag URL based on region
        flag_urls = {
            'Vietnam': 'https://flagcdn.com/w80/vn.png',
            'China': 'https://flagcdn.com/w80/cn.png',
            'Hong Kong': 'https://flagcdn.com/w80/hk.png'
        }
        flag_url = flag_urls.get(current_region, '')
        
        # Get region color
        region_colors = {
            'Vietnam': '#1C8575',  # VN teal-green
            'China': '#DE5862',    # China warm red
            'Hong Kong': '#DA901E' # HK amber
        }
        region_color = region_colors.get(current_region, '#1C8575')
        
        st.markdown(f"""
            <div class="vn-header">
                <img src="{flag_url}" width="50" height="33" style="border-radius: 3px;" />
                <div style="display: flex; flex-direction: column;">
                    <h2 style="margin: 0; padding: 0; color: {region_color}; font-size: 1.6rem; font-weight: 600; line-height: 1;">Language</h2>
                    <p style="margin: 0; padding: 0; color: #666; font-size: 0.9rem; line-height: 1;">Listen, guess, and learn new words!</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with header_right:
        # Display stars on the right
        filled_stars = '⭐' * current_stars
        empty_stars = '☆' * (3 - current_stars)
        st.markdown(f"""
            <div style="text-align: right; padding-top: 8px;">
                <div style="font-size: 1.5rem; letter-spacing: 2px; display: inline-block;">{filled_stars}{empty_stars} <span style="font-size: 0.9rem; color: #666; margin-left: 8px;">{current_stars}/3</span></div>
            </div>
        """, unsafe_allow_html=True)
    
    if back_clicked:
        st.session_state.nav_counter += 1
        reset_language_state()  # Reset language state when switching regions
        # Navigate back based on region
        if current_region == "Hong Kong":
            st.switch_page("pages/1_hk.py")
        elif current_region == "China":
            st.switch_page("pages/2_cn.py")
        elif current_region == "Vietnam":
            st.switch_page("pages/3_vn.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create two columns layout - image on left, content on right
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        # Display region image only, no box or text
        region_image_path = get_region_image_path(current_region)
        if region_image_path and region_image_path.exists():
            st.image(str(region_image_path), width='stretch')
    
    with right_col:
        # Title - just text, no box
        st.markdown("""
            <h3 style="margin: 0 0 1rem 0; display: flex; align-items: center; gap: 8px; font-size: 1.5rem; font-weight: 600;">
                <span style="font-size: 1.8rem;">🔊</span> What did you hear?
            </h3>
        """, unsafe_allow_html=True)
        
        # Display audio player
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
        
        # Add CSS to override button color - multiple selectors for higher specificity
        st.markdown("""
        <style>
        /* Target all possible button selectors */
        button[data-testid="baseButton-primary"],
        button[kind="primary"],
        div[data-testid="stForm"] button[data-testid="baseButton-primary"],
        div[data-testid="stForm"] button[kind="primary"],
        div.stForm button[kind="primary"],
        form button[kind="primary"] {
            background-color: #004DA0 !important;
            background: #004DA0 !important;
            border: none !important;
        }
        button[data-testid="baseButton-primary"]:hover,
        button[kind="primary"]:hover,
        div[data-testid="stForm"] button[data-testid="baseButton-primary"]:hover,
        div[data-testid="stForm"] button[kind="primary"]:hover {
            background-color: #003D80 !important;
            background: #003D80 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Get quiz options for this region
        quiz_options = get_listening_quiz_options(current_region)
        
        # If not submitted yet, show form normally
        if not st.session_state.language_submitted:
            # Use form for better user experience
            with st.form(key='language_form'):
                user_answer = st.radio(
                    "Select your answer",
                    quiz_options,
                    key="language_quiz",
                    index=None,
                    label_visibility="collapsed"
                )
                
                submitted = st.form_submit_button("Submit Answer", type="primary", width='stretch')
            
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
        
        # Display results if submitted - in 2 columns
        else:
            # Check if answer was correct
            is_correct = st.session_state.user_answer == lang_data['correct_answer']
            
            # Add CSS to reduce spacing around success/error messages and separator
            st.markdown("""
            <style>
            div[data-testid="stAlert"] {
                margin-top: 0rem !important;
                margin-bottom: 0.25rem !important;
                padding: 0.4rem 0.8rem !important;
            }
            hr {
                margin-top: 0.25rem !important;
                margin-bottom: 0.5rem !important;
            }
            /* Reduce spacing in info column */
            .element-container:has(h3) {
                margin-bottom: 0.1rem !important;
            }
            .stMarkdown + div[data-testid="stInfo"] {
                margin-top: 0.1rem !important;
            }
            div[data-testid="stInfo"] {
                margin-bottom: 0.3rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            if is_correct:
                st.success("🎉 Completed! You earned 3 stars!")
                st.balloons()
            else:
                st.error("❌ Incorrect. That's not what you heard.")
            
            # Create two columns: quiz on left, info on right
            st.markdown("---")
            quiz_col, info_col = st.columns([0.4, 0.6])
            
            with quiz_col:
                # Show the quiz options (read-only view)
                st.markdown("**Your selection:**")
                for option in quiz_options:
                    if option == st.session_state.user_answer:
                        if option == lang_data['correct_answer']:
                            st.markdown(f"✅ **{option}**")
                        else:
                            st.markdown(f"❌ **{option}**")
                    elif option == lang_data['correct_answer']:
                        st.markdown(f"✅ {option}")
                    else:
                        st.markdown(f"⚪ {option}")
            
            with info_col:
                st.markdown('<h4 style="margin: 0 0 0.2rem 0; font-size: 1.1rem; font-weight: 600;">📚 About this phrase</h4>', unsafe_allow_html=True)
                st.info(f"**Meaning:** {lang_data['meaning']}\n\n**Pronunciation:** {lang_data['welcome_message']}")
                
                # Try Again button below the info
                if st.button("🔄 Try Again", width='stretch', key="try_again_lang"):
                    st.session_state.language_submitted = False
                    st.session_state.language_stars = 0
                    st.session_state.user_answer = None
                    st.rerun()
    
    # Sidebar
    logo_path = Path(__file__).parent.parent.parent / "assets" / "images" / "Cultoro.jpg"
    with st.sidebar:
        if logo_path.exists():
            st.image(str(logo_path), width=200)
        else:
            st.markdown(
                """
                <div style="text-align:center; padding:1rem 0;">
                    <h3>🌍 Culturo</h3>
                    <p style="font-size:0.8rem; color:#666; margin:0;">Discover culture all the world!</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if st.button("← General", key="sidebar_general_lang", width="stretch"):
            st.session_state.nav_counter += 1
            if 'current_region' in st.session_state:
                del st.session_state['current_region']
            st.switch_page("main_app.py")

        with st.expander("Discover", expanded=True):
            if st.button("China", key="nav_cn_from_lang", width="stretch", disabled=(current_region == "China")):
                if current_region != "China":
                    st.session_state.current_region = "China"
                    st.switch_page("pages/2_cn.py")
            if st.button("Hong Kong", key="nav_hk_from_lang", width="stretch", disabled=(current_region == "Hong Kong")):
                if current_region != "Hong Kong":
                    st.session_state.current_region = "Hong Kong"
                    st.switch_page("pages/1_hk.py")
            if st.button("Viet Nam", key="nav_vn_from_lang", width="stretch", disabled=(current_region == "Vietnam")):
                if current_region != "Vietnam":
                    st.session_state.current_region = "Vietnam"
                    st.switch_page("pages/3_vn.py")

if __name__ == "__main__":
    main()