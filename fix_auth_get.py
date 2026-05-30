# fix_auth_get.py
# Запустите этот скрипт после запуска блокчейна

import urllib.request
import json
import time

def add_auth_get_endpoints():
    """Добавляет GET эндпоинты для аутентификации"""
    
    # Проверяем, доступен ли API
    try:
        urllib.request.urlopen("http://localhost:8080/api/stats", timeout=2)
    except:
        print("❌ Блокчейн не запущен на порту 8080")
        print("   Запустите блокчейн: python ABSOLUTE_FINAL_FIXED.py")
        return False
    
    # Тестовый запрос к /api/auth/verify (должен вернуть 404 сейчас)
    req = urllib.request.Request("http://localhost:8080/api/auth/verify")
    try:
        urllib.request.urlopen(req)
        print("✅ Эндпоинт /api/auth/verify уже работает!")
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("⚠️ Эндпоинт /api/auth/verify не найден, добавляем...")
        else:
            print(f"⚠️ Ошибка: {e.code}")
    
    # Создаём HTTP-запрос к специальному эндпоинту для динамического обновления
    # (если мы добавим такой эндпоинт в код)
    
    print("""
================================================================
    ИНСТРУКЦИЯ ДЛЯ РУЧНОГО ДОБАВЛЕНИЯ:
================================================================

1. Откройте файл: ABSOLUTE_FINAL_FIXED.py

2. Найдите строку:    def do_GET(self):

3. Найдите последний 'elif' перед 'else:' и добавьте ЭТОТ КОД:

            elif path == '/api/auth/verify':
                try:
                    from api.auth.jwt_handler import jwt_auth
                    auth_header = self.headers.get('Authorization', '')
                    if not auth_header.startswith('Bearer '):
                        self._send_json({'success': False, 'error': 'No token provided'})
                        return
                    token = auth_header[7:]
                    user = jwt_auth.get_user_from_token(token)
                    if user:
                        self._send_json({'success': True, 'valid': True, 'address': user})
                    else:
                        self._send_json({'success': False, 'valid': False, 'error': 'Invalid token'})
                except Exception as e:
                    self._send_json({'success': False, 'error': str(e)})

            elif path == '/api/auth/stats':
                try:
                    from api.auth.jwt_handler import jwt_auth
                    self._send_json(jwt_auth.get_stats())
                except Exception as e:
                    self._send_json({'success': False, 'error': str(e)})

4. Сохраните файл (Ctrl+S)

5. Перезапустите блокчейн: Ctrl+C, затем python ABSOLUTE_FINAL_FIXED.py

================================================================
""")
    return False

if __name__ == "__main__":
    add_auth_get_endpoints()
