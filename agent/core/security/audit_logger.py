import os
import json
import time
from datetime import datetime

class AuditLogger:
    def __init__(self, log_dir=None):
        if not log_dir:
            home = os.path.expanduser("~")
            log_dir = os.path.join(home, ".aether", "audit")
        
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        self.current_log_file = os.path.join(self.log_dir, f"audit_{datetime.now().strftime('%Y-%m')}.jsonl")

    def log_action(self, action_type, details, user_initiated=True):
        """
        Logs an immutable record of system changes or tool executions.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": action_type,
            "details": details,
            "user_initiated": user_initiated,
            "immutable_hash": "pending" # Placeholder for future blockchain/hash linking
        }
        
        with open(self.current_log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
            
    def get_recent_logs(self, limit=50):
        if not os.path.exists(self.current_log_file):
            return []
        
        with open(self.current_log_file, "r") as f:
            lines = f.readlines()
            return [json.loads(line) for line in lines[-limit:]]

audit_log = AuditLogger()
