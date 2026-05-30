# beacon/chain.py
from typing import List, Optional

class BeaconChain:
    """Beacon chain (Ethereum PoS consensus layer)"""
    
    SLOTS_PER_EPOCH = 32
    SECONDS_PER_SLOT = 12
    
    def __init__(self):
        self.slot = 0
        self.epoch = 0
        self.validators: List[str] = []
        self.attestations: dict = {}
    
    def advance_slot(self):
        """Move to next slot"""
        self.slot += 1
        if self.slot % self.SLOTS_PER_EPOCH == 0:
            self.epoch += 1
    
    def assign_proposer(self) -> Optional[str]:
        """Assign block proposer for current slot"""
        if not self.validators:
            return None
        return self.validators[self.slot % len(self.validators)]
    
    def add_validator(self, validator: str):
        """Register a new validator"""
        if validator not in self.validators:
            self.validators.append(validator)
    
    def add_attestation(self, block_hash: str, validator: str):
        """Add attestation vote from validator"""
        if block_hash not in self.attestations:
            self.attestations[block_hash] = []
        self.attestations[block_hash].append(validator)
    
    def get_attestation_count(self, block_hash: str) -> int:
        return len(self.attestations.get(block_hash, []))
    
    def get_epoch(self) -> int:
        return self.epoch
    
    def get_slot(self) -> int:
        return self.slot
    
    def get_validator_count(self) -> int:
        return len(self.validators)
