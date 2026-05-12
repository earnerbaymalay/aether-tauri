<div align="center">

# 📜 Aether — Version History

</div>

---

## v26.05.2 *(Current)*

**Release Date:** May 2026

### New Features
- **OpenClaw Hybrid Bridge** — All agentic reasoning and tool execution offloaded to the OpenClaw CLI (`generate_completion_stream` via subprocess pipe).
- **MCP Client Manager** — `agent/mcp_client.py` provides full Model Context Protocol server lifecycle management.
- **Universal Skill Engine** — `agent/skill_loader.py` auto-discovers skills from `toolbox/manifest.json` and `CLAUDE.md` imports.
- **AetherLink Alpha** — Initial P2P sync implementation for AetherVault fragments (port 8888).
- **Shadow Monitor** — Background thread distills facts from every conversation into `shadow_*.md` fragments silently.

### Improvements
- Optimized model context windows for 16GB RAM systems (default threads: 6).
- Non-TTY stdin mode added to `chat_loop()` for seamless Tauri subprocess communication.
- `aether.sh` now auto-detects `systemctl` vs `ollama serve` for cross-platform Ollama startup.

### Fixes
- Standardized project naming: `aether-desktop` (Desktop) and `aether-droid` (Android).
- `PYTHONPATH` now correctly set to include `agent/` for all local module imports.

### Documentation
- Comprehensive rewrite of README, USAGE, ECOSYSTEM, ROADMAP, TROUBLESHOOTING, and CONTRIBUTING.
- New `ARCHITECTURE.md` with full system design, data flow diagrams, and design system reference.

---

## v26.05.1

**Release Date:** May 2026 (initial)

### New Features
- Initial Aether-Tauri public release.
- Tauri desktop app with xterm.js terminal integration.
- Neural Pathway selector (AGENT, TURBO, CODE, LOGIC cards).
- AetherVault memory fragments (manual save).
- Nexus Shield system optimizer panel.
- Local Ollama inference integration.
- Real-time system info panel (platform, OS, arch, RAM, dependency check).

---

*Version format: `YY.MM.patch` (Year.Month.Patch)*
