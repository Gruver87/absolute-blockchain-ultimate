# network/gossip.py
import random
import threading
import requests
import time
from typing import List, Dict, Any

class GossipNode:
    def __init__(self, node_id: str = None):
        self.node_id = node_id or f"node_{random.randint(1000, 9999)}"
        self.peers: List[str] = []
        self.seen: set = set()
        self.lock = threading.RLock()
        self.running = False

    def add_peer(self, peer_url: str):
        with self.lock:
            if peer_url not in self.peers:
                self.peers.append(peer_url)

    def remove_peer(self, peer_url: str):
        with self.lock:
            if peer_url in self.peers:
                self.peers.remove(peer_url)

    def get_peers(self) -> List[str]:
        with self.lock:
            return self.peers.copy()

    def broadcast(self, path: str, data: Dict, timeout: int = 3):
        with self.lock:
            peers = self.peers.copy()
        for peer in peers:
            try:
                requests.post(peer + path, json=data, timeout=timeout)
            except:
                continue

    def gossip(self, path: str, data: Dict, hops: int = 2):
        data_id = f"{path}:{str(data)}"
        with self.lock:
            if data_id in self.seen:
                return
            self.seen.add(data_id)
            peers = self.peers.copy()

        if hops <= 0 or not peers:
            return

        # Выбираем 3 случайных пира
        selected = random.sample(peers, min(len(peers), 3))

        for peer in selected:
            try:
                requests.post(peer + path, json=data, timeout=2)
            except:
                continue

    def start_heartbeat(self, interval: int = 30):
        """Отправляет heartbeat peers"""
        def heartbeat_loop():
            while self.running:
                time.sleep(interval)
                self.broadcast("/api/peer/heartbeat", {"node_id": self.node_id})

        self.running = True
        thread = threading.Thread(target=heartbeat_loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False
