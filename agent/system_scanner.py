import os
import subprocess
import json
import platform
from pathlib import Path

class SystemScanner:
    def __init__(self):
        self.findings = {}

    def scan(self):
        """Performs a comprehensive system scan for Aether personalization."""
        self.findings["platform"] = platform.system()
        self.findings["platform_release"] = platform.release()
        self.findings["cpu"] = platform.processor()
        
        # 1. User Identity Discovery
        self.findings["user"] = self._discover_user_info()
        
        # 2. Dev Tools Check
        self.findings["tools"] = self._check_tools()
        
        # 3. Project Discovery
        self.findings["projects"] = self._discover_projects()
        
        # 4. Environment Highlights
        self.findings["env_highlights"] = {
            k: v for k, v in os.environ.items() 
            if any(x in k.lower() for x in ["path", "user", "appdata", "editor", "shell", "git", "ollama"])
        }
        
        return self.findings

    def _discover_user_info(self):
        """Attempts to find user identity via git and OS."""
        user = {
            "name": os.getlogin() if hasattr(os, "getlogin") else os.environ.get("USERNAME"),
            "git_name": "Unknown",
            "git_email": "Unknown"
        }
        try:
            name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, timeout=2)
            if name.returncode == 0: user["git_name"] = name.stdout.strip()
            email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True, timeout=2)
            if email.returncode == 0: user["git_email"] = email.stdout.strip()
        except:
            pass
        return user

    def _check_tools(self):
        tools = {}
        check_list = ["node", "npm", "python", "git", "gh", "docker", "ollama", "ffmpeg", "rustc", "cargo", "tauri"]
        for tool in check_list:
            try:
                # Some tools use --version, some just version
                cmd = [tool, "--version"]
                if tool == "tauri": cmd = ["cargo", "tauri", "--version"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    tools[tool] = result.stdout.strip().split("\n")[0]
            except:
                continue
        return tools

    def _discover_projects(self):
        """Heuristic search for user project directories."""
        projects = []
        home = Path.home()
        search_roots = [home, home / "Documents", home / "Desktop", home / "source" / "repos"]
        
        seen_dirs = set()
        for root in search_roots:
            if not root.exists(): continue
            try:
                for p in root.iterdir():
                    if p.is_dir() and not p.name.startswith("."):
                        if (p / ".git").exists() or (p / "package.json").exists() or (p / "requirements.txt").exists() or (p / "Cargo.toml").exists():
                            projects.append({"name": p.name, "path": str(p)})
                            seen_dirs.add(p)
                    if len(projects) > 20: break
            except:
                continue
        return projects

    def generate_report(self):
        """Converts findings into a raw technical Markdown report."""
        scan_data = self.scan()
        report = "# RAW SYSTEM SCAN REPORT\n\n"
        
        report += "## User Identity\n"
        report += f"- **System User:** {scan_data['user']['name']}\n"
        report += f"- **Git Name:** {scan_data['user']['git_name']}\n"
        report += f"- **Git Email:** {scan_data['user']['git_email']}\n\n"
        
        report += "## System Specs\n"
        report += f"- **OS:** {scan_data['platform']} {scan_data['platform_release']}\n"
        report += f"- **CPU:** {scan_data['cpu']}\n\n"
        
        report += "## Installed Runtimes & CLIs\n"
        for tool, ver in scan_data["tools"].items():
            report += f"- **{tool}:** {ver}\n"
        
        report += "\n## Discovered Projects\n"
        for proj in scan_data["projects"]:
            report += f"- **{proj['name']}** (`{proj['path']}`)\n"
            
        return report
