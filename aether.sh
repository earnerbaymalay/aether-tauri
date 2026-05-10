#!/bin/bash
# 🌌 Aether Terminal Launcher

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

# Launch Terminal-Based Aether Agent
echo "Launching Aether Terminal Interface..."
cd "$(dirname "$0")"
# Set Python path to include agent directory for local imports
export PYTHONPATH="$PYTHONPATH:$(pwd)/agent"
python3 agent/aether_agent.py
