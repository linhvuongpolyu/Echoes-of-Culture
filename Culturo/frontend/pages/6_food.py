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
logo_icon = str(logo_icon_path) if logo_icon_path.exists() else "🍜"

# Page configuration
st.set_page_config(
    page_title="Food - Culturo",
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
    </style>
    """, unsafe_allow_html=True)

# Initialize quiz data
def initialize_quiz():
    if 'food_quiz_answers' not in st.session_state:
        st.session_state.food_quiz_answers = [None, None, None]
    if 'food_quiz_submitted' not in st.session_state:
        st.session_state.food_quiz_submitted = False
    if 'food_quiz_score' not in st.session_state:
        st.session_state.food_quiz_score = 0

def reset_food_state():
    st.session_state.food_quiz_answers = [None, None, None]
    st.session_state.food_quiz_submitted = False
    st.session_state.food_quiz_score = 0
    if 'food_current_question' in st.session_state:
        st.session_state.food_current_question = 0

# Get current region from session state
def get_current_region():
    return st.session_state.get('current_region', 'Hong Kong')

# Get region-specific video file
def get_region_video(region):
    # Map region names to corresponding video filenames
    region_video_mapping = {
        'Hong Kong': 'hk_food.mp4',
        'China': 'cn_food.mp4', 
        'Vietnam': 'vn_food.mp4'
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
                "question": "What is the base of traditional Pho broth primarily made from?",
                "options": [
                    "Chicken and pork bones",
                    "Beef bones and spices",
                    "Seafood and lemongrass",
                    "Vegetables and tofu"
                ],
                "correct_answer": "Beef bones and spices"
            },
            {
                "question": "How long will the bones be simmered?",
                "options": [
                    "4 hours",
                    "12 hours",
                    "24 hours",
                    "48 hours"
                ],
                "correct_answer": "24 hours"
            },
            {
                "question": "What is the key ingredient that gives Pho broth its distinctive, warming aroma?",
                "options": [
                    "Lemongrass",
                    "Star anise",
                    "Chili peppers",
                    "Ginger"
                ],
                "correct_answer": "Star anise"
            }
        ],
        'China': [
            {
                "question": "When did Peking duck first appear in the menu?",
                "options": [
                    "1330s",
                    "1368s",
                    "1421s",
                    "1461s"
                ],
                "correct_answer": "1330s"
            },
            {
                "question": "The first Peking duck restaurant's name is",
                "options": [
                    "Yawang",
                    "Bianyifang",
                    "Quanjude",
                    "SDadong"
                ],
                "correct_answer": "Bianyifang"
            },
            {
                "question": "Which city is mentioned as the origin of the specific duck breed used for Peking Duck?",
                "options": [
                    "Beijing",
                    "Xian",
                    "Nanjing",
                    "Guangzhou"
                ],
                "correct_answer": "Nanjing"
            }
        ],
        'Hong Kong': [
            {
                "question": "What is the primary cooking method demonstrated in the video for making the buns?",
                "options": [
                    "Steaming",
                    "Frying",
                    "Baking",
                    "Boiling"
                ],
                "correct_answer": "Baking"
            },
            {
                "question": "What was added inside the buns?",
                "options": [
                    "Pineapple jam",
                    "Butter",
                    "Kaya coconut jam",
                    "Cheese"
                ],
                "correct_answer": "Butter"
            },
            {
                "question": "The name \"Pineapple Bun\" can be a bit confusing. According to the video, where does the name actually come from?",
                "options": [
                    "From the pineapple jam inside the bun.",
                    "From the tropical flavor added to the dough.",
                    "From the crisscross pattern on the topping that resembles a pineapple's skin.",
                    "It was originally created in Thailand, the \"Land of Pineapples\"."
                ],
                "correct_answer": "From the crisscross pattern on the topping that resembles a pineapple's skin."
            }
        ]
    }
    
    return quiz_data.get(region, quiz_data['Hong Kong'])  # Default to Hong Kong if region not found

# Get encouragement message based on score
def get_encouragement_message(score, region):
    if score == 0:
        messages = [
            f"Don't worry! Learning about {region}'s food culture is a journey. Every expert was once a beginner!",
            f"Not to worry! Exploring {region}'s cuisine is an adventure. Try again and you'll do better!",
            f"Keep your chin up! {region}'s food culture is rich and diverse. Give it another try!",
            f"Don't be discouraged! Learning about {region}'s culinary traditions takes time. You'll get it next time!"
        ]
        import random
        return random.choice(messages)
    elif score == 1:
        return f"Good start! You're beginning to understand {region}'s food culture. Keep learning!"
    elif score == 2:
        return f"Well done! You have a good knowledge of {region}'s culinary traditions!"
    else:  # score == 3
        return f"Excellent! You're a true expert on {region}'s food culture!"

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
    
    # Check if region changed and reset food state if needed
    if 'last_food_region' not in st.session_state:
        st.session_state.last_food_region = current_region
    elif st.session_state.last_food_region != current_region:
        reset_food_state()
        st.session_state.last_food_region = current_region
    
    # Initialize quiz state
    initialize_quiz()
    
    # Get current stars for food activity
    current_stars = star_manager.get_stars(current_region).get('Food', 0)
    
    # Header: Back button, title, and stars in the same row
    header_left, header_middle, header_right = st.columns([0.1, 0.75, 0.15])
    with header_left:
        back_clicked = st.button("←\nBack", key="back_btn_food", width='stretch')
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
            <div style="display: flex; align-items: center; gap: 12px;">
                <img src="{flag_url}" width="50" height="33" style="border-radius: 3px;" />
                <div style="display: flex; flex-direction: column;">
                    <h2 style="margin: 0; padding: 0; color: {region_color}; font-size: 1.6rem; font-weight: 600; line-height: 1;">Food</h2>
                    <p style="margin: 0; padding: 0; color: #666; font-size: 0.9rem; line-height: 1;">Taste the World, One Bite at a Time!</p>
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
        reset_food_state()  # Reset food state when switching regions
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
    if 'food_current_question' not in st.session_state:
        st.session_state.food_current_question = 0
    
    current_q_index = st.session_state.food_current_question
    
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
        if st.session_state.food_quiz_submitted:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Try Again", width="stretch"):
                st.session_state.food_quiz_answers = [None, None, None]
                st.session_state.food_quiz_submitted = False
                st.session_state.food_quiz_score = 0
                st.session_state.food_current_question = 0
                st.rerun()
    
    with quiz_col:
        # Display current question
        if not st.session_state.food_quiz_submitted:
            q = quiz_data[current_q_index]
            
            # Box 1: Header with Quiz Time and question number
            st.markdown(f"""
            <div style="background: white; padding: 0.5rem 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 1.2rem;">🍜</span>
                    <span style="font-weight: 600; font-size: 1rem;">Food Quiz!</span>
                    <span style="margin-left: auto; color: #666; font-size: 0.85rem;">Question {current_q_index + 1} of {len(quiz_data)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Box 2: Question and answer options in a simple white container
            with st.container(border=True):
                st.markdown(f"**{current_q_index + 1}. {q['question']}**")
                
                # Get current answer
                current_answer = st.session_state.food_quiz_answers[current_q_index]
                
                # Radio buttons for options
                user_answer = st.radio(
                    "Select your answer:",
                    q["options"],
                    key=f"food_q{current_q_index}_{current_region}_{st.session_state.nav_counter}",
                    index=None if current_answer is None else q["options"].index(current_answer),
                    label_visibility="collapsed"
                )
                
                # Store the answer
                if user_answer:
                    st.session_state.food_quiz_answers[current_q_index] = user_answer
            
            # Box 3: Navigation buttons - simple approach
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                if current_q_index > 0:
                    if st.button("← Back", width="stretch", key="back_q"):
                        st.session_state.food_current_question -= 1
                        st.rerun()
            
            with col2:
                if current_q_index < len(quiz_data) - 1:
                    if st.button("Next →", width="stretch", key="next_q"):
                        st.session_state.food_current_question += 1
                        st.rerun()
                else:
                    # Submit button on last question
                    if st.button("Submit Answer", type="primary", width="stretch", key="submit_quiz"):
                        # Check if all questions are answered
                        if None in st.session_state.food_quiz_answers:
                            st.error("Please answer all questions before submitting.")
                        else:
                            # Calculate score
                            score = 0
                            for i, quiz_q in enumerate(quiz_data):
                                if st.session_state.food_quiz_answers[i] == quiz_q["correct_answer"]:
                                    score += 1
                            
                            st.session_state.food_quiz_score = score
                            st.session_state.food_quiz_submitted = True
                            
                            # Save stars using star_manager
                            star_manager.update_stars(current_region, 'Food', score)
                            
                            st.rerun()
        
        # Display results if submitted
        else:
            # Different message and style based on score
            if st.session_state.food_quiz_score == 0:
                st.error(f"😔 Quiz completed. You earned {st.session_state.food_quiz_score} stars.")
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
                st.success(f"🎉 Completed! You earned {st.session_state.food_quiz_score} stars!")
                # Balloons effect for score > 0
                st.balloons()
            
            # Display star visualization
            stars_display = "⭐" * st.session_state.food_quiz_score + "☆" * (3 - st.session_state.food_quiz_score)
            st.markdown(f"<div style='text-align: center; font-size: 2rem; margin: 1rem 0;'>{stars_display}</div>", unsafe_allow_html=True)
            
            # Show encouragement message based on score
            encouragement_msg = get_encouragement_message(st.session_state.food_quiz_score, current_region)
            st.info(encouragement_msg)
            
            # Show correct answers with tighter spacing
            st.markdown("---")
            st.markdown("**Question Review:**")
            review_text = ""
            for i, q in enumerate(quiz_data):
                user_answer = st.session_state.food_quiz_answers[i]
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

        if st.button("← General", key="sidebar_general_food", width="stretch"):
            st.session_state.nav_counter += 1
            if 'current_region' in st.session_state:
                del st.session_state['current_region']
            st.switch_page("main_app.py")

        with st.expander("Discover", expanded=True):
            if st.button("China", key="nav_cn_from_food", width="stretch", disabled=(current_region == "China")):
                if current_region != "China":
                    st.session_state.current_region = "China"
                    st.switch_page("pages/2_cn.py")
            if st.button("Hong Kong", key="nav_hk_from_food", width="stretch", disabled=(current_region == "Hong Kong")):
                if current_region != "Hong Kong":
                    st.session_state.current_region = "Hong Kong"
                    st.switch_page("pages/1_hk.py")
            if st.button("Viet Nam", key="nav_vn_from_food", width="stretch", disabled=(current_region == "Vietnam")):
                if current_region != "Vietnam":
                    st.session_state.current_region = "Vietnam"
                    st.switch_page("pages/3_vn.py")


if __name__ == "__main__":
    main()