import requests
import time
import uuid
import sys
import subprocess
import os

def verify_persistence():
    PORT = 8003
    print(f"Starting FastAPI app on port {PORT}...")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )
    
    try:
        # Wait for startup
        time.sleep(5)
        
        # Define a thread ID
        thread_id = str(uuid.uuid4())
        print(f"Using Thread ID: {thread_id}")
        
        url = f"http://127.0.0.1:{PORT}/chat"
        headers = {"Content-Type": "application/json"}
        
        # Step 1: Give context
        print("\nStep 1: Sending 'Hi, I am verifying persistence.'")
        payload1 = {
            "message": "Hi, I am verifying persistence. My secret code is 12345.",
            "thread_id": thread_id
        }
        resp1 = requests.post(url, json=payload1, headers=headers)
        print(f"Response 1: {resp1.json()['response']}")
        
        # Step 2: Ask for context
        print("\nStep 2: Asking 'What is my secret code?'")
        payload2 = {
            "message": "What is my secret code?",
            "thread_id": thread_id
        }
        resp2 = requests.post(url, json=payload2, headers=headers)
        content = resp2.json()['response']
        print(f"Response 2: {content}")
        
        if "12345" in content:
            print("\nSUCCESS: Persistence worked! The agent remembered the code.")
        else:
            print("\nFAILURE: Agent did not remember the code.")
            
    except Exception as e:
        print(f"Error during verification: {e}")
        
    finally:
        print("Stopping app...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except:
            process.kill()
        
        # Print logs for debugging if needed
        stdout, stderr = process.communicate()
        if "Error" in str(stderr):
            print(f"App Stderr:\n{stderr.decode()}")

if __name__ == "__main__":
    verify_persistence()
