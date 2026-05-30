# core/block_validator.py
from typing import Dict, Any


class BlockValidator:
    """Базовый валидатор заголовка блока"""

    @staticmethod
    def validate_header(payload: Dict[str, Any]) -> bool:
        """Проверяет обязательные поля заголовка блока"""
        required = [
            "block_number",
            "state_root",
            "receipts_root",
            "block_hash",
            "transactions",
            "gas_used",
            "gas_limit",
            "parent_hash",
            "proposer"
        ]

        for field in required:
            if field not in payload:
                return False

        if payload.get("gas_used", 0) > payload.get("gas_limit", 0):
            return False

        return True

    @staticmethod
    def validate_transactions(transactions: list) -> bool:
        """Проверяет что транзакции имеют правильный формат"""
        for tx in transactions:
            required_tx_fields = ["from", "to", "amount", "gas", "nonce"]
            for field in required_tx_fields:
                if field not in tx:
                    return False
        return True
