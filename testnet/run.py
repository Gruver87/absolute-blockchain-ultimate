# testnet/run.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from state.state import State
from execution.engine import ExecutionEngine
from consensus.consensus import Consensus
from network.bus import NetworkBus
from node.node import Node

class Testnet:
    def __init__(self, node_count: int = 3):
        self.node_count = node_count
        self.bus = NetworkBus()
        self.nodes = []
        # Валидаторы теперь совпадают с ID нод
        self.validators = [f"node_{i}" for i in range(node_count)]
        
    def setup(self):
        print("\n" + "=" * 60)
        print("🚀 ABSOLUTE BLOCKCHAIN v28 — MULTI-NODE TESTNET")
        print("=" * 60)
        print(f"\n📋 Config: {self.node_count} nodes")
        print(f"👥 Validators: {self.validators}")
        
        for i in range(self.node_count):
            node_id = f"node_{i}"
            state = State()
            execution = ExecutionEngine(state)
            consensus = Consensus(self.validators.copy())
            
            node = Node(node_id, execution, consensus, self.bus, None)
            self.bus.register(node_id, node)
            self.nodes.append(node)
        
        # Initialize genesis account with huge balance
        for node in self.nodes:
            node.execution.state.get("foundation").balance = 10_000_000_000_000
            node.execution.state.get("foundation").nonce = 0
        
        print(f"\n✅ Network ready: {self.bus.get_node_count()} nodes connected")
        print(f"📡 Nodes: {self.bus.get_nodes()}")
    
    def run_simulation(self, tx_count: int = 6, rounds: int = 3):
        print("\n" + "=" * 60)
        print("🔄 SIMULATION STARTING")
        print("=" * 60)
        
        # Send test transactions
        print("\n📨 Sending transactions...")
        tx_counter = 0
        for i in range(tx_count):
            tx = {
                "from": "foundation",
                "to": f"user_{i}",
                "amount": 1000 + i * 100,
                "nonce": i
            }
            sender_node = self.nodes[i % len(self.nodes)]
            sender_node.receive_tx(tx)
            tx_counter += 1
        
        print(f"   ✅ {tx_counter} transactions sent\n")
        
        # Run consensus rounds
        print("⛏️ Consensus rounds starting...\n")
        for round_num in range(rounds):
            print(f"   Round {round_num + 1}/{rounds}")
            print(f"      Current leader: {self.nodes[0].consensus.get_leader()}")
            
            for node in self.nodes:
                node.produce_block()
            
            # Allow propagation
            time.sleep(0.3)
        
        # Show results
        self.print_network_stats()
    
    def print_network_stats(self):
        print("\n" + "=" * 60)
        print("📊 NETWORK STATISTICS")
        print("=" * 60)
        
        for node in self.nodes:
            stats = node.get_stats()
            print(f"\n   Node {stats['node_id']}:")
            print(f"      Chain height: {stats['chain_height']}")
            print(f"      Mempool size: {stats['mempool_size']}")
            print(f"      Blocks produced: {stats['blocks_produced']}")
            print(f"      Blocks received: {stats['blocks_received']}")
            print(f"      Transactions received: {stats['tx_received']}")
            print(f"      Is validator: {stats['validator']}")
        
        # Check chain consistency
        print("\n" + "=" * 60)
        print("🔗 CHAIN CONSISTENCY CHECK")
        print("=" * 60)
        
        heights = [node.get_chain_length() for node in self.nodes]
        if len(set(heights)) == 1:
            print(f"   ✅ All nodes at same height: {heights[0]}")
        else:
            print(f"   ⚠️ Nodes at different heights: {heights}")
        
        # Show last block if exists
        if heights[0] > 0:
            last_block = self.nodes[0].get_last_block()
            if last_block:
                print(f"\n   Last block:")
                print(f"      Number: {last_block.get('number')}")
                print(f"      Producer: {last_block.get('producer')}")
                print(f"      Transactions: {len(last_block.get('txs', []))}")
                print(f"      Hash: {last_block.get('hash', '')[:16]}...")

def main():
    print("\n" + "🎯" * 30)
    print("ABSOLUTE BLOCKCHAIN v28")
    print("Multi-Node Testnet Network")
    print("🎯" * 30)
    
    testnet = Testnet(node_count=3)
    testnet.setup()
    testnet.run_simulation(tx_count=6, rounds=3)
    
    print("\n" + "=" * 60)
    print("✅ TESTNET SIMULATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
