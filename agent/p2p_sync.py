"""
🔗 AetherLink Beta — Secure P2P Memory Sync for AetherVault.

Features:
  - Fernet envelope encryption (PBKDF2-derived key)
  - Length-prefixed message framing (no buffer truncation)
  - Conflict resolution with .conflict backups
  - mDNS peer discovery via zeroconf (graceful fallback)
  - Sync status tracking
"""

import os
import socket
import struct
import threading
import json
import hashlib
import time
import logging
from pathlib import Path
from datetime import datetime
from base64 import urlsafe_b64encode
from typing import Optional, Dict, Tuple

# Encryption
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# mDNS discovery (optional)
try:
    from zeroconf import ServiceInfo, ServiceBrowser, Zeroconf
    HAS_ZEROCONF = True
except ImportError:
    HAS_ZEROCONF = False

logger = logging.getLogger("Aether.Link")

# --- Constants ---
AETHERLINK_SERVICE_TYPE = "_aetherlink._tcp.local."
AETHERLINK_SALT = b"aetherlink_v2"
HEADER_SIZE = 4  # 4-byte big-endian length prefix


# ─── Crypto helpers ──────────────────────────────────────────────

def _derive_fernet_key(secret: str) -> bytes:
    """Derive a Fernet-compatible 32-byte key from a shared secret via PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=AETHERLINK_SALT,
        iterations=480_000,
    )
    return urlsafe_b64encode(kdf.derive(secret.encode()))


# ─── Framing helpers ─────────────────────────────────────────────

def _send_msg(sock: socket.socket, data: dict, fernet: Fernet):
    """Encrypt + length-prefix + send a JSON-serialisable dict."""
    payload = fernet.encrypt(json.dumps(data).encode())
    length = struct.pack("!I", len(payload))
    sock.sendall(length + payload)


def _recv_msg(sock: socket.socket, fernet: Fernet) -> Optional[dict]:
    """Receive a length-prefixed encrypted message; return decoded dict or None."""
    raw_len = _recv_exact(sock, HEADER_SIZE)
    if not raw_len:
        return None
    msg_len = struct.unpack("!I", raw_len)[0]
    if msg_len > 50 * 1024 * 1024:  # 50 MB safety cap
        logger.warning("Message exceeds 50 MB cap — dropping connection.")
        return None
    encrypted = _recv_exact(sock, msg_len)
    if not encrypted:
        return None
    try:
        decrypted = fernet.decrypt(encrypted)
        return json.loads(decrypted)
    except InvalidToken:
        logger.warning("Decryption failed — peer likely has wrong key.")
        return None


def _recv_exact(sock: socket.socket, n: int) -> Optional[bytes]:
    """Read exactly n bytes from sock, or return None on EOF/error."""
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return None
        buf.extend(chunk)
    return bytes(buf)


# ─── mDNS Discovery ─────────────────────────────────────────────

class AetherLinkDiscovery:
    """
    Advertises this node and discovers peers on the LAN using mDNS.
    Gracefully no-ops if zeroconf is not installed.
    """

    def __init__(self, port: int, node_name: str = None):
        self.port = port
        self.node_name = node_name or socket.gethostname()
        self.discovered_peers: Dict[str, Tuple[str, int]] = {}  # name → (ip, port)
        self._zc = None
        self._browser = None
        self._info = None

    def start(self):
        if not HAS_ZEROCONF:
            logger.info("zeroconf not installed — mDNS discovery disabled. Install with: pip install zeroconf")
            return

        try:
            self._zc = Zeroconf()

            # Register our own service
            local_ip = self._get_local_ip()
            self._info = ServiceInfo(
                AETHERLINK_SERVICE_TYPE,
                f"{self.node_name}.{AETHERLINK_SERVICE_TYPE}",
                addresses=[socket.inet_aton(local_ip)],
                port=self.port,
                properties={"version": "2"},
                server=f"{self.node_name}.local.",
            )
            self._zc.register_service(self._info)
            logger.info(f"📡 AetherLink mDNS: advertising on {local_ip}:{self.port}")

            # Browse for peers
            self._browser = ServiceBrowser(self._zc, AETHERLINK_SERVICE_TYPE, self)
        except Exception as e:
            logger.warning(f"mDNS discovery startup failed: {e}")

    @staticmethod
    def _get_local_ip() -> str:
        """Best-effort local LAN IP detection."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    # ── ServiceBrowser callbacks ──
    def add_service(self, zc, service_type, name):
        info = zc.get_service_info(service_type, name)
        if info and info.parsed_addresses():
            peer_ip = info.parsed_addresses()[0]
            peer_port = info.port
            if peer_ip != self._get_local_ip() or peer_port != self.port:
                self.discovered_peers[name] = (peer_ip, peer_port)
                logger.info(f"🔗 AetherLink peer discovered: {name} @ {peer_ip}:{peer_port}")

    def remove_service(self, zc, service_type, name):
        self.discovered_peers.pop(name, None)
        logger.info(f"🔌 AetherLink peer removed: {name}")

    def update_service(self, zc, service_type, name):
        self.add_service(zc, service_type, name)

    def stop(self):
        if self._zc:
            if self._info:
                self._zc.unregister_service(self._info)
            self._zc.close()


# ─── AetherLink Core ─────────────────────────────────────────────

class AetherLink:
    """
    AetherLink Beta: Encrypted, discoverable, conflict-aware P2P sync
    for AetherVault memory fragments.
    """

    def __init__(self, vault_path, port=8888, secret_key="aether_proto"):
        self.vault_path = Path(vault_path)
        self.port = port
        self.secret_key = secret_key
        self.running = False
        self.fernet = Fernet(_derive_fernet_key(secret_key))

        # Discovery
        self.discovery = AetherLinkDiscovery(port)

        # Sync tracking
        self.last_sync: Dict[str, datetime] = {}   # peer_ip:port → last sync time
        self.sync_stats: Dict[str, int] = {"sent": 0, "received": 0, "conflicts": 0}

        self._server_socket = None
        self._auto_sync_thread = None
        self._auto_sync_interval = 300  # 5 minutes

    # ── File helpers ──

    def _get_file_hash(self, path) -> str:
        hasher = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _build_manifest(self) -> dict:
        """Build {relative_path: {hash, mtime}} for all vault markdown files."""
        manifest = {}
        for p in self.vault_path.rglob("*.md"):
            if ".conflict." in p.name:
                continue  # Skip conflict backups
            rel = str(p.relative_to(self.vault_path))
            manifest[rel] = {
                "hash": self._get_file_hash(p),
                "mtime": p.stat().st_mtime,
            }
        return manifest

    # ── Server ──

    def start_server(self):
        """Start the TCP listener for incoming sync requests."""
        self.running = True
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        for _ in range(10):
            try:
                self._server_socket.bind(('0.0.0.0', self.port))
                logger.info(f"📡 AetherLink listening on port {self.port}")
                break
            except OSError:
                self.port += 1
        else:
            logger.error("AetherLink: Could not bind to any port in range.")
            self.running = False
            return

        # Update discovery port if it shifted
        self.discovery.port = self.port

        threading.Thread(target=self._run_listener, daemon=True, name="AetherLink-Listener").start()

    def _run_listener(self):
        self._server_socket.listen(5)
        while self.running:
            try:
                self._server_socket.settimeout(1.0)
                conn, addr = self._server_socket.accept()
                threading.Thread(
                    target=self._handle_client, args=(conn, addr),
                    daemon=True, name=f"AetherLink-Client-{addr}"
                ).start()
            except socket.timeout:
                continue
            except OSError:
                break

    def _handle_client(self, conn, addr):
        with conn:
            try:
                msg = _recv_msg(conn, self.fernet)
                if not msg:
                    return  # Decryption failed or bad framing

                if msg["type"] == "sync_manifest":
                    manifest = self._build_manifest()
                    _send_msg(conn, {"type": "manifest", "files": manifest}, self.fernet)

                elif msg["type"] == "get_file":
                    filename = msg["filename"]
                    safe_path = (self.vault_path / filename).resolve()
                    # Path traversal guard
                    if not str(safe_path).startswith(str(self.vault_path.resolve())):
                        _send_msg(conn, {"type": "error", "message": "Path traversal blocked"}, self.fernet)
                        return
                    if safe_path.exists():
                        content = safe_path.read_text(encoding="utf-8")
                        _send_msg(conn, {"type": "file_data", "content": content}, self.fernet)
                    else:
                        _send_msg(conn, {"type": "error", "message": "File not found"}, self.fernet)

            except Exception as e:
                logger.debug(f"AetherLink client handler error ({addr}): {e}")

    # ── Sync client ──

    def sync_with_peer(self, ip: str, peer_port: int = 8888) -> dict:
        """
        Sync vault with a remote peer. Returns stats dict.
        """
        peer_key = f"{ip}:{peer_port}"
        stats = {"fetched": 0, "skipped": 0, "conflicts": 0}
        logger.info(f"🔄 AetherLink syncing with {peer_key}...")

        try:
            # Step 1: Get remote manifest
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((ip, peer_port))
                _send_msg(s, {"type": "sync_manifest"}, self.fernet)
                resp = _recv_msg(s, self.fernet)

            if not resp or resp.get("type") != "manifest":
                logger.error(f"Sync with {peer_key}: bad manifest response")
                return stats

            peer_manifest = resp["files"]
            local_manifest = self._build_manifest()

            # Step 2: Compare and fetch
            for filename, peer_info in peer_manifest.items():
                peer_hash = peer_info["hash"]
                peer_mtime = peer_info["mtime"]
                local_info = local_manifest.get(filename)

                if local_info and local_info["hash"] == peer_hash:
                    stats["skipped"] += 1
                    continue  # Already in sync

                if local_info and local_info["mtime"] >= peer_mtime:
                    stats["skipped"] += 1
                    continue  # Local is newer or same age — keep ours

                # Remote is newer (or we don't have it)
                if local_info:
                    # Conflict: we have a different version, remote is newer
                    self._backup_conflict(filename)
                    stats["conflicts"] += 1
                    self.sync_stats["conflicts"] += 1

                # Fetch the file
                content = self._fetch_file(ip, peer_port, filename)
                if content is not None:
                    local_file = self.vault_path / filename
                    local_file.parent.mkdir(parents=True, exist_ok=True)
                    local_file.write_text(content, encoding="utf-8")
                    stats["fetched"] += 1
                    self.sync_stats["received"] += 1

            self.last_sync[peer_key] = datetime.now()
            logger.info(f"✅ Sync with {peer_key} complete: {stats}")

        except Exception as e:
            logger.error(f"❌ Sync with {peer_key} failed: {e}")

        return stats

    def _fetch_file(self, ip: str, port: int, filename: str) -> Optional[str]:
        """Fetch a single file from a peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(30)
                s.connect((ip, port))
                _send_msg(s, {"type": "get_file", "filename": filename}, self.fernet)
                resp = _recv_msg(s, self.fernet)
                if resp and resp.get("type") == "file_data":
                    return resp["content"]
        except Exception as e:
            logger.error(f"Failed to fetch {filename} from {ip}:{port}: {e}")
        return None

    def _backup_conflict(self, filename: str):
        """Backup the local version before overwriting with remote."""
        local_file = self.vault_path / filename
        if not local_file.exists():
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = local_file.stem
        suffix = local_file.suffix
        backup_name = f"{stem}.conflict.{timestamp}{suffix}"
        backup_path = local_file.parent / backup_name
        backup_path.write_text(local_file.read_text(encoding="utf-8"), encoding="utf-8")
        logger.info(f"📋 Conflict backup: {backup_name}")

    # ── Auto-sync ──

    def auto_sync(self):
        """Sync with all discovered peers."""
        if not self.discovery.discovered_peers:
            return
        for name, (ip, port) in list(self.discovery.discovered_peers.items()):
            try:
                self.sync_with_peer(ip, port)
            except Exception as e:
                logger.debug(f"Auto-sync with {name} failed: {e}")

    def start_auto_sync(self, interval: int = 300):
        """Start periodic background sync every `interval` seconds."""
        self._auto_sync_interval = interval

        def _loop():
            while self.running:
                time.sleep(self._auto_sync_interval)
                if self.running and self.discovery.discovered_peers:
                    logger.debug("AetherLink: running periodic auto-sync...")
                    self.auto_sync()

        self._auto_sync_thread = threading.Thread(target=_loop, daemon=True, name="AetherLink-AutoSync")
        self._auto_sync_thread.start()

    # ── Status ──

    def get_sync_status(self) -> dict:
        """Return sync status for display."""
        return {
            "running": self.running,
            "port": self.port,
            "discovered_peers": {
                name: {"ip": ip, "port": port}
                for name, (ip, port) in self.discovery.discovered_peers.items()
            },
            "last_sync": {
                peer: ts.strftime("%Y-%m-%d %H:%M:%S")
                for peer, ts in self.last_sync.items()
            },
            "stats": dict(self.sync_stats),
        }

    # ── Lifecycle ──

    def stop(self):
        self.running = False
        self.discovery.stop()
        if self._server_socket:
            try:
                self._server_socket.close()
            except Exception:
                pass


if __name__ == "__main__":
    # Minimal test: start two instances on localhost
    import tempfile, shutil

    vault_a = Path(tempfile.mkdtemp(prefix="aetherlink_a_"))
    vault_b = Path(tempfile.mkdtemp(prefix="aetherlink_b_"))

    # Write a test file in vault A
    (vault_a / "test_note.md").write_text("# Hello from Node A\nThis is a test.", encoding="utf-8")

    link_a = AetherLink(vault_a, port=18880)
    link_b = AetherLink(vault_b, port=18881)

    link_a.start_server()
    time.sleep(0.5)

    stats = link_b.sync_with_peer("127.0.0.1", link_a.port)
    print(f"Sync stats: {stats}")

    synced = (vault_b / "test_note.md").read_text(encoding="utf-8")
    assert "Hello from Node A" in synced, "Sync failed!"
    print("✅ AetherLink Beta self-test passed.")

    link_a.stop()
    link_b.stop()
    shutil.rmtree(vault_a)
    shutil.rmtree(vault_b)
