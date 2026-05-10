#!/usr/bin/env python3
"""
🌌 Aether Neural Operating Interface // V 26.05.1 (Premium TUI Edition)
High-performance Terminal-Only Agent Core with Advanced UX & Logging.
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
from logger import AetherLogger

# --- Constants & Configuration ---
DIR = Path.home() / "aether"
MODELS_DIR = DIR / "models"
TOOLBOX_DIR = DIR / "toolbox"
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

# Dynamic Hints
HINTS = [
    "Use AGENT for coding and tool-use tasks.",
    "The LOGIC pathway is best for architectural planning.",
    "Type 'settings' to configure the neural engine.",
    "AetherLink is listening for P2P sync on port 8888.",
    "Manage your long-term knowledge via '/memory'.",
    "Customize your experience in '/settings'.",
    "Use 'clear' to reset the interface view."
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
    "theme": "cyan",      # cyan, magenta, green, yellow, blue
    "verbosity": "NORMAL", # MINIMAL, NORMAL, DETAILED
    "log_level": "INFO"    # DEBUG, INFO, WARNING, ERROR
}

def load_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return {**DEFAULT_CONFIG, **json.load(f)}
        except:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

CONFIG = load_config()
LOGGER = AetherLogger(LOG_DIR, level=CONFIG["log_level"])

# --- Initialization ---
VAULT_PATHS = [VAULT_DIR]
SHARED_VAULT_PATH = Path("C:/Users/earnerbaymalay/Documents/vault")
if SHARED_VAULT_PATH.exists():
    VAULT_PATHS.append(SHARED_VAULT_PATH)

RAG = AetherRAG(VAULT_PATHS)
LINK = AetherLink(VAULT_DIR)

# --- Logic Classes ---

class HardwareMonitor:
    """Tracks real-time system resource utilization."""
    @staticmethod
    def get_stats():
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        return {"cpu": cpu, "ram": ram}

class SkillManifest:
    """The Skill Manifest: Dynamic tool loading from toolbox."""
    def __init__(self, manifest_path):
        self.manifest_path = Path(manifest_path)
        self.tools = []
        self.load_tools()

    def load_tools(self):
        if not self.manifest_path.exists():
            self.tools = []
            return
        try:
            with open(self.manifest_path, "r") as f:
                data = json.load(f)
                self.tools = [t for t in data.get("tools", []) if t.get("enabled", True)]
        except:
            self.tools = []

    def get_tool_descriptions(self):
        self.load_tools()
        desc = "Available Tools:\n"
        for t in self.tools:
            desc += f"- {t['name']}: {t['description']}\n"
        return desc

    def get_tool(self, name):
        self.load_tools()
        return next((t for t in self.tools if t["name"] == name), None)

MANIFEST = SkillManifest(TOOLBOX_DIR / "manifest.json")

class NeuralMemory:
    """Handles autonomous and manual memory fragment management."""
    def __init__(self, fragments_dir):
        self.fragments_dir = Path(fragments_dir)
        self.fragments_dir.mkdir(parents=True, exist_ok=True)

    def list_fragments(self):
        return sorted(list(self.fragments_dir.glob("*.md")), key=os.path.getmtime, reverse=True)

    def save_fragment(self, title, content, is_auto=False):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        filename = f"{'auto_' if is_auto else ''}{safe_title}_{timestamp}.md"
        path = self.fragments_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n{content}\n\n---\n*Type: {'Autonomous' if is_auto else 'Manual Fragment'} | Date: {datetime.now().strftime('%Y-%m-%d')}*")
        LOGGER.info(f"Memory fragment saved: {filename}")
        return path

    def synthesize_and_save(self, user_input, ai_response):
        prompt = f"""System: You are the Aether Memory Architect. 
Analyze the interaction. If there is new information about the user (preferences, facts, projects, system changes), 
distill it into a concise title and bullet points. If nothing is worth remembering, respond ONLY with 'NULL'.
User: {user_input}
AI: {ai_response}
Memory Update (Format: Title | Content):"""
        
        payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}
        try:
            r = requests.post(OLLAMA_API_URL, json=payload, timeout=15)
            update = r.json().get("response", "").strip()
            if "|" in update:
                title, content = update.split("|", 1)
                self.save_fragment(title.strip(), content.strip(), is_auto=True)
                return True
        except Exception as e:
            LOGGER.error(f"Memory synthesis failed: {e}")
        return False

MEMORY = NeuralMemory(FRAGMENTS_DIR)

# --- System Logic Functions ---

def get_user_sentiment(text):
    prompt = f"System: Analyze the sentiment. Respond with ONE WORD ONLY: CALM, URGENT, FRUSTRATED, CURIOUS, or HAPPY.\nUser: {text}\nSentiment: "
    payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=5)
        sentiment = r.json().get("response", "CALM").strip().upper()
        return sentiment if sentiment in ["CALM", "URGENT", "FRUSTRATED", "CURIOUS", "HAPPY"] else "CALM"
    except: return "CALM"

def check_command_safety(command):
    prompt = f"System: Aether Security Auditor. Destructive command? respond 'DANGEROUS' or 'SAFE'.\nCommand: {command}\nDecision: "
    payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=5)
        res = r.json().get("response", "SAFE").strip().upper()
        if "DANGEROUS" in res:
            LOGGER.warning(f"BLOCKED DANGEROUS COMMAND: {command}")
            return False
        return True
    except: return False

def verify_tool_output(intent, tool_name, output):
    prompt = f"System: Aether Neural Verifier. Did '{tool_name}' fulfill intent: {intent}?\nOutput: {output}\nDecision (SUCCESS/FAIL):"
    payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=10)
        return r.json().get("response", "SUCCESS").strip()
    except: return "SUCCESS"

def run_tool(name, args=""):
    LOGGER.info(f"Executing tool: {name} with args: {args}")
    if name == "shell_exec" and not check_command_safety(args):
        return "Security Alert: Command blocked by Aether Safety Guard."
    tool = MANIFEST.get_tool(name)
    if not tool: return f"Error: Tool '{name}' not found."
    script_path = TOOLBOX_DIR / tool["script"]
    try:
        import ast
        try:
            parsed = ast.literal_eval(f"({args})")
            cmd_args = [str(a) for a in parsed] if isinstance(parsed, tuple) else [str(parsed)]
        except: cmd_args = [args] if args else []
        cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)] + cmd_args
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return res.stdout.strip() if res.returncode == 0 else f"Error: {res.stderr.strip()}"
    except Exception as e: 
        LOGGER.error(f"Tool execution error ({name}): {e}")
        return str(e)

def generate_completion_stream(messages, model):
    payload = {"model": model, "messages": messages, "stream": True, "options": {"num_thread": CONFIG["threads"]}}
    try:
        r = requests.post(OLLAMA_CHAT_URL, json=payload, stream=True, timeout=120)
        for line in r.iter_lines():
            if line:
                content = json.loads(line.decode("utf-8")).get("message", {}).get("content", "")
                yield content
    except Exception as e: 
        LOGGER.error(f"Ollama stream error: {e}")
        yield f"Error: {e}"

def get_neural_guidance(query):
    prompt = f"System: Aether Neural Guide. Be extremely concise.\nUser: {query}\nGuide: "
    payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=10)
        return r.json().get("response", "Neural link unstable.")
    except: return "Guidance offline."

def get_neural_plan(query, context=""):
    prompt = f"System: Aether Logic Engine. 3-step plan for task.\nContext:\n{context}\nUser: {query}\nPlan:"
    payload = {"model": CONFIG["logic_model"], "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=45)
        return r.json().get("response", "Planning failed.")
    except: return "Logic engine offline."

def generate_system_profile(raw_report):
    prompt = f"System: Aether Personalization Engine. Concise User Persona.\nRaw Scan:\n{raw_report}\nPersona Profile:"
    payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=30)
        return r.json().get("response", "Profile generation failed.")
    except: return "Guidance offline."

def benchmark_tps():
    prompt = "Write a short 50-word technical summary of a CPU architecture."
    payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False, "options": {"num_predict": 100}}
    try:
        start = time.time()
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=15)
        duration = time.time() - start
        tokens = len(r.json().get("response", "").split()) * 1.3
        return tokens / duration if duration > 0 else 0.0
    except: return 0.0

def get_welcome_message():
    prompt = "System: Aether Guide. Concise welcome detailing multi-tier engine, fragmented memory, toolbox, and voice.\nWelcome Message:"
    payload = {"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}
    try:
        r = requests.post(OLLAMA_API_URL, json=payload, timeout=20)
        return r.json().get("response", "Welcome to Aether.")
    except: return "Welcome. System Online."

# --- Interaction Handlers ---

def handle_settings(ui):
    ui.mode = "SYSTEM_CONFIG"
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(ui.render_header())
        table = Table(title="[bold yellow]System Configuration[/bold yellow]", border_style="yellow")
        table.add_column("Key", style="cyan"); table.add_column("Value", style="magenta"); table.add_column("Description", style="dim")
        table.add_row("1. Uncensored", str(CONFIG["uncensored"]), "Toggle safety filters")
        table.add_row("2. RAG", str(CONFIG["rag_enabled"]), "Use AetherVault context")
        table.add_row("3. Threads", str(CONFIG["threads"]), "CPU threads for inference")
        table.add_row("4. Agent Model", CONFIG["active_model"], "Main reasoning engine")
        table.add_row("5. Turbo Model", CONFIG["turbo_model"], "Fast guidance engine")
        table.add_row("6. Logic Model", CONFIG["logic_model"], "Heavy planning engine")
        table.add_row("7. Auto-Memory", str(CONFIG["auto_memory"]), "Autonomous memory synthesis")
        table.add_row("8. Theme", CONFIG["theme"], "Primary UI color palette")
        table.add_row("9. Verbosity", CONFIG["verbosity"], "Output detail level")
        table.add_row("10. Log Level", CONFIG["log_level"], "Granularity of logs")
        
        console.print(table)
        console.print("\n[dim]Type a number to edit, 'help <num>', or 'back'.[/dim]")
        choice = console.input(f"[bold yellow]Settings » [/]").strip().lower()
        
        if choice == 'back': ui.mode = "NEURAL_LINK"; break
        
        if choice.startswith("help "):
            num = choice.split()[1]
            setting_map = {"1": "uncensored", "2": "rag_enabled", "3": "threads", "4": "active_model", "5": "turbo_model", "6": "logic_model", "7": "auto_memory", "8": "theme", "9": "verbosity", "10": "log_level"}
            if num in setting_map:
                with console.status("[dim]Consulting Neural Guide..."):
                    guidance = get_neural_guidance(f"Explain the technical impact of '{setting_map[num]}'.")
                console.print(Panel(guidance, title=f"Guidance: {setting_map[num]}", border_style=CONFIG["theme"]))
                console.input("\n[dim]Press Enter...[/]")
            continue

        if choice == '1': CONFIG["uncensored"] = not CONFIG["uncensored"]
        elif choice == '2': CONFIG["rag_enabled"] = not CONFIG["rag_enabled"]
        elif choice == '3':
            val = console.input("[bold white]New Thread Count » [/]")
            if val.isdigit(): CONFIG["threads"] = int(val)
        elif choice == '4':
            val = console.input("[bold white]New Agent Model ID » [/]")
            if val: CONFIG["active_model"] = val
        elif choice == '5':
            val = console.input("[bold white]New Turbo Model ID » [/]")
            if val: CONFIG["turbo_model"] = val
        elif choice == '6':
            val = console.input("[bold white]New Logic Model ID » [/]")
            if val: CONFIG["logic_model"] = val
        elif choice == '7': CONFIG["auto_memory"] = not CONFIG["auto_memory"]
        elif choice == '8':
            val = console.input("[bold white]New Theme (cyan/magenta/green/yellow/blue) » [/]").lower()
            if val in ["cyan", "magenta", "green", "yellow", "blue"]: CONFIG["theme"] = val
        elif choice == '9':
            val = console.input("[bold white]New Verbosity (MINIMAL/NORMAL/DETAILED) » [/]").upper()
            if val in ["MINIMAL", "NORMAL", "DETAILED"]: CONFIG["verbosity"] = val
        elif choice == '10':
            val = console.input("[bold white]New Log Level (DEBUG/INFO/WARNING/ERROR) » [/]").upper()
            if val in ["DEBUG", "INFO", "WARNING", "ERROR"]: 
                CONFIG["log_level"] = val
                LOGGER.set_level(val)
                
        save_config(CONFIG)

def handle_memory(ui):
    ui.mode = "MEMORY_VAULT"
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        console.print(ui.render_header())
        fragments = MEMORY.list_fragments()
        
        table = Table(title="[bold blue]Neural Memory Fragments[/bold blue]", border_style="blue", expand=True)
        table.add_column("#", justify="right", style="dim")
        table.add_column("Title", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Created", justify="right", style="dim")
        
        for i, frag in enumerate(fragments):
            f_type = "AUTO" if frag.name.startswith("auto_") else "MANUAL"
            date = datetime.fromtimestamp(os.path.getmtime(frag)).strftime("%Y-%m-%d")
            title = frag.name.split("_", 1)[1].replace(".md", "").replace("_", " ") if "_" in frag.name else frag.name
            table.add_row(str(i+1), title, f_type, date)
            if i > 9: break
            
        console.print(table)
        console.print("\n[dim]Commands: [bold]view <#> [/][bold]add [/][bold]edit <#> [/][bold]del <#> [/][bold]import [/][bold]back[/][/dim]")
        
        cmd = console.input("[bold blue]Memory » [/]").strip().lower()
        if cmd == 'back': ui.mode = "NEURAL_LINK"; break
        
        if cmd.startswith("view "):
            try:
                idx = int(cmd.split()[1]) - 1
                content = fragments[idx].read_text(encoding="utf-8")
                console.print(Panel(Markdown(content), title=fragments[idx].name, border_style=CONFIG["theme"]))
                console.input("\n[dim]Press Enter...[/]")
            except: pass
            
        elif cmd == "add":
            title = console.input("[bold white]Fragment Title » [/]")
            content = console.input("[bold white]Fragment Content » [/]")
            if title and content:
                MEMORY.save_fragment(title, content)
                RAG.index_vault()
                
        elif cmd.startswith("edit "):
            try:
                idx = int(cmd.split()[1]) - 1
                path = fragments[idx]
                title = console.input(f"[bold white]New Title (Current: {path.name}) » [/]")
                content = console.input("[bold white]New Content » [/]")
                if content:
                    os.remove(path)
                    MEMORY.save_fragment(title if title else "Edited Fragment", content)
                    RAG.index_vault()
            except: pass
            
        elif cmd.startswith("del "):
            try:
                idx = int(cmd.split()[1]) - 1
                os.remove(fragments[idx])
                RAG.index_vault()
            except: pass

        elif cmd == "import":
            console.print("[dim]Paste text from another source below (Type 'END' on a new line to finish):[/dim]")
            lines = []
            while True:
                line = console.input()
                if line.strip().upper() == "END": break
                lines.append(line)
            raw_text = "\n".join(lines)
            
            with console.status("[bold magenta]Neural Guide distilling import..."):
                prompt = f"System: Analyze this raw input. Distill into a concise memory fragment (Title | Content). Input:\n{raw_text}"
                res = requests.post(OLLAMA_API_URL, json={"model": CONFIG["turbo_model"], "prompt": prompt, "stream": False}).json().get("response", "")
                if "|" in res:
                    title, content = res.split("|", 1)
                    MEMORY.save_fragment(f"Imported: {title.strip()}", content.strip())
                    RAG.index_vault()
                    console.print("[green]✓ Memory imported and distilled.[/green]")
                    time.sleep(1)

# --- UI Render ---

class AetherUI:
    def __init__(self):
        self.history = []
        self.hint = HINTS[0]
        self.stats = {"tps": 0.0, "p2p_port": 0, "vault_size": 0}
        self.mode = "NEURAL_LINK"
        
    def render_header(self):
        status_color = "green" if "NEURAL_LINK" in self.mode else "yellow"
        hw = HardwareMonitor.get_stats()
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1); grid.add_column(justify="center", ratio=1); grid.add_column(justify="right", ratio=1)
        
        cpu_color = "red" if hw["cpu"] > 80 else "yellow" if hw["cpu"] > 50 else "green"
        ram_color = "red" if hw["ram"] > 80 else "yellow" if hw["ram"] > 50 else "green"

        grid.add_row(
            f"[bold {CONFIG['theme']}]🌌 AETHER[/bold {CONFIG['theme']}] [dim]v26.05.1[/dim]",
            f"[bold {status_color}]● {self.mode}[/bold {status_color}]",
            f"[dim]CPU: [{cpu_color}]{hw['cpu']:.0f}%[/][dim] | RAM: [{ram_color}]{hw['ram']:.0f}%[/][dim] | Vault: {self.stats['vault_size']} | P2P: {self.stats['p2p_port']}[/dim]"
        )
        info_line = f"[magenta]Model:[/] [bold white]{CONFIG['active_model']}[/] [dim]({CONFIG['threads']}T)[/dim] [dim]|[/] [magenta]Turbo:[/] {CONFIG['turbo_model']} [dim]|[/] [magenta]TPS:[/] {self.stats['tps']:.1f}"
        menu = "[dim]Commands: [bold]/settings[/] [bold]/memory[/] [bold]/models[/] [bold]/health[/] [bold]/clear[/] [bold]/exit[/][/dim]"
        return Panel(grid, title=info_line, subtitle=menu, border_style=CONFIG["theme"])

    def render_footer(self):
        return Text(f"💡 {self.hint}", justify="center", style="italic dim")

# --- Main Entry ---

def main():
    ui = AetherUI()
    scanner = SystemScanner()
    LINK.start_server(); ui.stats["p2p_port"] = LINK.port
    with console.status("[bold green]Syncing AetherVault..."): ui.stats["vault_size"] = RAG.index_vault()

    if not SYSTEM_PROFILE_PATH.exists():
        console.print(Panel("[bold yellow]NEURAL ONBOARDING REQUIRED[/bold yellow]\n\nAether has no profile. Grant permission for a **Neural System Scan**?\n- Dev tools\n- Project paths\n- Hardware specs\n\nStaying **100% local**.", border_style="yellow"))
        if console.input("[bold white]Allow Scan? (y/n) » [/]").strip().lower() == 'y':
            with console.status("[bold cyan]Scanning..."): raw = scanner.generate_report()
            with console.status("[bold magenta]Synthesizing..."): prof = generate_system_profile(raw)
            with console.status("[bold blue]Benchmarking..."): ui.stats["tps"] = benchmark_tps()
            SYSTEM_PROFILE_PATH.write_text(f"# SYSTEM_PROFILE.md\n\n{prof}\n\n{raw}", encoding="utf-8")
            ui.stats["vault_size"] = RAG.index_vault()
            console.print(Panel(prof, title="[bold green]Profile Synchronized[/bold green]", border_style="green")); time.sleep(2)

    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(ui.render_header())
    with console.status("[dim]Initializing Neural Link..."): welcome = get_welcome_message()
    console.print(Panel(Markdown(welcome), title="[bold cyan]SYSTEM INITIALIZED[/bold cyan]", border_style=CONFIG["theme"], padding=(1, 2)))
    
    history = [{"role": "system", "content": f"You are Aether. Technical, precise. Computer Use protocol active.\n{MANIFEST.get_tool_descriptions()}"}]

    while True:
        try:
            user_input = console.input("\n[bold white]User » [/]").strip()
            if not user_input: continue
            if user_input.startswith("/"):
                cmd = user_input[1:].lower()
                if cmd in ["exit", "quit"]: break
                if cmd == "clear": os.system('cls' if os.name == 'nt' else 'clear'); console.print(ui.render_header()); continue
                if cmd == "settings": handle_settings(ui); continue
                if cmd == "memory": handle_memory(ui); continue
                if cmd == "models": console.print(f"[bold cyan]Active Models:[/]\n- Agent: {CONFIG['active_model']}\n- Turbo: {CONFIG['turbo_model']}\n- Logic: {CONFIG['logic_model']}"); continue
                if cmd == "health":
                    with console.status("[dim]Checking..."): h = run_tool("system_monitor"); d = run_tool("dependency_checker")
                    console.print(Panel(h, title="Vitals", border_style="green")); console.print(Panel(d, title="Deps", border_style="blue")); continue
                guidance = get_neural_guidance(user_input); console.print(f"[yellow]![/] {guidance}"); continue

            ui.mode = "NEURAL_LINK"
            def bg_sentiment():
                ui.mode = f"NEURAL_LINK: {get_user_sentiment(user_input)}"
            threading.Thread(target=bg_sentiment, daemon=True).start()
            
            context = RAG.query(user_input) if CONFIG["rag_enabled"] else ""
            
            # Logic Tier Planning (Verbosity Dependent)
            if len(user_input.split()) > 10 and CONFIG["verbosity"] != "MINIMAL":
                with console.status("[bold magenta]Planning..."): plan = get_neural_plan(user_input, context)
                console.print(Panel(plan, title="Neural Plan", border_style="magenta"))

            history.append({"role": "user", "content": f"Context:\n{context}\nUser: {user_input}"})
            
            while True:
                console.print("[bold cyan]AI » [/]", end="")
                resp = ""; start = time.time(); tokens = 0
                for chunk in generate_completion_stream(history, CONFIG["active_model"]):
                    console.print(chunk, end=""); resp += chunk; tokens += 1
                ui.stats["tps"] = tokens / (time.time() - start) if (time.time()-start) > 0 else 0
                console.print(""); console.print(ui.render_header())

                if CONFIG["auto_memory"]: 
                    def bg_memory():
                        if MEMORY.synthesize_and_save(user_input, resp):
                            ui.stats["vault_size"] = RAG.index_vault()
                    threading.Thread(target=bg_memory, daemon=True).start()

                match = re.search(r"<tool>(\w+)\((.*)\)</tool>", resp)
                if match:
                    name, args = match.groups()
                    with console.status(f"[dim]Executing {name}..."): obs = run_tool(name, args)
                    with console.status("[dim]Verifying..."): ver = verify_tool_output(user_input, name, obs)
                    if "FAIL" in ver.upper():
                        console.print(Panel(f"[red]Result:[/]\n{obs}\n\n[bold yellow]Verification:[/]\n{ver}", title=f"Tool: {name}", border_style="yellow", expand=False))
                        history.append({"role": "assistant", "content": resp}); history.append({"role": "user", "content": f"Observation: {obs}\nVerification: {ver}"})
                        continue
                    
                    if CONFIG["verbosity"] == "DETAILED":
                        console.print(Panel(obs, title=f"Tool: {name}", border_style="green", expand=False))
                    
                    history.append({"role": "assistant", "content": resp}); history.append({"role": "user", "content": f"Observation: {obs}"})
                    continue
                history.append({"role": "assistant", "content": resp}); break
            ui.hint = random.choice(HINTS); console.print(ui.render_footer())
        except KeyboardInterrupt: break
        except Exception as e: 
            LOGGER.error(f"System Error: {e}")
            console.print(f"[bold red]System Error:[/] {e}")

if __name__ == "__main__":
    main()
