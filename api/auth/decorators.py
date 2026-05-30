# api/auth/decorators.py
# Декораторы для защиты API эндпоинтов

from functools import wraps
from api.auth.jwt_handler import jwt_auth

def require_auth(func):
    """Декоратор: требует валидный JWT токен"""
    @wraps(func)
    def wrapper(self, data=None):
        # Получаем токен из заголовка
        auth_header = self.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            self._send_json({
                'success': False,
                'error': 'Missing or invalid authorization header. Use: Bearer <token>'
            }, 401)
            return None
        
        token = auth_header[7:]  # Убираем 'Bearer '
        
        # Проверяем токен
        user = jwt_auth.get_user_from_token(token)
        if not user:
            self._send_json({
                'success': False,
                'error': 'Invalid or expired token'
            }, 401)
            return None
        
        # Добавляем пользователя в контекст
        self.auth_user = user
        return func(self, data)
    return wrapper

def optional_auth(func):
    """Декоратор: опциональная аутентификация"""
    @wraps(func)
    def wrapper(self, data=None):
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            user = jwt_auth.get_user_from_token(token)
            if user:
                self.auth_user = user
        return func(self, data)
    return wrapper
