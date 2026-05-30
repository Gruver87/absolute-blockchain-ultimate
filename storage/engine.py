# storage/engine.py
import json
import os
import threading
from typing import Dict, List, Any, Optional

class StorageEngine:
    """Persistent storage engine (RocksDB/LevelDB style)"""
    
    def __init__(self, path: str = "storage"):
        self.path = path
        self._lock = threading.RLock()
        
        # Create storage directory
        os.makedirs(path, exist_ok=True)
        
        # Sub-stores
        self._blocks = self._load_store("blocks.json")
        self._state = self._load_store("state.json")
        self._receipts = self._load_store("receipts.json")
        self._peers = self._load_store("peers.json")
    
    def _load_store(self, name: str) -> dict:
        filepath = os.path.join(self.path, name)
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_store(self, name: str, data: dict):
        filepath = os.path.join(self.path, name)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    
    # Block storage
    def put_block(self, block: Dict):
        with self._lock:
            block_number = block.get("number")
            if block_number is not None:
                self._blocks[str(block_number)] = block
                self._save_store("blocks.json", self._blocks)
    
    def get_block(self, number: int) -> Optional[Dict]:
        return self._blocks.get(str(number))
    
    def get_last_block(self) -> Optional[Dict]:
        if not self._blocks:
            return None
        max_key = max(int(k) for k in self._blocks.keys())
        return self._blocks[str(max_key)]
    
    def get_all_blocks(self) -> List[Dict]:
        return [self._blocks[k] for k in sorted(self._blocks.keys(), key=int)]
    
    # State storage
    def put_state(self, state_root: str, state_data: Dict):
        with self._lock:
            self._state[state_root] = state_data
            self._save_store("state.json", self._state)
    
    def get_state(self, state_root: str) -> Optional[Dict]:
        return self._state.get(state_root)
    
    # Receipt storage
    def put_receipt(self, tx_hash: str, receipt: Dict):
        with self._lock:
            self._receipts[tx_hash] = receipt
            self._save_store("receipts.json", self._receipts)
    
    def get_receipt(self, tx_hash: str) -> Optional[Dict]:
        return self._receipts.get(tx_hash)
    
    # Peer storage
    def add_peer(self, peer: str):
        with self._lock:
            if peer not in self._peers:
                self._peers[peer] = {"added_at": __import__("time").time()}
                self._save_store("peers.json", self._peers)
    
    def get_peers(self) -> List[str]:
        return list(self._peers.keys())
    
    # Stats
    def get_stats(self) -> Dict:
        return {
            "blocks": len(self._blocks),
            "state_roots": len(self._state),
            "receipts": len(self._receipts),
            "peers": len(self._peers)
        }
