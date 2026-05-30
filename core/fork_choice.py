# core/fork_choice.py
from typing import List, Any

class BlockChain:
    def __init__(self, chain: list, weight: int = 0):
        self.chain = chain
        self.weight = weight
    
    def total_weight(self) -> int:
        return self.weight
    
    def __len__(self):
        return len(self.chain)

class ForkChoice:
    """LMD-GHOST simplified fork choice rule"""
    
    @staticmethod
    def choose(chains: List[BlockChain]) -> BlockChain:
        """
        Choose the heaviest chain (highest weight + longest)
        """
        if not chains:
            return None
        
        def chain_score(c: BlockChain) -> tuple:
            return (c.total_weight(), len(c.chain))
        
        return max(chains, key=chain_score)
    
    @staticmethod
    def choose_by_weight(chains: List[BlockChain]) -> BlockChain:
        """Weight-only choice (simpler)"""
        if not chains:
            return None
        return max(chains, key=lambda c: c.total_weight())
