# mempool/mempool.py
from typing import Dict, List, Set

class Mempool:
    """Anti-spam transaction pool with ordering"""
    
    def __init__(self, max_size: int = 1000):
        self.txs: Dict[str, Dict] = {}
        self.seen: Set[str] = set()
        self.max_size = max_size
    
    def add(self, tx: Dict) -> bool:
        """Add transaction with spam protection"""
        tx_hash = tx.get("hash")
        if not tx_hash:
            tx_hash = self._calculate_hash(tx)
            tx["hash"] = tx_hash
        
        # Prevent duplicate and spam
        if tx_hash in self.seen:
            return False
        
        if len(self.txs) >= self.max_size:
            return False
        
        self.seen.add(tx_hash)
        self.txs[tx_hash] = tx
        return True
    
    def remove(self, tx_hash: str) -> bool:
        """Remove transaction by hash"""
        if tx_hash in self.txs:
            del self.txs[tx_hash]
            return True
        return False
    
    def get_sorted(self) -> List[Dict]:
        """Sort by gas price (highest first) and nonce"""
        return sorted(
            self.txs.values(),
            key=lambda tx: (tx.get("gas_price", 0), -tx.get("nonce", 0)),
            reverse=True
        )
    
    def get_all(self) -> List[Dict]:
        return list(self.txs.values())
    
    def size(self) -> int:
        return len(self.txs)
    
    def clear(self):
        self.txs.clear()
    
    def contains(self, tx_hash: str) -> bool:
        return tx_hash in self.txs
    
    def _calculate_hash(self, tx: Dict) -> str:
        import hashlib
        data = f"{tx.get('from')}{tx.get('to')}{tx.get('amount')}{tx.get('nonce', 0)}"
        return hashlib.sha256(data.encode()).hexdigest()
