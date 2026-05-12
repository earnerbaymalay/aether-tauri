<div align="center">

# 🌌 Aether — Ecosystem Guide

*The complete picture of all Aether nodes, shared services, and the unified vision.*

</div>

---

## 🏛️ Unified Architecture

The Aether project is built on a **Brain–Nervous System–Hands** pattern that scales from a mobile shell to a full desktop workstation:

```
┌─────────────────────────────────────────────────────────────────────┐
│                           🧠  THE BRAIN                             │
│            Local LLMs (Ollama): hermes3, qwen, deepseek             │
└─────────────────────────────────┬───────────────────────────────────┘
                                  │
┌─────────────────────────────────▼───────────────────────────────────┐
│                       ⚡  THE NERVOUS SYSTEM                         │
│      OpenClaw Hybrid Bridge + MCP Orchestration + AetherLink P2P    │
└──────────────────┬──────────────────────────────┬────────────────────┘
                   │                              │
┌──────────────────▼──────────────┐  ┌────────────▼───────────────────┐
│       🖥️  Aether-Tauri          │  │       📱  Aether-Droid          │
│   Tauri (Rust) + TypeScript     │  │   Termux (Bash) + Python        │
│   Full workstation UI           │  │   Mobile-optimized agent        │
└─────────────────────────────────┘  └────────────────────────────────┘
                   │                              │
┌──────────────────▼──────────────────────────────▼────────────────────┐
│                       🛠️  THE HANDS                                   │
│     Toolbox Scripts · MCP Servers · Nexus Shield · AetherFS           │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 The Workstations

### 🖥️ Aether-Tauri (`aether-tauri`)

The primary cross-platform neural workstation.

| Property | Detail |
| :--- | :--- |
| **Platforms** | Linux · Windows · macOS |
| **Frontend** | TypeScript + xterm.js (Tauri WebView) |
| **Backend** | Rust (Tauri native commands) |
| **Agent Core** | Python 3.10+ |
| **Inference** | Ollama (primary) · LM Studio (optional) · llama.cpp (optional) |
| **Key Features** | Multi-tier Neural Pathways, AetherVault, Nexus Shield, AetherFS, Aether Eye, Neural Monitor |

### 📱 Aether-Droid (`aether-droid`)

The lightweight mobile workstation for on-the-go agentic workflows.

| Property | Detail |
| :--- | :--- |
| **Platform** | Android (via Termux) |
| **Stack** | Bash · Python · `gum` (TUI) |
| **Key Features** | Mobile-optimized agent, battery management, tool use, AetherVault sync via AetherLink |
| **Target** | Automation tasks, voice-to-text pipelines, remote device control |

---

## 🗄️ AetherVault — Shared Sovereign Memory

AetherVault is the **cross-node knowledge layer** that ensures your AI partner learns from every interaction, regardless of device.

### Design Principles

- **Markdown-First:** All knowledge is stored as human-readable `.md` files — compatible with Obsidian, Bear, Logseq, or any Markdown editor.
- **Portable:** The vault is a plain directory. Back it up, version it with Git, or symlink it to a cloud folder if desired.
- **No LLM vendor lock-in:** The vault is agnostic to which model generated the content.

### Fragment Types

| Prefix | Type | Source |
| :--- | :--- | :--- |
| `shadow_*.md` | Auto-distilled | Background Shadow Monitor (TURBO model, silent) |
| `auto_*.md` | Agent-saved | Explicitly saved by the agent during a task |
| `*.md` | Manual | User-authored or imported Markdown notes |

### `SYSTEM_PROFILE.md`

A high-level profile document written by Aether to summarize persistent user preferences, recurring patterns, and key facts — analogous to a `CLAUDE.md` but for the personal context layer.

---

## 🔗 AetherLink — P2P Cross-Device Sync

AetherLink (`agent/p2p_sync.py`) provides **encrypted peer-to-peer synchronization** of vault fragments between nodes.

```
Aether-Tauri (port 8888)    ◄──────────────────►  Aether-Droid (port 8888)
    ~/.aether/vault/                                   ~/aether-vault/
       fragments/              Encrypted sync            fragments/
```

### How It Works

1. A listener thread starts on boot (port 8888) when AetherLink is active.
2. On connection, nodes exchange fragment hashes to identify deltas.
3. Missing or updated fragments are transferred with encryption.
4. Both nodes remain usable during sync (non-blocking).

> **Status:** Alpha. Currently supports basic fragment push/pull. Full conflict resolution is planned for Phase 4.

---

## 🦾 OpenClaw Integration

As of v26.05.2, the Aether ecosystem is unified under the **OpenClaw Hybrid Bridge**.

### What OpenClaw Provides

| Capability | Benefit |
| :--- | :--- |
| **MCP Support** | Out-of-the-box access to any Model Context Protocol server |
| **Tool Loop** | Battle-tested ReAct-style multi-step tool execution |
| **Skill Portability** | Skills added to OpenClaw are immediately available in Aether |
| **Model Routing** | Advanced context window management and model switching |

### Migration from Legacy Tool Parser

Previous versions of Aether included a custom XML/JSON tool parser. This has been fully replaced by the OpenClaw bridge. If you have custom tools, port them as MCP servers or add them to `toolbox/manifest.json` for direct Python dispatch.

---

## 🗺️ Shared Vision & Phases

| Phase | Status | Description |
| :--- | :--- | :--- |
| **Phase 1** | ✅ Complete | Local model inference, basic tool loops |
| **Phase 2** | ✅ Complete | AetherVault memory, Desktop + Droid nodes |
| **Phase 3** | 🔄 Current | OpenClaw bridge, MCP expansion, AetherLink stabilization |
| **Phase 4** | 🔮 Planned | Full multimodal (Vision + Voice), autonomous self-improvement, AetherDroid parity |

The long-term goal is a **Self-Evolving Neural Partner** that:
- Improves its own skills and configuration over time
- Operates across all your devices with seamless memory continuity
- Remains entirely under your control with zero cloud dependency

---

## 🛡️ Nexus Shield

The shared security and system optimization layer.

| Module | Platforms | Description |
| :--- | :--- | :--- |
| **Privacy Shield** | Windows · Linux | Blocks telemetry endpoints, ad trackers, and OS data collection |
| **Gaming Mode** | Windows · Linux | Applies high-performance power plan, disables background throttling |
| **AI Bloat Killer** | Windows | Disables Copilot, Windows Recall, and related AI services |
| **Ghost Mode** | All | Dynamic background process deprioritization during inference |
| **System Deep Clean** | All | Removes cache, temp files, and log accumulations |

---

*"Zero bytes leave the device. Total sovereignty over your digital life."*
