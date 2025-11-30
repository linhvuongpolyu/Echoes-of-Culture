#!/usr/bin/env python3
"""
Culturo Web Application Launcher
Educational Cultural Knowledge Exploration Web App

This launcher provides an easy way to start the Culturo web application
with proper configuration and user-friendly output.

Usage: python start_app.py
"""
import subprocess
import sys
import os
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        sys.exit(1)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        return True
    except ImportError:
        print("❌ Error: Streamlit is not installed!")
        print("\n📦 Please install required packages:")
        print("   pip install -r requirements.txt")
        print("\n💡 Or install Streamlit directly:")
        print("   pip install streamlit")
        return False

def get_system_info():
    """Get system information for debugging"""
    return {
        'platform': platform.system(),
        'python_version': sys.version.split()[0],
        'architecture': platform.architecture()[0]
    }

def setup_directories():
    """Ensure required directories exist and reset progress for fresh start"""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Always reset stars.json for fresh start every time
    stars_file = data_dir / "stars.json"
    stars_file.write_text('{}')
    print("🔄 Reset progress data for fresh learning experience")

def main():
    """Start the Streamlit application with enhanced setup"""
    print("\n" + "=" * 70)
    print("🌍 CULTURO - Cultural Knowledge Exploration Web App")
    print("   Interactive Educational Web-Based Learning Platform")
    print("=" * 70)
    
    # System check
    print("\n🔍 System Check:")
    check_python_version()
    
    system_info = get_system_info()
    print(f"   ✅ Python {system_info['python_version']} on {system_info['platform']}")
    
    if not check_dependencies():
        sys.exit(1)
    
    print("   ✅ All dependencies installed")
    
    # Setup
    setup_directories()
    
    # Application info
    print("\n🎯 Features Available:")
    print("   • 🗣️  Language Learning (Audio + Quiz)")
    print("   • 🎨 Animal Drawing (Interactive Canvas)")
    print("   • 🎭 Performance Culture (Video + Quiz)")
    print("   • 🍜 Food Culture (Video + Quiz)")
    print("   • ⭐ Star Achievement System")
    print("   • 🌍 3 Regions: Vietnam, China, Hong Kong")
    
    # Launch info
    frontend_dir = Path(__file__).parent / "frontend"
    print(f"\n🚀 Launching Web Application:")
    print(f"   📂 Server Directory: {frontend_dir}")
    print(f"   🌐 Local URL: http://localhost:8501")
    print(f"   📱 Browser: Will open automatically")
    print(f"   ⚡ Mode: Interactive Web-Based Learning")
    
    print("\n⌨️  Web Application Controls:")
    print("   • Web app opens automatically in your default browser")
    print("   • Press Ctrl+C in this terminal to stop the web server")
    print("   • Fresh start every time - progress resets on each launch")
    print("   • Close browser tab anytime - server keeps running until stopped")
    
    print("\n" + "=" * 70)
    print("🎓 Starting Web-Based Educational Experience...")
    print("🌐 Web server starting - browser will open shortly...")
    print("=" * 70)
    
    try:
        # Enhanced Streamlit launch with optimal settings
        subprocess.run(
            [
                "streamlit", "run", "main_app.py",
                "--server.headless", "false",
                "--browser.gatherUsageStats", "false",
                "--server.fileWatcherType", "none",  # Reduce resource usage
                "--theme.primaryColor", "#004DA0",    # Culturo blue theme
                "--theme.backgroundColor", "#EFF8FF",  # Light blue background
            ],
            cwd=frontend_dir,
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("👋 Thank you for using Culturo Web App!")
        print("   🌐 Web server stopped successfully")
        print("   💾 Your learning progress has been saved locally")
        print("   🚀 Continue your cultural journey anytime by restarting!")
        print("=" * 70)
        print("🌟 Keep exploring and learning through the web! 🌟")
    except FileNotFoundError:
        print("\n❌ Error: Streamlit command not found!")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure Streamlit is installed: pip install streamlit")
        print("   2. Check your Python PATH environment")
        print("   3. Try: python -m streamlit run frontend/main_app.py")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting application: {e}")
        print("\n🔧 Web Server Troubleshooting:")
        print("   1. Check if port 8501 is available for web server")
        print("   2. Try alternative port: streamlit run main_app.py --server.port 8502")
        print("   3. Ensure no other web servers are running on the same port")
        print("   4. Restart your terminal and try again")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\n📞 Support:")
        print("   • Check HOW_TO_RUN.md for detailed troubleshooting")
        print("   • Create an issue on GitHub with error details")
        sys.exit(1)

if __name__ == "__main__":
    main()
