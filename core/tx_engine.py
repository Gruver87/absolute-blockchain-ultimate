# core/tx_engine.py
import threading
import hashlib
import time
from typing import Dict, Any, Optional
from core.gas import GasSystem

class TransactionEngine:
    def __init__(self, state_manager, mempool, gas_executor: GasExecutor = None):
        self.state_manager = state_manager
        self.mempool = mempool
        self.gas_system = GasSystem()
        self.gas_executor = gas_executor or GasExecutor()
        self.lock = threading.RLock()
        self.nonce_manager = NonceManager()

    def validate(self, tx: Dict[str, Any]) -> tuple[bool, str]:
        """Полная валидация транзакции"""
        # Проверка обязательных полей
        required = ['from', 'to', 'amount', 'nonce', 'signature', 'public_key']
        for field in required:
            if field not in tx:
                return False, f"Missing field: {field}"

        # Проверка суммы
        if tx['amount'] <= 0:
            return False, "Amount must be positive"

        # Проверка nonce (защита от replay)
        from core.wallet import Wallet
        if not self.nonce_manager.validate(tx['from'], tx['nonce']):
            return False, f"Invalid nonce. Expected: {self.nonce_manager.get_next_nonce(tx['from'])}"

        # Проверка подписи
        message = f"{tx['from']}{tx['to']}{tx['amount']}{tx['nonce']}"
        if not Wallet.verify(tx['public_key'], tx['signature'], message):
            return False, "Invalid signature"

        # Проверка баланса
        balance = self.state_manager.get_balance_satoshi(tx['from'])
        total = tx['amount'] + tx.get('fee', 1000)
        if balance < total:
            return False, f"Insufficient balance. Required: {total}, Available: {balance}"

        # Проверка газа
        gas_required = self.gas_system.estimate(tx)
        if not self.gas_executor.can_execute(gas_required):
            return False, f"Gas limit exceeded. Required: {gas_required}"

        return True, "OK"

    def process(self, tx: Dict[str, Any]) -> Dict[str, Any]:
        """Обработка транзакции"""
        valid, msg = self.validate(tx)
        if not valid:
            return {'status': 'rejected', 'error': msg}

        with self.lock:
            # Выполняем газ
            gas_required = self.gas_system.estimate(tx)
            self.gas_executor.execute(gas_required)

            # Обновляем nonce
            self.nonce_manager.increment(tx['from'])

            # Добавляем в мемпул
            tx_id = hashlib.sha256(f"{tx['from']}{tx['to']}{tx['amount']}{tx['nonce']}{time.time()}".encode()).hexdigest()
            tx['hash'] = tx_id
            self.mempool.add(tx)

            return {
                'status': 'accepted',
                'tx_hash': tx_id,
                'gas_used': gas_required
            }

    def apply(self, tx: Dict[str, Any]) -> bool:
        """Применяет транзакцию к состоянию (после майнинга)"""
        if not self.validate(tx)[0]:
            return False

        total = tx['amount'] + tx.get('fee', 1000)
        self.state_manager.subtract_balance(tx['from'], total)
        self.state_manager.add_balance(tx['to'], tx['amount'])
        self.mempool.remove(tx.get('hash'))
        return True

class NonceManager:
    def __init__(self):
        self._nonces: Dict[str, int] = {}
        self._lock = threading.RLock()

    def get_next_nonce(self, address: str) -> int:
        with self._lock:
            return self._nonces.get(address, 0)

    def validate(self, address: str, nonce: int) -> bool:
        with self._lock:
            expected = self._nonces.get(address, 0)
            return nonce == expected

    def increment(self, address: str) -> int:
        with self._lock:
            self._nonces[address] = self._nonces.get(address, 0) + 1
            return self._nonces[address]
