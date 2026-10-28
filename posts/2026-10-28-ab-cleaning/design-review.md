# Design review: 2026-10-28-ab-cleaning (Spotless Co.)

Choices (design:design-system, pick): layout `bento` (last 4: split-screen, inset-card, editorial-split, dark-mono), sections menu-list → big-testimonial → bento-steps → faq-accordion → booking-bar, font `condensed` (Anton caps + Schibsted; prev sans; Instrument Serif italic only for the hero accent word), shape `round` (prev soft), mode `tinted` (pale cobalt page, prev dark). Accent cobalt #2348D9 + mint #B9EED3 (prev mustard), dark #0B1430. Frame palette `pal-sage` (last 3: cloud, midnight, sand).
Hero/header: Prosper asked mid-run (2026-10-28) for heroes to take their theme from boards 03 + 01. Rebuilt as a dark stage: gloved hands with a spray bottle masked so they float on the dark ground with a cobalt glow behind them, glass pill nav with mint underline, "your weekend," italic over "HANDED BACK.", 02/04 counter, outline arrows, vertical indicators, dot pagination, toggle CTA with WhatsApp knob, rotating "FREE RE-CLEAN · 24H GUARANTEE" badge. The bento tiles (version B booking card, rating, clipped-corner hours) sit under it.

## 1. design:design-critique
- recent_sites: the first version echoed recent sites in three places: the FAQ heading "Before you book" (mechanic), split-form ending (dentist "Book your check-up this week") and 4-column numbered steps (landscaping). Changed to "Keys, pets and re-cleans", a full-width booking-bar CTA and a bento of steps.
- Hero h1 at 122px pushed the CTAs out of the tile → fixed (then replaced by the new 03+01 hero stage).
- Hero subject vs mechanic (also dark/glow): this one is a masked subject with no frame, an italic-over-bold headline, counter/arrows/dots, and bento tiles below on a tinted page. It doesn't read as the same page.
- Step 01 repeated the hero photo → swapped to mop-living. Step 01 number on photo → navy pill. CTA heading wrapped to 4 lines → nowrap at 132px.
- Slide: B "/visit" wrapped and the team line squeezed → nowrap; top shade darkened so the rating line reads.

## 2. design:ux-copy
- One primary CTA everywhere: "Book a clean" (nav, hero toggle, B card, booking bar, slide A + B). "Free re-clean" and "Products included" used the same way across site and slide (site said "Our own products" → fixed).
- Hero support line trimmed 17 → 12 words. No banned heading formulas; labels 1–3 words; every price has a unit (per visit / per home / per month / per seat).

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures, no text < 13px, no targets < 44px ("Ask on WhatsApp" link raised to 44px min-height).
- Check-by-eye: B tile/card text sits on top + bottom navy shades; step 01 text on a bottom shade, number on a solid pill; hero headline sits on the dark stage (subject masked out under the copy); frame labels on sage are dark. All readable.
- "Most booked" is a worded tag; WhatsApp buttons have aria-labels; badge and arrows aria-hidden.

## 4. design:design-system (audit)
- All colours are `:root` tokens (incl. --stage, --glow, --shade, --shade-2); no raw hex/rgba in the rules (grep checked; the SVG badge uses style="fill:var(--…)").
- Fonts: Anton, Schibsted, Instrument Serif (local). Gutter 56px, sections 112px. Radius 28/18px + full pills (round).
- Must-haves: nav CTA, CTA repeated in the end band, WhatsApp buttons, Rand prices, footer "Concept by CAAS Studios". Queue item records layout, sections, font, shape, mode.
