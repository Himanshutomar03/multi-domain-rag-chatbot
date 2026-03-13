import requests

BASE = "http://127.0.0.1:8000"

print("=== Health Check ===")
r = requests.get(f"{BASE}/health")
print(f"Status: {r.status_code}, Response: {r.json()}")

print("\n=== Medical Domain Test ===")
r = requests.post(f"{BASE}/api/chat", json={"message": "What are the symptoms of anemia?", "domain": "medical"})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"Mode: {data.get('mode', 'N/A')}")
    print(f"Answer: {data.get('answer', 'N/A')[:300]}...")
else:
    print(f"Error: {r.text[:300]}")

print("\n=== Education Domain Test ===")
r = requests.post(f"{BASE}/api/chat", json={"message": "What is machine learning?", "domain": "education"})
print(f"Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"Mode: {data.get('mode', 'N/A')}")
    print(f"Answer: {data.get('answer', 'N/A')[:300]}...")
else:
    print(f"Error: {r.text[:300]}")
