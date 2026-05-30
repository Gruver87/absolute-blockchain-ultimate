# execution/receipts.py
import hashlib
import json
from typing import Dict, Any


class Receipt:
    """Transaction receipt как в Ethereum"""

    def __init__(
        self,
        tx_hash: str,
        status: str,
        gas_used: int,
        fee_paid: int,
        logs: list = None
    ):
        self.tx_hash = tx_hash
        self.status = status
        self.gas_used = gas_used
        self.fee_paid = fee_paid
        self.logs = logs or []

    def serialize(self) -> Dict[str, Any]:
        return {
            "tx_hash": self.tx_hash,
            "status": self.status,
            "gas_used": self.gas_used,
            "fee_paid": self.fee_paid,
            "logs": self.logs
        }

    def hash(self) -> str:
        """Deterministic receipt hash"""
        encoded = json.dumps(
            self.serialize(),
            sort_keys=True
        ).encode()
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def from_dict(data: dict) -> "Receipt":
        return Receipt(
            tx_hash=data.get("tx_hash"),
            status=data.get("status"),
            gas_used=data.get("gas_used"),
            fee_paid=data.get("fee_paid"),
            logs=data.get("logs", [])
        )
