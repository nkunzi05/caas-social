"""Side-by-side sheet of the last N posted sites (+ the new one) to check they don't look alike.

Usage:  python3 tools/recent_sites.py posts/<new-id> [N=4] [out.jpg]
Writes a contact sheet (default: <scratch>/recent_sites.jpg, or the given path) with the
new site.jpg on the far right. Read it during the design critique (RUNBOOK step 5a).
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def main():
    new = Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    out = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("recent_sites.jpg")
    done = json.load(open("content/queue.json"))["done"]
    prev = [Path(d["post"]) for d in done if d.get("post") and Path(d["post"]) != new
            and (Path(d["post"]) / "site.jpg").exists()][-n:]
    cols = prev + [new]
    W = 300
    ims = []
    for c in cols:
        im = Image.open(c / "site.jpg")
        ims.append(im.resize((W, int(im.height * W / im.width))))
    H = max(i.height for i in ims) + 34
    sheet = Image.new("RGB", (len(ims) * (W + 12), H), "white")
    d = ImageDraw.Draw(sheet)
    for k, (c, im) in enumerate(zip(cols, ims)):
        x = k * (W + 12)
        sheet.paste(im, (x, 34))
        meta = next((q for q in done if q.get("post") == str(c)), {})
        label = c.name[11:40] + ("  <- NEW" if c == new else f"  [{meta.get('layout', '?')}]")
        d.text((x + 2, 10), label, fill="red" if c == new else "black")
    sheet.save(out, quality=85)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
