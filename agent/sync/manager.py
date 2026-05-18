import json
import hashlib

class SyncManager:
    def __init__(self):
        self.rules = {
            "tags": [], # e.g. "work", "personal"
            "types": ["shadow", "user"] # Fragment types to sync
        }

    def determine_sync_action(self, local_fragment, remote_fragment):
        """
        Deterministic merge strategy for simultaneous edits.
        """
        if not local_fragment and remote_fragment:
            return "download"
        if local_fragment and not remote_fragment:
            return "upload"
            
        local_hash = hashlib.sha256(json.dumps(local_fragment).encode()).hexdigest()
        remote_hash = hashlib.sha256(json.dumps(remote_fragment).encode()).hexdigest()
        
        if local_hash == remote_hash:
            return "skip"
            
        # Conflict resolution: Newest wins (based on modified timestamp)
        if local_fragment.get("modified_at", 0) > remote_fragment.get("modified_at", 0):
            return "upload"
        else:
            return "download"

    def apply_selective_sync(self, fragment):
        """Allow per-tag or per-fragment-type sync rules."""
        if fragment.get("type") not in self.rules["types"]:
            return False
            
        if self.rules["tags"]:
            # If tags are specified, fragment must match at least one
            fragment_tags = fragment.get("tags", [])
            if not any(tag in self.rules["tags"] for tag in fragment_tags):
                return False
                
        return True

sync_manager = SyncManager()
