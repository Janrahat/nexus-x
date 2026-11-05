from urllib.parse import urlparse
def run():
    raw=input("URL: ").strip(); p=urlparse(raw)
    if p.scheme not in ("http","https") or not p.hostname:
        print("Enter a valid http(s) URL."); return
    print("Scheme:",p.scheme,"Host:",p.hostname,"Port:",p.port or "default")
    print("Embedded credentials:",bool(p.username or p.password))
    print("Fragment present:",bool(p.fragment))
