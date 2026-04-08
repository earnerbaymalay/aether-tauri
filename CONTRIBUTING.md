# Contributing to Aether Desktop

Thanks for your interest! Aether Desktop is the Tauri-based desktop companion to the Aether AI ecosystem.

## Quick Guide

1. Fork and branch from `main`
2. Make your changes (TypeScript, Rust, or documentation)
3. Build and test locally: `npm run tauri dev`
4. Submit a PR with a clear description

## Coding Standards

### Frontend (TypeScript)
- Use strict TypeScript mode
- No `any` types without justification
- Components should be functional with clear props interfaces
- Use xterm.js for terminal rendering (don't replace)

### Backend (Rust/Tauri)
- Follow Rust clippy recommendations
- No unsafe blocks without documented justification
- Keep Tauri commands minimal — delegate to Ollama/llama.cpp

### General
- No hardcoded credentials or API keys
- Document new features in the README
- Test on at least one target platform (macOS, Windows, or Linux)

## Building

```bash
npm install
npm run tauri dev    # Development
npm run tauri build   # Production
```

## What's Needed

- [ ] Settings/configuration UI
- [ ] Toolbox integration
- [ ] AetherVault knowledge loading
- [ ] Model management UI
- [ ] Session management
- [ ] Multi-model support (beyond Ollama)
