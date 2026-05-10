import os
import json
import re
import subprocess
import requests
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.status import Status
from rich.rule import Rule
from rich.syntax import Syntax

# --- Configuration ---
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "hermes3:8b"  # Capable and uncensored
# Search for toolbox in common locations
possible_paths = [
    Path.home() / "aether-tauri" / "toolbox",
    Path.home() / "aether" / "toolbox",
    Path("C:/Users/earnerbaymalay/aether-tauri/toolbox")
]
TOOLBOX_DIR = next((p for p in possible_paths if p.exists()), possible_paths[0])
MANIFEST_PATH = TOOLBOX_DIR / "manifest.json"

console = Console()

class Hands:
    """The Hands: External Code / Tools"""
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.tools = self._load_tools()

    def _load_tools(self):
        if not self.manifest_path.exists():
            return []
        with open(self.manifest_path, 'r') as f:
            return json.load(f).get("tools", [])

    def get_tool_descriptions(self):
        return "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])

    def execute(self, tool_name, args_str):
        tool = next((t for t in self.tools if t["name"] == tool_name), None)
        if not tool:
            return f"Error: Tool '{tool_name}' not found."
        
        script_path = TOOLBOX_DIR / tool["script"]
        try:
            # Smart argument parsing: try to parse as a comma-separated list of strings or JSON
            # For simplicity, we'll split by comma if not valid JSON
            import ast
            try:
                # Use ast.literal_eval to safely parse tuple-like strings: "path", "content"
                args = ast.literal_eval(f"({args_str})")
                if isinstance(args, tuple):
                    cmd_args = [str(a) for a in args]
                else:
                    cmd_args = [str(args)]
            except:
                cmd_args = [args_str]

            cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)] + cmd_args
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return f"Error executing tool: {result.stderr.strip()}"
            return result.stdout.strip()
        except Exception as e:
            return f"Exception during tool execution: {str(e)}"

class NervousSystem:
    """The Nervous System: Agent Logic / Framework"""
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.hands = Hands(MANIFEST_PATH)
        self.history = [
            {"role": "system", "content": f"""You are Aether, an advanced autonomous agent with full 'Computer Use' capabilities.
            
You operate using a Brain-Nervous System-Hands architecture.
- Brain: Your LLM core ({self.model}).
- Nervous System: Your reasoning, planning, and recursive loop.
- Hands: Your tools for interacting with the file system, network, and OS.

Available Hands (Tools):
{self.hands.get_tool_descriptions()}

Computer Use Protocol:
1. Goal: Accomplish the user's task autonomously.
2. Multi-step: Use as many tool calls as needed. Read files to understand context, write files to save work, use shell_exec for advanced operations.
3. Tool Format: <tool>tool_name(arg1, arg2, ...)</tool>
   - Example: <tool>write_file("test.txt", "hello world")</tool>
   - Example: <tool>shell_exec("dir /s")</tool>
4. Reasoning: Before each tool call, explain your plan. After each observation, analyze the result.
5. Finality: Only provide a final answer when the task is complete.

Be technical, precise, and exert your full computer use capabilities to solve complex problems.
"""}
        ]

    def think(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        console.print(Rule(style="dim"))
        
        while True:
            # 1. The Brain decides what to do
            with console.status("[bold cyan]Brain reasoning...", spinner="dots", spinner_style="cyan"):
                response = self._call_brain()
            
            # 2. The Nervous System checks for tool calls
            tool_match = re.search(r"<tool>(\w+)\((.*)\)</tool>", response)
            if tool_match:
                tool_name, tool_args = tool_match.groups()
                
                # Show reasoning before tool call
                reasoning_text = response.split("<tool>")[0].strip()
                if reasoning_text:
                    console.print(Panel(Markdown(reasoning_text), title="[bold blue]🧠 Brain[/bold blue]", border_style="blue", padding=(1, 2)))
                
                # 3. The Hands execute the tool
                console.print(f"[bold magenta]⚡ Nervous System[/bold magenta] dispatching to [bold yellow]Hands[/bold yellow]: [bold]{tool_name}({tool_args})[/bold]")
                with console.status(f"[bold yellow]Executing {tool_name}...", spinner="bouncingBar", spinner_style="yellow"):
                    observation = self.hands.execute(tool_name, tool_args)
                
                # Format observation output
                obs_content = observation if observation else "Process completed with no output."
                console.print(Panel(obs_content, title=f"[bold green]👁️ Observation: {tool_name}[/bold green]", border_style="green", padding=(1, 2)))
                
                # Add observation to history and loop back to the Brain
                self.history.append({"role": "assistant", "content": response})
                self.history.append({"role": "user", "content": f"Observation: {observation}"})
                continue
            else:
                # No more tools needed, final response
                console.print(Panel(Markdown(response), title="[bold cyan]✨ Final Response[/bold cyan]", border_style="cyan", padding=(1, 2)))
                self.history.append({"role": "assistant", "content": response})
                return response

    def _call_brain(self):
        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": False
        }
        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=120)
            r.raise_for_status()
            return r.json()["message"]["content"]
        except Exception as e:
            return f"Brain Error: {str(e)}"

# --- Main Interaction ---
def main():
    agent = NervousSystem()
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = """
[bold cyan]█████╗ ███████╗████████╗██╗  ██╗███████╗██████╗     █████╗ ██╗[/bold cyan]
[bold cyan]██╔══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗   ██╔══██╗██║[/bold cyan]
[bold cyan]███████║█████╗     ██║   ███████║█████╗  ██████╔╝   ███████║██║[/bold cyan]
[bold cyan]██╔══██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗   ██╔══██║██║[/bold cyan]
[bold cyan]██║  ██║███████╗   ██║   ██║  ██║███████╗██║  ██║██╗██║  ██║██║[/bold cyan]
[bold cyan]╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝[/bold cyan]
    """
    console.print(banner, justify="center")
    
    import platform
    sys_info = f"Win32" if os.name == 'nt' else platform.system()
    info_panel = Panel(
        f"[bold magenta]CORE:[/] {DEFAULT_MODEL} | [bold magenta]ARCH:[/] Brain-Nervous-Hands | [bold magenta]SYS:[/] {sys_info}",
        border_style="magenta",
        expand=False
    )
    # Center the info panel by printing an empty layout or just using justify
    from rich.align import Align
    console.print(Align.center(info_panel))
    
    console.print(Rule("SYSTEM ONLINE", style="bold green"))
    
    while True:
        try:
            user_input = console.input("\n[bold white]User » [/]")
            if not user_input.strip(): continue
            if user_input.lower() in ["exit", "quit"]: break
            if user_input.lower() == "clear":
                os.system('cls' if os.name == 'nt' else 'clear')
                console.print(Rule("SYSTEM READY", style="bold green"))
                continue
            
            agent.think(user_input)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[bold red]System Error:[/] {e}")

if __name__ == "__main__":
    main()
