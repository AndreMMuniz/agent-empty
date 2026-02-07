import requests
import json

try:
    url = "http://127.0.0.1:8002/chat"
    payload = {"message": "Como posso otimizar meu repeating group no Bubble?"}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload, headers=headers)
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")

except Exception as e:
    print(f"Failed to connect: {e}")
