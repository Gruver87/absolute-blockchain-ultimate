# quick_test.py
import requests
import time

print("=" * 50)
print("БЫСТРЫЙ ТЕСТ ЭНДПОИНТОВ")
print("=" * 50)

endpoints = [
    ("/api/health", "GET"),
    ("/api/stats", "GET"),
    ("/api/auth/stats", "GET"),
]

for ep, method in endpoints:
    try:
        if method == "GET":
            r = requests.get(f"http://localhost:8080{ep}", timeout=3)
        else:
            r = requests.post(f"http://localhost:8080{ep}", timeout=3)
        
        if r.status_code == 200:
            print(f"✅ {ep} -> {r.status_code}")
            if ep == "/api/health":
                print(f"   {r.json().get('status', 'N/A')}")
            elif ep == "/api/stats":
                print(f"   Blocks: {r.json().get('blocks', 'N/A')}")
            elif ep == "/api/auth/stats":
                print(f"   Sessions: {r.json().get('active_sessions', 'N/A')}")
        else:
            print(f"❌ {ep} -> {r.status_code}")
    except Exception as e:
        print(f"❌ {ep} -> Error: {e}")

print("=" * 50)
print("Тест завершён")
print("=" * 50)
