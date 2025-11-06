import streamlit as st

def show_book_style_intro():
    # 设置页面样式
    st.markdown("""
        <style>
        .book-container {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 15px;
            border-left: 8px solid #8B4513;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .book-title {
            font-family: 'Georgia', serif;
            color: #2c3e50;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .chapter-title {
            font-family: 'Georgia', serif;
            color: #8B4513;
            border-bottom: 2px solid #8B4513;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        .page-content {
            font-family: 'Georgia', serif;
            font-size: 1.1em;
            line-height: 1.8;
            text-align: justify;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # 书本容器开始
    st.markdown('<div class="book-container">', unsafe_allow_html=True)
    
    # 书本标题
    st.markdown('<h1 class="book-title">🌍 世界乐器探索之旅</h1>', unsafe_allow_html=True)
    
    # 使用分栏创建书本对开页效果
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="page-content">', unsafe_allow_html=True)
        st.markdown("### 📖 前言")
        st.markdown("""
        欢迎打开这本**交互式乐器百科全书**。在这里，你将踏上一段奇妙的音乐文化之旅，探索世界各地的传统乐器，感受不同文明的音乐魅力。
        
        从东方的古老弦乐到西方的古典管乐，每一件乐器都承载着一个民族的历史与情感。
        """)
        
        st.markdown("### 🎯 项目愿景")
        st.markdown("""
        我们致力于通过现代技术，让传统音乐文化以更生动、更互动的方式呈现。让每一个点击都成为一次音乐 discovery。
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="page-content">', unsafe_allow_html=True)
        st.markdown("### 🌟 特色功能")
        st.markdown("""
        - **🗺️ 交互地图** - 点击探索乐器发源地
        - **🎵 听觉体验** - 聆听真实乐器音色
        - **📚 文化背景** - 了解乐器历史故事
        - **🎨 视觉盛宴** - 精美插画与设计
        """)
        
        st.markdown("### 👥 适合人群")
        st.markdown("""
        - 音乐爱好者
        - 文化研究者
        - 教育工作者
        - 好奇的探索者
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 书本容器结束
    st.markdown('</div>', unsafe_allow_html=True)

# 在主函数中调用
def main():
    show_book_style_intro()
    # ... 其他地图代码