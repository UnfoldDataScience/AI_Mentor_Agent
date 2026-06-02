import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

SESSIONS_DIR = "sessions"


class SessionStorage:
    def __init__(self):
        os.makedirs(SESSIONS_DIR, exist_ok=True)

    def new_session_id(self) -> str:
        return str(uuid.uuid4())[:8]

    def save_session(
        self,
        session_id: str,
        messages: List[Dict],
        metadata: Dict = None,
    ) -> None:
        data = {
            "session_id": session_id,
            "updated_at": datetime.now().isoformat(),
            "messages": messages,
            "metadata": metadata or {},
        }
        path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_session(self, session_id: str) -> Optional[Dict]:
        path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_sessions(self) -> List[Dict]:
        sessions = []
        if not os.path.exists(SESSIONS_DIR):
            return sessions
        for filename in sorted(os.listdir(SESSIONS_DIR), reverse=True):
            if not filename.endswith(".json"):
                continue
            path = os.path.join(SESSIONS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            sessions.append(
                {
                    "session_id": data["session_id"],
                    "updated_at": data.get("updated_at", ""),
                    "message_count": len(data["messages"]),
                    "metadata": data.get("metadata", {}),
                }
            )
        return sessions

    def delete_session(self, session_id: str) -> None:
        path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
        if os.path.exists(path):
            os.remove(path)
