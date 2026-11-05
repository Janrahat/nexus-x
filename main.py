#!/usr/bin/env python3
"""Modular NEXUS X terminal launcher."""
from core.ui import banner, choose
from core.utils import pause
from modules import system_intelligence, ip_analyzer, dns_intelligence, port_scanner, website_checker, ssl_analyzer, url_analyzer, hashes, password_auditor, device_info, metadata_analyzer, wifi_info
MENU = [
    ("System intelligence", system_intelligence.run),
    ("IP intelligence", ip_analyzer.run),
    ("DNS lookup", dns_intelligence.run),
    ("Authorized TCP port check", port_scanner.run),
    ("Website security headers", website_checker.run),
    ("TLS certificate check", ssl_analyzer.run),
    ("URL analysis", url_analyzer.run),
    ("File SHA-256", hashes.run),
    ("Password strength audit", password_auditor.run),
    ("Device information", device_info.run),
    ("File metadata", metadata_analyzer.run),
    ("Wi-Fi connection details", wifi_info.run),
]
def main():
    while True:
        banner()
        for i, (name, _) in enumerate(MENU, 1): print(f"  [cyan]{i:02}[/cyan]  {name}")
        print("  [red]00[/red]  Exit")
        choice = choose("Select module")
        if choice in ("0", "00", "q", "quit"): break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            try: MENU[int(choice)-1][1]()
            except KeyboardInterrupt: print("\\n[!] Cancelled.")
            except Exception as exc: print(f"[!] Module error: {exc}")
            pause()
        else: print("[!] Invalid choice.")
if __name__ == "__main__": main()
