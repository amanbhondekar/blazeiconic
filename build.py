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
    h1, eyebrow, lede    builds the page hero (title, small label, one line)
    {{> name}} in a body includes src/partials/name.html

    section: key        adds the section sub-navigation under the hero (see SUBNAV)
    hero_image: name     overrides the picked hero picture (src/assets/img/<name>.jpg)

Many pages (Talent, Expertise, PR, Portfolio, Journal, News, the Blaze Universe) are
generated from the structured data in content.py. Header, footer and layout are defined
here and in src/layout.html, so the navigation is edited in one place.
"""
import html
import re
import shutil
import zlib
from pathlib import Path

import content

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "public"

SITE = "Blaze Iconic"

# Page-hero images (src/assets/img); each page picks one by its URL. Swap files for real photography.
HERO_IMAGES = ["hero-b", "hero-c", "hero-d"]

# Header: four items and two calls to action (IA, Final Navigation System)
NAV = [
    ("Talent", "/talent/"),
    ("Expertise", "/expertise/"),
    ("PR", "/pr/"),
    ("Portfolio", "/portfolio/"),
]

# Section sub-navigation, shown under the page hero
SUBNAV = {
    "expertise": [("Overview", "/expertise/")] + [(e["name"], f"/expertise/{e['slug']}/") for e in content.EXPERTISE],
    "pr": [("Overview", "/pr/")] + [(e["name"], f"/pr/{e['slug']}/") for e in content.PR],
    "portfolio": [("All", "/portfolio/")] + [(n, f"/portfolio/{s}/") for s, n in content.PORT_CATS],
    "journal": [("All", "/journal/")] + [(n, f"/journal/{s}/") for s, n in content.JOURNAL_CATS],
    "news": [("All", "/news/")] + [(n, f"/news/{s}/") for s, n in content.NEWS_CATS],
    "get-scouted": [
        ("About Scouting", "/get-scouted/"),
        ("What We're Looking For", "/get-scouted/looking-for/"),
        ("Requirements", "/get-scouted/requirements/"),
        ("Application", "/get-scouted/apply/"),
    ],
    "about": [("About Blaze Iconic", "/about/"), ("Our Approach", "/about/our-approach/"), ("Contact / Desks", "/about/contact/")],
}

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
    links.append('<a class="btn btn--line" href="/get-scouted/">Get Scouted</a>')
    links.append('<a class="btn" href="/enquire/">Enquire</a>')
    return f"""<header class="site-header">
  <div class="hd-inner">
    <a class="hd-word" href="/" aria-label="Blaze Iconic, home"><img src="/assets/logo/wordmark-landscape-paper.svg" alt="Blaze Iconic" width="162" height="20"></a>
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

    def col(title, href, links):
        items = "".join(f'<a href="{h}">{n}</a>' for n, h in links)
        return f'<div class="ft-col"><h2><a href="{href}">{title}</a></h2>{items}</div>'

    journal = col("Journal", "/journal/", [(n, f"/journal/{s}/") for s, n in content.JOURNAL_CATS])
    about = col("About", "/about/", [("About Blaze Iconic", "/about/"), ("Our Approach", "/about/our-approach/"), ("Contact / Desks", "/about/contact/")])
    news = col("News", "/news/", [(n, f"/news/{s}/") for s, n in content.NEWS_CATS])
    universe = col("The Blaze Universe", "/#universe", [(f"{u['name']}", f"/{u['slug']}/") for u in content.UNIVERSE])
    return f"""<footer class="site-footer">
  <div class="ft-main">
    <nav class="ft-cols" aria-label="Footer">
      {journal}
      {about}
      {news}
      {universe}
    </nav>
  </div>
  <a class="ft-wordmark" href="/" aria-label="Blaze Iconic, home"><img src="/assets/logo/wordmark-landscape-paper.svg" alt="Blaze Iconic" width="527" height="65" loading="lazy"></a>
  <div class="ft-base">
    {colophon}
    <span>{ADDRESS}</span>
    <span>{EMAIL}</span>
    <span class="ft-legal"><a href="/terms/">Terms</a><a href="/privacy/">Privacy</a><a href="/accessibility/">Accessibility</a><a href="/get-scouted/requirements/#under-18">Under-18 policy</a></span>
    <a href="#">Back to top <span aria-hidden="true">&uarr;</span></a>
  </div>
</footer>"""


def subnav_html(meta: dict) -> str:
    key = meta.get("section")
    if not key or not meta.get("h1") or key not in SUBNAV:
        return ""
    links = "".join(
        '<a href="{}"{}>{}</a>'.format(h, ' aria-current="page"' if h == meta["path"] else "", html.escape(n)) for n, h in SUBNAV[key]
    )
    label = key.replace("-", " ").title()
    return '<nav class="hx-subnav" aria-label="{} sections">{}</nav>'.format(label, links) + "\n"


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
    img = meta.get("hero_image") or HERO_IMAGES[zlib.crc32(meta["path"].encode()) % len(HERO_IMAGES)]
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
      </div>
    </div>
  </div>
</section>
"""


def expand_partials(text: str) -> str:
    frags = content.fragments()
    text = re.sub(r"\{\{@([\w-]+)\}\}", lambda m: frags[m.group(1)], text)
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
    for extra in ("components.css", "preview.js", "talent.js", "enquire.js"):
        shutil.copy(SRC / extra, OUT / extra)
    (OUT / "robots.txt").write_text("# Staging build: keep out of search until launch\nUser-agent: *\nDisallow: /\n", encoding="utf-8")

    count = 0
    pages = [parse_page(f) for f in sorted((SRC / "pages").glob("*.html"))] + content.generate()
    seen = set()
    for meta in pages:
        path = meta["path"]
        assert path not in seen, f"duplicate page path {path}"
        seen.add(path)
        legal = meta.get("legal", "").lower() == "yes"
        title = meta["title"]
        full_title = SITE if path == "/" else f"{title} · {SITE}"

        page = (
            layout.replace("{{title}}", html.escape(full_title))
            .replace("{{description}}", html.escape(meta.get("description", "")))
            .replace("{{header}}", header_html(path))
            .replace("{{footer}}", footer_html(legal))
            .replace("{{brief}}", brief_html(meta))
            .replace("{{body_class}}", " ".join(c for c in ("home" if path == "/" else "", "has-hero" if path == "/" or meta.get("h1") else "") if c))
            .replace("{{head_extra}}", f'<link rel="stylesheet" href="{meta["css"]}">' if meta.get("css") else "")
            .replace("{{scripts_extra}}", f'<script src="{meta["js"]}" defer></script>' if meta.get("js") else "")
            .replace("{{content}}", hero_html(meta) + subnav_html(meta) + expand_partials(meta["body"]))
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
