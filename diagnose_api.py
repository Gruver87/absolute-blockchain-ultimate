# diagnose_api.py
import requests
import json

BASE = "http://localhost:8080"

def test_endpoint(name, method="GET", data=None):
    url = f"{BASE}{name}"
    try:
        if method == "GET":
            r = requests.get(url, timeout=3)
        else:
            r = requests.post(url, json=data, timeout=3)
        print(f"✅ {name} -> {r.status_code}")
        if r.status_code == 200:
            try:
                print(f"   Response: {json.dumps(r.json(), indent=2)[:200]}")
            except:
                print(f"   Response: {r.text[:200]}")
        return True
    except Exception as e:
        print(f"❌ {name} -> Error: {e}")
        return False

print("=" * 60)
print("ДИАГНОСТИКА API")
print("=" * 60)

# Базовые тесты
test_endpoint("/")
test_endpoint("/api/stats")
test_endpoint("/ping")

# Auth тесты
print("\n--- AUTH TESTS ---")
test_endpoint("/api/auth/challenge", "POST", {"address": "foundation"})
test_endpoint("/api/auth/verify")
test_endpoint("/api/auth/stats")

print("\n" + "=" * 60)
print("Диагностика завершена")
print("=" * 60)
