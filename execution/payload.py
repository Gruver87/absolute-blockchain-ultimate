# execution/payload.py
from dataclasses import dataclass
from typing import List


@dataclass
class ExecutionPayload:
    """Execution payload как в Engine API (Ethereum)"""
    parent_hash: str
    block_number: int
    proposer: str

    state_root: str
    receipts_root: str

    gas_used: int
    gas_limit: int

    timestamp: int

    transactions: List[dict]

    block_hash: str

    def to_dict(self) -> dict:
        return {
            "parent_hash": self.parent_hash,
            "block_number": self.block_number,
            "proposer": self.proposer,
            "state_root": self.state_root,
            "receipts_root": self.receipts_root,
            "gas_used": self.gas_used,
            "gas_limit": self.gas_limit,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "block_hash": self.block_hash
        }
