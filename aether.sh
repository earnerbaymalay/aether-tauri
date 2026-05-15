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
echo "Launching Aether Terminal Interface (Caffeine Active)..."
cd "$(dirname "$0")"
# Set Python path to include agent directory for local imports
export PYTHONPATH="$PYTHONPATH:$(pwd)/agent"

# Ensure Caffeine is installed (as requested)
if ! command -v caffeinate &>/dev/null; then
    echo "caffeinate utility not found. Checking for Caffeine app..."
    if ! ls -d /Applications/Caffeine.app &>/dev/null; then
        echo "Installing Caffeine..."
        brew install --cask caffeine --no-quarantine
    fi
fi

# Launch with caffeinate to prevent system sleep
caffeinate -i python3 agent/aether_agent.py
