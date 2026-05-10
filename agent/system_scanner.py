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
        
        # 1. Dev Tools Check
        self.findings["tools"] = self._check_tools()
        
        # 2. Project Discovery (Scan home directory for common project markers)
        self.findings["projects"] = self._discover_projects()
        
        # 3. Environment Variables (Relevant ones)
        self.findings["env_highlights"] = {
            k: v for k, v in os.environ.items() 
            if any(x in k.lower() for x in ["path", "user", "appdata", "editor", "shell"])
        }
        
        return self.findings

    def _check_tools(self):
        tools = {}
        check_list = ["node", "npm", "python", "git", "gh", "docker", "ollama", "ffmpeg", "go", "rustc"]
        for tool in check_list:
            try:
                result = subprocess.run([tool, "--version"], capture_output=True, text=True, timeout=2)
                if result.returncode == 0:
                    tools[tool] = result.stdout.strip().split("\n")[0]
            except:
                continue
        return tools

    def _discover_projects(self):
        """Heuristic search for user project directories."""
        projects = []
        home = Path.home()
        # Common places to look
        search_roots = [home, home / "Documents", home / "Desktop"]
        
        seen_dirs = set()
        for root in search_roots:
            if not root.exists(): continue
            try:
                # Look for .git or package.json as project markers
                for p in root.iterdir():
                    if p.is_dir() and not p.name.startswith("."):
                        if (p / ".git").exists() or (p / "package.json").exists() or (p / "requirements.txt").exists():
                            projects.append({"name": p.name, "path": str(p)})
                            seen_dirs.add(p)
                    if len(projects) > 15: break # Limit discovery
            except:
                continue
        return projects

    def generate_report(self):
        """Converts findings into a raw technical Markdown report."""
        scan_data = self.scan()
        report = "# RAW SYSTEM SCAN REPORT\n\n"
        
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
