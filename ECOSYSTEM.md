# 🌌 Aether Ecosystem & Architecture

The Aether ecosystem is designed to be the uncompromising, local-first alternative to closed-loop AI providers. By combining a Rust desktop client, a Python backend, and advanced neural models, Aether achieves something Big Tech can't: **true data sovereignty without sacrificing intelligence.**

---

## 🏗️ Core Architecture (The Engine Room)

At the heart of Aether is `api_server.py`, a robust FastAPI backend that orchestrates the entire intelligence stack.

### 1. Neural Pathways (Model Routing)
Aether does not rely on a single monolithic model. It dynamically routes queries based on the task:
- **AGENT (e.g., Hermes-3-8B):** High-logic, tool-use capable model for system operations and complex problem solving.
- **TURBO (e.g., Llama-3.2-3B):** Ultra-fast model for transcription, summarization, and daily chatter.
- **CODE (e.g., Qwen-Coder-3B):** Specialized syntax generation and refactoring.
- **LOGIC (e.g., DeepSeek-R1):** Advanced Chain-of-Thought reasoning for architectural design.

### 2. AetherVault (Persistent Neural Memory)
Big AI charges you for memory. Aether uses local storage (`~/.aether/vault/`). 
The **Shadow Monitor** passively runs in the background, extracting key facts from your conversations and saving them as Markdown fragments. These fragments are automatically retrieved via RAG (Retrieval-Augmented Generation) during future conversations, giving Aether long-term, context-aware memory.

### 3. Model Context Protocol (MCP) Integration
Aether acts as an MCP Client. Rather than hardcoding tools, Aether dynamically attaches to standard MCP servers (Filesystem, Postgres, Web Search), allowing its `AGENT` pathway to interact with your local machine with absolute precision.

---

## 🖥️ Mission Control (Tauri Desktop)

The desktop client is built on Rust (Tauri) and React. It provides a "Mission Control" experience:
- **Zero Latency:** Commands sent from the UI are piped directly to the local Python engine.
- **Diagnostic Dashboard:** Real-time telemetry on CPU, RAM, and Neural Server health.
- **Self-Healing Watchdog:** The Tauri layer continuously polls the `api_server`. If a crash is detected, Aether will attempt to auto-recover its MCP links and restart the inference engine.

---

## 📱 Neural Link (Mobile Sync)

Your intelligence should travel with you. Aether includes **AetherLink**, a custom peer-to-peer (P2P) synchronization protocol.
- Generate a QR Code in Mission Control.
- Scan it with the Aether-Droid app.
- Active memory fragments and conversational state are beamed securely over your local network using Zeroconf discovery. **No cloud intermediation.**

---

## 🛡️ The Nexus Shield

The local AI revolution isn't just about running models; it's about reclaiming your hardware. 
Aether's **Nexus Shield** includes Python and PowerShell scripts to forcefully disable OS-level telemetry (like Windows Copilot and Recall), freeing up system resources to dedicate entirely to neural inference.

*We don't share your data. We actively prevent others from taking it.*

---

## 🔮 The Roadmap Forward

Aether is evolving rapidly. Our targets:
- **Phase A (Complete):** Guided hardware onboarding and model selection.
- **Phase B (Complete):** Self-healing diagnostics and Watchdog APIs.
- **Phase C (Complete):** Unified Mission Control layouts and P2P mobile sync.
- **Phase D (Upcoming):** True distributed inference (swarm computing) across multiple Aether nodes on a LAN.

Join us in building the open neural future.
