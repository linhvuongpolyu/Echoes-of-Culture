# 🚀 How to Run Culturo Web Application

## 📋 Prerequisites

- **Python**: Version 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Web Browser**: Chrome, Firefox, Safari, or Edge (latest versions recommended)
- **Memory**: At least 2GB RAM recommended
- **Storage**: 500MB free disk space
- **Network**: No internet required after installation (runs locally)

## ⚡ Quick Start Guide

### 1. 📥 Download the Project

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/linhvuongpolyu/Culturo.git
cd Culturo/Culturo
```

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to your desired folder
3. Navigate to the `Culturo/Culturo` directory

### 2. 🔧 Install Dependencies

**Create virtual environment (Recommended)**
```bash
# Windows
python -m venv culturo_env
culturo_env\Scripts\activate

# macOS/Linux  
python3 -m venv culturo_env
source culturo_env/bin/activate
```

**Install required packages**
```bash
pip install -r requirements.txt
```

### 3. 🎯 Run the Application

**Option A: Using the launcher script (Recommended)**
```bash
python start_app.py
```

**Option B: Direct Streamlit command**
```bash
cd frontend
streamlit run main_app.py --server.headless false
```

### 4. 🌐 Access the Web Application

- The web app automatically opens in your default browser
- **Local URL:** http://localhost:8501 (main access point)
- **Network URL:** (displayed in terminal for LAN access from other devices)
- **Web Interface:** Full browser-based interaction
- **Stop Application:** Press `Ctrl+C` in the terminal to stop the web server

## 🎮 Web Application Features

### 🗺️ **Browser-Based Dashboard**
- Interactive country cards with progress tracking
- Real-time star count and completion statistics
- Beautiful gradient backgrounds and smooth web animations
- Responsive design that adapts to your browser window

### 🎯 **Learning Activities**

#### 🗣️ **Language Learning**
- Audio pronunciation guides
- Multiple choice quizzes
- Instant feedback with cultural context
- Region-specific greetings and phrases

#### 🎨 **Animal Drawing** 
- Interactive drawing canvas
- Region-specific animal references
- Instant completion with star rewards
- Creative expression encouragement

#### 🎭 **Performance Culture**
- Educational videos with cultural insights
- Single-question navigation system
- Detailed explanations and reviews
- Traditional art forms exploration

#### 🍜 **Food Culture**
- Culinary tradition videos
- Interactive food knowledge quizzes
- Recipe origins and cultural significance
- Multi-question format with progress tracking

### 🌟 **Achievement System**
- **Star Rewards**: 1-3 stars per activity based on performance
- **Progress Tracking**: Visual indicators and completion percentages
- **Celebration Effects**: Balloons, confetti, and animations
- **Completion Rewards**: Special effects for 100% completion

## 💾 Data Management

- **Progress Storage**: Automatically saved locally in `data/stars.json`
- **Session Persistence**: Progress saved between browser sessions
- **Web-Safe Storage**: Uses local file system (not browser cookies)
- **Reset Option**: Delete `data/stars.json` to reset all progress
- **Privacy**: All data stored locally on your computer
- **No Internet Required**: Fully offline web application

## 🔧 Troubleshooting

### "Python is not recognized"
**Windows:**
1. Install Python from [python.org](https://python.org)
2. Check "Add Python to PATH" during installation
3. Restart command prompt

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### "Streamlit is not installed"
```bash
pip install --upgrade streamlit
```

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### App won't start
1. Check Python version: `python --version` (should be 3.8+)
2. Verify you're in the correct directory: `Culturo/Culturo`
3. Try reinstalling dependencies: `pip install --force-reinstall -r requirements.txt`

### Browser doesn't open automatically
- **Manual Access**: Open your browser and go to http://localhost:8501
- **Port Conflict**: Check if port 8501 is available
- **Alternative Port**: Try `streamlit run main_app.py --server.port 8502`
- **Firewall**: Ensure your firewall allows local web server access
- **Browser Issues**: Try a different browser or incognito/private mode

### Performance issues
1. Close other browser tabs
2. Restart the application
3. Clear browser cache
4. Check available system memory

### Video/Audio not playing
1. Ensure media files exist in `assets/` directory
2. Check browser permissions for media playback
3. Try a different browser
4. Verify file formats are supported

## 🛠️ Advanced Configuration

### Custom Port
```bash
streamlit run main_app.py --server.port 8080
```

### Network Access (LAN)
```bash
streamlit run main_app.py --server.address 0.0.0.0
```

### Development Mode
```bash
streamlit run main_app.py --logger.level debug
```

## 🌐 Web Browser Compatibility

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| Chrome  | 90+     | ✅ Fully Supported | Recommended for best performance |
| Firefox | 88+     | ✅ Fully Supported | Excellent HTML5 support |
| Safari  | 14+     | ✅ Fully Supported | Works great on macOS/iOS |
| Edge    | 90+     | ✅ Fully Supported | Modern Chromium-based |
| Opera   | 76+     | ✅ Supported | Good alternative browser |
| IE      | Any     | ❌ Not Supported | Lacks modern web standards |

**Note**: The application uses modern web technologies (HTML5, CSS3, JavaScript ES6+), so recent browser versions are required.

## 🔄 Updating the Application

```bash
git pull origin main
pip install --upgrade -r requirements.txt
python start_app.py
```

## 📞 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify system requirements
3. Create an issue on GitHub with:
   - Your operating system
   - Python version
   - Error messages
   - Steps to reproduce

---

**Happy Learning! 🎓✨**

Explore the rich cultural traditions of Vietnam, China, and Hong Kong through our interactive web-based learning platform!

### 🌐 Web Application Benefits:
- **Modern Interface**: Clean, responsive web design
- **Cross-Platform**: Works on any device with a modern browser
- **Local Privacy**: Your data stays on your computer
- **Easy Sharing**: Can be accessed by family members on the same network
- **Future-Ready**: Easy to deploy to cloud platforms when needed
```bash
pip install streamlit
```

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Port already in use
Streamlit will automatically find another available port, or you can specify one:
```bash
streamlit run main_app.py --server.port 8502
```

## Architecture

**Before:** Flask Backend + Streamlit Frontend (unnecessarily complex)  
**Now:** Pure Streamlit (simple and efficient)

All data management is handled directly by Streamlit using a simple JSON file.

