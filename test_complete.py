# test_complete.py
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
    print("ПОЛНОЕ ТЕСТИРОВАНИЕ ABSOLUTE BLOCKCHAIN v15.2")
    print("=" * 60)
    
    results = {"pass": 0, "fail": 0}
    
    print("\n[1] Health check:")
    try:
        r = requests.get(f"{BASE}/api/health", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ {data.get('status')}, Height: {data.get('height')}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    print("\n[2] Challenge:")
    try:
        r = requests.post(f"{BASE}/api/auth/challenge", json={"address": "foundation"}, timeout=5)
        print(f"    Status: {r.status_code}")
        data = r.json()
        nonce = data.get('nonce')
        message = data.get('message')
        print(f"    ✅ Nonce: {nonce[:32]}...")
        results["pass"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
        return
    
    print("\n[3] Login:")
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
            return
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
        return
    
    print("\n[4] Verify token:")
    try:
        r = requests.get(f"{BASE}/api/auth/verify", 
                         headers={"Authorization": f"Bearer {token}"}, timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Valid: {data.get('valid')}, Address: {data.get('address')}")
            print(f"    Expires in: {data.get('expires_in')}s")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    print("\n[5] Auth stats:")
    try:
        r = requests.get(f"{BASE}/api/auth/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Sessions: {data.get('active_sessions', 0)}")
            print(f"    Challenges: {data.get('active_challenges', 0)}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    print("\n[6] API stats (total_supply):")
    try:
        r = requests.get(f"{BASE}/api/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            total = data.get('total_supply', 0)
            print(f"    Total supply: {total}")
            if isinstance(total, int):
                print(f"    ✅ Total supply is INTEGER!")
                results["pass"] += 1
            else:
                print(f"    ⚠️ Total supply is still FLOAT")
                results["fail"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    print("\n" + "=" * 60)
    print(f"📊 РЕЗУЛЬТАТЫ:")
    print(f"   ✅ Успешно: {results['pass']}")
    print(f"   ❌ Ошибок: {results['fail']}")
    
    if results['fail'] == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("🔒 Integer economics работает!")
    else:
        print("\n⚠️ Есть ошибки, требуется проверка")
    print("=" * 60)

if __name__ == "__main__":
    test()
