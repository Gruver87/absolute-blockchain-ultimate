# engine/api.py
from typing import Dict, Any, Optional
from execution.payload import ExecutionPayload
from execution.payload_validator import PayloadValidator
from state.state import State


class EngineAPI:
    """Engine API — связь между Consensus и Execution Layer"""

    def __init__(self):
        self.current_payload = None
        self.last_validated = None

    def new_payload(self, payload: ExecutionPayload, state: State, receipts: list) -> Dict:
        """
        engine_newPayloadV1
        Consensus layer отправляет новый блок для валидации
        """
        # Валидация payload
        is_valid = PayloadValidator.validate(payload, state, receipts)

        if not is_valid:
            return {
                "status": "INVALID",
                "error": "Payload validation failed"
            }

        self.current_payload = payload
        self.last_validated = payload.block_hash

        return {
            "status": "VALID",
            "block_hash": payload.block_hash,
            "state_root": payload.state_root
        }

    def forkchoice_updated(self, head_hash: str, safe_hash: str = None, finalized_hash: str = None) -> Dict:
        """
        engine_forkchoiceUpdatedV1
        Обновление выбора цепочки
        """
        return {
            "status": "VALID",
            "head_block_hash": head_hash,
            "safe_block_hash": safe_hash,
            "finalized_block_hash": finalized_hash
        }

    def get_payload(self, block_hash: str) -> Optional[ExecutionPayload]:
        """
        engine_getPayloadV1
        Получение payload по хэшу
        """
        if self.current_payload and self.current_payload.block_hash == block_hash:
            return self.current_payload
        return None
