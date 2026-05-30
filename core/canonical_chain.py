# core/canonical_chain.py
"""
Canonical chain management — Ethereum-style
Tracks HEAD, SAFE, FINALIZED blocks
"""

from typing import Dict, Any, Optional, List


class CanonicalChain:
    """
    Управление канонической цепочкой блоков
    """

    def __init__(self):
        self.blocks: Dict[str, Dict] = {}  # hash -> block
        self.height_index: Dict[int, str] = {}  # height -> hash
        self.head: Optional[Dict] = None
        self.safe: Optional[Dict] = None
        self.finalized: Optional[Dict] = None

    def add_block(self, block: Dict[str, Any]) -> bool:
        """
        Добавляет блок в каноническую цепочку
        """
        block_hash = block.get("block_hash")
        if not block_hash:
            return False

        self.blocks[block_hash] = block
        self.height_index[block.get("block_number", 0)] = block_hash

        # Update head if this is the highest block
        if self.head is None:
            self.head = block
        elif block.get("block_number", 0) > self.head.get("block_number", 0):
            self.head = block

        return True

    def get_block_by_hash(self, block_hash: str) -> Optional[Dict]:
        return self.blocks.get(block_hash)

    def get_block_by_height(self, height: int) -> Optional[Dict]:
        block_hash = self.height_index.get(height)
        if block_hash:
            return self.blocks.get(block_hash)
        return None

    def get_head(self) -> Optional[Dict]:
        return self.head

    def get_head_height(self) -> int:
        if self.head:
            return self.head.get("block_number", 0)
        return 0

    def get_head_hash(self) -> Optional[str]:
        if self.head:
            return self.head.get("block_hash")
        return None

    def update_safe(self, block: Dict):
        self.safe = block

    def update_finalized(self, block: Dict):
        self.finalized = block

    def get_safe(self) -> Optional[Dict]:
        return self.safe

    def get_finalized(self) -> Optional[Dict]:
        return self.finalized

    def get_chain(self) -> List[Dict]:
        """Возвращает цепочку в порядке возрастания высоты"""
        chain = []
        for height in sorted(self.height_index.keys()):
            block_hash = self.height_index[height]
            block = self.blocks.get(block_hash)
            if block:
                chain.append(block)
        return chain

    def get_last_blocks(self, count: int = 10) -> List[Dict]:
        """Возвращает последние N блоков"""
        chain = self.get_chain()
        return chain[-count:]

    def contains(self, block_hash: str) -> bool:
        return block_hash in self.blocks

    def size(self) -> int:
        return len(self.blocks)
