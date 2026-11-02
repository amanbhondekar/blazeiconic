"""Generate the placeholder image set (original artwork, brand palette only).

    python tools/make_images.py

Soft silk-fabric studies: a fold height field is lit like a photograph, then
colour-graded between the kit colours (Ink, Wine, Blaze Red, Paper) with film
grain and a vignette. They stand in for photography; replace any file in
src/assets/img with a real photo of the same name and the site picks it up.
"""
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, zoom

OUT = Path(__file__).resolve().parent.parent / "src" / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

INK = np.array([0x17, 0x13, 0x0F], float)
PAPER = np.array([0xF5, 0xF0, 0xE6], float)
RED = np.array([0xB2, 0x1F, 0x2D], float)
WINE = np.array([0x3A, 0x0F, 0x1F], float)


def mix(a, b, t):
    return a * (1 - t) + b * t


# (position, colour) stops per treatment; every colour is a kit colour or a blend of two
GRADES = {
    "wine":  [(0.00, INK), (0.40, WINE), (0.78, mix(WINE, RED, .75)), (1.00, mix(RED, PAPER, .28))],
    "ink":   [(0.00, INK), (0.55, mix(INK, WINE, .45)), (1.00, mix(WINE, PAPER, .22))],
    "red":   [(0.00, WINE), (0.45, RED), (1.00, mix(RED, PAPER, .38))],
    "paper": [(0.00, mix(PAPER, INK, .5)), (0.50, mix(PAPER, INK, .1)), (1.00, PAPER)],
    # Light theme: soft Paper for hero and band grounds (text sits on them), and a red-free graphite
    "soft":     [(0.00, mix(PAPER, INK, .30)), (0.50, mix(PAPER, INK, .08)), (1.00, PAPER)],
    # Dark theme: deep Ink silk for heroes and the band (Paper type sits on them), red-free
    "deep":     [(0.00, INK), (0.55, mix(INK, PAPER, .13)), (1.00, mix(INK, PAPER, .36))],
    "graphite": [(0.00, INK), (0.55, mix(INK, PAPER, .22)), (1.00, mix(INK, PAPER, .62))],
}


def smooth_noise(rng, h, w, sigma):
    n = gaussian_filter(rng.standard_normal((h, w)), sigma)
    return n / (n.std() + 1e-9)


def silk(w, h, seed, waves=7, tilt=0.6):
    """Lit fold height field -> luminance 0..1 at (h, w)."""
    rng = np.random.default_rng(seed)
    sw = 360                                   # field resolution; folds are smooth
    sh = max(2, int(sw * h / w))
    yy, xx = np.mgrid[0:sh, 0:sw]
    x = xx / sw
    y = yy / sw
    warp_x = smooth_noise(rng, sh, sw, sw / 9) * 0.55
    warp_y = smooth_noise(rng, sh, sw, sw / 9) * 0.55
    height = np.zeros((sh, sw))
    for i in range(waves):
        theta = tilt + rng.normal(0, 0.45)
        freq = rng.uniform(1.2, 5.2) * (1 + i * 0.28)
        amp = 1.0 / (1 + i * 0.7)
        phase = rng.uniform(0, 2 * np.pi)
        u = (x + warp_x * 0.35) * np.cos(theta) + (y + warp_y * 0.35) * np.sin(theta)
        height += amp * np.sin(2 * np.pi * freq * u + phase + warp_x * 2.2)
    height += smooth_noise(rng, sh, sw, sw / 22) * 0.25
    height = gaussian_filter(height, 1.2)

    gy, gx = np.gradient(height)
    s = 3.2
    nx, ny, nz = -gx * s, -gy * s, np.ones_like(height)
    norm = np.sqrt(nx**2 + ny**2 + nz**2)
    nx, ny, nz = nx / norm, ny / norm, nz / norm
    light = np.array([-0.45, -0.55, 0.70])
    light /= np.linalg.norm(light)
    diffuse = np.clip(nx * light[0] + ny * light[1] + nz * light[2], 0, 1)
    half = light + np.array([0, 0, 1.0])
    half /= np.linalg.norm(half)
    spec = np.clip(nx * half[0] + ny * half[1] + nz * half[2], 0, 1) ** 55
    tone = diffuse * 0.8 + spec * 0.55
    lo, hi = np.percentile(tone, [2, 99.6])
    tone = np.clip((tone - lo) / (hi - lo), 0, 1) ** 1.15
    return zoom(tone, (h / sh, w / sw), order=3)[:h, :w]


def grade(tone, stops):
    pos = np.array([p for p, _ in stops])
    cols = np.stack([c for _, c in stops])
    out = np.empty(tone.shape + (3,))
    for ch in range(3):
        out[..., ch] = np.interp(tone, pos, cols[:, ch])
    return out


def render(name, w, h, seed, treatment, dark_edges=0.35, quality=80):
    rng = np.random.default_rng(seed + 1000)
    tone = silk(w, h, seed)
    img = grade(tone, GRADES[treatment])
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    vignette = 1 - dark_edges * np.clip(r - 0.35, 0, 1) ** 1.6
    img *= vignette[..., None]
    grain = rng.normal(0, 3.2, (h, w))[..., None]
    img = np.clip(img + grain, 0, 255).astype(np.uint8)
    Image.fromarray(img).save(OUT / f"{name}.jpg", quality=quality, optimize=True, progressive=True)
    print(f"{name}.jpg  {w}x{h}  {(OUT / f'{name}.jpg').stat().st_size // 1024} KB")


# Light theme: Paper-soft grounds for heroes and band (Ink type sits on them),
# Paper and red-free graphite for content imagery. No wine or red in the pictures:
# Blaze Red is reserved for the accent and for hover states.
SOFT = dict(dark_edges=0.30)

# Heroes and band (wide)
render("hero-a", 2400, 1500, 11, "deep", **SOFT)
render("hero-b", 2000, 1250, 22, "deep", **SOFT)
render("hero-c", 2000, 1250, 33, "deep", **SOFT)
render("hero-d", 2000, 1250, 44, "deep", **SOFT)
render("band", 2400, 1350, 55, "deep", **SOFT)

# Package previews (5:4)
for i, (seed, tone) in enumerate([(61, "paper"), (62, "graphite"), (63, "paper"), (64, "graphite"), (65, "paper")], 1):
    render(f"prev-{i}", 1250, 1000, seed, tone, dark_edges=0.15 if tone == "paper" else 0.3)

# Work cards (4:5). "paper" cards take Ink credit text; "graphite" cards take Paper text.
for i, (seed, tone) in enumerate([(71, "paper"), (72, "graphite"), (73, "paper"), (74, "paper"), (75, "graphite"), (76, "paper"), (77, "graphite"), (78, "paper")], 1):
    render(f"card-{i}", 1000, 1250, seed, tone, dark_edges=0.15 if tone == "paper" else 0.3)

# People and portrait (4:5)
for i, (seed, tone) in enumerate([(81, "paper"), (82, "graphite"), (83, "paper")], 1):
    render(f"person-{i}", 900, 1125, seed, tone, dark_edges=0.15 if tone == "paper" else 0.3)
render("portrait", 1000, 1250, 91, "graphite")
print("done ->", OUT)
