# execution/block_hash.py
import hashlib
import json
from typing import Dict


class BlockHash:
    """Детерминированный hash блока"""

    @staticmethod
    def compute(payload_data: Dict) -> str:
        """Вычисляет block hash из payload данных"""
        encoded = json.dumps(
            payload_data,
            sort_keys=True
        ).encode()
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def compute_from_fields(
        parent_hash: str,
        block_number: int,
        proposer: str,
        state_root: str,
        receipts_root: str,
        gas_used: int,
        timestamp: int
    ) -> str:
        """Вычисляет block hash из отдельных полей"""
        payload_data = {
            "parent_hash": parent_hash,
            "block_number": block_number,
            "proposer": proposer,
            "state_root": state_root,
            "receipts_root": receipts_root,
            "gas_used": gas_used,
            "timestamp": timestamp
        }
        return BlockHash.compute(payload_data)
