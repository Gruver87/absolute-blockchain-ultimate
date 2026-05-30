# dynamic_patch.py
# Запустите этот скрипт, когда блокчейн уже работает

import sys
import inspect
import importlib

print("=" * 50)
print("ДИНАМИЧЕСКОЕ ДОБАВЛЕНИЕ ЭНДПОИНТОВ")
print("=" * 50)

# Находим модуль ABSOLUTE_FINAL_FIXED
try:
    # Пытаемся найти APIHandler в загруженных модулях
    for name, module in sys.modules.items():
        if hasattr(module, 'APIHandler'):
            handler_class = module.APIHandler
            print(f"✅ Найден APIHandler в модуле: {name}")
            break
    else:
        print("❌ APIHandler не найден в загруженных модулях")
        print("   Убедитесь, что блокчейн запущен")
        sys.exit(1)
    
    # Сохраняем оригинальный do_GET
    original_do_GET = handler_class.do_GET
    
    # Создаём новый do_GET с дополнительными эндпоинтами
    def new_do_GET(self):
        path = self.path
        
        # Новые эндпоинты
        if path == '/api/health':
            import json
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'status': 'healthy',
                'version': '15.2',
                'network': 'Absolute Blockchain'
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        if path == '/api/auth/stats':
            try:
                from api.auth.jwt_handler import jwt_auth
                import json
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                stats = jwt_auth.get_stats()
                response = {
                    'success': True,
                    'active_sessions': stats.get('active_refresh_tokens', 0),
                    'active_challenges': stats.get('active_challenges', 0),
                    'blacklist_size': stats.get('blacklist_size', 0)
                }
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
            return
        
        if path == '/api/auth/verify':
            try:
                from api.auth.jwt_handler import jwt_auth
                import json
                auth_header = self.headers.get('Authorization', '')
                if not auth_header.startswith('Bearer '):
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'error': 'No token provided'}
                    self.wfile.write(json.dumps(response).encode())
                    return
                token = auth_header[7:]
                user = jwt_auth.get_user_from_token(token)
                if user:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {'success': True, 'valid': True, 'address': user}
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'valid': False, 'error': 'Invalid token'}
                    self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
            return
        
        # Для всех остальных - оригинальный обработчик
        original_do_GET(self)
    
    # Применяем патч
    handler_class.do_GET = new_do_GET
    print("✅ Эндпоинты динамически добавлены!")
    print("   - /api/health")
    print("   - /api/auth/stats")
    print("   - /api/auth/verify")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50)
