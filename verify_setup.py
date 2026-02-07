import requests
import sys
import time
import subprocess
import os
import signal

def run_verification():
    """
    Starts the FastAPI app and sends a test request.
    """
    print("Starting FastAPI app...")
    # Start the app in a subprocess
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )
    
    try:
        # Wait for app to start
        print("Waiting for app to start...")
        time.sleep(5)
        
        # Check health
        try:
            health = requests.get("http://127.0.0.1:8000/")
            print(f"Health Check: {health.status_code} - {health.json()}")
        except Exception as e:
            print(f"Health Check Failed: {e}")
            return

        # Test Chat Endpoint
        payload = {"message": "How do I optimize a repeating group in Bubble?"}
        print(f"Sending test payload: {payload}")
        
        try:
            response = requests.post("http://127.0.0.1:8000/chat", json=payload)
            print(f"Chat Response: {response.status_code}")
            if response.status_code == 200:
                print(f"Response Content: {response.json()}")
            else:
                print(f"Error Content: {response.text}")
        except Exception as e:
            print(f"Chat Request Failed: {e}")

    finally:
        # cleanup
        print("Stopping app...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        
        # Print logs if any
        stdout, stderr = process.communicate()
        if stdout: print(f"App Stdout:\n{stdout.decode()}")
        if stderr: print(f"App Stderr:\n{stderr.decode()}")

if __name__ == "__main__":
    run_verification()
