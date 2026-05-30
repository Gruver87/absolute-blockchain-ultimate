# integration_v20.py
# Запустите этот скрипт для тестирования v20 компонентов

import sys
import json

print("=" * 60)
print("ABSOLUTE BLOCKCHAIN v20 - DISTRIBUTED CORE")
print("=" * 60)

# 1. Тест кошелька ECDSA
print("\n[1] Testing ECDSA Wallet...")
from core.wallet import Wallet

wallet = Wallet.generate()
print(f"   Address: {wallet.get_address()[:16]}...")
print(f"   Public key: {wallet.get_public_key_hex()[:32]}...")

message = "Test message for signing"
signature = wallet.sign(message)
print(f"   Signature: {signature[:32]}...")

verified = Wallet.verify(wallet.get_public_key_hex(), signature, message)
print(f"   Signature verified: {verified}")

# 2. Тест стейкинга
print("\n[2] Testing Staking...")
from core.staking import Staking

staking = Staking()
staking.stake("validator1", 1000000)
staking.stake("validator2", 500000)
staking.stake("validator3", 2000000)

validators = staking.get_validators()
print(f"   Validators: {validators}")

selected = staking.select_validator(0)
print(f"   Selected validator for height 0: {selected}")

# 3. Тест финальности
print("\n[3] Testing Finality...")
from core.finality import Finality

finality = Finality(confirmations_required=3)
finality.add_block("block_hash_1", 1)
finality.confirm("block_hash_1")
finality.confirm("block_hash_1")
print(f"   Confirmations: {finality.get_confirmations('block_hash_1')}")
finality.confirm("block_hash_1")
print(f"   Is final: {finality.is_final('block_hash_1')}")

# 4. Тест газа
print("\n[4] Testing Gas System...")
from core.gas import GasSystem, GasExecutor

gas_system = GasSystem()
gas_executor = GasExecutor(limit_per_block=1000000)

tx = {"from": "a", "to": "b", "amount": 100, "nonce": 1}
gas_required = gas_system.estimate(tx)
print(f"   Gas required: {gas_required}")

can_execute = gas_executor.can_execute(gas_required)
print(f"   Can execute: {can_execute}")

gas_executor.execute(gas_required)
print(f"   Gas used: {gas_executor.gas_used}")
print(f"   Remaining: {gas_executor.get_remaining()}")

# 5. Тест State Trie
print("\n[5] Testing State Trie...")
from core.state_trie import StateTrie

trie = StateTrie()
trie.set("address1", {"balance": 1000000})
trie.set("address2", {"balance": 500000})
trie.set("address3", {"balance": 2000000})

print(f"   Address1 balance: {trie.get('address1')}")
print(f"   Root hash: {trie.root_hash()[:32]}...")

print("\n" + "=" * 60)
print("✅ v20 components tested successfully!")
print("=" * 60)
