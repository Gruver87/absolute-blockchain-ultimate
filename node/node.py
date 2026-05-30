# node/node.py
import hashlib
import time
from typing import Dict, List, Any, Optional
from execution.engine import ExecutionEngine
from consensus.consensus import Consensus
from state.state import State

class Node:
    """Full blockchain node with consensus and network"""
    
    def __init__(self, node_id: str, execution: ExecutionEngine, consensus: Consensus, network, db=None):
        self.id = node_id
        self.execution = execution
        self.consensus = consensus
        self.network = network
        self.db = db
        
        self.chain: List[Dict] = []
        self.mempool: Dict[str, Dict] = {}
        self.blocks_received = 0
        self.tx_received = 0
    
    def receive_tx(self, tx: Dict) -> None:
        """Receive and store transaction"""
        tx_hash = tx.get("hash") or self._calculate_tx_hash(tx)
        tx["hash"] = tx_hash
        self.mempool[tx_hash] = tx
        self.tx_received += 1
        print(f"   📥 Node {self.id} received tx: {tx_hash[:8]}...")
    
    def receive_block(self, block: Dict) -> None:
        """Receive and validate block"""
        if self.validate_block(block):
            self.chain.append(block)
            self.blocks_received += 1
            print(f"   📦 Node {self.id} received block #{block.get('number', '?')} from {block.get('producer', '?')}")
            
            # Remove transactions from mempool
            for tx in block.get("txs", []):
                tx_hash = tx.get("hash")
                if tx_hash in self.mempool:
                    del self.mempool[tx_hash]
    
    def receive_chain(self, chain: List[Dict]) -> None:
        """Receive full chain for sync"""
        if len(chain) > len(self.chain):
            self.chain = chain
            print(f"   🔄 Node {self.id} synced chain to height {len(chain)}")
    
    def produce_block(self) -> Optional[Dict]:
        """Produce a new block (if this node is the leader)"""
        leader = self.consensus.get_leader()
        if leader != self.id:
            return None
        
        if not self.mempool:
            return None
        
        txs = list(self.mempool.values())
        state_root = self.execution.get_state_root()
        block_number = len(self.chain)
        
        block = {
            "number": block_number,
            "timestamp": int(time.time()),
            "txs": txs,
            "state_root": state_root,
            "producer": self.id,
            "parent_hash": self.get_last_block_hash(),
            "hash": None
        }
        block["hash"] = self._calculate_block_hash(block)
        
        # Apply block to state
        if self.execution.apply_block(block):
            self.chain.append(block)
            self.mempool.clear()
            print(f"   ⛏️ Node {self.id} produced block #{block_number}")
            
            # Broadcast to network
            self.network.broadcast(self.id, "block", block)
            
            # Move consensus round
            self.consensus.next_round()
            
            return block
        
        return None
    
    def validate_block(self, block: Dict) -> bool:
        """Validate incoming block"""
        if not block:
            return False
        
        # Check block number
        if block.get("number") != len(self.chain):
            return False
        
        # Check parent hash
        if block.get("parent_hash") != self.get_last_block_hash():
            return False
        
        # Validate producer
        if not self.consensus.validate_block(block, block.get("producer", "")):
            return False
        
        # Validate block hash
        calculated_hash = self._calculate_block_hash(block)
        if block.get("hash") != calculated_hash:
            return False
        
        return True
    
    def get_last_block(self) -> Optional[Dict]:
        return self.chain[-1] if self.chain else None
    
    def get_last_block_hash(self) -> str:
        last = self.get_last_block()
        if last:
            return last.get("hash", "0" * 64)
        return "0" * 64
    
    def get_chain_length(self) -> int:
        return len(self.chain)
    
    def get_mempool_size(self) -> int:
        return len(self.mempool)
    
    def get_stats(self) -> Dict:
        return {
            "node_id": self.id,
            "chain_height": self.get_chain_length(),
            "mempool_size": self.get_mempool_size(),
            "blocks_produced": len([b for b in self.chain if b.get("producer") == self.id]),
            "blocks_received": self.blocks_received,
            "tx_received": self.tx_received,
            "validator": self.id in self.consensus.get_validators()
        }
    
    def _calculate_tx_hash(self, tx: Dict) -> str:
        data = f"{tx.get('from')}{tx.get('to')}{tx.get('amount')}{tx.get('nonce', 0)}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _calculate_block_hash(self, block: Dict) -> str:
        data = f"{block.get('number')}{block.get('timestamp')}{block.get('txs')}{block.get('parent_hash')}{block.get('producer')}{block.get('state_root')}"
        return hashlib.sha256(data.encode()).hexdigest()
