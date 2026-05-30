# execution/evm_final.py
from typing import Dict, Any

class EVM:
    """Production-grade EVM core"""
    
    GAS_BASE = 21000
    
    def __init__(self):
        self.gas_used = 0
        self.return_data = None
    
    def execute(self, tx: Dict, state) -> Dict:
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        gas_limit = tx.get("gas", self.GAS_BASE)
        
        sender = state.get(from_addr)
        receiver = state.get(to_addr)
        
        required = amount + gas_limit
        if sender.balance < required:
            return {
                "status": "failed",
                "error": f"insufficient balance: {sender.balance} < {required}",
                "gas_used": 0
            }
        
        sender.balance -= required
        receiver.balance += amount
        sender.nonce += 1
        
        self.gas_used = gas_limit
        
        return {
            "status": "success",
            "gas_used": self.gas_used,
            "from": from_addr,
            "to": to_addr,
            "amount": amount
        }
