# execution/evm.py
from typing import Dict, Any

class EVM:
    """Ethereum Virtual Machine — correct gas calculation"""
    
    GAS_BASE = 21000
    
    def __init__(self):
        self.gas_used = 0
    
    def execute(self, tx: Dict, state) -> Dict:
        """
        Execute transaction with correct gas and balance check
        """
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        gas_limit = tx.get("gas", self.GAS_BASE)
        
        # Get mutable account references
        sender = state.get(from_addr)
        receiver = state.get(to_addr)
        
        # Debug output
        print(f"   DEBUG: sender.balance={sender.balance}, amount={amount}, gas={gas_limit}")
        
        # Balance check (sender must have enough for amount + gas)
        required = amount + gas_limit
        if sender.balance < required:
            return {
                "status": "failed",
                "error": f"insufficient balance: {sender.balance} < {required}",
                "gas_used": 0,
                "from": from_addr,
                "to": to_addr,
                "amount": amount,
                "sender_balance": sender.balance,
                "receiver_balance": receiver.balance
            }
        
        # IN-PLACE MUTATION (critical for state consistency)
        sender.balance -= required
        receiver.balance += amount
        sender.nonce += 1
        
        self.gas_used = gas_limit
        
        return {
            "status": "success",
            "gas_used": self.gas_used,
            "from": from_addr,
            "to": to_addr,
            "amount": amount,
            "sender_balance": sender.balance,
            "receiver_balance": receiver.balance,
            "sender_nonce": sender.nonce
        }
    
    def reset(self):
        self.gas_used = 0
