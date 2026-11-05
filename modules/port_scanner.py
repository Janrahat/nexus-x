import socket
from core.utils import valid_host
from core.auth import require_authorization
def run():
    host = input("Target host you own: ").strip()
    if not valid_host(host): print("Invalid host."); return
    if not require_authorization(): return
    raw = input("Ports (comma-separated, max 32; e.g. 22,80,443): ")
    try: ports = list(dict.fromkeys(int(x.strip()) for x in raw.split(",")))
    except ValueError: print("Invalid port list."); return
    if not ports or len(ports) > 32 or any(p < 1 or p > 65535 for p in ports): print("Use 1-32 valid ports."); return
    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=1): print(f"{port}: open")
        except OSError: print(f"{port}: closed or filtered")
