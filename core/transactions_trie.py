# core/transactions_trie.py
import hashlib
from typing import List


class TransactionsTrie:
    """Merkle Patricia Trie для транзакций"""

    @staticmethod
    def compute_root(transactions: List[dict]) -> str:
        """Вычисляет transactions root (Merkle root)"""
        if not transactions:
            return hashlib.sha256(b"empty_transactions").hexdigest()

        # Каждая транзакция имеет свой хэш
        hashes = []
        for tx in transactions:
            # Вычисляем хэш транзакции
            if "hash" in tx:
                tx_hash = tx["hash"]
            else:
                # Детерминированный хэш из содержимого
                import json
                encoded = json.dumps(tx, sort_keys=True).encode()
                tx_hash = hashlib.sha256(encoded).hexdigest()
            hashes.append(tx_hash)

        # Построение Merkle tree
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
    def compute_root_from_hashes(hashes: List[str]) -> str:
        """Вычисляет root из предвычисленных хэшей"""
        if not hashes:
            return hashlib.sha256(b"empty_transactions").hexdigest()

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
