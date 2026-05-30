# api/auth/jwt_handler.py
import jwt
import time
import secrets
from typing import Dict, Optional
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from api.auth.crypto_utils import verify_signature, generate_challenge_message

load_dotenv()

@dataclass
class TokenPair:
    access_token: str
    refresh_token: str
    access_expires_in: int
    refresh_expires_in: int
    token_type: str = "Bearer"

class JWTAuthenticator:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET', 'absolute_blockchain_super_secret_key_2025')
        self.algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        self.access_expire_minutes = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 15))
        self.refresh_expire_days = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_DAYS', 7))
        
        self._blacklist: Dict[str, float] = {}
        self._refresh_tokens: Dict[str, dict] = {}
        self._challenges: Dict[str, dict] = {}
        self._stats = {'challenges_created': 0, 'tokens_issued': 0}
    
    def create_challenge(self, address: str) -> dict:
        nonce = secrets.token_hex(32)
        expires_at = time.time() + 300
        timestamp = int(time.time())
        
        self._challenges[address] = {
            'nonce': nonce,
            'expires_at': expires_at,
            'timestamp': timestamp,
            'created_at': time.time()
        }
        self._stats['challenges_created'] += 1
        
        message = generate_challenge_message(address, nonce, timestamp, int(expires_at))
        
        return {
            'nonce': nonce,
            'message': message,
            'expires_in': 300
        }
    
    def verify_challenge(self, address: str, nonce: str, signature: str) -> bool:
        challenge = self._challenges.get(address)
        if not challenge:
            return False
        
        if challenge['nonce'] != nonce:
            return False
        
        if time.time() > challenge['expires_at']:
            if address in self._challenges:
                del self._challenges[address]
            return False
        
        # Реальная проверка подписи
        message = generate_challenge_message(
            address, 
            nonce, 
            challenge['timestamp'], 
            int(challenge['expires_at'])
        )
        
        if not verify_signature(address, message, signature):
            return False
        
        if address in self._challenges:
            del self._challenges[address]
        
        return True
    
    def generate_tokens(self, address: str, role: str = "user") -> TokenPair:
        now = int(time.time())
        
        access_payload = {
            'sub': address,
            'role': role,
            'type': 'access',
            'iat': now,
            'exp': now + (self.access_expire_minutes * 60),
            'jti': secrets.token_hex(16)
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)
        
        refresh_payload = {
            'sub': address,
            'type': 'refresh',
            'iat': now,
            'exp': now + (self.refresh_expire_days * 24 * 3600),
            'jti': secrets.token_hex(16)
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)
        
        self._refresh_tokens[refresh_token] = {
            'address': address,
            'role': role,
            'created_at': now,
            'expires_at': refresh_payload['exp']
        }
        self._stats['tokens_issued'] += 1
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires_in=self.access_expire_minutes * 60,
            refresh_expires_in=self.refresh_expire_days * 24 * 3600
        )
    
    def verify_access_token(self, token: str) -> Optional[dict]:
        try:
            if token in self._blacklist:
                return None
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get('type') != 'access':
                return None
            return payload
        except:
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[TokenPair]:
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=[self.algorithm])
            if payload.get('type') != 'refresh':
                return None
            address = payload.get('sub')
            if refresh_token not in self._refresh_tokens:
                return None
            role = self._refresh_tokens[refresh_token].get('role', 'user')
            return self.generate_tokens(address, role)
        except:
            return None
    
    def revoke_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={'verify_exp': False})
            expires_at = payload.get('exp', time.time() + 3600)
            self._blacklist[token] = expires_at
            if payload.get('type') == 'refresh' and token in self._refresh_tokens:
                del self._refresh_tokens[token]
            return True
        except:
            return False
    
    def get_user_from_token(self, token: str) -> Optional[str]:
        payload = self.verify_access_token(token)
        return payload.get('sub') if payload else None
    
    def get_stats(self) -> dict:
        return {
            'active_challenges': len(self._challenges),
            'active_refresh_tokens': len(self._refresh_tokens),
            'blacklist_size': len(self._blacklist),
            'challenges_created': self._stats['challenges_created'],
            'tokens_issued': self._stats['tokens_issued']
        }

jwt_auth = JWTAuthenticator()
