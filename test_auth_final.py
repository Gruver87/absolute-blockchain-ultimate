# test_auth_final.py
# Финальное тестирование JWT аутентификации

import requests
import json

BASE_URL = "http://localhost:8080"

def test_auth():
    print("=" * 60)
    print("Финальное тестирование JWT аутентификации")
    print("=" * 60)
    
    results = {"success": 0, "failed": 0}
    
    # 1. Получение challenge
    print("\n[1] Получение challenge...")
    resp = requests.post(f"{BASE_URL}/api/auth/challenge", 
                         json={"address": "foundation"})
    print(f"    Status: {resp.status_code}")
    
    if resp.status_code != 200:
        print(f"    ❌ Ошибка: {resp.text}")
        results["failed"] += 1
        return
    
    data = resp.json()
    if not data.get('success'):
        print(f"    ❌ Ошибка: {data.get('error')}")
        results["failed"] += 1
        return
    
    nonce = data.get('nonce')
    print(f"    ✅ Nonce получен: {nonce[:32]}...")
    print(f"    Expires in: {data.get('expires_in')}s")
    results["success"] += 1
    
    # 2. Аутентификация
    print("\n[2] Аутентификация...")
    resp = requests.post(f"{BASE_URL}/api/auth/login",
                         json={
                             "address": "foundation",
                             "nonce": nonce,
                             "signature": "test_signature_for_jwt_auth"
                         })
    print(f"    Status: {resp.status_code}")
    
    if resp.status_code != 200:
        print(f"    ❌ Ошибка: {resp.text}")
        results["failed"] += 1
        return
    
    data = resp.json()
    if not data.get('success'):
        print(f"    ❌ Ошибка: {data.get('error')}")
        results["failed"] += 1
        return
    
    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    
    print(f"    ✅ Authenticated!")
    print(f"    Access token: {access_token[:50]}...")
    print(f"    Refresh token: {refresh_token[:50]}...")
    print(f"    Access expires in: {data.get('access_expires_in')}s")
    results["success"] += 1
    
    # 3. Проверка токена (теперь должен работать!)
    print("\n[3] Проверка токена...")
    resp = requests.get(f"{BASE_URL}/api/auth/verify",
                       headers={"Authorization": f"Bearer {access_token}"})
    print(f"    Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get('valid'):
            print(f"    ✅ Token valid: True")
            print(f"    Address: {data.get('address', 'N/A')}")
            results["success"] += 1
        else:
            print(f"    ❌ Token invalid: {data.get('error')}")
            results["failed"] += 1
    else:
        print(f"    ❌ Ошибка: {resp.text}")
        results["failed"] += 1
    
    # 4. Обновление токена
    print("\n[4] Обновление токена...")
    resp = requests.post(f"{BASE_URL}/api/auth/refresh",
                        json={"refresh_token": refresh_token})
    print(f"    Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        if data.get('success'):
            print(f"    ✅ New access token generated")
            print(f"    New token: {data.get('access_token', '')[:50]}...")
            results["success"] += 1
        else:
            print(f"    ❌ Ошибка: {data.get('error')}")
            results["failed"] += 1
    else:
        print(f"    ❌ Ошибка: {resp.text}")
        results["failed"] += 1
    
    # 5. Статистика
    print("\n[5] Статистика аутентификации...")
    resp = requests.get(f"{BASE_URL}/api/auth/stats")
    if resp.status_code == 200:
        stats = resp.json()
        print(f"    Active challenges: {stats.get('active_challenges', 0)}")
        print(f"    Active refresh tokens: {stats.get('active_refresh_tokens', 0)}")
        results["success"] += 1
    else:
        print(f"    ❌ Ошибка: {resp.text}")
        results["failed"] += 1
    
    # 6. Выход
    print("\n[6] Выход...")
    resp = requests.post(f"{BASE_URL}/api/auth/logout",
                        headers={"Authorization": f"Bearer {access_token}"})
    print(f"    Status: {resp.status_code}")
    
    if resp.status_code == 200:
        print(f"    ✅ Logout successful")
        results["success"] += 1
    else:
        print(f"    ❌ Ошибка: {resp.text}")
        results["failed"] += 1
    
    # 7. Проверка после выхода
    print("\n[7] Проверка после выхода...")
    resp = requests.get(f"{BASE_URL}/api/auth/verify",
                       headers={"Authorization": f"Bearer {access_token}"})
    print(f"    Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        if not data.get('valid'):
            print(f"    ✅ Token invalid as expected")
            results["success"] += 1
        else:
            print(f"    ❌ Token still valid!")
            results["failed"] += 1
    else:
        print(f"    ⚠️ Could not verify after logout")
    
    # Итоги
    print("\n" + "=" * 60)
    print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"   ✅ Успешно: {results['success']}")
    print(f"   ❌ Ошибок: {results['failed']}")
    
    if results['failed'] == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("\n⚠️ Есть ошибки, требуется проверка")
    
    print("=" * 60)

if __name__ == "__main__":
    test_auth()
