"""Minimal text report writer."""
from pathlib import Path
from datetime import datetime, timezone
def save_report(title, lines):
    folder = Path("reports"); folder.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    path = folder / f"{stamp}.txt"
    path.write_text(title + "\\n" + "\\n".join(map(str, lines)) + "\\n", encoding="utf-8")
    return path
