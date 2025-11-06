import streamlit as st

st.set_page_config(page_title="Zoom Gallery", layout="wide")

# selection stored in session state so clicking does not use URL/query params and
# the page won't navigate to a new URL. Use st.session_state['selected'] to track.
if 'selected' not in st.session_state:
    st.session_state['selected'] = ""
selected = st.session_state['selected']

# sample items (emoji + title); replace with images or HTML if you have assets
items = [
    {"id": "item1", "label": "🎸", "title": "吉他"},
    {"id": "item2", "label": "🎹", "title": "钢琴"},
    {"id": "item3", "label": "🎻", "title": "小提琴"},
    {"id": "item4", "label": "🎷", "title": "萨克斯"},
    {"id": "item5", "label": "🥁", "title": "鼓"},
    {"id": "item6", "label": "🪕", "title": "班卓琴"},
    {"id": "item7", "label": "🪗", "title": "手风琴"},
    {"id": "item8", "label": "🎺", "title": "小号"}
]

# CSS for grid, items, selected and dim effect
st.markdown(
    """
    <style>
    .gallery { display: flex; flex-wrap: wrap; gap: 18px; justify-content: center; align-items: flex-start; padding: 20px; }
    .item-link { text-decoration: none; }
    .item {
        width: 180px;
        height: 220px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 6px 18px rgba(15,23,42,0.08);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: transform 0.45s cubic-bezier(.2,.9,.4,1), opacity 0.35s ease, box-shadow 0.35s ease;
        color: #111827;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans', 'Helvetica Neue', Arial;
    }
    .item .emoji { font-size: 64px; margin-bottom: 12px; }
    .item .title { font-size: 18px; color: #374151; }

    /* selected item: float to center and enlarge (smaller magnification) */
    .item.selected {
        opacity: 1 !important;
        transform: translate(-50%, -50%) scale(1.5) !important;
        position: fixed !important;
        left: 50% !important;
        top: 52% !important;
        z-index: 9999 !important;
        width: 360px !important;
        height: 440px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        border-radius: 12px !important;
        box-shadow: 0 30px 80px rgba(2,6,23,0.45) !important;
        background: linear-gradient(180deg,#ffffff,#f8fafc) !important;
    }

    /* show a close hint when selected */
    .close-hint { position: fixed; right: 24px; top: 18px; z-index: 10000; background: #111827; color: #fff; padding: 8px 12px; border-radius: 8px; opacity: 0.9; }

    /* responsive */
    @media (max-width: 700px) {
        .item { width: 140px; height: 180px; }
        .item.selected { width: 260px !important; height: 360px !important; transform: translate(-50%, -50%) scale(1.3) !important; }
    }
    /* style Streamlit buttons used as cards */
    .stButton>button {
        width: 100%;
        height: 220px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 6px 18px rgba(15,23,42,0.08);
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        font-size:16px;
        color: #111827;
    }
    .stButton>button:focus { outline: none; }
    .stButton>button .label { font-size: 64px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Build a grid with Streamlit columns and a small Select button for each item.
gallery_class = "gallery"
if selected:
    gallery_class += " dimmed"

# Render items in a responsive grid using columns (3 per row)
cols_per_row = 4
rows = [items[i:i+cols_per_row] for i in range(0, len(items), cols_per_row)]

for row in rows:
    cols = st.columns(len(row))
    for c, it in zip(cols, row):
        with c:
            # Render each item as a single Streamlit button styled to look like the card.
            label = f"{it['label']}\n\n{it['title']}"
            btn_key = f'card_{it["id"]}'
            clicked = st.button(label, key=btn_key)
            if clicked:
                st.session_state['selected'] = it['id']
                # rerun will happen automatically

# Close button when selected
if selected:
    if st.button('关闭（返回页面）'):
        st.session_state['selected'] = ""

# Visual overlay for the selected item: render a centered large card using raw HTML/CSS.
# The overlay uses pointer-events: none so clicks pass through to underlying buttons and
# users can still click other cards to switch selection. Closing is done with the Close button above.
if selected:
    sel = next((it for it in items if it['id'] == selected), None)
    if sel:
        overlay_html = f"""
        <div class="selected-overlay">
          <div class="emoji">{sel['label']}</div>
          <div class="title">{sel['title']}</div>
        </div>
        <style>
        /* dim all buttons (cards) when something is selected */
        .stButton>button {{ opacity: 0.35 !important; transition: opacity 0.2s ease; }}

        /* overlay visual (does not capture pointer events so underlying buttons still clickable) */
        .selected-overlay {{
            position: fixed !important;
            left: 50% !important;
            top: 52% !important;
            transform: translate(-50%, -50%) scale(1.5) !important;
            z-index: 9999 !important;
            width: 360px !important;
            height: 440px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 12px !important;
            box-shadow: 0 30px 80px rgba(2,6,23,0.45) !important;
            background: linear-gradient(180deg,#ffffff,#f8fafc) !important;
            pointer-events: none !important;
        }}
        .selected-overlay .emoji {{ font-size: 96px; margin-bottom: 14px; }}
        .selected-overlay .title {{ font-size: 20px; color:#374151; }}
        </style>
        """
        st.markdown(overlay_html, unsafe_allow_html=True)

# a short explanation and usage tip
st.markdown("""
点击任意一个物品会把它放大到页面中心，其他物品颜色会变淡。\n
提示：
- 要关闭放大视图，点击右上角的 "关闭（返回页面）" 按钮，或点击浏览器地址栏的刷新按钮。\n
你也可以把 `items` 换成图片：将 `<div class="emoji">{...}</div>` 换成 `<img src="/path/to/img.png" style="max-width:100%;height:auto;border-radius:8px">` 并确保图片路径可访问。
""")
