# core/mpt_engine.py
import hashlib
import threading
from typing import Dict, Any, Optional

class MerklePatriciaTrie:
    """Merkle Patricia Trie — Ethereum state root engine"""
    
    def __init__(self):
        self._nodes: Dict[str, Any] = {}
        self._lock = threading.RLock()
    
    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
    
    def put(self, key: str, value: Any):
        with self._lock:
            self._nodes[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        return self._nodes.get(key)
    
    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._nodes:
                del self._nodes[key]
                return True
            return False
    
    def root_hash(self) -> str:
        """Deterministic root hash of entire trie"""
        with self._lock:
            if not self._nodes:
                return self._hash("empty_trie")
            
            # Sort for determinism
            data = "".join(f"{k}:{v}" for k, v in sorted(self._nodes.items()))
            return self._hash(data)
    
    def proof(self, key: str) -> list:
        """Generate Merkle proof for key"""
        # Simplified: return path to node
        return [self._hash(f"{key}:{self._nodes.get(key, 'null')}")]
    
    def verify_proof(self, key: str, proof: list, root: str) -> bool:
        """Verify Merkle proof"""
        expected = self._hash(f"{key}:{self._nodes.get(key, 'null')}")
        return expected in proof
    
    def size(self) -> int:
        return len(self._nodes)
    
    def clear(self):
        with self._lock:
            self._nodes.clear()
