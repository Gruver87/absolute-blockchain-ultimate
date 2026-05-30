# core/priority_mempool.py
"""
Simplified priority mempool for testing
Ordering: priority_fee DESC, nonce ASC, timestamp ASC
"""

import heapq
import time
import hashlib
from typing import List, Dict, Optional, Tuple


class PriorityMempool:
    """
    Simplified priority mempool
    """

    def __init__(self):
        self._heap: List[Tuple[int, int, float, Dict]] = []
        self._tx_hashes: set = set()

    def _tx_hash(self, tx: Dict) -> str:
        """Вычисляет детерминированный хэш транзакции"""
        raw = (
            f"{tx.get('from', '')}|"
            f"{tx.get('to', '')}|"
            f"{tx.get('amount', 0)}|"
            f"{tx.get('nonce', 0)}|"
            f"{tx.get('priority_fee', 0)}"
        )
        return hashlib.sha256(raw.encode()).hexdigest()

    def add_transaction(self, tx: Dict) -> bool:
        """
        Добавляет транзакцию в mempool
        """
        # Устанавливаем значения по умолчанию
        tx.setdefault("priority_fee", 0)
        tx.setdefault("nonce", 0)
        tx.setdefault("timestamp", time.time())
        tx.setdefault("to", "")
        tx.setdefault("amount", 0)
        tx.setdefault("from", "unknown")

        # Защита от дубликатов
        tx_hash = self._tx_hash(tx)
        if tx_hash in self._tx_hashes:
            return False

        # Создаём entry для heap
        # priority_fee отрицательный для max heap
        entry = (
            -tx["priority_fee"],   # DESC (higher first)
            tx["nonce"],           # ASC (lower first)
            tx["timestamp"],       # ASC (older first)
            tx
        )

        heapq.heappush(self._heap, entry)
        self._tx_hashes.add(tx_hash)

        return True

    def pop_best(self) -> Optional[Dict]:
        """Извлекает лучшую транзакцию (с наивысшим приоритетом)"""
        if not self._heap:
            return None

        _, _, _, tx = heapq.heappop(self._heap)

        # Удаляем из хэшей
        tx_hash = self._tx_hash(tx)
        if tx_hash in self._tx_hashes:
            self._tx_hashes.remove(tx_hash)

        return tx

    def get_best_transactions(self, limit: int = 100) -> List[Dict]:
        """Возвращает лучшие транзакции без удаления"""
        if not self._heap:
            return []
        heap_copy = self._heap.copy()
        result = []
        for _ in range(min(limit, len(heap_copy))):
            _, _, _, tx = heapq.heappop(heap_copy)
            result.append(tx)
        return result

    def get_all(self) -> List[Dict]:
        """Возвращает все транзакции в правильном порядке"""
        sorted_entries = sorted(self._heap, key=lambda x: (x[0], x[1], x[2]))
        return [entry[3] for entry in sorted_entries]

    def size(self) -> int:
        return len(self._heap)

    def clear(self):
        self._heap.clear()
        self._tx_hashes.clear()

    def contains(self, tx_hash: str) -> bool:
        return tx_hash in self._tx_hashes

    def get_stats(self) -> Dict:
        return {
            "size": len(self._heap),
            "unique_hashes": len(self._tx_hashes)
        }
