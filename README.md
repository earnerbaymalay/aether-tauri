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

**Aether is a sovereign neural workstation.** It provides a high-autonomy interface to local AI models (Ollama, llama.cpp), giving you a private, offline command center that runs entirely on your own hardware. 

This repository houses the **Tauri-based desktop workstation**, unified for both **Windows** and **macOS**.

---

## 🚀 Quick Start

### 1. Prerequisites (All Platforms)
- **[Ollama](https://ollama.com/):** Must be running locally for model inference.
- **Node.js 20+:** Required for the UI and dev tools.
- **Python 3.12+:** Required for the autonomous Agent Core.

### 2. Setup (Windows)
Run the automated PowerShell installer:
```powershell
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

### 3. Setup (macOS)
Run the automated shell installer:
```bash
chmod +x ./install.sh
./install.sh
```

### 4. Launch
Launch the neural interface from your terminal:
```bash
# Windows
ai

# macOS
./aether.sh
```

---

### Aether Ecosystem

<div align="center">

| Platform | Repository | Version |
|----------|------------|---------|
| 📱 **Android (Termux)** | [aether-android](https://github.com/earnerbaymalay/aether-android) | 26.05.1 |
| 🖥️ **Desktop (Tauri)** | [aether-tauri](https://github.com/earnerbaymalay/aether-tauri) | 26.05.1 |

</div>

---

## 🌌 Core Architecture

- **🧠 The Brain:** Specialized model tiers (`HERMES` for agency, `DEEPSEEK` for logic).
- **🛠️ The Toolbox:** Platform-native tools (PowerShell for Windows, Bash for macOS/Linux).
- **🗄️ AetherVault:** Markdown-based persistent memory with **Neural Distillation**.

---

## Documentation

- **[📖 Usage Guide](USAGE.md)** — Toolbox, AetherVault, and Setup.
- **[🗺️ Roadmap](ROADMAP.md)** — Future development goals and feature tracking.
- **[🔧 Troubleshooting](TROUBLESHOOTING.md)** — Ollama connections and script permissions.

---

[MIT License](LICENSE)
