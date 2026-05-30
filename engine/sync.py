# engine/sync.py
from typing import List, Dict, Optional
import time
import threading

class SyncEngine:
    """Blockchain sync engine — fast and full sync modes"""
    
    MODE_FULL = "full"
    MODE_FAST = "fast"
    
    def __init__(self, node, p2p, storage):
        self.node = node
        self.p2p = p2p
        self.storage = storage
        self.mode = self.MODE_FULL
        self.is_syncing = False
    
    def start_sync(self, mode: str = MODE_FULL):
        """Start synchronization with network"""
        self.mode = mode
        self.is_syncing = True
        
        thread = threading.Thread(target=self._sync_loop, daemon=True)
        thread.start()
    
    def _sync_loop(self):
        while self.is_syncing:
            try:
                # Request chain from peers
                peers = self.p2p.get_peers()
                if not peers:
                    time.sleep(5)
                    continue
                
                # Get best chain
                best_chain = self._fetch_best_chain()
                if best_chain and len(best_chain) > len(self.node.chain):
                    self._apply_chain(best_chain)
                
                time.sleep(10)
            except:
                time.sleep(5)
    
    def _fetch_best_chain(self) -> Optional[List[Dict]]:
        """Fetch chain from best peer"""
        import requests
        for peer in self.p2p.get_peers()[:3]:
            try:
                r = requests.get(f"{peer}/api/chain", timeout=5)
                if r.status_code == 200:
                    return r.json().get("chain", [])
            except:
                continue
        return None
    
    def _apply_chain(self, chain: List[Dict]):
        """Apply synced chain to local node"""
        # Fast sync: just store blocks
        if self.mode == self.MODE_FAST:
            for block in chain:
                self.storage.put_block(block)
            self.node.chain = chain
        else:
            # Full sync: validate each block
            for block in chain:
                if self.node._validate_block(block):
                    self.node.chain.append(block)
    
    def stop_sync(self):
        self.is_syncing = False
    
    def get_status(self) -> dict:
        return {
            "mode": self.mode,
            "syncing": self.is_syncing,
            "local_height": len(self.node.chain),
            "peers": len(self.p2p.get_peers())
        }
