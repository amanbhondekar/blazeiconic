"""Copy brand assets from 'Web Assets' into src/assets.

Re-run after the brand files change:  python tools/setup_assets.py

Logo artwork is supplied, never retyped, so the only change made here is the
fill colour (Ink on Paper, Paper on Ink, Red on Paper), as the brand kit allows.
"""
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "Web Assets"
OUT = ROOT / "src" / "assets"

INK, PAPER, RED = "#17130F", "#F5F0E6", "#B21F2D"

# Fonts -----------------------------------------------------------------
fonts_out = OUT / "fonts"
fonts_out.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(WEB / "Fonts" / "Stardom_Complete.zip") as z:
    for member in z.namelist():
        name = Path(member).name
        if name in ("Stardom-Regular.woff2", "Stardom-Regular.woff"):
            (fonts_out / name).write_bytes(z.read(member))
        elif name == "FFL.txt":
            (fonts_out / "Stardom-FFL-license.txt").write_bytes(z.read(member))

# Ronzino (body): Regular 400, Medium 500, Bold 700 as woff2, plus its licence
ronzino_zip = WEB / "Fonts" / "ronzino-main.zip"
if ronzino_zip.exists():
    wanted = {"Ronzino-Regular.woff2", "Ronzino-Medium.woff2", "Ronzino-Bold.woff2"}
    with zipfile.ZipFile(ronzino_zip) as z:
        for member in z.namelist():
            name = Path(member).name
            if name in wanted and "/fonts/" in member:
                (fonts_out / name).write_bytes(z.read(member))
            elif name == "LICENSE.txt" and member.count("/") == 1:
                (fonts_out / "Ronzino-license.txt").write_bytes(z.read(member))

# Logos -----------------------------------------------------------------
logo_out = OUT / "logo"
logo_out.mkdir(parents=True, exist_ok=True)
src_dir = WEB / "Logo Files" / "SVG"
variants = {
    "Wordmark-Landscape.svg": ("wordmark-landscape", {"ink": INK, "paper": PAPER, "red": RED}),
    "Wordmark-Portrait.svg": ("wordmark-portrait", {"ink": INK, "paper": PAPER}),
    "Logomark-Avatarmark.svg": ("mark", {"ink": INK, "paper": PAPER, "red": RED}),
}
for filename, (slug, colours) in variants.items():
    svg = (src_dir / filename).read_text(encoding="utf-8")
    for tone, hex_ in colours.items():
        out = re.sub(r'fill="black"', f'fill="{hex_}"', svg)
        (logo_out / f"{slug}-{tone}.svg").write_text(out, encoding="utf-8")

# Favicon: Bi mark on a Red tile, mark at 50% of the width (brand kit p.5)
mark = (src_dir / "Logomark-Avatarmark.svg").read_text(encoding="utf-8")
paths = "".join(re.findall(r"<path[^>]*/>", mark)).replace('fill="black"', f'fill="{PAPER}"')
scale = 32 / 82  # mark is 82 wide; tile is 64
tx, ty = 16, (64 - 63 * scale) / 2
favicon = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
    f'<rect width="64" height="64" fill="{RED}"/>'
    f'<g transform="translate({tx} {ty:.2f}) scale({scale:.4f})">{paths}</g></svg>'
)
(OUT / "favicon.svg").write_text(favicon, encoding="utf-8")

print("assets ready in", OUT)
