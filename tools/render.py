"""Render every slide*.html in a post folder to 1080x1350 JPGs.

Usage:  python3 tools/render.py posts/<post-id>
Output: posts/<post-id>/slide1.jpg, slide2.jpg, ...
Needs:  pip install playwright pillow && python3 -m playwright install chromium
"""
import asyncio
import sys
from pathlib import Path

from PIL import Image
from playwright.async_api import async_playwright

W, H = 1080, 1350


async def render(folder: Path):
    slides = sorted(folder.glob("slide*.html"))
    if not slides and not (folder / "site.html").exists():
        sys.exit(f"No slide*.html files in {folder}")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        site = folder / "site.html"
        if site.exists():
            # "showcase" posts: render the full homepage mockup first; the slides crop site.jpg
            sp = await browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=2)
            await sp.goto(site.resolve().as_uri())
            await sp.wait_for_load_state("networkidle")
            await sp.wait_for_timeout(800)
            tmp = folder / "site.png"
            await sp.screenshot(path=str(tmp), full_page=True)
            im = Image.open(tmp).convert("RGB")
            im.save(folder / "site.jpg", quality=90, optimize=True)
            tmp.unlink()
            print(folder / "site.jpg", f"{im.width // 2}x{im.height // 2} css px")
            await sp.close()
        page = await browser.new_page(viewport={"width": W, "height": H})
        for html in slides:
            png = html.with_suffix(".png")
            await page.goto(html.resolve().as_uri())
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(800)  # let web fonts settle
            await page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": W, "height": H})
            jpg = html.with_suffix(".jpg")
            Image.open(png).convert("RGB").save(jpg, quality=88, optimize=True, progressive=True)
            png.unlink()
            print(jpg)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(render(Path(sys.argv[1])))
