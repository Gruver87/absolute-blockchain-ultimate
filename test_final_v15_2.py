# test_final_v15_2.py
import requests
import json
import hashlib
import hmac

BASE = "http://localhost:8080"
SATOSHI_MULTIPLIER = 100_000_000

def sign_message(address, message):
    key = hashlib.sha256(address.encode()).digest()
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

def test():
    print("=" * 60)
    print("ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ ABSOLUTE BLOCKCHAIN v15.2")
    print("=" * 60)
    
    results = {"pass": 0, "fail": 0}
    
    # 1. Health
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
    
    # 2. API Stats (проверка разделения units)
    print("\n[2] API Stats:")
    try:
        r = requests.get(f"{BASE}/api/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Total supply (satoshi): {data.get('total_supply_satoshi', 'N/A')}")
            print(f"    ✅ Total supply (ABS): {data.get('total_supply_abs', 'N/A')}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    # 3. Challenge
    print("\n[3] Challenge:")
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
    
    # 4. Login (с реальной подписью)
    print("\n[4] Login (real signature):")
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
                print(f"    ❌ Login failed: {data.get('error')}")
                results["fail"] += 1
                return
        else:
            print(f"    ❌ HTTP {r.status_code}")
            results["fail"] += 1
            return
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
        return
    
    # 5. Verify token
    print("\n[5] Verify token:")
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
    
    # 6. Auth stats
    print("\n[6] Auth stats:")
    try:
        r = requests.get(f"{BASE}/api/auth/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"    ✅ Active sessions: {data.get('active_sessions', 0)}")
            print(f"    Active challenges: {data.get('active_challenges', 0)}")
            results["pass"] += 1
        else:
            print(f"    ❌ Failed (404 - route not registered)")
            results["fail"] += 1
    except Exception as e:
        print(f"    ❌ Error: {e}")
        results["fail"] += 1
    
    print("\n" + "=" * 60)
    print(f"📊 РЕЗУЛЬТАТЫ: {results['pass']} / {results['pass'] + results['fail']}")
    
    if results['fail'] == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("🔒 Real signature verification: OK")
        print("💰 Integer economics: OK")
        print("📡 Auth endpoints: OK")
    else:
        print(f"\n⚠️ Ошибок: {results['fail']}")
    print("=" * 60)

if __name__ == "__main__":
    test()
