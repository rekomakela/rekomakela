"""Write the profile SVGs (light and dark) next to this file: python3 assets/build.py"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "light": {"fg": "#1f2328", "muted": "#59636e", "line": "#d1d9e0", "tile": "#f6f8fa", "accent": "#0969da", "own": "#1a7f37"},
    "dark": {"fg": "#e6edf3", "muted": "#9198a1", "line": "#3d444d", "tile": "#151b23", "accent": "#4493f8", "own": "#3fb950"},
}
W = 840

STATS = [
    ("314,000+", "products compared", "Hintapiste.fi"),
    ("29", "online shops", "Hintapiste.fi"),
    ("1,100+", "agent code changes", "Jul–Oct 2026, all tested"),
    ("69", "test steps per change", "before release"),
]

ROLES = [  # (label, place, start, end, own project)
    ("Affiliate marketing and SEO consulting", "Independent", 2018.0, 2021.67, False),
    ("SEO and digital marketing development", "Terveystalo", 2021.67, 2022.67, False),
    ("SEO / Digital Marketing Specialist", "Terveystalo", 2022.67, 2024.33, False),
    ("Digital Sales Specialist", "Terveystalo", 2024.33, 2026.8, False),
    ("Hintapiste.fi, built by AI agents", "Own project", 2026.5, 2026.8, True),
]


def text(x, y, s, size, fill, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')


def svg(h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{"".join(body)}</svg>\n')


def header(c):
    body = [
        text(0, 40, "Reko Mäkelä", 34, c["fg"], 600),
        text(0, 72, "AI agents, automation and SEO for marketing · Helsinki", 17, c["muted"]),
    ]
    gap, top, th = 12, 100, 104
    tw = (W - gap * 3) / 4
    for i, (big, label, note) in enumerate(STATS):
        x = i * (tw + gap)
        body.append(f'<rect x="{x + .5}" y="{top + .5}" width="{tw - 1}" height="{th - 1}" rx="10" fill="{c["tile"]}" stroke="{c["line"]}"/>')
        body.append(text(x + 16, top + 42, big, 28, c["accent"], 600))
        body.append(text(x + 16, top + 66, label, 14, c["fg"]))
        body.append(text(x + 16, top + 87, note, 12, c["muted"]))
    return svg(top + th + 2, body, "Reko Mäkelä: AI agents, automation and SEO for marketing, Helsinki. "
               + "; ".join(f"{b} {l} ({n})" for b, l, n in STATS))


def timeline(c):
    y0, row, left, right = 16, 38, 0, W
    start, end = 2018.0, 2027.0
    sx = lambda year: left + (year - start) / (end - start) * (right - left)
    body = []
    rows = len(ROLES)
    axis = y0 + rows * row + 8
    for year in range(2018, 2028):
        x = sx(year)
        body.append(f'<line x1="{x}" y1="{y0 - 8}" x2="{x}" y2="{axis}" stroke="{c["line"]}" stroke-dasharray="2 4"/>')
        if year < 2027:
            body.append(text(x + 4, axis + 18, str(year), 12, c["muted"]))
    for i, (label, place, a, b, own) in enumerate(ROLES):
        y = y0 + i * row
        colour = c["own"] if own else c["accent"]
        body.append(f'<rect x="{sx(a)}" y="{y}" width="{max(sx(b) - sx(a), 8)}" height="10" rx="5" fill="{colour}"/>')
        caption = f"{label} · {place}"
        if sx(a) > W / 2:
            body.append(text(sx(b), y + 27, caption, 13, c["fg"], anchor="end"))
        else:
            body.append(text(sx(a), y + 27, caption, 13, c["fg"]))
    return svg(axis + 26, body, "Career timeline: " + "; ".join(f"{l}, {p}, {int(a)}–{'now' if b > 2026.7 else int(b)}" for l, p, a, b, _ in ROLES))


for name, theme in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(theme), encoding="utf-8")
    (OUT / f"timeline-{name}.svg").write_text(timeline(theme), encoding="utf-8")
