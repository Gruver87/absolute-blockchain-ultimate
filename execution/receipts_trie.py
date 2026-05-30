# execution/receipts_trie.py
import hashlib
from typing import List
from execution.receipts import Receipt


class ReceiptsTrie:
    """Merkle Patricia Trie для receipt roots (как в Ethereum)"""

    @staticmethod
    def build_root(receipts: List[Receipt]) -> str:
        """Вычисляет receipts root (Merkle root)"""
        if not receipts:
            return hashlib.sha256(b"empty_receipts").hexdigest()

        hashes = [r.hash() for r in receipts]

        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])

            new_level = []
            for i in range(0, len(hashes), 2):
                combined = (hashes[i] + hashes[i + 1]).encode()
                new_hash = hashlib.sha256(combined).hexdigest()
                new_level.append(new_hash)

            hashes = new_level

        return hashes[0]

    @staticmethod
    def build_root_from_hashes(hashes: List[str]) -> str:
        """Build root from pre-computed hashes"""
        if not hashes:
            return hashlib.sha256(b"empty_receipts").hexdigest()

        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])

            new_level = []
            for i in range(0, len(hashes), 2):
                combined = (hashes[i] + hashes[i + 1]).encode()
                new_hash = hashlib.sha256(combined).hexdigest()
                new_level.append(new_hash)

            hashes = new_level

        return hashes[0]
