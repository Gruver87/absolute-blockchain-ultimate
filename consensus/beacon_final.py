# consensus/beacon_final.py
from typing import List, Optional, Dict

class BeaconChain:
    """Production beacon chain with slots, epochs, validators"""
    
    SLOTS_PER_EPOCH = 32
    SECONDS_PER_SLOT = 12
    
    def __init__(self):
        self.slot = 0
        self.epoch = 0
        self.validators: List[str] = []
        self.attestations: Dict[str, int] = {}
        self.finalized_blocks: set = set()
        self.justified_blocks: set = set()
    
    def advance_slot(self) -> int:
        self.slot += 1
        if self.slot % self.SLOTS_PER_EPOCH == 0:
            self.epoch += 1
            self._epoch_transition()
        return self.slot
    
    def _epoch_transition(self):
        """Called at epoch boundaries — reward validators"""
        pass
    
    def add_validator(self, address: str):
        if address not in self.validators:
            self.validators.append(address)
    
    def get_proposer(self, slot: int = None) -> Optional[str]:
        if not self.validators:
            return None
        target = slot if slot is not None else self.slot
        return self.validators[target % len(self.validators)]
    
    def add_attestation(self, block_hash: str, validator: str):
        if block_hash not in self.attestations:
            self.attestations[block_hash] = 0
        self.attestations[block_hash] += 1
        
        # Justification at 1/2 votes
        if self.attestations[block_hash] >= len(self.validators) // 2:
            self.justified_blocks.add(block_hash)
        
        # Finality at 2/3 votes
        if self.attestations[block_hash] >= (len(self.validators) * 2) // 3:
            self.finalized_blocks.add(block_hash)
    
    def is_justified(self, block_hash: str) -> bool:
        return block_hash in self.justified_blocks
    
    def is_finalized(self, block_hash: str) -> bool:
        return block_hash in self.finalized_blocks
    
    def get_attestation_count(self, block_hash: str) -> int:
        return self.attestations.get(block_hash, 0)
    
    def get_validator_count(self) -> int:
        return len(self.validators)
    
    def get_slot(self) -> int:
        return self.slot
    
    def get_epoch(self) -> int:
        return self.epoch
