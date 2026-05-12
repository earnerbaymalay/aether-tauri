<div align="center">

# 🌌 A E T H E R — T A U R I
### *The Local-First Neural Operating Interface.*

[![Version](https://img.shields.io/badge/version-26.05.2-50fa7b?style=for-the-badge)](VERSIONS.md)
[![Tauri](https://img.shields.io/badge/framework-Tauri-FFC131?style=for-the-badge&logo=tauri)](https://tauri.app/)
[![Python](https://img.shields.io/badge/agent-Python%203.10+-3776AB?style=for-the-badge&logo=python)](agent/)
[![License](https://img.shields.io/badge/license-MIT-f1fa8c?style=for-the-badge)](LICENSE)

**[📲 Install](#-quick-start)** · **[📖 Usage Guide](USAGE.md)** · **[🏛️ Architecture](ARCHITECTURE.md)** · **[🌌 Ecosystem](ECOSYSTEM.md)** · **[🔧 Troubleshooting](TROUBLESHOOTING.md)**

</div>

---

![Aether - Tauri](docs/media/hero.svg)

## What is Aether?

**Aether is your sovereign neural workstation.** It bridges you and your local LLMs through a high-autonomy, tool-augmented interface — running entirely on your own hardware with zero telemetry, zero accounts, and zero cloud dependency.

This repository is the **Aether-Tauri workstation**: a cross-platform desktop application built on Rust (Tauri) and TypeScript, with a Python agentic core. It delivers a unified, high-performance experience on **Linux**, **Windows**, and **macOS**.

> *"Zero bytes leave the device. Total sovereignty over your digital life."*

---

## 🚀 Quick Start

### Prerequisites

| Dependency | Purpose | Install |
| :--- | :--- | :--- |
| **[Ollama](https://ollama.com/)** | Local model inference engine | `curl -fsSL https://ollama.com/install.sh \| sh` |
| **[OpenClaw](https://github.com/google/gemini-cli)** | Agentic bridge & MCP orchestration | See OpenClaw docs |
| **Node.js 20+** | Frontend build toolchain | [nodejs.org](https://nodejs.org) |
| **Rust** | Tauri native backend | `curl --proto '=https' --tlsf1.2 -sSf https://sh.rustup.rs \| sh` |
| **Python 3.10+** | Agent core runtime | [python.org](https://python.org) |

### Installation

```bash
# 1. Pull the recommended agentic model stack
ollama pull hermes3:8b          # Primary agent (tool use + reasoning)
ollama pull qwen2.5-coder:3b    # Code specialist
ollama pull deepseek-r1:8b      # Deep logic & planning

# 2. Install frontend and agent dependencies
npm install
pip3 install -r requirements.txt

# 3. Make launcher executable (Linux/macOS)
chmod +x ./aether.sh
```

### Launch

```bash
# Start the OpenClaw gateway (required for bridge mode)
openclaw gateway --port 18789 --force &

# Launch Aether (starts Ollama if not running, then launches the agent)
./aether.sh
```

---

## 🌌 Core Features

| Feature | Description |
| :--- | :--- |
| **🦾 OpenClaw Hybrid Bridge** | Offloads complex reasoning and tool execution to the OpenClaw CLI ecosystem while keeping Aether's native UI. |
| **🧠 Multi-Tier Neural Pathways** | Routes queries to the optimal model: `AGENT`, `TURBO`, `CODE`, or `LOGIC`. |
| **🗄️ AetherVault** | Persistent, markdown-based memory system using background **Shadow Monitor** distillation. Obsidian-compatible. |
| **📂 AetherFS** | System-wide semantic file search and indexing via the RAG engine. |
| **🛡️ Nexus Shield** | One-click privacy hardening: telemetry blocking, AI bloat removal, and system deep-clean. |
| **👁️ Aether Eye** | Real-time screen awareness using local vision models (moondream). |
| **🔗 AetherLink** | Encrypted P2P memory synchronization across Aether nodes (port 8888). |
| **🛠️ MCP Integration** | Full Model Context Protocol ecosystem — add tools once, use everywhere. |
| **📊 Neural Monitor** | Real-time TUI dashboard for Ollama, OpenClaw, LM Studio, and hardware metrics. |
| **🔒 Zero-Cloud** | No telemetry, no accounts, no subscriptions. |

---

## 🧠 Neural Pathways (AI Tiers)

Aether routes your queries to the optimal model based on the task type selected at startup:

| Tier | Model | Best For | Speed |
| :--- | :--- | :--- | :--- |
| 🤖 **AGENT** | `hermes3:8b` | Tool use, system ops, complex reasoning, full autonomy | 10–15 t/s |
| ⚡ **TURBO** | `llama3.2:3b` | Daily questions, summaries, translations, fast responses | 25+ t/s |
| 💻 **CODE** | `qwen2.5-coder:3b` | Code generation, review, debugging, and refactoring | 18+ t/s |
| 🧠 **LOGIC** | `deepseek-r1:8b` | Architectural planning, philosophical inquiry, deep analysis | 22+ t/s |

---

## 📁 Project Structure

```
aether-tauri/
├── agent/                  # Python agentic core
│   ├── aether_agent.py     # Main agent loop, UI, and command handlers
│   ├── mcp_client.py       # MCP server manager
│   ├── p2p_sync.py         # AetherLink P2P synchronization
│   ├── rag_engine.py       # AetherFS semantic search (RAG)
│   ├── skill_loader.py     # Universal skill discovery engine
│   └── system_scanner.py   # Hardware & dependency detection
├── src/
│   ├── main.ts             # Tauri frontend TypeScript
│   └── styles/app.css      # Design system & component styles
├── src-tauri/              # Rust/Tauri backend (native commands)
├── toolbox/                # Cross-platform skill scripts & manifest
│   └── manifest.json       # Tool registry
├── tools/
│   └── monitor.py          # Neural Monitor TUI dashboard
├── index.html              # Main application shell
├── aether.sh               # Cross-platform launch script
└── requirements.txt        # Python dependencies
```

---

## 📚 Documentation

| Document | Description |
| :--- | :--- |
| **[USAGE.md](USAGE.md)** | Complete guide to Bridge Mode, AetherVault, slash commands, and the Neural Monitor |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | Deep-dive into the system design, data flows, and module responsibilities |
| **[ECOSYSTEM.md](ECOSYSTEM.md)** | Holistic overview of Aether-Desktop, Aether-Droid, AetherVault, and AetherLink |
| **[ROADMAP.md](ROADMAP.md)** | Completed milestones and upcoming development goals |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Solutions for common build, bridge, model, and permission errors |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | Standards, patterns, and contribution workflow |
| **[VERSIONS.md](VERSIONS.md)** | Changelog and version history |

---

[MIT License](LICENSE)
