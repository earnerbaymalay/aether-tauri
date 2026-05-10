#!/bin/bash
# 🌌 Aether-Tauri Launcher

# Ensure Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "Starting Ollama..."
    if command -v systemctl &>/dev/null; then
        sudo systemctl start ollama
    else
        ollama serve &
    fi
    sleep 5
fi

# Launch Tauri App in Dev Mode
echo "Launching Aether Neural Interface..."
npm run tauri dev
