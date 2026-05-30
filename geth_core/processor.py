# geth_core/processor.py
import hashlib
import time
from typing import List, Dict, Any, Optional

class Block:
    def __init__(self, number: int, transactions: List[Dict], parent_hash: str,
                 proposer: str = None, state_root: str = None):
        self.number = number
        self.timestamp = int(time.time())
        self.transactions = transactions
        self.parent_hash = parent_hash
        self.proposer = proposer or "unknown"
        self.state_root = state_root or hashlib.sha256(b"empty").hexdigest()
        self.gas_used = sum(tx.get("gas", 21000) for tx in transactions)
        self.hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        data = f"{self.number}{self.timestamp}{self.transactions}{self.parent_hash}{self.proposer}{self.state_root}{self.gas_used}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "parent_hash": self.parent_hash,
            "proposer": self.proposer,
            "state_root": self.state_root,
            "gas_used": self.gas_used,
            "hash": self.hash
        }

class BlockProcessor:
    """Core blockchain logic — process and validate blocks"""
    
    def __init__(self, state, evm, db):
        self.state = state
        self.evm = evm
        self.db = db
        self.chain: List[Block] = []
    
    def process_block(self, block: Block) -> bool:
        """Process a single block"""
        if not self._validate_block(block):
            return False
        
        # Execute all transactions
        for tx in block.transactions:
            receipt = self.evm.execute(tx, self.state)
            if receipt.get("status") != "success":
                return False
            self.db.put_receipt(tx.get("hash", ""), receipt)
        
        # Update state root
        block.state_root = self.state.root_hash()
        block.hash = block._calculate_hash()
        
        # Store block
        self.db.put_block(block.number, block.to_dict())
        self.chain.append(block)
        
        return True
    
    def _validate_block(self, block: Block) -> bool:
        if block.number != len(self.chain):
            return False
        if block.number > 0:
            if block.parent_hash != self.chain[-1].hash:
                return False
        return True
    
    def get_last_block(self) -> Optional[Block]:
        return self.chain[-1] if self.chain else None
    
    def get_chain_height(self) -> int:
        return len(self.chain)
    
    def get_state_root(self) -> str:
        return self.state.root_hash()
