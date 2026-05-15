#!/bin/bash
# 🌌 Aether Workstation Launcher

echo "🚀 Starting Aether Workstation..."

# 1. Ensure dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "[*] Installing Node.js dependencies..."
    npm install
fi

if [ ! -d "venv" ]; then
    echo "[*] Creating Python virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

# 2. Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "[*] Starting Ollama..."
    ollama serve &
    sleep 5
fi

# 2.5 Ensure OpenClaw bridge is running
if ! pgrep -x "openclaw" > /dev/null; then
    echo "[*] Starting OpenClaw bridge..."
    if command -v openclaw &>/dev/null; then
        openclaw gateway --port 18789 --force &
        sleep 2
    else
        echo "[!] openclaw not found in PATH. Skipping bridge..."
    fi
fi

# 3. Launch Tauri App
echo "[*] Launching UI..."
npm run tauri:dev
