# execution/engine_api.py
from typing import Dict, Any
from execution.core import ExecutionLayer

class EngineAPI:
    """Engine API — bridge between Execution Layer and Consensus Layer"""
    
    def __init__(self, execution: ExecutionLayer):
        self.execution = execution
    
    def new_payload(self, block: Dict) -> Dict:
        """
        Consensus client sends new block payload
        Returns execution result and state root
        """
        receipts = self.execution.execute_block(block)
        
        return {
            "status": "VALID",
            "state_root": self.execution.get_state_root(),
            "receipts": receipts,
            "gas_used": sum(r.get("gas_used", 0) for r in receipts)
        }
    
    def fork_choice_updated(self, head_block_hash: str, finalized_block_hash: str = None) -> Dict:
        """
        Consensus client updates fork choice
        Returns payload status
        """
        return {
            "status": "SUCCESS",
            "head_block_hash": head_block_hash,
            "finalized_block_hash": finalized_block_hash
        }
    
    def get_payload(self, block_hash: str) -> Dict:
        """Retrieve payload by block hash"""
        return self.execution.db.get_block(block_hash)
