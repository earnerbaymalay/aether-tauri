# Aether Desktop

Aether for macOS, Windows, and Linux. Built with Tauri -- a Rust backend with a TypeScript frontend rendered through xterm.js.

[![Version](https://img.shields.io/badge/version-foundation-81a1c1?style=for-the-badge)](https://github.com/earnerbaymalay/aether/blob/main/VERSIONS.md)
[![Tauri](https://img.shields.io/badge/framework-Tauri-FFC131?style=for-the-badge&logo=tauri)](https://tauri.app/)
[![License](https://img.shields.io/badge/license-MIT-f1fa8c?style=for-the-badge)](LICENSE)

[Quick Start](#quick-start) · [Architecture](#architecture) · [Android Version](https://github.com/earnerbaymalay/aether)

---

## What It Does

Aether Desktop connects to local AI models running Ollama or llama.cpp through a terminal-style interface. Same local-first approach as the mobile versions.

## Quick Start

Requires Node.js 18+, Rust, and Ollama running locally.

```bash
git clone https://github.com/earnerbaymalay/aether-desktop.git
cd aether-desktop
npm install
npm run tauri dev
```

Start Ollama (`ollama serve`), pull a model (`ollama pull llama3.2`), configure your endpoint in settings.

For a production build:
```bash
npm run tauri build
```

## Architecture

```
aether-desktop/
├── src-tauri/              # Rust backend
│   ├── src/main.rs
│   ├── Cargo.toml
│   └── tauri.conf.json
├── src/                    # TypeScript frontend
│   ├── main.ts
│   ├── components/
│   └── styles/
├── index.html
├── package.json
└── vite.config.ts
```

## Ecosystem

| Platform | Repo | Status |
|----------|------|--------|
| Android | [aether](https://github.com/earnerbaymalay/aether) | 26.04.2 |
| macOS/iPad | [aether-apple](https://github.com/earnerbaymalay/aether-apple) | 26.04 |
| Desktop | this repo | Foundation |

---

[MIT License](LICENSE)
