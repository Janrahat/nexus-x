#!/usr/bin/env python3
"""NEXUS X v2.0: 28 defensive utilities for Termux and Kali Linux."""
import base64, hashlib, ipaddress, json, os, platform, re, secrets, socket, ssl, string
import urllib.error, urllib.parse, urllib.request
from pathlib import Path
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

C = Console()
RED = "bright_red"
UA = "NEXUS-X/2.0 defensive diagnostics"

def banner():
    # Clear the previous screen before drawing one compact mobile header.
    C.file.write("\033[3J\033[2J\033[H")
    C.file.flush()
    logo = (
        "█   █ █████ █   █ █████ █████   █   █\n"
        "██  █ █     ██ ██ █     █   █    █ █\n"
        "█ █ █ ████  █ █ █ ████  █████     █\n"
        "█  ██ █     █   █ █     ██        █\n"
        "█   █ █████ █   █ █████ █  ██   █   █\n"
        " ▌  ▌  ▌ ▌   ▌  ▌  ▌ ▌   ▌  ▌    ▌ ▌\n"
        "  ▌    ▌     ▌       ▌     ▌       ▌"
    )
    logo_text = Text(logo, style="bold bright_red", justify="center")
    C.print(Panel(
        Align.center(
            logo_text,
            "[bold bright_cyan]POWER  /  INTELLIGENCE  /  SECURITY[/]\n"
            "[dim]NEXUS X v2.0  •  28 ETHICAL TOOLS[/]\n"
            "[dim]github.com/Janrahat/nexus-x[/]\n"
            "[bold green]● LOCAL READY[/]  [bold yellow]● AUTHORIZED USE ONLY[/]"
        ),
        border_style=RED,
        box=box.HEAVY,
        padding=(0, 1)
    ))

def show(title, rows):
    t=Table(title=f"[bold bright_red]{title}[/]",box=box.SQUARE,border_style=RED,expand=True)
    t.add_column("FIELD",style="bold bright_red",ratio=1)
    t.add_column("RESULT",style="white",ratio=2,overflow="fold")
    for k,v in rows: t.add_row(str(k),str(v))
    C.print(t)

def ask_url(label="Website URL"):
    raw=Prompt.ask(f"[bright_cyan]{label}[/]").strip()
    if "://" not in raw: raw="https://"+raw
    p=urllib.parse.urlsplit(raw)
    if p.scheme not in ("http","https") or not p.hostname: raise ValueError("Enter a valid HTTP/HTTPS URL.")
    return raw,p

def get(url, method="GET", limit=8000):
    req=urllib.request.Request(url,headers={"User-Agent":UA},method=method)
    try:
        with urllib.request.urlopen(req,timeout=7) as r: return r.status,r.headers,r.geturl(),r.read(limit)
    except urllib.error.HTTPError as e: return e.code,e.headers,e.geturl(),e.read(limit)

def permit():
    return Prompt.ask("[yellow]Do you own this system or have permission? Type YES[/]",default="NO").strip()=="YES"

def t01():
    url,p=ask_url("Your authorized website")
    if not permit(): return
    s,h,final,_=get(url,"HEAD",1000)
    show("WEBSITE SECURITY HEADERS",[("HTTP",s),("HTTPS",p.scheme=="https"),("HSTS",h.get("Strict-Transport-Security","MISSING")),("CSP",h.get("Content-Security-Policy","MISSING")),("X-Frame",h.get("X-Frame-Options","MISSING")),("X-Content-Type",h.get("X-Content-Type-Options","MISSING")),("Referrer",h.get("Referrer-Policy","MISSING")),("Final URL",final)])

def t02():
    url,p=ask_url()
    s,h,final,_=get(url,"HEAD",1000)
    show("WEBSITE INFORMATION",[("HOST",p.hostname),("SCHEME",p.scheme),("STATUS",s),("FINAL URL",final),("SERVER",h.get("Server","hidden")),("CONTENT TYPE",h.get("Content-Type","unknown")),("LENGTH",h.get("Content-Length","unknown"))])

def t03():
    raw=Prompt.ask("[cyan]URL to parse[/]").strip()
    if "://" not in raw: raw="https://"+raw
    p=urllib.parse.urlsplit(raw)
    if p.scheme not in ("http","https") or not p.hostname: raise ValueError("Invalid HTTP/HTTPS URL.")
    show("URL ANALYZER",[("SCHEME",p.scheme),("HOST",p.hostname),("PORT",p.port or "default"),("PATH",p.path or "/"),("QUERY",p.query or "none"),("FRAGMENT",p.fragment or "none"),("USER INFO","present" if p.username else "none")])

def t04():
    ip=ipaddress.ip_address(Prompt.ask("[cyan]IP address[/]").strip())
    show("IP INTELLIGENCE",[("ADDRESS",ip),("VERSION",ip.version),("PRIVATE",ip.is_private),("GLOBAL",ip.is_global),("LOOPBACK",ip.is_loopback),("MULTICAST",ip.is_multicast),("REVERSE",socket.getfqdn(str(ip)))])

def t05():
    if not permit(): return
    host=Prompt.ask("[cyan]Authorized host[/]").strip()
    ports=Prompt.ask("[cyan]TCP ports, max 20[/]",default="22,53,80,443,8080")
    socket.getaddrinfo(host,None)
    rows=[]
    for x in ports.split(",")[:20]:
        try: p=int(x.strip())
        except ValueError: continue
        if not 1<=p<=65535: continue
        try:
            with socket.create_connection((host,p),timeout=1.2): state="OPEN"
        except OSError: state="CLOSED / FILTERED"
        rows.append((p,state))
    show("LIMITED TCP CHECK",rows or [("RESULT","No valid ports")])

def t06():
    if not permit(): return
    host=Prompt.ask("[cyan]Your host / authorized device[/]").strip()
    try:
        ip=socket.gethostbyname(host)
        with socket.create_connection((ip,443),timeout=3): result="TCP 443 reachable"
    except OSError as e: ip="unresolved"; result=str(e)
    show("HOST REACHABILITY",[("HOST",host),("IP",ip),("RESULT",result)])

def t07():
    show("LOCAL DEVICE CONTEXT",[("PLATFORM",platform.platform()),("PYTHON",platform.python_version()),("MACHINE",platform.machine()),("HOST",socket.gethostname()),("HOME",os.environ.get("HOME","unknown")),("TERMUX PREFIX",os.environ.get("PREFIX","not Termux"))])

def t08():
    host=Prompt.ask("[cyan]Hostname to resolve[/]").strip()
    rows=sorted({x[4][0] for x in socket.getaddrinfo(host,None)})
    show("DNS ADDRESS LOOKUP",[("HOST",host),("ADDRESSES","\n".join(rows))])

def t09():
    if not permit(): return
    host=Prompt.ask("[cyan]Authorized TLS hostname[/]").strip()
    ctx=ssl.create_default_context()
    with socket.create_connection((host,443),timeout=5) as sock:
        with ctx.wrap_socket(sock,server_hostname=host) as s:
            cert=s.getpeercert()
            show("TLS CERTIFICATE",[("HOST",host),("TLS",s.version()),("CIPHER",s.cipher()[0]),("SUBJECT",cert.get("subject")),("ISSUER",cert.get("issuer")),("EXPIRES",cert.get("notAfter"))])

def t10():
    domain=Prompt.ask("[cyan]Public domain name[/]").strip().lower()
    if not re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}",domain): raise ValueError("Enter a domain such as example.com")
    s,h,_,body=get("https://rdap.org/domain/"+urllib.parse.quote(domain),limit=9000)
    d=json.loads(body.decode("utf-8","replace"))
    events=d.get("events",[])
    show("PUBLIC DOMAIN RDAP",[("DOMAIN",d.get("ldhName",domain)),("STATUS",", ".join(d.get("status",[]))),("EVENTS","; ".join(e.get("eventAction","")+": "+e.get("eventDate","") for e in events[:6])),("HTTP",s)])

def t11():
    host=Prompt.ask("[cyan]Hostname[/]").strip()
    rows=socket.getaddrinfo(host,None)
    unique=sorted({("IPv6" if x[0]==socket.AF_INET6 else "IPv4",x[4][0]) for x in rows})
    show("DNS RECORD RESOLUTION",unique)

def t12():
    email=Prompt.ask("[cyan]Email address (format check only)[/]").strip()
    ok=bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_{}|~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",email))
    show("EMAIL FORMAT VALIDATOR",[("INPUT",email),("FORMAT","VALID" if ok else "INVALID"),("MAILBOX CHECK","not performed")])

def t13():
    q=Prompt.ask("[cyan]Public search topic (no private personal data)[/]")
    enc=urllib.parse.quote_plus(q)
    show("MANUAL SEARCH LINKS",[("GOOGLE","https://www.google.com/search?q="+enc),("DUCKDUCKGO","https://duckduckgo.com/?q="+enc),("MODE","manual browser search only")])

def t14():
    url,p=ask_url("Your website")
    if not permit(): return
    target=urllib.parse.urlunsplit((p.scheme,p.netloc,"/robots.txt","",""))
    s,h,_,body=get(target,limit=5000)
    C.print(Panel(body.decode("utf-8","replace") or "(empty)",title=f"ROBOTS.TXT — HTTP {s}",border_style=RED))

def t15():
    url,p=ask_url("Your website")
    if not permit(): return
    target=urllib.parse.urlunsplit((p.scheme,p.netloc,"/sitemap.xml","",""))
    s,h,_,body=get(target,limit=6000)
    C.print(Panel(body.decode("utf-8","replace") or "(empty)",title=f"SITEMAP — HTTP {s}",border_style=RED))

def t16():
    url,p=ask_url()
    s,h,_,_=get(url,"HEAD",1000)
    show("HTTP RESPONSE PROFILE",[("STATUS",s),("SERVER",h.get("Server","hidden")),("TYPE",h.get("Content-Type","unknown")),("CACHE",h.get("Cache-Control","not set")),("LAST MODIFIED",h.get("Last-Modified","not set")),("VIA",h.get("Via","not set"))])

def t17():
    host=Prompt.ask("[cyan]TLS hostname[/]").strip()
    pem=ssl.get_server_certificate((host,443))
    C.print(Panel(pem[:3000],title="TLS CERTIFICATE PEM",border_style=RED))

def t18():
    raw=Prompt.ask("[cyan]Public IP address only[/]").strip()
    ip=ipaddress.ip_address(raw)
    if not ip.is_global: raise ValueError("Only public global IP addresses are accepted.")
    _,_,_,body=get("https://ipwho.is/"+str(ip),limit=5000)
    d=json.loads(body.decode("utf-8","replace"))
    if not d.get("success",True): raise ValueError(d.get("message","Lookup failed"))
    show("PUBLIC IP GEO SUMMARY",[("IP",d.get("ip")),("COUNTRY",d.get("country")),("REGION",d.get("region")),("CITY",d.get("city")),("ISP",d.get("connection",{}).get("isp")),("NOTE","Approximate IP-level data, not a person's location")])

def t19():
    url,p=ask_url("Your website")
    if not permit(): return
    target=urllib.parse.urlunsplit((p.scheme,p.netloc,"/.well-known/security.txt","",""))
    s,h,_,body=get(target,limit=5000)
    C.print(Panel(body.decode("utf-8","replace") or "(not found / empty)",title=f"SECURITY.TXT — HTTP {s}",border_style=RED))

def t20():
    pw=Prompt.ask("[yellow]Demo phrase only — never enter a real password[/]",password=True)
    rows=[("12+ characters",len(pw)>=12),("Uppercase",bool(re.search(r"[A-Z]",pw))),("Lowercase",bool(re.search(r"[a-z]",pw))),("Number",bool(re.search(r"\d",pw))),("Symbol",bool(re.search(r"[^A-Za-z0-9]",pw)))]
    show("PASSWORD STRENGTH DEMO",[(k,"PASS" if v else "NEEDS WORK") for k,v in rows])
    C.print("[dim]Local heuristic only; not a security guarantee.[/]")

def t21():
    n=int(Prompt.ask("[cyan]Length (16–64)[/]",default="20"))
    if not 16<=n<=64: raise ValueError("Length must be 16–64.")
    alphabet=string.ascii_letters+string.digits+"!@#$%^&*()-_=+"
    C.print(Panel("".join(secrets.choice(alphabet) for _ in range(n)),title="SECURE RANDOM PASSWORD",border_style=RED))
    C.print("[yellow]Save in a password manager. Never reuse it.[/]")

def t22():
    value=Prompt.ask("[cyan]Text to hash[/]")
    show("TEXT HASH GENERATOR",[("SHA-256",hashlib.sha256(value.encode()).hexdigest()),("SHA-512",hashlib.sha512(value.encode()).hexdigest())])

def t23():
    path=Path(Prompt.ask("[cyan]Local file path[/]").strip()).expanduser()
    if not path.is_file(): raise ValueError("File not found.")
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    show("LOCAL FILE SHA-256",[("FILE",path),("SIZE",path.stat().st_size),("SHA-256",h.hexdigest())])

def t24():
    mode=Prompt.ask("[cyan]encode or decode[/]",choices=["encode","decode"],default="encode")
    value=Prompt.ask("[cyan]Text / Base64 value[/]")
    result=base64.b64encode(value.encode()).decode() if mode=="encode" else base64.b64decode(value,validate=True).decode("utf-8","replace")
    C.print(Panel(result,title="BASE64 "+mode.upper(),border_style=RED))

def t25():
    mode=Prompt.ask("[cyan]encode or decode[/]",choices=["encode","decode"],default="encode")
    value=Prompt.ask("[cyan]Text / URL encoded value[/]")
    result=urllib.parse.quote(value,safe="") if mode=="encode" else urllib.parse.unquote(value)
    C.print(Panel(result,title="URL "+mode.upper(),border_style=RED))

def t26():
    raw=Prompt.ask("[cyan]Paste JSON on one line[/]")
    C.print(Panel(json.dumps(json.loads(raw),indent=2,ensure_ascii=False),title="JSON FORMATTER",border_style=RED))

def t27():
    net=ipaddress.ip_interface(Prompt.ask("[cyan]IPv4/CIDR e.g. 192.168.1.10/24[/]"))
    show("IP SUBNET CALCULATOR",[("IP",net.ip),("NETWORK",net.network.network_address),("NETMASK",net.netmask),("BROADCAST",net.network.broadcast_address),("PREFIX",net.network.prefixlen),("TOTAL ADDRESSES",net.network.num_addresses),("USABLE HOSTS (approx.)",max(0,net.network.num_addresses-2))])

def t28():
    token=Prompt.ask("[cyan]JWT token (local decode only)[/]").strip()
    parts=token.split(".")
    if len(parts)!=3: raise ValueError("JWT must have three sections.")
    def dec(x):
        x += "="*((-len(x))%4)
        return base64.urlsafe_b64decode(x).decode("utf-8","replace")
    C.print(Panel(json.dumps(json.loads(dec(parts[0])),indent=2),title="JWT HEADER",border_style=RED))
    C.print(Panel(json.dumps(json.loads(dec(parts[1])),indent=2),title="JWT PAYLOAD",border_style=RED))
    C.print("[yellow]Signature is NOT verified. Treat token contents as sensitive.[/]")

GROUPS=[
("NETWORK SCANNER",[(1,"Website Security Header Audit",t01),(2,"Website Information",t02),(3,"Website URL Analyzer",t03),(4,"IP Address Analyzer",t04),(5,"Authorized TCP Port Check",t05),(6,"Authorized Host Reachability",t06),(7,"Local Device / Network Info",t07),(8,"DNS Address Resolver",t08),(9,"TLS Certificate Inspector",t09)]),
("OSINT / INSPECTION",[(10,"Public Domain RDAP Lookup",t10),(11,"DNS Record Resolution",t11),(12,"Email Format Validator",t12),(13,"Manual Search Query Builder",t13),(14,"Robots.txt Viewer (own site)",t14),(15,"Sitemap Viewer (own site)",t15),(16,"HTTP Response Profile",t16),(17,"TLS Certificate PEM Viewer",t17),(18,"Public IP Geo Summary",t18),(19,"Security.txt Viewer (own site)",t19)]),
("UTILITIES / DEFENSE",[(20,"Password Strength Demo",t20),(21,"Secure Password Generator",t21),(22,"Text Hash Generator",t22),(23,"Local File SHA-256",t23),(24,"Base64 Encoder / Decoder",t24),(25,"URL Encoder / Decoder",t25),(26,"JSON Formatter",t26),(27,"IP Subnet Calculator",t27),(28,"JWT Local Decoder (no verify)",t28)])
]

def group_panel(title,items):
    x=Text()
    x.append("┌─ "+title+"\n",style="bold white")
    for i,(n,label,_) in enumerate(items):
        x.append("└── " if i==len(items)-1 else "├── ",style=RED)
        x.append(f"[{n:02d}] ",style="bold bright_red")
        x.append(label+"\n",style="white")
    return Panel(x,border_style=RED,box=box.SQUARE,padding=(0,1))

def menu():
    panels=[group_panel(title,items) for title,items in GROUPS]
    if C.width>=112: C.print(Columns(panels,equal=True,expand=True,padding=(0,1)))
    else:
        for p in panels: C.print(p)
    C.print(Panel(Align.center("[bold bright_red][I][/] Info     [bold bright_red][S][/] Settings     [bold bright_red][Q][/] Exit"),border_style=RED,box=box.SQUARE))
    C.print(Align.center("[dim]Choose a tool number: 01–28[/]"))

def main():
    while True:
        banner()
        C.print(f"[dim]{platform.system()} {platform.release()} | Python {platform.python_version()} | {C.width} columns[/]\n")
        menu()
        choice=Prompt.ask("[bold bright_red]NEXUS-X[/] [white]SELECT TOOL[/]",default="Q").strip().upper()
        if choice in ("Q","0","00"): break
        if choice=="I":
            show("ABOUT NEXUS X",[("VERSION","2.0"),("TOOLS","28 defensive utilities"),("PLATFORMS","Termux / Kali / Linux"),("POLICY","Authorized diagnostics; no credential attacks or exploitation")])
            C.input("ENTER to return..."); continue
        if choice=="S":
            C.print(Panel("Responsive layout is automatic. Network requests use conservative timeouts.",title="SETTINGS",border_style=RED))
            C.input("ENTER to return..."); continue
        try: number=int(choice)
        except ValueError:
            C.print("[yellow]Enter 01–28, I, S, or Q.[/]"); C.input("ENTER to continue..."); continue
        selected=next(((name,fn) for _,items in GROUPS for n,name,fn in items if n==number),None)
        if not selected:
            C.print("[yellow]Choose a number from 01 to 28.[/]"); C.input("ENTER to continue..."); continue
        name,fn=selected
        C.clear()
        C.print(Panel(f"[bold bright_red]NEXUS X[/] [white]// {number:02d} {name.upper()}[/]",border_style=RED,box=box.HEAVY))
        try: fn()
        except KeyboardInterrupt: C.print("\n[yellow]Cancelled.[/]")
        except Exception as e: C.print(f"[bold red]TOOL ERROR[/] [white]{type(e).__name__}: {e}[/]")
        C.input("\n[dim]ENTER = BACK TO MENU[/]")
    C.print(Panel(Align.center("[bold bright_red]NEXUS X OFFLINE[/]\n[dim]Authorized use only.[/]"),border_style=RED,box=box.HEAVY))

if __name__=="__main__": main()
