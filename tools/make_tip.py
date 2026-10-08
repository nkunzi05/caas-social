"""Build a 2-slide tip carousel from a JSON spec.

Usage:  python3 tools/make_tip.py posts/<post-id>/spec.json
Spec:   {"number": 1, "headline": "...", "points": [["Title", "One line"], ...3 items], "theme": "ink"|"paper"}
Writes slide1.html (the tip) and slide2.html (the call to action) next to the spec.
"""
import html
import json
import sys
from pathlib import Path

CSS = "../../brand/brand.css"


def esc(s):
    return html.escape(s, quote=True)


def tip_slide(spec):
    theme = spec.get("theme", "ink")
    num = f"{int(spec['number']):02d}"
    points = "".join(
        f"""
      <div class="pt">
        <div class="n">{i + 1:02d}</div>
        <div><div class="t">{esc(t)}</div><div class="d">{esc(d)}</div></div>
      </div>"""
        for i, (t, d) in enumerate(spec["points"])
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Tip {num}</title>
<link rel="stylesheet" href="{CSS}">
<style>
  .big {{ font-size: 220px; font-weight: 800; letter-spacing: -0.06em; line-height: 0.8; color: var(--signal); }}
  .paper .big {{ color: var(--ink); -webkit-text-stroke: 0; }}
  .head {{ font-size: 76px; margin-top: 36px; max-width: 900px; }}
  .pts {{ display: flex; flex-direction: column; margin-top: 64px; }}
  .pt {{ display: flex; gap: 32px; padding: 30px 0; border-top: 1px solid var(--line); }}
  .paper .pt {{ border-top-color: rgba(7,11,20,0.18); }}
  .n {{ font-size: 20px; font-weight: 700; width: 48px; padding-top: 8px; color: var(--signal); }}
  .paper .n {{ color: var(--ink); }}
  .t {{ font-size: 36px; font-weight: 700; letter-spacing: -0.02em; }}
  .d {{ font-size: 24px; line-height: 1.35; margin-top: 8px; color: var(--soft); }}
  .paper .d {{ color: #3a4150; }}
</style></head>
<body><div class="slide {theme}">
  <div class="topbar"><div class="wordmark">CAAS STUDIOS</div><div class="kicker">Website tip {num}</div></div>
  <div style="margin-top: 72px" class="big">#{num}</div>
  <h1 class="display head">{esc(spec['headline'])}</h1>
  <div class="pts">{points}
  </div>
  <div class="footer"><span>Save this for later</span><strong>Swipe &rarr;</strong></div>
</div></body></html>
"""


def cta_slide(spec):
    line = esc(spec.get("cta_line", "Want a website that does this for you?"))
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Call to action</title>
<link rel="stylesheet" href="{CSS}">
<style>
  .head {{ font-size: 112px; margin-top: auto; }}
  .sub {{ font-size: 30px; line-height: 1.3; font-weight: 500; margin: 36px 0 0; max-width: 780px; }}
  .btns {{ display: flex; gap: 16px; flex-wrap: wrap; margin-top: 140px; }}
  .base {{ display: flex; justify-content: space-between; font-size: 20px; font-weight: 600; padding-top: 24px; margin-top: 28px; border-top: 2px solid var(--ink); }}
</style></head>
<body><div class="slide signal">
  <div class="topbar"><div class="wordmark">CAAS STUDIOS</div><div class="kicker">Your turn</div></div>
  <h2 class="display head">{line}</h2>
  <p class="sub">Clean, fast websites for small businesses. Designed around your brand.</p>
  <div class="btns">
    <span class="pill solid">DM us &ldquo;SITE&rdquo;</span>
    <span class="pill">WhatsApp +27 665 989 442</span>
  </div>
  <div class="base"><span>caas-studios.vercel.app</span><span>Cape Town</span></div>
</div></body></html>
"""


if __name__ == "__main__":
    spec_path = Path(sys.argv[1])
    spec = json.loads(spec_path.read_text())
    (spec_path.parent / "slide1.html").write_text(tip_slide(spec))
    (spec_path.parent / "slide2.html").write_text(cta_slide(spec))
    print("wrote", spec_path.parent / "slide1.html", spec_path.parent / "slide2.html")
