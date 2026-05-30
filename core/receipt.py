# core/receipt.py
import hashlib
import time
from typing import Dict, Any, List
from dataclasses import dataclass, field

@dataclass
class Receipt:
    """Transaction receipt (Ethereum-style)"""
    tx_hash: str
    status: str
    gas_used: int
    block_number: int = 0
    timestamp: int = field(default_factory=lambda: int(time.time()))
    logs: List[Dict] = field(default_factory=list)
    
    def hash(self) -> str:
        data = f"{self.tx_hash}{self.status}{self.gas_used}{self.block_number}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        return {
            "tx_hash": self.tx_hash,
            "status": self.status,
            "gas_used": self.gas_used,
            "block_number": self.block_number,
            "timestamp": self.timestamp,
            "logs": self.logs
        }

class ReceiptStore:
    def __init__(self):
        self._receipts: List[Receipt] = []
    
    def add(self, receipt: Receipt):
        self._receipts.append(receipt)
    
    def get_by_tx(self, tx_hash: str) -> List[Receipt]:
        return [r for r in self._receipts if r.tx_hash == tx_hash]
    
    def get_by_block(self, block_number: int) -> List[Receipt]:
        return [r for r in self._receipts if r.block_number == block_number]
    
    def root_hash(self) -> str:
        if not self._receipts:
            return hashlib.sha256(b"empty_receipts").hexdigest()
        data = "".join(r.hash() for r in self._receipts)
        return hashlib.sha256(data.encode()).hexdigest()
