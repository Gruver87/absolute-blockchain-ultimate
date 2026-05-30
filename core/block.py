# core/block.py
import hashlib
import time
from typing import List, Dict, Any

class Block:
    """Mainnet-style block structure"""
    
    def __init__(self, number: int, transactions: List[Dict], parent_hash: str,
                 state_root: str = None, proposer: str = None):
        self.number = number
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.parent_hash = parent_hash
        self.proposer = proposer or "unknown"
        self.state_root = state_root or hashlib.sha256(b"empty_state").hexdigest()
        self.gas_used = sum(tx.get("gas", 21000) for tx in transactions)
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        data = f"{self.number}{self.timestamp}{self.transactions}{self.parent_hash}{self.proposer}{self.state_root}{self.gas_used}{self.nonce}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "parent_hash": self.parent_hash,
            "proposer": self.proposer,
            "state_root": self.state_root,
            "gas_used": self.gas_used,
            "hash": self.hash
        }
    
    @staticmethod
    def genesis() -> "Block":
        return Block(0, [], "0" * 64, hashlib.sha256(b"genesis_state").hexdigest(), "genesis")
