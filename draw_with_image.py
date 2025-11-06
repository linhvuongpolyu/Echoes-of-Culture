import streamlit as st

st.set_page_config(page_title="画图板（左图右画）", layout="wide")

st.title("参考图片 + 简易画图板")

left, right = st.columns([1, 1])

with left:
    st.subheader("参考图片（示意框）")
    # Removed uploader per request — show a placeholder box instead.
    st.markdown(
        """
        <div style='width:100%; height:420px; border:2px dashed #bbb; display:flex; align-items:center; justify-content:center; border-radius:8px; background:#fafafa;'>
          <div style='text-align:center; color:#666;'>
            <div style='font-size:20px; margin-bottom:10px;'>参考图片位置</div>
            <div style='font-size:12px;'>请将参考图片放入项目的 assets/ 文件夹以在界面中使用（可选）</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
        <button id="undoBtn">撤销</button>
        <button id="finalBtn">确认完成</button>
        <button id="downloadBtn">下载PNG</button>
      </div>
      <canvas id="drawCanvas" width="800" height="600" style="border:1px solid #ddd; touch-action: none; display:block; margin-top:8px; background:#fff"></canvas>
    </div>

    <script>
    (function(){
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

      // Undo history (store ImageData snapshots)
      const HISTORY_LIMIT = 60;
      const history = [];
      function pushHistory(){
        try{
          if(history.length >= HISTORY_LIMIT) history.shift();
          // store a snapshot of the current canvas pixels
          const img = ctx.getImageData(0,0,canvas.width, canvas.height);
          history.push(img);
        }catch(e){
          console.warn('pushHistory failed', e);
        }
      }

      function setLocked(v){
        locked = !!v;
        // disable controls when locked
        colorPicker.disabled = locked;
        brushSize.disabled = locked;
        clearBtn.disabled = locked;
        undoBtn.disabled = locked;
        finalBtn.disabled = locked;
        downloadBtn.disabled = false; // allow download even after lock
        // visual cue
        if(locked){
          finalBtn.textContent = '已确认';
          finalBtn.style.opacity = '0.6';
          // insert a small notice if not exists
          const noteId = 'canvas-locked-note';
          if(!document.getElementById(noteId)){
            const note = document.createElement('div');
            note.id = noteId;
            note.style.marginTop = '8px';
            note.style.padding = '8px';
            note.style.background = '#fff6f6';
            note.style.border = '1px solid #ffd6d6';
            note.style.color = '#a00';
            note.style.borderRadius = '6px';
            note.textContent = '已确认：画布已锁定，无法再进行绘制或修改。';
            const wrapper = canvas.parentNode;
            if(wrapper && wrapper.parentNode) wrapper.parentNode.insertBefore(note, wrapper.nextSibling);
          }
        }else{
          finalBtn.textContent = '确认完成';
          finalBtn.style.opacity = '1';
          const exist = document.getElementById('canvas-locked-note');
          if(exist && exist.parentNode) exist.parentNode.removeChild(exist);
        }
      }

      function getPos(e){
        // Map client coords to canvas pixel coordinates, accounting for CSS scaling and DPR
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        let clientX, clientY;
        if(e.touches && e.touches.length){
          clientX = e.touches[0].clientX;
          clientY = e.touches[0].clientY;
        }else{
          clientX = e.clientX;
          clientY = e.clientY;
        }
        const x = (clientX - rect.left) * scaleX;
        const y = (clientY - rect.top) * scaleY;
        return {x:x, y:y, scaleX:scaleX, scaleY:scaleY};
      }

      function start(e){
        if(locked) return;
        // save state before starting a stroke
        pushHistory();
        drawing = true;
        const p = getPos(e);
        lastX = p.x; lastY = p.y;
      }
      function stop(e){ drawing = false; }
      function draw(e){
        if(!drawing || locked) return;
        e.preventDefault();
        const p = getPos(e);
        ctx.strokeStyle = colorPicker.value;
        // scale brush size to canvas pixel space
        const scale = (p.scaleX + p.scaleY) / 2;
        ctx.lineWidth = Math.max(1, Math.round(parseInt(brushSize.value,10) * scale));
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
        if(locked) return;
        pushHistory();
        ctx.clearRect(0,0,canvas.width, canvas.height);
      });

      undoBtn.addEventListener('click', ()=>{
        if(locked) return;
        if(history.length === 0){
          ctx.clearRect(0,0,canvas.width, canvas.height);
          return;
        }
        const img = history.pop();
        try{ ctx.putImageData(img, 0, 0); }catch(e){ console.warn('undo failed', e); ctx.clearRect(0,0,canvas.width, canvas.height); }
      });

      finalBtn.addEventListener('click', ()=>{
        const ok = confirm('确认完成后将无法再修改画布，是否确定？');
        if(ok) setLocked(true);
      });

      downloadBtn.addEventListener('click', ()=>{
        // allow download at any time; don't alter locking here
        try{
          const data = canvas.toDataURL('image/png');
          const a = document.createElement('a');
          a.href = data;
          a.download = 'drawing.png';
          a.click();
        }catch(e){ console.error('download failed', e); }
      });
    })();
    </script>
    '''

    st.components.v1.html(canvas_html, height=680)
