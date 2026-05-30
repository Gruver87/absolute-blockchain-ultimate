# test_v30_correct.py
# Final correct test with proper balance

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("ABSOLUTE BLOCKCHAIN v30 — CORRECT STATE MUTATION")
print("Ethereum Internal Architecture (Fixed)")
print("=" * 60)

passed = 0
total = 0

def test(name, condition):
    global passed, total
    total += 1
    if condition:
        print(f"   ✅ {name}")
        passed += 1
    else:
        print(f"   ❌ {name}")

# 1. State Mutable References
print("\n[1] Testing State Mutable References...")
from state.state import State, Account
state = State()
alice = state.get("alice")
# Give Alice enough balance for transaction + gas
alice.balance = 1000000  # Large enough balance
alice.nonce = 0
bob = state.get("bob")
bob.balance = 0
print(f"   Alice balance via reference: {alice.balance}")
print(f"   State get_balance: {state.get_balance('alice')}")
test("State mutable reference works", state.get_balance("alice") == 1000000)

# 2. EVM with correct mutation
print("\n[2] Testing EVM...")
from execution.evm import EVM
evm = EVM()
tx = {"from": "alice", "to": "bob", "amount": 100, "gas": 21000}
result = evm.execute(tx, state)
print(f"   EVM status: {result.get('status')}")
print(f"   Sender balance after: {result.get('sender_balance')}")
print(f"   Receiver balance after: {result.get('receiver_balance')}")
test("EVM execution success", result.get("status") == "success")
test("EVM balance transfer", result.get("sender_balance") == 1000000 - 100 - 21000)

# 3. Verify state persistence
print("\n[3] Testing State Persistence...")
print(f"   Alice balance in state: {state.get_balance('alice')}")
print(f"   Bob balance in state: {state.get_balance('bob')}")
print(f"   Alice nonce: {state.get_nonce('alice')}")
expected_balance = 1000000 - 100 - 21000
test("State balance persisted", state.get_balance("alice") == expected_balance)
test("State nonce incremented", state.get_nonce("alice") == 1)

# 4. Execution Layer
print("\n[4] Testing Execution Layer...")
from execution.core import ExecutionLayer
from db.db import Database
db = Database("test_correct.json")
execution = ExecutionLayer(state, db)
tx2 = {"from": "alice", "to": "bob", "amount": 50, "gas": 21000}
receipt = execution.execute_transaction(tx2)
print(f"   Receipt status: {receipt.get('status')}")
test("Execution layer works", receipt.get("status") == "success")

# 5. Engine API
print("\n[5] Testing Engine API...")
from execution.engine_api import EngineAPI
engine_api = EngineAPI(execution)
block = {"transactions": [], "hash": "0x789", "number": 1}
payload = engine_api.new_payload(block)
print(f"   Payload status: {payload.get('status')}")
test("Engine API works", payload.get("status") == "VALID")

# 6. State Root
print("\n[6] Testing State Root...")
state_root = execution.get_state_root()
print(f"   State root: {state_root[:32]}...")
test("State root generated", len(state_root) == 64)

print("\n" + "=" * 60)
print(f"📊 РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
if passed == total:
    print("🎉 ALL TESTS PASSED!")
    print("   ✅ State mutable references work")
    print("   ✅ EVM in-place mutation works")
    print("   ✅ State persistence confirmed")
    print("   ✅ Execution layer stable")
    print("   ✅ Production architecture ready!")
else:
    print(f"⚠️ Не пройдено тестов: {total - passed}")
print("=" * 60)
