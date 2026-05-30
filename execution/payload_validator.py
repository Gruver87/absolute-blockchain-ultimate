# execution/payload_validator.py
from execution.payload import ExecutionPayload
from execution.state_root import StateRoot
from execution.receipts_trie import ReceiptsTrie
from execution.block_hash import BlockHash
from state.state import State
from execution.receipts import Receipt


class PayloadValidator:
    """Валидатор execution payload (Engine API style)"""

    @staticmethod
    def validate(
        payload: ExecutionPayload,
        state: State,
        receipts: list,
        parent_state: State = None
    ) -> bool:
        """Проверяет корректность payload"""

        # 1. Проверка state root
        computed_state_root = StateRoot.compute(state)
        if payload.state_root != computed_state_root:
            print(f"   ❌ State root mismatch: {payload.state_root[:16]} != {computed_state_root[:16]}")
            return False

        # 2. Проверка receipts root
        computed_receipts_root = ReceiptsTrie.build_root(receipts)
        if payload.receipts_root != computed_receipts_root:
            print(f"   ❌ Receipts root mismatch")
            return False

        # 3. Проверка block hash
        payload_data = {
            "parent_hash": payload.parent_hash,
            "block_number": payload.block_number,
            "proposer": payload.proposer,
            "state_root": payload.state_root,
            "receipts_root": payload.receipts_root,
            "gas_used": payload.gas_used,
            "timestamp": payload.timestamp
        }
        computed_block_hash = BlockHash.compute(payload_data)
        if payload.block_hash != computed_block_hash:
            print(f"   ❌ Block hash mismatch")
            return False

        # 4. Проверка gas limit
        if payload.gas_used > payload.gas_limit:
            print(f"   ❌ Gas used exceeds limit")
            return False

        return True
