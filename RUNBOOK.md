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
It names a `format` (`ab`, `landing`, `before-after`, `columns` or `monitor`), an `industry`, a made-up `brand` and a `slug`.
Post folder: `posts/<YYYY-MM-DD>-<format>-<slug>` (date = today, Africa/Johannesburg).

Prebuilt items: if the item has `"prebuilt": "<folder>"`, copy that folder's files into the post folder, re-render with `tools/render.py`, look at the result, and continue from step 6. Do not redesign it.

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
- **columns** and **monitor** both start from `site.html`: a full 1280px-wide desktop homepage for the business, with the same section rhythm as `posts/_examples/04-columns/site.html` (photo hero with two-line headline + accent second line + glass booking/quote bar + stat row; about statement with grey continuation + photo + facts list; 3 service/product cards with prices, middle one dark with a chip; dark features grid with one accent stat tile; 4-step "how it works" list beside a photo; photo CTA band with WhatsApp; footer "Concept by CAAS Studios"). Pick ONE accent colour that suits the industry. Copy `showcase.css`. Slides crop `site.jpg` with `background-size: <card width>px auto` and `background-position: 0 -<section offsetTop × card width/1280>px`; measure section offsets with Playwright (`section.offsetTop`) rather than guessing, and never let a crop end on a sliver of the next section. Swap every blurred background photo to this item's hero photo. Needs 6–7 photos (hero, about, 3 cards, steps, CTA).
  - **columns** → `posts/_examples/04-columns/` (3-slide carousel): (1) overview: back column = lower half of the page, front column = top of the page, "CAAS STUDIOS · Website concept" label + "Swipe" pill; (2) close-up of the cards section with a short headline about the idea (accent on the second half); (3) "Want a site like this?" + close-up of the steps section + DM/WhatsApp CTA + 3 chips.
  - **monitor** → `posts/_examples/05-monitor/` (single image): "© 2026 CAAS Studios" / "@prosper.builds" top row, big two-line title "<Industry>" (white) + "Website" (ghosted white ~32%), the site hero on the desktop monitor (`.screen` crops site.jpg from the top), white base band with "UI/UX Design" + "Concept for an invented <business type>" and the DM "SITE" pill, blurred hero photo behind. Keep the industry title to one line at 118px (≈14 characters; shrink the font if longer). Only the hero shows, but still build the full site.html so it can be reused.
- **Inspiration from siteinspire (every other columns/monitor post):** before designing site.html, open `https://www.siteinspire.com/websites` (or a category such as `/websites/categories/minimal`), pick ONE featured site in a fitting industry or style, open its siteinspire page and the live site, and borrow only its *design language*: section rhythm, type mood (e.g. editorial serif + small sans labels), whitespace, colour temperature and UI details. Never copy its name, logo, wording, photos or exact layout. Write all content fresh for the invented business. Add `"inspiration": "<siteinspire URL>"` to the queue item. Available local fonts: Schibsted Grotesk (sans) and Instrument Serif (editorial serif, incl. italic). Reference: `posts/_inspiration/2026-10-09-bakery/`.
- Link `../../brand/ui.css` (adjust the relative path for the folder depth) and `stock/<slug>/…` photos with relative paths. Fonts come from `brand/fonts.css` (local files).
- Industry-fitting copy, real South African prices in Rand, services that business actually sells. Ratings/review counts may appear inside the mockup UI (it is a concept site); never in the caption as facts.
- Footer sig: "CAAS STUDIOS" left; right side per format as in the references.
- Concept number NN for landing posts = number of `landing` posts already posted + 2.

## 5. Render and check
`python3 tools/render.py posts/<id>` then LOOK at the JPG (Read tool). For columns/monitor, render.py first renders `site.html` to `site.jpg`, then the slides — look at site.jpg (downscaled) AND every slide. Fix and re-render if anything is clipped, overlapping, misspelled, unreadable over a photo, or leaves a big empty area.

## 6. Caption
Write `caption.txt`: a hook line (for ab: ask people to comment A or B; for before-after: "Which one would you book?"; for columns: "Swipe through a full homepage concept for …"; for monitor: "Would you book through this homepage?"), 1–2 short lines on the design idea, the CTA ("Want a site like this? DM us \"SITE\" or WhatsApp +27 665 989 442."), then 6–9 hashtags (always #caasstudios #webdesign #smallbusinesssa #capetown, plus industry/topic tags). Mention it's a concept for an invented business.

## 7. Commit and push
Mark the queue item `"status": "posted"` with `"post": "posts/<id>"` and move it to `done`.
```bash
git add -A && git commit -m "Post <id>" && git push origin HEAD:main
```
Push MUST succeed before publishing — Metricool downloads the image from GitHub.

## 8. Publish via Metricool
- Brand (blogId): `7037975`, network `instagram`, timezone `Africa/Johannesburg`.
- Media URL: `https://raw.githubusercontent.com/nkunzi05/caas-social/main/posts/<id>/slide1.jpg` — confirm it returns HTTP 200 first (wait up to ~2 minutes after pushing).
- Columns posts are carousels: `media` = the 3 URLs slide1.jpg … slide3.jpg in order (check all three return 200). Instagram type stays `POST`.
- `createScheduledPost` with `date` = now + 5 minutes, `publicationDate` = same in Africa/Johannesburg, `text` = caption, `media` = [URL], `providers` = `[{"network":"instagram"}]`, `instagramData` = `{"type":"POST"}`, `autoPublish: true`, `draft: false`.

## 9. Report
Send Prosper a short message: what was posted, the image, and anything that went wrong.
If the queue has fewer than 6 `todo` items left, add 12 new ones: new industries and made-up brands, formats rotating ab → landing → before-after → columns, then ab → landing → before-after → monitor.
