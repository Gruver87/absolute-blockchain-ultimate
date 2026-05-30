# consensus/beacon.py
from typing import List, Optional

class BeaconChain:
    """Ethereum Beacon Chain — slots, epochs, validators"""
    
    SLOTS_PER_EPOCH = 32
    SECONDS_PER_SLOT = 12
    
    def __init__(self):
        self.slot = 0
        self.epoch = 0
        self.validators: List[str] = []
        self.proposer_history: dict = {}
    
    def advance_slot(self) -> int:
        """Move to next slot"""
        self.slot += 1
        if self.slot % self.SLOTS_PER_EPOCH == 0:
            self.epoch += 1
            self._epoch_transition()
        return self.slot
    
    def _epoch_transition(self):
        """Called at epoch boundaries"""
        # Reward validators, apply penalties, etc.
        pass
    
    def get_proposer(self, slot: int = None) -> Optional[str]:
        """Get block proposer for given slot"""
        if not self.validators:
            return None
        target_slot = slot if slot is not None else self.slot
        return self.validators[target_slot % len(self.validators)]
    
    def add_validator(self, validator: str, stake: int = 32):
        self.validators.append(validator)
    
    def get_validator_count(self) -> int:
        return len(self.validators)
    
    def get_epoch(self) -> int:
        return self.epoch
    
    def get_slot(self) -> int:
        return self.slot
    
    def get_slot_in_epoch(self) -> int:
        return self.slot % self.SLOTS_PER_EPOCH
