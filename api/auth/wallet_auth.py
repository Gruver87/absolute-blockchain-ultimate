# api/auth/wallet_auth.py
import secrets
import time

class WalletAuthenticator:
    def __init__(self):
        self.challenges = {}
    
    def create_challenge(self, address):
        nonce = secrets.token_hex(32)
        self.challenges[address] = {
            'nonce': nonce, 
            'expires': time.time() + 300
        }
        message = f"Absolute Blockchain Login\nAddress: {address}\nNonce: {nonce}\nExpires: {time.time() + 300}"
        return {'nonce': nonce, 'message': message}
    
    def authenticate(self, address, signature):
        if address not in self.challenges:
            return False, "No active challenge. Request /api/auth/challenge first"
        if time.time() > self.challenges[address]['expires']:
            del self.challenges[address]
            return False, "Challenge expired"
        # В production здесь проверка подписи
        del self.challenges[address]
        return True, "OK"

wallet_auth = WalletAuthenticator()
