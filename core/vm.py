# core/vm.py
import threading
from typing import Dict, Any
from core.mpt import MerklePatriciaTrie

class EVM:
    """Simplified EVM execution engine"""
    
    GAS_PER_OP = 10
    BASE_GAS = 21000
    
    def __init__(self):
        self.gas_used = 0
    
    def execute(self, tx: Dict[str, Any], state: MerklePatriciaTrie) -> Dict[str, Any]:
        """Execute a transaction and update state"""
        from_addr = tx["from"]
        to_addr = tx["to"]
        amount = tx["amount"]
        gas_limit = tx.get("gas", self.BASE_GAS)
        
        # Get current balances
        from_balance = state.get(from_addr) or {"balance": 0}
        to_balance = state.get(to_addr) or {"balance": 0}
        
        # Check balance
        if from_balance.get("balance", 0) < amount + self.BASE_GAS:
            raise Exception(f"Insufficient balance: {from_balance.get('balance', 0)} < {amount + self.BASE_GAS}")
        
        # Execute transfer
        from_balance["balance"] -= amount + self.BASE_GAS
        to_balance["balance"] += amount
        
        # Update state
        state.update(from_addr, from_balance)
        state.update(to_addr, to_balance)
        
        # Update nonce
        nonce = from_balance.get("nonce", 0)
        from_balance["nonce"] = nonce + 1
        state.update(from_addr, from_balance)
        
        self.gas_used = self.BASE_GAS
        
        return {
            "status": "success",
            "gas_used": self.gas_used,
            "from": from_addr,
            "to": to_addr,
            "amount": amount
        }
    
    def reset(self):
        self.gas_used = 0
