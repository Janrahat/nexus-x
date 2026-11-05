#!/usr/bin/env python3
"""NEXUS X: mobile-friendly defensive diagnostics for authorized systems."""
import hashlib
import ipaddress
import platform
import re
import socket
import ssl
import urllib.error
import urllib.request
from urllib.parse import urlparse

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich.text import Text

console = Console()
RED = "bright_red"
CYAN = "bright_cyan"
MUTED = "grey70"

ACTIONS = []


def banner():
    console.clear()
    width = max(36, min(console.width, 72))
    title = Text("N E X U S   X", style="bold bright_red", justify="center")
    drips = Text(" ░ ▒ ▓  ░ ▒ ▓  ░ ▒ ▓ ", style="bold red", justify="center")
    subtitle = Text("POWER  /  INTELLIGENCE  /  SECURITY", style="bold bright_cyan", justify="center")
    art = Text()
    art.append(title)
    art.append("\n")
    art.append(drips)
    art.append("\n")
    art.append(subtitle)
    console.print(Panel(
        Align.center(art),
        border_style="bright_red",
        box=box.HEAVY,
        padding=(1, 1),
        width=width,
    ))
    console.print(Align.center("[bold green]● ONLINE[/]  [dim]LOCAL MODE[/]  [bold yellow]● AUTHORIZED USE ONLY[/]"))
    console.print()

def system_snapshot():
    return [
        ("PLATFORM", platform.system() + " " + platform.release()),
        ("PYTHON", platform.python_version()),
        ("DEVICE", platform.machine()),
        ("HOST", socket.gethostname()[:24]),
    ]


def show_table(title, rows):
    table = Table(
        title=f"[bold bright_cyan]{title}[/]",
        box=box.ROUNDED,
        border_style=CYAN,
        header_style="bold bright_red",
        expand=True,
    )
    table.add_column("FIELD", style="bold bright_red", ratio=1)
    table.add_column("RESULT", style="white", ratio=2, overflow="fold")
    for key, value in rows:
        table.add_row(str(key), str(value))
    console.print(table)


def authorized():
    answer = Prompt.ask(
        "[bold yellow]Confirm you own this target or have permission. Type YES[/]",
        default="NO",
    ).strip()
    return answer == "YES"


def system_info():
    show_table("SYSTEM INTELLIGENCE", system_snapshot())


def ip_dns():
    host = Prompt.ask("[bright_cyan]IP address or hostname[/]").strip()
    try:
        ip = ipaddress.ip_address(host)
        rows = [
            ("ADDRESS", ip), ("VERSION", ip.version),
            ("PRIVATE", ip.is_private), ("GLOBAL", ip.is_global),
            ("LOOPBACK", ip.is_loopback), ("RESERVED", ip.is_reserved),
        ]
    except ValueError:
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(host, None)})
        rows = [("HOSTNAME", host), ("RESOLVED", ", ".join(addresses))]
    show_table("IP / DNS INTELLIGENCE", rows)


def port_check():
    if not authorized():
        console.print("[yellow]Cancelled: authorization not confirmed.[/]")
        return
    host = Prompt.ask("[bright_cyan]Authorized host[/]").strip()
    try:
        socket.getaddrinfo(host, None)
    except OSError as exc:
        console.print(f"[red]DNS error: {exc}[/]")
        return
    raw_ports = Prompt.ask("[bright_cyan]TCP ports (max 32)[/]", default="22,80,443,8080")
    results = []
    for raw in raw_ports.split(",")[:32]:
        try:
            port = int(raw.strip())
        except ValueError:
            continue
        if not 1 <= port <= 65535:
            continue
        try:
            with socket.create_connection((host, port), timeout=1.5):
                state = "[green]OPEN[/]"
        except OSError:
            state = "[dim]CLOSED / FILTERED[/]"
        results.append((port, state))
    show_table("LIMITED TCP PORT CHECK", results or [("RESULT", "No valid ports supplied")])


def website_headers():
    if not authorized():
        console.print("[yellow]Cancelled: authorization not confirmed.[/]")
        return
    value = Prompt.ask("[bright_cyan]Authorized website URL[/]").strip()
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Only valid HTTP/HTTPS URLs are accepted.")
    request = urllib.request.Request(value, headers={"User-Agent": "NEXUS-X/2.0"}, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            status, headers, final_url = response.status, response.headers, response.url
    except urllib.error.HTTPError as exc:
        status, headers, final_url = exc.code, exc.headers, exc.url
    show_table("WEBSITE SECURITY HEADERS", [
        ("HTTP STATUS", status), ("FINAL URL", final_url),
        ("HTTPS", parsed.scheme == "https"),
        ("HSTS", headers.get("Strict-Transport-Security", "missing")),
        ("CSP", headers.get("Content-Security-Policy", "missing")),
        ("X-CONTENT-TYPE", headers.get("X-Content-Type-Options", "missing")),
        ("X-FRAME", headers.get("X-Frame-Options", "missing")),
        ("REFERRER", headers.get("Referrer-Policy", "missing")),
    ])


def tls_check():
    if not authorized():
        console.print("[yellow]Cancelled: authorization not confirmed.[/]")
        return
    host = Prompt.ask("[bright_cyan]Authorized TLS hostname[/]").strip()
    context = ssl.create_default_context()
    with socket.create_connection((host, 443), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=host) as secure:
            cert = secure.getpeercert()
            show_table("TLS CERTIFICATE", [
                ("TLS VERSION", secure.version()), ("CIPHER", secure.cipher()),
                ("SUBJECT", cert.get("subject")), ("ISSUER", cert.get("issuer")),
                ("EXPIRES", cert.get("notAfter")),
            ])


def url_info():
    value = Prompt.ask("[bright_cyan]URL to inspect[/]").strip()
    if "://" not in value:
        value = "https://" + value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Invalid HTTP/HTTPS URL.")
    show_table("URL ANALYSIS", [
        ("SCHEME", parsed.scheme), ("HOST", parsed.hostname),
        ("PORT", parsed.port or "default"), ("PATH", parsed.path or "/"),
        ("QUERY", parsed.query or "none"), ("FRAGMENT", parsed.fragment or "none"),
    ])


def hash_file():
    path = Prompt.ask("[bright_cyan]Local file path[/]").strip()
    digest = hashlib.sha256()
    with open(path, "rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    show_table("LOCAL FILE SHA-256", [("FILE", path), ("SHA-256", digest.hexdigest())])


def password_audit():
    password = Prompt.ask(
        "[yellow]Demo string only — never enter a real password[/]",
        password=True,
    )
    checks = [
        ("12+ CHARACTERS", len(password) >= 12),
        ("UPPERCASE", bool(re.search(r"[A-Z]", password))),
        ("LOWERCASE", bool(re.search(r"[a-z]", password))),
        ("NUMBER", bool(re.search(r"\d", password))),
        ("SYMBOL", bool(re.search(r"[^A-Za-z0-9]", password))),
    ]
    show_table("PASSWORD STRENGTH DEMO", [
        (label, "[green]PASS[/]" if passed else "[red]NEEDS WORK[/]")
        for label, passed in checks
    ])
    console.print("[dim]Local heuristic only — not a breach check or security guarantee.[/]")


ACTIONS = [
    ("System intelligence", "Device and OS details", system_info),
    ("IP / DNS intelligence", "Address and hostname lookup", ip_dns),
    ("Limited TCP port check", "Small authorized port check", port_check),
    ("Website security headers", "Review HTTP response headers", website_headers),
    ("SSL / TLS certificate", "Inspect certificate details", tls_check),
    ("URL analyzer", "Break down a web address", url_info),
    ("Local file SHA-256", "Calculate a local file hash", hash_file),
    ("Password strength demo", "Test a sample phrase only", password_audit),
]


def show_menu():
    groups = [
        ("NETWORK SCANNER", [
            (2, "IP / DNS Intelligence"),
            (3, "Limited TCP Port Check"),
            (4, "Website Security Headers"),
            (5, "SSL / TLS Certificate"),
        ]),
        ("OSINT / INSPECTION", [
            (6, "URL Analyzer"),
        ]),
        ("UTILITIES", [
            (1, "System Intelligence"),
            (7, "Local File SHA-256"),
            (8, "Password Strength Demo"),
        ]),
    ]
    for heading, items in groups:
        console.print(f"[bold bright_red]       ┌── [bold white]{heading}[/]")
        for position, (number, label) in enumerate(items):
            branch = "└──" if position == len(items) - 1 else "├──"
            console.print(
                f"[red]       {branch}[/] [bold bright_red][{number:02d}][/] "
                f"[bold white]{label}[/]"
            )
        console.print()
    console.print("[bold red]       └── [00] EXIT[/]")
    console.print(Align.center("[dim]Enter a module number  •  Ctrl+C to quit[/]"))

def main():
    while True:
        banner()
        console.print(
            f"[bold bright_cyan]DEVICE[/] [white]{platform.system()} {platform.release()}[/]  "
            f"[bold bright_cyan]PY[/] [white]{platform.python_version()}[/]"
        )
        console.print("[bold green]● READY[/]  [dim]LOCAL TERMINAL[/]  [bold yellow]● PERMISSION REQUIRED FOR REMOTE TESTS[/]\n")
        show_menu()
        try:
            choice = IntPrompt.ask("[bold bright_red]NEXUS X[/] [white]SELECT[/]", default=0)
        except (KeyboardInterrupt, EOFError):
            break
        if choice == 0:
            break
        if 1 <= choice <= len(ACTIONS):
            console.clear()
            console.print(Panel(
                f"[bold bright_red]NEXUS X[/]  [bold white]// {ACTIONS[choice - 1][0].upper()}[/]",
                border_style=RED,
                box=box.DOUBLE,
            ))
            try:
                ACTIONS[choice - 1][2]()
            except Exception as exc:
                console.print(f"[bold red]MODULE ERROR[/] [white]{exc}[/]")
            console.input("\n[dim]ENTER = BACK TO MAIN MENU[/]")
        else:
            console.print("[yellow]Invalid module ID.[/]")
            console.input("[dim]Press Enter to continue...[/]")
    console.print(Panel(
        Align.center("[bold bright_red]NEXUS X OFFLINE[/]\n[dim]Stay safe. Test only with permission.[/]"),
        border_style=RED,
        box=box.DOUBLE,
    ))

if __name__ == "__main__":
    main()
