# core/block_header.py
from dataclasses import dataclass
import hashlib
import json


@dataclass
class BlockHeader:
    """Ethereum-style block header (отдельно от body)"""
    parent_hash: str
    number: int
    timestamp: int
    proposer: str
    
    state_root: str
    transactions_root: str
    receipts_root: str
    
    gas_limit: int
    gas_used: int
    
    def hash(self) -> str:
        """Вычисляет block header hash"""
        data = {
            "parent_hash": self.parent_hash,
            "number": self.number,
            "timestamp": self.timestamp,
            "proposer": self.proposer,
            "state_root": self.state_root,
            "transactions_root": self.transactions_root,
            "receipts_root": self.receipts_root,
            "gas_limit": self.gas_limit,
            "gas_used": self.gas_used
        }
        encoded = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()


@dataclass
class BlockBody:
    """Ethereum-style block body (отдельно от header)"""
    transactions: list
    uncles: list = None


@dataclass
class FullBlock:
    """Полный блок (header + body)"""
    header: BlockHeader
    body: BlockBody
    
    def hash(self) -> str:
        return self.header.hash()
