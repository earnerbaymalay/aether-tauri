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

## 🗄️ AetherVault: Persistent Memory

AetherVault is more than just a folder; it's a structured knowledge base that evolves with you.

### How it Works
1. **Fragments:** Transient thoughts and current session context.
2. **Memories:** Distilled knowledge extracted from fragments.
3. **Shadow Monitor:** A background process that silently extracts facts and preferences from your conversations into "Shadow Fragments."

### Neural Distillation
Periodically, the background process runs a "Distillation" task. It analyzes recent Fragments and updates the core `SYSTEM_PROFILE.md` and relevant Memory files, ensuring the AI always has an up-to-date mental model of your preferences and projects.

---

## 🚀 Commands & Shortcuts

- `/settings` - Configure models, threads, and UI theme.
- `/memory` - Inspect recent AetherVault fragments.
- `/health` - Run a system vitals check (CPU, RAM, Dependencies).
- `/auto-fix` - Paste an error message to receive a self-healing command suggestion.
- `/clear` - Resets the terminal interface view.

---

[MIT License](LICENSE)
