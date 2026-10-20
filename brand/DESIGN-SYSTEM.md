# CAAS Studios concept-site design system

Prosper, 2026-10-20: "the websites are starting to look too alike." From 13 to 20 Oct, five of six sites used the same skeleton: dark photo hero with a two-line headline and glass booking bar, then a stat row, a grey-continuation about statement, three cards with the middle one dark, a dark 3×2 feature grid with one accent tile, four step rows beside a photo, and a photo CTA band. Only the colours changed.

This file splits what stays **fixed** (so every site is still clearly CAAS-quality) from what must **vary** (so the feed doesn't repeat). Every post records its choices on the queue item, and each run checks them against the last posts.

## 1. Fixed (the shared system)
- **Canvas:** 1280px desktop page, side gutter 56px (64 or 72 are also fine), sections 96–120px vertical padding.
- **Fonts:** only the local ones in `brand/fonts.css`: Schibsted Grotesk (sans), Instrument Serif (display serif + italic), Anton (condensed display caps).
- **Colour tokens:** declare them once in `:root` and use only `var(--…)` after that: `--ink --ink-2 --ink-3 --paper --line --acc --acc-ink --dark` (add `--acc-2` if needed). No raw hex values in the rules.
- **Contrast (WCAG AA, checked by `tools/a11y_check.py`):** body text ≥ 4.5:1, text ≥ 24px (or ≥ 19px bold) ≥ 3:1. `--ink-3` must still reach 4.5:1 on `--paper` (≈ #6F6862 on cream, not #8A867E/#958A83). Text on a bright accent uses `--acc-ink` (dark), never white. Text over photos always sits on a shade or scrim.
- **Sizes:** text ≥ 13px (chips/tags too), buttons/pills ≥ 44px tall, every pill has a verb label.
- **Must-haves on every site:** a nav with a primary CTA, one clear primary CTA repeated at the end, a WhatsApp button, real Rand prices, and a footer with "Concept by CAAS Studios".

## 2. Varies: pick per post and record on the queue item

### a) `layout`: the page archetype (must differ from each of the last 4 posts)
| id | Hero | Page rhythm |
|---|---|---|
| `photo-overlay` | Full-bleed photo, headline bottom-left, glass booking bar, stat row | The old default. Use it at most once in any 5 posts |
| `editorial-split` | Paper background; big serif headline on the left half; a tall uncropped photo on the right; no overlay | Numbered list rows (not cards) for services, a long pull quote, and a typographic price list |
| `type-giant` | One giant word in Anton or wide caps fills the width; a cut-out or framed photo overlaps it | Horizontal scrolling strip of services, marquee ticker band, big-number facts |
| `bento` | A grid of 5–7 tiles of mixed sizes: photo tiles, headline tile, rating tile, CTA tile, opening-hours tile | Bento again for features; FAQ accordion; split CTA with a short form |
| `centered-magazine` | Centred serif headline and subline on solid colour, then a 3-photo strip or a wide panorama below | Alternating zig-zag rows (image left, then right), testimonial carousel, centred CTA |
| `split-screen` | 50/50: solid colour panel with the copy and CTA on the left, a photo collage on the right | Tabs for services, timeline for the process, map plus hours block |
| `inset-card` | Hero is a rounded card inset on a coloured page, with a floating pill nav and a dot or slide counter | Price-comparison table, gallery masonry, a newsletter or booking form |
| `dark-mono` | The whole site is dark (no light sections): a glowing focal photo and accent-only highlights | Outline cards, a large numbered process, a full-width giant-type CTA |

### b) `sections`: choose the middle of the page from these, never the same 4 in the same order as the previous post
- **Services:** 3 cards · numbered list rows · horizontal scroller · tabs · bento · price table · menu-style typographic list
- **Proof:** stat row · one big testimonial · review cards · "as seen in" or certification badges · before/after strip
- **About:** statement paragraph · founder portrait with a quote · timeline · photo + facts list
- **Process:** step rows · horizontal timeline · accordion · 3 big numbers
- **CTA:** photo band · split with a short form · giant-type footer CTA · sticky-style booking bar

### c) `font`: the type pairing (must differ from the previous post)
`sans` (Schibsted only, tight) · `serif` (Instrument Serif display + Schibsted body) · `condensed` (Anton caps display + Schibsted body) · `mixed` (Instrument Serif italic accent word inside a bold sans headline)

### d) `shape`: the radius personality (must differ from the previous post)
`sharp` (0–4px, hairlines, editorial) · `soft` (10–16px) · `round` (24–32px cards, full pills)

### e) `mode`: the page tone
`light` (paper/white) · `tinted` (a pale accent-tinted page) · `dark` (dark throughout). At most two `light` in a row.

Record these on the queue item, e.g. `"layout": "bento", "sections": ["tabs","testimonial","timeline","split-form"], "font": "condensed", "shape": "sharp", "mode": "tinted"`. (`type` stays reserved for `"reel"`.) Posts before 2026-10-20 count as `photo-overlay` / `serif` or `sans` / `round` / `light`.

## 3. Copy rules (ux-copy)
- CTAs start with a verb and name the outcome: "Check your date", "Get a quote in 1 hour", "Book a free trial". Never "Learn more", "Submit", "Click here" or "Read more" (the deliberate BEFORE phone is the one exception).
- One term for one thing: if the hero says "viewing", the CTA band also says "viewing", not "tour".
- Headings say something specific about this business. These formulas are overused, so don't use them: "X, Zero Y", "From A to B", "Something for Every…", "Everything You Need…", "Choose Your Kind of…", "Why Choose Us".
- Section labels are 1–3 words. Supporting lines are ≤ 14 words. Prices always show what the unit is (/ night, / guest, from).

## 4. Accessibility rules (accessibility-review)
- Run `python3 tools/a11y_check.py posts/<id>`: zero FAIL lines before publishing. Then look at every "check by eye" line in the render and confirm a shade or scrim sits behind it.
- No meaning by colour alone: a "Most booked" chip has words, not just colour.
- Real `<img>` tags (if any) have alt text. Buttons are `<a>` or `<button>` with text.
