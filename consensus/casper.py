# consensus/casper.py
from typing import Dict, Set

class CasperFFG:
    """Casper Friendly Finality Gadget — Ethereum finality model"""
    
    def __init__(self):
        self.votes: Dict[str, Set[str]] = {}
        self.justified: Set[str] = set()
        self.finalized: Set[str] = set()
    
    def vote(self, block_hash: str, validator: str) -> bool:
        """Validator votes for a block"""
        if block_hash not in self.votes:
            self.votes[block_hash] = set()
        self.votes[block_hash].add(validator)
        
        # Check if block becomes justified (simple 1/2)
        if len(self.votes[block_hash]) >= 2:  # Simplified threshold
            self.justified.add(block_hash)
        
        return True
    
    def finalized(self, block_hash: str, total_validators: int) -> bool:
        """Check if block is finalized (2/3 threshold)"""
        if block_hash not in self.votes:
            return False
        # 2/3 finality rule (simplified)
        threshold = int(total_validators * 2 / 3)
        return len(self.votes.get(block_hash, set())) >= threshold
    
    def is_justified(self, block_hash: str) -> bool:
        return block_hash in self.justified
    
    def is_finalized(self, block_hash: str) -> bool:
        return block_hash in self.finalized
    
    def get_vote_count(self, block_hash: str) -> int:
        return len(self.votes.get(block_hash, set()))
