import os
import platform
import subprocess
import json
import argparse
from pathlib import Path

def get_config_path():
    return Path.home() / ".aether" / "config.json"

def apply_tweak(description, cmd, is_powershell=False):
    print(f"  → {description}...")
    try:
        if is_powershell:
            subprocess.run(["powershell.exe", "-Command", cmd], capture_output=True, check=True)
        else:
            subprocess.run(cmd, shell=True, capture_output=True, check=True)
        return True
    except Exception as e:
        print(f"    [!] Failed: {e}")
        return False

def optimize_windows():
    print("🌌 Initializing Windows Nexus Fusion (Administrator Rights Required)...")
    
    # 1. Network Throttling & Responsiveness
    apply_tweak("Optimizing Network Throttling Index", 
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' -Name 'NetworkThrottlingIndex' -Value 0xffffffff", 
                True)
    apply_tweak("Setting System Responsiveness to Gaming Mode", 
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile' -Name 'SystemResponsiveness' -Value 0", 
                True)
    
    # 2. Privacy & Telemetry
    apply_tweak("Disabling Data Collection Telemetry", 
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection' -Name 'AllowTelemetry' -Value 0", 
                True)
    apply_tweak("Disabling Advertising ID", 
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo' -Name 'Enabled' -Value 0", 
                True)
    
    # 3. AI Bloat (Copilot/Recall)
    apply_tweak("Disabling Windows Copilot", 
                "Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsCopilot' -Name 'TurnOffWindowsCopilot' -Value 1", 
                True)
    
    # 4. Clean & Flush
    apply_tweak("Flushing DNS Cache", "ipconfig /flushdns")
    apply_tweak("Cleaning Temp Files", "Remove-Item -Path $env:TEMP\\* -Recurse -Force -ErrorAction SilentlyContinue", True)
    
    print("✓ Windows Nexus optimizations applied.")

def optimize_linux():
    print("🌌 Initializing Linux Nexus Fusion (Sudo Required)...")
    
    # 1. Kernel / VM Optimizations
    apply_tweak("Reducing Swappiness (Better RAM utilization)", "sudo sysctl -w vm.swappiness=10")
    apply_tweak("Increasing File Watcher Limits (Better Dev performance)", "sudo sysctl -w fs.inotify.max_user_watches=524288")
    
    # 2. Cleanup
    if os.path.exists("/usr/bin/apt"):
        apply_tweak("Cleaning APT Cache", "sudo apt-get clean")
    apply_tweak("Cleaning User Cache", f"rm -rf {os.path.expanduser('~/.cache/*')}")
    
    # 3. Docker Maintenance
    if subprocess.run(["command", "-v", "docker"], shell=True, capture_output=True).returncode == 0:
        apply_tweak("Pruning unused Docker resources", "docker system prune -f")
        
    print("✓ Linux Nexus optimizations applied.")

def optimize_mac():
    print("🌌 Initializing macOS Darwin Nexus Fusion...")
    
    # 1. Memory & Disk
    apply_tweak("Purging Inactive Memory", "sudo purge")
    apply_tweak("Flushing DNS Cache", "sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder")
    
    # 2. Cleanup
    apply_tweak("Cleaning User Cache", f"rm -rf {os.path.expanduser('~/.cache/*')}")
    
    print("✓ macOS optimizations applied.")

def run_ghost_mode():
    print("👻 Ghost Mode Engaged. Monitoring system for dynamic optimization...")
    import psutil
    import time
    
    high_perf_apps = ["rustc", "npm", "node", "ollama", "llama-cli", "python3", "docker", "vlc", "steam"]
    gaming_mode_active = False
    
    try:
        while True:
            # Check for high-performance apps
            active_apps = [p.name().lower() for p in psutil.process_iter(['name'])]
            found_high_perf = any(app in " ".join(active_apps) for app in high_perf_apps)
            
            if found_high_perf and not gaming_mode_active:
                print("🚀 High-performance application detected. Engaging Gaming Mode...")
                if platform.system() == "Windows":
                    # Ultimate Performance
                    subprocess.run('powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61', shell=True)
                elif platform.system() == "Linux":
                    # Simple linux equivalent
                    subprocess.run("sudo cpupower frequency-set -g performance", shell=True)
                gaming_mode_active = True
                
            elif not found_high_perf and gaming_mode_active:
                print("🍃 System idle. Reverting to balanced power...")
                if platform.system() == "Windows":
                    subprocess.run('powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e', shell=True)
                elif platform.system() == "Linux":
                    subprocess.run("sudo cpupower frequency-set -g powersave", shell=True)
                gaming_mode_active = False
                
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nGhost Mode terminated.")

def main():
    parser = argparse.ArgumentParser(description="Nexus Fusion System Optimizer for Aether")
    parser.add_argument("--auto", action="store_true", help="Run with default optimizations")
    parser.add_argument("--ghost", action="store_true", help="Engage background Ghost Mode")
    args = parser.parse_args()

    if args.ghost:
        run_ghost_mode()
        return

    system = platform.system()
    if system == "Windows":
        optimize_windows()
    elif system == "Linux":
        optimize_linux()
    elif system == "Darwin":
        optimize_mac()
    else:
        print(f"Unknown system: {system}. Basic cleanup only.")
        apply_tweak("Cleaning User Cache", f"rm -rf {os.path.expanduser('~/.cache/*')}")

if __name__ == "__main__":
    main()
