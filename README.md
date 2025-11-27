# 🌍 Culturo - Cultural Knowledge Exploration App

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

Culturo is an interactive educational web application that helps primary and secondary students explore cultural diversity through gamified experiences. Students can discover the rich traditions of **Vietnam**, **Hong Kong**, and **China** through engaging activities covering language, performing arts, cuisine, and traditional animals.

## ✨ Features

### 🗺️ **Interactive Cultural Explorer**
- **Three Regions**: Vietnam 🇻🇳, China 🇨🇳, Hong Kong 🇭🇰
- **Beautiful UI**: Modern design with region-specific colors and flags
- **Progress Tracking**: Star-based achievement system

### 🎯 **Four Learning Activities**

#### 🗣️ **Language Learning**
- Listen to authentic regional pronunciations
- Multiple choice pronunciation quiz
- Learn traditional greetings in local languages
- Audio-based interactive learning

#### 🎨 **Animal Drawing**
- Interactive drawing canvas
- Region-specific animal references (pandas, water buffalo, etc.)
- Creative expression through art
- Instant completion feedback

#### 🎭 **Performance Culture**
- Educational videos about traditional performances
- Single-question navigation quiz format
- Learn about Water Puppetry, Face Changing, Ying Ge Dance
- Detailed question review and explanations

#### 🍜 **Food Culture**
- Culinary tradition videos
- Interactive food culture quizzes
- Learn about Pho, Peking Duck, Pineapple Bun origins
- Recipe insights and cultural significance

### 🎮 **Gamification Elements**
- **Star System**: Earn 1-3 stars per activity based on performance
- **Progress Tracking**: Visual progress indicators
- **Achievement Effects**: Balloons, confetti, and celebration animations
- **Completion Rewards**: Special congratulations with multiple effects

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/linhvuongpolyu/Culturo.git
   cd Culturo/Culturo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python start_app.py
   ```

4. **Access the web application**
   - The app automatically opens in your default web browser
   - Local URL: `http://localhost:8501`
   - Network URL: Available for LAN access (displayed in terminal)

## 📱 User Interface

### Main Dashboard
- **Region Cards**: Interactive cards for each country with progress tracking
- **Statistics**: Total stars earned and countries explored
- **Navigation**: Sidebar with logo and region switching

### Activity Pages
- **Consistent Header**: Flag, activity name, and star display
- **Two-Column Layout**: Content on left, activities on right
- **Progress Indicators**: Visual feedback and encouragement messages

## 🏗️ Technical Architecture

- **Application Type**: Local web application
- **Web Framework**: Streamlit (Python-based web framework)
- **Frontend**: Browser-based interface with HTML/CSS/JavaScript
- **Backend**: Local Python server
- **Styling**: Custom CSS with responsive web design
- **Data Storage**: Local JSON file-based (no database required)
- **Media Assets**: Local video, audio, and image files served via web server
- **Session Management**: Web-based session state management

## 📁 Project Structure

```
Culturo/
├── assets/                 # Media files
│   ├── images/            # UI images and references
│   ├── videos/            # Educational videos
│   ├── languages/         # Audio files and language images
│   └── map/               # Country maps
├── backend/               # Future API expansion
├── data/                  # JSON data storage
├── frontend/              # Streamlit application
│   ├── main_app.py       # Main dashboard
│   ├── pages/            # Activity pages
│   └── utils/            # Helper utilities
├── requirements.txt       # Python dependencies
├── start_app.py          # Application launcher
└── HOW_TO_RUN.md         # Detailed setup guide
```

## 🎨 Customization

### Adding New Regions
1. Add region data to activity functions
2. Include flag URLs and colors
3. Add corresponding media assets
4. Update navigation logic

### Extending Activities
1. Create new page files in `frontend/pages/`
2. Update navigation in region pages
3. Add star tracking for new activities

## 📊 Data Management

- **Progress Persistence**: Stars saved in `data/stars.json`
- **Session Management**: Region switching with state reset
- **Performance**: Optimized for local file system

## 🎯 Educational Objectives

- **Cultural Awareness**: Understanding diverse Asian traditions through interactive web content
- **Language Exposure**: Audio-based pronunciation and greeting familiarity
- **Creative Expression**: Web-based drawing and artistic activities
- **Knowledge Retention**: Interactive quiz-based learning with immediate feedback
- **Digital Literacy**: Modern web application interaction skills
- **Progress Motivation**: Gamified achievement system with visual feedback

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Development Team**: Educational technology specialists
- **Cultural Consultants**: Regional culture experts
- **UI/UX Design**: Interactive learning experience designers

## 🙏 Acknowledgments

- Cultural content reviewers and educational consultants
- Media asset contributors and translators
- Beta testing educators and students
- Open source community for Streamlit framework

---

## 🌐 Application Type

**Culturo** is a **local web application** - it runs a web server on your computer and opens in your browser, combining the convenience of web technology with the privacy and control of local installation.

**Benefits of this approach:**
- ✅ Modern, responsive web-based interface
- ✅ Cross-platform compatibility (Windows, macOS, Linux)
- ✅ No internet required after installation
- ✅ Easy to use - just click and learn!
- ✅ Potential for future cloud deployment

**Note**: This project replaces the previous Echoes-of-Culture proposal. The original proposal is retained in the repository for reference and to document the team's development process.

*For detailed technical information, see the `Culturo_Project_Proposal.md` file.*
