# test_updated.py
import requests
import json
import hashlib
import hmac

BASE = "http://localhost:8080"

def sign_message(address, message):
    key = hashlib.sha256(address.encode()).digest()
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

def test():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ПОСЛЕ МИГРАЦИИ")
    print("=" * 60)
    
    # 1. Проверка сервера
    print("\n[1] Проверка сервера:")
    try:
        r = requests.get(f"{BASE}/api/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    ✅ Сервер работает")
        else:
            print(f"    ❌ Ошибка: {r.status_code}")
            return
    except Exception as e:
        print(f"    ❌ Сервер не отвечает: {e}")
        print("    Запустите: python ABSOLUTE_FINAL_FIXED.py")
        return
    
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
        else:
            print(f"    ❌ Failed")
            return
    except Exception as e:
        print(f"    ❌ Error: {e}")
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
                
                # 4. Verify
                print("\n[4] Verify token:")
                r = requests.get(f"{BASE}/api/auth/verify", 
                                 headers={"Authorization": f"Bearer {token}"}, timeout=5)
                print(f"    Status: {r.status_code}")
                if r.status_code == 200:
                    data = r.json()
                    print(f"    ✅ Valid: {data.get('valid')}")
                else:
                    print(f"    ❌ Verify failed")
                
                # 5. Stats
                print("\n[5] Auth stats:")
                r = requests.get(f"{BASE}/api/auth/stats", timeout=5)
                print(f"    Status: {r.status_code}")
                if r.status_code == 200:
                    data = r.json()
                    print(f"    ✅ Sessions: {data.get('active_sessions', 0)}")
            else:
                print(f"    ❌ Login failed")
        else:
            print(f"    ❌ HTTP {r.status_code}")
    except requests.Timeout:
        print(f"    ❌ Timeout - сервер завис")
    except Exception as e:
        print(f"    ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Тестирование завершено")
    print("=" * 60)

if __name__ == "__main__":
    test()
