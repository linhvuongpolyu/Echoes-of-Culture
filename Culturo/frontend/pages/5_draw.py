import streamlit as st
import os
import base64
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.star_manager import star_manager

st.set_page_config(page_title="painting", layout="wide")

# Get current region (from session state)
def get_current_region():
    # Get current region directly from session state
    return st.session_state.get('current_region', 'Hong Kong')

def get_image_base64(image_path):
    """Convert image to base64 encoding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return None

def get_region_image(region):
    """Get corresponding reference image based on region"""
    base_dir = os.path.dirname(__file__)
    assets_dir = os.path.join(base_dir, '..', '..', 'assets', 'images')
    
    # Define image filenames corresponding to each region
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
    
    # If specific image not found, return default image or None
    return None

def display_drawing_interface(region):
    """Display drawing interface"""
    # Add back navigation buttons at the top
    col_back1, col_back2, col_back3 = st.columns([1, 1, 2])
    
    with col_back1:
        if st.button("⬅️ Back to Main Map", width='stretch'):
            # Increment navigation counter and clear region state
            st.session_state.nav_counter += 1
            if 'current_region' in st.session_state:
                del st.session_state['current_region']
            st.switch_page("main_app.py")
    
    with col_back2:
        if st.button(f"⬅️ Back to {region}", width='stretch'):
            # Increment navigation counter for fresh render
            st.session_state.nav_counter += 1
            if region == "Hong Kong":
                st.switch_page("pages/1_hk.py")
            elif region == "China":
                st.switch_page("pages/2_cn.py")
            elif region == "Vietnam":
                st.switch_page("pages/3_vn.py")
    
    st.markdown("---")
    st.title(f"🎨 {region} - Animal Drawing")
    
    # Initialize drawing completion state
    if f'drawing_completed_{region}' not in st.session_state:
        st.session_state[f'drawing_completed_{region}'] = False
    
    # Get region-specific reference image
    reference_image_path = get_region_image(region)
    
    left, right = st.columns([1, 1])

    with left:
        st.subheader("Reference Image")
        
        if reference_image_path and os.path.exists(reference_image_path):
            st.image(reference_image_path, width='stretch', caption=f"{region} Animal Reference Image")
        else:
            st.warning(f"⚠️ Reference image for {region} not found")
            st.markdown(
                f"""
                <div style='width:100%; height:420px; border:2px dashed #bbb; display:flex; align-items:center; justify-content:center; border-radius:8px; background:#fafafa;'>
                  <div style='text-align:center; color:#666;'>
                    <div style='font-size:20px; margin-bottom:10px;'>{region} Reference Image</div>
                    <div style='font-size:12px;'>Please place image in assets/ folder</div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with right:
        st.subheader("Drawing Area")
        st.markdown("Choose brush color and size, draw with left mouse button. When finished, click the **'Submit Drawing'** button below to earn 3 stars⭐️⭐️⭐️")

        canvas_html = f'''
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <label style="font-weight:bold;">Color:</label>
            <input type="color" id="colorPicker" value="#ff0000" />
            <label style="font-weight:bold;">Size:</label>
            <input id="brushSize" type="range" min="1" max="60" value="6" />
            <button id="clearBtn" style="padding:4px 8px; border:1px solid #ccc; border-radius:4px; background:#f5f5f5;">Clear</button>
            <button id="undoBtn" style="padding:4px 8px; border:1px solid #ccc; border-radius:4px; background:#f5f5f5;">Undo</button>
            <button id="downloadBtn" style="padding:4px 8px; border:1px solid #2196F3; border-radius:4px; background:#2196F3; color:white;">Download Image</button>
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
            pushHistory();
            drawing = true;
            const p = getPos(e);
            lastX = p.x; lastY = p.y;
          }}
          function stop(e){{ drawing = false; }}
          function draw(e){{
            if(!drawing) return;
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
            pushHistory();
            ctx.clearRect(0,0,canvas.width, canvas.height);
          }});

          undoBtn.addEventListener('click', ()=>{{
            if(history.length === 0){{
              ctx.clearRect(0,0,canvas.width, canvas.height);
              return;
            }}
            const img = history.pop();
            try{{ ctx.putImageData(img, 0, 0); }}catch(e){{ console.warn('undo failed', e); ctx.clearRect(0,0,canvas.width, canvas.height); }}
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

        # Display canvas (scrolling=False to prevent nesting issues)
        st.components.v1.html(canvas_html, height=680, scrolling=False)
        
        # Add Submit Drawing button below the canvas
        st.markdown("---")
        
        # Check if already completed
        if st.session_state[f'drawing_completed_{region}']:
            st.success("🎉 Drawing completed! You earned 3 stars! ⭐⭐⭐")
            if st.button("🔄 Reset Drawing", width='stretch'):
                st.session_state[f'drawing_completed_{region}'] = False
                star_manager.update_stars(region, 'Draw Animals', 0)
                st.rerun()
        else:
            if st.button("✅ Submit Drawing (Earn 3 Stars!)", type="primary", width='stretch'):
                # Mark as completed and award stars
                st.session_state[f'drawing_completed_{region}'] = True
                star_manager.update_stars(region, 'Draw Animals', 3)
                st.balloons()
                st.rerun()

# Main interface
def main():
    # Initialize navigation counter to force fresh renders
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0
    
    # Get current region
    current_region = get_current_region()
    
    # Display current progress - using star_manager
    region_stars = star_manager.get_stars(current_region)
    region_total = star_manager.get_total_stars(current_region)
    draw_stars = region_stars['Draw Animals']
    
    # Display progress info in sidebar
    st.sidebar.markdown(f"### 📊 {current_region} Progress")
    st.sidebar.markdown(f"**Total Progress:** {region_total}/12")
    st.sidebar.markdown(f"**Drawing Task:** {'⭐' * draw_stars}{'☆' * (3 - draw_stars)}")
    
    if draw_stars == 3:
        st.sidebar.success("✅ Drawing task completed!")
    
    # Return buttons
    if st.sidebar.button("← Return to Main Map", width='stretch'):
        # Increment navigation counter and clear region state
        st.session_state.nav_counter += 1
        if 'current_region' in st.session_state:
            del st.session_state['current_region']
        st.switch_page("main_app.py")
    
    # Return to region page button
    if st.sidebar.button(f"← Return to {current_region} Page", use_container_width=True):
        # Increment navigation counter for fresh render
        st.session_state.nav_counter += 1
        if current_region == "Hong Kong":
            st.switch_page("pages/1_hk.py")
        elif current_region == "China":
            st.switch_page("pages/2_cn.py")
        elif current_region == "Vietnam":
            st.switch_page("pages/3_vn.py")
    
    
    # Display drawing interface
    display_drawing_interface(current_region)

if __name__ == "__main__":
    main()