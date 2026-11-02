"""Static site builder for Blaze Iconic.

    python tools/setup_assets.py   # once, or when brand files change
    python build.py                # src/ -> public/

Pages live in src/pages/. Each starts with `key: value` lines, then `---`,
then the page body. Keys:

    title, description   <title> and meta description
    path                 URL, e.g. /packages/   (404 -> /404.html)
    job, action, needs   shown in the build-notes strip; delete with the strip
    legal: yes           adds the colophon to the footer (legal pages only)
    css, js              extra stylesheet / script for one page (Home uses /home.js)
    h1, eyebrow, lede, cta
                         builds the page hero (cta is "Label | /href")
    {{> name}} in a body includes src/partials/name.html

Header, footer and layout are defined here and in src/layout.html, so the
navigation is edited in one place.
"""
import html
import re
import shutil
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "public"

SITE = "Blaze Iconic"

# Page-hero images (src/assets/img); each page picks one by its URL. Swap files for real photography.
HERO_IMAGES = ["hero-b", "hero-c", "hero-d"]

# Header: five items and one button (IA, Navigation and footer)
NAV = [
    ("Packages", "/packages/"),
    ("How it works", "/how-it-works/"),
    ("Work", "/work/"),
    ("Standards", "/standards/"),
    ("About", "/about/"),
]

# Bracketed values are placeholders until Blaze confirms them (IA: "Needs from Blaze")
ENTITY = "[LEGAL ENTITY]"
ADDRESS = "[US ADDRESS]"
EMAIL = "[EMAIL ADDRESS]"


def parse_page(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    head, _, body = raw.partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    meta["body"] = body.strip()
    return meta


def header_html(current: str) -> str:
    links = []
    for label, href in NAV:
        active = ' aria-current="page"' if current.startswith(href) else ""
        links.append(f'<a href="{href}"{active}>{label}</a>')
    links.append('<a class="btn btn--sm" href="/book/">Book a call</a>')
    return f"""<header class="site-header">
  <div class="hd-inner">
    <a class="hd-word" href="/" aria-label="Blaze Iconic, home"><img src="/assets/logo/wordmark-landscape-ink.svg" alt="Blaze Iconic" width="162" height="20"></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span><span></span></button>
    <nav class="nav" id="site-nav" aria-label="Primary">
      {chr(10).join('      ' + l for l in links).strip()}
    </nav>
  </div>
</header>"""


def footer_html(legal: bool) -> str:
    colophon = (
        f'<span>Published by {ENTITY}. Part of Blaze Iconic.</span>' if legal else f"<span>&copy; [YEAR] {ENTITY}</span>"
    )
    return f"""<footer class="site-footer">
  <div class="ft-main">
    <div class="ft-lead">
      <h2 class="ft-title">Start with a call.</h2>
      <div class="ft-actions">
        <a class="hx-btn hx-btn--red" href="/book/">Book a call <span class="arrow">&rarr;</span></a>
        <a class="hx-btn hx-btn--line" href="/contact/">Contact us <span class="arrow">@</span></a>
      </div>
    </div>
    <nav class="ft-cols" aria-label="Footer">
      <div class="ft-col">
        <h2>Company</h2>
        <a href="/about/">About</a><a href="/faq/">FAQ</a><a href="/contact/">Contact</a><a href="/book/">Book a call</a>
      </div>
      <div class="ft-col">
        <h2>Our titles</h2>
        <a href="https://blazemagazines.com" rel="noopener">Blaze Mags <span aria-hidden="true">&nearr;</span></a>
        <!-- The Black Mags and Mirror Mags: add once their landing pages are live -->
      </div>
      <div class="ft-col">
        <h2>Legal</h2>
        <a href="/terms/">Terms</a><a href="/privacy/">Privacy</a><a href="/accessibility/">Accessibility</a><a href="/standards/#under-18">Under-18 policy</a>
      </div>
    </nav>
  </div>
  <a class="ft-wordmark" href="/" aria-label="Blaze Iconic, home"><img src="/assets/logo/wordmark-landscape-ink.svg" alt="Blaze Iconic" width="527" height="65" loading="lazy"></a>
  <div class="ft-base">
    {colophon}
    <span>{ADDRESS}</span>
    <span>{EMAIL}</span>
    <a href="#">Back to top <span aria-hidden="true">&uarr;</span></a>
  </div>
</footer>"""


def brief_html(meta: dict) -> str:
    if not meta.get("job"):
        return ""
    rows = [("Job", meta.get("job")), ("Main action", meta.get("action", "—")), ("Needs from Blaze", meta.get("needs", "—"))]
    dl = "".join(f"<div><dt>{k}</dt><dd>{html.escape(v)}</dd></div>" for k, v in rows)
    return f"""<aside class="brief" aria-label="Build notes">
  <p class="label brief-title"><span>Build notes · remove before launch</span><span>{html.escape(meta['path'])}</span></p>
  <dl>{dl}</dl>
</aside>"""


def hero_html(meta: dict) -> str:
    """Page hero: the Home hero, shorter, with the page name as the giant title."""
    if not meta.get("h1"):
        return ""
    cta = ""
    if meta.get("cta"):
        label, _, href = meta["cta"].partition("|")
        cta = f'<a class="hx-btn hx-btn--red" href="{href.strip()}">{html.escape(label.strip())} <span class="arrow">&rarr;</span></a>'
    img = HERO_IMAGES[zlib.crc32(meta["path"].encode()) % len(HERO_IMAGES)]
    return f"""<section class="hx-hero hx-hero--page">
  <img class="hx-hero-bg" src="/assets/img/{img}.jpg" alt="" width="2000" height="1250" fetchpriority="high">
  <div class="hx-hero-shade" aria-hidden="true"></div>
  <div class="hx-hero-inner">
    <div class="hx-hero-meta">
      <span class="hx-label">{html.escape(meta.get('eyebrow', meta['h1']))}</span>
      <span class="hx-label">Blaze Iconic</span>
    </div>
    <div class="hx-title-wrap">
      <h1 class="hx-h1">{html.escape(meta['h1'])}</h1>
      <div class="hx-rule"></div>
      <div class="hx-hero-foot">
        <p class="hx-tagline">{html.escape(meta.get('lede', ''))}</p>
        {cta}
      </div>
    </div>
    <div class="hx-hero-bottom">
      <span class="hx-label hx-dim">Publisher and PR service</span>
      <span class="hx-label">Scroll <span class="hx-arrow-down" aria-hidden="true">&darr;</span></span>
    </div>
  </div>
</section>
"""


def expand_partials(text: str) -> str:
    return re.sub(
        r"\{\{>\s*([\w-]+)\s*\}\}",
        lambda m: (SRC / "partials" / f"{m.group(1)}.html").read_text(encoding="utf-8"),
        text,
    )


def main() -> None:
    layout = (SRC / "layout.html").read_text(encoding="utf-8")

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    shutil.copytree(SRC / "assets", OUT / "assets")
    shutil.copy(SRC / "styles.css", OUT / "styles.css")
    shutil.copy(SRC / "main.js", OUT / "main.js")
    for extra in ("components.css", "home.js"):
        shutil.copy(SRC / extra, OUT / extra)
    (OUT / "robots.txt").write_text("# Staging build: keep out of search until launch\nUser-agent: *\nDisallow: /\n", encoding="utf-8")

    count = 0
    for page_file in sorted((SRC / "pages").glob("*.html")):
        meta = parse_page(page_file)
        path = meta["path"]
        legal = meta.get("legal", "").lower() == "yes"
        title = meta["title"]
        full_title = SITE if path == "/" else f"{title} · {SITE}"

        page = (
            layout.replace("{{title}}", html.escape(full_title))
            .replace("{{description}}", html.escape(meta.get("description", "")))
            .replace("{{header}}", header_html(path))
            .replace("{{footer}}", footer_html(legal))
            .replace("{{brief}}", brief_html(meta))
            .replace("{{body_class}}", "home" if path == "/" else "")
            .replace("{{head_extra}}", f'<link rel="stylesheet" href="{meta["css"]}">' if meta.get("css") else "")
            .replace("{{scripts_extra}}", f'<script src="{meta["js"]}" defer></script>' if meta.get("js") else "")
            .replace("{{content}}", hero_html(meta) + expand_partials(meta["body"]))
        )
        page = page.replace("{{entity}}", ENTITY).replace("{{address}}", ADDRESS).replace("{{email}}", EMAIL)

        if path == "/404.html":
            target = OUT / "404.html"
        else:
            target = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page, encoding="utf-8")
        count += 1

    print(f"built {count} pages -> {OUT}")


if __name__ == "__main__":
    main()
