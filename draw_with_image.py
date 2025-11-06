import streamlit as st

st.set_page_config(page_title="画图板（左图右画）", layout="wide")

st.title("参考图片 + 简易画图板")

left, right = st.columns([1, 1])

with left:
    st.subheader("参考图片（可上传）")
    uploaded = st.file_uploader("上传图片（PNG / JPG）", type=["png", "jpg", "jpeg"])
    if uploaded:
        st.image(uploaded, use_column_width=True)
    else:
        st.info("尚未上传参考图片，您可以在此上传一张图片作为参考。")

with right:
    st.subheader("画图区（鼠标绘制）")
    st.markdown("选择画笔颜色和大小，左键绘制，清除可重来。")

    canvas_html = '''
    <div style="display:flex; flex-direction:column; gap:8px;">
      <div style="display:flex; gap:8px; align-items:center;">
        <label>颜色：</label>
        <input type="color" id="colorPicker" value="#ff0000" />
        <label>大小：</label>
        <input id="brushSize" type="range" min="1" max="60" value="6" />
        <button id="clearBtn">清除</button>
        <button id="downloadBtn">下载PNG</button>
      </div>
      <canvas id="drawCanvas" width="800" height="600" style="border:1px solid #ddd; touch-action: none;"></canvas>
    </div>

    <script>
    (function(){
      const canvas = document.getElementById('drawCanvas');
      const ctx = canvas.getContext('2d');
      let drawing = false;
      let lastX = 0, lastY = 0;

      const colorPicker = document.getElementById('colorPicker');
      const brushSize = document.getElementById('brushSize');
      const clearBtn = document.getElementById('clearBtn');
      const downloadBtn = document.getElementById('downloadBtn');

      function getPos(e){
        const rect = canvas.getBoundingClientRect();
        if (e.touches) {
          return {x: e.touches[0].clientX - rect.left, y: e.touches[0].clientY - rect.top};
        }
        return {x: e.clientX - rect.left, y: e.clientY - rect.top};
      }

      function start(e){
        drawing = true;
        const p = getPos(e);
        lastX = p.x; lastY = p.y;
      }
      function stop(e){ drawing = false; }
      function draw(e){
        if (!drawing) return;
        e.preventDefault();
        const p = getPos(e);
        ctx.strokeStyle = colorPicker.value;
        ctx.lineWidth = parseInt(brushSize.value, 10);
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(p.x, p.y);
        ctx.stroke();
        lastX = p.x; lastY = p.y;
      }

      canvas.addEventListener('mousedown', start);
      canvas.addEventListener('touchstart', start);
      window.addEventListener('mouseup', stop);
      canvas.addEventListener('touchend', stop);
      canvas.addEventListener('mousemove', draw);
      canvas.addEventListener('touchmove', draw, {passive:false});

      clearBtn.addEventListener('click', ()=>{
        ctx.clearRect(0,0,canvas.width, canvas.height);
      });

      downloadBtn.addEventListener('click', ()=>{
        const data = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = data;
        a.download = 'drawing.png';
        a.click();
      });
    })();
    </script>
    '''

    st.components.v1.html(canvas_html, height=680)
