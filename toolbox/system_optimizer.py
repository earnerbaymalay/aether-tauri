import os
import platform
import subprocess
from pathlib import Path

def optimize_windows():
    print("🌌 Optimizing Windows (Nexus11 Fusion Logic)...")
    # 1. Clean Temp Files
    subprocess.run(["powershell.exe", "-Command", "Remove-Item -Path $env:TEMP\* -Recurse -Force -ErrorAction SilentlyContinue"], capture_output=True)
    # 2. Flush DNS
    subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    # 3. Optimize Network Throttling
    subprocess.run(["powershell.exe", "-Command", "Set-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile' -Name 'NetworkThrottlingIndex' -Value 0xffffffff"], capture_output=True)
    print("✓ Windows optimizations applied.")

def optimize_linux():
    print("🌌 Optimizing Linux (Native Logic)...")
    # 1. Clean Package Manager Cache
    if os.path.exists("/usr/bin/apt"):
        subprocess.run(["sudo", "apt-get", "clean"], capture_output=True)
    # 2. Optimize Swappiness (Reduce disk thrashing)
    subprocess.run(["sudo", "sysctl", "vm.swappiness=10"], capture_output=True)
    # 3. Clean user cache
    subprocess.run(["rm", "-rf", os.path.expanduser("~/.cache/*")], capture_output=True)
    print("✓ Linux optimizations applied.")

def optimize_mac():
    print("🌌 Optimizing macOS (Darwin Logic)...")
    # 1. Purge memory
    subprocess.run(["sudo", "purge"], capture_output=True)
    # 2. Flush DNS
    subprocess.run(["sudo", "dscacheutil", "-flushcache"], capture_output=True)
    subprocess.run(["sudo", "killall", "-HUP", "mDNSResponder"], capture_output=True)
    print("✓ macOS optimizations applied.")

def main():
    system = platform.system()
    if system == "Windows":
        optimize_windows()
    elif system == "Linux":
        optimize_linux()
    elif system == "Darwin":
        optimize_mac()
    else:
        print(f"Unknown system: {system}. Basic cleanup only.")
        subprocess.run(["rm", "-rf", os.path.expanduser("~/.cache/*")], capture_output=True)

if __name__ == "__main__":
    main()
