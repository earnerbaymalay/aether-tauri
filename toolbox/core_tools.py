"""
Aether Core Tools
Implementation for foundational tools used by the Aether agent.
"""
import os
import re
import subprocess
import platform
import datetime
import json
from pathlib import Path
from typing import Optional, List
import requests
import psutil

# --- File Operations ---

def read_file(path: str) -> str:
    """Reads the entire content of a file."""
    try:
        p = Path(path).expanduser()
        if not p.is_file():
            return f"Error: '{path}' is not a valid file."
        return p.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(path: str, content: str) -> str:
    """Writes content to a file, creating directories if needed."""
    try:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Success: Written to '{path}'."
    except Exception as e:
        return f"Error writing file: {str(e)}"

def edit_file(path: str, old_text: str, new_text: str) -> str:
    """Surgical replacement of text in a file."""
    try:
        p = Path(path).expanduser()
        if not p.is_file():
            return f"Error: '{path}' not found."
        content = p.read_text(encoding="utf-8")
        if old_text not in content:
            return f"Error: Original text not found in '{path}'."
        new_content = content.replace(old_text, new_text)
        p.write_text(new_content, encoding="utf-8")
        return f"Success: Updated '{path}'."
    except Exception as e:
        return f"Error editing file: {str(e)}"

def list_files(path: str) -> str:
    """Lists files and directories at a path."""
    try:
        p = Path(path).expanduser()
        if not p.is_dir():
            return f"Error: '{path}' is not a directory."
        
        items = sorted(os.listdir(p))
        files = [f for f in items if (p / f).is_file()]
        dirs = [d for d in items if (p / d).is_dir()]
        
        output = [f"Listing for: {p.absolute()}", ""]
        output.append("[Directories]")
        output.extend([f"  {d}/" for d in dirs] if dirs else ["  (None)"])
        output.append("\n[Files]")
        output.extend([f"  {f}" for f in files] if files else ["  (None)"])
        
        return "\n".join(output)
    except Exception as e:
        return f"Error: {str(e)}"

def grep_search(pattern: str, path: str, include_glob: str = "*") -> str:
    """Search for pattern in files using regex."""
    try:
        p = Path(path).expanduser()
        matches = []
        regex = re.compile(pattern, re.IGNORECASE)
        
        for file in p.rglob(include_glob):
            if file.is_file():
                try:
                    content = file.read_text(encoding="utf-8", errors="ignore")
                    for i, line in enumerate(content.splitlines(), 1):
                        if regex.search(line):
                            matches.append(f"{file.relative_to(p)}:{i}: {line.strip()}")
                except: continue
        
        return "\n".join(matches) if matches else "No matches found."
    except Exception as e:
        return f"Error: {str(e)}"

def glob_files(pattern: str, path: str = ".") -> str:
    """Lists files matching a glob pattern."""
    try:
        p = Path(path).expanduser()
        files = [str(f.relative_to(p)) for f in p.rglob(pattern) if f.is_file()]
        return "\n".join(files) if files else "No matches."
    except Exception as e:
        return f"Error: {str(e)}"

# --- System & Utility ---

def shell_exec(command: str) -> str:
    """Executes a shell command safely."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
        out = f"Code: {result.returncode}\n"
        if result.stdout: out += f"Out:\n{result.stdout[:5000]}\n"
        if result.stderr: out += f"Err:\n{result.stderr[:2000]}\n"
        return out
    except Exception as e:
        return f"Execution Error: {str(e)}"

def get_date() -> str:
    """Returns current system date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

def get_sys_info() -> str:
    """Returns detailed system and hardware information."""
    info = {
        "os": platform.system(),
        "os_release": platform.release(),
        "arch": platform.machine(),
        "cpu": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "hostname": platform.node()
    }
    return json.dumps(info, indent=2)

def get_battery() -> str:
    """Returns battery status if available."""
    battery = psutil.sensors_battery()
    if not battery:
        return "Battery information not available (Desktop or unsupported OS)."
    return f"Level: {battery.percent}% | Plugged in: {battery.power_plugged}"

# --- Network & Web ---

def web_search(query: str) -> str:
    """Privacy-first web search via DuckDuckGo."""
    try:
        url = "https://duckduckgo.com/html/"
        headers = {"User-Agent": "Mozilla/5.0"}
        params = {"q": query}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        
        # More robust extraction
        links = re.findall(r'href="([^"]+)" class="result__a"', r.text)
        if not links: return "No results found."
        
        results = [f"{i}. {l}" for i, l in enumerate(links[:5], 1)]
        return "\n".join(results)
    except Exception as e:
        return f"Search Error: {str(e)}"

def web_read(url: str) -> str:
    """Fetches web page content and returns it as text."""
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Aether-Agent/1.0"})
        r.raise_for_status()
        # Clean HTML tags (basic)
        text = re.sub(r'<[^>]+>', '', r.text)
        text = "\n".join([l.strip() for l in text.splitlines() if l.strip()])
        return text[:10000] # Cap output
    except Exception as e:
        return f"Read Error: {str(e)}"

# --- Future/Stubs ---

def gh_status() -> str:
    return shell_exec("git status")

def obsidian_list_notes() -> str:
    vault_path = Path.home() / "Documents/Obsidian Vault"
    if not vault_path.exists(): return "Obsidian vault not found."
    return glob_files("*.md", str(vault_path))

# ... (other stubs kept as is or implemented as needed)
def log_analyzer(log_path: str) -> str: return "Stub: Log analyzer logic pending."
def dependency_checker(project_path: str) -> str: return "Stub: Dependency checker logic pending."
def model_router(action: str) -> str: return "Stub: Model router logic pending."
def config_manager(action: str, key: str = None, value: str = None) -> str: return "Stub: Config manager logic pending."
def backup_manager(action: str) -> str: return "Stub: Backup manager logic pending."
def system_monitor() -> str: return "Stub: System monitor logic pending."
def lsp_server(action: str, file_path: str = None) -> str: return "Stub: LSP server logic pending."
def token_optimizer(text: str) -> str: return "Stub: Token optimizer logic pending."
def voice_ops(action: str, text: str = None) -> str: return "Stub: Voice ops logic pending."
def net_scan(target: str) -> str: return "Stub: Net scan logic pending."
def net_recon(target: str) -> str: return "Stub: Net recon logic pending."
