# 📖 Aether - Tauri Usage Guide

Welcome to the command center. This guide covers the essential operations of the Aether workstation.

---

## 🛠️ The Neural Toolbox

The Toolbox is the bridge between the AI and your operating system. It allows the agent to perform actions on your behalf.

### Available Tools
- **File System:** Create, read, and modify files within allowed directories.
- **Terminal Execution:** Run PowerShell (Windows) or Bash (Linux/macOS) commands.
- **System Analysis:** Query system hardware, network status, and running processes.

### Safety First
By default, Aether prompts for confirmation before executing high-impact system commands. You can configure "Trust Zones" in `config.json` to allow certain directories or scripts to run without manual approval.

---

## 🗄️ AetherVault: Persistent Memory

AetherVault is more than just a folder; it's a structured knowledge base that evolves with you.

### How it Works
1. **Fragments:** Transient thoughts and current session context.
2. **Memories:** Distilled knowledge extracted from fragments.
3. **Journal:** A time-series log of your interactions and system changes.

### Neural Distillation
Periodically, the background process runs a "Distillation" task. It analyzes recent Fragments and updates the core `SYSTEM_PROFILE.md` and relevant Memory files, ensuring the AI always has an up-to-date mental model of your preferences and projects.

---

## ⚙️ Configuration

Your `~/.aether/config.json` is the heart of the system.

### Key Settings
- `active_model`: The primary model for chat and general tasks.
- `turbo_model`: A smaller, faster model used for quick tasks like summarization or tool selection.
- `logic_model`: A large model (like DeepSeek) reserved for complex reasoning and debugging.
- `rag_enabled`: Toggle the local vector database for document search.

---

## 🚀 Advanced Usage

### Running as a Background Agent
You can start Aether in "Headless Mode" to act as a background assistant that monitors system events:
```bash
./aether.sh --headless
```

### Extending the Toolbox
You can add custom scripts to `~/aether/toolbox`. Any executable placed here will automatically be indexed and available for the AI to call.

---

[MIT License](LICENSE)
