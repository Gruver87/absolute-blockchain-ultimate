# api/auth_get_patch.py
# Патч для добавления GET эндпоинтов в API

def patch_api_get_endpoints(server_instance):
    """Добавляет auth GET эндпоинты в API сервер"""
    
    if not hasattr(server_instance, 'RequestHandlerClass'):
        return False
    
    handler_class = server_instance.RequestHandlerClass
    original_do_GET = handler_class.do_GET
    
    def patched_do_GET(self):
        path = self.path
        
        # Auth GET эндпоинты
        if path == '/api/auth/verify':
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
            return
        
        if path == '/api/auth/stats':
            try:
                from api.auth.jwt_handler import jwt_auth
                self._send_json(jwt_auth.get_stats())
            except Exception as e:
                self._send_json({'success': False, 'error': str(e)})
            return
        
        # Для всех остальных - оригинальный обработчик
        original_do_GET(self)
    
    handler_class.do_GET = patched_do_GET
    print("✅ Auth GET endpoints patched successfully")
    return True
