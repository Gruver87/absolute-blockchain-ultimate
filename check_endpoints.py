# check_endpoints.py
import requests
import time

print("=" * 60)
print("ДИАГНОСТИКА ЭНДПОИНТОВ")
print("=" * 60)

endpoints = [
    ("/api/health", "GET"),
    ("/api/stats", "GET"),
    ("/api/auth/stats", "GET"),
    ("/api/auth/verify", "GET"),
]

for ep, method in endpoints:
    try:
        if method == "GET":
            r = requests.get(f"http://localhost:8080{ep}", timeout=3)
        else:
            r = requests.post(f"http://localhost:8080{ep}", timeout=3)
        
        if r.status_code == 200:
            print(f"✅ {ep} -> {r.status_code}")
            if ep == "/api/stats":
                data = r.json()
                if "total_supply_satoshi" in data:
                    print(f"   ✅ Улучшенный формат!")
                else:
                    print(f"   ⚠️ Старый формат")
        else:
            print(f"❌ {ep} -> {r.status_code}")
    except Exception as e:
        print(f"❌ {ep} -> Error: {e}")

print("=" * 60)
