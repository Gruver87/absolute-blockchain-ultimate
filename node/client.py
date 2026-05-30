# node/client.py
import time
import threading
from typing import Dict, List, Optional

class FullNode:
    """Production full node client (orchestration layer)"""
    
    def __init__(self, node_id: str, execution, consensus, p2p, storage):
        self.id = node_id
        self.execution = execution
        self.consensus = consensus
        self.p2p = p2p
        self.storage = storage
        
        self.chain: List[Dict] = []
        self.mempool: Dict = {}
        self.is_running = False
        self._lock = threading.RLock()
    
    def start(self):
        """Start the node"""
        self.is_running = True
        print(f"🚀 Node {self.id} started")
        
        # Load chain from storage
        self._load_chain()
        
        # Start sync loop
        self._start_sync()
    
    def _load_chain(self):
        blocks = self.storage.get_all_blocks()
        if blocks:
            self.chain = blocks
            print(f"   📦 Loaded {len(blocks)} blocks from storage")
    
    def _start_sync(self):
        def sync_loop():
            while self.is_running:
                time.sleep(5)
                # Sync with peers
                pass
        thread = threading.Thread(target=sync_loop, daemon=True)
        thread.start()
    
    def receive_tx(self, tx: Dict):
        """Receive and validate transaction"""
        tx_hash = tx.get("hash")
        if not tx_hash:
            import hashlib
            data = f"{tx.get('from')}{tx.get('to')}{tx.get('amount')}"
            tx_hash = hashlib.sha256(data.encode()).hexdigest()
            tx["hash"] = tx_hash
        
        with self._lock:
            self.mempool[tx_hash] = tx
        
        # Broadcast to network
        self.p2p.broadcast_tx(tx)
    
    def receive_block(self, block: Dict):
        """Receive and validate block"""
        if self._validate_block(block):
            with self._lock:
                self.chain.append(block)
                self.storage.put_block(block)
    
    def produce_block(self) -> Optional[Dict]:
        """Produce new block (if validator)"""
        if not self.consensus.get_proposer() == self.id:
            return None
        
        with self._lock:
            txs = list(self.mempool.values())
        
        if not txs:
            return None
        
        block = {
            "number": len(self.chain),
            "timestamp": int(time.time()),
            "transactions": txs,
            "parent_hash": self._get_last_block_hash(),
            "producer": self.id,
            "state_root": self.execution.get_state_root()
        }
        
        # Execute block
        receipts = self.execution.execute_block(block)
        
        with self._lock:
            self.chain.append(block)
            self.mempool.clear()
            self.storage.put_block(block)
        
        # Broadcast
        self.p2p.broadcast_block(block)
        
        return block
    
    def _validate_block(self, block: Dict) -> bool:
        if not block:
            return False
        if block.get("number") != len(self.chain):
            return False
        if block.get("parent_hash") != self._get_last_block_hash():
            return False
        return True
    
    def _get_last_block_hash(self) -> str:
        if self.chain:
            return self.chain[-1].get("hash", "0" * 64)
        return "0" * 64
    
    def get_stats(self) -> Dict:
        return {
            "node_id": self.id,
            "chain_height": len(self.chain),
            "mempool_size": len(self.mempool),
            "peers": len(self.p2p.get_peers())
        }
    
    def stop(self):
        self.is_running = False
        print(f"🛑 Node {self.id} stopped")
