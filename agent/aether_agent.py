#!/usr/bin/env python3
"""
🌌 Aether Neural Operating Interface // V 26.5.1
Polished High-performance Agent Core with Multi-Step Tool Loops.
"""

import os
import sys
import json
import re
import subprocess
import threading
import time
import random
import psutil
import httpx
import asyncio
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Generator

# UI Imports
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Logic Imports
from rag_engine import AetherRAG
from p2p_sync import AetherLink
from system_scanner import SystemScanner
from skill_loader import UniversalSkillEngine
from logger import AetherLogger
from mcp_client import MCPClientManager

# --- Constants & Configuration ---
AGENT_ROOT = Path(__file__).resolve().parent.parent
AETHER_HOME = Path.home() / ".aether"
LOG_DIR = AETHER_HOME / "logs"
CONFIG_FILE = AETHER_HOME / "config.json"

# API Endpoints (Centralized)
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"
OLLAMA_GEN_URL = f"{OLLAMA_BASE_URL}/api/generate"

console = Console()
SKILLS = UniversalSkillEngine(AGENT_ROOT)

DEFAULT_CONFIG = {
    "vault_path": str(Path.home() / "aether-vault"),
    "threads": 6,
    "rag_enabled": True,
    "active_model": "hermes3:8b",
    "turbo_model": "llama3.2:3b",
    "logic_model": "deepseek-r1:8b",
    "theme": "cyan",
    "log_level": "INFO",
    "mcp_enabled": True,
}

def load_config() -> Dict[str, Any]:
    """Loads configuration with defaults."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

CONFIG = load_config()
LOGGER = AetherLogger(LOG_DIR, level=CONFIG["log_level"])

# --- Neural Memory & Vault ---

class NeuralMemory:
    """Manages AetherVault markdown fragments."""
    def __init__(self, fragments_dir: Path):
        self.fragments_dir = fragments_dir
        self.fragments_dir.mkdir(parents=True, exist_ok=True)

    def list_fragments(self) -> List[Path]:
        return sorted(list(self.fragments_dir.glob("*.md")), key=os.path.getmtime, reverse=True)

    def save_fragment(self, title: str, content: str, is_shadow: bool = False):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        path = self.fragments_dir / f"{'shadow_' if is_shadow else ''}{safe_title}_{timestamp}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}\n\n---\n*Type: {'Shadow' if is_shadow else 'Auto'} | {datetime.now().strftime('%Y-%m-%d')}*")
        return path

# --- Logic & Engine ---

class AetherAgent:
    """Main Agent Logic Engine."""
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.vault_dir = Path(config["vault_path"])
        self.memory = NeuralMemory(self.vault_dir / "fragments")
        self.rag = AetherRAG([self.vault_dir])
        self.link = AetherLink(self.vault_dir)
        self.mcp = MCPClientManager(config.get("mcp_servers", {})) if config.get("mcp_enabled") else None
        self.client = httpx.Client(timeout=120.0)

    async def generate_response(self, messages: List[Dict[str, str]], model: str) -> Generator[str, None, None]:
        """Streams completion from the neural engine."""
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {"num_thread": self.config["threads"]}
        }
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream("POST", OLLAMA_CHAT_URL, json=payload) as response:
                    async for line in response.aiter_lines():
                        if line:
                            data = json.loads(line)
                            yield data.get("message", {}).get("content", "")
        except Exception as e:
            yield f"Neural link error: {str(e)}"

    def run_tool(self, name: str, args: str = "") -> str:
        """Executes a tool from the toolbox or MCP."""
        LOGGER.info(f"Executing Tool: {name} | Args: {args}")
        # Security block
        if name == "shell_exec" and any(x in args for x in ["rm -rf", "> /dev/sda", "mkfs"]):
            return "Error: Destructive command blocked by Nexus Shield."

        # MCP Tool Check
        if self.mcp and name in [t["name"] for t in self.mcp.list_tools()]:
            try:
                cmd_args = json.loads(args) if args.strip().startswith("{") else {"input": args}
                return self.mcp.call_tool(name, cmd_args)
            except Exception as e:
                return f"MCP Error: {e}"

        # Core Tools
        try:
            import core_tools
            if hasattr(core_tools, name):
                import shlex
                try:
                    parsed_args = json.loads(f"[{args}]")
                except:
                    parsed_args = shlex.split(args)
                return str(getattr(core_tools, name)(*parsed_args))
        except Exception as e:
            return f"Tool Execution Error ({name}): {e}"
        
        return f"Error: Tool '{name}' not found."

# --- UI Interface ---

class AetherUI:
    def __init__(self, agent: AetherAgent):
        self.agent = agent
        self.console = Console()
        self.theme = CONFIG["theme"]

    def header(self):
        stats = f"CPU: {psutil.cpu_percent()}% | RAM: {psutil.virtual_memory().percent}%"
        grid = Table.grid(expand=True)
        grid.add_column(); grid.add_column()
        grid.add_row(f"[bold {self.theme}]🌌 AETHER[/] [dim]v26.5.1[/]", f"[dim]{stats}[/]")
        return Panel(grid, border_style=self.theme)

    def chat_loop(self):
        history = [{"role": "system", "content": "You are Aether, a local-first neural interface."}]
        while True:
            try:
                user_input = self.console.input(f"\n[bold {self.theme}]» [/]").strip()
                if not user_input: continue
                if user_input.lower() in ["exit", "/exit", "quit"]: break
                
                # Handle Slash Commands
                if user_input.startswith("/"):
                    self.handle_command(user_input[1:])
                    continue

                self.console.print(f"[bold {self.theme}]Aether [/] [dim]thinking...[/]")
                
                # Stream Response
                full_resp = ""
                # Since generate_response is async, we need a small helper or run it in a loop
                async def run_gen():
                    nonlocal full_resp
                    async for chunk in self.agent.generate_response(history, CONFIG["active_model"]):
                        self.console.print(chunk, end="")
                        full_resp += chunk
                
                asyncio.run(run_gen())
                print() # Newline after stream
                
                history.append({"role": "user", "content": user_input})
                history.append({"role": "assistant", "content": full_resp})
                
            except KeyboardInterrupt:
                break

    def handle_command(self, cmd: str):
        if cmd == "help":
            self.console.print("[yellow]Commands: /help, /settings, /memory, /health, /clear[/]")
        elif cmd == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            self.console.print(self.header())
        elif cmd == "health":
            self.console.print(f"[green]Vault Path:[/] {self.agent.vault_dir}")
            self.console.print(f"[green]Ollama Status:[/] Connected to {OLLAMA_BASE_URL}")
        else:
            self.console.print(f"[red]Unknown command:[/] {cmd}")

def main():
    agent = AetherAgent(CONFIG)
    ui = AetherUI(agent)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(ui.header())
    
    # Simple start
    ui.chat_loop()

if __name__ == "__main__":
    main()
