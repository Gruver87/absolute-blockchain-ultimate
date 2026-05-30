# geth_state/hardening.py
import hashlib
import threading
from typing import Dict, Any, Optional

class ConsistentState:
    """State with deterministic execution and root hash verification"""
    
    def __init__(self):
        self._accounts: Dict[str, Dict] = {}
        self._lock = threading.RLock()
        self._last_root = None
    
    def get_account(self, address: str) -> Dict:
        with self._lock:
            if address not in self._accounts:
                self._accounts[address] = {"balance": 0, "nonce": 0}
            return self._accounts[address]
    
    def set_balance(self, address: str, balance: int):
        self.get_account(address)["balance"] = balance
    
    def increment_nonce(self, address: str):
        self.get_account(address)["nonce"] += 1
    
    def root_hash(self) -> str:
        """Deterministic root hash — must be identical across all nodes"""
        with self._lock:
            data = "".join(
                f"{addr}:{acc['balance']}:{acc['nonce']}"
                for addr, acc in sorted(self._accounts.items())
            )
            return hashlib.sha256(data.encode()).hexdigest()
    
    def verify_root(self, expected_root: str) -> bool:
        """Verify that current state matches expected root"""
        current = self.root_hash()
        return current == expected_root
    
    def snapshot(self) -> Dict:
        """Create state snapshot for recovery"""
        with self._lock:
            return {
                "accounts": self._accounts.copy(),
                "root": self.root_hash(),
                "timestamp": __import__("time").time()
            }
    
    def restore(self, snapshot: Dict):
        """Restore state from snapshot"""
        with self._lock:
            self._accounts = snapshot["accounts"].copy()
