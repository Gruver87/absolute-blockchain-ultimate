# state/state.py
import hashlib
from typing import Dict, Any

class Account:
    """Mutable account object — changes persist in state"""
    def __init__(self):
        self.balance = 0
        self.nonce = 0
        self.storage: Dict[str, Any] = {}
    
    def to_dict(self) -> dict:
        return {
            "balance": self.balance,
            "nonce": self.nonce,
            "storage": self.storage
        }

class State:
    """State management — always returns mutable references"""
    
    def __init__(self):
        self._accounts: Dict[str, Account] = {}
    
    def get(self, address: str) -> Account:
        """
        CRITICAL: Returns mutable reference to account.
        Any modifications to returned object will persist.
        """
        if address not in self._accounts:
            self._accounts[address] = Account()
        return self._accounts[address]
    
    def get_balance(self, address: str) -> int:
        return self.get(address).balance
    
    def set_balance(self, address: str, balance: int):
        self.get(address).balance = balance
    
    def get_nonce(self, address: str) -> int:
        return self.get(address).nonce
    
    def set_nonce(self, address: str, nonce: int):
        self.get(address).nonce = nonce
    
    def increment_nonce(self, address: str):
        self.get(address).nonce += 1
    
    def root(self) -> str:
        """Calculate state root hash"""
        if not self._accounts:
            return hashlib.sha256(b"empty_state").hexdigest()
        
        # Deterministic ordering
        data = "".join(
            f"{addr}:{acc.balance}:{acc.nonce}"
            for addr, acc in sorted(self._accounts.items())
        )
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        return {addr: acc.to_dict() for addr, acc in self._accounts.items()}
    
    def clear(self):
        self._accounts.clear()
