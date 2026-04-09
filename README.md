# Aether Desktop

Aether for macOS, Windows, and Linux. Built with Tauri, it features a Rust backend and a TypeScript frontend rendered through xterm.js.

[![Version](https://img.shields.io/badge/version-26.04.2-50fa7b?style=for-the-badge)](https://github.com/earnerbaymalay/aether/blob/main/VERSIONS.md)
[![Tauri](https://img.shields.io/badge/framework-Tauri-FFC131?style=for-the-badge&logo=tauri)](https://tauri.app/)
[![License](https://img.shields.io/badge/license-MIT-f1fa8c?style=for-the-badge)](LICENSE)

[Quick start](#quick-start) · [Architecture](#architecture) · [Android version](https://github.com/earnerbaymalay/aether)

---

## Functions

Aether Desktop connects to local AI models, such as those running Ollama or llama.cpp, through a terminal-style interface. It maintains the same local-first approach found in the mobile versions.

---

## Quick start

Requires Node.js 18+, Rust, and Ollama running locally.

```bash
git clone https://github.com/earnerbaymalay/aether-desktop.git
cd aether-desktop
npm install
npm run tauri dev
```

To use, start Ollama (`ollama serve`), pull a model (`ollama pull llama3.2`), then configure your endpoint in the Aether Desktop settings.

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

| Platform | Repository | Status |
|----------|------------|--------|
| Android | [aether](https://github.com/earnerbaymalay/aether) | 26.04.2 |
| macOS/iPad | [aether-apple](https://github.com/earnerbaymalay/aether-apple) | 26.04.2 |
| Desktop | This repository | 26.04.2 |

---

[MIT License](LICENSE)
