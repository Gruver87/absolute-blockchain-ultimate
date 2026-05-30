# execution/vm.py
class EVM:
    """Ethereum Virtual Machine (simplified)"""
    
    GAS_PER_TX = 21000
    GAS_PER_BYTE = 10
    
    def execute(self, tx: dict, state) -> dict:
        """Execute transaction and update state"""
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        
        sender = state.get(from_addr)
        receiver = state.get(to_addr)
        
        # Check balance
        if sender.balance < amount + self.GAS_PER_TX:
            raise Exception(f"Insufficient balance: {sender.balance} < {amount + self.GAS_PER_TX}")
        
        # Transfer
        sender.balance -= amount + self.GAS_PER_TX
        receiver.balance += amount
        sender.nonce += 1
        
        return {
            "status": "success",
            "gas_used": self.GAS_PER_TX,
            "from": from_addr,
            "to": to_addr,
            "amount": amount
        }
