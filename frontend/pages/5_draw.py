import streamlit as st
import os
import base64

st.set_page_config(page_title="painting", layout="wide")

# 初始化星星数据
if 'stars' not in st.session_state:
    st.session_state.stars = {
        'Hong Kong': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
        'China': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
        'Vietnam': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
    }

# 获取当前地区（从session state）
def get_current_region():
    # 直接从session state获取当前地区
    return st.session_state.get('current_region', 'Hong Kong')

def get_image_base64(image_path):
    """Convert image to base64 encoding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

def get_region_image(region):
    """根据地区获取对应的参考图片"""
    base_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(base_dir, '..', '..', 'assets', 'images')
    
    # 定义各地区对应的图片文件名
    region_images = {
        'Hong Kong': 'hk_pic.png',
        'China': 'cn_pic.png', 
        'Vietnam': 'vn_pic.png'
    }
    
    image_file = region_images.get(region)
    if image_file:
        image_path = os.path.join(assets_dir, image_file)
        if os.path.exists(image_path):
            return image_path
    
    # 如果找不到特定图片，返回默认图片或None
    return None

def display_drawing_interface(region):
    """显示画图界面"""
    st.title(f"🎨 {region} - 动物绘画")
    
    # 获取地区对应的参考图片
    reference_image_path = get_region_image(region)
    
    left, right = st.columns([1, 1])

    with left:
        st.subheader("参考图片")
        
        if reference_image_path and os.path.exists(reference_image_path):
            st.image(reference_image_path, use_container_width=True, caption=f"{region}动物参考图片")
        else:
            st.warning(f"⚠️ {region}的参考图片未找到")
            st.markdown(
                f"""
                <div style='width:100%; height:420px; border:2px dashed #bbb; display:flex; align-items:center; justify-content:center; border-radius:8px; background:#fafafa;'>
                  <div style='text-align:center; color:#666;'>
                    <div style='font-size:20px; margin-bottom:10px;'>{region}参考图片</div>
                    <div style='font-size:12px;'>请将图片放入 assets/ 文件夹</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.subheader("绘画区域")
        st.markdown("选择画笔颜色和大小，用鼠标左键绘画，完成后点击确认获得3颗星⭐️⭐️⭐️")

        canvas_html = f'''
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <label style="font-weight:bold;">颜色:</label>
            <input type="color" id="colorPicker" value="#ff0000" />
            <label style="font-weight:bold;">大小:</label>
            <input id="brushSize" type="range" min="1" max="60" value="6" />
            <button id="clearBtn" style="padding:4px 8px; border:1px solid #ccc; border-radius:4px; background:#f5f5f5;">清除</button>
            <button id="undoBtn" style="padding:4px 8px; border:1px solid #ccc; border-radius:4px; background:#f5f5f5;">撤销</button>
            <button id="finalBtn" style="padding:4px 8px; border:1px solid #4CAF50; border-radius:4px; background:#4CAF50; color:white;">完成绘画</button>
            <button id="downloadBtn" style="padding:4px 8px; border:1px solid #2196F3; border-radius:4px; background:#2196F3; color:white;">下载图片</button>
          </div>
          <canvas id="drawCanvas" width="800" height="600" style="border:1px solid #ddd; touch-action: none; display:block; margin-top:8px; background:#fff"></canvas>
        </div>

        <script>
        (function(){{
          const canvas = document.getElementById('drawCanvas');
          const ctx = canvas.getContext('2d');
          let drawing = false;
          let lastX = 0, lastY = 0;
          let locked = false;

          const colorPicker = document.getElementById('colorPicker');
          const brushSize = document.getElementById('brushSize');
          const clearBtn = document.getElementById('clearBtn');
          const undoBtn = document.getElementById('undoBtn');
          const finalBtn = document.getElementById('finalBtn');
          const downloadBtn = document.getElementById('downloadBtn');

          // Undo history
          const HISTORY_LIMIT = 60;
          const history = [];
          function pushHistory(){{
            try{{
              if(history.length >= HISTORY_LIMIT) history.shift();
              const img = ctx.getImageData(0,0,canvas.width, canvas.height);
              history.push(img);
            }}catch(e){{
              console.warn('pushHistory failed', e);
            }}
          }}

          function setLocked(v){{
            locked = !!v;
            colorPicker.disabled = locked;
            brushSize.disabled = locked;
            clearBtn.disabled = locked;
            undoBtn.disabled = locked;
            finalBtn.disabled = locked;
            downloadBtn.disabled = false;
            
            if(locked){{
              finalBtn.textContent = '已完成';
              finalBtn.style.opacity = '0.6';
              finalBtn.style.background = '#888';
              
              // 发送完成信号到Streamlit
              const data = {{region: '{region}', action: 'drawing_completed'}};
              window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: JSON.stringify(data)
              }}, '*');
              
              const noteId = 'canvas-locked-note';
              if(!document.getElementById(noteId)){{
                const note = document.createElement('div');
                note.id = noteId;
                note.style.marginTop = '8px';
                note.style.padding = '12px';
                note.style.background = '#f0fff0';
                note.style.border = '2px solid #4CAF50';
                note.style.color = '#2E7D32';
                note.style.borderRadius = '8px';
                note.style.fontWeight = 'bold';
                note.style.textAlign = 'center';
                note.innerHTML = '🎉 绘画已完成！获得 <span style="color: #FFD700; font-size: 1.2em;">⭐️⭐️⭐️</span> 3颗星！';
                const wrapper = canvas.parentNode;
                if(wrapper && wrapper.parentNode) wrapper.parentNode.insertBefore(note, wrapper.nextSibling);
              }}
            }}
          }}

          function getPos(e){{
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            let clientX, clientY;
            if(e.touches && e.touches.length){{
              clientX = e.touches[0].clientX;
              clientY = e.touches[0].clientY;
            }}else{{
              clientX = e.clientX;
              clientY = e.clientY;
            }}
            const x = (clientX - rect.left) * scaleX;
            const y = (clientY - rect.top) * scaleY;
            return {{x:x, y:y, scaleX:scaleX, scaleY:scaleY}};
          }}

          function start(e){{
            if(locked) return;
            pushHistory();
            drawing = true;
            const p = getPos(e);
            lastX = p.x; lastY = p.y;
          }}
          function stop(e){{ drawing = false; }}
          function draw(e){{
            if(!drawing || locked) return;
            e.preventDefault();
            const p = getPos(e);
            ctx.strokeStyle = colorPicker.value;
            const scale = (p.scaleX + p.scaleY) / 2;
            ctx.lineWidth = Math.max(1, Math.round(parseInt(brushSize.value,10) * scale));
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(p.x, p.y);
            ctx.stroke();
            lastX = p.x; lastY = p.y;
          }}

          canvas.addEventListener('mousedown', start);
          canvas.addEventListener('touchstart', start);
          window.addEventListener('mouseup', stop);
          canvas.addEventListener('touchend', stop);
          canvas.addEventListener('mousemove', draw);
          canvas.addEventListener('touchmove', draw, {{passive:false}});

          clearBtn.addEventListener('click', ()=>{{
            if(locked) return;
            pushHistory();
            ctx.clearRect(0,0,canvas.width, canvas.height);
          }});

          undoBtn.addEventListener('click', ()=>{{
            if(locked) return;
            if(history.length === 0){{
              ctx.clearRect(0,0,canvas.width, canvas.height);
              return;
            }}
            const img = history.pop();
            try{{ ctx.putImageData(img, 0, 0); }}catch(e){{ console.warn('undo failed', e); ctx.clearRect(0,0,canvas.width, canvas.height); }}
          }});

          finalBtn.addEventListener('click', ()=>{{
            const ok = confirm('确认完成后将获得3颗星⭐️⭐️⭐️，是否确定？');
            if(ok) setLocked(true);
          }});

          downloadBtn.addEventListener('click', ()=>{{
            try{{
              const data = canvas.toDataURL('image/png');
              const a = document.createElement('a');
              a.href = data;
              a.download = 'drawing_{region}.png';
              a.click();
            }}catch(e){{ console.error('download failed', e); }}
          }});
        }})();
        </script>
        '''

        # 显示画布
        drawing_data = st.components.v1.html(canvas_html, height=680)
        
        # 处理绘画完成事件
        if drawing_data:
            try:
                import json
                data = json.loads(drawing_data)
                if data.get('action') == 'drawing_completed':
                    region = data.get('region')
                    if region in st.session_state.stars:
                        st.session_state.stars[region]['Draw Animals'] = 3
                        st.success(f"🎉 {region}动物绘画完成！获得3颗星！")
                        st.rerun()
            except:
                pass

# 主界面
def main():
    # 获取当前地区
    current_region = get_current_region()
    
    # 显示当前进度
    region_total = sum(st.session_state.stars[current_region].values())
    draw_stars = st.session_state.stars[current_region]['Draw Animals']
    
    # 在侧边栏显示进度信息
    st.sidebar.markdown(f"### 📊 {current_region}进度")
    st.sidebar.markdown(f"**总进度:** {region_total}/12")
    st.sidebar.markdown(f"**绘画任务:** {'⭐' * draw_stars}{'☆' * (3 - draw_stars)}")
    
    if draw_stars == 3:
        st.sidebar.success("✅ 绘画任务已完成！")
    
    # 返回按钮
    if st.sidebar.button("← 返回主地图", use_container_width=True):
        st.switch_page("main_app.py")
    
    # 返回原地区页面按钮
    if st.sidebar.button(f"← 返回{current_region}页面", use_container_width=True):
        if current_region == "Hong Kong":
            st.switch_page("pages/1_hk.py")
        elif current_region == "China":
            st.switch_page("pages/2_cn.py")
        elif current_region == "Vietnam":
            st.switch_page("pages/3_vn.py")
    
    # 测试按钮 - 手动完成绘画
    if st.sidebar.button("🎨 手动完成绘画（测试）", use_container_width=True):
        st.session_state.stars[current_region]['Draw Animals'] = 3
        st.sidebar.success("🎉 获得3颗星！")
        st.rerun()
    
    # 显示画图界面
    display_drawing_interface(current_region)

if __name__ == "__main__":
    main()