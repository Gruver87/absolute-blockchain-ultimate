# consensus/fork_choice.py
from typing import List, Any

class Chain:
    def __init__(self, blocks: list, weight: int = 0):
        self.blocks = blocks
        self.weight = weight
    
    def __len__(self):
        return len(self.blocks)

class LMDGHOST:
    """Latest Message Driven GHOST — Ethereum fork choice rule"""
    
    @staticmethod
    def choose_head(chains: List[Chain]) -> Chain:
        """Choose heaviest chain (weight + length)"""
        if not chains:
            return None
        
        def score(c: Chain) -> tuple:
            return (c.weight, len(c.blocks))
        
        return max(chains, key=score)
    
    @staticmethod
    def choose_by_votes(chains: List[Chain], votes: dict) -> Chain:
        """Weight by validator votes"""
        def score(c: Chain) -> int:
            vote_score = sum(votes.get(b.hash, 0) for b in c.blocks)
            return c.weight + vote_score
        return max(chains, key=score)
