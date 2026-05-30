# network/bus.py
from typing import List, Dict, Any
import threading
import time

class NetworkBus:
    """Simulated P2P network bus for multi-node communication"""
    
    def __init__(self):
        self.nodes: Dict[str, Any] = {}
        self.messages: List[Dict] = []
        self._lock = threading.RLock()
        self._handlers = {}
    
    def register(self, node_id: str, node) -> None:
        """Register a node in the network"""
        with self._lock:
            self.nodes[node_id] = node
            print(f"   📡 Node {node_id} joined the network")
    
    def unregister(self, node_id: str) -> None:
        with self._lock:
            if node_id in self.nodes:
                del self.nodes[node_id]
                print(f"   📡 Node {node_id} left the network")
    
    def broadcast(self, sender_id: str, msg_type: str, data: Dict) -> None:
        """Broadcast message to all nodes except sender"""
        with self._lock:
            recipients = {k: v for k, v in self.nodes.items() if k != sender_id}
        
        for node_id, node in recipients.items():
            if msg_type == "tx":
                node.receive_tx(data)
            elif msg_type == "block":
                node.receive_block(data)
            elif msg_type == "chain":
                node.receive_chain(data)
    
    def send_to(self, sender_id: str, target_id: str, msg_type: str, data: Dict) -> bool:
        """Send message to specific node"""
        with self._lock:
            if target_id in self.nodes:
                target = self.nodes[target_id]
                if msg_type == "tx":
                    target.receive_tx(data)
                elif msg_type == "block":
                    target.receive_block(data)
                return True
            return False
    
    def get_node_count(self) -> int:
        return len(self.nodes)
    
    def get_nodes(self) -> List[str]:
        return list(self.nodes.keys())
