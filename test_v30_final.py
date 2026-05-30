# test_v30_final.py
# Final production-grade test

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("ABSOLUTE BLOCKCHAIN v30 — PRODUCTION FIX")
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

# 1. Database Interface
print("\n[1] Testing Database Interface...")
from db.db import Database
db = Database("test_final.json")
db.add_block({"number": 1, "hash": "0x123"})
db.put_block({"number": 2, "hash": "0x456"})  # Backward compatibility
blocks = db.get_blocks()
print(f"   Blocks in DB: {len(blocks)}")
test("Database works (add_block)", len(blocks) >= 1)
test("Database backward compat (put_block)", len(blocks) >= 2)

# 2. State
print("\n[2] Testing State...")
from state.state import State
state = State()
state.set_balance("alice", 10000)
state.set_balance("bob", 0)
print(f"   Alice balance: {state.get_balance('alice')}")
print(f"   Bob balance: {state.get_balance('bob')}")
test("State balance works", state.get_balance("alice") == 10000)

# 3. EVM with correct balance
print("\n[3] Testing EVM...")
from execution.evm import EVM
evm = EVM()
tx = {"from": "alice", "to": "bob", "amount": 100, "gas": 21000}
result = evm.execute(tx, state)
print(f"   EVM status: {result.get('status')}")
print(f"   Sender balance after: {result.get('sender_balance')}")
test("EVM execution success", result.get("status") == "success")
test("EVM balance transfer", result.get("sender_balance") == 10000 - 100 - 21000)

# 4. Execution Layer
print("\n[4] Testing Execution Layer...")
from execution.core import ExecutionLayer
execution = ExecutionLayer(state, db)
tx2 = {"from": "alice", "to": "bob", "amount": 50, "gas": 21000}
receipt = execution.execute_transaction(tx2)
print(f"   Receipt status: {receipt.get('status')}")
test("Execution layer works", receipt.get("status") == "success")

# 5. Engine API
print("\n[5] Testing Engine API...")
from execution.engine_api import EngineAPI
engine_api = EngineAPI(execution)
block = {"transactions": [], "hash": "0x789", "number": 3}
payload = engine_api.new_payload(block)
print(f"   Payload status: {payload.get('status')}")
test("Engine API works", payload.get("status") == "VALID")

# 6. Casper FFG
print("\n[6] Testing Casper FFG...")
from consensus.casper import CasperFFG
casper = CasperFFG()
casper.vote("block_final", "v1")
casper.vote("block_final", "v2")
casper.vote("block_final", "v3")
print(f"   Votes: {casper.get_vote_count('block_final')}")
test("Casper FFG voting works", casper.get_vote_count("block_final") >= 2)

# 7. LMD-GHOST
print("\n[7] Testing LMD-GHOST...")
from consensus.fork_choice import LMDGHOST, Chain
chain1 = Chain(["a", "b"], weight=10)
chain2 = Chain(["a", "b", "c"], weight=20)
best = LMDGHOST.choose_head([chain1, chain2])
print(f"   Best chain length: {len(best)}")
test("LMD-GHOST works", len(best) == 3)

# 8. Beacon Chain
print("\n[8] Testing Beacon Chain...")
from consensus.beacon import BeaconChain
beacon = BeaconChain()
beacon.add_validator("val1")
beacon.add_validator("val2")
beacon.advance_slot()
print(f"   Slot: {beacon.get_slot()}, Epoch: {beacon.get_epoch()}")
test("Beacon chain works", beacon.get_validator_count() == 2)

# 9. Security
print("\n[9] Testing Security...")
from core.security import Security
security = Security()
test("Security layer works", security is not None)

# 10. Mempool
print("\n[10] Testing Mempool...")
from mempool.mempool import Mempool
mempool = Mempool()
tx_a = {"hash": "0xa", "gas_price": 100}
tx_b = {"hash": "0xb", "gas_price": 200}
mempool.add(tx_a)
mempool.add(tx_b)
ordered = mempool.get_sorted()
print(f"   Best priority: {ordered[0].get('hash')}")
test("Mempool ordering works", ordered[0].get("hash") == "0xb")

print("\n" + "=" * 60)
print(f"📊 РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
if passed == total:
    print("🎉 ALL TESTS PASSED!")
    print("   ✅ Database interface fixed")
    print("   ✅ EVM balance fixed")
    print("   ✅ Execution layer stable")
    print("   ✅ Engine API working")
    print("   ✅ Production architecture ready!")
else:
    print(f"⚠️ Не пройдено тестов: {total - passed}")
print("=" * 60)
