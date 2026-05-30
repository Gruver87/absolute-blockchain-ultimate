# api/auth_routes.py
# Дополнительные auth эндпоинты для API

def setup_auth_routes(handler):
    """Добавляет auth эндпоинты в API handler"""
    
    # Сохраняем оригинальный do_POST
    original_do_POST = handler.do_POST
    
    def new_do_POST(self):
        path = self.path
        
        # Обработка auth эндпоинтов
        if path == '/api/auth/challenge':
            import json
            from api.auth.wallet_auth import wallet_auth
            
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b'{}'
            data = json.loads(body.decode('utf-8'))
            address = data.get('address')
            
            if not address:
                self._send_json({'success': False, 'error': 'Address required'}, 400)
                return
            
            challenge = wallet_auth.create_challenge(address)
            self._send_json({
                'success': True,
                'nonce': challenge['nonce'],
                'message': challenge['message']
            })
            return
        
        elif path == '/api/auth/login':
            import json
            from api.auth.wallet_auth import wallet_auth
            
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else b'{}'
            data = json.loads(body.decode('utf-8'))
            address = data.get('address')
            signature = data.get('signature')
            
            if not address or not signature:
                self._send_json({'success': False, 'error': 'Address and signature required'}, 400)
                return
            
            success, msg = wallet_auth.authenticate(address, signature)
            if not success:
                self._send_json({'success': False, 'error': msg}, 401)
                return
            
            self._send_json({
                'success': True,
                'message': 'Authentication successful',
                'address': address
            })
            return
        
        # Для всех остальных эндпоинтов вызываем оригинальный обработчик
        original_do_POST(self)
    
    # Заменяем метод
    handler.do_POST = new_do_POST
    return handler
