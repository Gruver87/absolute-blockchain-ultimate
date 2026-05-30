# test_final_v2.py
import requests
import json
import hashlib
import hmac
import time

BASE = "http://localhost:8080"

def sign_message(address, message):
    key = hashlib.sha256(address.encode()).digest()
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

def test():
    print("=" * 60)
    print("ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ v15.2 (INTEGER ECONOMICS)")
    print("=" * 60)
    
    # Проверка доступности сервера
    print("\n[0] Проверка сервера:")
    try:
        r = requests.get(f"{BASE}/api/stats", timeout=3)
        print(f"    ✅ Сервер доступен (status {r.status_code})")
    except Exception as e:
        print(f"    ❌ Сервер не отвечает: {e}")
        print("    Запустите блокчейн: python ABSOLUTE_FINAL_FIXED.py")
        return
    
    results = {"pass": 0, "fail": 0}
    
    # 1. Health
    print("\n[1] Health check:")
    try:
        r = requests.get(f"{BASE}/api/health", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ {data.get('status')}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed (404 - endpoint не зарегистрирован)")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # 2. Challenge
    print("\n[2] Challenge:")
    try:
        r = requests.post(f"{BASE}/api/auth/challenge", json={"address": "foundation"}, timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            nonce = data.get('nonce')
            message = data.get('message')
            print(f"    ✅ Nonce получен")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
            return
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
        return
    
    # 3. Login
    print("\n[3] Login:")
    try:
        signature = sign_message("foundation", message)
        r = requests.post(f"{BASE}/api/auth/login", json={
            "address": "foundation",
            "nonce": nonce,
            "signature": signature
        }, timeout=10)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if data.get('success'):
                token = data.get('access_token')
                print(f"    ✅ Token получен")
                results["pass"] += 1
            else:
                print(f"    ❌ Login failed: {data}")
                results["fail"] += 1
                return
        else:
            print(f"    ❌ HTTP {r.status_code}")
            results["fail"] += 1
            return
    except requests.Timeout:
        print(f"    ❌ Timeout - сервер завис")
        print("    Возможно, БД заблокирована")
        results["fail"] += 1
        return
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
        return
    
    # 4. Verify
    print("\n[4] Verify token:")
    try:
        r = requests.get(f"{BASE}/api/auth/verify", 
                         headers={"Authorization": f"Bearer {token}"}, timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Valid: {data.get('valid')}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # 5. Stats
    print("\n[5] Auth stats:")
    try:
        r = requests.get(f"{BASE}/api/auth/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Active sessions: {data.get('active_sessions', 0)}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    print("\n" + "=" * 60)
    print(f"📊 РЕЗУЛЬТАТЫ: {results['pass']} / {results['pass'] + results['fail']}")
    
    if results['fail'] == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print(f"\n⚠️ Ошибок: {results['fail']}")
    print("=" * 60)

if __name__ == "__main__":
    test()
