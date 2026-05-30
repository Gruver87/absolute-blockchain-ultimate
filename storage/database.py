# storage/database.py
import json
import os
from typing import Dict, Any, Optional, List


class Database:
    """Простое хранилище для тестов"""

    def __init__(self, path: str = "test_data.json"):
        self.path = path
        self._data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except:
                return {"blocks": []}
        return {"blocks": []}

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self._data, f, indent=2)

    def put_block(self, number: int, block: Dict):
        self._data["blocks"].append(block)
        self._save()

    def get_all_blocks(self) -> List[Dict]:
        return self._data.get("blocks", [])

    def get_block(self, number: int) -> Optional[Dict]:
        for block in self._data.get("blocks", []):
            if block.get("block_number") == number:
                return block
        return None

    def clear(self):
        self._data = {"blocks": []}
        self._save()
