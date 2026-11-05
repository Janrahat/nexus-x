import hashlib
from pathlib import Path
def run():
    p=Path(input('Local file path: ').strip()).expanduser()
    if not p.is_file(): print('File not found.'); return
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    print('SHA-256:',h.hexdigest())
