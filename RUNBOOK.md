# CAAS Studios — daily Instagram post runbook

Each run publishes EXACTLY ONE post to Instagram (@prosper.builds) through Metricool.
Prosper approved fully automatic posting, **weekdays only (Mon–Fri, never on weekends)**. Follow these steps in order.

**Reels only (since 2026-10-15). Every post is a Reel, no exceptions.** Never write "swipe" anywhere (slides, sigs, captions). Goal: grow toward 10k followers. Every post is published as an Instagram **Reel** (`reel.mp4`, made in step 5b from the designed slide/site). No more image or carousel posts. The design work (steps 3–5) is unchanged: the Reel is built from it.

## 1. Setup
```bash
git clone https://github.com/nkunzi05/caas-social && cd caas-social
pip install --break-system-packages playwright pillow && python3 -m playwright install chromium
```

## 2. Pick the item
**One post per day guard:** first call Metricool `getScheduledPosts` (blogId 7037975, Africa/Johannesburg) for today 00:00–23:59. If a non-draft Instagram post is already scheduled or published for today (ignore drafts) (Prosper sometimes has one made early), do NOT make another: send Prosper a one-line note ("Today's post was already scheduled: <brand>") and stop.

Open `content/queue.json`. Take the FIRST entry in `queue` with `"status": "todo"`. Only that one entry — never more than one post per run.
It names a `format` (`ab`, `landing`, `before-after`, `columns` or `monitor`), an `industry`, a made-up `brand` and a `slug`.
Post folder: `posts/<YYYY-MM-DD>-<format>-<slug>` (date = today, Africa/Johannesburg).

Prebuilt items: if the item has `"prebuilt": "<folder>"`, copy that folder's files into the post folder, re-render with `tools/render.py`, look at the result, and continue from step 6. Do not redesign it.

Duplicate guard: the queue is the source of truth. An item marked `"posted"` is never posted again. If this item's folder already exists with pushed JPGs but it is still `"todo"` (a previous run failed midway), reuse it and continue from step 6.

## 3. Get stock photos (free Unsplash only)
The workspace cannot download from Unsplash directly; a GitHub workflow does it.
1. `WebFetch https://unsplash.com/s/photos/<industry-term>?license=free` and pick 6–7 photos (every post now needs a full site) that fit (people at work, the space, the product). Skip photos with visible brand logos, watermarks, face masks, or anything dated or low quality.
2. For each pick, `WebFetch` its photo page and get the base `og:image` URL (`https://images.unsplash.com/photo-…`, cut at `?`). Use it ONLY if the page says "Free to use under the Unsplash License" (never Unsplash+).
3. Append lines to `stock/requests.txt`: `<slug>/<name>.jpg <images.unsplash.com URL> <unsplash page URL>`. Reuse photos already in `stock/<slug>/` when the industry has a set.
4. Commit and push. The "Fetch stock photos" workflow downloads them into `stock/<slug>/` within ~1–2 minutes. Poll with `git pull` every 15 s for up to 5 minutes. If photos don't arrive, check the latest run at `https://api.github.com/repos/nkunzi05/caas-social/actions/runs?per_page=1`; if it failed, try different photos once, then stop and report.
5. Look at the photos (make a contact sheet and Read it) before designing.

## 4. Design the slide (single 1080×1350 slide) AND the full site
**Every format gets a full website scroll (Prosper, 2026-10-14).** Besides slide1.html, EVERY post (ab, landing, before-after, columns, monitor) builds `site.html`: a full 1280px desktop homepage, plus `showcase.css`. **The site's layout comes from `brand/DESIGN-SYSTEM.md` (Prosper, 2026-10-20: "the websites are starting to look too alike"), not from a fixed template.** What the site is per format:
- **landing**: the full version of the homepage in the slide (same brand, nav, hero headline, accent, photos), continued down the page.
- **before-after**: the AFTER redesign as a full site (same headline, CTA and WhatsApp button as the after phone).
- **ab**: the business's full site, with version B of the UI element (the bolder one) in the hero booking/quote bar.
- **columns / monitor**: as below.
The Reel opens on slide1 for 3 s, crossfades into site.jpg and scrolls it to the footer (step 5b). Reference: `posts/2026-10-14-landing-coffee-shop/` (landing slide + full site).

**Design system first (every post, Prosper 2026-10-20).** Before writing any HTML, run the `design:design-system` skill (Skill tool) against `brand/DESIGN-SYSTEM.md` and the last 4 entries in `done`. Pick a `layout` archetype not used by any of the last 4 posts, a `sections` mix, and a `font`, `shape` and `mode` that differ from the previous post, as that file's rules say. Write them on the queue item. Put the colour tokens in `:root` and use only `var(--…)` after that. Then build site.html for that archetype. Hero UI details from the UI board (below) still apply, but inside the chosen archetype.

Copy the approved reference for the format and adapt it to the industry. Match its quality and structure exactly:
- **ab** → `posts/_examples/01-ab/slide1.html`: eyebrow `<INDUSTRY> BOOKING/ORDERING`, a question headline ("Which … gets more clients?"), two versions of the same real UI element for this business (A: clean light card with photo on top; B: photo-led dark card with glass panel). Both must look good; B is the bolder one. A/B circles under the cards, footer "Comment A or B ↓".
- **landing** → `posts/_examples/02-landing/slide1.html`: "Concept NN — <Industry> website" eyebrow, full homepage mockup: nav + logo + CTA pill, big photo hero with a two-line headline (second line in a warm accent), short subline, CTA, rating line, a floating glass info card, then the lower row (about block + two dark photo tiles with "Learn more").
- **before-after** → `posts/_examples/03-before-after/slide1.html`: "Which one would you book/hire/visit?", two phones. BEFORE = a believable average template site (plain header, dim stock photo with a generic "Welcome to …" line, an "About Us" text block, grey service boxes, "contact us" link, "Read More" button, dated © footer) — plausible but forgettable, never cartoonish. AFTER = photo-led redesign with chip, bold headline, one clear CTA + WhatsApp button. The after must clearly win.
- **columns** and **monitor** both start from `site.html`: a full 1280px-wide desktop homepage for the business, built from the layout archetype and section mix you picked in `brand/DESIGN-SYSTEM.md` (`posts/_examples/04-columns/site.html` shows the quality bar and the `photo-overlay` archetype only. Don't copy its structure unless that archetype is your pick). Pick ONE accent colour that suits the industry. Copy `showcase.css`. Slides crop `site.jpg` with `background-size: <card width>px auto` and `background-position: 0 -<section offsetTop × card width/1280>px`; measure section offsets with Playwright (`section.offsetTop`) rather than guessing, and never let a crop end on a sliver of the next section. Swap every blurred background photo to this item's hero photo. Needs 6–7 photos (as many as the chosen layout uses).
  - **columns** → `posts/_examples/04-columns/` (3-slide carousel; for Reels only `site.html` + slide1 are needed, slides 2–3 are optional): (1) overview: back column = lower half of the page, front column = top of the page, "CAAS STUDIOS · Website concept" label + DM "SITE" pill; (2) close-up of the cards section with a short headline about the idea (accent on the second half); (3) "Want a site like this?" + close-up of the steps section + DM/WhatsApp CTA + 3 chips.
  - **monitor** → `posts/_examples/05-monitor/` (single image): "© 2026 CAAS Studios" / "@prosper.builds" top row, big two-line title "<Industry>" (white) + "Website" (ghosted white ~32%), the site hero on the desktop monitor (`.screen` crops site.jpg from the top), white base band with "UI/UX Design" + "Concept for an invented <business type>" and the DM "SITE" pill, blurred hero photo behind. Keep the industry title to one line at 118px (≈14 characters; shrink the font if longer). Only the hero shows, but still build the full site.html so it can be reused.
- **UI inspiration board (every post, Prosper 2026-10-16):** before designing, open `posts/_inspiration/ui-board/` (Read the 3 JPGs and README.md). Pick ONE board style that suits the industry and isn't the one the previous post used (record `"ui_ref": "01" | "02" | "03"` on the queue item), and bring 2–3 of its UI details into the hero of the mockup (the after phone, the landing/site hero, version B, the monitor screen): e.g. a floating pill nav, a circular rotating-text badge, a giant wide-caps display word, an avatar stack + hairline rules, a clipped-corner info card, an italic accent word over a bold word with a full stop, a slide counter / dot pagination, or a cut-out subject on a matching dark background. Borrow design language only: never their names, logos, wording or artwork. It must still read as a real site for this business, with the CTA and WhatsApp clear.
  - **Headers and hero sections (Prosper, 2026-10-28):** the site header + hero now always take their theme from boards **03** (subject that floats on a matching dark ground, italic accent word over a bold word with a full stop, 02/04 counter, thin outline arrows, dot pagination, logo letter + accent dot) and **01** (floating glass pill nav with an accent underline, a coloured glow behind the focal subject, toggle CTA with a round knob, rotating-text badge, vertical indicators). Combine details from both in every hero (a dark hero stage even when the rest of the page is light or tinted), and blend the focal photo into the dark ground with a soft mask so it reads as a cut-out. Board 02 is no longer used for heroes. Record `"ui_ref": "03+01"`. Vary the subject, accent colour and arrangement each post so heroes don't repeat.
  - **More boards (Prosper, 2026-10-28): 04–10** in the same folder (see its README). Hero = 01 + 03 plus ONE of 04 (giant word behind the subject), 05 (cut-out subject on a vivid gradient, stepped condensed caps, 01/07 progress pill) or 06 (duotone subject on a big accent circle, 01—03 progress line), rotated so consecutive posts don't use the same one; record `"ui_ref": "03+01+04"` etc. Pricing sections take their theme from 07/08 (giant word or glow behind glass plan cards, featured middle card, month/year toggle), FAQs from 09 (dark rows with an accent glow from the left edge, thin +/−), galleries from 10 (coverflow cards + glass caption/control bar); record `"ui_sections"`. Never use photos of real, recognisable people from these boards; always our own Unsplash photos.
- **Inspiration from siteinspire (every other columns/monitor post):** before designing site.html, open `https://www.siteinspire.com/websites` (or a category such as `/websites/categories/minimal`), pick ONE featured site in a fitting industry or style, open its siteinspire page and the live site, and borrow only its *design language*: section rhythm, type mood (e.g. editorial serif + small sans labels), whitespace, colour temperature and UI details. Never copy its name, logo, wording, photos or exact layout. Write all content fresh for the invented business. Add `"inspiration": "<siteinspire URL>"` to the queue item. Available local fonts: Schibsted Grotesk (sans), Instrument Serif (editorial serif, incl. italic) and Anton (condensed display caps). Reference: `posts/_inspiration/2026-10-09-bakery/`.
- **Colour rotation (Prosper wants the colours to change from time to time):** don't let the feed look the same every day.
  - *ab / landing / before-after:* add ONE palette class from `brand/palettes.css` to the `.post` div (`<div class="post pal-sand">`). Light: `pal-cloud` (original grey), `pal-sand`, `pal-sage`, `pal-blush`, `pal-sky`, `pal-butter`. Dark frames: `pal-midnight`, `pal-forest`, `pal-espresso`. Look at the last 3 entries in `done`: never reuse a palette any of them used (missing `palette` = `cloud`), and use a dark frame about every 3rd post. Pick one that suits the industry and photos.
  - *Inside the mockup:* also vary the accent colour (the second headline line, chips, stat tiles) per industry, and never use the same accent as the previous post. Don't default to warm orange/beige every time: try deep green, cobalt, terracotta, plum, teal, mustard, etc. where it fits.
  - *columns / monitor:* the frame comes from the blurred hero photo, so vary the site's accent and its dark-section colour (navy, forest, aubergine, espresso…) instead.
  - Record it on the queue item: `"palette": "<name>"`, `"accent": "<hex>"`. After rendering, check every frame label (eyebrow, question, sig, A/B circles) is readable on the chosen background.
- Link `../../brand/ui.css` (adjust the relative path for the folder depth) and `stock/<slug>/…` photos with relative paths. Fonts come from `brand/fonts.css` (local files).
- Industry-fitting copy, real South African prices in Rand, services that business actually sells. Ratings/review counts may appear inside the mockup UI (it is a concept site); never in the caption as facts.
- Footer sig: "CAAS STUDIOS" left; right side per format as in the references.
- Concept number NN for landing posts = number of `landing` posts already posted + 2.

## 5. Render and check
`python3 tools/render.py posts/<id>` then LOOK at the JPG (Read tool). Every post has a site.html now: render.py first renders `site.html` to `site.jpg`, then the slides — look at site.jpg (downscaled) AND every slide. Fix and re-render if anything is clipped, overlapping, misspelled, unreadable over a photo, or leaves a big empty area.

## 5a. Design pass with the design skills (every post, Prosper 2026-10-20)
After the first render and before the Reel, run these four skills with the Skill tool, in this order. Fix what each one finds, re-render, and repeat until all four are clean. Save the short results to `posts/<id>/design-review.md` (a few lines per skill: what it found and what you changed). Commit that file with the post.
1. **`design:design-critique`**: run `python3 tools/recent_sites.py posts/<id> 4 <scratch>/recent.jpg`, Read the sheet, then critique site.jpg and slide1.jpg with the skill's framework (first impression, usability, hierarchy, consistency). A hard requirement: at a glance, the new site must NOT look like any of the last 4 sites (same hero composition, same order of section types, or same card or grid pattern). If it does, redesign it (another archetype or section mix); a recolour doesn't count.
2. **`design:ux-copy`**: review every headline, CTA, section label and price line against the copy rules in `brand/DESIGN-SYSTEM.md` §3 (verb-led, specific CTAs; one term per thing; none of the banned heading formulas; units on prices). Rewrite anything weak.
3. **`design:accessibility-review`**: run `python3 tools/a11y_check.py posts/<id>`. It must report 0 contrast failures, no text under 13px and no pills under 44px. Then check by eye that each "check by eye" item has a shade behind it in the render.
4. **`design:design-system`** (audit mode): confirm that site.html uses only the `:root` tokens (no stray hex values in the rules) and the fonts, gutter and must-haves in §1, and that the queue item records `layout`, `sections`, `font`, `shape` and `mode`.
If a skill isn't available in the run, apply the same checklist by hand (from DESIGN-SYSTEM.md) and note that in design-review.md. Never skip the checks.

## 5b. Make the Reel
`python3 tools/reel.py posts/<id> --hook "<hook>"` → `reel.mp4` (1080×1920; 13 s for a slide, 20 s when the post has a full `site.html` to scroll) + `reel-cover.jpg`.
- The hook is the big line at the top for the whole video: a question that makes people stop, ≤ 45 characters, about the business (e.g. "Would you order your coffee from this site?", "Which one gets more bookings: A or B?", "Would you hire this plumber from his site?"). No hashtags or emojis in it.
- Every post has a site.html, so every Reel is 22 s: slide1 for 3 s, crossfade, then the full `site.jpg` scrolls to the footer. (A post without site.html falls back to a 13 s zoom; that should not happen.) The last 2 s are the "Want a site like this? DM SITE" end card.
- **Soundtrack (since 2026-10-16):** every Reel has music. reel.py adds an original, royalty-free track made by `tools/music.py` (synthesised from scratch: no samples, no licence, nothing Instagram can mute). The style is picked from the post id; choose one to fit the brand with `--music lofi|chill|upbeat|house` (lofi = cafés, salons, cosy; chill = editorial, property, calm; upbeat = trades, fitness, bold; house = bars, fashion, nightlife). Never put copyrighted or "trending" songs into reel.mp4. Check the reel has an audio stream (`ffprobe -v error -show_entries stream=codec_type -of csv reel.mp4` lists `audio`). To add music to an existing reel without re-rendering: `python3 tools/music.py posts/<id> [--style <style>]`.
- LOOK at it: grab frames at 0.5, 3.5, 6.4, 8.8 and 12 s (`ffmpeg -ss <t> -i reel.mp4 -frames:v 1 -vf scale=300:-1 fN.png`), put them side by side and Read the strip. Fix and re-render if the hook wraps to 3+ lines, a zoomed frame cuts off a headline badly, or the end card is unreadable.

## 6. Caption
Write `caption.txt`: a hook line (for ab: ask people to comment A or B; for before-after: "Which one would you book?"; for columns/monitor: "Would you book through this homepage?"; never say "swipe": it's a Reel), 1–2 short lines on the design idea, the CTA ("Want a site like this? DM us \"SITE\" or WhatsApp +27 665 989 442."), then 6–9 hashtags (always #caasstudios #webdesign #smallbusinesssa #capetown, plus 1–2 reach tags such as #webdesigner #uiux #websitedesign, plus industry tags). Mention it's a concept for an invented business.

## 7. Commit and push
Mark the queue item `"status": "posted"` with `"post": "posts/<id>"` and move it to `done`.
```bash
git add -A && git commit -m "Post <id>" && git push origin HEAD:main
```
Push MUST succeed before publishing — Metricool downloads the image from GitHub.

## 8. Publish via Metricool
- Brand (blogId): `7037975`, network `instagram`, timezone `Africa/Johannesburg`.
- Media URL: `https://raw.githubusercontent.com/nkunzi05/caas-social/main/posts/<id>/reel.mp4` — confirm it returns HTTP 200 first (wait up to ~2 minutes after pushing). Every format, columns included, is ONE video.
- Time: peak for this account is 10:00–11:00 SAST. `date` = today 10:30 SAST if that is ≥ 5 minutes away, otherwise now + 5 minutes.
- `createScheduledPost` with `date`, `publicationDate` = same in Africa/Johannesburg, `text` = caption, `media` = [reel URL], `providers` = `[{"network":"instagram"}]`, `instagramData` = `{"type":"REEL","showReelOnFeed":true}`, `videoCoverMilliseconds: 800`, `autoPublish: true`, `draft: false`.
- Record `"type": "reel"` and `"hook": "<hook>"` on the queue item (commit + push that small change after publishing).

## 9. Report
Send Prosper a short message: what was posted, the Reel cover (`reel-cover.jpg`) and the reel.mp4, and anything that went wrong.
Once a week (Mondays), add one line on growth: followers now vs. last Monday (Metricool `getAnalyticsDataByMetrics`, metrics IGEV01 followers, IGEV43 gained, IGEV30 avg reach per reel).
If the queue has fewer than 6 `todo` items left, add 12 new ones: new industries and made-up brands, formats rotating ab → landing → before-after → columns, then ab → landing → before-after → monitor.
