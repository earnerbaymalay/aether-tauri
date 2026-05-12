<div align="center">

# 📖 Aether — Usage Guide

*Everything you need to operate the neural workstation.*

</div>

---

## Table of Contents

1. [Launching Aether](#-launching-aether)
2. [Selecting a Neural Pathway](#-neural-pathways)
3. [OpenClaw Hybrid Bridge](#-openclaw-hybrid-bridge)
4. [Slash Commands](#-slash-commands)
5. [AetherVault — Neural Memory](#-aethervault)
6. [MCP Tool Integration](#-mcp-tool-integration)
7. [Nexus Shield](#-nexus-shield)
8. [Neural Monitor](#-neural-monitor)

---

## 🚀 Launching Aether

The recommended launch sequence ensures all services are online before Aether starts:

```bash
# Step 1 — Start the OpenClaw gateway (required for bridge mode)
openclaw gateway --port 18789 --force &

# Step 2 — Launch Aether (auto-starts Ollama if not running)
./aether.sh
```

`aether.sh` handles the following automatically:
- Checks if the `ollama` process is running. If not, it starts it via `systemctl` (Linux) or `ollama serve` (macOS/Windows).
- Sets `PYTHONPATH` to include the `agent/` directory for local Python imports.
- Launches `agent/aether_agent.py` as the agent core.

> **Note:** For Windows users, use the PowerShell installer: `powershell -ExecutionPolicy Bypass -File .\install-windows.ps1`

---

## 🧠 Neural Pathways

When you open the Tauri window, you are presented with four **Neural Pathway** cards. Each routes your session to a different specialized model.

| Pathway | Model | Ideal Tasks |
| :--- | :--- | :--- |
| **🤖 AGENT** | `hermes3:8b` | Tool use, system commands, web search, complex multi-step tasks |
| **⚡ TURBO** | `llama3.2:3b` | Fast Q&A, summaries, translations, and daily-use queries |
| **💻 CODE** | `qwen2.5-coder:3b` | Code generation, debugging, refactoring, review |
| **🧠 LOGIC** | `deepseek-r1:8b` | Architectural planning, deep reasoning, philosophical inquiry |

Click a card to initialize the xterm.js terminal and boot the agent with the selected model context.

> **Tip:** You can check available models at any time with `ollama list`.

---

## 🦾 OpenClaw Hybrid Bridge

Aether uses a **Hybrid Bridge** architecture. The UI, memory management, and local services remain in Aether, while actual intelligence and tool execution are offloaded to the **OpenClaw CLI**.

### Architecture Flow

```
User Input (xterm.js)
    │
    ▼
Aether Frontend (Tauri / TypeScript)
    │  invoke('send_to_agent')
    ▼
Aether Agent Core (Python)
    │  subprocess: openclaw agent --message "..."
    ▼
OpenClaw CLI → Ollama / MCP Servers
    │  stdout stream
    ▼
Terminal Output (streamed back line-by-line)
```

### Why the Bridge Exists

- **Full MCP Support:** OpenClaw natively handles Model Context Protocol servers (DuckDuckGo, memory, fetch, etc.)
- **Better Tool Loops:** OpenClaw's optimized ReAct loops handle multi-step tasks more reliably than a custom parser.
- **Unified Skills:** Any skill installed in your global OpenClaw config is automatically available in Aether.
- **Zero Maintenance:** You don't need to maintain a tool parser — the bridge delegates this entirely.

### Configuring the Bridge

Ensure `~/.openclaw/openclaw.json` has the correct model reference:

```bash
openclaw config set agents.defaults.model.primary "ollama/hermes3:8b"
openclaw gateway --port 18789 --force
```

---

## ⚡ Slash Commands

Inside the Aether terminal session, these slash commands are available:

| Command | Description |
| :--- | :--- |
| `/help` | Display the command reference table |
| `/settings` | Interactive configuration editor (models, threads, theme, vault path) |
| `/memory` | View the 10 most recent AetherVault memory fragments |
| `/health` | Full system vitals check: Vault, Models directory, Ollama status |
| `/auto-fix` | Paste an error message; the LOGIC model suggests a one-step repair command |
| `/clear` | Clear the terminal view and re-render the header panel |
| `/exit` | Gracefully terminate the agent session |

### `/settings` Reference

When you run `/settings`, an interactive editor appears. Enter the number of the field you want to change:

| # | Key | Default | Description |
| :- | :--- | :--- | :--- |
| 1 | Uncensored | `false` | Remove safety guardrails for the primary model |
| 2 | RAG | `true` | Enable AetherFS semantic search context injection |
| 3 | Threads | `6` | CPU threads for inference |
| 4 | Browser | `firefox` | Default browser for tool use |
| 5 | Theme | `cyan` | Rich terminal color theme |
| 6 | Log Level | `INFO` | Verbosity of `~/.aether/logs/aether.log` |
| 7 | Vault Path | `~/Documents/Vault` | Path to your AetherVault knowledge base |

Settings are persisted to `~/.aether/config.json`.

---

## 🗄️ AetherVault

AetherVault is a **persistent, markdown-based memory system** that enriches every session with long-term context.

### How It Works

1. **Fragment Storage:** Facts and preferences extracted from your conversations are saved as `.md` files in `<vault_path>/fragments/`.
2. **Shadow Monitor:** After every exchange, a background thread uses the TURBO model to silently extract key facts and save them as `shadow_*.md` fragments — without interrupting your session.
3. **RAG Context Injection:** At startup, the RAG engine indexes your entire vault and injects relevant context into the system prompt automatically (when `rag_enabled = true`).
4. **Manual Fragments:** You can save notes directly from the terminal (future `/save` command) or by placing `.md` files in your vault directory.

### Vault Priority

Aether uses the first path that exists, in this order:

```
~/Documents/Vault   (Obsidian default)
~/aether-vault      (Fallback)
~/.aether/config.json → vault_path  (Custom override via /settings)
```

### AetherLink (P2P Sync)

`AetherLink` (`agent/p2p_sync.py`) runs a listener on **port 8888** to synchronize memory fragments between Aether nodes (Desktop ↔ Droid).

```
~/.aether/
├── config.json          ← Runtime configuration
├── logs/
│   └── aether.log       ← Session logs
└── sessions/            ← Conversation histories (future)

~/Documents/Vault/        ← (or custom vault_path)
├── SYSTEM_PROFILE.md     ← High-level user profile
└── fragments/
    ├── shadow_*.md       ← Auto-extracted by Shadow Monitor
    ├── auto_*.md         ← Agent-saved memories
    └── *.md              ← Manual notes
```

---

## 🛠️ MCP Tool Integration

Aether supports the **Model Context Protocol (MCP)** through the `agent/mcp_client.py` module.

### Enabling MCP

In `/settings`, or by editing `~/.aether/config.json`:

```json
{
  "mcp_enabled": true,
  "mcp_servers": {
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    }
  }
}
```

MCP servers are started automatically on agent boot when `mcp_enabled` is `true`. Their tools are injected into the system prompt and are available to OpenClaw for execution.

---

## 🛡️ Nexus Shield

Nexus Shield is accessible from the System Panel via the **🛡️ Nexus Shield** button.

| Control | Description |
| :--- | :--- |
| **Privacy Shield** | Blocks telemetry, ads, and Cortana (Windows-focused) |
| **Gaming Mode** | Applies maximum power plan and network optimizations |
| **AI Bloat Killer** | Disables Copilot and Windows Recall |
| **Ghost Mode** | Enables dynamic background process management |
| **System Deep Clean** | Runs a full wipe of cache and temporary files |

Toggles invoke `run_nexus_optimization()` in the Tauri backend via the Rust command `run_nexus_optimization`. Status updates appear at the bottom of the panel.

---

## 📊 Neural Monitor

The Neural Monitor is a **real-time TUI dashboard** that runs independently of the main Aether window.

### Launching

```bash
# Option 1: Run directly
python3 tools/monitor.py

# Option 2: If installed as a system command
aether-monitor
```

### What It Tracks

| Category | Metrics |
| :--- | :--- |
| **Services** | Ollama (port 11434), OpenClaw (port 18789), LM Studio |
| **Processes** | Aether Agent (`aether_agent.py`), Tauri process, OpenClaw daemon |
| **Hardware** | Live CPU %, RAM usage %, and available memory |

> **Tip:** Run the monitor in a split terminal alongside your Aether session for a full operator view.
