# diagnose_startup.py
import requests
import time

print("=" * 60)
print("ДИАГНОСТИКА ЗАПУСКА")
print("=" * 60)

# Проверка доступности
for i in range(10):
    try:
        r = requests.get("http://localhost:8080/api/stats", timeout=2)
        print(f"✅ Сервер отвечает (попытка {i+1})")
        break
    except:
        print(f"⏳ Ожидание сервера... ({i+1}/10)")
        time.sleep(2)
else:
    print("❌ Сервер не запущен!")
    exit()

print("\n--- ПРОВЕРКА ЭНДПОИНТОВ ---")

endpoints = [
    "/api/health",
    "/api/auth/verify",
    "/api/auth/stats"
]

for ep in endpoints:
    try:
        r = requests.get(f"http://localhost:8080{ep}", timeout=3)
        print(f"✅ {ep} -> {r.status_code}")
        if r.status_code == 200:
            print(f"   Response: {r.json()}")
    except Exception as e:
        print(f"❌ {ep} -> {e}")

print("\n" + "=" * 60)
