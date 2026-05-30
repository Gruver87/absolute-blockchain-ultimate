# core/mempool.py
import threading
from typing import Dict, List, Any

class Mempool:
    """Transaction pool with MEV-resistant ordering"""
    
    def __init__(self):
        self._txs: Dict[str, Dict] = {}
        self._lock = threading.RLock()
    
    def add(self, tx: Dict) -> bool:
        with self._lock:
            tx_hash = tx.get("hash")
            if not tx_hash:
                return False
            self._txs[tx_hash] = tx
            return True
    
    def remove(self, tx_hash: str) -> bool:
        with self._lock:
            if tx_hash in self._txs:
                del self._txs[tx_hash]
                return True
            return False
    
    def get_sorted(self) -> List[Dict]:
        """Sort by gas price (high to low) and nonce (low to high)"""
        with self._lock:
            return sorted(
                self._txs.values(),
                key=lambda x: (
                    -x.get("gas_price", 0),
                    x.get("nonce", 0)
                )
            )
    
    def get_all(self) -> List[Dict]:
        with self._lock:
            return list(self._txs.values())
    
    def size(self) -> int:
        return len(self._txs)
    
    def clear(self):
        with self._lock:
            self._txs.clear()
