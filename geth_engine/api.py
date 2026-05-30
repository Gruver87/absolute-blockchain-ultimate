# geth_engine/api.py
from typing import Dict, List, Any

class EngineAPI:
    """Engine API — bridge between Execution and Consensus layers"""
    
    def __init__(self, execution, db):
        self.execution = execution
        self.db = db
    
    def new_payload(self, block: Dict) -> Dict:
        """
        Consensus client sends new block payload
        Returns execution result and state root
        """
        try:
            # Create and process block
            from geth_core.processor import Block
            
            # Ensure required fields exist
            block_number = block.get("number", 0)
            transactions = block.get("transactions", [])
            parent_hash = block.get("parent_hash", "0" * 64)
            proposer = block.get("proposer", "unknown")
            
            # Create block object
            block_obj = Block(
                number=block_number,
                transactions=transactions,
                parent_hash=parent_hash,
                proposer=proposer
            )
            
            # Process block
            success = self.execution.process_block(block_obj)
            
            return {
                "status": "VALID" if success else "INVALID",
                "state_root": self.execution.get_state_root(),
                "block_hash": block_obj.hash,
                "block_number": block_number
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "state_root": self.execution.get_state_root() if self.execution else None
            }
    
    def fork_choice_updated(self, head_hash: str, finalized_hash: str = None) -> Dict:
        """
        Update fork choice
        """
        return {
            "status": "SUCCESS",
            "head_block_hash": head_hash,
            "finalized_block_hash": finalized_hash
        }
    
    def get_payload(self, block_hash: str) -> Dict:
        """Retrieve payload by hash"""
        blocks = self.db.get_all_blocks()
        for block in blocks:
            if block.get("hash") == block_hash:
                return block
        return None
