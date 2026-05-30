# geth_sync/sync.py
import time
import threading
import requests
from typing import List, Dict, Optional

class SyncEngine:
    """Blockchain sync engine — fast and full sync modes"""
    
    MODE_FULL = "full"
    MODE_SNAP = "snap"
    MODE_FAST = "fast"
    
    def __init__(self, node, p2p, db):
        self.node = node
        self.p2p = p2p
        self.db = db
        self.mode = self.MODE_FULL
        self.is_syncing = False
        self.progress = 0
    
    def start_sync(self, mode: str = MODE_FULL):
        self.mode = mode
        self.is_syncing = True
        self.progress = 0
        
        thread = threading.Thread(target=self._sync_loop, daemon=True)
        thread.start()
    
    def _sync_loop(self):
        while self.is_syncing:
            try:
                if self.mode == self.MODE_SNAP:
                    self._snap_sync()
                elif self.mode == self.MODE_FAST:
                    self._fast_sync()
                else:
                    self._full_sync()
                
                time.sleep(5)
            except:
                time.sleep(5)
    
    def _full_sync(self):
        """Full sync — download and execute every block"""
        peers = self.p2p.get_peers()
        if not peers:
            return
        
        for peer in peers[:3]:
            try:
                r = requests.get(f"{peer}/api/chain", timeout=10)
                if r.status_code == 200:
                    chain = r.json().get("chain", [])
                    self._process_chain(chain)
                    self.progress = len(chain)
                    break
            except:
                continue
    
    def _fast_sync(self):
        """Fast sync — download headers + state"""
        # Simplified: download only headers first
        pass
    
    def _snap_sync(self):
        """Snap sync — download state snapshot"""
        # Simplified: download compressed state
        pass
    
    def _process_chain(self, chain: List[Dict]):
        """Process downloaded chain"""
        from geth_core.processor import Block
        
        for block_data in chain:
            block = Block(
                number=block_data.get("number", 0),
                transactions=block_data.get("transactions", []),
                parent_hash=block_data.get("parent_hash", "0" * 64),
                proposer=block_data.get("proposer")
            )
            self.node.process_block(block)
    
    def stop_sync(self):
        self.is_syncing = False
    
    def get_status(self) -> Dict:
        return {
            "mode": self.mode,
            "syncing": self.is_syncing,
            "progress": self.progress
        }
