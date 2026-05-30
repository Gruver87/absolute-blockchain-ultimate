# test_simple.py
import requests
import time

BASE = "http://localhost:8080"

print("=" * 50)
print("ПРОСТАЯ ДИАГНОСТИКА API")
print("=" * 50)

# Тест 1: базовый эндпоинт
print("\n[1] Тест /api/stats:")
try:
    r = requests.get(f"{BASE}/api/stats", timeout=5)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        print(f"    ✅ Работает")
except Exception as e:
    print(f"    ❌ Ошибка: {e}")

# Тест 2: тестовый эндпоинт
print("\n[2] Тест /api/test:")
try:
    r = requests.get(f"{BASE}/api/test", timeout=5)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        print(f"    ✅ Работает: {r.json()}")
except Exception as e:
    print(f"    ❌ Ошибка: {e}")

# Тест 3: challenge
print("\n[3] Тест /api/auth/challenge:")
try:
    r = requests.post(f"{BASE}/api/auth/challenge", json={"address": "foundation"}, timeout=5)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"    ✅ Nonce получен: {data.get('nonce', '')[:32]}...")
except Exception as e:
    print(f"    ❌ Ошибка: {e}")

print("\n" + "=" * 50)
print("Диагностика завершена")
print("=" * 50)
