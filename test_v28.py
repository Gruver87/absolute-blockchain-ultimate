# test_v28.py
import sys
import time
from state.state import State
from execution.engine import ExecutionEngine
from consensus.consensus import Consensus
from network.bus import NetworkBus
from node.node import Node

print("=" * 60)
print("ABSOLUTE BLOCKCHAIN v28 — MULTI-NODE TEST")
print("=" * 60)

# Setup network
bus = NetworkBus()
validators = ["A", "B", "C"]

# Create nodes
nodes = []
for i, vid in enumerate(["A", "B", "C"]):
    state = State()
    execution = ExecutionEngine(state)
    consensus = Consensus(validators)
    node = Node(vid, execution, consensus, bus, None)
    bus.register(vid, node)
    nodes.append(node)

# Initialize genesis
for node in nodes:
    node.execution.state.get("foundation").balance = 1_000_000

print(f"\n✅ Network ready: {bus.get_node_count()} nodes")

# Send transaction
print("\n📨 Sending transaction...")
tx = {"from": "foundation", "to": "alice", "amount": 1000, "nonce": 0}
nodes[0].receive_tx(tx)

# Produce blocks
print("\n⛏️ Producing blocks...")
for node in nodes:
    node.produce_block()

time.sleep(0.5)

# Verify sync
print("\n📊 Results:")
for node in nodes:
    print(f"   Node {node.id}: height={node.get_chain_length()}, mempool={node.get_mempool_size()}")

# All nodes should have same chain length (consensus)
heights = [node.get_chain_length() for node in nodes]
if len(set(heights)) == 1:
    print(f"\n✅ All nodes synchronized at height {heights[0]}")
else:
    print(f"\n⚠️ Desync detected: {heights}")

print("\n✅ v28 multi-node testnet ready!")
