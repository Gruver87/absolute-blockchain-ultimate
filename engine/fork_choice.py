# engine/fork_choice.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class ForkChoiceState:
    """Fork choice state как в Engine API"""
    head_block_hash: str
    safe_block_hash: str
    finalized_block_hash: str


class ForkChoiceUpdated:
    """engine_forkchoiceUpdatedV1 — связь CL ↔ EL"""

    def __init__(self):
        self.head = None
        self.safe = None
        self.finalized = None

    def update(self, state: ForkChoiceState) -> dict:
        """Обновляет fork choice"""
        self.head = state.head_block_hash
        self.safe = state.safe_block_hash
        self.finalized = state.finalized_block_hash

        # В реальном клиенте здесь перестройка цепочки
        return {
            "status": "VALID",
            "head_block_hash": self.head,
            "safe_block_hash": self.safe,
            "finalized_block_hash": self.finalized
        }

    def get_status(self) -> dict:
        return {
            "head": self.head,
            "safe": self.safe,
            "finalized": self.finalized
        }
