import socket
from core.utils import valid_host
def run():
    host = input("IP address or hostname: ").strip()
    if not valid_host(host): print("Invalid host."); return
    try:
        print("Resolved addresses:")
        for item in sorted({x[4][0] for x in socket.getaddrinfo(host, None)}): print(" -", item)
    except OSError as exc: print("Lookup failed:", exc)
