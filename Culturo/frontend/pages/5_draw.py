import streamlit as st
import os
import base64
import sys
from pathlib import Path

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))
from utils.star_manager import star_manager

st.set_page_config(page_title="painting", layout="wide")

# CSS styles matching Vietnam page
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
    </style>
    """, unsafe_allow_html=True)

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
    # Get current stars for drawing activity
    current_stars = star_manager.get_stars(region).get('Draw Animals', 0)
    
    # Header: Back button, title, and stars in the same row
    header_left, header_middle, header_right = st.columns([0.1, 0.75, 0.15])
    with header_left:
        back_clicked = st.button("←\nBack", key="back_btn", width='stretch')
    with header_middle:
        # Get flag URL based on region
        flag_urls = {
            'Vietnam': 'https://flagcdn.com/w80/vn.png',
            'China': 'https://flagcdn.com/w80/cn.png',
            'Hong Kong': 'https://flagcdn.com/w80/hk.png'
        }
        flag_url = flag_urls.get(region, '')
        
        # Get region color
        region_colors = {
          'Vietnam': '#1C8575',  # VN teal-green
          'China': '#DE5862',    # China warm red
          'Hong Kong': '#DA901E' # HK amber
        }
        region_color = region_colors.get(region, '#1C8575')
        
        st.markdown(f"""
            <div class="vn-header">
                <img src="{flag_url}" width="50" height="33" style="border-radius: 3px;" />
                <div style="display: flex; flex-direction: column;">
                    <h2 style="margin: 0; padding: 0; color: {region_color}; font-size: 1.6rem; font-weight: 600; line-height: 1;">Drawing</h2>
                    <p style="margin: 0; padding: 0; color: #666; font-size: 0.9rem; line-height: 1;">Draw each country's animals your way</p>
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
        if region == "Hong Kong":
            st.switch_page("pages/1_hk.py")
        elif region == "China":
            st.switch_page("pages/2_cn.py")
        elif region == "Vietnam":
            st.switch_page("pages/3_vn.py")
    
    # Initialize drawing completion state
    if f'drawing_completed_{region}' not in st.session_state:
        st.session_state[f'drawing_completed_{region}'] = False
    
    # Show balloons if just completed
    if st.session_state.get(f'show_balloons_{region}', False):
        st.balloons()
        st.session_state[f'show_balloons_{region}'] = False
    
    # Get region-specific reference image
    reference_image_path = get_region_image(region)
    
    # New layout: Left sidebar + Right canvas
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        # Reference section with box container
        st.markdown("""
        <div style="background: white; padding: 6px 14px; border-radius: 10px; border: 1px solid #E0E0E0; margin-bottom: 0px;">
            <h4 style="margin: 0; display: flex; align-items: center; gap: 6px; font-size: 0.95rem; font-weight: 600;">
                <span style="font-size: 16px;">📸</span> Reference
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        if reference_image_path and os.path.exists(reference_image_path):
            # Move image inside the visual container using custom HTML
            img_base64 = get_image_base64(reference_image_path)
            if img_base64:
                st.markdown(f"""
                <div style="background: white; padding: 0 14px 6px 14px; border-radius: 10px; border: 1px solid #E0E0E0; margin-top: -10px; margin-bottom: 8px;">
                    <img src="data:image/png;base64,{img_base64}" style="width: 100%; max-height: 250px; object-fit: contain; border-radius: 8px;">
                </div>
                """, unsafe_allow_html=True)
            else:
                st.image(reference_image_path, width='stretch')
        else:
            st.markdown(
                f"""
                <div style='background: white; padding: 6px 14px; border-radius: 10px; border: 1px solid #E0E0E0; margin-top: -10px; margin-bottom: 8px;'>
                    <div style='width:100%; height:150px; border:2px dashed #bbb; display:flex; align-items:center; justify-content:center; border-radius:8px; background:#fafafa;'>
                        <div style='text-align:center; color:#666;'>
                            <div style='font-size:16px; margin-bottom:5px;'>{region} Reference</div>
                            <div style='font-size:11px;'>Image not found</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        # Submit button below reference
        if st.session_state[f'drawing_completed_{region}']:
            st.success("🎉 Completed! You earned 3 stars!")
            if st.button("🔄 Reset Drawing", width='stretch', key="reset_left"):
                st.session_state[f'drawing_completed_{region}'] = False
                star_manager.update_stars(region, 'Draw Animals', 0)
                st.rerun()
        else:
            st.markdown("""
            <style>
            div[data-testid="stButton"] button[kind="primary"] {
                background-color: #004DA0 !important;
                border: none !important;
            }
            div[data-testid="stButton"] button[kind="primary"]:hover {
                background-color: #003D80 !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("🖌️ Submit Drawing", type="primary", width='stretch', key="submit_left"):
                # Mark as completed and award stars
                st.session_state[f'drawing_completed_{region}'] = True
                st.session_state[f'show_balloons_{region}'] = True
                star_manager.update_stars(region, 'Draw Animals', 3)
                st.rerun()
    
    with right_col:
        # Canvas section - single unified box
        st.markdown("""
        <div style="background: white; padding: 6px 14px 0 14px; border-radius: 10px; border: 1px solid #E0E0E0;">
            <h4 style="margin: 0 0 6px 0; display: flex; align-items: center; gap: 6px; font-size: 0.95rem; font-weight: 600;">
                <span style="font-size: 16px;">🎨</span> Your Masterpiece
            </h4>
        """, unsafe_allow_html=True)
        
        canvas_html = f'''
        <div style="display:flex; flex-direction:column; gap:0px; margin-bottom: 6px;">
          <div style="display:flex; gap:10px; margin-bottom:10px; align-items:center;">
            <label style="font-weight:600; font-size:0.9rem;">Color:</label>
            <input type="color" id="colorPicker" value="#4F48E8" style="width:50px; height:35px; border:1px solid #E0E0E0; border-radius:5px; cursor:pointer;">
            <label style="font-weight:600; font-size:0.9rem;">Brush Size:</label>
            <input id="brushSize" type="range" min="1" max="20" value="5" style="flex:1;">
            <button id="clearBtn" style="padding:6px 12px; border:1px solid #E0E0E0; border-radius:5px; background:#fff; cursor:pointer; font-size:0.85rem;">🗑️ Clear</button>
            <button id="undoBtn" style="padding:6px 12px; border:1px solid #E0E0E0; border-radius:5px; background:#fff; cursor:pointer; font-size:0.85rem;">↩️ Undo</button>
            <button id="downloadBtn" style="padding:6px 12px; border:1px solid #4F48E8; border-radius:5px; background:#4F48E8; color:#fff; cursor:pointer; font-size:0.85rem;">💾 Save</button>
          </div>
          <canvas id="drawCanvas" width="800" height="430" style="border:1px solid #E0E0E0; touch-action: none; display:block; background:#fff; border-radius:8px; cursor:crosshair;"></canvas>
        </div>

        <script>
        (function(){{
          const canvas = document.getElementById('drawCanvas');
          const ctx = canvas.getContext('2d');
          const colorPicker = document.getElementById('colorPicker');
          const brushSize = document.getElementById('brushSize');
          const clearBtn = document.getElementById('clearBtn');
          const undoBtn = document.getElementById('undoBtn');
          const downloadBtn = document.getElementById('downloadBtn');
          
          const storageKey = 'drawing_canvas_{region}';
          
          let drawing = false;
          let lastX = 0, lastY = 0;
          let currentColor = colorPicker.value;
          let isEraser = false;

          // Undo history
          const HISTORY_LIMIT = 30;
          const history = [];
          
          // Load saved drawing on init (using sessionStorage instead of localStorage)
          function loadDrawing(){{
            try{{
              const savedData = sessionStorage.getItem(storageKey);
              if(savedData){{
                const img = new Image();
                img.onload = function(){{
                  ctx.drawImage(img, 0, 0);
                }};
                img.src = savedData;
              }}
            }}catch(e){{
              console.warn('Failed to load drawing', e);
            }}
          }}
          
          // Save drawing to sessionStorage (will be cleared when browser/tab closes)
          function saveDrawing(){{
            try{{
              const dataURL = canvas.toDataURL('image/png');
              sessionStorage.setItem(storageKey, dataURL);
            }}catch(e){{
              console.warn('Failed to save drawing', e);
            }}
          }}
          
          function pushHistory(){{
            try{{
              if(history.length >= HISTORY_LIMIT) history.shift();
              const img = ctx.getImageData(0,0,canvas.width, canvas.height);
              history.push(img);
            }}catch(e){{
              console.warn('pushHistory failed', e);
            }}
          }}

          // Update color when picker changes
          colorPicker.addEventListener('change', (e) => {{
            currentColor = e.target.value;
            isEraser = false;
          }});

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
          
          function stop(e){{ 
            drawing = false;
            saveDrawing(); // Auto-save after each drawing action
          }}
          
          function draw(e){{
            if(!drawing) return;
            e.preventDefault();
            const p = getPos(e);
            
            if(isEraser){{
              ctx.globalCompositeOperation = 'destination-out';
              ctx.strokeStyle = 'rgba(0,0,0,1)';
            }} else {{
              ctx.globalCompositeOperation = 'source-over';
              ctx.strokeStyle = currentColor;
            }}
            
            const size = parseInt(brushSize.value, 10);
            ctx.lineWidth = size;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.beginPath();
            ctx.moveTo(lastX, lastY);
            ctx.lineTo(p.x, p.y);
            ctx.stroke();
            lastX = p.x; lastY = p.y;
          }}

          // Clear button
          clearBtn.addEventListener('click', () => {{
            pushHistory();
            ctx.clearRect(0,0,canvas.width, canvas.height);
            saveDrawing();
          }});

          // Undo button
          undoBtn.addEventListener('click', () => {{
            if(history.length === 0){{
              ctx.clearRect(0,0,canvas.width, canvas.height);
              saveDrawing();
              return;
            }}
            const img = history.pop();
            try{{ 
              ctx.putImageData(img, 0, 0);
              saveDrawing();
            }}catch(e){{ 
              console.warn('undo failed', e); 
              ctx.clearRect(0,0,canvas.width, canvas.height);
              saveDrawing();
            }}
          }});
          
          // Download button
          downloadBtn.addEventListener('click', () => {{
            try{{
              const dataURL = canvas.toDataURL('image/png');
              const a = document.createElement('a');
              a.href = dataURL;
              a.download = 'my_drawing_{region}.png';
              a.click();
            }}catch(e){{
              console.error('Download failed', e);
            }}
          }});

          canvas.addEventListener('mousedown', start);
          canvas.addEventListener('touchstart', start);
          window.addEventListener('mouseup', stop);
          canvas.addEventListener('touchend', stop);
          canvas.addEventListener('mousemove', draw);
          canvas.addEventListener('touchmove', draw, {{passive:false}});
          
          // Load saved drawing when page loads
          loadDrawing();
        }})();
        </script>
        '''
        
        st.components.v1.html(canvas_html, height=400, scrolling=False)
        
        # Close the single unified box
        st.markdown('</div>', unsafe_allow_html=True)

# Main interface
def main():
    # Initialize navigation counter to force fresh renders
    if 'nav_counter' not in st.session_state:
        st.session_state.nav_counter = 0
    
    # Get current region
    current_region = get_current_region()
    
    # Sidebar unified with country pages
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

      if st.button("← General", key="sidebar_general_draw", width="stretch"):
        st.session_state.nav_counter += 1
        if 'current_region' in st.session_state:
          del st.session_state['current_region']
        st.switch_page("main_app.py")

      with st.expander("Discover", expanded=True):
        # Disable current region button to indicate context
        if st.button("China", key="nav_cn_from_draw", width="stretch", disabled=(current_region == "China")):
          if current_region != "China":
            st.session_state.current_region = "China"; st.switch_page("pages/2_cn.py")
        if st.button("Hong Kong", key="nav_hk_from_draw", width="stretch", disabled=(current_region == "Hong Kong")):
          if current_region != "Hong Kong":
            st.session_state.current_region = "Hong Kong"; st.switch_page("pages/1_hk.py")
        if st.button("Viet Nam", key="nav_vn_from_draw", width="stretch", disabled=(current_region == "Vietnam")):
          if current_region != "Vietnam":
            st.session_state.current_region = "Vietnam"; st.switch_page("pages/3_vn.py")

      # Progress block hidden for cleaner interface
      # region_stars = star_manager.get_stars(current_region)
      # region_total = star_manager.get_total_stars(current_region)
      # draw_stars = region_stars['Draw Animals']
      # st.markdown(f"### 📊 {current_region} Progress")
      # st.markdown(f"**Total Progress:** {region_total}/12")
      # st.markdown(f"**Drawing Task:** {'⭐' * draw_stars}{'☆' * (3 - draw_stars)}")
      # if draw_stars == 3:
      #   st.success("✅ Drawing task completed!")
    
    
    # Display drawing interface
    display_drawing_interface(current_region)

if __name__ == "__main__":
    main()