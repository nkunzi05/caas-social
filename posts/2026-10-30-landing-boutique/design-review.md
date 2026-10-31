# Design review: 2026-10-30-landing-boutique (Atelier Nine)

Choices (design:design-system, pick): layout `inset-card` (last 4: editorial-split, dark-mono, type-giant, split-screen), sections horizontal-scroller → price-table → masonry-gallery → review-cards → faq-accordion → split-form, font `serif` (prev mixed), shape `round` (prev sharp), mode `light` (prev tinted). Accent raspberry #C21F47 + blush #F7CBD6 on wine-black #170A0E (last 3 accents: mustard, coral, blueprint blue). Frame palette `pal-espresso` (last 3: sand, blush, cloud; dark frame due). Hero ui_ref 03+01+04: rounded dark hero card inset on the paper page, floating glass pill nav with accent underline, a9 logo letter + accent dot, italic "dressed for it." over a bold H1 with a full stop, crimson glow behind the model blended in with a soft mask, giant ghosted "NINE" behind her (board 04), toggle CTA with round knob, rotating-text badge, 02/04 counter + dots, outline arrows, vertical indicators.

## 1. design:design-critique
- recent_sites sheet: first inset-card hero (rounded card on a paper page, not full-bleed), first product scroller and masonry gallery.
- Found: the first pricing pass (3 dark glass cards, glowing middle card, board 08) repeated the cleaning post's pricing pattern → replaced with a light price-comparison table on a blush inset card (featured column dark).
- Found: FAQ (title left, rows right) matched the mechanic layout → heading row on top, questions in a 2-column grid.
- Found: giant "ATELIER" word sat behind the headline and read as noise → "NINE", right-aligned behind the model only.
- Found: rotating badge text overran its circle ("CAFREE") → shorter text; info card price wrapped → wider card; subline broke "30-/minute" → non-breaking hyphen.
- Slide: CTA rendered underlined → fixed; empty space under the about block → 4.9 ★ proof line with hairline.

## 2. design:ux-copy
- One term: "fitting" for the service and every CTA (Book a fitting / Book my fitting / Book a quick·occasion·wardrobe fitting); H2 "Personal styling prices" → "Fitting prices in Cape Town" (label keeps "Personal styling").
- "What our clients wore out." (reads as damaged clothes) → "Clients who left dressed for it." (echoes the hero).
- FAQ answer aligned with the table (R650 occasion fee back, R500 back on wardrobe fittings). Slide tile "90 min, back off your buy" → "90 min, fee back off your buy".
- Prices all carry units (/ 30 min, / 90 min, / half day, / night, / item); no banned heading formulas.

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures, no text < 13px, no pills < 44px (review stars on white were 2.17:1 → darker --star-d).
- Check-by-eye: hero copy sits on the solid wine-black stage (photo is masked to the right half); gallery captions and split-photo caption on 0.86 scrim pills; slide tiles have top + bottom scrims; frame labels on espresso are light.
- Product photos and hero model have role="img" + aria-label; giant word and badge aria-hidden; FAQ questions role="button" tabindex; "Most booked" chip uses words.

## 4. design:design-system (audit)
- SEO: one H1 "Women's clothing boutique in Cape Town." + keyword subline with sizes and price fact (16 words); eyebrow names brand + category + street; nav uses service words; title "Women's Clothing Boutique in Cape Town | Atelier Nine" (53 chars); meta description 160 chars; H2s carry "Cape Town boutique", "Fitting prices in Cape Town", "Book a fitting in Cape Town".
- All colours in `:root` (incl. --mask for the photo mask); 0 hex/rgba values in the rules (script-checked).
- Fonts Instrument Serif + Schibsted; gutter 64px, sections 110px; radius 28/18px + full pills (round). Must-haves: nav CTA, CTA repeated in the split form, WhatsApp buttons, Rand prices, footer "Concept by CAAS Studios". Queue item records layout, sections, font, shape, mode.

## v2 (2026-10-31): Prosper, "improve the site and make it look less like AI"
What read as generated, and what replaced it:
- Hero stacked every board widget at once (glass pill nav, glow + masked cut-out, ghost "NINE", rotating badge, 02/04 counter, dots, vertical bars, arrows, floating glass card, knob CTA). → A plain shop header (announcement bar, centred serif wordmark, Bag (0)), and a hero that is just a wine panel beside the uncropped studio photo, with a product caption on the photo. No glow, masks or decorative controls.
- Every H2 had an italic accent half in colour ("…at our *Cape Town boutique.*"). → Plain serif sentence-case headings; italic only once, in the H1.
- SaaS patterns (4-stat trust strip, 3 star-rated review cards with initial avatars, comparison table with ticks, +/− accordion). → One customer quote, a typographic fitting list with time and price, plain two-column Q&A.
- Generic copy. → Specific shop details: owners' note (Lindi & Mei, the old shoe-repair shop, sizes 6–22, tailor upstairs), parking off Rheede Street, Card/SnapScan/Zapper, 14-day returns, "four left", "knitted in Woodstock", new-in emails.
- Everything 28px-round with pills on photos. → 6px images, 14px cards, pills only for buttons; captions under photos, not on scrims.
- New-in is a plain 4-up product grid; "See all 64 pieces" link. White-blazer no longer used twice (booking photo is browsing.jpg).
- Checks: a11y_check 0 contrast failures (WhatsApp link green darkened to #17733F for 4.5:1); one H1 with the keyword; title/meta unchanged; all colours in :root. Note: the fitting price list is a typographic list, like the photographer site's price list (4 posts back); the rest of the page differs.
- shape changed round → soft. Reel re-rendered in the repo; the published Instagram Reel (Metricool 410914907, 30 Oct) is not replaced.
