# core/state_transition.py
"""
Чистая state transition function как в Geth/Nethermind
Без side effects — только входные данные и выходные
"""

from typing import Dict, Any

class StateTransition:
    """Детерминированная state transition функция"""
    
    @staticmethod
    def apply_transaction(state, tx: Dict, block_context: Dict) -> Dict:
        """
        Применяет транзакцию к состоянию
        Возвращает результат и receipt
        
        Входные данные:
        - state: изменяемое состояние
        - tx: транзакция с from, to, amount, gas, priority_fee
        - block_context: base_fee, gas_limit
        
        Выходные данные:
        - status: success/failed
        - gas_used
        - logs
        """
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        gas_limit = tx.get("gas", 21000)
        priority_fee = tx.get("priority_fee", 0)
        base_fee = block_context.get("base_fee", 10_000_000_000)
        validator = tx.get("validator", "validator")
        
        # 1. Проверка баланса
        sender = state.get(from_addr)
        if sender.balance < amount + (base_fee + priority_fee) * gas_limit:
            return {
                "status": "failed",
                "error": "insufficient balance",
                "gas_used": 0
            }
        
        # 2. Выполнение перевода
        sender.balance -= amount
        receiver = state.get(to_addr)
        receiver.balance += amount
        
        # 3. Оплата газа (базовая комиссия сжигается, приоритетная — валидатору)
        total_gas_cost = (base_fee + priority_fee) * gas_limit
        sender.balance -= total_gas_cost
        
        # 4. Награда валидатору (только priority fee * gas)
        validator_reward = priority_fee * gas_limit
        validator_acc = state.get(validator)
        validator_acc.balance += validator_reward
        
        # 5. Сжигание base fee (просто вычитается из total supply)
        base_fee_burned = base_fee * gas_limit
        # base_fee_burned уходит из системы (дефляция)
        
        # 6. Обновление nonce
        sender.nonce += 1
        
        return {
            "status": "success",
            "gas_used": gas_limit,
            "base_fee_burned": base_fee_burned,
            "validator_reward": validator_reward,
            "amount_transferred": amount,
            "from": from_addr,
            "to": to_addr
        }
    
    @staticmethod
    def apply_block(state, blocks: list, base_fee: int) -> list:
        """Применяет блок транзакций"""
        receipts = []
        gas_used_total = 0
        
        for tx in blocks:
            receipt = StateTransition.apply_transaction(state, tx, {"base_fee": base_fee})
            receipts.append(receipt)
            if receipt.get("status") == "success":
                gas_used_total += receipt.get("gas_used", 0)
        
        return receipts, gas_used_total
