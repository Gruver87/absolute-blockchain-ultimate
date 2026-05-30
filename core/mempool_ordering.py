# core/mempool_ordering.py
import time
from typing import List, Dict
from dataclasses import dataclass, field


@dataclass(order=True)
class PrioritizedTransaction:
    """Транзакция с приоритетом для mempool"""
    priority: int
    timestamp: float = field(compare=False)
    tx: Dict = field(compare=False)


class MempoolOrdering:
    """
    Ethereum-style mempool ordering:
    - Highest priority_fee first
    - Then lowest nonce
    - Then earliest timestamp
    """

    def __init__(self):
        self.pending: List[PrioritizedTransaction] = []
        self._nonce_tracker: Dict[str, int] = {}

    def add_transaction(self, tx: Dict) -> bool:
        """Добавляет транзакцию с правильным приоритетом"""
        from_addr = tx.get("from")
        nonce = tx.get("nonce", 0)
        priority_fee = tx.get("priority_fee", 0)

        # Nonce check
        expected_nonce = self._nonce_tracker.get(from_addr, 0)
        if nonce != expected_nonce:
            return False

        # Priority = gas_price (higher is better)
        # В Ethereum: priority = gas_price
        priority = priority_fee

        ptx = PrioritizedTransaction(
            priority=priority,
            timestamp=time.time(),
            tx=tx
        )

        self.pending.append(ptx)
        # Сортируем по приоритету (убывание), затем по времени (возрастание)
        self.pending.sort(key=lambda x: (-x.priority, x.timestamp))

        return True

    def get_transactions(self, limit: int = 100) -> List[Dict]:
        """Возвращает транзакции в правильном порядке"""
        return [ptx.tx for ptx in self.pending[:limit]]

    def commit_transaction(self, tx: Dict):
        """Подтверждает транзакцию (увеличивает nonce)"""
        from_addr = tx.get("from")
        self._nonce_tracker[from_addr] = self._nonce_tracker.get(from_addr, 0) + 1

        # Удаляем из pending
        self.pending = [ptx for ptx in self.pending if ptx.tx.get("hash") != tx.get("hash")]

    def size(self) -> int:
        return len(self.pending)

    def clear(self):
        self.pending.clear()
