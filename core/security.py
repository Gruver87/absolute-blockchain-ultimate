# core/security.py
import hashlib
import time
from typing import Dict, Set

class Security:
    """Security layer: signatures + replay protection + anti-spam"""
    
    def __init__(self):
        self.seen_transactions: Set[str] = set()
        self.blacklisted_peers: Set[str] = set()
    
    def verify_signature(self, tx: Dict) -> bool:
        """Verify transaction signature (ECDSA placeholder)"""
        expected = hashlib.sha256(
            f"{tx.get('from')}{tx.get('to')}{tx.get('amount')}".encode()
        ).hexdigest()
        return tx.get("signature") == expected
    
    def replay_protection(self, tx: Dict) -> bool:
        """Prevent replay attacks"""
        tx_hash = tx.get("hash") or self._calculate_hash(tx)
        if tx_hash in self.seen_transactions:
            return False
        self.seen_transactions.add(tx_hash)
        return True
    
    def validate_tx(self, tx: Dict) -> bool:
        """Full transaction validation"""
        if not self.verify_signature(tx):
            return False
        if not self.replay_protection(tx):
            return False
        return True
    
    def blacklist_peer(self, peer: str):
        self.blacklisted_peers.add(peer)
    
    def is_peer_blacklisted(self, peer: str) -> bool:
        return peer in self.blacklisted_peers
    
    def _calculate_hash(self, tx: Dict) -> str:
        data = f"{tx.get('from')}{tx.get('to')}{tx.get('amount')}{tx.get('nonce', 0)}"
        return hashlib.sha256(data.encode()).hexdigest()
