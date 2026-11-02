# Design review: 2026-11-02-before-after-construction (Bedrock Build)

Choices (design:design-system, pick): layout `bento` (last 4: dark-mono, type-giant, split-screen, inset-card), sections bento-services → price-table (board 08 glow on the featured column) → before-after-strip → big-testimonial → big-numbers → faq-tiles (board 09) → split-form, font `condensed` (Anton + Schibsted; prev serif), shape `sharp` (4px; prev soft), mode `tinted` (pale concrete #ECEEE4; prev light). Accent high-vis lime #C6F135 (prev 3: #FF6B4A, #5B8CFF, #C21F47), dark graphite #111310 with an olive glow. Frame palette `pal-sage` (last 3: blush, cloud, espresso; light after a dark frame). Hero boards 03 + 01 + 05: cut-out worker on a dark ground with lime glow, italic accent word over stepped condensed caps H1 ending in a full stop, 01/07 progress pill, glass nav bar with accent underline, toggle CTA with round knob, rotating badge.

## 1. design:design-critique
- recent_sites sheet: only bento hero in the set (tiles: stage, cut-out, rating, price, hours, latest-project); no other site opens with a tile grid.
- Found: pricing as 3 glowing plan cards matched the cleaning site's pricing → rebuilt as a finish comparison table (rows = spec, featured Mid column glows).
- Found: FAQ as a right-hand list of rows matched the mechanic site → 2×2 grid of open answer tiles.
- Found: H1 at 118px wrapped to 4 lines and pushed the CTA out of the stage → 92px, nowrap, 2 stepped lines; empty space under the CTA filled with a hairline facts row.
- Found: AFTER phone left a gap above the CTA → stage flexes to fill, CTA sits at the bottom. Power-tool tile cropped to a vest only → swapped for the rebar photo. Quote widow ("early.") fixed.

## 2. design:ux-copy
- One term: "site visit" everywhere (nav, hero, CTA band, form button, badge, phone). CTAs verb-led: Book a site visit, Book a free site visit, Price my plan, Book my site visit.
- Labels cut to 1–3 words ("Week 3 to week 38" → "Build progress", "How a build runs" → "Our promises"). Supporting lines trimmed to ≤ 14 words (services intro 16 → 12, CTA band 17 → 11).
- Every price shows its unit (/ m², / m, from). No banned heading formulas.

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures, no text < 13px; nav logo raised to a 44px target (was 40px).
- Check by eye: nav on glass over solid dark; hero text on the dark stage gradient; latest-handover caption now on a full-height scrim; Mid column rows on dark with glow only behind the button; FAQ text on olive→graphite. All readable. Text on lime uses --acc-ink.
- "Most booked" / "Fastest quote" are words, not colour only; WhatsApp buttons have aria-labels; badge and progress pill are aria-hidden; rebar tile has role=img + aria-label.

## 4. design:design-system (audit)
- SEO: one H1 "Home builders in Cape Town."; eyebrow "Bedrock Build · Building contractor in Cape Town"; subline with second keyword + price fact; nav uses service words; H2s "Building services in Cape Town", "Building prices in Cape Town", "Book a site visit in Cape Town this week"; title 42 chars; meta description 156 chars.
- Tokens: all colours in :root; grep finds no hex/rgba outside it (mask colour moved to --mask, badge SVG fills use var()).
- Fonts Anton / Schibsted / Instrument Serif italic only; gutter 56px; sections 104px. Must-haves: nav CTA, CTA repeated in the split-form band, WhatsApp buttons, Rand prices, "Concept by CAAS Studios" footer. Queue item records layout, sections, font, shape, mode.
