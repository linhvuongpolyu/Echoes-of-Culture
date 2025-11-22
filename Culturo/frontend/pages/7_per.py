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
    page_title="Performance Culture Quiz",
    page_icon="🎭",
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

# Get current region from session state
def get_current_region():
    current_region = st.session_state.get('current_region', 'Hong Kong')

    # Check if the region has changed
    if 'last_region' in st.session_state and st.session_state['last_region'] != current_region:
        # Reset performance-related session state variables
        st.session_state.performance_quiz_answers = [None, None, None]
        st.session_state.performance_quiz_submitted = False
        st.session_state.performance_quiz_score = 0

    # Update the last_region to the current region
    st.session_state['last_region'] = current_region

    return current_region

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
                "question": "What is the historical origin of water puppetry in Vietnam, and which region is it most associated with?",
                "options": [
                    "It originated in the imperial city of Hue in central Vietnam during the 15th century.",
                    "It began in the Mekong Delta in southern Vietnam as a form of entertainment for fishermen.",
                    "It originated in the villages of the Red River Delta in northern Vietnam around the 11th century.",
                    "It was imported from China during the period of Chinese domination."
                ],
                "correct_answer": "It originated in the villages of the Red River Delta in northern Vietnam around the 11th century."
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
                    "The heroes from the classic novel Water Margin",
                    "A celebration of the harvest season"
                ],
                "correct_answer": "The heroes from the classic novel Water Margin"
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
    
    # Set page title based on region
    st.title(f"🎭 {current_region} Performance Culture")
    st.markdown(f"### Explore the unique performance culture of {current_region} and test your knowledge!")
    
    # Initialize quiz state
    initialize_quiz()
    
    # Display region header
    st.markdown(f'<div class="region-header">', unsafe_allow_html=True)
    st.markdown(f"### Currently exploring: {current_region}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display video
    st.markdown("---")
    st.markdown(f"### 🎬 {current_region} Performance Culture Video")
    
    # Get the correct video for the current region
    video_path = get_region_video(current_region)
    
    if video_path and os.path.exists(video_path):
        try:
            st.video(video_path)
        except Exception as e:
            st.error(f"Unable to play video: {e}")
            # Fallback to online video
            st.video('https://sample-videos
    else:
        st.warning("Video not available for the selected region.")
    
    # Get region-specific quiz questions
    quiz_data = get_region_quiz_data(current_region)
    
    # Use table to wrap questions and submit button for single submission
    with st.form(key='quiz_form'):
        # Display questions - Removed the container borders
        for i, q in enumerate(quiz_data):
            # Removed the container with background color
            st.markdown(f'<div class="question">Question {i+1}: {q["question"]}</div>', unsafe_allow_html=True)
            
            # Get current answer or default to None
            current_answer = st.session_state.per_quiz_answers[i]

            # Ensure current_answer is valid before finding index
            if current_answer not in q["options"]:
                current_answer = None

            # Create radio buttons for options
            user_answer = st.radio(
                f"Select your answer for question {i+1}:",
                q["options"],
                key=f"per_q{i}_{current_region}",
                index=None if current_answer is None else q["options"].index(current_answer)
            )

            # Store the answer
            if user_answer:
                st.session_state.per_quiz_answers[i] = user_answer

            # Add some space between questions
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit button inside the form
        submitted = st.form_submit_button("Submit Answer", type="primary", use_container_width=True)
    
    # Handle form submission
    if submitted:
        # Check if all questions are answered
        if None in st.session_state.per_quiz_answers:
            st.error("Please answer all questions before submitting.")
        else:
            # Calculate score
            score = 0
            for i, q in enumerate(quiz_data):
                if st.session_state.per_quiz_answers[i] == q["correct_answer"]:
                    score += 1
            
            st.session_state.per_quiz_score = score
            st.session_state.per_quiz_submitted = True
            
            # Save stars using star_manager
            star_manager.update_stars(current_region, 'Performance', score)
            
            st.rerun()
    
    # Display results if submitted
    if st.session_state.per_quiz_submitted:
        st.markdown("---")
        st.markdown("### 📊 Quiz Results")
        
        # Show score and stars earned
        st.markdown(f'<div class="star-result">', unsafe_allow_html=True)
        st.markdown(f"### You earned {st.session_state.per_quiz_score} out of 3 stars! ⭐")
        
        # Display star visualization
        stars_display = "⭐" * st.session_state.per_quiz_score + "☆" * (3 - st.session_state.per_quiz_score)
        st.markdown(f"### {stars_display}")
        
        # Show encouragement message based on score
        encouragement_msg = get_encouragement_message(st.session_state.per_quiz_score, current_region)
        st.markdown(f'<div class="encouragement">{encouragement_msg}</div>', unsafe_allow_html=True)
        
        # Show correct answers with user answers
        st.markdown("### Question Review:")
        for i, q in enumerate(quiz_data):
            user_answer = st.session_state.per_quiz_answers[i]
            correct_answer = q["correct_answer"]
            is_correct = user_answer == correct_answer
            
            if is_correct:
                st.markdown(f"✅ **Question {i+1}:** Your answer '{user_answer}' is correct!")
            else:
                # 安全地处理用户答案和正确答案
                user_answer_display = user_answer if user_answer else "No answer"
                st.markdown(f"❌ **Question {i+1}:** Your answer '{user_answer_display}' is incorrect.")
                st.markdown(f"<span class='correct-answer'>Correct answer: {correct_answer}</span>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Reset or navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Retry Quiz", use_container_width=True):
                st.session_state.per_quiz_answers = [None, None, None]
                st.session_state.per_quiz_submitted = False
                st.session_state.per_quiz_score = 0
                st.rerun()
        
        with col2:
            if st.button("Back to Main", width='stretch'):
                # Increment navigation counter and clear region state
                st.session_state.nav_counter += 1
                if 'current_region' in st.session_state:
                    del st.session_state['current_region']
                st.switch_page("main_app.py")
        
        with col3:
            if st.button(f"Back to {current_region}", width='stretch'):
                # Increment navigation counter for fresh render
                st.session_state.nav_counter += 1
                # Determine which region page to go back to
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