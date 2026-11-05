"""Terminal UI helpers."""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
console = Console()
def banner():
    console.clear()
    console.print(Panel(Text("N E X U S   X\\nAuthorized Security Toolkit", justify="center", style="bold bright_cyan"), border_style="bright_blue"))
def choose(label="Choice"):
    return console.input(f"[bold cyan]{label} > [/]").strip()
def info(message): console.print(f"[cyan][*][/cyan] {message}")
def good(message): console.print(f"[green][+][/green] {message}")
def warn(message): console.print(f"[yellow][!][/yellow] {message}")
def error(message): console.print(f"[red][-][/red] {message}")
