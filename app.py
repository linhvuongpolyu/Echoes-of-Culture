import streamlit as st
import pandas as pd

def create_book_style_intro():
    # 设置页面配置
    st.set_page_config(
        page_title="世界乐器探索书",
        page_icon="📚",
        layout="wide"
    )
    
    # 自定义CSS样式
    st.markdown("""
    <style>
    .book-page {
        background: linear-gradient(to right, #fefefe, #f9f9f9);
        padding: 40px;
        border-radius: 10px;
        border-left: 8px solid #8B4513;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.1);
        margin: 20px 0;
        font-family: 'Georgia', serif;
    }
    .chapter-title {
        color: #8B4513;
        border-bottom: 2px solid #8B4513;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .page-number {
        text-align: right;
        color: #666;
        font-style: italic;
        margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 创建书本封面
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   color: white; border-radius: 15px; margin: 20px 0;'>
            <h1 style='font-size: 3em; margin-bottom: 20px;'>🌍 世界乐器地图</h1>
            <h3 style='font-weight: 300;'>交互式音乐文化探索之旅</h3>
            <p style='margin-top: 30px; font-style: italic;'>—— 打开这本神奇的音乐之书 ——</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 使用tabs创建书本章节
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 第一章：前言", 
        "🎵 第二章：乐器世界", 
        "🗺️ 第三章：使用指南", 
        "🌟 第四章：关于"
    ])
    
    with tab1:
        st.markdown('<div class="book-page">', unsafe_allow_html=True)
        st.markdown('<h2 class="chapter-title">📖 欢迎来到音乐的世界</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **音乐是人类最古老的语言**，跨越时空，连接心灵。
            
            在这本交互式书籍中，你将踏上一段奇妙的旅程：
            
            - 🌏 探索世界各地的传统乐器
            - 🎶 聆听每种乐器的独特音色  
            - 📚 了解乐器背后的文化故事
            - 🎨 体验现代科技与古典艺术的融合
            """)
            
        with col2:
            # 可以添加图片或数据可视化
            st.image("https://via.placeholder.com/300x200?text=音乐世界地图", 
                    caption="世界音乐文化分布", use_column_width=True)
        
        st.markdown('<div class="page-number">- 1 -</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="book-page">', unsafe_allow_html=True)
        st.markdown('<h2 class="chapter-title">🎵 乐器家族</h2>', unsafe_allow_html=True)
        
        # 使用expander创建可展开的乐器介绍
        with st.expander("🎻 弦乐器家族", expanded=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image("https://via.placeholder.com/150x100?text=古筝", caption="中国古筝")
            with col2:
                st.markdown("""
                **古筝** - 中国传统弹拨乐器
                - 历史：2500多年
                - 音色：悠扬婉转
                - 名曲：《渔舟唱晚》
                """)
        
        with st.expander("🎺 管乐器家族"):
            st.markdown("管乐器通过气流振动发声...")
            
        with st.expander("🥁 打击乐器家族"):
            st.markdown("打击乐器通过敲击发声...")
            
        st.markdown('<div class="page-number">- 2 -</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="book-page">', unsafe_allow_html=True)
        st.markdown('<h2 class="chapter-title">🗺️ 如何使用这本交互书</h2>', unsafe_allow_html=True)
        
        steps = [
            {"step": "1", "title": "浏览地图", "desc": "查看世界地图上的乐器分布"},
            {"step": "2", "title": "点击标记", "desc": "选择感兴趣的乐器标记"},
            {"step": "3", "title": "阅读介绍", "desc": "了解乐器的历史和文化背景"},
            {"step": "4", "title": "聆听音色", "desc": "点击播放按钮欣赏乐器声音"}
        ]
        
        for step in steps:
            with st.container():
                st.markdown(f"**{step['step']}. {step['title']}**")
                st.markdown(f"*{step['desc']}*")
                st.markdown("---")
        
        st.markdown('<div class="page-number">- 3 -</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="book-page">', unsafe_allow_html=True)
        st.markdown('<h2 class="chapter-title">🌟 关于本项目</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        **技术栈**：
        - 🐍 Python - 后端逻辑
        - 🎯 Streamlit - 网页界面
        - 🗺️ Folium - 交互地图
        - 🔊 Pygame - 音频播放
        
        **项目特色**：
        - 完全使用Python开发
        - 响应式设计
        - 真实的乐器音色
        - 丰富的文化内容
        """)
        
        # 添加项目数据统计
        col1, col2, col3 = st.columns(3)
        col1.metric("乐器数量", "12", "3种新分类")
        col2.metric("音频样本", "24", "全部真实录制")
        col3.metric("文化区域", "8", "覆盖全球")
        
        st.markdown('<div class="page-number">- 4 -</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 在主应用中使用
def main():
    create_book_style_intro()
    
    # 添加过渡到地图部分
    st.markdown("---")
    st.markdown("## 🎯 准备好开始探索了吗？")
    
    if st.button("🚀 进入交互地图"):
        # 这里可以切换到地图界面
        st.success("正在加载交互地图...")
        # show_interactive_map()  # 你的地图函数

if __name__ == "__main__":
    main()