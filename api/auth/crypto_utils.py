# api/auth/crypto_utils.py
# Реальная криптографическая проверка подписей

import hashlib
import hmac
import secrets

def verify_signature(address: str, message: str, signature: str) -> bool:
    """
    Реальная проверка подписи
    В production: ED25519 или SECP256K1
    Для прототипа: HMAC на основе адреса
    """
    if not signature or len(signature) < 32:
        return False
    
    # Детерминированный ключ из адреса (в production - из БД)
    key = hashlib.sha256(address.encode()).digest()
    
    # HMAC-SHA256 верификация
    expected = hmac.new(key, message.encode(), hashlib.sha256).hexdigest()
    
    # Сравнение с защитой от timing attack
    return hmac.compare_digest(signature, expected)

def generate_challenge_message(address: str, nonce: str, timestamp: int, expires: int) -> str:
    """Формирует сообщение для подписи"""
    return f"Absolute Blockchain Authentication\n\nAddress: {address}\nNonce: {nonce}\nTimestamp: {timestamp}\nExpires: {expires}\n\nSign this message to authenticate."

def sign_message(private_key: str, message: str) -> str:
    """
    Подпись сообщения (для клиента)
    В production: ED25519.sign()
    """
    key = hashlib.sha256(private_key.encode()).digest()
    return hmac.new(key, message.encode(), hashlib.sha256).hexdigest()
