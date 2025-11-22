#!/usr/bin/env python3
"""
Culturo App Launcher
Simple launcher for the Streamlit application
"""
import subprocess
import sys
import os

def main():
    """Start the Streamlit application"""
    print("=" * 60)
    print("🌍 Starting Culturo - Cultural Knowledge Exploration App")
    print("=" * 60)
    
    # Reset star data on startup
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    stars_file = os.path.join(data_dir, "stars.json")
    
    if os.path.exists(stars_file):
        os.remove(stars_file)
        print("🔄 Reset star data for fresh start")
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    
    print(f"\n📂 Frontend directory: {frontend_dir}")
    print("🚀 Launching Streamlit application...")
    print("\nPress Ctrl+C to stop the application\n")
    print("=" * 60)
    
    try:
        # Run streamlit directly with configuration flags
        subprocess.run(
            [
                "streamlit", "run", "main_app.py",
                "--server.headless", "false",
                "--browser.gatherUsageStats", "false"
            ],
            cwd=frontend_dir,
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("👋 Application closed. Thank you for using Culturo!")
        print("=" * 60)
    except FileNotFoundError:
        print("\n❌ Error: Streamlit is not installed!")
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
