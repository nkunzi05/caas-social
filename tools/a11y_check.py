"""WCAG 2.1 AA contrast + size check for a post's site.html and slide*.html.

Usage:  python3 tools/a11y_check.py posts/<id>
Checks every visible text element whose background is a solid colour (walks up the
ancestors to the first non-transparent background). Text that sits on a photo or a
gradient is listed separately as "check by eye" (look at it in the render).
Also flags: text under 13px, buttons/pills under 44px tall, <img> without alt.
Exit code 1 if any hard failure, so a run can't miss it.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

JS = r"""
() => {
  const parse = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(s => parseFloat(s)); return {r:p[0], g:p[1], b:p[2], a: p.length > 3 ? p[3] : 1}; };
  const out = [];
  const seen = new Set();
  const photos = [...document.querySelectorAll('body *')].filter(e => { const s = getComputedStyle(e); return s.backgroundImage && s.backgroundImage !== 'none' && e.getBoundingClientRect().width > 40; });
  for (const el of document.querySelectorAll('body *')) {
    const txt = [...el.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent.trim()).join(' ').trim();
    if (!txt) continue;
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    if (cs.visibility === 'hidden' || cs.display === 'none' || r.width === 0 || parseFloat(cs.opacity) === 0) continue;
    const fg = parse(cs.color); let bg = null, photo = false, node = el;
    while (node && node !== document.documentElement) {
      const s = getComputedStyle(node);
      if (s.backgroundImage && s.backgroundImage !== 'none') { photo = true; break; }
      const b = parse(s.backgroundColor);
      if (b && b.a >= 0.9) { bg = b; break; }
      if (b && b.a > 0.05) { photo = true; break; }   // glass / translucent panel
      node = node.parentElement;
    }
    // a photo layer painted above that background and overlapping the text (hero .ph pattern)
    if (!photo && bg) {
      for (const ph of photos) {
        if (ph === el || !node.contains(ph)) continue;
        const pr = ph.getBoundingClientRect();
        if (r.left < pr.right && r.right > pr.left && r.top < pr.bottom && r.bottom > pr.top) { photo = true; break; }
      }
    }
    const key = txt.slice(0, 40) + '|' + cs.color;
    if (seen.has(key)) continue; seen.add(key);
    out.push({txt: txt.slice(0, 48), fg, bg, photo, size: parseFloat(cs.fontSize), weight: parseInt(cs.fontWeight),
              tag: el.tagName.toLowerCase(), cls: el.className && el.className.baseVal === undefined ? el.className : ''});
  }
  const pills = [...document.querySelectorAll('a, button, .pill')].map(e => ({t: e.textContent.trim().slice(0, 30), h: e.getBoundingClientRect().height}));
  const imgs = [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length;
  return {out, pills, imgs};
}
"""


def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c["r"]) + 0.7152 * ch(c["g"]) + 0.0722 * ch(c["b"])


def blend(fg, bg):
    a = fg["a"]
    return {k: fg[k] * a + bg[k] * (1 - a) for k in "rgb"} | {"a": 1}


def ratio(fg, bg):
    f = blend(fg, bg)
    l1, l2 = sorted([lum(f), lum(bg)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main(folder: Path):
    pages = [p for p in [folder / "site.html", *sorted(folder.glob("slide*.html"))] if p.exists()]
    fails, eye = 0, []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for html in pages:
            w = 1280 if html.name == "site.html" else 1080
            pg = b.new_page(viewport={"width": w, "height": 900})
            pg.goto(html.resolve().as_uri())
            pg.wait_for_timeout(600)
            res = pg.evaluate(JS)
            print(f"\n== {html.name}")
            for t in res["out"]:
                large = t["size"] >= 24 or (t["size"] >= 18.66 and t["weight"] >= 700)
                need = 3.0 if large else 4.5
                if t["size"] < 13 and html.name == "site.html":
                    print(f"  SMALL  {t['size']:.0f}px  '{t['txt']}'")
                if t["photo"] or not t["bg"]:
                    eye.append(f"{html.name}: '{t['txt']}'")
                    continue
                r = ratio(t["fg"], t["bg"])
                if r < need:
                    fails += 1
                    print(f"  FAIL   {r:4.2f}:1 (needs {need}) {t['size']:.0f}px '{t['txt']}'")
            for pl in res["pills"]:
                if 0 < pl["h"] < 44 and html.name == "site.html":
                    print(f"  TARGET {pl['h']:.0f}px tall (min 44) '{pl['t']}'")
            if res["imgs"]:
                print(f"  ALT    {res['imgs']} <img> without alt")
            pg.close()
        b.close()
    print(f"\nText on photos / glass, check by eye in the render ({len(eye)}):")
    for e in eye[:40]:
        print("  -", e)
    print(f"\n{fails} contrast failure(s).")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
