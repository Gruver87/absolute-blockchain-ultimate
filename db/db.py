# db/db.py
import json
import os
import threading
from typing import Any, Optional, List, Dict

class Database:
    """Persistent storage with backward compatibility"""
    
    def __init__(self, path: str = "chain_data.json"):
        self.path = path
        self._lock = threading.RLock()
        self._cache = self._load()
    
    def _load(self) -> dict:
        if not os.path.exists(self.path):
            return {"blocks": [], "state": {}, "receipts": [], "peers": []}
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except:
            return {"blocks": [], "state": {}, "receipts": [], "peers": []}
    
    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self._cache, f, indent=2)
    
    def put(self, key: str, value: Any):
        with self._lock:
            self._cache[key] = value
            self._save()
    
    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._cache.get(key, default)
    
    # ----- Block methods (primary interface) -----
    def add_block(self, block: Dict) -> None:
        """Add block to chain (primary)"""
        with self._lock:
            self._cache["blocks"].append(block)
            self._save()
    
    def put_block(self, block: Dict) -> None:
        """Backward compatibility alias for add_block"""
        self.add_block(block)
    
    def get_blocks(self) -> List[Dict]:
        return self.get("blocks", [])
    
    def get_last_block(self) -> Optional[Dict]:
        blocks = self.get_blocks()
        return blocks[-1] if blocks else None
    
    def get_block_by_number(self, number: int) -> Optional[Dict]:
        blocks = self.get_blocks()
        if number < len(blocks):
            return blocks[number]
        return None
    
    def get_block_by_hash(self, block_hash: str) -> Optional[Dict]:
        for block in self.get_blocks():
            if block.get("hash") == block_hash:
                return block
        return None
    
    # ----- State methods -----
    def put_state(self, state_root: str, state_data: Dict):
        with self._lock:
            self._cache["state"][state_root] = state_data
            self._save()
    
    def get_state(self, state_root: str) -> Optional[Dict]:
        return self.get("state", {}).get(state_root)
    
    # ----- Receipt methods -----
    def add_receipt(self, receipt: Dict):
        with self._lock:
            self._cache["receipts"].append(receipt)
            self._save()
    
    def get_receipts(self) -> List[Dict]:
        return self.get("receipts", [])
    
    # ----- Peer methods -----
    def add_peer(self, peer: str):
        with self._lock:
            if peer not in self._cache["peers"]:
                self._cache["peers"].append(peer)
                self._save()
    
    def get_peers(self) -> List[str]:
        return self.get("peers", [])
    
    # ----- Chain info -----
    def get_chain_length(self) -> int:
        return len(self.get_blocks())
    
    def clear(self):
        with self._lock:
            self._cache = {"blocks": [], "state": {}, "receipts": [], "peers": []}
            self._save()
