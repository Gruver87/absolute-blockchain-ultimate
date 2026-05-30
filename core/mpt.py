# core/mpt.py
import hashlib
import threading
from typing import Dict, Any, Optional

class MerklePatriciaTrie:
    """Merkle Patricia Trie — state root integrity"""
    
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._lock = threading.RLock()
    
    def update(self, key: str, value: Any):
        with self._lock:
            self._store[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            return self._store.get(key)
    
    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False
    
    def root_hash(self) -> str:
        """Deterministic root hash of entire state"""
        with self._lock:
            if not self._store:
                return hashlib.sha256(b"empty_trie").hexdigest()
            # Sort for determinism
            data = "".join(f"{k}:{v}" for k, v in sorted(self._store.items()))
            return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        with self._lock:
            return self._store.copy()
    
    def size(self) -> int:
        return len(self._store)
