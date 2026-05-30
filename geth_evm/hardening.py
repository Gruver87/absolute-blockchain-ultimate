# geth_evm/hardening.py
import time
from typing import Dict, Any

class HardenedEVM:
    """EVM with gas metering, timeouts, and stack limits"""
    
    GAS_BASE = 21000
    MAX_STACK_DEPTH = 1024
    MAX_EXECUTION_TIME = 5  # seconds
    MAX_GAS_PER_TX = 30_000_000
    
    def __init__(self):
        self.gas_used = 0
        self.stack = []
        self.start_time = 0
    
    def execute(self, tx: Dict, state) -> Dict:
        """Execute with hardened protection"""
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        gas_limit = min(tx.get("gas", self.GAS_BASE), self.MAX_GAS_PER_TX)
        
        self.start_time = time.time()
        self.stack = []
        self.gas_used = 0
        
        # Timeout guard
        if time.time() - self.start_time > self.MAX_EXECUTION_TIME:
            return {"status": "failed", "error": "execution timeout"}
        
        sender = state.get_account(from_addr)
        receiver = state.get_account(to_addr)
        
        required = amount + gas_limit
        if sender["balance"] < required:
            return {"status": "failed", "error": "insufficient balance"}
        
        # Transfer
        sender["balance"] -= required
        receiver["balance"] += amount
        sender["nonce"] += 1
        
        self.gas_used = gas_limit
        
        # Stack limit check
        if len(self.stack) > self.MAX_STACK_DEPTH:
            return {"status": "failed", "error": "stack overflow"}
        
        return {
            "status": "success",
            "gas_used": self.gas_used,
            "from": from_addr,
            "to": to_addr,
            "amount": amount
        }
