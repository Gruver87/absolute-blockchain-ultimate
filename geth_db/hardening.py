# geth_db/hardening.py
import json
import os
import threading
import time
from typing import Dict, Any, Optional

class WriteAheadLog:
    """Write-ahead log for crash recovery"""
    
    def __init__(self, path: str = "wal.log"):
        self.path = path
        self._lock = threading.RLock()
        # Create directory if needed
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._init_log()
    
    def _init_log(self):
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)
    
    def write(self, operation: str, data: Dict):
        with self._lock:
            with open(self.path, "r") as f:
                log = json.load(f)
            log.append({"op": operation, "data": data, "ts": time.time()})
            with open(self.path, "w") as f:
                json.dump(log, f)
    
    def recover(self) -> list:
        with self._lock:
            with open(self.path, "r") as f:
                return json.load(f)

class HardenedDatabase:
    """Database with crash recovery and snapshot support"""
    
    def __init__(self, path: str = "hardened_db"):
        self.path = path
        os.makedirs(path, exist_ok=True)
        self.wal = WriteAheadLog(os.path.join(path, "wal.log"))
        self._data: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._recover()
    
    def _recover(self):
        """Recover from WAL after crash"""
        ops = self.wal.recover()
        for op in ops:
            if op["op"] == "put":
                self._data[op["data"]["key"]] = op["data"]["value"]
        self._save_snapshot()
    
    def _save_snapshot(self):
        snapshot_path = os.path.join(self.path, f"snapshot_{int(time.time())}.json")
        with open(snapshot_path, "w") as f:
            json.dump(self._data, f)
    
    def put(self, key: str, value: Any):
        with self._lock:
            self.wal.write("put", {"key": key, "value": value})
            self._data[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        return self._data.get(key)
