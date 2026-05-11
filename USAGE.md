# 📖 Aether - Tauri Usage Guide

Welcome to the command center. This guide covers the essential operations of the Aether workstation, now powered by the **OpenClaw Hybrid Bridge**.

---

## 🦾 OpenClaw Hybrid Bridge

Aether now uses a "Hybrid Bridge" architecture. While the UI and local management stay in Aether, the actual intelligence and tool execution are offloaded to **OpenClaw**.

### Benefits
- **Full MCP Support:** Use any Model Context Protocol server (like DuckDuckGo) directly.
- **Advanced Agency:** Better multi-step task execution via OpenClaw's optimized loops.
- **Unified Skills:** Aether gains all skills installed in your OpenClaw ecosystem.

### Setup
Ensure the OpenClaw gateway is running before launching Aether:
```bash
openclaw gateway --port 18789 --force &
```

---

## 🧠 Neural Pathways (AI Tiers)

Aether routes your queries through specialized "Neural Pathways" based on the task type.

- **🤖 AGENT (Primary):** Powered by `hermes3:8b`. This is your go-to for system operations, internet searches, and complex problem-solving.
- **💻 CODE:** Powered by `qwen2.5-coder:3b`. A hyper-optimized model for generating, reviewing, and debugging code.
- **🧠 LOGIC:** Powered by `deepseek-r1:8b`. Best for architectural planning, philosophical inquiry, or intense reasoning.

---

## 🗄️ AetherVault: Neural Knowledge Base

AetherVault is now decoupled from the core application state, allowing you to use **Obsidian** or any separate local directory as your neural knowledge base.

### Features
- **Obsidian Native:** If `~/Documents/Vault` exists, Aether automatically integrates with your Obsidian vault.
- **Configurable Path:** Use `/settings` to point the neural vault to any local folder.
- **Independent Storage:** The vault is kept separate from `aether-droid` (which handles models) to ensure your knowledge remains portable and clean.
- **Shadow Monitor:** Background extraction of facts and preferences continues to enrich your chosen vault location.

---

## 🚀 Commands & Shortcuts

- `/settings` - Configure models, threads, and UI theme.
- `/memory` - Inspect recent AetherVault fragments.
- `/health` - Run a system vitals check (CPU, RAM, Dependencies).
- `/auto-fix` - Paste an error message to receive a self-healing command suggestion.
- `/clear` - Resets the terminal interface view.

---

## 📊 Aether Neural Monitor

The Aether Neural Monitor is a real-time TUI dashboard that tracks the health of all neural services and system resources.

### Launching the Monitor
Run the following command in a separate terminal window:
```bash
aether-monitor
```
Or run it directly from the repository:
```bash
python3 tools/monitor.py
```

It monitors:
- **Services:** Ollama, OpenClaw, and LM Studio.
- **Processes:** Aether Agent, Aether Tauri, and OpenClaude.
- **Hardware:** Live CPU and RAM usage.
