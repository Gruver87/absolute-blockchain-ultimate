# core/gas.py
import threading
from typing import Dict, Any

class GasSystem:
    BASE_GAS = 21000
    GAS_PER_BYTE = 10
    GAS_PER_NONCE = 100

    def estimate(self, tx: Dict[str, Any]) -> int:
        """Оценивает газ для транзакции"""
        gas = self.BASE_GAS
        gas += len(str(tx)) * self.GAS_PER_BYTE
        if tx.get('nonce'):
            gas += self.GAS_PER_NONCE
        return gas

class GasExecutor:
    def __init__(self, limit_per_block: int = 10_000_000):
        self.limit_per_block = limit_per_block
        self.gas_used = 0
        self.lock = threading.RLock()

    def reset(self):
        with self.lock:
            self.gas_used = 0

    def can_execute(self, gas_required: int) -> bool:
        with self.lock:
            return self.gas_used + gas_required <= self.limit_per_block

    def execute(self, gas_required: int) -> bool:
        with self.lock:
            if self.gas_used + gas_required <= self.limit_per_block:
                self.gas_used += gas_required
                return True
            return False

    def get_remaining(self) -> int:
        with self.lock:
            return self.limit_per_block - self.gas_used
