import os
import json
import uuid
from datetime import datetime

class SessionManager:
    def __init__(self):
        home = os.path.expanduser("~")
        self.session_dir = os.path.join(home, ".aether", "sessions")
        os.makedirs(self.session_dir, exist_ok=True)
        self.current_session_id = None

    def new_session(self, name="Unnamed Session"):
        """Creates a new named conversation history."""
        self.current_session_id = str(uuid.uuid4())
        session_data = {
            "id": self.current_session_id,
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "history": []
        }
        self.save_session(session_data)
        return self.current_session_id

    def save_session(self, session_data):
        if not self.current_session_id:
            return
        
        filepath = os.path.join(self.session_dir, f"{self.current_session_id}.json")
        with open(filepath, "w") as f:
            json.dump(session_data, f, indent=2)

    def load_session(self, session_id):
        """Restores a conversation history."""
        filepath = os.path.join(self.session_dir, f"{session_id}.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                self.current_session_id = session_id
                return json.load(f)
        return None

    def list_sessions(self):
        sessions = []
        for filename in os.listdir(self.session_dir):
            if filename.endswith(".json"):
                with open(os.path.join(self.session_dir, filename), "r") as f:
                    data = json.load(f)
                    sessions.append({"id": data.get("id"), "name": data.get("name"), "created_at": data.get("created_at")})
        return sessions

session_manager = SessionManager()
