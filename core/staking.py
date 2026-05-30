# core/staking.py
import threading
from typing import Dict, List, Tuple

class Staking:
    def __init__(self):
        self.stakes: Dict[str, int] = {}
        self.lock = threading.RLock()

    def stake(self, validator: str, amount: int) -> bool:
        with self.lock:
            self.stakes[validator] = self.stakes.get(validator, 0) + amount
            return True

    def unstake(self, validator: str, amount: int) -> bool:
        with self.lock:
            if validator not in self.stakes or self.stakes[validator] < amount:
                return False
            self.stakes[validator] -= amount
            return True

    def get_validators(self) -> List[Tuple[str, int]]:
        with self.lock:
            return sorted(self.stakes.items(), key=lambda x: x[1], reverse=True)

    def select_validator(self, height: int) -> str:
        validators = self.get_validators()
        if not validators:
            return None
        return validators[height % len(validators)][0]

    def get_stake(self, validator: str) -> int:
        return self.stakes.get(validator, 0)

    def get_total_stake(self) -> int:
        return sum(self.stakes.values())
