# core/finality.py
import threading
from typing import Dict, Set

class FinalityGadget:
    """Casper-like finality gadget"""
    
    def __init__(self, required_confirmations: int = 12):
        self.required = required_confirmations
        self._confirmations: Dict[str, int] = {}
        self._justified: Set[str] = set()
        self._finalized: Set[str] = set()
        self._lock = threading.RLock()
    
    def justify(self, block_hash: str) -> bool:
        with self._lock:
            self._justified.add(block_hash)
            return True
    
    def confirm(self, block_hash: str) -> bool:
        with self._lock:
            self._confirmations[block_hash] = self._confirmations.get(block_hash, 0) + 1
            if self._confirmations[block_hash] >= self.required:
                self._finalized.add(block_hash)
                return True
            return False
    
    def is_final(self, block_hash: str) -> bool:
        return block_hash in self._finalized
    
    def is_justified(self, block_hash: str) -> bool:
        return block_hash in self._justified
    
    def get_confirmations(self, block_hash: str) -> int:
        return self._confirmations.get(block_hash, 0)
    
    def reset(self):
        with self._lock:
            self._confirmations.clear()
            self._justified.clear()
            self._finalized.clear()
