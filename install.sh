#!/bin/bash
# 🌌 Aether-Tauri macOS Installer
# Sets up dependencies for the Neural Operating Interface on macOS.

ACCENT="\033[1;32m"
RST="\033[0m"

echo -e "${ACCENT}🌌 Initializing Aether-Tauri macOS Setup...${RST}"

# Check for Homebrew
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Installing..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Node.js & Rust
echo "Installing Node.js and Rust..."
brew install node rustup-init
rustup-init -y
source $HOME/.cargo/env

# Install Ollama if missing
if ! command -v ollama &>/dev/null; then
    echo "Installing Ollama..."
    brew install --cask ollama
fi

# Install project dependencies
echo "Installing npm dependencies..."
npm install

echo -e "${ACCENT}✓ Setup Complete. Run './aether-apple.sh' to launch.${RST}"
