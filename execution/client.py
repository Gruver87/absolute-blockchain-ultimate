# execution/client.py
from execution.vm import EVM
from state.state import State
from db.db import Database

class ExecutionClient:
    """Execution client (Geth-style)"""
    
    def __init__(self, state: State, vm: EVM, db: Database):
        self.state = state
        self.vm = vm
        self.db = db
        self.mempool = {}
    
    def process_transaction(self, tx: dict) -> dict:
        """Process a single transaction"""
        try:
            result = self.vm.execute(tx, self.state)
            self.db.put(tx.get("hash", ""), result)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "failed", "error": str(e)}
    
    def build_block(self, txs: list) -> dict:
        """Build a block from transactions"""
        state_root = self.state.root()
        return {
            "transactions": txs,
            "state_root": state_root,
            "tx_count": len(txs)
        }
    
    def get_state_root(self) -> str:
        return self.state.root()
