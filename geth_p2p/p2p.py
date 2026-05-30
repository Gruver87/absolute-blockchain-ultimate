# geth_p2p/p2p.py
import threading
import time
from typing import List, Dict, Set

class Peer:
    """Network peer representation"""
    def __init__(self, url: str):
        self.url = url
        self.last_seen = time.time()
        self.capabilities = []
    
    def is_alive(self) -> bool:
        return time.time() - self.last_seen < 60

class DevP2P:
    """DevP2P network stack (simplified)"""
    
    PROTOCOLS = ["eth", "snap", "les"]
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self._peers: Dict[str, Peer] = {}
        self._blacklist: Set[str] = set()
        self._lock = threading.RLock()
    
    def add_peer(self, url: str):
        with self._lock:
            if url not in self._peers and url not in self._blacklist:
                self._peers[url] = Peer(url)
    
    def remove_peer(self, url: str):
        with self._lock:
            self._peers.pop(url, None)
    
    def blacklist(self, url: str):
        with self._lock:
            self._blacklist.add(url)
            self._peers.pop(url, None)
    
    def handshake(self, url: str) -> bool:
        """Perform protocol handshake"""
        import requests
        try:
            r = requests.get(f"{url}/api/status", timeout=2)
            return r.status_code == 200
        except:
            return False
    
    def broadcast(self, protocol: str, msg_type: str, data: Dict) -> int:
        """Broadcast message to all peers"""
        if protocol not in self.PROTOCOLS:
            return 0
        
        sent = 0
        with self._lock:
            peers = list(self._peers.keys())
        
        for url in peers:
            if self.handshake(url):
                try:
                    import requests
                    requests.post(f"{url}/api/message", 
                                 json={"protocol": protocol, "type": msg_type, "data": data},
                                 timeout=2)
                    sent += 1
                except:
                    self.blacklist(url)
        
        return sent
    
    def broadcast_tx(self, tx: Dict) -> int:
        return self.broadcast("eth", "tx", tx)
    
    def broadcast_block(self, block: Dict) -> int:
        return self.broadcast("eth", "block", block)
    
    def get_peers(self) -> List[str]:
        return list(self._peers.keys())
    
    def get_stats(self) -> Dict:
        return {
            "node_id": self.node_id,
            "peers": len(self._peers),
            "blacklisted": len(self._blacklist)
        }
