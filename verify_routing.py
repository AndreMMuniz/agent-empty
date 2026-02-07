import requests
import time
import uuid
import sys
import subprocess
import os

def verify_routing():
    PORT = 8005
    print(f"Starting FastAPI app on port {PORT}...")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )
    
    try:
        # Wait for startup with retries
        url = f"http://127.0.0.1:{PORT}/chat"
        print(f"URL: {url}")
        
        connected = False
        for i in range(10):
            try:
                print(f"Attempt {i+1} to connect...")
                check = requests.get(f"http://127.0.0.1:{PORT}/")
                if check.status_code == 200:
                    connected = True
                    print("Connected!")
                    break
            except:
                time.sleep(3)
        
        if not connected:
            print("Could not connect to app.")
            return

        thread_id = str(uuid.uuid4())
        print(f"Using Thread ID: {thread_id}")
        headers = {"Content-Type": "application/json"}
        
        # Test 1: Consultation
        print("\nTest 1: Consultation Query")
        payload1 = {"message": "How do I create a new page in Bubble?", "thread_id": thread_id}
        resp1 = requests.post(url, json=payload1, headers=headers)
        if resp1.status_code == 200:
            print(f"Response: {resp1.json()['response'][:100]}...")
        else:
            print(f"Error {resp1.status_code}: {resp1.text}")
        
        # Test 2: Log Analysis
        print("\nTest 2: Log Analysis Query")
        payload2 = {"message": "Error 500: Database connection failed at line 42.", "thread_id": thread_id}
        resp2 = requests.post(url, json=payload2, headers=headers)
        if resp2.status_code == 200:
            print(f"Response: {resp2.json()['response'][:100]}...")
        else:
            print(f"Error {resp2.status_code}: {resp2.text}")

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        print("Stopping app...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()
            
        stdout, stderr = process.communicate()
        if stderr and "Error" in stderr.decode():
             print(f"App Stderr:\n{stderr.decode()}")

if __name__ == "__main__":
    verify_routing()
