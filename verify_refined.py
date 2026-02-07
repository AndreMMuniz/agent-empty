import requests
import time
import uuid
import sys
import subprocess
import os

def verify_refined_architecture():
    PORT = 8004
    print(f"Starting FastAPI app on port {PORT}...")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=os.getcwd()
    )
    
    try:
        # Wait for startup and DB initialization
        time.sleep(8)
        
        thread_id = str(uuid.uuid4())
        print(f"Using Thread ID: {thread_id}")
        
        url = f"http://127.0.0.1:{PORT}/chat"
        headers = {"Content-Type": "application/json"}
        
        # Send message
        print("\nSending message to trigger logging...")
        payload = {
            "message": "Explain Bubble.io visual programming.",
            "thread_id": thread_id
        }
        resp = requests.post(url, json=payload, headers=headers)
        
        if resp.status_code == 200:
            print("Chat Response Received.")
            print(f"Content: {resp.json()['response'][:50]}...")
            print("\nSUCCESS: Application is running with new architecture.")
            print("Note: To verify structured logs, check the 'logs_analysis' table in Postgres.")
        else:
            print(f"FAILURE: Status {resp.status_code}")
            print(resp.text)

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
        if stderr:
            print(f"App Stderr:\n{stderr.decode()}")
        if stdout:
             print(f"App Stdout:\n{stdout.decode()}")

if __name__ == "__main__":
    verify_refined_architecture()
