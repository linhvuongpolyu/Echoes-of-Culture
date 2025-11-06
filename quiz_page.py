import streamlit as st

st.set_page_config(page_title="问答页面", layout="centered")

# Sample question set. Each question has text, a list of 4 options, and the index (0-based) of the correct answer.
QUESTIONS = [
    {"q": "下列哪个是 Python 的数据类型？", "options": ["div", "span", "list", "css"], "answer": 2},
    {"q": "世界上最大的大陆是？", "options": ["非洲", "欧亚大陆", "南极洲", "澳大利亚"], "answer": 1},
    {"q": "HTML 用于什么？", "options": ["样式表", "网页结构", "后端服务", "数据库管理"], "answer": 1},
]

if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'selected' not in st.session_state:
    st.session_state.selected = None
if 'answered' not in st.session_state:
    st.session_state.answered = False

q_idx = st.session_state.q_idx
question = QUESTIONS[q_idx]

st.title("简易问答页面")
st.markdown(f"**题目 {q_idx+1} / {len(QUESTIONS)}**")
st.write(question['q'])

# Unified styles for option boxes and feedback
st.markdown(
    """
    <style>
    .option-box { padding:10px; border-radius:8px; border:1px solid #e6e6e6; background:#fff; width:100%; }
    .option-box button { height:112px; width:100%; border-radius:8px; font-size:16px; padding:8px 12px; text-align:left; }
    .option-tile { padding:14px; min-height:112px; border-radius:8px; margin-bottom:8px; display:flex; align-items:center; }
    .option-tile.selected { background:#f0f8ff; border:1px solid #9ec5ff; }
    .option-tile.default { background:#ffffff; border:1px solid #e6e6e6; }
    .feedback-box { padding:12px; border-radius:8px; margin-top:8px; font-weight:600; }
    .feedback-box.correct { background:#e6ffed; border:1px solid #b7f0c4; color:#0a6; }
    .feedback-box.wrong { background:#ffecec; border:1px solid #ffb8b8; color:#a00; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Build clickable large option boxes using links that set a query param (?sel=)
options = question['options']

# Render options as native Streamlit buttons (styled to be larger boxes).
# We inject a small CSS snippet to enlarge buttons. When not answered, show clickable buttons;
# when answered, show static colored boxes with feedback.
user_sel = st.session_state.selected
if not st.session_state.answered:
    # Render a single boxed area containing the option buttons (no duplicate displays).
    st.markdown("<div class='option-box'>", unsafe_allow_html=True)
    for i, opt in enumerate(options):
        # option button — clicking sets the selected index
        clicked = st.button(opt, key=f"opt_btn_{q_idx}_{i}")
        if clicked:
            st.session_state.selected = i
            user_sel = i
        # show a small spacer
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # show current selection inside the box area for clarity
    if user_sel is not None:
        st.info(f"当前选择：{options[user_sel]}")

    # Confirm / Next buttons
    col1, col2 = st.columns([1,1])
    with col1:
        confirm = st.button("确认")
    with col2:
        nxt = st.button("下一题")

    if confirm:
        if st.session_state.selected is not None:
            st.session_state.answered = True
# When answered, show feedback under the Confirm/Next buttons (do not replace the option boxes)
if st.session_state.answered:
    user_idx = st.session_state.selected
    correct_idx = question['answer']
    # feedback block
    if user_idx == correct_idx:
        st.markdown("<div class='feedback-box correct'>回答正确！</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='feedback-box wrong'>回答错误，正确答案：<strong>{options[correct_idx]}</strong></div>", unsafe_allow_html=True)
# Next question logic
if nxt:
    st.session_state.q_idx = (st.session_state.q_idx + 1) % len(QUESTIONS)
    st.session_state.selected = None
    st.session_state.answered = False


# Small instructions
st.markdown("---")
st.caption('说明：选择一个选项后点击“确认”查看正确/错误，点击“下一题”进入下一题。')
