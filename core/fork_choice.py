# core/fork_choice.py
"""
Fork choice rule — LMD-GHOST simplified
Chooses the heaviest/longest chain
"""

from typing import List, Dict, Any, Optional


class ForkChoice:
    """
    Упрощённый fork choice rule
    Выбирает цепочку с наибольшей высотой
    """

    @staticmethod
    def choose_head(chains: List[List[Dict]]) -> Optional[Dict]:
        """
        Выбирает голову из нескольких цепочек
        Простейшее правило: самая длинная цепочка
        """
        if not chains:
            return None

        best = None
        best_height = -1

        for chain in chains:
            if not chain:
                continue
            height = chain[-1].get("block_number", -1)
            if height > best_height:
                best_height = height
                best = chain[-1]

        return best

    @staticmethod
    def choose_head_by_weight(chains: List[Dict]) -> Optional[Dict]:
        """
        Выбирает голову по весу (weight = block_number для простоты)
        """
        if not chains:
            return None

        return max(chains, key=lambda x: x.get("block_number", 0))

    @staticmethod
    def compare_chains(chain_a: List[Dict], chain_b: List[Dict]) -> int:
        """
        Сравнивает две цепочки
        Returns: 1 if A is better, -1 if B is better, 0 if equal
        """
        if not chain_a and not chain_b:
            return 0
        if not chain_a:
            return -1
        if not chain_b:
            return 1

        height_a = chain_a[-1].get("block_number", 0)
        height_b = chain_b[-1].get("block_number", 0)

        if height_a > height_b:
            return 1
        elif height_b > height_a:
            return -1
        else:
            return 0
