#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
pkg update -y
pkg install -y python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo 'Run: python nexus_x.py'
