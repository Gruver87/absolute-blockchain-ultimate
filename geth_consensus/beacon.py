# geth_consensus/beacon.py
from typing import List, Optional, Dict

class BeaconChain:
    """Beacon chain — PoS consensus layer"""
    
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
        return self.slot
    
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
        
        # Justification (1/2 votes)
        if self.attestations[block_hash] >= len(self.validators) // 2:
            self.justified_blocks.add(block_hash)
        
        # Finality (2/3 votes)
        if self.attestations[block_hash] >= (len(self.validators) * 2) // 3:
            self.finalized_blocks.add(block_hash)
    
    def is_finalized(self, block_hash: str) -> bool:
        return block_hash in self.finalized_blocks
    
    def is_justified(self, block_hash: str) -> bool:
        return block_hash in self.justified_blocks
    
    def get_attestation_count(self, block_hash: str) -> int:
        return self.attestations.get(block_hash, 0)
    
    def get_validator_count(self) -> int:
        return len(self.validators)
    
    def get_slot(self) -> int:
        return self.slot
    
    def get_epoch(self) -> int:
        return self.epoch
    
    def lmd_ghost(self, chains: List) -> any:
        """LMD-GHOST fork choice rule"""
        if not chains:
            return None
        return max(chains, key=lambda c: (c.get("weight", 0), c.get("length", 0)))
