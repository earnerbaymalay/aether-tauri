<div align="center">

# 🌌 A E T H E R — T A U R I
### *The Local-First Neural Operating Interface.*

[![Version](https://img.shields.io/badge/version-26.05.2-50fa7b?style=for-the-badge)](VERSIONS.md)
[![Tauri](https://img.shields.io/badge/framework-Tauri-FFC131?style=for-the-badge&logo=tauri)](https://tauri.app/)
[![License](https://img.shields.io/badge/license-MIT-f1fa8c?style=for-the-badge)](LICENSE)

**[📲 Download](https://github.com/earnerbaymalay/aether-tauri/releases)** · **[🌐 Sideload Hub](https://earnerbaymalay.github.io/sideload/)** · **[📖 Usage Guide](USAGE.md)** · **[🔧 Troubleshooting](TROUBLESHOOTING.md)**

</div>

---

![Aether - Tauri](docs/media/hero.svg)

## What is Aether?

**Aether is your sovereign neural workstation.** It's designed to be a high-autonomy bridge between you and your local LLMs. By running entirely on your own hardware, Aether ensures that your thoughts, data, and workflows remain private and offline.

This repository contains the **Aether-Tauri workstation**, offering a unified, high-performance experience for **Linux**, **Windows**, and **macOS**.

---

## 🚀 Quick Start

### 1. Prerequisites (All Platforms)
- **[Ollama](https://ollama.com/):** Engine for model inference.
- **[OpenClaw](https://github.com/google/gemini-cli):** The neural backbone for tool and MCP management.
- **Node.js 20+** & **Rust**: Development toolchain.

### 2. Setup
Install system dependencies and pull optimized models:
```bash
# Pull recommended agentic models
ollama pull hermes3:8b
ollama pull qwen2.5-coder:3b

# Install dependencies
npm install
```

### 3. Launch
Initialize the OpenClaw gateway and the neural interface:
```bash
# Start OpenClaw Gateway (required for bridge mode)
openclaw gateway --port 18789 --force &

# Launch Aether
./aether.sh
```

---

## 🌌 Core Features

- **🦾 OpenClaw Hybrid Bridge:** Offloads complex reasoning and tool execution to the OpenClaw ecosystem while maintaining Aether's native UI.
- **🧠 Multi-Tier Brain:** Optimized model selection (e.g., `HERMES-8B` for agency, `QWEN-3B` for high-speed coding).
- **🛠️ MCP Integration:** Access to the full Model Context Protocol ecosystem, including DuckDuckGo search and system-wide skills.
- **🗄️ AetherVault:** A persistent, markdown-based memory system that uses **Neural Distillation** to summarize and store long-term context.
- **🔒 Zero-Cloud:** No telemetry, no accounts, no subscriptions. Total data sovereignty.

---

## 🌌 Universal Computer Use

Aether has evolved into a self-evolving neural partner with the following advanced modules:
- **👻 Ghost Mode:** Dynamic background process monitoring and optimization.
- **👁️ Aether Eye (Vision):** Real-time screen awareness via `moondream`.
- **📂 AetherFS:** System-wide semantic search across all local files.
- **🔗 AetherLink (P2P Sync):** Secure, encrypted cross-device memory synchronization.

---

## AI Tiers (Neural Pathways)

| Tier | Model | Best For |
| :--- | :--- | :--- |
| 🤖 **AGENT** | `hermes3:8b` | Tool use, complex tasks, memory, and full autonomy. |
| 💻 **CODE** | `qwen2.5-coder:3b` | Code generation, review, and logic. Optimized for performance. |
| 🧠 **LOGIC** | `deepseek-r1:8b` | Deep reasoning, architectural planning, and "thinking" mode. |

---

## Documentation

- **[📖 Usage Guide](USAGE.md)** — Deep dive into the Bridge Mode, AetherVault, and Setup.
- **[🗺️ Roadmap](ROADMAP.md)** — Future development goals and completed integrations.
- **[🔧 Troubleshooting](TROUBLESHOOTING.md)** — Fixing bridge connections and model errors.


---

[MIT License](LICENSE)
