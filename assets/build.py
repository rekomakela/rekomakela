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

TILES = [  # (since, skill lines, proof)
    ("Since 2018", ("SEO and", "search demand"), "Affiliate sites, Terveystalo"),
    ("Since 2021", ("CRO and", "A/B testing"), "Opening-hours test, 6 cities"),
    ("Since 2021", ("Analytics and", "reporting"), "Reports with next steps"),
    ("Since 2024", ("AI-assisted", "workflows"), "Searchint, Copilot agents"),
]
TAGLINE = "SEO, CRO and analytics, with AI-assisted workflows · Helsinki"

# Hintapiste.fi daily Google Search impressions, 12 Aug to 9 Oct 2026, read off the
# Search Console performance chart (sums to 5,293; Search Console total 5.28k).
GROWTH_START = (2026, 8, 12)
GROWTH = [0, 0, 0, 17, 19, 12, 23, 26, 14, 17, 19, 24, 30, 35, 40, 38, 31, 51, 63, 101, 68, 65, 75, 63,
          68, 75, 82, 44, 52, 59, 119, 59, 54, 101, 126, 147, 155, 117, 140, 113, 131, 117, 141, 167,
          112, 122, 133, 108, 133, 87, 134, 117, 99, 169, 140, 145, 171, 288, 438]
GROWTH_TOTALS = "5,280 impressions · 42 clicks · average position 22.3 · last 3 months"

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
        text(0, 72, TAGLINE, 17, c["muted"]),
    ]
    gap, top, th = 12, 100, 124
    tw = (W - gap * 3) / 4
    for i, (since, lines, proof) in enumerate(TILES):
        x = i * (tw + gap)
        body.append(f'<rect x="{x + .5}" y="{top + .5}" width="{tw - 1}" height="{th - 1}" rx="10" fill="{c["tile"]}" stroke="{c["line"]}"/>')
        body.append(text(x + 16, top + 28, since, 12, c["accent"], 600))
        body.append(text(x + 16, top + 54, lines[0], 19, c["fg"], 600))
        body.append(text(x + 16, top + 78, lines[1], 19, c["fg"], 600))
        body.append(text(x + 16, top + 106, proof, 13, c["muted"]))
    return svg(top + th + 2, body, f"Reko Mäkelä. {TAGLINE}. "
               + "; ".join(f"{' '.join(l)}, {s.lower()}: {p}" for s, l, p in TILES))


def growth(c):
    import datetime
    start = datetime.date(*GROWTH_START)
    left, right, top, bottom, ymax = 36, W - 70, 70, 250, 450
    n = len(GROWTH)
    sx = lambda i: left + i / (n - 1) * (right - left)
    sy = lambda v: bottom - v / ymax * (bottom - top)
    body = [
        text(0, 22, "Hintapiste.fi in Google Search: daily impressions", 18, c["fg"], 600),
        text(0, 46, GROWTH_TOTALS, 13, c["muted"]),
    ]
    for v in (0, 150, 300, 450):
        body.append(f'<line x1="{left}" y1="{sy(v)}" x2="{right}" y2="{sy(v)}" stroke="{c["line"]}"/>')
        body.append(text(left - 8, sy(v) + 4, str(v), 11, c["muted"], anchor="end"))
    for i in range(n):
        day = start + datetime.timedelta(days=i)
        if day.day in (1, 15):
            body.append(text(sx(i), bottom + 20, f"{day.day} {day.strftime('%b')}", 11, c["muted"], anchor="middle"))
    line = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(GROWTH))
    body.append(f'<polygon points="{sx(0)},{bottom} {line} {sx(n - 1)},{bottom}" fill="{c["accent"]}" fill-opacity="0.15"/>')
    body.append(f'<polyline points="{line}" fill="none" stroke="{c["accent"]}" stroke-width="2.5" stroke-linejoin="round"/>')
    end = start + datetime.timedelta(days=n - 1)
    body.append(f'<circle cx="{sx(n - 1)}" cy="{sy(GROWTH[-1])}" r="4.5" fill="{c["accent"]}"/>')
    body.append(text(sx(n - 1) + 10, sy(GROWTH[-1]) + 5, str(GROWTH[-1]), 15, c["fg"], 600))
    body.append(text(sx(n - 1) + 10, sy(GROWTH[-1]) + 22, f"{end.day} {end.strftime('%b')}", 11, c["muted"]))
    title = (f"Hintapiste.fi daily Google Search impressions grew from 0 on {start.day} {start.strftime('%b')} "
             f"to {GROWTH[-1]} on {end.day} {end.strftime('%b')} {end.year}. {GROWTH_TOTALS}.")
    return svg(bottom + 30, body, title)


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
    (OUT / f"growth-{name}.svg").write_text(growth(theme), encoding="utf-8")
