# consensus/client.py
from typing import List, Set

class ConsensusClient:
    """Consensus client (PoS + Finality + Fork Choice)"""
    
    def __init__(self):
        self.finalized_blocks: Set[str] = set()
        self.head = None
        self._confirmations: dict = {}
    
    def on_new_block(self, block: dict):
        self.head = block
    
    def fork_choice(self, chains: List) -> any:
        """LMD-GHOST simplified: choose heaviest chain"""
        if not chains:
            return None
        return max(chains, key=lambda c: getattr(c, 'weight', len(c.chain) if hasattr(c, 'chain') else 0))
    
    def finalize(self, block_hash: str):
        self.finalized_blocks.add(block_hash)
    
    def is_final(self, block_hash: str) -> bool:
        return block_hash in self.finalized_blocks
    
    def confirm_block(self, block_hash: str) -> bool:
        self._confirmations[block_hash] = self._confirmations.get(block_hash, 0) + 1
        if self._confirmations[block_hash] >= 12:
            self.finalize(block_hash)
            return True
        return False
    
    def get_confirmations(self, block_hash: str) -> int:
        return self._confirmations.get(block_hash, 0)
