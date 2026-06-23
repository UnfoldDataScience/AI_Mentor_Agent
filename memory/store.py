import json
import os
import uuid
from datetime import datetime
from typing import Dict, List

MEMORY_DIR = "memory"
MEMORY_FILE = os.path.join(MEMORY_DIR, "user_memory.json")


class MemoryStore:
    def __init__(self):
        os.makedirs(MEMORY_DIR, exist_ok=True)

    def _load(self) -> List[Dict]:
        if not os.path.exists(MEMORY_FILE):
            return []
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("memories", [])

    def _save(self, memories: List[Dict]) -> None:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump({"memories": memories}, f, indent=2, ensure_ascii=False)

    def add(self, content: str) -> Dict:
        memories = self._load()
        entry = {
            "id": str(uuid.uuid4())[:8],
            "content": content,
            "created_at": datetime.now().isoformat(),
        }
        memories.append(entry)
        self._save(memories)
        return entry

    def get_all(self) -> List[Dict]:
        return self._load()

    def delete(self, memory_id: str) -> None:
        memories = [m for m in self._load() if m["id"] != memory_id]
        self._save(memories)

    def format_for_prompt(self) -> str:
        memories = self.get_all()
        if not memories:
            return ""
        return "\n".join(f"- {m['content']}" for m in memories)
