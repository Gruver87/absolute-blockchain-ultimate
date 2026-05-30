# geth_db/db.py
import json
import os
import threading
from typing import Dict, Any, Optional, List

class Database:
    """Production-grade persistent storage (LevelDB/RocksDB style)"""
    
    def __init__(self, path: str = "geth_data"):
        self.path = path
        self._lock = threading.RLock()
        os.makedirs(path, exist_ok=True)
        
        # Separate stores for different data types
        self._blocks = self._load_store("blocks.json")
        self._headers = self._load_store("headers.json")
        self._receipts = self._load_store("receipts.json")
        self._trie_nodes = self._load_store("trie_nodes.json")
        self._state = self._load_store("state.json")
    
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
    def put_block(self, number: int, block: Dict):
        with self._lock:
            self._blocks[str(number)] = block
            self._save_store("blocks.json", self._blocks)
    
    def get_block(self, number: int) -> Optional[Dict]:
        return self._blocks.get(str(number))
    
    def get_last_block(self) -> Optional[Dict]:
        if not self._blocks:
            return None
        max_num = max(int(k) for k in self._blocks.keys())
        return self._blocks[str(max_num)]
    
    def get_all_blocks(self) -> List[Dict]:
        return [self._blocks[k] for k in sorted(self._blocks.keys(), key=int)]
    
    # Header storage
    def put_header(self, number: int, header: Dict):
        with self._lock:
            self._headers[str(number)] = header
            self._save_store("headers.json", self._headers)
    
    def get_header(self, number: int) -> Optional[Dict]:
        return self._headers.get(str(number))
    
    # Receipt storage
    def put_receipt(self, tx_hash: str, receipt: Dict):
        with self._lock:
            self._receipts[tx_hash] = receipt
            self._save_store("receipts.json", self._receipts)
    
    def get_receipt(self, tx_hash: str) -> Optional[Dict]:
        return self._receipts.get(tx_hash)
    
    # Trie node storage
    def put_node(self, node_hash: str, node_data: Dict):
        with self._lock:
            self._trie_nodes[node_hash] = node_data
            self._save_store("trie_nodes.json", self._trie_nodes)
    
    def get_node(self, node_hash: str) -> Optional[Dict]:
        return self._trie_nodes.get(node_hash)
    
    # State storage
    def put_state_root(self, root_hash: str, state: Dict):
        with self._lock:
            self._state[root_hash] = state
            self._save_store("state.json", self._state)
    
    def get_state(self, root_hash: str) -> Optional[Dict]:
        return self._state.get(root_hash)
    
    def get_stats(self) -> Dict:
        return {
            "blocks": len(self._blocks),
            "headers": len(self._headers),
            "receipts": len(self._receipts),
            "trie_nodes": len(self._trie_nodes),
            "state_roots": len(self._state)
        }
