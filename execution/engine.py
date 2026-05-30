# execution/engine.py
from state.state import State
from typing import Dict, Any

class ExecutionEngine:
    """Executes transactions and updates state"""
    
    def __init__(self, state: State):
        self.state = state
    
    def apply_transaction(self, tx: Dict[str, Any]) -> bool:
        """Apply a single transaction to state"""
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        
        sender = self.state.get(from_addr)
        receiver = self.state.get(to_addr)
        
        if sender.balance < amount:
            return False
        
        sender.balance -= amount
        receiver.balance += amount
        sender.nonce += 1
        
        return True
    
    def apply_block(self, block: Dict[str, Any]) -> bool:
        """Apply all transactions in a block"""
        for tx in block.get("txs", []):
            if not self.apply_transaction(tx):
                return False
        return True
    
    def get_state_root(self) -> str:
        return self.state.root()
    
    def get_account(self, address: str):
        return self.state.get(address)
