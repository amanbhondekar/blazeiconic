"""Check that every internal href/src in public/ points at a file that exists.

    python tools/check_links.py
"""
import re
from pathlib import Path

pub = Path(__file__).resolve().parent.parent / "public"
bad, checked = [], 0
for page in pub.rglob("*.html"):
    for m in re.finditer(r'(?:href|src)="([^"#?]+)', page.read_text(encoding="utf-8")):
        url = m.group(1)
        if url.startswith(("http", "mailto:")):
            continue
        checked += 1
        target = pub / url.lstrip("/")
        if url.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            bad.append((str(page.relative_to(pub)), url))
print(f"checked {checked} internal refs; broken: {bad or 'none'}")
