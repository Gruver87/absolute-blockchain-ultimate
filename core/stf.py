# core/stf.py
from typing import Dict, Any
from core.vm import EVM
from core.mpt import MerklePatriciaTrie

class StateTransitionFunction:
    """Core of blockchain — applies transactions to state"""
    
    def __init__(self, state: MerklePatriciaTrie):
        self.state = state
        self.vm = EVM()
    
    def apply_transaction(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """Apply a single transaction and return receipt"""
        try:
            result = self.vm.execute(tx, self.state)
            return {
                "status": "success",
                "gas_used": result.get("gas_used", 0),
                "result": result
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e),
                "gas_used": 0
            }
    
    def apply_block(self, block_txs: list) -> list:
        """Apply all transactions in a block"""
        receipts = []
        for tx in block_txs:
            receipt = self.apply_transaction(tx)
            receipts.append(receipt)
        return receipts
    
    def get_state_root(self) -> str:
        return self.state.root_hash()
