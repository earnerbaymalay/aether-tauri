<div align="center">

# 🌌 A E T H E R — T A U R I
### *The Local-First Neural Operating Interface.*

[![Version](https://img.shields.io/badge/version-26.05.1-50fa7b?style=for-the-badge)](VERSIONS.md)
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
- **[Ollama](https://ollama.com/):** The engine for model inference. Must be running locally.
- **Node.js 20+:** Powers the neural interface's logic.
- **Rust:** The backbone for Tauri's high-speed native bridge.

### 2. Setup (Linux - Mint/Ubuntu/Debian)
Install system dependencies and the Rust toolchain:
```bash
sudo apt-get update
sudo apt-get install -y libwebkit2gtk-4.1-dev build-essential curl wget file libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env
npm install
```

### 3. Setup (Windows)
Run the automated PowerShell installer:
```powershell
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

### 4. Setup (macOS)
Run the automated shell installer:
```bash
chmod +x ./install.sh
./install.sh
```

### 5. Launch
Initialize the neural interface:
```bash
# Linux & macOS
./aether.sh

# Windows
ai
```

---

## 🌌 Core Features

- **🧠 Multi-Tier Brain:** Configurable model selection for different tasks (e.g., `HERMES` for agency, `DEEPSEEK` for deep logic).
- **🛠️ Integrated Toolbox:** Execute system-level commands (PowerShell/Bash) through the AI agent.
- **🗄️ AetherVault:** A persistent, markdown-based memory system that uses **Neural Distillation** to summarize and store long-term context.
- **🔒 Zero-Cloud:** No telemetry, no accounts, no subscriptions. Total data sovereignty.

---

## 🌌 Universal Computer Use

Aether has evolved into a self-evolving neural partner with the following advanced modules:
- **👻 Ghost Mode:** Dynamic background process monitoring and optimization.
- **👁️ Aether Eye (Vision):** Real-time screen awareness and UI debugging via moondream.
- **📂 AetherFS (Semantic FS):** System-wide semantic search across all your local files.
- **🌀 Ralph Loop:** Autonomous ReAct loop for multi-turn terminal task execution.
- **🔗 AetherLink (P2P Sync):** Secure, encrypted cross-device memory synchronization.
- **⌨️ System Automation:** Direct control over windows, applications, and input events.

## 🛡️ Nexus Shield

Aether now includes a visual system optimizer and privacy manager. Access it via the "Nexus Shield" button to manage:
- **Privacy Shield:** Block telemetry and OS-level ads.
- **Gaming Mode:** Optimize power plans and network priority.
- **AI Bloat Killer:** Disable integrated Copilot and Recall features.

## Documentation

- **[📖 Usage Guide](USAGE.md)** — Deep dive into the Toolbox, AetherVault, and Setup.
- **[🗺️ Roadmap](ROADMAP.md)** — What's coming next (Vision, Real-time Analysis).
- **[🔧 Troubleshooting](TROUBLESHOOTING.md)** — Fixing connection issues and build errors.

---

[MIT License](LICENSE)
