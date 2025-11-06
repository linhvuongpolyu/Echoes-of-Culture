import streamlit as st
import base64
import re

st.set_page_config(page_title="Language Practice", layout="wide")

st.title("语言学习 — 听说练习")

# Sample phrases
PHRASES = [
    {"id": "p1", "text": "你好，我叫小明。很高兴认识你。"},
    # {"id": "p2", "text": "今天天气很好，我们去公园散步吧。"},
    # {"id": "p3", "text": "请把门关上，谢谢。"},
    # {"id": "p4", "text": "你喜欢听什么音乐？"},
    # {"id": "p5", "text": "学习语言需要每天练习。"},
]

# We will not persist recordings across pages or sessions. Recorded audio will be
# displayed temporarily in-page only and will not be saved to disk or session state.


# Helper: small HTML player using Web Speech API to speak text at given rate
def play_text_via_speech(text: str, rate: float = 1.0):
    # Escape text for JS
    safe = text.replace("\"", '\\"').replace("\n", "\\n")
    html = f"""
    <div>
      <button id="speak">▶ 播放（页面内合成语音）</button>
      <script>
        const text = "{safe}";
        const rate = {rate};
        const btn = document.getElementById('speak');
        btn.onclick = () => {{
          if (!window.speechSynthesis) {{
            alert('浏览器不支持 SpeechSynthesis');
            return;
          }}
          const utter = new SpeechSynthesisUtterance(text);
          utter.rate = rate;
          // set a Chinese voice if available
          const voices = window.speechSynthesis.getVoices();
          for (let v of voices) {{ if (/zh|Chinese/i.test(v.lang) || /zh|Chinese/i.test(v.name)) {{ utter.voice = v; break; }} }}
          window.speechSynthesis.cancel();
          window.speechSynthesis.speak(utter);
        }}
        // auto-trigger a small click so Streamlit will just show the player and the user can click
      </script>
    </div>
    """
    # Use components.html to run the player in the browser; user must click the small button.
    st.components.v1.html(html, height=60)


# Recorder component: returns a dataURL (base64) of recorded audio when the user stops recording
def record_component(key: str):
    """Embed a small browser recorder. Playback is handled inside the component
    so audio never needs to be saved on the server."""
    html = """
    <div>
      <style>
        .rec-btn { padding: 10px 14px; font-size: 16px; margin-right:6px; }
        .rec-state { font-size: 14px; margin-left: 10px; color:#374151 }
        .player { margin-top:10px; display:flex; align-items:center; gap:8px; }
      </style>
      <button id="record" class="rec-btn">开始录音</button>
      <button id="stop" class="rec-btn" disabled>停止</button>
      <span id="state" class="rec-state">未录制</span>
      <div id="player" class="player" aria-hidden="true"></div>
      <script>
        const startBtn = document.getElementById('record');
        const stopBtn = document.getElementById('stop');
        const stateSpan = document.getElementById('state');
        const playerDiv = document.getElementById('player');
        let mediaRecorder;
        let audioChunks = [];
        async function start(){
          try{
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
            mediaRecorder.onstart = () => { stateSpan.textContent = '录音中...'; startBtn.disabled = true; stopBtn.disabled = false; audioChunks = []; }
            mediaRecorder.onstop = async () => {
              stateSpan.textContent = '正在处理...';
              const blob = new Blob(audioChunks, { type: 'audio/webm' });
              const reader = new FileReader();
              reader.onloadend = () => {
                const base64data = reader.result; // data:audio/webm;base64,...
                playerDiv.innerHTML = '';
                const audio = document.createElement('audio');
                audio.src = base64data;
                audio.controls = true;
                audio.style.maxWidth = '480px';
                playerDiv.appendChild(audio);
                const playBtn = document.createElement('button');
                playBtn.textContent = '▶ 播放录音';
                playBtn.className = 'rec-btn';
                playBtn.onclick = () => { audio.play(); };
                playerDiv.appendChild(playBtn);
                playerDiv.setAttribute('aria-hidden','false');
              };
              reader.readAsDataURL(blob);
              startBtn.disabled = false; stopBtn.disabled = true; stateSpan.textContent = '完成';
            }
            mediaRecorder.start();
          }catch(err){
            alert('无法访问麦克风：' + err);
          }
        }
        startBtn.addEventListener('click', start);
        stopBtn.addEventListener('click', () => { if (mediaRecorder) mediaRecorder.stop(); });
      </script>
    </div>
    """
    st.components.v1.html(html, height=180)
    return None


st.markdown("""
说明：点击“播放（原速/慢速）”会在浏览器中合成并播放示例句子；点击“录音”打开浏览器录音控件，录音结束后会把音频返回并在页面中显示播放控件。
""")

for ph in PHRASES:
  st.subheader(ph['text'])
  cols = st.columns([1, 1, 1, 1])

  with cols[0]:
    if st.button('播放（原速）', key=f'play_norm_{ph["id"]}'):
      play_text_via_speech(ph['text'], rate=1.0)

  with cols[1]:
    if st.button('播放（慢速）', key=f'play_slow_{ph["id"]}'):
      play_text_via_speech(ph['text'], rate=0.8)

  with cols[2]:
    if st.button('录音', key=f'rec_{ph["id"]}'):
      dataurl = record_component(key=ph['id'])
      # dataurl should be like "data:audio/webm;base64,..."
      if dataurl and isinstance(dataurl, str) and dataurl.startswith('data:'):
        # display audio immediately (temporary in-page only)
        st.success('录音已完成（页面会暂存，可回放）')
        m = re.match(r'data:(?P<mime>[^;]+);base64,(?P<data>.+)', dataurl)
        if m:
          audio_bytes = base64.b64decode(m.group('data'))
          st.audio(audio_bytes)
        else:
          st.write('无法识别的音频格式')

  with cols[3]:
    # Informational note: recordings are temporary and will be cleared when
    # the page is refreshed or navigated away from.
    st.write('（录音回放为页面临时内容，切换页面或刷新后将消失）')

st.markdown('---')
st.markdown('录音仅在当前页面临时保存；切换页面或刷新将清除录音。')
