#!/usr/bin/env python3
"""
🌌 Aether Neural Operating Interface // V 26.05.1
High-performance Agent Core with Multi-Step Tool Loops & Universal Skills.
"""

import os, sys, json, re, subprocess, threading, time, requests, random, psutil
from pathlib import Path
from datetime import datetime

# UI Imports
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.markdown import Markdown
from rich.text import Text
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule

# Logic Imports
from rag_engine import AetherRAG
from p2p_sync import AetherLink
from system_scanner import SystemScanner
from skill_loader import UniversalSkillEngine
from logger import AetherLogger

# --- Constants & Configuration ---
AGENT_ROOT = Path(__file__).resolve().parent.parent
DIR = Path.home() / "aether"
MODELS_DIR = DIR / "models"
TOOLBOX_DIR = AGENT_ROOT / "toolbox"
KNOWLEDGE_DIR = DIR / "knowledge"
VAULT_DIR = KNOWLEDGE_DIR / "aethervault"
FRAGMENTS_DIR = VAULT_DIR / "fragments"
LOG_DIR = Path.home() / ".aether" / "logs"
SESSION_DIR = Path.home() / ".aether" / "sessions"
CONFIG_FILE = Path.home() / ".aether" / "config.json"
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
SYSTEM_PROFILE_PATH = VAULT_DIR / "SYSTEM_PROFILE.md"

FRAGMENTS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

console = Console()
SKILLS = UniversalSkillEngine(AGENT_ROOT)

# Dynamic Hints
HINTS = [
    "Use AGENT for coding and tool-use tasks.",
    "The LOGIC pathway is best for architectural planning.",
    "Type '/settings' to configure the neural engine.",
    "AetherLink is listening for P2P sync on port 8888.",
    "Manage your knowledge via '/memory'.",
    "Aether supports multi-step tool loops (ReAct).",
    "Try dropping a CLAUDE.md file to import skills.",
    "Use '/health' to check system vitals and dependencies.",
    "Need to fix a terminal error? Use '/auto-fix'.",
    "Type '/help' to see all available slash commands.",
    "The Shadow Monitor autonomously extracts facts in the background.",
    "Specialized Coder model is active for '/auto-fix' tasks."
]

# --- State & Persistence ---
DEFAULT_CONFIG = {
    "threads": 6,
    "uncensored": False,
    "auto_memory": True,
    "rag_enabled": True,
    "active_model": "hermes3:8b",
    "turbo_model": "llama3.2:3b",
    "logic_model": "deepseek-r1:8b",
    "theme": "cyan",
    "verbosity": "NORMAL",
    "log_level": "INFO",
    "browser_type": "firefox"
}

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except: return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

CONFIG = load_config()
LOGGER = AetherLogger(LOG_DIR, level=CONFIG["log_level"])

# --- Initialization ---
VAULT_PATHS = [VAULT_DIR]

RAG = AetherRAG(VAULT_PATHS)
LINK = AetherLink(VAULT_DIR)

# --- Logic Classes ---

class HardwareMonitor:
    @staticmethod
    def get_stats():
        return {"cpu": psutil.cpu_percent(), "ram": psutil.virtual_memory().percent}

class SkillManifest:
    def __init__(self, manifest_path):
        self.manifest_path = Path(manifest_path)
        self.tools = []
        self.load_tools()

    def load_tools(self):
        if not self.manifest_path.exists(): return
        try:
            with open(self.manifest_path, "r") as f:
                data = json.load(f)
                self.tools = [t for t in data.get("tools", []) if t.get("enabled", True)]
        except: pass

    def get_tool_descriptions(self):
        self.load_tools()
        return "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])

    def get_tool(self, name):
        self.load_tools()
        return next((t for t in self.tools if t["name"] == name), None)

MANIFEST = SkillManifest(TOOLBOX_DIR / "manifest.json")

class NeuralMemory:
    def __init__(self, fragments_dir):
        self.fragments_dir = Path(fragments_dir)

    def list_fragments(self):
        return sorted(list(self.fragments_dir.glob("*.md")), key=os.path.getmtime, reverse=True)

    def save_fragment(self, title, content, is_auto=False, is_shadow=False):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        prefix = "auto_" if is_auto else "shadow_" if is_shadow else ""
        path = self.fragments_dir / f"{prefix}{safe_title}_{timestamp}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}\n\n---\n*Type: {'Shadow' if is_shadow else 'Auto' if is_auto else 'Manual'} | {datetime.now().strftime('%Y-%m-%d')}*")
        return path

    def background_shadow_monitor(self, user_input, ai_response):
        prompt = f"System: Aether Shadow Monitor. Extract facts/prefs (Title | Content) or respond 'NULL'.\nUser: {user_input}\nAI: {ai_response}\nExtraction:"
        try:
            r = requests.post(OLLAMA_API_URL, json={"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}, timeout=20)
            update = r.json().get("response", "").strip()
            if "|" in update and "NULL" not in update.upper():
                title, content = update.split("|", 1)
                self.save_fragment(title.strip(), content.strip(), is_shadow=True)
        except: pass

MEMORY = NeuralMemory(FRAGMENTS_DIR)

# --- System Functions ---

def run_tool(name, args=""):
    LOGGER.info(f"Tool: {name} | Args: {args}")
    if name == "shell_exec" and "rm -rf" in args: return "Error: Destructive command blocked."
    if name == "mcp_call": return "MCP Error: No active MCP host found."
    
    tool = MANIFEST.get_tool(name)
    if not tool: return f"Error: Tool '{name}' not found."
    
    try:
        import core_tools
        if hasattr(core_tools, name):
            try:
                import shlex
                try:
                    parsed = json.loads(f"[{args}]")
                    cmd_args = [str(a) for a in parsed]
                except:
                    cmd_args = shlex.split(args)
            except: cmd_args = [args.strip()] if args else []
            return str(getattr(core_tools, name)(*cmd_args))
    except Exception as e:
        pass # fallback to script if not in core_tools

    try:
        import shlex
        try:
            try:
                parsed = json.loads(f"[{args}]")
                cmd_args = [str(a) for a in parsed]
            except:
                cmd_args = shlex.split(args)
        except: cmd_args = [args.strip()] if args else []
            
        if os.name == 'nt':
            cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(TOOLBOX_DIR / tool["script"])] + cmd_args
        else:
            script_path = TOOLBOX_DIR / tool["script"]
            if script_path.suffix == ".ps1":
                sh_variant = script_path.with_suffix(".sh")
                if sh_variant.exists(): script_path = sh_variant
                else:
                    py_variant = script_path.with_suffix(".py")
                    if py_variant.exists(): script_path = py_variant
            
            if script_path.suffix == ".py":
                cmd = [sys.executable, str(script_path)] + cmd_args
            else:
                cmd = ["bash", str(script_path)] + cmd_args
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return res.stdout.strip() if res.returncode == 0 else f"Error: {res.stderr.strip()}"
    except Exception as e: return str(e)

def verify_tool_output(intent, tool_name, output):
    prompt = f"System: Verifier. Did {tool_name} fulfill {intent}?\nOutput: {output}\nDecision (SUCCESS/FAIL):"
    try:
        r = requests.post(OLLAMA_API_URL, json={"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}, timeout=10)
        return r.json().get("response", "SUCCESS").strip()
    except: return "SUCCESS"

def generate_completion_stream(messages, model):
    payload = {"model": model, "messages": messages, "stream": True, "options": {"num_thread": CONFIG["threads"]}}
    try:
        r = requests.post(OLLAMA_CHAT_URL, json=payload, stream=True, timeout=120)
        for line in r.iter_lines():
            if line: yield json.loads(line.decode("utf-8")).get("message", {}).get("content", "")
    except: yield "Link unstable."

def get_neural_plan(query, context=""):
    prompt = f"System: Planner. 3-step plan.\nContext: {context}\nUser: {query}\nPlan:"
    try:
        r = requests.post(OLLAMA_API_URL, json={"model": CONFIG["logic_model"], "prompt": prompt, "stream": False}, timeout=45)
        return r.json().get("response", "Planning failed.")
    except: return "Logic engine offline."

# --- Interaction Handlers ---

def handle_help(ui):
    ui.mode = "HELP"
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(ui.render_header())
    table = Table(title="Aether Command Reference", border_style="cyan", expand=True)
    table.add_column("Command", style="yellow"); table.add_column("Description")
    table.add_row("/help", "Display this reference guide")
    table.add_row("/settings", "Configure models, threads, and browser")
    table.add_row("/memory", "Manage AetherVault memory fragments")
    table.add_row("/auto-fix", "Self-healing error analysis")
    table.add_row("/health", "Check system vitals and dependencies")
    table.add_row("/clear", "Reset interface view")
    table.add_row("/exit", "Terminate session")
    console.print(table)
    console.input("\nPress Enter to return...")

def handle_settings(ui):
    ui.mode = "SETTINGS"
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(ui.render_header())
        table = Table(title="System Configuration", border_style="yellow")
        table.add_column("Key", style="cyan"); table.add_column("Value", style="magenta")
        table.add_row("1. Uncensored", str(CONFIG["uncensored"]))
        table.add_row("2. RAG", str(CONFIG["rag_enabled"]))
        table.add_row("3. Threads", str(CONFIG["threads"]))
        table.add_row("4. Browser", CONFIG["browser_type"])
        table.add_row("5. Browser Path", CONFIG["browser_path"])
        table.add_row("6. Theme", CONFIG["theme"])
        table.add_row("7. Log Level", CONFIG["log_level"])
        console.print(table)
        choice = console.input("\nEdit # or 'back' » ").strip()
        if choice == 'back': break
        if choice == '1': CONFIG["uncensored"] = not CONFIG["uncensored"]
        elif choice == '2': CONFIG["rag_enabled"] = not CONFIG["rag_enabled"]
        elif choice == '3': CONFIG["threads"] = int(console.input("Threads » "))
        elif choice == '4': CONFIG["browser_type"] = console.input("Browser » ")
        elif choice == '5': CONFIG["browser_path"] = console.input("Path » ")
        elif choice == '6': CONFIG["theme"] = console.input("Theme » ")
        elif choice == '7': CONFIG["log_level"] = console.input("Log Level » ")
        save_config(CONFIG)

def handle_memory(ui):
    ui.mode = "VAULT"
    fragments = MEMORY.list_fragments()
    table = Table(title="AetherVault Fragments")
    table.add_column("#"); table.add_column("Title"); table.add_column("Date")
    for i, f in enumerate(fragments[:10]):
        table.add_row(str(i+1), f.name, datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m-%d"))
    console.print(table)
    console.input("\nPress Enter...")

def handle_auto_fix(ui, error):
    console.print(f"[yellow]Analyzing fix for:[/] {error}")
    prompt = f"System: Auto-Fix. Suggest 1-step command.\nError: {error}\nFix:"
    res = requests.post(OLLAMA_API_URL, json={"model": CONFIG["logic_model"], "prompt": prompt, "stream": False}).json().get("response", "")
    console.print(Panel(res, title="Suggestion"))
    if "```" in res and console.input("Apply? (y/n) » ").lower() == 'y':
        cmd = re.search(r"```.*?\n(.*?)\n```", res, re.DOTALL).group(1)
        console.print(run_tool("shell_exec", cmd))

# --- UI & Main ---

class AetherUI:
    def __init__(self):
        self.stats = {"tps": 0.0, "p2p_port": 8888, "vault_size": 0}
        self.mode = "NEURAL_LINK"
        self.hint = random.choice(HINTS)
        
    def rotate_hint(self):
        self.hint = random.choice(HINTS)

    def render_header(self):
        hw = HardwareMonitor.get_stats()
        grid = Table.grid(expand=True)
        grid.add_column(); grid.add_column(); grid.add_column()
        grid.add_row(f"[bold {CONFIG['theme']}]🌌 AETHER[/] [dim]v26.05.1[/]", f"[bold]● {self.mode}[/]", f"[dim]CPU: {hw['cpu']}% | RAM: {hw['ram']}% | Vault: {self.stats['vault_size']}[/]")
        menu = "[dim]Commands: [bold]/settings /memory /health /auto-fix /help[/][/dim]"
        return Panel(grid, title=f"Model: {CONFIG['active_model']} | TPS: {self.stats['tps']:.1f}", subtitle=menu, border_style=CONFIG["theme"])

    def render_footer(self):
        return Text(f"💡 {self.hint}", justify="center", style="italic dim")

def chat_loop(ui, history):
    while True:
        try:
            ui.rotate_hint()
            console.print(ui.render_footer())
            user_input = console.input("\n[bold white]User » [/]").strip()
            if not user_input: continue
            if user_input.startswith("/"):
                cmd = user_input[1:].lower()
                if cmd == "exit": break
                if cmd == "help": handle_help(ui); continue
                if cmd == "settings": handle_settings(ui); continue
                if cmd == "memory": handle_memory(ui); continue
                if cmd == "auto-fix": handle_auto_fix(ui, console.input("Error » ")); continue
                if cmd == "clear": os.system('cls' if os.name == 'nt' else 'clear'); console.print(ui.render_header()); continue
                continue

            ui.mode = "NEURAL_LINK"
            context = RAG.query(user_input) if CONFIG["rag_enabled"] else ""
            if len(user_input.split()) > 10:
                with console.status("[magenta]Planning..."): console.print(Panel(get_neural_plan(user_input, context), title="Neural Plan"))

            history.append({"role": "user", "content": f"Context: {context}\nUser: {user_input}"})
            
            for step in range(10): # Max 10 steps
                console.print("[bold cyan]AI » [/]", end="")
                resp = ""; start = time.time(); tokens = 0
                for chunk in generate_completion_stream(history, CONFIG["active_model"]):
                    console.print(chunk, end="")
                    sys.stdout.flush()
                    resp += chunk; tokens += 1
                ui.stats["tps"] = tokens / (time.time() - start) if (time.time()-start) > 0 else 0
                console.print("")
                sys.stdout.flush()
                console.print(ui.render_header())

                threading.Thread(target=lambda: MEMORY.background_shadow_monitor(user_input, resp), daemon=True).start()

                tool_match = re.search(r"<tool>(\w+)\((.*?)\)</tool>", resp, re.DOTALL)
                if tool_match:
                    name, args = tool_match.groups()
                    history.append({"role": "assistant", "content": resp})
                    with console.status(f"[yellow]Step {step+1}: {name}..."):
                        obs = run_tool(name, args)
                        ver = verify_tool_output(user_input, name, obs)
                    console.print(Panel(obs, title=f"Step {step+1}: {name} ({ver})", border_style="green" if "SUCCESS" in ver.upper() else "yellow"))
                    history.append({"role": "user", "content": f"Observation: {obs}\nVerification: {ver}"})
                    continue
                history.append({"role": "assistant", "content": resp}); break
        except KeyboardInterrupt: break

def main():
    ui = AetherUI()
    with console.status("[green]Syncing..."): ui.stats["vault_size"] = RAG.index_vault()
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(ui.render_header())
    SKILLS.discover_skills(os.getcwd())
    
    prompt = f"""You are Aether. Technical Agent.
PROTOCOL: Use <tool>name(args)</tool> for all actions. Solve tasks iteratively.
TOOLS:
{MANIFEST.get_tool_descriptions()}
{SKILLS.get_skill_prompt()}
"""
    chat_loop(ui, [{"role": "system", "content": prompt}])

if __name__ == "__main__":
    main()
