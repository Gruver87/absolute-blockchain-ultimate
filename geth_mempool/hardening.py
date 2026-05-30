# geth_mempool/hardening.py
import time
import threading
from typing import Dict, List, Set

class HardenedMempool:
    """Anti-spam mempool with gas price filtering and replacement rules"""
    
    MIN_GAS_PRICE = 1  # Minimum gas price to accept
    MAX_TX_PER_ADDRESS = 100
    TX_TTL = 3600  # 1 hour
    
    def __init__(self):
        self._txs: Dict[str, dict] = {}
        self._nonce_tracker: Dict[str, int] = {}
        self._seen: Set[str] = set()
        self._lock = threading.RLock()
    
    def add(self, tx: Dict) -> bool:
        """Add transaction with spam protection"""
        tx_hash = tx.get("hash")
        if not tx_hash:
            return False
        
        from_addr = tx.get("from")
        gas_price = tx.get("gas_price", 0)
        
        with self._lock:
            # Anti-spam: minimum gas price
            if gas_price < self.MIN_GAS_PRICE:
                return False
            
            # Anti-spam: per-address limit
            addr_txs = [t for t in self._txs.values() if t.get("from") == from_addr]
            if len(addr_txs) >= self.MAX_TX_PER_ADDRESS:
                return False
            
            # Nonce ordering (prevent replay)
            expected_nonce = self._nonce_tracker.get(from_addr, 0)
            if tx.get("nonce", 0) < expected_nonce:
                return False
            
            # TTL check
            if time.time() - tx.get("timestamp", 0) > self.TX_TTL:
                return False
            
            self._txs[tx_hash] = tx
            self._seen.add(tx_hash)
            
            # Update nonce tracker if this is the next expected nonce
            if tx.get("nonce", 0) == expected_nonce:
                self._nonce_tracker[from_addr] = expected_nonce + 1
            
            return True
    
    def get_ordered(self) -> List[Dict]:
        """Order by gas price (highest first)"""
        with self._lock:
            return sorted(
                self._txs.values(),
                key=lambda tx: tx.get("gas_price", 0),
                reverse=True
            )
    
    def remove(self, tx_hash: str):
        with self._lock:
            self._txs.pop(tx_hash, None)
    
    def size(self) -> int:
        return len(self._txs)
