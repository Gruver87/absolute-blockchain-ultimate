# consensus/block_builder.py
"""
Geth-style block builder
txpool -> execute -> receipts -> payload
"""

import time
import copy
from typing import Dict, Any, List, Optional
from core.canonical_engine import StateTransitionEngine


class BlockBuilder:
    """
    Geth-style block builder

    txpool -> execute -> receipts -> payload
    """

    def __init__(self, mempool, gas_limit: int = 30_000_000):
        self.mempool = mempool
        self.gas_limit = gas_limit

    # =========================================================
    # BUILD BLOCK
    # =========================================================

    def build_block(
        self,
        parent_hash: str,
        block_number: int,
        proposer: str,
        state,
        base_fee: int = 1
    ) -> Dict[str, Any]:
        """
        Build execution payload from mempool
        """
        included_txs = []
        receipts = []
        gas_used = 0

        working_state = copy.deepcopy(state)

        while True:
            tx = self.mempool.pop_best()

            if tx is None:
                break

            tx_gas = tx.get("gas", 21000)

            # gas limit reached
            if gas_used + tx_gas > self.gas_limit:
                # Put back the transaction? No, it's popped
                # In real client, we'd track future transactions
                break

            context = {
                "base_fee": base_fee,
                "burn_pool": 0
            }

            result = StateTransitionEngine.apply_transaction(
                working_state,
                tx,
                context
            )

            if result.get("status") != "success":
                continue

            # update state
            working_state = result.get("state", working_state)

            included_txs.append(tx)

            receipts.append({
                "tx_hash": tx.get("hash", ""),
                "status": "success",
                "gas_used": result.get("gas_used", 0)
            })

            gas_used += result.get("gas_used", 0)

        # Create execution payload
        from execution.payload import ExecutionPayload
        
        state_root = working_state.root()
        
        # Create receipts root
        from execution.receipts_trie import ReceiptsTrie
        from execution.receipts import Receipt
        
        receipt_objects = []
        for r in receipts:
            receipt_objects.append(Receipt(
                tx_hash=r["tx_hash"],
                status=r["status"],
                gas_used=r["gas_used"],
                fee_paid=0  # TODO: calculate fee
            ))
        
        receipts_root = ReceiptsTrie.build_root(receipt_objects)
        
        # Create block hash
        from execution.block_hash import BlockHash
        payload_data = {
            "parent_hash": parent_hash,
            "block_number": block_number,
            "proposer": proposer,
            "state_root": state_root,
            "receipts_root": receipts_root,
            "gas_used": gas_used,
            "timestamp": int(time.time())
        }
        block_hash = BlockHash.compute(payload_data)

        payload = ExecutionPayload(
            parent_hash=parent_hash,
            block_number=block_number,
            proposer=proposer,
            state_root=state_root,
            receipts_root=receipts_root,
            gas_used=gas_used,
            gas_limit=self.gas_limit,
            timestamp=payload_data["timestamp"],
            transactions=included_txs,
            block_hash=block_hash
        )

        return {
            "payload": payload,
            "state": working_state,
            "transactions": included_txs,
            "receipts": receipts,
            "gas_used": gas_used
        }
