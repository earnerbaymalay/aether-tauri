# 🔧 Aether - Tauri Troubleshooting

Having issues? Here are the most common solutions.

---

## 🏗️ Build & Installation

### Linux: Missing WebKit2GTK
**Error:** `Could not find libwebkit2gtk-4.1`
**Fix:** Install the development headers:
```bash
sudo apt-get install libwebkit2gtk-4.1-dev
```

### Windows: PowerShell Execution Policy
**Error:** `Script cannot be loaded because running scripts is disabled`
**Fix:** Run the installer with a bypass flag:
```powershell
powershell -ExecutionPolicy Bypass -File .\install-windows.ps1
```

### macOS: App is "Damaged"
**Fix:** This is often a Gatekeeper issue. Run:
```bash
xattr -d com.apple.quarantine /Applications/Aether.app
```

---

## 🦾 OpenClaw Bridge Issues

### Connection Refused (Port 18789)
**Error:** `OpenClaw Bridge Error: [Errno 111] Connection refused`
**Fix:** Ensure the OpenClaw gateway is running. Start it with:
```bash
openclaw gateway --port 18789 --force
```

### Model Not Found (OpenClaw)
**Error:** `LLM request failed: model_not_found`
**Fix:** Check your `~/.openclaw/openclaw.json` and ensure the model name matches exactly what `ollama list` reports.
```bash
# Verify model names
ollama list
# Update OpenClaw config if necessary
openclaw config set agents.defaults.model.primary "ollama/hermes3:8b"
```

### No Tool Response
If the AI seems to ignore tools, verify that `supportsTools` is set to `true` in your OpenClaw model configuration.

---

## 🧠 AI & Model Issues

### Ollama Not Found
**Check:** Ensure Ollama is running in the background.
```bash
# Check status (Linux/macOS)
pgrep -x ollama

# Restart service (Linux)
sudo systemctl restart ollama
```

### Model Missing
**Error:** `Model 'llama3.2:3b' not found`
**Fix:** Manually pull the required models:
```bash
ollama pull hermes3:8b
ollama pull llama3.2:3b
```

### Inference is Slow
- **Hardware:** Ensure you have enough RAM/VRAM. AI inference is resource-intensive.
- **Background Tasks:** Close other GPU-heavy apps (browsers, games).
- **Model Size:** If 8B models are too slow, try 1B or 3B versions (e.g., `llama3.2:1b`).

---

## 🛠️ Toolbox & Permissions

### Permission Denied (Linux/macOS)
**Error:** `sh: ./aether.sh: Permission denied`
**Fix:** Grant execution rights:
```bash
chmod +x ./aether.sh
```

### Script Execution Fails
If a tool fails to run, check the logs in `~/.aether/logs/aether.log`. Often, this is due to a missing system dependency or the script not being in the system PATH.

---

[MIT License](LICENSE)
