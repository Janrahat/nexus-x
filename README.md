# NEXUS X — ULTIMATE CYBER FRAMEWORK

**POWER. INTELLIGENCE. SECURITY.**

A modular Python cybersecurity toolkit for Kali Linux, Termux, Debian, and Ubuntu. Designed for authorized security testing, network diagnostics, and defensive research only.

## Features
- System and device information
- IP address and DNS intelligence
- TCP port checks for explicitly authorized targets
- Website HTTP security-header inspection
- SSL/TLS certificate inspection
- Common-subdomain DNS checks
- URL parsing and local file SHA-256 metadata
- Password-strength heuristics (never enter a real password)
- JSON report generation

## Requirements
- Python 3.10+
- Install dependencies: `python -m pip install -r requirements.txt`

## Install

### Kali / Debian / Ubuntu
```bash
chmod +x install_kali.sh
./install_kali.sh
```

### Termux
```bash
chmod +x install_termux.sh
./install_termux.sh
```

Then run:
```bash
python main.py
```

## Authorization and safety
Only test systems you own or have explicit written permission to assess. Remote modules ask for authorization before running. Use conservative timeouts and avoid disruptive scanning. This project is not an exploitation framework.

## Project status
Initial source upload. Some checks are intentionally lightweight and platform-dependent; see module notes and test results before relying on findings.
