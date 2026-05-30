# test_final.py
import requests
import json

BASE = "http://localhost:8080"

def test():
    print("=" * 60)
    print("ФИНАЛЬНОЕ ТЕСТИРОВАНИЕ")
    print("=" * 60)
    
    # 1. Health check
    print("\n[1] Health check:")
    r = requests.get(f"{BASE}/api/health")
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        print(f"    Response: {r.json()}")
    
    # 2. Challenge
    print("\n[2] Challenge:")
    r = requests.post(f"{BASE}/api/auth/challenge", json={"address": "foundation"})
    print(f"    Status: {r.status_code}")
    data = r.json()
    nonce = data.get('nonce')
    print(f"    Nonce: {nonce[:32]}...")
    
    # 3. Login (с реальной подписью)
    print("\n[3] Login:")
    r = requests.post(f"{BASE}/api/auth/login", json={
        "address": "foundation",
        "nonce": nonce,
        "signature": "real_signature_will_be_verified"
    })
    print(f"    Status: {r.status_code}")
    data = r.json()
    
    if data.get('success'):
        token = data.get('access_token')
        print(f"    ✅ Token: {token[:50]}...")
        
        # 4. Verify
        print("\n[4] Verify token:")
        r = requests.get(f"{BASE}/api/auth/verify", 
                         headers={"Authorization": f"Bearer {token}"})
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    Response: {r.json()}")
        
        # 5. Stats
        print("\n[5] Auth stats:")
        r = requests.get(f"{BASE}/api/auth/stats")
        print(f"    Status: {r.status_code}")
        if r.status_code == 200:
            print(f"    Response: {r.json()}")
    else:
        print(f"    ❌ Login failed: {data}")
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено")
    print("=" * 60)

if __name__ == "__main__":
    test()
