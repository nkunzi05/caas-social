"""Turn a rendered post into a 1080x1920 Instagram Reel (MP4, ~13 s, 30 fps).

Usage:  python3 tools/reel.py posts/<post-id> --hook "Would you order coffee from this site?" [--seconds 20]
        [--bg stock/<slug>/<photo>.jpg]   background photo (blurred); default = first stock photo the slide uses
Output: posts/<post-id>/reel.mp4 (13 s for a slide, 20 s for a full-site scroll; + reel-cover.jpg, the first frame, to look at)

How it moves:
  * posts with site.html (columns / monitor): the full homepage scrolls top -> bottom inside a browser card.
  * single-slide posts (ab / landing / before-after): the slide is shown whole, the camera zooms (1.45x) to
    the top-left headline, drops to the lower row, pans across it, then pulls back out.
  The last ~2 s fade to an end card: "Want a site like this? DM "SITE"".
Needs: playwright, pillow, ffmpeg.
"""
import argparse
import asyncio
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.async_api import async_playwright

W, H, FPS = 1080, 1920, 30
SECONDS = 13.0                                         # single-slide reels; site scrolls default to 20 s
CARD_X, CARD_Y, CARD_W, CARD_H = 100, 420, 880, 1100   # 4:5 like the feed slide; inside the Reels safe zone
ROOT = Path(__file__).resolve().parent.parent


def ease(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


LAYER_HTML = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{fonts}">
<style>
  html,body {{ margin:0; width:{W}px; height:{H}px; overflow:hidden; background:transparent;
    font-family:'Schibsted Grotesk',sans-serif; color:#fff; }}
  .bg {{ position:absolute; inset:-60px; background:#111 url('{bg}') center/cover; filter:blur(38px) brightness(.55) saturate(1.1); }}
  .tint {{ position:absolute; inset:0; background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.05) 40%,rgba(0,0,0,.45)); }}
  .hook {{ position:absolute; left:80px; right:80px; top:200px; height:190px; display:flex; align-items:center; justify-content:center;
    text-align:center; font-size:{hook_size}px; line-height:1.04; font-weight:800; letter-spacing:-.035em; text-wrap:balance; }}
  .card {{ position:absolute; left:{CX}px; top:{CY}px; width:{CW}px; height:{CH}px; border-radius:34px;
    box-shadow:0 30px 90px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.12); background:#000; }}
  .sig {{ position:absolute; left:100px; right:100px; top:1556px; display:flex; justify-content:space-between;
    font-size:24px; font-weight:600; color:rgba(255,255,255,.78); }}
  .sig b {{ color:#fff; font-weight:800; letter-spacing:.14em; }}
  .end {{ position:absolute; inset:0; background:rgba(8,8,10,.72); display:flex; flex-direction:column; align-items:center;
    justify-content:center; text-align:center; gap:34px; }}
  .end h2 {{ margin:0; font-size:96px; line-height:1; font-weight:800; letter-spacing:-.04em; }}
  .end .pill {{ background:#fff; color:#0E1220; border-radius:999px; padding:26px 54px; font-size:46px; font-weight:800; }}
  .end p {{ margin:0; font-size:32px; color:rgba(255,255,255,.8); font-weight:500; }}
</style></head><body>{body}</body></html>"""


async def build_layers(folder: Path, hook: str, bg: Path, tmp: Path):
    fonts = (ROOT / "brand/fonts.css").as_uri()
    hook_size = 76 if len(hook) <= 34 else 64 if len(hook) <= 48 else 54
    common = dict(fonts=fonts, W=W, H=H, bg=bg.resolve().as_uri(), hook_size=hook_size,
                  CX=CARD_X, CY=CARD_Y, CW=CARD_W, CH=CARD_H)
    base_body = ('<div class="bg"></div><div class="tint"></div>'
                 f'<div class="hook">{hook}</div><div class="card"></div>'
                 '<div class="sig"><b>CAAS STUDIOS</b><span>@prosper.builds</span></div>')
    end_body = ('<div class="end"><h2>Want a site<br>like this?</h2>'
                '<div class="pill">DM &ldquo;SITE&rdquo;</div><p>@prosper.builds &middot; CAAS Studios</p></div>')
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})
        for name, body in (("base", base_body), ("end", end_body)):
            f = tmp / f"{name}.html"
            f.write_text(LAYER_HTML.format(body=body, **common))
            await pg.goto(f.as_uri())
            await pg.wait_for_load_state("networkidle")
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(tmp / f"{name}.png"), omit_background=True)
        # Hi-res source for the zoom: the slide at 2x
        content = None
        if not (folder / "site.jpg").exists():
            hp = await b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
            await hp.goto((folder / "slide1.html").resolve().as_uri())
            await hp.wait_for_load_state("networkidle")
            await hp.wait_for_timeout(800)
            content = tmp / "slide2x.png"
            await hp.screenshot(path=str(content), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        await b.close()
    return content


def slide_camera(t: float):
    """Return (cx, cy, zoom) in 0..1 slide coords for single-slide posts."""
    keys = [  # time, cx, cy, zoom
        (0.0, .5, .5, 1.0), (1.4, .5, .5, 1.0),
        (3.0, .42, .33, 1.45), (4.6, .42, .33, 1.45),   # top-left: headline / question
        (6.4, .36, .73, 1.45),                          # drop to the lower row, left side
        (8.8, .64, .73, 1.45), (9.4, .64, .73, 1.45),   # pan across it
        (10.6, .5, .5, 1.0), (SECONDS, .5, .5, 1.0)]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t <= t1:
            k = ease((t - t0) / (t1 - t0)) if t1 > t0 else 1
            return tuple(x + (y - x) * k for x, y in zip(a, b))
    return keys[-1][1:]


def render(folder: Path, hook: str, bg: Path, seconds: float = 0):
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        slide2x = asyncio.run(build_layers(folder, hook, bg, tmp))
        base = Image.open(tmp / "base.png").convert("RGB")
        end = Image.open(tmp / "end.png").convert("RGBA")
        mask = Image.new("L", (CARD_W, CARD_H), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, CARD_W - 1, CARD_H - 1), 34, fill=255)

        site = folder / "site.jpg"
        seconds = seconds or (20.0 if site.exists() else SECONDS)
        end_start = seconds - 2.2                       # end card fades in from here
        if site.exists():
            src = Image.open(site).convert("RGB")
            src = src.resize((CARD_W, round(src.height * CARD_W / src.width)), Image.LANCZOS)
            travel = max(src.height - CARD_H, 0)
        else:
            src = Image.open(slide2x).convert("RGB")
            sw, sh = src.size

        out = folder / "reel.mp4"
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", str(FPS), "-i", "-", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
             "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
             "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "128k", str(out)],
            stdin=subprocess.PIPE)
        n = int(seconds * FPS)
        for i in range(n):
            t = i / FPS
            if site.exists():
                k = ease((t - 1.5) / (end_start - 0.8 - 1.5))
                y = round(travel * k)
                card = src.crop((0, y, CARD_W, y + CARD_H))
            else:
                cx, cy, z = slide_camera(t)
                cw, ch = sw / z, sh / z
                x0 = min(max(cx * sw - cw / 2, 0), sw - cw)
                y0 = min(max(cy * sh - ch / 2, 0), sh - ch)
                card = src.resize((CARD_W, CARD_H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
            frame = base.copy()
            frame.paste(card, (CARD_X, CARD_Y), mask)
            a = ease((t - end_start) / 0.6)
            if a > 0:
                e = end.copy()
                e.putalpha(e.getchannel("A").point(lambda v: int(v * a)))
                frame.paste(e, (0, 0), e)
            if i == int(0.8 * FPS):
                frame.save(folder / "reel-cover.jpg", quality=88)
            ff.stdin.write(frame.tobytes())
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit("ffmpeg failed")
        print(out, f"{out.stat().st_size / 1e6:.1f} MB")


def default_bg(folder: Path) -> Path:
    for f in ("slide1.html", "site.html"):
        p = folder / f
        if p.exists():
            m = re.findall(r"stock/[\w\-/]+\.jpg", p.read_text())
            if m:
                return ROOT / m[0]
    sys.exit("No --bg given and no stock photo found in the slide")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--hook", required=True)
    ap.add_argument("--bg")
    ap.add_argument("--seconds", type=float, default=0, help="length; default 13 (slide) or 20 (site scroll)")
    a = ap.parse_args()
    folder = Path(a.folder)
    render(folder, a.hook, Path(a.bg) if a.bg else default_bg(folder), a.seconds)
