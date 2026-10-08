# CAAS Studios — daily Instagram post runbook

Each run publishes EXACTLY ONE post to Instagram (@prosper.builds) through Metricool.
Prosper approved fully automatic posting. Follow these steps in order.

## 1. Setup
```bash
git clone https://github.com/nkunzi05/caas-social && cd caas-social
pip install --break-system-packages playwright pillow && python3 -m playwright install chromium
```

## 2. Pick the item
Open `content/queue.json`. Take the FIRST entry in `queue` with `"status": "todo"`. Only that one entry — never more than one post per run.
It names a `format` (`ab`, `landing` or `before-after`), an `industry`, a made-up `brand` and a `slug`.
Post folder: `posts/<YYYY-MM-DD>-<format>-<slug>` (date = today, Africa/Johannesburg).

Duplicate guard: the queue is the source of truth. An item marked `"posted"` is never posted again. If this item's folder already exists with pushed JPGs but it is still `"todo"` (a previous run failed midway), reuse it and continue from step 6.

## 3. Get stock photos (free Unsplash only)
The workspace cannot download from Unsplash directly; a GitHub workflow does it.
1. `WebFetch https://unsplash.com/s/photos/<industry-term>?license=free` and pick 4–6 photos that fit (people at work, the space, the product). Skip photos with visible brand logos, watermarks, face masks, or anything dated or low quality.
2. For each pick, `WebFetch` its photo page and get the base `og:image` URL (`https://images.unsplash.com/photo-…`, cut at `?`). Use it ONLY if the page says "Free to use under the Unsplash License" (never Unsplash+).
3. Append lines to `stock/requests.txt`: `<slug>/<name>.jpg <images.unsplash.com URL> <unsplash page URL>`. Reuse photos already in `stock/<slug>/` when the industry has a set.
4. Commit and push. The "Fetch stock photos" workflow downloads them into `stock/<slug>/` within ~1–2 minutes. Poll with `git pull` every 15 s for up to 5 minutes. If photos don't arrive, check the latest run at `https://api.github.com/repos/nkunzi05/caas-social/actions/runs?per_page=1`; if it failed, try different photos once, then stop and report.
5. Look at the photos (make a contact sheet and Read it) before designing.

## 4. Design the slide (single 1080×1350 slide)
Copy the approved reference for the format and adapt it to the industry. Match its quality and structure exactly:
- **ab** → `posts/_examples/01-ab/slide1.html`: eyebrow `<INDUSTRY> BOOKING/ORDERING`, a question headline ("Which … gets more clients?"), two versions of the same real UI element for this business (A: clean light card with photo on top; B: photo-led dark card with glass panel). Both must look good; B is the bolder one. A/B circles under the cards, footer "Comment A or B ↓".
- **landing** → `posts/_examples/02-landing/slide1.html`: "Concept NN — <Industry> website" eyebrow, full homepage mockup: nav + logo + CTA pill, big photo hero with a two-line headline (second line in a warm accent), short subline, CTA, rating line, a floating glass info card, then the lower row (about block + two dark photo tiles with "Learn more").
- **before-after** → `posts/_examples/03-before-after/slide1.html`: "Which one would you book/hire/visit?", two phones. BEFORE = a believable average template site (plain header, dim stock photo with a generic "Welcome to …" line, an "About Us" text block, grey service boxes, "contact us" link, "Read More" button, dated © footer) — plausible but forgettable, never cartoonish. AFTER = photo-led redesign with chip, bold headline, one clear CTA + WhatsApp button. The after must clearly win.
- Link `../../brand/ui.css` (adjust the relative path for the folder depth) and `stock/<slug>/…` photos with relative paths. Fonts come from `brand/fonts.css` (local files).
- Industry-fitting copy, real South African prices in Rand, services that business actually sells. Ratings/review counts may appear inside the mockup UI (it is a concept site); never in the caption as facts.
- Footer sig: "CAAS STUDIOS" left; right side per format as in the references.
- Concept number NN for landing posts = number of `landing` posts already posted + 2.

## 5. Render and check
`python3 tools/render.py posts/<id>` then LOOK at the JPG (Read tool). Fix and re-render if anything is clipped, overlapping, misspelled, unreadable over a photo, or leaves a big empty area.

## 6. Caption
Write `caption.txt`: a hook line (for ab: ask people to comment A or B; for before-after: "Which one would you book?"), 1–2 short lines on the design idea, the CTA ("Want a site like this? DM us \"SITE\" or WhatsApp +27 665 989 442."), then 6–9 hashtags (always #caasstudios #webdesign #smallbusinesssa #capetown, plus industry/topic tags). Mention it's a concept for an invented business.

## 7. Commit and push
Mark the queue item `"status": "posted"` with `"post": "posts/<id>"` and move it to `done`.
```bash
git add -A && git commit -m "Post <id>" && git push origin HEAD:main
```
Push MUST succeed before publishing — Metricool downloads the image from GitHub.

## 8. Publish via Metricool
- Brand (blogId): `7037975`, network `instagram`, timezone `Africa/Johannesburg`.
- Media URL: `https://raw.githubusercontent.com/nkunzi05/caas-social/main/posts/<id>/slide1.jpg` — confirm it returns HTTP 200 first (wait up to ~2 minutes after pushing).
- `createScheduledPost` with `date` = now + 5 minutes, `publicationDate` = same in Africa/Johannesburg, `text` = caption, `media` = [URL], `providers` = `[{"network":"instagram"}]`, `instagramData` = `{"type":"POST"}`, `autoPublish: true`, `draft: false`.

## 9. Report
Send Prosper a short message: what was posted, the image, and anything that went wrong.
If the queue has fewer than 6 `todo` items left, add 12 new ones: new industries and made-up brands, formats rotating ab → landing → before-after.
