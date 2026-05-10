import os
import socket
import threading
import json
import time
from pathlib import Path

class AetherLink:
    def __init__(self, vault_path, port=8888):
        self.vault_path = Path(vault_path)
        self.port = port
        self.running = False
        self.peers = set()

    def start_server(self):
        """Starts a background listener for P2P sync with automatic port failover."""
        self.running = True
        # Create socket here to catch bind error early
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Try to bind, incrementing port if occupied
        max_retries = 10
        for _ in range(max_retries):
            try:
                self.server_socket.bind(('0.0.0.0', self.port))
                break
            except OSError as e:
                if e.errno == 10048: # Address already in use
                    self.port += 1
                else:
                    raise
        
        threading.Thread(target=self._run_listener, daemon=True).start()

    def _run_listener(self):
        with self.server_socket as s:
            s.listen()
            while self.running:
                try:
                    s.settimeout(1.0) # Allow checking self.running periodically
                    conn, addr = s.accept()
                except socket.timeout:
                    continue
                except OSError:
                    break
                    
                with conn:
                    data = conn.recv(1024)
                    if data:
                        try:
                            msg = json.loads(data.decode())
                            if msg['type'] == 'sync_request':
                                self._handle_sync(conn)
                        except json.JSONDecodeError:
                            pass

    def _handle_sync(self, conn):
        # Implementation for actual file transfer would go here
        # Simplified: Send list of files in vault
        files = [f.name for f in self.vault_path.glob("*.md")]
        conn.sendall(json.dumps({"type": "file_list", "files": files}).encode())

    def broadcast_presence(self):
        """Simulates finding other Aether instances on the local network."""
        # Real implementation would use UDP discovery
        pass

    def sync_with_peer(self, ip):
        """Syncs the local vault with a peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, self.port))
                s.sendall(json.dumps({"type": "sync_request"}).encode())
                data = s.recv(4096)
                return json.loads(data.decode())
        except Exception as e:
            return {"error": str(e)}
