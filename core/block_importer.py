# core/block_importer.py
import copy
from typing import Dict, Any
from core.block_validator import BlockValidator
from core.canonical_engine import StateTransitionEngine


class BlockImporter:
    """Geth-style block import pipeline"""

    @staticmethod
    def import_block(payload: Dict[str, Any], state, db, base_fee: int = 1) -> Dict[str, Any]:
        """
        Импортирует блок в цепочку

        Pipeline:
        1. validate header
        2. copy state
        3. re-execute transactions
        4. compare state root
        5. compare receipts root
        6. store block
        """

        # 1. validate header
        if not BlockValidator.validate_header(payload):
            return {
                "status": "INVALID_HEADER",
                "error": "Missing required fields"
            }

        # 2. copy state
        working_state = copy.deepcopy(state)

        receipts = []
        total_gas = 0

        # 3. re-execute txs
        context = {"base_fee": base_fee, "burn_pool": 0}

        for tx in payload.get("transactions", []):
            result = StateTransitionEngine.apply_transaction(
                working_state,
                tx,
                context
            )

            if result.get("status") != "success":
                return {
                    "status": "INVALID_TX",
                    "error": result.get("error", "Transaction execution failed"),
                    "tx": tx
                }

            working_state = result.get("state", working_state)
            receipts.append(result)
            total_gas += result.get("gas_used", 0)

        # 4. compare state root
        new_state_root = working_state.root()

        if new_state_root != payload.get("state_root"):
            return {
                "status": "INVALID_STATE_ROOT",
                "expected": payload.get("state_root"),
                "got": new_state_root
            }

        # 5. compare receipts root (simplified for now)
        # In real client, we'd compute receipts root from receipts

        # 6. store block
        block_number = payload.get("block_number")
        if block_number is not None:
            db.put_block(block_number, payload)

        return {
            "status": "VALID",
            "new_state": working_state,
            "receipts": receipts,
            "gas_used": total_gas
        }
