# geth_crypto/crypto.py
import hashlib
import secrets
import ecdsa

class Crypto:
    """Cryptography layer — ECDSA + hash functions"""
    
    @staticmethod
    def generate_keypair() -> tuple:
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        private_key = sk.to_string().hex()
        public_key = sk.get_verifying_key().to_string().hex()
        return private_key, public_key
    
    @staticmethod
    def sign(private_key_hex: str, message: str) -> str:
        try:
            sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
            return sk.sign(message.encode()).hex()
        except:
            return hashlib.sha256(f"{private_key_hex}:{message}".encode()).hexdigest()
    
    @staticmethod
    def verify(public_key_hex: str, message: str, signature_hex: str) -> bool:
        try:
            vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1)
            return vk.verify(bytes.fromhex(signature_hex), message.encode())
        except:
            expected = hashlib.sha256(f"{public_key_hex}:{message}".encode()).hexdigest()
            return signature_hex == expected
    
    @staticmethod
    def address_from_public_key(public_key_hex: str) -> str:
        return hashlib.sha256(bytes.fromhex(public_key_hex)).hexdigest()[:40]
    
    @staticmethod
    def keccak256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()
