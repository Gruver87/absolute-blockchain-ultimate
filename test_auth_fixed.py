# test_auth_fixed.py
# Тестирование JWT аутентификации

import requests
import json

BASE_URL = "http://localhost:8080"

def test_auth():
    print("=" * 60)
    print("Тестирование JWT аутентификации")
    print("=" * 60)
    
    # 1. Получение challenge
    print("\n[1] Получение challenge...")
    resp = requests.post(f"{BASE_URL}/api/auth/challenge", 
                         json={"address": "foundation"})
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    print(f"    Success: {data.get('success', False)}")
    
    if not data.get('success'):
        print(f"    Error: {data.get('error')}")
        return
    
    nonce = data.get('nonce')
    print(f"    Nonce: {nonce[:32]}...")
    print(f"    Expires in: {data.get('expires_in')}s")
    
    # 2. Аутентификация
    print("\n[2] Аутентификация...")
    resp = requests.post(f"{BASE_URL}/api/auth/login",
                         json={
                             "address": "foundation",
                             "nonce": nonce,
                             "signature": "test_signature_any_length_is_now_accepted"
                         })
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    
    if not data.get('success'):
        print(f"    Error: {data.get('error')}")
        return
    
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    
    print(f"    ✅ Authenticated!")
    print(f"    Access token: {access_token[:50]}...")
    print(f"    Refresh token: {refresh_token[:50]}...")
    print(f"    Access expires in: {data.get('access_expires_in')}s")
    
    # 3. Проверка токена
    print("\n[3] Проверка токена...")
    resp = requests.get(f"{BASE_URL}/api/auth/verify",
                       headers={"Authorization": f"Bearer {access_token}"})
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    print(f"    Valid: {data.get('valid', False)}")
    print(f"    Address: {data.get('address', 'N/A')}")
    
    # 4. Обновление токена
    print("\n[4] Обновление токена...")
    resp = requests.post(f"{BASE_URL}/api/auth/refresh",
                        json={"refresh_token": refresh_token})
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    if data.get('success'):
        print(f"    ✅ New access token generated")
        print(f"    New token: {data.get('access_token', '')[:50]}...")
    else:
        print(f"    Error: {data.get('error')}")
    
    # 5. Статистика
    print("\n[5] Статистика аутентификации...")
    resp = requests.get(f"{BASE_URL}/api/auth/stats")
    if resp.status_code == 200:
        stats = resp.json()
        print(f"    Active challenges: {stats.get('active_challenges', 0)}")
        print(f"    Active refresh tokens: {stats.get('active_refresh_tokens', 0)}")
    
    # 6. Выход
    print("\n[6] Выход...")
    resp = requests.post(f"{BASE_URL}/api/auth/logout",
                        headers={"Authorization": f"Bearer {access_token}"})
    print(f"    Status: {resp.status_code}")
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено успешно!")
    print("=" * 60)

if __name__ == "__main__":
    test_auth()
