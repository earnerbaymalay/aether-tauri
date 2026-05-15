#!/bin/bash

# Aether Ecosystem: Pre-Flight Hardware Audit
# Detects system specs and maps to "Pro" or "Lite" profiles.

echo "--- Aether Hardware Audit ---"

OS_TYPE=$(uname)
TOTAL_RAM_GB=0

if [[ "$OS_TYPE" == "Darwin" ]]; then
    TOTAL_RAM_BYTES=$(sysctl hw.memsize | awk '{print $2}')
    TOTAL_RAM_GB=$((TOTAL_RAM_BYTES / 1024 / 1024 / 1024))
    MODEL_NAME=$(sysctl -n hw.model)
    CPU_CORES=$(sysctl -n hw.ncpu)
    echo "OS: macOS ($MODEL_NAME)"
elif [[ "$OS_TYPE" == "Linux" ]]; then
    TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    TOTAL_RAM_GB=$((TOTAL_RAM_KB / 1024 / 1024))
    CPU_CORES=$(nproc)
    echo "OS: Linux"
else
    echo "OS: Unknown ($OS_TYPE)"
    exit 1
fi

echo "CPU Cores: $CPU_CORES"
echo "Total RAM: ${TOTAL_RAM_GB}GB"

# Profile Mapping
if [ "$TOTAL_RAM_GB" -ge 16 ]; then
    PROFILE="Pro"
    CAPABILITIES="Heavy LLMs, Multi-agent Swarms, High-speed RAG"
else
    PROFILE="Lite"
    CAPABILITIES="Quantized LLMs, Single-agent workflows, Cloud-assist"
fi

echo "----------------------------"
echo "Assigned Profile: $PROFILE"
echo "Capabilities: $CAPABILITIES"
echo "----------------------------"

# Save to ecosystem config
mkdir -p ~/.aether
echo "{\"profile\": \"$PROFILE\", \"ram\": $TOTAL_RAM_GB, \"cores\": $CPU_CORES, \"last_audit\": \"$(date)\"}" > ~/.aether/hw_profile.json

echo "Hardware profile saved to ~/.aether/hw_profile.json"
