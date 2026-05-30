# core/db.py
import json
import os
import threading
from typing import Any, Optional

class Database:
    """Persistent storage engine (LevelDB-like)"""
    
    def __init__(self, path: str = "chain_data.json"):
        self.path = path
        self._lock = threading.RLock()
        self._data = self._load()
    
    def _load(self) -> dict:
        if not os.path.exists(self.path):
            return {"chain": [], "state": {}, "receipts": [], "peers": []}
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {"chain": [], "state": {}, "receipts": [], "peers": []}
    
    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=2)
    
    def put(self, key: str, value: Any):
        with self._lock:
            self._data[key] = value
            self._save()
    
    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._data.get(key, default)
    
    def append_block(self, block: dict):
        with self._lock:
            self._data["chain"].append(block)
            self._save()
    
    def get_chain(self) -> list:
        return self.get("chain", [])
    
    def get_last_block(self) -> Optional[dict]:
        chain = self.get_chain()
        return chain[-1] if chain else None
