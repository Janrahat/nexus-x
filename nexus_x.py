#!/usr/bin/env python3
"""NEXUS X: defensive diagnostics for systems you own or are authorized to test."""
import hashlib, ipaddress, platform, socket, ssl, urllib.request, urllib.error, re
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt

console = Console()
RED = "bright_red"

def banner():
    console.print(Panel("[bold bright_red]N E X U S   X[/]\n[white]POWER. INTELLIGENCE. SECURITY.[/]", border_style=RED))
    console.print("[dim]Authorized defensive diagnostics only[/]\n")

def table(title, rows):
    t = Table(title=title, border_style=RED)
    t.add_column("FIELD", style="bright_red")
    t.add_column("RESULT", overflow="fold")
    for k, v in rows: t.add_row(str(k), str(v))
    console.print(t)

def authorized():
    return Prompt.ask("[yellow]Do you own this target or have written permission? Type YES[/]").strip() == "YES"

def system_info():
    table("SYSTEM INTELLIGENCE", [("OS", platform.platform()), ("Python", platform.python_version()), ("Machine", platform.machine()), ("Hostname", socket.gethostname())])

def ip_dns():
    host = Prompt.ask("IP address or hostname").strip()
    try:
        ip = ipaddress.ip_address(host)
        rows = [("Address", ip), ("Version", ip.version), ("Private", ip.is_private), ("Global", ip.is_global), ("Loopback", ip.is_loopback), ("Reserved", ip.is_reserved)]
    except ValueError:
        rows = [("Hostname", host), ("Resolved addresses", ", ".join(sorted({x[4][0] for x in socket.getaddrinfo(host, None)})))]
    table("IP / DNS INTELLIGENCE", rows)

def port_check():
    if not authorized():
        console.print("[yellow]Cancelled: authorization not confirmed.[/]"); return
    host = Prompt.ask("Authorized host").strip()
    try: socket.getaddrinfo(host, None)
    except OSError as e: console.print(f"[red]DNS error: {e}[/]"); return
    ports = Prompt.ask("Comma-separated TCP ports", default="22,80,443,8080")
    found=[]
    for raw in ports.split(",")[:32]:
        try: port=int(raw.strip())
        except ValueError: continue
        if not 1 <= port <= 65535: continue
        try:
            with socket.create_connection((host, port), timeout=1.5): found.append((port, "open"))
        except OSError: found.append((port, "closed / filtered"))
    table("LIMITED TCP PORT CHECK", found)

def website_headers():
    if not authorized():
        console.print("[yellow]Cancelled: authorization not confirmed.[/]"); return
    value=Prompt.ask("Authorized website URL").strip()
    if "://" not in value: value="https://"+value
    p=urlparse(value)
    if p.scheme not in ("http","https") or not p.hostname: raise ValueError("Only valid HTTP/HTTPS URLs are accepted.")
    req=urllib.request.Request(value, headers={"User-Agent":"NEXUS-X/1.0"}, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=5) as r: status, headers, final=r.status, r.headers, r.url
    except urllib.error.HTTPError as e: status, headers, final=e.code, e.headers, e.url
    table("WEBSITE SECURITY HEADERS", [("HTTP status",status),("Final URL",final),("HTTPS",p.scheme=="https"),("HSTS",headers.get("Strict-Transport-Security","missing")),("CSP",headers.get("Content-Security-Policy","missing")),("X-Content-Type-Options",headers.get("X-Content-Type-Options","missing")),("X-Frame-Options",headers.get("X-Frame-Options","missing")),("Referrer-Policy",headers.get("Referrer-Policy","missing"))])

def tls_check():
    if not authorized():
        console.print("[yellow]Cancelled: authorization not confirmed.[/]"); return
    host=Prompt.ask("Authorized TLS hostname").strip()
    ctx=ssl.create_default_context()
    with socket.create_connection((host,443),timeout=5) as sock:
        with ctx.wrap_socket(sock,server_hostname=host) as ss:
            cert=ss.getpeercert()
            table("TLS CERTIFICATE", [("TLS version",ss.version()),("Cipher",ss.cipher()),("Subject",cert.get("subject")),("Issuer",cert.get("issuer")),("Expires",cert.get("notAfter"))])

def url_info():
    value=Prompt.ask("URL").strip()
    if "://" not in value: value="https://"+value
    p=urlparse(value)
    if p.scheme not in ("http","https") or not p.hostname: raise ValueError("Invalid HTTP/HTTPS URL.")
    table("URL ANALYSIS", [("Scheme",p.scheme),("Host",p.hostname),("Port",p.port or "default"),("Path",p.path or "/"),("Query",p.query),("Fragment",p.fragment)])

def hash_file():
    path=Prompt.ask("Local file path").strip()
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    table("FILE HASH", [("File",path),("SHA-256",h.hexdigest())])

def password_audit():
    pw=Prompt.ask("Test string only (do NOT enter a real password)", password=True)
    checks=[("12+ characters",len(pw)>=12),("Uppercase",bool(re.search(r"[A-Z]",pw))),("Lowercase",bool(re.search(r"[a-z]",pw))),("Number",bool(re.search(r"\\d",pw))),("Symbol",bool(re.search(r"[^A-Za-z0-9]",pw)))]
    table("PASSWORD HEURISTIC", [(k,"PASS" if v else "FAIL") for k,v in checks])
    console.print("[dim]Local heuristic only; not a breach check or security guarantee.[/]")

ACTIONS=[("System intelligence",system_info),("IP / DNS intelligence",ip_dns),("Limited TCP port check",port_check),("Website security headers",website_headers),("SSL/TLS certificate",tls_check),("URL analyzer",url_info),("Local file SHA-256",hash_file),("Password strength demo",password_audit)]
def main():
    banner()
    while True:
        for i,(name,_) in enumerate(ACTIONS,1): console.print(f"[bright_red]{i:02d}[/]  {name}")
        console.print("[bright_red]00[/]  Exit")
        try: choice=IntPrompt.ask("\n[bold bright_red]NEXUS X[/] Select",default=0)
        except (KeyboardInterrupt,EOFError): break
        if choice==0: break
        if 1<=choice<=len(ACTIONS):
            try: ACTIONS[choice-1][1]()
            except Exception as e: console.print(f"[red]Error: {e}[/]")
        else: console.print("[yellow]Choose a listed option.[/]")
    console.print("[bright_red]NEXUS X offline. Stay authorized.[/]")
if __name__=="__main__": main()
