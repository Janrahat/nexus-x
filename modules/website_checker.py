import urllib.request
from core.utils import valid_host
from core.auth import require_authorization
HEADERS = ["Strict-Transport-Security","Content-Security-Policy","X-Content-Type-Options","X-Frame-Options","Referrer-Policy","Permissions-Policy"]
def run():
    host = input("Website hostname you administer: ").strip()
    if not valid_host(host): print("Invalid host."); return
    if not require_authorization(): return
    req = urllib.request.Request("https://" + host, headers={"User-Agent":"NEXUS-X/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            print("HTTP status:", res.status)
            for key in HEADERS: print(f"{key}: {res.headers.get(key, 'MISSING')}")
    except Exception as exc: print("Request failed:", exc)
