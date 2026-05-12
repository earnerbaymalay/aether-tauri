<div align="center">

# 🤝 Contributing to Aether-Tauri

*Build the sovereign neural workstation with us.*

</div>

---

## Getting Started

1. **Fork** the repository and create a feature branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Make your changes following the standards below.
3. **Build and test locally** before submitting:
   ```bash
   npm run tauri dev       # Development server with hot-reload
   ./aether.sh             # Test the Python agent directly
   python3 verify_core.py  # Run the core verification checks
   ```
4. Submit a **Pull Request** with a clear title and description covering *what* changed and *why*.

---

## Coding Standards

### Frontend — TypeScript

- Use **strict TypeScript** mode (configured in `tsconfig.json`). No `any` types without an explicit justification comment.
- All components should be **functional** with clearly typed props and return types.
- Use `@tauri-apps/api` imports for all native bridge calls — do not use `window.__TAURI__` directly.
- **Do not replace xterm.js** for terminal rendering. It is required for ANSI escape code support from the Rich-powered Python agent.
- Avoid inline styles. All styling belongs in `src/styles/app.css` using the established CSS custom property tokens.

### Backend — Rust / Tauri

- Follow all `clippy` recommendations (`cargo clippy -- -D warnings`).
- No `unsafe` blocks without a documented justification comment explaining the invariant being upheld.
- Keep Tauri commands **minimal and focused**. Delegate heavy logic to the Python agent or platform scripts — don't duplicate it in Rust.
- Emit typed events (`agent-stdout`, `agent-stderr`) for any streaming output; don't try to return streaming data from a command.

### Agent Core — Python

- Target **Python 3.10+** compatible syntax.
- All new agent modules must be importable from `agent/` with a relative import (set `PYTHONPATH` via `aether.sh`).
- Use `rich` for all console output inside the agent — do not use bare `print()` for UI rendering.
- New slash commands must be registered in both `handle_help()` (the table) and `chat_loop()` (the dispatch block).
- Background tasks (like Shadow Monitor) must be run as **daemon threads** (`daemon=True`) so they don't block agent shutdown.

### General

- **No hardcoded credentials or API keys** anywhere in the codebase.
- **Document new features** in the relevant `.md` file before or alongside your PR.
- **Test on at least one target platform** (macOS, Windows, or Linux) before submitting.
- Log meaningful events at the appropriate level via `LOGGER` (`INFO` for normal ops, `ERROR` for failures).

---

## Design System Rules

When contributing UI changes, adhere to the established design system in `src/styles/app.css`:

- **Only use CSS custom properties** from `:root` for colors — never hardcode hex values in component styles.
- New interactive components must include `transition` properties for hover/active states.
- Modal overlays use `position: fixed; z-index: 100` and the `--surface` background with a `--teal` border.
- Buttons always use the `.btn` base class, with modifier classes (`.btn-small`, `.btn-nexus`) for variants.

See [ARCHITECTURE.md — Frontend Design System](ARCHITECTURE.md#-frontend-design-system) for the full token reference.

---

## Project Structure Quick Reference

```
aether-tauri/
├── agent/          ← Python agent core (all .py files)
├── src/
│   ├── main.ts     ← Tauri frontend logic
│   └── styles/     ← CSS design system
├── src-tauri/      ← Rust/Tauri backend
├── toolbox/        ← Skill scripts + manifest.json
├── tools/          ← Standalone utilities (monitor.py)
└── docs/           ← Media assets (hero.svg, screenshots)
```

---

## What's Needed

The following features are tracked as open work items. Contributions welcome:

- [ ] **Settings UI panel** — A native settings overlay to replace the terminal-based `/settings` flow
- [ ] **AetherVault browser** — A panel to view, search, and delete memory fragments from the Tauri UI
- [ ] **Model management UI** — Pull, delete, and switch models from the System Panel
- [ ] **Session persistence** — Save and restore named conversation histories
- [ ] **Multi-model support** — Add LM Studio and llama.cpp as first-class inference backends alongside Ollama
- [ ] **AetherLink status widget** — Show P2P sync state in the System Info panel
- [ ] **Windows toolbox parity** — Ensure all `toolbox/` scripts have working `.ps1` equivalents

---

## Submitting Issues

When filing a bug report, please include:

1. Your OS and version
2. Output of `ollama info` (GPU/CPU inference mode)
3. The relevant section of `~/.aether/logs/aether.log`
4. Steps to reproduce

---

[MIT License](LICENSE)
