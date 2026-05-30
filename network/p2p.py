# network/p2p.py
import time
from typing import List, Dict, Set

class SecureP2P:
    """Attack-resistant P2P network layer"""
    
    def __init__(self, node_id: str = None):
        self.node_id = node_id or f"node_{int(time.time())}"
        self.peers: List[str] = []
        self.blacklist: Set[str] = set()
        self.message_history: Set[str] = set()  # Anti-replay
    
    def add_peer(self, peer_url: str):
        if peer_url not in self.peers and peer_url not in self.blacklist:
            self.peers.append(peer_url)
    
    def remove_peer(self, peer_url: str):
        if peer_url in self.peers:
            self.peers.remove(peer_url)
    
    def blacklist_peer(self, peer_url: str):
        self.blacklist.add(peer_url)
        self.remove_peer(peer_url)
    
    def is_peer_trusted(self, peer_url: str) -> bool:
        return peer_url not in self.blacklist
    
    def send(self, peer_url: str, message: Dict) -> bool:
        """Send message to peer with validation"""
        if peer_url in self.blacklist:
            return False
        
        # Anti-replay
        msg_id = f"{peer_url}:{message.get('type')}:{message.get('data')}"
        if msg_id in self.message_history:
            return False
        self.message_history.add(msg_id)
        
        try:
            # In real implementation: network send
            return True
        except:
            self.blacklist_peer(peer_url)
            return False
    
    def broadcast(self, msg_type: str, data: Dict) -> int:
        """Broadcast message to all trusted peers"""
        sent = 0
        for peer in self.peers:
            if self.send(peer, {"type": msg_type, "data": data}):
                sent += 1
        return sent
    
    def broadcast_tx(self, tx: Dict):
        self.broadcast("tx", tx)
    
    def broadcast_block(self, block: Dict):
        self.broadcast("block", block)
    
    def get_peers(self) -> List[str]:
        return self.peers.copy()
    
    def get_blacklist(self) -> Set[str]:
        return self.blacklist.copy()
