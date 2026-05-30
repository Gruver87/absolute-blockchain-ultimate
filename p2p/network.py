# p2p/network.py
import requests
import threading
import time
from typing import List, Dict, Set

class P2PNetwork:
    """Production-ready P2P gossip network"""
    
    TOPICS = ["tx", "block", "attestation"]
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.peers: List[str] = []
        self.blacklist: Set[str] = set()
        self._lock = threading.RLock()
        self._message_cache: Set[str] = set()
    
    def add_peer(self, peer_url: str):
        with self._lock:
            if peer_url not in self.peers and peer_url not in self.blacklist:
                self.peers.append(peer_url)
                print(f"   📡 Peer added: {peer_url}")
    
    def remove_peer(self, peer_url: str):
        with self._lock:
            if peer_url in self.peers:
                self.peers.remove(peer_url)
    
    def blacklist_peer(self, peer_url: str):
        with self._lock:
            self.blacklist.add(peer_url)
            self.remove_peer(peer_url)
    
    def broadcast(self, topic: str, data: Dict) -> int:
        """Broadcast message to all peers"""
        if topic not in self.TOPICS:
            return 0
        
        msg_id = f"{topic}:{data.get('hash', str(data))}"
        if msg_id in self._message_cache:
            return 0
        self._message_cache.add(msg_id)
        
        sent = 0
        with self._lock:
            peers = self.peers.copy()
        
        for peer in peers:
            try:
                requests.post(f"{peer}/api/message", json={"topic": topic, "data": data}, timeout=2)
                sent += 1
            except:
                self.blacklist_peer(peer)
        
        return sent
    
    def broadcast_tx(self, tx: Dict) -> int:
        return self.broadcast("tx", tx)
    
    def broadcast_block(self, block: Dict) -> int:
        return self.broadcast("block", block)
    
    def get_peers(self) -> List[str]:
        return self.peers.copy()
    
    def get_blacklist(self) -> Set[str]:
        return self.blacklist.copy()
    
    def get_stats(self) -> Dict:
        return {
            "node_id": self.node_id,
            "peers": len(self.peers),
            "blacklisted": len(self.blacklist),
            "cached_messages": len(self._message_cache)
        }
