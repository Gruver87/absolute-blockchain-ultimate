# core/state_trie.py
import hashlib
import threading
from typing import Dict, Any, Optional

class StateTrie:
    def __init__(self):
        self._state: Dict[str, Dict] = {}
        self._lock = threading.RLock()

    def _hash(self, key: str, value: Any) -> str:
        return hashlib.sha256(f"{key}:{value}".encode()).hexdigest()

    def set(self, key: str, value: Any):
        with self._lock:
            self._state[key] = {
                "value": value,
                "hash": self._hash(key, value)
            }

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._state.get(key)
            return entry["value"] if entry else None

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._state:
                del self._state[key]
                return True
            return False

    def root_hash(self) -> str:
        with self._lock:
            if not self._state:
                return hashlib.sha256(b"empty").hexdigest()
            combined = "".join(v["hash"] for v in self._state.values())
            return hashlib.sha256(combined.encode()).hexdigest()

    def get_all(self) -> Dict:
        with self._lock:
            return {k: v["value"] for k, v in self._state.items()}
