# api/auth_patch.py
# Автоматически добавляет auth эндпоинты в API

import sys
import types

def apply_auth_patch(server_instance):
    """Применяет патч к API серверу"""
    
    if not hasattr(server_instance, 'RequestHandlerClass'):
        return
    
    handler_class = server_instance.RequestHandlerClass
    
    # Сохраняем оригинальный do_POST
    original_do_POST = handler_class.do_POST
    
    def patched_do_POST(self):
        path = self.path
        
        # Auth эндпоинты
        if path == '/api/auth/challenge':
            try:
                from api.auth.wallet_auth import wallet_auth
                import json
                cl = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(cl) if cl > 0 else b'{}'
                data = json.loads(body.decode('utf-8'))
                addr = data.get('address')
                if not addr:
                    self._send_json({'success': False, 'error': 'Address required'}, 400)
                    return
                ch = wallet_auth.create_challenge(addr)
                self._send_json({'success': True, 'nonce': ch['nonce'], 'message': ch['message']})
            except Exception as e:
                self._send_json({'success': False, 'error': str(e)}, 500)
            return
        
        if path == '/api/auth/login':
            try:
                from api.auth.wallet_auth import wallet_auth
                import json
                cl = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(cl) if cl > 0 else b'{}'
                data = json.loads(body.decode('utf-8'))
                addr = data.get('address')
                sig = data.get('signature')
                if not addr or not sig:
                    self._send_json({'success': False, 'error': 'Address and signature required'}, 400)
                    return
                ok, msg = wallet_auth.authenticate(addr, sig)
                if not ok:
                    self._send_json({'success': False, 'error': msg}, 401)
                    return
                self._send_json({'success': True, 'message': 'Authenticated', 'address': addr})
            except Exception as e:
                self._send_json({'success': False, 'error': str(e)}, 500)
            return
        
        # Для всех остальных - оригинальный обработчик
        original_do_POST(self)
    
    # Применяем патч
    handler_class.do_POST = patched_do_POST
    print("✅ Auth patch applied successfully")
