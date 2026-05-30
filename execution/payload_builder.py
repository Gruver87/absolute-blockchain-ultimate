# execution/payload_builder.py
import time
from typing import List

from execution.payload import ExecutionPayload
from execution.state_root import StateRoot
from execution.receipts_trie import ReceiptsTrie
from execution.block_hash import BlockHash
from state.state import State
from execution.receipts import Receipt


class PayloadBuilder:
    """Построитель execution payload"""

    GAS_LIMIT = 30_000_000

    @staticmethod
    def build(
        parent_hash: str,
        block_number: int,
        proposer: str,
        state: State,
        receipts: List[Receipt],
        transactions: List[dict]
    ) -> ExecutionPayload:
        """Строит execution payload из состояния и транзакций"""

        # 1. Вычисляем state root
        state_root = StateRoot.compute(state)

        # 2. Вычисляем receipts root
        receipts_root = ReceiptsTrie.build_root(receipts)

        # 3. Вычисляем gas used
        gas_used = sum(r.gas_used for r in receipts)

        # 4. Собираем данные для hash
        payload_data = {
            "parent_hash": parent_hash,
            "block_number": block_number,
            "proposer": proposer,
            "state_root": state_root,
            "receipts_root": receipts_root,
            "gas_used": gas_used,
            "timestamp": int(time.time())
        }

        # 5. Вычисляем block hash
        block_hash = BlockHash.compute(payload_data)

        # 6. Создаём payload
        return ExecutionPayload(
            parent_hash=parent_hash,
            block_number=block_number,
            proposer=proposer,
            state_root=state_root,
            receipts_root=receipts_root,
            gas_used=gas_used,
            gas_limit=PayloadBuilder.GAS_LIMIT,
            timestamp=payload_data["timestamp"],
            transactions=transactions,
            block_hash=block_hash
        )
