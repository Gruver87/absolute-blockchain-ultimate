# geth_state/state.py
import hashlib
import threading
from typing import Dict, Any, Optional

class Account:
    """Ethereum account model"""
    def __init__(self):
        self.balance = 0
        self.nonce = 0
        self.code_hash = None
        self.storage_root = None
    
    def to_dict(self) -> dict:
        return {
            "balance": self.balance,
            "nonce": self.nonce,
            "code_hash": self.code_hash,
            "storage_root": self.storage_root
        }

class StateDB:
    """State database with Merkle Patricia Trie"""
    
    def __init__(self, db):
        self.db = db
        self._accounts: Dict[str, Account] = {}
        self._lock = threading.RLock()
    
    def get_account(self, address: str) -> Account:
        with self._lock:
            if address not in self._accounts:
                self._accounts[address] = Account()
            return self._accounts[address]
    
    def get_balance(self, address: str) -> int:
        return self.get_account(address).balance
    
    def set_balance(self, address: str, balance: int):
        self.get_account(address).balance = balance
    
    def get_nonce(self, address: str) -> int:
        return self.get_account(address).nonce
    
    def increment_nonce(self, address: str):
        self.get_account(address).nonce += 1
    
    def root_hash(self) -> str:
        """Compute state root hash (Merkle Patricia Trie)"""
        with self._lock:
            if not self._accounts:
                return hashlib.sha256(b"empty_state").hexdigest()
            
            # Build trie structure
            data = "".join(
                f"{addr}:{acc.balance}:{acc.nonce}"
                for addr, acc in sorted(self._accounts.items())
            )
            return hashlib.sha256(data.encode()).hexdigest()
    
    def commit(self):
        """Commit state to persistent storage"""
        root = self.root_hash()
        state_data = {addr: acc.to_dict() for addr, acc in self._accounts.items()}
        self.db.put_state_root(root, state_data)
        return root
    
    def clear(self):
        with self._lock:
            self._accounts.clear()
