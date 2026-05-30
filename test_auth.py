# test_auth.py
# Тестирование JWT аутентификации

import requests
import json
import time

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
    print(f"    Nonce: {data.get('nonce', 'N/A')[:32]}...")
    print(f"    Success: {data.get('success', False)}")
    
    nonce = data.get('nonce')
    
    if not nonce:
        print("    ❌ Не удалось получить nonce")
        return
    
    # 2. Аутентификация
    print("\n[2] Аутентификация...")
    resp = requests.post(f"{BASE_URL}/api/auth/login",
                         json={
                             "address": "foundation",
                             "nonce": nonce,
                             "signature": "test_signature_64_chars_long_for_demo_purpose_only"
                         })
    print(f"    Status: {resp.status_code}")
    data = resp.json()
    
    if resp.status_code == 200 and data.get('success'):
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')
        
        print(f"    ✅ Authenticated!")
        
        if access_token:
            print(f"    Access token: {access_token[:50]}...")
            print(f"    Expires in: {data.get('access_expires_in', 'N/A')}s")
        else:
            print(f"    ⚠️ No access_token in response")
            print(f"    Response data: {data}")
            return
        
        # 3. Проверка токена
        print("\n[3] Проверка токена...")
        resp = requests.get(f"{BASE_URL}/api/auth/verify",
                           headers={"Authorization": f"Bearer {access_token}"})
        print(f"    Status: {resp.status_code}")
        if resp.status_code == 200:
            verify_data = resp.json()
            print(f"    Valid: {verify_data.get('valid', False)}")
            print(f"    Address: {verify_data.get('address', 'N/A')}")
        
        # 4. Обновление токена
        if refresh_token:
            print("\n[4] Обновление токена...")
            resp = requests.post(f"{BASE_URL}/api/auth/refresh",
                                json={"refresh_token": refresh_token})
            print(f"    Status: {resp.status_code}")
            if resp.status_code == 200:
                refresh_data = resp.json()
                if refresh_data.get('success'):
                    print(f"    ✅ New access token generated")
                else:
                    print(f"    ⚠️ Refresh failed: {refresh_data}")
        
        # 5. Выход
        print("\n[5] Выход...")
        resp = requests.post(f"{BASE_URL}/api/auth/logout",
                            headers={"Authorization": f"Bearer {access_token}"})
        print(f"    Status: {resp.status_code}")
        
    else:
        print(f"    ❌ Authentication failed")
        print(f"    Response: {data}")
    
    # 6. Статистика
    print("\n[6] Статистика аутентификации...")
    resp = requests.get(f"{BASE_URL}/api/auth/stats")
    if resp.status_code == 200:
        stats = resp.json()
        print(f"    Active challenges: {stats.get('active_challenges', 0)}")
        print(f"    Active refresh tokens: {stats.get('active_refresh_tokens', 0)}")
    
    print("\n" + "=" * 60)
    print("Тестирование завершено!")
    print("=" * 60)

if __name__ == "__main__":
    test_auth()
