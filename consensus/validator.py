# consensus/validator.py
from typing import List, Dict

class Validator:
    """Validator with stake and slashing conditions"""
    
    def __init__(self, address: str, stake: int = 32):
        self.address = address
        self.stake = stake
        self.slashed = False
        self.attestations = 0
        self.proposals = 0
        self.missed_slots = 0
    
    def slash(self) -> int:
        """Slash validator — penalize stake"""
        slashed_amount = self.stake
        self.stake = 0
        self.slashed = True
        return slashed_amount
    
    def attest(self) -> bool:
        if not self.slashed:
            self.attestations += 1
            return True
        return False
    
    def propose(self) -> bool:
        if not self.slashed:
            self.proposals += 1
            return True
        return False
    
    def miss_slot(self):
        self.missed_slots += 1
    
    def get_reward(self) -> int:
        """Calculate reward based on participation"""
        if self.slashed:
            return 0
        return (self.attestations * 10) + (self.proposals * 100)

class ValidatorSet:
    """Set of all active validators"""
    
    def __init__(self):
        self.validators: Dict[str, Validator] = {}
    
    def add_validator(self, address: str, stake: int = 32):
        self.validators[address] = Validator(address, stake)
    
    def get_validator(self, address: str) -> Validator:
        return self.validators.get(address)
    
    def get_all(self) -> List[Validator]:
        return list(self.validators.values())
    
    def get_active_count(self) -> int:
        return len([v for v in self.validators.values() if not v.slashed])
    
    def total_stake(self) -> int:
        return sum(v.stake for v in self.validators.values())
    
    def slash_validator(self, address: str) -> int:
        if address in self.validators:
            return self.validators[address].slash()
        return 0
