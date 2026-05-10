#!/bin/bash
# 🌌 Aether-Tauri macOS Launcher

# Ensure Ollama is running
if ! pgrep -x "Ollama" > /dev/null; then
    echo "Starting Ollama..."
    open -a Ollama
    sleep 5
fi

# Launch Tauri App in Dev Mode (Terminal Interface)
echo "Launching Aether Neural Interface..."
npm run tauri dev
