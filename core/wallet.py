# core/wallet.py
import hashlib
import ecdsa
import secrets

class Wallet:
    def __init__(self, private_key_hex=None):
        if private_key_hex:
            self.private_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
        else:
            self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def get_address(self):
        pub = self.public_key.to_string()
        return hashlib.sha256(pub).hexdigest()

    def get_private_key_hex(self):
        return self.private_key.to_string().hex()

    def get_public_key_hex(self):
        return self.public_key.to_string().hex()

    def sign(self, data: str) -> str:
        return self.private_key.sign(data.encode()).hex()

    @staticmethod
    def verify(public_key_hex: str, signature_hex: str, data: str) -> bool:
        try:
            vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1)
            return vk.verify(bytes.fromhex(signature_hex), data.encode())
        except:
            return False

    def to_dict(self):
        return {
            'address': self.get_address(),
            'public_key': self.get_public_key_hex(),
            'private_key': self.get_private_key_hex()
        }

    @staticmethod
    def generate():
        return Wallet()

    @staticmethod
    def from_private_key(private_key_hex):
        return Wallet(private_key_hex)
