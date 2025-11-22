import subprocess
import time
import sys
import os

def start_backend():
    """starting the backend API service"""
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    return subprocess.Popen([sys.executable, "api_server.py"], cwd=backend_dir)

def start_frontend():
    """starting the frontend Streamlit app"""
    frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
    return subprocess.Popen(["streamlit", "run", "main_app.py"], cwd=frontend_dir)

if __name__ == "__main__":
    print("starting the backend API service...")
    backend_process = start_backend()
    
    # wait for backend to start
    time.sleep(3)
    
    print("starting the frontend Streamlit app...")
    frontend_process = start_frontend()
    
    try:
        # wait for processes to complete
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("closing application...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()
        print("application closed")