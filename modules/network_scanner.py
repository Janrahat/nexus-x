"""Conservative single-host connectivity check; no subnet sweeping."""
import socket
from core.utils import valid_host
def run():
    host = input("Host: ").strip()
    if not valid_host(host): print("Invalid host."); return
    try:
        print("Reachable TCP service on port 443:", end=" ")
        with socket.create_connection((host, 443), timeout=3): print("yes")
    except OSError: print("not confirmed")
