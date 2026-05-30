# test_real_auth.py
import requests
import json
import hashlib
import hmac

BASE = "http://localhost:8080"

def sign_message(address, message):
    """Симуляция подписи для теста"""
    key = hashlib.sha256(address.encode()).digest()
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()

def test():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ РЕАЛЬНОЙ АУТЕНТИФИКАЦИИ")
    print("=" * 60)
    
    # 1. Health check
    print("\n[1] Health check:")
    r = requests.get(f"{BASE}/api/health", timeout=5)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        print(f"    ✅ {r.json()}")
    
    # 2. Challenge
    print("\n[2] Challenge:")
    r = requests.post(f"{BASE}/api/auth/challenge", json={"address": "foundation"}, timeout=5)
    print(f"    Status: {r.status_code}")
    data = r.json()
    nonce = data.get('nonce')
    message = data.get('message')
    print(f"    Nonce: {nonce[:32]}...")
    
    # 3. Login с реальной подписью
    print("\n[3] Login (с реальной подписью):")
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
        print(f"    ✅ Token получен: {token[:50]}...")
        
        # 4. Verify
        print("\n[4] Verify token:")
        r = requests.get(f"{BASE}/api/auth/verify", 
                         headers={"Authorization": f"Bearer {token}"}, timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    ✅ {r.json()}")
        
        # 5. Stats
        print("\n[5] Auth stats:")
        r = requests.get(f"{BASE}/api/auth/stats", timeout=5)
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    ✅ {r.json()}")
    else:
        print(f"    ❌ Login failed: {data}")
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено")
    print("=" * 60)

if __name__ == "__main__":
    test()
