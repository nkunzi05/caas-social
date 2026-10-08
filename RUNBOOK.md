# CAAS Studios — daily Instagram post runbook

Each weekday run publishes ONE post to Instagram (@prosper.builds) through Metricool.
Prosper approved fully automatic posting. Follow these steps in order.

## 1. Setup
```bash
git clone https://github.com/nkunzi05/caas-social && cd caas-social
pip install --break-system-packages playwright pillow && python3 -m playwright install chromium
```

## 2. Pick today's item
Open `content/queue.json`. Take the FIRST entry in `queue` with `"status": "todo"`.
Post folder: `posts/<YYYY-MM-DD>-<type>-<slug or tip number>` (date = today, Africa/Johannesburg).
Duplicate guard: the queue is the source of truth. An item marked `"posted"` is never posted again. If the folder for THIS item already exists with pushed JPGs but the item is still `"todo"` (a previous run failed midway), reuse it and continue from step 5. Other posts from the same day don't matter — more than one post per day is allowed.

## 3a. Tip post (`"type": "tip"`)
1. Write `spec.json` in the post folder:
   `{"number": N, "headline": "<from queue>", "theme": "ink" or "paper" (alternate), "points": [[title, one line], ×3]}`
   - Titles ≤ 5 words, lines ≤ 12 words. Practical, specific advice for small business owners. No invented statistics.
2. `python3 tools/make_tip.py posts/<id>/spec.json`

## 3b. Concept carousel (`"type": "concept"`)
Hand-write 3 slides as `slide1.html`, `slide2.html`, `slide3.html`, using `posts/2026-10-08-concept-orven/` as the reference for quality and structure:
- **slide1 — cover:** paper (#D9DBE1) background, CAAS STUDIOS wordmark + "Concept NN — <industry>", a punchy 2-line hook headline (~84px, 800 weight), and a big rounded card (radius 28px) showing the concept brand's website homepage: logo + nav, a giant hero word, and a 3–4 item grid of their services/products drawn with HTML/CSS shapes and inline SVG (no photos, no emoji, no real brands). Footer: "Concept site · not a real client" and "Swipe →".
- **slide2 — behind the design:** ink background, headline about the design idea, a large featured visual on the left, and TYPE / COLOUR / LAYOUT notes on the right with real colour swatches from the concept.
- **slide3 — CTA:** copy `slide3.html` from the ORVEN post and change only the headline if it helps.
- Each concept gets its own palette and personality fitting the industry, but keep the CAAS frame (wordmark, Schibsted Grotesk, footer) identical.
- Link `../../brand/brand.css` or include the Google Fonts link for Schibsted Grotesk. Every slide is exactly 1080×1350.
- Concept number NN = number of concept posts already done + 1.

## 4. Render and check
`python3 tools/render.py posts/<id>` then LOOK at every JPG (Read tool). Fix and re-render if anything is clipped, overlapping, empty-looking, or misspelled.

## 5. Caption
Write `caption.txt` in the post folder: hook line, 1–2 short lines of value, a CTA ("DM us \"SITE\" or WhatsApp +27 665 989 442"), then 6–9 hashtags (always #caasstudios #webdesign #smallbusinesssa, plus topic/industry and #capetown). Light emoji use is fine in captions.

## 6. Commit and push
Mark the queue item `"status": "posted"` with `"post": "posts/<id>"`, move it to `done`.
```bash
git add -A && git commit -m "Post <id>" && git push origin HEAD:main
```
Push MUST succeed before publishing — Metricool downloads the images from GitHub.

## 7. Publish via Metricool
- Brand (blogId): `7037975`, network `instagram`, timezone `Africa/Johannesburg`.
- Media URLs (in slide order): `https://raw.githubusercontent.com/nkunzi05/caas-social/main/posts/<id>/slide1.jpg`, …
- First confirm each URL returns HTTP 200 (WebFetch or curl); wait up to ~2 minutes after pushing.
- `createScheduledPost` with `date` = now + 5 minutes, `publicationDate` = same in Africa/Johannesburg, `text` = caption, `media` = URLs, `providers` = `[{"network":"instagram"}]`, `instagramData` = `{"type":"POST"}`, `autoPublish: true`, `draft: false`.

## 8. Report
Send Prosper a short message: what was posted, the first image, and anything that went wrong.
If the queue has fewer than 6 `todo` items left, add 10 new ones (alternating concept/tip, new industries and new topics, no repeats).
