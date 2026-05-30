# geth_p2p/hardening.py
import time
import threading
from typing import Dict, List, Set

class PeerScore:
    """Peer scoring system — good behavior → score up, bad → ban"""
    
    def __init__(self):
        self.scores: Dict[str, int] = {}
        self.banned: Set[str] = set()
    
    def reward(self, peer: str, points: int = 1):
        if peer in self.banned:
            return
        self.scores[peer] = self.scores.get(peer, 0) + points
    
    def punish(self, peer: str, points: int = 5):
        if peer in self.banned:
            return
        self.scores[peer] = self.scores.get(peer, 0) - points
        if self.scores[peer] < -20:
            self.banned.add(peer)
    
    def is_banned(self, peer: str) -> bool:
        return peer in self.banned
    
    def get_score(self, peer: str) -> int:
        return self.scores.get(peer, 0)

class AntiEclipseProtection:
    """Protection against eclipse attacks"""
    
    def __init__(self):
        self._peers: Set[str] = set()
        self._trusted_seeds: Set[str] = set()
        self._lock = threading.RLock()
    
    def add_seed(self, seed: str):
        with self._lock:
            self._trusted_seeds.add(seed)
    
    def add_peer(self, peer: str):
        with self._lock:
            self._peers.add(peer)
    
    def get_diverse_peers(self, count: int = 5) -> List[str]:
        """Return peers from different IP ranges"""
        with self._lock:
            # Simple diversity: mix trusted seeds and regular peers
            all_peers = list(self._trusted_seeds) + list(self._peers)
            return all_peers[:count]
    
    def is_eclipsed(self) -> bool:
        """Check if node is under eclipse attack"""
        return len(self._peers) < 3 and len(self._trusted_seeds) == 0
