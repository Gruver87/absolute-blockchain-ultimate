# geth_consensus/slashing.py
from typing import Dict, Set

class Slashing:
    """Validator slashing for misbehavior"""
    
    def __init__(self):
        self.double_votes: Dict[str, Set[str]] = {}
        self.slashed_validators: Set[str] = set()
        self.slashed_stake: Dict[str, int] = {}
        self.vote_history: Dict[str, Dict] = {}  # Track votes per validator
    
    def record_vote(self, validator: str, block_hash: str, epoch: int):
        """Record validator vote, detect double voting"""
        key = f"{validator}:{epoch}"
        
        # Initialize if first vote
        if key not in self.double_votes:
            self.double_votes[key] = set()
        
        # Check for double vote (voting for two different blocks in same epoch)
        if block_hash in self.double_votes[key]:
            # Already voted for this block in this epoch — duplicate, not slash
            return
        
        # If already voted for a different block in this epoch -> double vote!
        if len(self.double_votes[key]) > 0:
            self._slash(validator)
            return
        
        # First vote for this epoch
        self.double_votes[key].add(block_hash)
        
        # Track vote history
        if validator not in self.vote_history:
            self.vote_history[validator] = {}
        self.vote_history[validator][epoch] = block_hash
    
    def _slash(self, validator: str):
        """Slash validator — reduce stake and mark as slashed"""
        if validator not in self.slashed_validators:
            self.slashed_validators.add(validator)
            self.slashed_stake[validator] = self.slashed_stake.get(validator, 0) + 1
            print(f"🔥 Validator {validator} slashed for double voting!")
    
    def is_slashed(self, validator: str) -> bool:
        return validator in self.slashed_validators
    
    def get_slashed_count(self) -> int:
        return len(self.slashed_validators)
    
    def get_slashed_stake(self, validator: str) -> int:
        return self.slashed_stake.get(validator, 0)
    
    def reset(self):
        self.double_votes.clear()
        self.slashed_validators.clear()
        self.slashed_stake.clear()
        self.vote_history.clear()
