#!/usr/bin/env python3
import os
import time
import psutil
import requests
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text

console = Console()

SERVICES = {
    "Ollama": {"port": 11434, "url": "http://localhost:11434/api/tags"},
    "OpenClaw": {"port": 18789, "url": "http://localhost:18789/health"},
    "LM Studio": {"port": 1234, "url": "http://localhost:1234/v1/models"},
}

PROCESSES = {
    "Aether (Agent)": "aether_agent.py",
    "Aether (Tauri)": "aether-tauri",
    "OpenClaude": "openclaude",
}

def check_service(name, config):
    try:
        r = requests.get(config["url"], timeout=0.5)
        if r.status_code == 200:
            return "[bold green]ONLINE[/]", f"{config['port']}"
    except:
        pass
    return "[bold red]OFFLINE[/]", "-"

def check_process(name, pattern):
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if pattern in str(proc.info['cmdline']) or pattern == proc.info['name']:
                cpu = proc.cpu_percent(interval=None)
                mem = proc.memory_info().rss / (1024 * 1024)
                return "[bold green]ACTIVE[/]", f"{cpu:.1f}% CPU | {mem:.0f}MB"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return "[bold red]INACTIVE[/]", "-"

def generate_monitor():
    table = Table(box=None, expand=True)
    table.add_column("Neural Service", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Metrics/Port", justify="right", style="dim")

    table.add_section()
    # Check Network Services
    for name, config in SERVICES.items():
        status, detail = check_service(name, config)
        table.add_row(name, status, detail)

    table.add_section()
    # Check System Processes
    for name, pattern in PROCESSES.items():
        status, detail = check_process(name, pattern)
        table.add_row(name, status, detail)

    # Hardware Vitals
    hw_grid = Table.grid(expand=True)
    hw_grid.add_column()
    hw_grid.add_column(justify="right")
    hw_grid.add_row(f"System CPU: {psutil.cpu_percent()}%", f"RAM: {psutil.virtual_memory().percent}%")

    layout = Layout()
    layout.split(
        Layout(Panel(table, title="[bold magenta]🌌 AETHER NEURAL MONITOR[/]", border_style="magenta")),
        Layout(Panel(hw_grid, border_style="dim"), size=3)
    )
    return layout

def main():
    with Live(generate_monitor(), refresh_per_second=2) as live:
        try:
            while True:
                time.sleep(0.5)
                live.update(generate_monitor())
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
