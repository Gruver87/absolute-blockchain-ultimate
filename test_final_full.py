# test_final_full.py
import requests
import json
import hashlib
import hmac

BASE = "http://localhost:8080"

def sign_message(address, message):
    """Реальная подпись для теста"""
    key = hashlib.sha256(address.encode()).digest()
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

def test():
    print("=" * 60)
    print("ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ v15.2")
    print("=" * 60)
    
    results = {"pass": 0, "fail": 0}
    
    # 1. Health check
    print("\n[1] Health check:")
    try:
        r = requests.get(f"{BASE}/api/health", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Version: {data.get('version')}, Height: {data.get('height')}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
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
            print(f"    ✅ Nonce: {nonce[:32]}...")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # 3. Login с реальной подписью
    print("\n[3] Login (real signature):")
    try:
        signature = sign_message("foundation", message)
        r = requests.post(f"{BASE}/api/auth/login", json={
            "address": "foundation",
            "nonce": nonce,
            "signature": signature
        }, timeout=5)
        print(f"    Status: {r.status_code}")
        data = r.json()
        if data.get('success'):
            token = data.get('access_token')
            print(f"    ✅ Token: {token[:50]}...")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed: {data}")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # 4. Verify token
    print("\n[4] Verify token:")
    try:
        r = requests.get(f"{BASE}/api/auth/verify", 
                         headers={"Authorization": f"Bearer {token}"}, timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Valid: {data.get('valid')}, Address: {data.get('address')}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # 5. Auth stats
    print("\n[5] Auth stats:")
    try:
        r = requests.get(f"{BASE}/api/auth/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Sessions: {data.get('active_refresh_tokens', 0)}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # 6. API stats (проверка что float ещё есть)
    print("\n[6] API stats (проверка total_supply):")
    try:
        r = requests.get(f"{BASE}/api/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            total_supply = data.get('total_supply', 0)
            print(f"    Total supply: {total_supply}")
            if isinstance(total_supply, (int, float)):
                print(f"    ⚠️ Внимание: total_supply всё ещё float")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # Итоги
    print("\n" + "=" * 60)
    print(f"📊 РЕЗУЛЬТАТЫ:")
    print(f"   ✅ Пройдено: {results['pass']}")
    print(f"   ❌ Ошибок: {results['fail']}")
    
    if results['fail'] == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    else:
        print("\n⚠️ Есть ошибки, требуется проверка")
    print("=" * 60)

if __name__ == "__main__":
    test()
