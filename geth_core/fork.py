# geth_core/fork.py
from typing import List, Dict, Optional

class ForkHandler:
    """Safe fork handling with reorg protection"""
    
    MAX_REORG_DEPTH = 64  # Maximum blocks to roll back
    
    def __init__(self, processor):
        self.processor = processor
        self.chain: List[Dict] = []
    
    def add_block(self, block: Dict) -> bool:
        """Add block with fork resolution"""
        if not self._validate_parent(block):
            # Fork detected — check if this chain is better
            return self._handle_fork(block)
        
        self.chain.append(block)
        return True
    
    def _validate_parent(self, block: Dict) -> bool:
        if not self.chain:
            return True
        return block.get("parent_hash") == self.chain[-1].get("hash")
    
    def _handle_fork(self, block: Dict) -> bool:
        """Handle fork — find common ancestor and reorg if necessary"""
        # Find common ancestor
        common_height = self._find_common_ancestor(block)
        if common_height < 0:
            return False
        
        # Check if new chain is longer
        new_chain = self._build_chain(block)
        if len(new_chain) <= len(self.chain):
            return False
        
        # Reorg: roll back to common ancestor
        if len(self.chain) - common_height > self.MAX_REORG_DEPTH:
            return False  # Too deep, reject
        
        # Execute reorg
        self.chain = self.chain[:common_height + 1] + new_chain
        return True
    
    def _find_common_ancestor(self, block: Dict) -> int:
        """Find height of common ancestor"""
        for i, b in enumerate(reversed(self.chain)):
            if b.get("hash") == block.get("parent_hash"):
                return len(self.chain) - i - 1
        return -1
    
    def _build_chain(self, block: Dict) -> List[Dict]:
        """Build chain from block following parent links"""
        chain = [block]
        return chain
    
    def get_head(self) -> Optional[Dict]:
        return self.chain[-1] if self.chain else None
