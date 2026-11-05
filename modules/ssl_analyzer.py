import socket, ssl
from datetime import datetime
from core.utils import valid_host
from core.auth import require_authorization
def run():
    host = input("TLS hostname you administer: ").strip()
    if not valid_host(host): print("Invalid host."); return
    if not require_authorization(): return
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host,443),timeout=5) as raw:
            with ctx.wrap_socket(raw,server_hostname=host) as sock:
                cert = sock.getpeercert()
                print("TLS version:", sock.version())
                print("Subject:", cert.get("subject"))
                print("Issuer:", cert.get("issuer"))
                print("Expires:", cert.get("notAfter"))
    except Exception as exc: print("TLS check failed:", exc)
