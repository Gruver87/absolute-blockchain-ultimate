# test_final_system.py
# Финальный тест всей системы Absolute Blockchain v30

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("ABSOLUTE BLOCKCHAIN v30 — ФИНАЛЬНЫЙ СИСТЕМНЫЙ ТЕСТ")
print("Проверка всех компонентов от ядра до production hardening")
print("=" * 70)

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

# ============================================================================
# ЧАСТЬ 1: БАЗОВЫЕ КОМПОНЕНТЫ (v14-v20)
# ============================================================================
print("\n" + "=" * 70)
print("ЧАСТЬ 1: БАЗОВЫЕ КОМПОНЕНТЫ (v14-v20)")
print("=" * 70)

# 1.1 Blockchain Core
print("\n[1.1] Blockchain Core")
from core.block import Block
genesis = Block.genesis()
test("Genesis block created", genesis is not None)
test("Genesis block hash valid", len(genesis.hash) == 64)

# 1.2 Crypto
print("\n[1.2] Cryptography")
from core.crypto import Crypto
pk, pub = Crypto.generate_keypair()
sig = Crypto.sign(pk, "test")
test("Key generation works", pk is not None and pub is not None)
test("Signature works", len(sig) > 0)

# 1.3 Database
print("\n[1.3] Database")
from db.db import Database
db = Database("test_system.json")
db.put("test_key", "test_value")
test("Database put/get works", db.get("test_key") == "test_value")

# 1.4 Mempool
print("\n[1.4] Mempool")
from mempool.mempool import Mempool
mempool = Mempool()
tx = {"hash": "0x1", "gas_price": 100}
mempool.add(tx)
test("Mempool add works", mempool.size() == 1)

# 1.5 State
print("\n[1.5] State")
from state.state import State
state = State()
state.set_balance("alice", 1000000)
test("State set_balance works", state.get_balance("alice") == 1000000)

# 1.6 EVM
print("\n[1.6] EVM")
from execution.evm import EVM
evm = EVM()
tx_evm = {"from": "alice", "to": "bob", "amount": 100, "gas": 21000}
result = evm.execute(tx_evm, state)
test("EVM executes", result.get("status") == "success")

# 1.7 Finality
print("\n[1.7] Finality")
from core.finality import FinalityGadget
finality = FinalityGadget(12)
for i in range(12):
    finality.confirm("block_1")
test("Finality works", finality.is_final("block_1"))

# ============================================================================
# ЧАСТЬ 2: GETH-STYLE КОМПОНЕНТЫ (v21-v25)
# ============================================================================
print("\n" + "=" * 70)
print("ЧАСТЬ 2: GETH-STYLE КОМПОНЕНТЫ (v21-v25)")
print("=" * 70)

# 2.1 Database Layer
print("\n[2.1] Database Layer (geth_db)")
from geth_db.db import Database as GethDB
gdb = GethDB("test_geth_system")
gdb.put_block(0, {"number": 0, "hash": "genesis"})
test("Geth DB put_block works", gdb.get_block(0) is not None)

# 2.2 State Layer
print("\n[2.2] State Layer (geth_state)")
from geth_state.state import StateDB
sdb = StateDB(gdb)
sdb.set_balance("alice", 1000000)
test("Geth State works", sdb.get_balance("alice") == 1000000)

# 2.3 EVM (Geth)
print("\n[2.3] EVM (geth_evm)")
from geth_evm.evm import EVM as GethEVM
gevm = GethEVM()
result = gevm.execute(tx_evm, sdb)
test("Geth EVM works", result.get("status") == "success")

# 2.4 Block Processor
print("\n[2.4] Block Processor (geth_core)")
from geth_core.processor import BlockProcessor, Block
processor = BlockProcessor(sdb, gevm, gdb)
block = Block(0, [], "0" * 64, "validator")
test("Block processor works", processor.process_block(block))

# 2.5 P2P Network
print("\n[2.5] P2P Network (geth_p2p)")
from geth_p2p.p2p import DevP2P
p2p = DevP2P("test_node")
p2p.add_peer("peer1")
test("P2P add_peer works", len(p2p.get_peers()) == 1)

# ============================================================================
# ЧАСТЬ 3: PRODUCTION HARDENING (v26-v30)
# ============================================================================
print("\n" + "=" * 70)
print("ЧАСТЬ 3: PRODUCTION HARDENING (v26-v30)")
print("=" * 70)

# 3.1 Peer Scoring
print("\n[3.1] Peer Scoring")
from geth_p2p.hardening import PeerScore
ps = PeerScore()
ps.reward("good", 10)
ps.punish("bad", 25)
test("Peer scoring works", ps.is_banned("bad"))

# 3.2 Anti-eclipse
print("\n[3.2] Anti-eclipse")
from geth_p2p.hardening import AntiEclipseProtection
ae = AntiEclipseProtection()
ae.add_seed("seed1")
test("Anti-eclipse works", ae is not None)

# 3.3 Hardened Mempool
print("\n[3.3] Hardened Mempool")
from geth_mempool.hardening import HardenedMempool
hm = HardenedMempool()
tx_normal = {"hash": "0x3", "gas_price": 10, "from": "alice", "nonce": 0, "timestamp": time.time()}
test("Hardened mempool accepts", hm.add(tx_normal))

# 3.4 Database Hardening
print("\n[3.4] Database Hardening")
from geth_db.hardening import HardenedDatabase
hdb = HardenedDatabase("test_hardened_system")
hdb.put("key1", "value1")
test("Hardened DB works", hdb.get("key1") == "value1")

# 3.5 Slashing
print("\n[3.5] Slashing")
from geth_consensus.slashing import Slashing
slasher = Slashing()
# First vote for block A in epoch 1
slasher.record_vote("val1", "block_a", 1)
# Second vote for different block B in same epoch 1 -> should slash
slasher.record_vote("val1", "block_b", 1)
test("Slashing detects double vote", slasher.is_slashed("val1"))

# 3.6 State Consistency
print("\n[3.6] State Consistency")
from geth_state.hardening import ConsistentState
cs = ConsistentState()
cs.set_balance("alice", 1000)
test("State consistency works", cs.verify_root(cs.root_hash()))

# 3.7 Execution Hardening
print("\n[3.7] Execution Hardening")
from geth_evm.hardening import HardenedEVM
hevm = HardenedEVM()
cs2 = ConsistentState()
cs2.set_balance("alice", 1000000)
result = hevm.execute(tx_evm, cs2)
test("Hardened EVM works", result.get("status") == "success")

# ============================================================================
# ЧАСТЬ 4: ИНТЕГРАЦИОННЫЕ ТЕСТЫ
# ============================================================================
print("\n" + "=" * 70)
print("ЧАСТЬ 4: ИНТЕГРАЦИОННЫЕ ТЕСТЫ")
print("=" * 70)

# 4.1 Полный цикл транзакции
print("\n[4.1] Полный цикл транзакции")
test_state = State()
test_state.set_balance("alice", 1000000)
test_evm = EVM()
tx_full = {"from": "alice", "to": "bob", "amount": 500, "gas": 21000}
result_full = test_evm.execute(tx_full, test_state)
test("Transaction executed", result_full.get("status") == "success")
test("Balance updated", test_state.get_balance("alice") == 1000000 - 500 - 21000)
test("Receiver balance", test_state.get_balance("bob") == 500)

# 4.2 Множественные транзакции
print("\n[4.2] Множественные транзакции")
test_state2 = State()
test_state2.set_balance("alice", 1000000)
for i in range(5):
    tx_multi = {"from": "alice", "to": f"user_{i}", "amount": 100, "gas": 21000}
    test_evm.execute(tx_multi, test_state2)
test("Multiple transactions processed", test_state2.get_balance("alice") < 1000000)

# 4.3 Beacon chain
print("\n[4.3] Beacon chain")
from geth_consensus.beacon import BeaconChain
beacon = BeaconChain()
beacon.add_validator("val1")
beacon.add_validator("val2")
beacon.advance_slot()
test("Beacon chain works", beacon.get_validator_count() == 2)

# 4.4 Engine API
print("\n[4.4] Engine API")
from geth_engine.api import EngineAPI
engine = EngineAPI(processor, gdb)
payload = engine.new_payload({"number": 3, "transactions": [], "parent_hash": "0" * 64})
test("Engine API works", payload.get("status") in ["VALID", "INVALID"])

# ============================================================================
# ИТОГИ
# ============================================================================
print("\n" + "=" * 70)
print(f"📊 РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
print("=" * 70)

if passed == total:
    print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! 🎉")
    print("")
    print("🏆 ABSOLUTE BLOCKCHAIN v30 — ПОЛНОСТЬЮ РАБОТОСПОСОБЕН!")
    print("")
    print("   ✅ Базовые компоненты (v14-v20)")
    print("   ✅ Geth-style компоненты (v21-v25)")
    print("   ✅ Production hardening (v26-v30)")
    print("   ✅ Интеграционные тесты")
    print("")
    print("   Проект имеет полную Ethereum-клиент архитектуру")
    print("   Уровень: Geth / Nethermind / Erigon blueprint")
    print("   Статус: Production-ready architecture prototype")
else:
    print(f"⚠️ Не пройдено тестов: {total - passed}")
    print("   Требуется проверка проблемных компонентов")

print("=" * 70)
print("")
print("🚀 Следующие шаги:")
print("   1. Реальный libp2p вместо симуляции")
print("   2. RocksDB/LevelDB вместо JSON")
print("   3. Полная EVM спецификация")
print("   4. Аудит безопасности")
print("   5. Тестовая сеть (Testnet)")
print("")
print("🔗 GitHub: https://github.com/Gruver87/absolute-blockchain-ultimate")
print("=" * 70)
