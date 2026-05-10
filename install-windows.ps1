# Aether - Tauri - Windows Installation Script

function Write-Step($msg) {
    Write-Host "`n[*] $msg" -ForegroundColor Cyan
}

Write-Host "==========================================" -ForegroundColor Green
Write-Host "         A E T H E R - T A U R I          " -ForegroundColor Green
Write-Host "          WINDOWS INSTALLER V26.05.1      " -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# 1. Check Python
Write-Step "Checking Python environment..."
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCmd) {
    Write-Host "[OK] Python found." -ForegroundColor Green
} else {
    Write-Host "[FAIL] Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}

# 2. Check Ollama
Write-Step "Checking Ollama (Neural Engine)..."
$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaCmd) {
    Write-Host "[OK] Ollama found." -ForegroundColor Green
    Write-Host "  Pulling recommended models..."
    ollama pull llama3.2:3b
    ollama pull hermes3:8b
    ollama pull deepseek-r1:8b
    ollama pull qwen2.5-coder:7b
} else {
    Write-Host "[WARN] Ollama not found. Aether requires Ollama for inference." -ForegroundColor Yellow
    Write-Host "  Download from: https://ollama.com/" -ForegroundColor White
}

# 3. Install Python Dependencies
Write-Step "Installing Agent dependencies..."
pip install requests colorama --quiet
Write-Host "[OK] Dependencies satisfied." -ForegroundColor Green

# 4. Configure Local Paths
Write-Step "Configuring workspace..."
$aetherPath = "$HOME\aether"
if (-not (Test-Path $aetherPath)) {
    New-Item -ItemType Directory -Path $aetherPath -Force | Out-Null
    New-Item -ItemType Directory -Path "$aetherPath\knowledge\aethervault" -Force | Out-Null
    Write-Host "[OK] Created local Aether directory at $aetherPath" -ForegroundColor Green
}

# 5. Create 'ai' Alias
Write-Step "Creating global 'ai' command..."
$binDir = "$HOME\.local\bin"
if (-not (Test-Path $binDir)) { New-Item -ItemType Directory -Path $binDir -Force | Out-Null }

$batContent = "@echo off`npushd ""$PSScriptRoot\agent""`npython aether_agent.py %*`npopd"
$batContent | Out-File -FilePath "$binDir\ai.bat" -Encoding ASCII

# Check if binDir is in PATH
if ($env:PATH -notlike "*$binDir*") {
    Write-Host "[WARN] $binDir is not in your PATH." -ForegroundColor Yellow
    Write-Host "  Add it manually to use the 'ai' command from anywhere." -ForegroundColor Gray
} else {
    Write-Host "[OK] 'ai' command is now active." -ForegroundColor Green
}

Write-Host "`n[DONE] Setup Complete! Type 'ai' to begin your session." -ForegroundColor Green
