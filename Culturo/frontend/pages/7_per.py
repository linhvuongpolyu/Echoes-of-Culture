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
logo_path = Path(__file__).parent.parent.parent / "assets" / "images" / "Cultoro.jpg"
logo_icon_path = Path(__file__).parent.parent.parent / "assets" / "images" / "logo.png"
logo_icon = str(logo_icon_path) if logo_icon_path.exists() else "🎭"

# Page configuration
st.set_page_config(
    page_title="Performance - Culturo",
    page_icon=logo_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
    <style>
        /* Hide sidebar navigation items above logo */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* Remove top padding from sidebar */
        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
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
        
        /* Adjust main content area spacing */
        .main .block-container {
            padding-top: 2rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }
        
        /* Header row tweaks */
        .vn-header { display: flex; align-items: center; gap: 6px; }
        
        /* Video styling */
        .video-container {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .video-player {
            width: 80%;
            max-width: 800px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        /* Quiz styling */
        .quiz-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .question {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .star-result {
            text-align: center;
            padding: 20px;
            background-color: transparent;
            border: none;
            border-radius: 0;
            margin-top: 20px;
        }
        .region-header {
            text-align: center;
            padding: 10px;
            background-color: transparent;
            border: none;
            border-radius: 0;
            margin-bottom: 20px;
        }
        .correct-answer {
            color: green;
            font-weight: bold;
        }
        .incorrect-answer {
            color: red;
        }
        /* Remove borders from radio buttons */
        div[data-testid="stRadio"] > div {
            background-color: transparent;
            border: none;
            padding: 0;
        }
        /* Hide the quiz container borders */
        .quiz-container {
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            margin-bottom: 10px;
            box-shadow: none;
            border: none;
        }
        /* Encouragement message styling */
        .encouragement {
            text-align: center;
            padding: 20px;
            background-color: transparent;
            border: none;
            border-radius: 0;
            margin-top: 20px;
            border: 1px solid #ffeaa7;
        }
        /* Progress styling */
        .progress-section {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize quiz data
def initialize_quiz():
    if 'per_quiz_answers' not in st.session_state:
        st.session_state.per_quiz_answers = [None, None, None]
    if 'per_quiz_submitted' not in st.session_state:
        st.session_state.per_quiz_submitted = False
    if 'per_quiz_score' not in st.session_state:
        st.session_state.per_quiz_score = 0

def reset_performance_state():
    st.session_state.per_quiz_answers = [None, None, None]
    st.session_state.per_quiz_submitted = False
    st.session_state.per_quiz_score = 0
    if 'per_current_question' in st.session_state:
        st.session_state.per_current_question = 0

# Get current region from session state
def get_current_region():
    return st.session_state.get('current_region', 'Hong Kong')

# Get region-specific video file
def get_region_video(region):
    # Map region names to corresponding video filenames
    region_video_mapping = {
        'Hong Kong': 'hk_per.mp4',
        'China': 'cn_per.mp4', 
        'Vietnam': 'vn_per.mp4'
    }
    
    video_filename = region_video_mapping.get(region)
    
    if video_filename:
        # Use relative path from project root directory
        project_root = Path(__file__).parent.parent.parent
        video_path = project_root / "assets" / "videos" / video_filename
        
        if video_path.exists():
            return str(video_path)
    
    return None

# Get region-specific quiz questions
def get_region_quiz_data(region):
    # Region-specific quiz questions based on user's input
    quiz_data = {
        'Vietnam': [
            {
                "question": "Where is the best place in Vietnam to watch the Water Puppet Show?",
                "options": [
                    "Danang Theater",
                    "Hanoi Thang Long Theater", 
                    "Hoi An Theater",
                    "Ho Chi Minh City Thao Dien Village"
                ],
                "correct_answer": "Hanoi Thang Long Theater"
            },
            {
                "question": "How are the puppeteers able to control the puppets without being seen by the audience?",
                "options": [
                    "They use long strings while standing on a platform above the stage.",
                    "They operate the puppets using rods from the sides of the stage, dressed in black.",
                    "They stand and manipulate the puppets using long bamboo rods and strings from behind a bamboo screen, hidden in waist-deep water.",
                    "They use remote control and digital technology to animate the puppets."
                ],
                "correct_answer": "They stand and manipulate the puppets using long bamboo rods and strings from behind a bamboo screen, hidden in waist-deep water."
            },
            {
                "question": "What are the traditional stories of Water Puppetry primarily based on?",
                "options": [
                    "Scenes from daily rural life and ancient Vietnamese folklore.",
                    "Tales from Indian mythology and epic poems",
                    "Stories about the royal court and famous emperors.",
                    "Buddhist parables and religious teachings."
                ],
                "correct_answer": "Scenes from daily rural life and ancient Vietnamese folklore."
            }
        ],
        'China': [
            {
                "question": "What is the Chinese art of 'Face Changing' called?",
                "options": [
                    "Jingju",
                    "Bian Lian", 
                    "Qigong",
                    "Shen Yun"
                ],
                "correct_answer": "Bian Lian"
            },
            {
                "question": "Face Changing is most associated with which Chinese performing art?",
                "options": [
                    "Puppet Show",
                    "Sichuan Opera",
                    "Beijing Acrobatics", 
                    "Lion Dance"
                ],
                "correct_answer": "Sichuan Opera"
            },
            {
                "question": "What is the primary mechanism traditionally used to perform the rapid mask changes?",
                "options": [
                    "Digital projections and holograms",
                    "The performer quickly turns their back to the audience",
                    "Elaborate, pre-arranged silk masks and subtle hand movements",
                    "A team of assistants hidden on stage"
                ],
                "correct_answer": "Elaborate, pre-arranged silk masks and subtle hand movements"
            }
        ],
        'Hong Kong': [
            {
                "question": "The Chao Shan Ying Ge Dance is a traditional folk performance most associated with which Chinese province?",
                "options": [
                    "Sichuan",
                    "Guangdong",
                    "Shaanxi", 
                    "Jiangsu"
                ],
                "correct_answer": "Guangdong"
            },
            {
                "question": "What is the main theme or story depicted in the Ying Ge Dance?",
                "options": [
                    "The legend of the Monkey King",
                    "The story of a famous Qing Dynasty emperor",
                    "The heroes from the classic novel Outlaws of the Marshes",
                    "A celebration of the harvest season"
                ],
                "correct_answer": "The heroes from the classic novel Outlaws of the Marshes"
            },
            {
                "question": "Which of these is a characteristic feature of the dancers' appearance?",
                "options": [
                    "Elaborate, colorful face paint patterns",
                    "They perform on stilts",
                    "They wear masks and traditional opera costumes", 
                    "They carry small drums and strike powerful, rhythmic movements"
                ],
                "correct_answer": "Elaborate, colorful face paint patterns"
            }
        ]
    }
    
    return quiz_data.get(region, quiz_data['Hong Kong'])  # Default to Hong Kong if region not found

# Get encouragement message based on score
def get_encouragement_message(score, region):
    if score == 0:
        messages = [
            f"Don't worry! Learning about {region}'s performance culture is a journey. Every expert was once a beginner!",
            f"Not to worry! Exploring {region}'s performing arts is an adventure. Try again and you'll do better!",
            f"Keep your chin up! {region}'s performance culture is rich and diverse. Give it another try!",
            f"Don't be discouraged! Learning about {region}'s performing traditions takes time. You'll get it next time!"
        ]
        import random
        return random.choice(messages)
    elif score == 1:
        return f"Good start! You're beginning to understand {region}'s performance culture. Keep learning!"
    elif score == 2:
        return f"Well done! You have a good knowledge of {region}'s performing traditions!"
    else:  # score == 3
        return f"Excellent! You're a true expert on {region}'s performance culture!"
# Display progress
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

# Main page
def main():
    # Initialize navigation counter to force fresh renders
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0
    
    # Get current region
    current_region = get_current_region()
    
    # Check if region changed and reset performance state if needed
    if 'last_performance_region' not in st.session_state:
        st.session_state.last_performance_region = current_region
    elif st.session_state.last_performance_region != current_region:
        reset_performance_state()
        st.session_state.last_performance_region = current_region
    
    # Initialize quiz state
    initialize_quiz()
    
    # Get current stars for performance activity
    current_stars = star_manager.get_stars(current_region).get('Performance', 0)
    
    # Header: Back button, title, and stars in the same row
    header_left, header_middle, header_right = st.columns([0.1, 0.75, 0.15])
    with header_left:
        back_clicked = st.button("←\nBack", key="back_btn_per", width='stretch')
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
                    <h2 style="margin: 0; padding: 0; color: {region_color}; font-size: 1.6rem; font-weight: 600; line-height: 1;">Performance Art</h2>
                    <p style="margin: 0; padding: 0; color: #666; font-size: 0.9rem; line-height: 1;">Ready to explore art from around the world?</p>
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
        reset_performance_state()  # Reset performance state when switching regions
        # Navigate back based on region
        if current_region == "Hong Kong":
            st.switch_page("pages/1_hk.py")
        elif current_region == "China":
            st.switch_page("pages/2_cn.py")
        elif current_region == "Vietnam":
            st.switch_page("pages/3_vn.py")
    
    # Get region-specific quiz questions
    quiz_data = get_region_quiz_data(current_region)
    
    # Initialize current question index
    if 'per_current_question' not in st.session_state:
        st.session_state.per_current_question = 0
    
    current_q_index = st.session_state.per_current_question
    
    # Add spacing between header and content
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create two columns layout
    video_col, quiz_col = st.columns([0.5, 0.5])
    
    with video_col:
        # Get the correct video for the current region
        video_path = get_region_video(current_region)
        
        if video_path and os.path.exists(video_path):
            try:
                st.video(video_path)
                st.markdown("<p style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 0.5rem;'>Click play to watch the video</p>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Unable to play video: {e}")
        else:
            st.warning("Video not available for the selected region.")
        
        # Try Again button appears here when quiz is completed
        if st.session_state.per_quiz_submitted:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Try Again", width="stretch"):
                st.session_state.per_quiz_answers = [None, None, None]
                st.session_state.per_quiz_submitted = False
                st.session_state.per_quiz_score = 0
                st.session_state.per_current_question = 0
                st.rerun()
    
    with quiz_col:
        # Display current question
        if not st.session_state.per_quiz_submitted:
            q = quiz_data[current_q_index]
            
            # Box 1: Header with Quiz Time and question number
            st.markdown(f"""
            <div style="background: white; padding: 0.5rem 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 1.2rem;">📝</span>
                    <span style="font-weight: 600; font-size: 1rem;">Quiz Time!</span>
                    <span style="margin-left: auto; color: #666; font-size: 0.85rem;">Question {current_q_index + 1} of {len(quiz_data)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Box 2: Question and answer options in a simple white container
            with st.container(border=True):
                st.markdown(f"**{current_q_index + 1}. {q['question']}**")
                
                # Get current answer
                current_answer = st.session_state.per_quiz_answers[current_q_index]
                
                # Radio buttons for options
                user_answer = st.radio(
                    "Select your answer:",
                    q["options"],
                    key=f"per_q{current_q_index}_{current_region}_{st.session_state.nav_counter}",
                    index=None if current_answer is None else q["options"].index(current_answer),
                    label_visibility="collapsed"
                )
                
                # Store the answer
                if user_answer:
                    st.session_state.per_quiz_answers[current_q_index] = user_answer
            
            # Box 3: Navigation buttons - simple approach
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if current_q_index > 0:
                    if st.button("← Back", width="stretch", key="back_q"):
                        st.session_state.per_current_question -= 1
                        st.rerun()
            
            with col2:
                if current_q_index < len(quiz_data) - 1:
                    if st.button("Next →", width="stretch", key="next_q"):
                        st.session_state.per_current_question += 1
                        st.rerun()
                else:
                    # Submit button on last question
                    if st.button("Submit Answer", type="primary", width="stretch", key="submit_quiz"):
                            # Check if all questions are answered
                            if None in st.session_state.per_quiz_answers:
                                st.error("Please answer all questions before submitting.")
                            else:
                                # Calculate score
                                score = 0
                                for i, quiz_q in enumerate(quiz_data):
                                    if st.session_state.per_quiz_answers[i] == quiz_q["correct_answer"]:
                                        score += 1
                                
                                st.session_state.per_quiz_score = score
                                st.session_state.per_quiz_submitted = True
                                
                                # Save stars using star_manager
                                star_manager.update_stars(current_region, 'Performance', score)
                                
                                st.rerun()
        
        # Display results if submitted
        else:
            # Different message and style based on score
            if st.session_state.per_quiz_score == 0:
                st.error(f"😔 Quiz completed. You earned {st.session_state.per_quiz_score} stars.")
                # Snow effect for 0 stars (gentle, contemplative)
                st.markdown("""
                <style>
                @keyframes snowfall {
                    0% { transform: translateY(-10vh) translateX(0px); opacity: 1; }
                    100% { transform: translateY(100vh) translateX(100px); opacity: 0; }
                }
                .snowflake {
                    position: fixed;
                    top: -10vh;
                    color: #ddd;
                    user-select: none;
                    pointer-events: none;
                    animation: snowfall 3s linear infinite;
                    z-index: 1000;
                }
                </style>
                <div class="snowflake" style="left: 10%; animation-delay: 0s;">❄️</div>
                <div class="snowflake" style="left: 20%; animation-delay: 0.5s;">❄️</div>
                <div class="snowflake" style="left: 30%; animation-delay: 1s;">❄️</div>
                <div class="snowflake" style="left: 40%; animation-delay: 1.5s;">❄️</div>
                <div class="snowflake" style="left: 50%; animation-delay: 2s;">❄️</div>
                <div class="snowflake" style="left: 60%; animation-delay: 2.5s;">❄️</div>
                <div class="snowflake" style="left: 70%; animation-delay: 0.8s;">❄️</div>
                <div class="snowflake" style="left: 80%; animation-delay: 1.2s;">❄️</div>
                <div class="snowflake" style="left: 90%; animation-delay: 1.8s;">❄️</div>
                """, unsafe_allow_html=True)
            else:
                st.success(f"🎉 Completed! You earned {st.session_state.per_quiz_score} stars!")
                # Balloons effect for score > 0
                st.balloons()
            
            # Display star visualization
            stars_display = "⭐" * st.session_state.per_quiz_score + "☆" * (3 - st.session_state.per_quiz_score)
            st.markdown(f"<div style='text-align: center; font-size: 2rem; margin: 1rem 0;'>{stars_display}</div>", unsafe_allow_html=True)
            
            # Show encouragement message based on score
            encouragement_msg = get_encouragement_message(st.session_state.per_quiz_score, current_region)
            st.info(encouragement_msg)
            
            # Show correct answers with tighter spacing
            st.markdown("---")
            st.markdown("**Question Review:**")
            review_text = ""
            for i, q in enumerate(quiz_data):
                user_answer = st.session_state.per_quiz_answers[i]
                correct_answer = q["correct_answer"]
                is_correct = user_answer == correct_answer
                
                if is_correct:
                    review_text += f"✅ **Q{i+1}:** Correct!  \n"
                else:
                    review_text += f"❌ **Q{i+1}:** {correct_answer}  \n"
            
            st.markdown(review_text, unsafe_allow_html=True)
    
    # Sidebar
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

        if st.button("← General", key="sidebar_general_per", width="stretch"):
            st.session_state.nav_counter += 1
            if 'current_region' in st.session_state:
                del st.session_state['current_region']
            st.switch_page("main_app.py")

        with st.expander("Discover", expanded=True):
            if st.button("China", key="nav_cn_from_per", width="stretch", disabled=(current_region == "China")):
                if current_region != "China":
                    st.session_state.current_region = "China"
                    st.switch_page("pages/2_cn.py")
            if st.button("Hong Kong", key="nav_hk_from_per", width="stretch", disabled=(current_region == "Hong Kong")):
                if current_region != "Hong Kong":
                    st.session_state.current_region = "Hong Kong"
                    st.switch_page("pages/1_hk.py")
            if st.button("Viet Nam", key="nav_vn_from_per", width="stretch", disabled=(current_region == "Vietnam")):
                if current_region != "Vietnam":
                    st.session_state.current_region = "Vietnam"
                    st.switch_page("pages/3_vn.py")

if __name__ == "__main__":
    main()