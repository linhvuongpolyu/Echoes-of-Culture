# How to Run Culturo App

## Quick Start

The app has been simplified to use **pure Streamlit** - no backend API server needed!

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

**Option A: Using the launcher script (Recommended)**
```bash
python start_app.py
```

**Option B: Direct Streamlit command**
```bash
cd frontend
streamlit run main_app.py
```

### 3. Access the App

The app will automatically open in your browser at:
- **Local URL:** http://localhost:8501
- **Network URL:** (shown in terminal)

## Features

- 🗺️ **Interactive Map:** Click on regions (Hong Kong, China, Vietnam) to explore
- 🗣️ **Language:** Learn regional pronunciations  
- 🎨 **Draw Animals:** Interactive drawing activities
- 🍜 **Food Culture:** Video quizzes about regional cuisine
- 🎭 **Performance Culture:** Learn about traditional performances
- ⭐ **Star System:** Earn stars and track your progress (saved locally)

## Data Storage

- Stars and progress are saved in `data/stars.json`
- No database or API server required
- Data persists between sessions

## Troubleshooting

### "Streamlit is not installed"
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

