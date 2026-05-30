# consensus/consensus.py
from typing import List, Optional, Dict

class Consensus:
    """Simple leader-based consensus with round rotation"""
    
    def __init__(self, validators: List[str]):
        self.validators = validators
        self.round = 0
        self.finalized_blocks = set()
    
    def get_leader(self) -> Optional[str]:
        """Get current block proposer"""
        if not self.validators:
            return None
        return self.validators[self.round % len(self.validators)]
    
    def next_round(self) -> int:
        """Move to next consensus round"""
        self.round += 1
        return self.round
    
    def validate_block(self, block: Dict, proposer: str) -> bool:
        """Validate block from proposer"""
        if proposer != self.get_leader():
            return False
        return True
    
    def finalize(self, block_hash: str) -> None:
        self.finalized_blocks.add(block_hash)
    
    def is_final(self, block_hash: str) -> bool:
        return block_hash in self.finalized_blocks
    
    def get_validators(self) -> List[str]:
        return self.validators.copy()
