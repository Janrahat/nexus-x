import socket
from core.utils import valid_host
def run():
    host = input("Domain or IP: ").strip()
    if not valid_host(host): print("Invalid host."); return
    try:
        print("Canonical name:", socket.getfqdn(host))
        for row in socket.getaddrinfo(host, None): print(row[4][0])
    except OSError as exc: print("DNS lookup failed:", exc)
