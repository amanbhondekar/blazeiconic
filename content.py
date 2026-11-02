"""Structured content and page generators for Blaze Iconic.

build.py merges the pages made here with the hand-written ones in src/pages.
Everything follows the sitemap and IA (blaze-iconic-sitemap-ia.md): Talent,
Expertise, PR and Portfolio in the header; Journal, About and News in the
footer; The Blaze Universe as a homepage section with its own landing pages.

Bracketed text is a placeholder until Blaze supplies the fact. No claims,
names or figures are invented.
"""
import html

# --------------------------------------------------------------------------
# Imagery: generated placeholder art (tools/make_images.py). Swap files of the
# same name for photography.
# --------------------------------------------------------------------------
POOL = [(f"card-{i}", 1000, 1250) for i in range(1, 9)] + [
    ("person-1", 900, 1125), ("person-2", 900, 1125), ("person-3", 900, 1125), ("portrait", 1000, 1250),
]
WIDE = ["hero-b", "hero-c", "hero-d", "hero-a"]


def pool(i: int):
    name, w, h = POOL[i % len(POOL)]
    return f"/assets/img/{name}.jpg", w, h


def esc(s: str) -> str:
    return html.escape(s, quote=True)


# --------------------------------------------------------------------------
# Talent
# --------------------------------------------------------------------------
CATEGORIES = [("fashion", "Fashion"), ("beauty", "Beauty"), ("swimwear", "Swimwear"), ("boudoir", "Boudoir")]
CAT_NAME = dict(CATEGORIES)

# (slug, primary category, optional secondary). Names are placeholders.
MODELS = [
    ("model-01", "fashion", "beauty"),
    ("model-02", "beauty", None),
    ("model-03", "swimwear", "fashion"),
    ("model-04", "boudoir", None),
    ("model-05", "fashion", None),
    ("model-06", "beauty", "fashion"),
    ("model-07", "swimwear", None),
    ("model-08", "boudoir", "swimwear"),
]


def model_name(slug: str) -> str:
    return f"[Model name {slug[-2:]}]"


# --------------------------------------------------------------------------
# Expertise (what Blaze does) and PR (how Blaze positions and amplifies)
# --------------------------------------------------------------------------
EXPERTISE = [
    dict(slug="photoshoots", name="Photoshoots", enquire="photoshoot", portfolio="photoshoots",
         lede="Campaign, fashion, beauty, product and model shoots, with production and talent sourcing in one place.",
         covers=["Campaign photoshoots", "Fashion shoots", "Beauty shoots", "Product shoots", "Model shoots", "Production capabilities", "Talent sourcing"]),
    dict(slug="cover-features", name="Cover Features", enquire="editorial-cover", portfolio="feature-covers", paid=True,
         lede="Magazine cover opportunities, with talent placement, cover production and publication relationships.",
         covers=["Magazine cover opportunities", "Talent placement", "Cover production", "Publication relationships", "Featured talent"]),
    dict(slug="billboards", name="Billboards", enquire="photoshoot", portfolio="billboards",
         lede="Out-of-home campaigns and billboard placements, led by talent and carried through to execution.",
         covers=["OOH campaigns", "Billboard placements", "Talent-led advertising", "Campaign execution"]),
    dict(slug="editorial", name="Editorial", enquire="editorial-cover", portfolio="editorials",
         lede="Fashion and beauty editorials, from production and casting to creative collaboration.",
         covers=["Fashion editorials", "Beauty editorials", "Editorial production", "Talent casting", "Creative collaborations"]),
    dict(slug="runway-events", name="Runway & Events", enquire="book-talent", portfolio="",
         lede="Runway casting, fashion events and show appearances, with event production support.",
         covers=["Runway casting", "Fashion events", "Event talent", "Show appearances", "Event production support"]),
]

PR = [
    dict(slug="media-relations", name="Media Relations", enquire="pr-media", portfolio="",
         lede="Press outreach and media relationships that open editorial opportunities and placements.",
         covers=["Press outreach", "Media relationships", "Editorial opportunities", "Press placements", "Media coverage"]),
    dict(slug="talent-positioning", name="Talent Positioning", enquire="pr-media", portfolio="",
         lede="Personal brand positioning and profile building, with strategic media opportunities for talent.",
         covers=["Personal brand positioning", "Talent visibility", "Profile building", "Strategic media opportunities"]),
    dict(slug="campaign-pr", name="Campaign PR", enquire="pr-media", portfolio="",
         lede="Launch publicity for campaigns, brands, fashion and beauty, events and products.",
         covers=["Campaign launches", "Brand publicity", "Fashion and beauty PR", "Event PR", "Product and campaign amplification"]),
    dict(slug="digital-social", name="Digital & Social", enquire="pr-media", portfolio="",
         lede="Digital PR and social amplification that extend visibility online through content-led publicity.",
         covers=["Digital PR", "Social amplification", "Online visibility", "Content-led publicity"]),
    dict(slug="reputation", name="Reputation", enquire="pr-media", portfolio="",
         lede="Reputation strategy for brands and talent, including issue management and crisis communication.",
         covers=["Reputation strategy", "Issue management", "Crisis communication", "Brand and talent reputation"]),
]

# --------------------------------------------------------------------------
# Portfolio (proof)
# --------------------------------------------------------------------------
PORT_CATS = [("photoshoots", "Photoshoots"), ("feature-covers", "Feature Covers"), ("editorials", "Editorials"), ("billboards", "Billboards")]
PORT_NAME = dict(PORT_CATS)
EXPERTISE_FOR = {"photoshoots": "photoshoots", "feature-covers": "cover-features", "editorials": "editorial", "billboards": "billboards"}

# (slug, category)
ITEMS = [
    ("item-01", "photoshoots"), ("item-02", "feature-covers"), ("item-03", "editorials"), ("item-04", "billboards"),
    ("item-05", "photoshoots"), ("item-06", "feature-covers"), ("item-07", "editorials"), ("item-08", "billboards"),
]

# --------------------------------------------------------------------------
# Journal (evergreen, editorial) and News (timely)
# --------------------------------------------------------------------------
JOURNAL_CATS = [("fashion", "Fashion"), ("beauty", "Beauty"), ("talent", "Talent"), ("culture", "Culture"), ("industry", "Industry")]
NEWS_CATS = [("blaze-updates", "Blaze Updates"), ("talent-news", "Talent News"), ("announcements", "Announcements"), ("press", "Press")]
JOURNAL_ITEMS = [("story-01", "fashion"), ("story-02", "beauty"), ("story-03", "talent"), ("story-04", "culture"), ("story-05", "industry"), ("story-06", "talent")]
NEWS_ITEMS = [("update-01", "blaze-updates"), ("update-02", "talent-news"), ("update-03", "announcements"), ("update-04", "press")]

# --------------------------------------------------------------------------
# The Blaze Universe
# --------------------------------------------------------------------------
UNIVERSE = [
    dict(slug="the-black-mags", name="The Black Mags", kind="Magazine", img="prev-1",
         sections=["Latest Issue", "Stories", "Covers", "Archive"],
         lede="[One sentence on The Black Mags: what it publishes and who it is for.]"),
    dict(slug="maxi-boudoir", name="Maxi Boudoir", kind="Magazine", img="prev-2",
         sections=["Latest Issue", "Stories", "Covers", "Archive"],
         lede="[One sentence on Maxi Boudoir: what it publishes and who it is for.]"),
    dict(slug="mirror", name="Mirror", kind="Podcast", img="prev-3",
         sections=["Latest Episode", "Episodes", "About"],
         lede="[One sentence on Mirror: what the podcast covers and who hosts it.]"),
]


# ==========================================================================
# Components
# ==========================================================================
def gcard(href, img, w, h, title, sub="", tab=False, extra="", attrs=""):
    """Image card: 4:5 picture, name and a small line underneath. Red bar and red name on hover."""
    label = '<span class="label-tab">Sponsored feature</span>' if tab else ""
    sub_html = f'<span class="hx-label hx-dim">{sub}</span>' if sub else ""
    return (
        f'<a class="hx-gcard reveal {extra}" href="{href}" {attrs}>'
        f'<span class="hx-gimg"><img src="{img}" alt="" width="{w}" height="{h}" loading="lazy" draggable="false">{label}</span>'
        f'<span class="hx-gcap"><span class="hx-gname">{title}</span>{sub_html}</span></a>'
    )


def rail(cards):
    return '<div class="hx-rail"><div class="hx-track">' + "".join(cards) + "</div></div>"


def head(label, title, link=None):
    right = f'<a class="hx-btn hx-btn--sm" href="{link[1]}">{link[0]} <span class="arrow">&nearr;</span></a>' if link else ""
    return (
        f'<div class="hx-head"><div><p class="hx-label reveal">{label}</p>'
        f'<h2 class="hx-display reveal">{title}</h2></div>{right}</div>'
    )


def portfolio_card(slug, cat, i, extra=""):
    img, w, h = pool(i + 3)
    return gcard(f"/portfolio/{slug}/", img, w, h, f"[Project / Brand name {slug[-2:]}]", f"{PORT_NAME[cat]} &middot; [Year]", tab=(cat == "feature-covers"), extra=extra)


def talent_card(slug, cat, sec, i, extra=""):
    img, w, h = pool(i)
    cats = f"{cat} {sec}" if sec else cat
    sub = CAT_NAME[cat] + (f" &middot; {CAT_NAME[sec]}" if sec else "")
    return gcard(f"/talent/{slug}/", img, w, h, model_name(slug), sub, extra=extra, attrs=f'data-cats="{cats}"')


def page(title, path, body, **meta):
    d = dict(title=title, path=path, body=body, description=meta.pop("description", f"[Meta description: {title}.]"))
    d.update(meta)
    return d


def cta_block(enquire_type=None):
    return "{{> cta-split}}"


# ==========================================================================
# Generators
# ==========================================================================
def talent_pages():
    pages = []
    chips = '<div class="hx-chips" role="group" aria-label="Filter talent by category"><a class="hx-chip is-on" href="#all" data-filter="all" aria-pressed="true">All</a>' + "".join(
        f'<a class="hx-chip" href="#{s}" data-filter="{s}" aria-pressed="false">{n}</a>' for s, n in CATEGORIES
    ) + "</div>"
    cards = "".join(talent_card(s, c, sc, i) for i, (s, c, sc) in enumerate(MODELS))
    body = f"""<section class="hx-paper" id="directory">
  {head("01 &mdash; All Talent", "The roster")}
  {chips}
  <div class="hx-grid hx-grid--4" id="talentGrid">{cards}</div>
  <p class="hx-empty" id="talentEmpty" hidden>[No talent in this category yet.]</p>
  <p class="hx-hint hx-grid-note">Only filters the roster supports are shown. [Location, availability and specialisation can be added once the roster data exists.]</p>
</section>

{{{{> cta-split}}}}"""
    pages.append(page(
        "Talent", "/talent/", body,
        description="[Meta description: the Blaze Iconic roster across Fashion, Beauty, Swimwear and Boudoir.]",
        eyebrow="Talent", h1="Talent", lede="One directory for every model Blaze Iconic represents, filtered by category.",
        cta="Enquire | /enquire/?type=book-talent", js="/talent.js", section="",
        job="Model discovery and booking. One directory, category filters, an individual profile for every model.",
        action="Book / Enquire from a profile", needs="Roster, model names, hero images, categories, optional location."))

    for i, (slug, cat, sec) in enumerate(MODELS):
        name = model_name(slug)
        img, w, h = pool(i)
        cats = CAT_NAME[cat] + (f", {CAT_NAME[sec]}" if sec else "")
        related = [(s, c, k) for k, (s, c) in enumerate(ITEMS)][:4]
        port = rail([portfolio_card(s, c, k) for s, c, k in related])
        digs = "".join(
            f'<figure class="hx-dig reveal"><img src="{pool(i + 1 + d)[0]}" alt="" width="{pool(i + 1 + d)[1]}" height="{pool(i + 1 + d)[2]}" loading="lazy"><figcaption class="hx-label hx-dim">Digital 0{d + 1}</figcaption></figure>'
            for d in range(4)
        )
        body = f"""<section class="hx-paper hx-profile">
  <img class="hx-profile-img" src="{img}" alt="" width="{w}" height="{h}" fetchpriority="high">
  <div class="hx-profile-text">
    <a class="hx-link" href="/talent/#{cat}">&larr; All Talent</a>
    <p class="hx-label" style="opacity:.65">{CAT_NAME[cat]}</p>
    <h1 class="hx-name">{name}</h1>
    <dl class="hx-spec">
      <div><dt>Categories</dt><dd>{cats}</dd></div>
      <div><dt>Measurements</dt><dd>[Height, bust, waist, hips, shoe, hair, eyes]</dd></div>
      <div><dt>Location</dt><dd>[City]</dd></div>
    </dl>
    <p class="hx-text">Is this talent right for your project? Selected portfolio, digitals and video are below. [Short line on range and camera presence.]</p>
    <div class="hx-inline-links">
      <a class="hx-btn hx-btn--red" href="/enquire/?type=book-talent&amp;talent={slug}">Book / Enquire <span class="arrow">&rarr;</span></a>
    </div>
  </div>
</section>

<section class="hx-section hx-alt hx-bordered">
  {head("01 &mdash; Selected portfolio", "Selected work", ("Open portfolio", "/portfolio/"))}
  {port}
</section>

<section class="hx-paper">
  {head("02 &mdash; Digitals", "Digitals")}
  <div class="hx-grid hx-grid--4 hx-digs">{digs}</div>
</section>

<section class="hx-section hx-alt hx-bordered">
  {head("03 &mdash; Video / Reels", "Video and reels")}
  <div class="hx-panel hx-panel--wide reveal"><img src="/assets/img/{WIDE[i % 4]}.jpg" alt="" width="2000" height="1250" loading="lazy"><p>[Video / reel embed]</p></div>
</section>

{{{{> cta-split}}}}"""
        pages.append(page(
            name, f"/talent/{slug}/", body,
            description=f"[Meta description: {name}, {cats}, Blaze Iconic.]",
            job="Answer: is this talent suitable for my project? Visual range, camera presence, categories, measurements, booking.",
            action="Book / Enquire", needs="Hero image, selected portfolio, digitals, reels, categories, measurements, location."))
    return pages


def service_pages(section, items, hub_title, hub_lede, hub_job, hub_needs, paid_note=False):
    """Expertise and PR share one shape: a hub with a list and preview, then one page per service."""
    pages = []
    base = f"/{section}/"
    rows = "".join(
        f'<a class="hx-row{" is-active" if i == 0 else ""}" data-index="{i}" href="{base}{it["slug"]}/"><span class="hx-label hx-dim hx-row-idx">0{i + 1}</span>'
        f'<span class="hx-row-name">{it["name"]}</span><span class="hx-label hx-dim">View &rarr;</span></a>'
        for i, it in enumerate(items)
    )
    body = f"""<section class="hx-paper">
  {head("01 &mdash; " + hub_title, hub_lede)}
  <div class="hx-list-grid">
    <div class="hx-list">{rows}</div>
    <figure class="hx-preview">
      <img class="hx-preview-img" id="hxPreview" src="/assets/img/prev-1.jpg" alt="" width="1250" height="1000" loading="lazy">
      <figcaption class="hx-preview-tag hx-label" id="hxPreviewTag">Preview 01</figcaption>
    </figure>
  </div>
</section>

{{{{> cta-split}}}}"""
    pages.append(page(
        hub_title, base, body,
        description=f"[Meta description: {hub_title} at Blaze Iconic.]",
        eyebrow=hub_title, h1=hub_title, lede=hub_lede, cta=f"Enquire | /enquire/?type={items[0]['enquire']}",
        js="/preview.js", section=section, job=hub_job, action="Enquire", needs=hub_needs))

    for i, it in enumerate(items):
        covers = "".join(
            f'<div class="hx-row"><span class="hx-label hx-dim hx-row-idx">0{k + 1}</span><span class="hx-row-name">{c}</span><span class="hx-label hx-dim"></span></div>'
            for k, c in enumerate(it["covers"])
        )
        paid = ""
        if it.get("paid"):
            paid = ('<aside class="hx-notice reveal" style="margin-top:var(--sp-5)"><span class="label-tab" style="justify-self:start">Sponsored feature</span>'
                    '<p>[Where a cover feature is paid, it carries the Sponsored feature label above the headline. Wording pending counsel.]</p></aside>')
        if it["portfolio"]:
            related = [(s, c, k) for k, (s, c) in enumerate(ITEMS) if c == it["portfolio"]]
            proof = (head("02 &mdash; Related work", f"{PORT_NAME[it['portfolio']]} in the portfolio", ("Open portfolio", f"/portfolio/{it['portfolio']}/"))
                     + rail([portfolio_card(s, c, k) for s, c, k in related]))
        else:
            proof = (head("02 &mdash; Related work", "See it in the portfolio", ("Open portfolio", "/portfolio/"))
                     + rail([portfolio_card(s, c, k) for s, c, k in [(s, c, k) for k, (s, c) in enumerate(ITEMS)][:3]]))
        nxt = items[(i + 1) % len(items)]
        body = f"""<section class="hx-paper">
  <div class="hx-cols">
    <div class="hx-cols-head">
      <p class="hx-label reveal">01 &mdash; What it covers</p>
      <h2 class="hx-display reveal">{it['name']}</h2>
      <p class="hx-lede reveal" style="margin-top:var(--sp-4)">{it['lede']} [Fuller description, written by Blaze.]</p>
      <div class="hx-inline-links reveal" style="margin-top:var(--sp-4)"><a class="hx-btn hx-btn--red" href="/enquire/?type={it['enquire']}">Enquire <span class="arrow">&rarr;</span></a></div>
    </div>
    <div class="hx-cols-body">
      <div class="hx-list hx-list--plain reveal">{covers}</div>
      {paid}
    </div>
  </div>
</section>

<section class="hx-section hx-alt hx-bordered">
  {proof}
</section>

<section class="hx-strip hx-bordered">
  <a class="hx-strip-item" href="{base}{nxt['slug']}/"><span class="hx-label hx-dim">Next</span><span class="hx-strip-name">{nxt['name']} &rarr;</span></a>
  <a class="hx-strip-item" href="{base}"><span class="hx-label hx-dim">All</span><span class="hx-strip-name">{hub_title} &uarr;</span></a>
</section>

{{{{> cta-split}}}}"""
        pages.append(page(
            it["name"], f"{base}{it['slug']}/", body,
            description=f"[Meta description: {it['name']}, {hub_title} at Blaze Iconic.]",
            eyebrow=hub_title, h1=it["name"], lede=it["lede"], cta=f"Enquire | /enquire/?type={it['enquire']}", section=section))
    return pages


def portfolio_pages():
    pages = []
    all_cards = lambda cats: "".join(portfolio_card(s, c, k) for k, (s, c) in enumerate(ITEMS) if c in cats)
    pages.append(page(
        "Portfolio", "/portfolio/",
        f"""<section class="hx-paper">
  {head("01 &mdash; All", "Selected work")}
  <div class="hx-grid hx-grid--3">{all_cards([c for c, _ in PORT_CATS])}</div>
</section>

{{{{> cta-split}}}}""",
        description="[Meta description: selected Blaze Iconic work across photoshoots, feature covers, editorials and billboards.]",
        eyebrow="Portfolio", h1="Portfolio", lede="What Blaze Iconic has produced, facilitated or placed, curated as work and not as a feed.",
        cta="Enquire | /enquire/", section="portfolio",
        job="Proof layer. Visual-first and editorial, not an Instagram-style feed.",
        action="Enquire from a project", needs="Projects, hero images, brands, publications, years, credits and usage permissions."))
    blurbs = {
        "photoshoots": "Campaign, fashion and beauty imagery, talent-led shoots and selected project photography.",
        "feature-covers": "Magazine covers, publication features, talent covers and cover stories.",
        "editorials": "Editorial spreads, fashion and beauty stories, and styled shoots.",
        "billboards": "Billboard campaigns, OOH placements, large-format advertising and talent-led campaigns.",
    }
    for slug, name in PORT_CATS:
        pages.append(page(
            name, f"/portfolio/{slug}/",
            f"""<section class="hx-paper">
  {head("01 &mdash; " + name, name)}
  <div class="hx-grid hx-grid--3">{all_cards([slug])}</div>
</section>

{{{{> cta-split}}}}""",
            description=f"[Meta description: {name} in the Blaze Iconic portfolio.]",
            eyebrow="Portfolio", h1=name, lede=blurbs[slug], cta="Enquire | /enquire/", section="portfolio"))
    for k, (slug, cat) in enumerate(ITEMS):
        title = f"[Project / Brand name {slug[-2:]}]"
        img = WIDE[k % 4]
        sel = "".join(
            f'<figure class="hx-dig reveal"><img src="{pool(k + 5 + d)[0]}" alt="" width="{pool(k + 5 + d)[1]}" height="{pool(k + 5 + d)[2]}" loading="lazy"></figure>' for d in range(3)
        )
        tab = '<span class="label-tab" style="margin-bottom:var(--sp-2)">Sponsored feature</span>' if cat == "feature-covers" else ""
        exp = EXPERTISE_FOR[cat]
        exp_name = next(e["name"] for e in EXPERTISE if e["slug"] == exp)
        enq = next(e["enquire"] for e in EXPERTISE if e["slug"] == exp)
        body = f"""<section class="hx-paper">
  <div class="hx-cols">
    <div class="hx-cols-head">
      <a class="hx-link" href="/portfolio/{cat}/">&larr; {PORT_NAME[cat]}</a>
      <p class="hx-label" style="margin-top:var(--sp-4);opacity:.65">{PORT_NAME[cat]}</p>
      {tab}
      <h1 class="hx-name" style="margin-top:var(--sp-2)">{title}</h1>
    </div>
    <div class="hx-cols-body">
      <dl class="hx-spec">
        <div><dt>Project / Brand</dt><dd>{title}</dd></div>
        <div><dt>Category</dt><dd>{PORT_NAME[cat]}</dd></div>
        <div><dt>Year</dt><dd>[Year]</dd></div>
        <div><dt>Talent</dt><dd><a href="/talent/model-{(k % 8) + 1:02d}/">{model_name(f"model-{(k % 8) + 1:02d}")}</a></dd></div>
        <div><dt>Publication / Brand</dt><dd>[Publication or brand]</dd></div>
      </dl>
      <div class="hx-inline-links"><a class="hx-btn hx-btn--red" href="/enquire/?type={enq}">Enquire <span class="arrow">&rarr;</span></a><a class="hx-btn" href="/expertise/{exp}/">Related: {exp_name} <span class="arrow">&nearr;</span></a></div>
    </div>
  </div>
</section>

<section class="hx-section hx-alt hx-bordered">
  {head("01 &mdash; Selected images", "Selected images")}
  <div class="hx-grid hx-grid--3">{sel}</div>
</section>

{{{{> cta-split}}}}"""
        pages.append(page(
            title, f"/portfolio/{slug}/", body, hero_image=img, description=f"[Meta description: {title}, {PORT_NAME[cat]}.]",
            job="A portfolio item. Not every item needs to be a full case study; depth follows the importance of the project.",
            action="Enquire / related expertise", needs="Hero image, selected images, brand, year, talent, publication, usage permission."))
    return pages


def article_pages(section, label, cats, items, hub_title, hub_lede, hub_job):
    pages = []
    base = f"/{section}/"
    cat_name = dict(cats)

    def rows(sel):
        out = []
        for k, (slug, cat) in enumerate(items):
            if sel and cat != sel:
                continue
            out.append(
                f'<a class="hx-row" href="{base}{slug}/"><span class="hx-label hx-dim hx-row-idx">0{k + 1}</span>'
                f'<span class="hx-row-name">[{label} title {slug[-2:]}]</span><span class="hx-label hx-dim">{cat_name[cat]} &middot; [Date]</span></a>'
            )
        return "".join(out) or '<p class="hx-empty">[Nothing here yet.]</p>'

    pages.append(page(
        hub_title, base,
        f"""<section class="hx-paper">
  {head("01 &mdash; Latest", f"Latest from the {hub_title}")}
  <div class="hx-list hx-list--plain">{rows(None)}</div>
</section>

{{{{> cta-split}}}}""",
        description=f"[Meta description: {hub_title} from Blaze Iconic.]",
        eyebrow=hub_title, h1=hub_title, lede=hub_lede, cta="Enquire | /enquire/", section=section, job=hub_job,
        action="Read a story", needs="Content owner and publishing rhythm. Merge News into Journal later if volume stays low."))
    for slug, name in cats:
        pages.append(page(
            name, f"{base}{slug}/",
            f"""<section class="hx-paper">
  {head("01 &mdash; " + name, name)}
  <div class="hx-list hx-list--plain">{rows(slug)}</div>
</section>

{{{{> cta-split}}}}""",
            description=f"[Meta description: {name}, {hub_title} from Blaze Iconic.]",
            eyebrow=hub_title, h1=name, lede=f"{hub_title}: {name}.", cta="Enquire | /enquire/", section=section))
    for k, (slug, cat) in enumerate(items):
        t = f"[{label} title {slug[-2:]}]"
        body = f"""<section class="hx-paper">
  <div class="hx-cols">
    <div class="hx-cols-head">
      <a class="hx-link" href="{base}{cat}/">&larr; {cat_name[cat]}</a>
      <p class="hx-label" style="margin-top:var(--sp-4);opacity:.65">{cat_name[cat]} &middot; [Date] &middot; [Author]</p>
      <h1 class="hx-name" style="margin-top:var(--sp-2)">{t}</h1>
    </div>
    <div class="hx-cols-body">
      <p class="hx-lede">[Standfirst: one or two sentences.]</p>
      <img class="hx-article-img" src="/assets/img/{WIDE[k % 4]}.jpg" alt="" width="2000" height="1250" loading="lazy">
      <div class="hx-text"><p>[Article body, written by Blaze.]</p></div>
    </div>
  </div>
</section>

<section class="hx-strip hx-bordered hx-alt">
  <a class="hx-strip-item" href="{base}"><span class="hx-label hx-dim">More</span><span class="hx-strip-name">All {hub_title} &rarr;</span></a>
</section>

{{{{> cta-split}}}}"""
        pages.append(page(t, f"{base}{slug}/", body, description=f"[Meta description: {t}.]"))
    return pages


def universe_pages():
    pages = []
    for u in UNIVERSE:
        anchors = "".join(f'<a class="hx-chip" href="#{s.lower().replace(" ", "-")}">{s}</a>' for s in u["sections"])
        blocks = []
        for k, s in enumerate(u["sections"]):
            sid = s.lower().replace(" ", "-")
            cls = "hx-paper" if k % 2 == 0 else "hx-section hx-alt hx-bordered"
            if s in ("Covers", "Latest Issue", "Latest Episode"):
                cards = rail([
                    gcard("#", pool(k + j)[0], pool(k + j)[1], pool(k + j)[2], f"[{s} item {j + 1}]", u["kind"])
                    for j in range(3)
                ])
            else:
                cards = '<div class="hx-list hx-list--plain">' + "".join(
                    f'<div class="hx-row"><span class="hx-label hx-dim hx-row-idx">0{j + 1}</span><span class="hx-row-name">[{s} entry {j + 1}]</span><span class="hx-label hx-dim">[Date]</span></div>'
                    for j in range(3)
                ) + "</div>"
            blocks.append(f'<section class="{cls}" id="{sid}">{head(f"0{k + 1} &mdash; {s}", s)}{cards}</section>')
        body = f"""<section class="hx-strip hx-bordered">
  <div class="hx-chips" role="navigation" aria-label="{u['name']}">{anchors}</div>
  <a class="hx-link" href="/#universe">The Blaze Universe &nearr;</a>
</section>

{''.join(blocks)}

{{{{> cta-split}}}}"""
        pages.append(page(
            u["name"], f"/{u['slug']}/", body,
            description=f"[Meta description: {u['name']}, a {u['kind'].lower()} in the Blaze Universe.]",
            eyebrow=u["kind"], h1=u["name"], lede=u["lede"], cta="Enquire | /enquire/?type=editorial-cover", section="", hero_image="hero-b" if u["kind"] == "Magazine" else "hero-d",
            job=f"A property in the Blaze Universe, not a sub-page of the agency's services. {u['kind']}.",
            action="Open the latest", needs="Destination (own site or this page), logo artwork, latest issue or episode, links."))
    return pages


def generate():
    pages = []
    pages += talent_pages()
    pages += service_pages(
        "expertise", EXPERTISE, "Expertise", "What Blaze Iconic does for brands, clients and production teams.",
        "Explain what Blaze can provide. Five services, terminology exactly as defined.", "Descriptions and capability detail for each service.")
    pages += service_pages(
        "pr", PR, "PR", "How Blaze Iconic positions, promotes and amplifies talent, campaigns and brands.",
        "A standalone capability: media, positioning, campaigns, digital and reputation.", "Descriptions, proof points and any case material per capability.")
    pages += portfolio_pages()
    pages += article_pages("journal", "Story", JOURNAL_CATS, JOURNAL_ITEMS, "Journal",
                           "Blaze Iconic's editorial voice: fashion, beauty, talent, culture and industry.",
                           "Evergreen editorial content; does not compete with The Black Mags or Maxi Boudoir.")
    pages += article_pages("news", "Update", NEWS_CATS, NEWS_ITEMS, "News",
                           "Timely updates and announcements from Blaze Iconic.",
                           "Timely updates, not long-form editorial. Merge into Journal later if content volume is low.")
    pages += universe_pages()
    return pages


def fragments():
    """Blocks the hand-written Home page pulls in with {{@name}}."""
    frag = {}
    frag["talent_rail"] = rail([talent_card(s, c, sc, i) for i, (s, c, sc) in enumerate(MODELS)])
    frag["talent_chips"] = '<div class="hx-chips" role="navigation" aria-label="Talent categories">' + "".join(
        f'<a class="hx-chip" href="/talent/#{s}">{n}</a>' for s, n in CATEGORIES
    ) + "</div>"
    frag["expertise_rows"] = "".join(
        f'<a class="hx-row{" is-active" if i == 0 else ""}" data-index="{i}" href="/expertise/{e["slug"]}/"><span class="hx-label hx-dim hx-row-idx">0{i + 1}</span>'
        f'<span class="hx-row-name">{e["name"]}</span><span class="hx-label hx-dim">View &rarr;</span></a>'
        for i, e in enumerate(EXPERTISE)
    )
    frag["portfolio_grid"] = '<div class="hx-grid hx-grid--3">' + "".join(portfolio_card(s, c, k) for k, (s, c) in enumerate(ITEMS[:3])) + "</div>"
    frag["pr_links"] = " ".join(f'<a href="/pr/{p["slug"]}/">{p["name"]}</a>' for p in PR)
    frag["universe_cards"] = '<div class="hx-grid hx-grid--3">' + "".join(
        gcard(f"/{u['slug']}/", f"/assets/img/{u['img']}.jpg", 1250, 1000, u["name"], u["kind"]) for u in UNIVERSE
    ) + "</div>"

    def rows(base, label, cats, items, n):
        cn = dict(cats)
        return "".join(
            f'<a class="hx-row" href="{base}{slug}/"><span class="hx-label hx-dim hx-row-idx">0{k + 1}</span>'
            f'<span class="hx-row-name">[{label} title {slug[-2:]}]</span><span class="hx-label hx-dim">{cn[cat]}</span></a>'
            for k, (slug, cat) in enumerate(items[:n])
        )

    frag["journal_head"] = head("06 &mdash; Journal", "Latest stories", ("Journal", "/journal/"))
    frag["news_head"] = head("07 &mdash; News", "Latest updates", ("News", "/news/"))
    frag["journal_rows"] = rows("/journal/", "Story", JOURNAL_CATS, JOURNAL_ITEMS, 3)
    frag["news_rows"] = rows("/news/", "Update", NEWS_CATS, NEWS_ITEMS, 3)
    return frag
