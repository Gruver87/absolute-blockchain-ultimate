# geth_evm/evm.py
from typing import Dict, Any, List

class Stack:
    """EVM stack machine"""
    def __init__(self, max_depth: int = 1024):
        self._items: List[Any] = []
        self.max_depth = max_depth
    
    def push(self, item: Any):
        if len(self._items) >= self.max_depth:
            raise Exception("stack overflow")
        self._items.append(item)
    
    def pop(self) -> Any:
        if not self._items:
            raise Exception("stack underflow")
        return self._items.pop()
    
    def peek(self) -> Any:
        if not self._items:
            return None
        return self._items[-1]
    
    def size(self) -> int:
        return len(self._items)

class Memory:
    """EVM memory model"""
    def __init__(self):
        self._data: bytearray = bytearray()
    
    def get(self, offset: int, size: int) -> bytes:
        if offset + size > len(self._data):
            self._data.extend(b'\x00' * (offset + size - len(self._data)))
        return bytes(self._data[offset:offset + size])
    
    def set(self, offset: int, value: bytes):
        if offset + len(value) > len(self._data):
            self._data.extend(b'\x00' * (offset + len(value) - len(self._data)))
        self._data[offset:offset + len(value)] = value

class EVM:
    """Ethereum Virtual Machine"""
    
    GAS_BASE = 21000
    GAS_ADD = 3
    GAS_MUL = 5
    GAS_SLOAD = 50
    GAS_SSTORE = 100
    
    def __init__(self):
        self.stack = Stack()
        self.memory = Memory()
        self.gas_used = 0
        self.pc = 0
    
    def execute(self, tx: Dict, state) -> Dict:
        """Execute transaction"""
        from_addr = tx.get("from")
        to_addr = tx.get("to")
        amount = tx.get("amount", 0)
        gas_limit = tx.get("gas", self.GAS_BASE)
        
        sender = state.get_account(from_addr)
        receiver = state.get_account(to_addr)
        
        required = amount + gas_limit
        if sender.balance < required:
            return {
                "status": "failed",
                "error": f"insufficient balance: {sender.balance} < {required}",
                "gas_used": 0
            }
        
        # Transfer
        sender.balance -= required
        receiver.balance += amount
        sender.nonce += 1
        
        self.gas_used = gas_limit
        
        return {
            "status": "success",
            "gas_used": self.gas_used,
            "from": from_addr,
            "to": to_addr,
            "amount": amount,
            "sender_balance": sender.balance,
            "receiver_balance": receiver.balance
        }
    
    def execute_bytecode(self, bytecode: bytes, state) -> Dict:
        """Execute bytecode (opcode interpreter)"""
        self.pc = 0
        self.gas_used = 0
        
        while self.pc < len(bytecode):
            opcode = bytecode[self.pc]
            self.pc += 1
            
            if opcode == 0x00:  # STOP
                break
            elif opcode == 0x01:  # ADD
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push(a + b)
                self.gas_used += self.GAS_ADD
            elif opcode == 0x02:  # MUL
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.push(a * b)
                self.gas_used += self.GAS_MUL
            elif opcode == 0x54:  # SLOAD
                key = self.stack.pop()
                self.stack.push(0)
                self.gas_used += self.GAS_SLOAD
            elif opcode == 0x55:  # SSTORE
                key = self.stack.pop()
                value = self.stack.pop()
                self.gas_used += self.GAS_SSTORE
            else:
                raise ValueError(f"Unknown opcode: {hex(opcode)}")
        
        return {
            "status": "success",
            "gas_used": self.gas_used,
            "stack_depth": self.stack.size()
        }
    
    def reset(self):
        self.stack = Stack()
        self.memory = Memory()
        self.gas_used = 0
        self.pc = 0
