<div align="center">

# 🌌 A E T H E R — D E S K T O P
### *Local AI Workstation for macOS, Windows & Linux*

<p align="center">
  <a href="https://earnerbaymalay.github.io/sideload/">
    📲 <strong>Install on any device — phone, Mac, or iPad — from one place: Sideload Hub</strong>
  </a>
</p>

[![Version](https://img.shields.io/badge/version-foundation-81a1c1?style=for-the-badge)](https://github.com/earnerbaymalay/aether/blob/main/VERSIONS.md)
[![Tauri](https://img.shields.io/badge/framework-Tauri-FFC131?style=for-the-badge&logo=tauri)](https://tauri.app/)
[![Platform](https://img.shields.io/badge/platform-macOS_%7C_Windows_%7C_Linux-4c566a?style=for-the-badge)](https://github.com/earnerbaymalay/aether-desktop)
[![License](https://img.shields.io/badge/License-MIT-f1fa8c?style=for-the-badge)](LICENSE)
[![Privacy](https://img.shields.io/badge/Privacy-100%25_Local-bd93f9?style=for-the-badge)](#why-local)

[Quick Start](#quick-start) · [Architecture](#architecture) · [Android Version](https://github.com/earnerbaymalay/aether) · [Apple Version](https://github.com/earnerbaymalay/aether-apple)

</div>

---

## Overview

Aether Desktop brings the local AI philosophy to desktop — a Tauri-based application that connects to local AI models (Ollama, llama.cpp) through a terminal-style interface rendered with xterm.js.

**Same philosophy as the mobile version:** 100% local, private, offline AI. Adapted for desktop with a proper terminal UI.

### Features

| Feature | Status |
|---------|--------|
| Terminal UI (xterm.js) | ✅ |
| 4 AI tier routing (Agent, Turbo, Code, Logic) | ✅ |
| Ollama backend integration | ✅ |
| Cross-platform (Tauri) | ✅ |
| Settings & configuration | 🔄 In Progress |
| Toolbox integration | 🔄 In Progress |
| AetherVault knowledge loading | 🔄 Planned |

---

## Quick Start

### Prerequisites
- Node.js 18+
- Rust (for Tauri)
- Ollama running locally (or llama.cpp server)

### Build
```bash
# Clone
git clone https://github.com/earnerbaymalay/aether-desktop.git
cd aether-desktop

# Install dependencies
npm install

# Development
npm run tauri dev

# Production build
npm run tauri build
```

### Usage
1. Start Ollama: `ollama serve`
2. Pull a model: `ollama pull llama3.2`
3. Launch Aether Desktop
4. Configure your model endpoint in settings
5. Start chatting

---

## Architecture

```
aether-desktop/
├── src-tauri/              # Rust backend (Tauri)
│   ├── src/main.rs         # Tauri app entry
│   ├── Cargo.toml          # Rust dependencies
│   └── tauri.conf.json     # Tauri configuration
├── src/                    # TypeScript frontend
│   ├── main.ts             # App entry
│   ├── components/         # UI components
│   └── styles/             # CSS styles
├── index.html              # Main HTML
├── package.json            # Node dependencies
└── vite.config.ts          # Vite build config
```

### Tech Stack
- **Backend**: Rust (Tauri)
- **Frontend**: TypeScript + Vite
- **Terminal**: xterm.js
- **AI Backend**: Ollama (HTTP API)

---

## Ecosystem

Aether Desktop is part of the broader Aether ecosystem:

| Platform | Repo | Status |
|----------|------|--------|
| 📱 Android (Flagship) | [aether](https://github.com/earnerbaymalay/aether) | ✅ Active (26.04.2) |
| 🍎 macOS/iPad | [aether-apple](https://github.com/earnerbaymalay/aether-apple) | ✅ Complete (26.04) |
| 🖥️ Desktop (this) | [aether-desktop](https://github.com/earnerbaymalay/aether-desktop) | 🔄 Foundation |

All share the same philosophy: **local-first, private, free, open source.**

---

## Why Local?

| | Cloud AI | Aether |
|---|---|---|
| Cost | $20-200/month | Free |
| Internet | Required | Not needed |
| Privacy | Data on their servers | Zero bytes leave device |
| Latency | Network-dependent | Instant |
| Memory | Per-session | Persistent |

---

## Contributing

Fork, branch, and submit a PR. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

<div align="center">

**[MIT License](LICENSE)** — Free forever. Use it. Modify it. Share it.

*Develop natively. Think locally. Evolve autonomously.*

</div>
