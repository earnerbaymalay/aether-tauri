import os
import socket
import threading
import json
import hashlib
import time
from pathlib import Path

class AetherLink:
    """
    Enhanced AetherLink: Secure, local P2P sync for AetherVault.
    """
    def __init__(self, vault_path, port=8888, secret_key="aether_proto"):
        self.vault_path = Path(vault_path)
        self.port = port
        self.secret_key = secret_key
        self.running = False
        self.peers = set()

    def _get_file_hash(self, path):
        hasher = hashlib.md5()
        with open(path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def start_server(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        for _ in range(10):
            try:
                self.server_socket.bind(('0.0.0.0', self.port))
                print(f"📡 AetherLink Listening on port {self.port}")
                break
            except OSError:
                self.port += 1
        
        threading.Thread(target=self._run_listener, daemon=True).start()

    def _run_listener(self):
        self.server_socket.listen()
        while self.running:
            try:
                self.server_socket.settimeout(1.0)
                conn, addr = self.server_socket.accept()
                threading.Thread(target=self._handle_client, args=(conn,)).start()
            except socket.timeout:
                continue
            except OSError:
                break

    def _handle_client(self, conn):
        with conn:
            try:
                data = conn.recv(1024).decode()
                msg = json.loads(data)
                
                if msg.get('key') != self.secret_key:
                    return # Authentication fail
                    
                if msg['type'] == 'sync_list':
                    # Send list of files and hashes
                    manifest = {f.name: self._get_file_hash(f) for f in self.vault_path.glob("**/*.md")}
                    conn.sendall(json.dumps({"type": "manifest", "files": manifest}).encode())
                
                elif msg['type'] == 'get_file':
                    # Send file content
                    filename = msg['filename']
                    safe_path = (self.vault_path / filename).resolve()
                    if self.vault_path in safe_path.parents:
                        content = safe_path.read_text(encoding="utf-8")
                        conn.sendall(json.dumps({"type": "file_data", "content": content}).encode())
            except:
                pass

    def sync_with_peer(self, ip, peer_port=8888):
        print(f"🔄 Syncing with peer {ip}:{peer_port}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, peer_port))
                s.sendall(json.dumps({"type": "sync_list", "key": self.secret_key}).encode())
                
                resp = s.recv(4096).decode()
                peer_manifest = json.loads(resp)['files']
                
                for filename, peer_hash in peer_manifest.items():
                    local_file = self.vault_path / filename
                    if not local_file.exists() or self._get_file_hash(local_file) != peer_hash:
                        print(f"  📥 Fetching update for: {filename}")
                        # Request specific file
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                            s2.connect((ip, peer_port))
                            s2.sendall(json.dumps({"type": "get_file", "filename": filename, "key": self.secret_key}).encode())
                            f_resp = s2.recv(1000000).decode() # Large buffer for content
                            content = json.loads(f_resp)['content']
                            local_file.parent.mkdir(parents=True, exist_ok=True)
                            local_file.write_text(content, encoding="utf-8")
                print("✅ Sync Complete.")
        except Exception as e:
            print(f"❌ Sync failed: {e}")

if __name__ == "__main__":
    # Test script
    link = AetherLink("aethervault")
    # link.start_server()
    # time.sleep(1)
    # link.sync_with_peer("127.0.0.1", link.port)
