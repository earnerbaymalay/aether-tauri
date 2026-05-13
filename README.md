https://github.com/earnerbaymalay/sideload
https://earnerbaymalay.github.io

![Aether Banner](docs/assets/aether_banner.png)

<div align="center">
  <h1>🌌 Aether — Tauri Workstation</h1>
  <p><em>The ultimate local‑first neural operating interface.</em></p>
</div>

---

## 🚀 Why Aether?

Aether gives you **full sovereignty** over your AI workflows. It runs **entirely on your hardware** – no cloud, no telemetry, no accounts. Compared to other AI tools, Aether:

- **Zero‑cloud**: All models run locally via Ollama.
- **Hybrid Bridge**: Leverages OpenClaw for tool‑augmented reasoning.
- **Unified UI**: Combines a premium Tauri desktop experience with a powerful Python agent core.
- **Extensible**: Plug‑in your own skills, scripts, or custom models with the MCP protocol.

---

## ✨ Quick Start

1. **Install prerequisites** (Ollama, OpenClaw, Node 20+, Rust, Python 3.10+). See the full guide in [GETTING_STARTED.md](docs/GETTING_STARTED.md).
2. **Pull recommended models**:
   ```bash
   ollama pull hermes3:8b   # General purpose agent
   ollama pull qwen2.5-coder:3b   # Code specialist
   ollama pull deepseek-r1:8b   # Deep logical reasoning
   ```
3. **Install dependencies** and launch:
   ```bash
   npm install           # Front‑end packages
   pip install -r requirements.txt   # Python agent deps
   ./aether.sh           # Starts the bridge and UI
   ```

---

## 📚 Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** – Step‑by‑step onboarding for all skill levels.
- **[USAGE.md](USAGE.md)** – Detailed usage guide, slash commands, and advanced workflows.
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** – Deep dive into the system design and data flows.
- **[COMPETITIVE_ANALYSIS.md](docs/COMPETITIVE_ANALYSIS.md)** – How Aether stacks up against other AI platforms.
- **[ADVANCED_FEATURES.md](docs/ADVANCED_FEATURES.md)** – Full capabilities, customization, and plugin system.
- **[STYLE_GUIDE.md](docs/STYLE_GUIDE.md)** – Branding, color palette, and UI component standards.

---

## 🤝 Contribute

We welcome contributions! Please read our updated [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT © 2024‑2026 Aether Team

