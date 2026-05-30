# core/canonical_engine.py
"""
Geth-style State Transition Engine - DEVNET VERSION
Low fees for testing, immutable state with deepcopy
"""

import copy
from typing import Dict, Any, Tuple

class StateTransitionEngine:
    """Каноническая state transition функция"""
    
    INTRINSIC_GAS = 21000
    
    @staticmethod
    def apply_transaction(state, tx: Dict, context: Dict) -> Dict:
        """
        PURE STATE TRANSITION FUNCTION
        
        Возвращает:
        {
            "status": "success" или "failed",
            "state": новое состояние,
            "gas_used": количество использованного газа,
            "receipt": receipt с деталями
        }
        """
        # Извлекаем параметры
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        gas_limit = tx.get("gas", StateTransitionEngine.INTRINSIC_GAS)
        # DEVNET: низкие комиссии для тестов
        priority_fee = tx.get("priority_fee", 1)  # 1 вместо 1_000_000_000
        base_fee = context.get("base_fee", 1)     # 1 вместо 10_000_000_000
        validator = tx.get("validator", "validator")
        
        gas_used = StateTransitionEngine.INTRINSIC_GAS
        fee_total = gas_used * (base_fee + priority_fee)
        base_fee_burned = gas_used * base_fee
        validator_reward = gas_used * priority_fee
        
        # 1. VALIDATION PHASE
        sender_balance = state.get_balance(from_addr)
        if sender_balance < amount + fee_total:
            return {
                "status": "failed",
                "error": "insufficient balance",
                "gas_used": 0,
                "state": None
            }
        
        # 2. CREATE NEW STATE (IMMUTABLE - DEEPCOPY!)
        new_state = copy.deepcopy(state)
        
        # 3. TRANSFER AMOUNT
        new_state.set_balance(from_addr, new_state.get_balance(from_addr) - amount)
        new_state.set_balance(to_addr, new_state.get_balance(to_addr) + amount)
        
        # 4. PAY GAS
        new_state.set_balance(from_addr, new_state.get_balance(from_addr) - fee_total)
        
        # 5. VALIDATOR REWARD
        new_state.set_balance(validator, new_state.get_balance(validator) + validator_reward)
        
        # 6. BURN BASE FEE
        if "burn_pool" in context:
            context["burn_pool"] = context.get("burn_pool", 0) + base_fee_burned
        
        # 7. UPDATE NONCE
        new_state.increment_nonce(from_addr)
        
        # 8. RECEIPT
        receipt = {
            "gas_used": gas_used,
            "fee_paid": fee_total,
            "base_fee_burned": base_fee_burned,
            "validator_reward": validator_reward,
            "amount_transferred": amount,
            "from": from_addr,
            "to": to_addr
        }
        
        return {
            "status": "success",
            "state": new_state,
            "gas_used": gas_used,
            "receipt": receipt
        }
    
    @staticmethod
    def apply_block(state, block: Dict, base_fee: int = 1) -> Tuple[Any, list]:
        """Execute entire block"""
        current_state = copy.deepcopy(state)
        receipts = []
        context = {"base_fee": base_fee, "burn_pool": 0}
        
        for tx in block.get("transactions", []):
            result = StateTransitionEngine.apply_transaction(current_state, tx, context)
            
            if result.get("status") == "success":
                current_state = result["state"]
                receipts.append(result["receipt"])
            else:
                receipts.append({"status": "failed", "error": result.get("error")})
        
        return current_state, receipts
