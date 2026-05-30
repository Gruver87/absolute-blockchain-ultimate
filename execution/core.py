# execution/core.py
from typing import Dict, List, Any
from state.state import State
from db.db import Database

class ExecutionLayer:
    """Execution Client with correct state mutation"""
    
    def __init__(self, state: State, db: Database):
        self.state = state
        self.db = db
        self.mempool: Dict[str, Dict] = {}
        self.evm = None
    
    def _get_evm(self):
        from execution.evm import EVM
        if self.evm is None:
            self.evm = EVM()
        return self.evm
    
    def execute_transaction(self, tx: Dict) -> Dict:
        """Execute single transaction with correct state mutation"""
        evm = self._get_evm()
        result = evm.execute(tx, self.state)
        return result
    
    def execute_block(self, block: Dict) -> List[Dict]:
        """Execute all transactions in a block"""
        receipts = []
        evm = self._get_evm()
        
        for tx in block.get("transactions", []):
            receipt = evm.execute(tx, self.state)
            receipts.append(receipt)
        
        # Update state root
        block["state_root"] = self.state.root()
        
        # Save block
        self.db.add_block(block)
        
        return receipts
    
    def get_state_root(self) -> str:
        return self.state.root()
    
    def add_to_mempool(self, tx: Dict):
        import hashlib
        tx_hash = tx.get("hash")
        if not tx_hash:
            data = f"{tx.get('from')}{tx.get('to')}{tx.get('amount')}{tx.get('nonce', 0)}"
            tx_hash = hashlib.sha256(data.encode()).hexdigest()
            tx["hash"] = tx_hash
        self.mempool[tx_hash] = tx
    
    def get_mempool_txs(self) -> List[Dict]:
        return list(self.mempool.values())
    
    def clear_mempool(self):
        self.mempool.clear()
