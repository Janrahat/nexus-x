# NEXUS X v2.0 — Defensive Security Toolkit

**POWER / INTELLIGENCE / SECURITY**

NEXUS X is a Python terminal toolkit for Termux, Kali Linux, Debian, Ubuntu, and other Python 3 systems. It contains 28 defensive diagnostics and local utilities. It is designed for systems you own or are explicitly authorized to assess.

## 28 tools

### Network scanner
1. Website security-header audit
2. Website information
3. Website URL analyzer
4. IP address analyzer
5. Authorized TCP port check (small user-selected port list)
6. Authorized host reachability
7. Local device / network information
8. DNS address resolver
9. TLS certificate inspector

### OSINT / inspection
10. Public domain RDAP lookup
11. DNS record resolution
12. Email format validator (syntax only; does not verify mailbox existence)
13. Manual public search-query builder
14. robots.txt viewer (own/authorized website)
15. sitemap viewer (own/authorized website)
16. HTTP response profile
17. TLS certificate PEM viewer
18. Public IP geolocation summary (approximate IP-level data)
19. security.txt viewer (own/authorized website)

### Utilities / defense
20. Password-strength demo (use sample phrases only; never enter a real password)
21. Secure random password generator
22. Text hash generator (SHA-256 / SHA-512)
23. Local file SHA-256
24. Base64 encoder / decoder
25. URL encoder / decoder
26. JSON formatter
27. IP subnet calculator
28. JWT local decoder (does not verify signatures)

## Installation

### Termux
```bash
pkg update && pkg upgrade -y
pkg install git python -y
git clone https://github.com/Janrahat/nexus-x.git
cd nexus-x
python -m pip install -r requirements.txt
python nexus_x.py
```

### Kali Linux
```bash
sudo apt update
sudo apt install -y git python3 python3-venv
git clone https://github.com/Janrahat/nexus-x.git
cd nexus-x
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python nexus_x.py
```

## Tests
Run the built-in test suite:
```bash
python -m unittest discover -s tests -v
```

## Important limitations and safe use
- Only run remote checks against systems you own or have explicit permission to assess.
- Port checking is intentionally limited and is not a full network scanner.
- Email validation checks syntax only; mailbox existence is not tested.
- IP geolocation is approximate and must not be used to identify a person's precise location.
- A JWT decode only displays its header and payload; it does not validate the signature or trust the token.
- Password strength output is a local heuristic, not a guarantee.
- Results depend on network access, DNS, remote server behavior, and the Python environment. Review findings manually.

## Project status
NEXUS X v2.0 is an evolving defensive toolkit. A menu entry is not proof of a fully validated feature: test each tool in your own environment before relying on it. Contributions and bug reports are welcome.
