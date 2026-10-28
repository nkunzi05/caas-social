# Design review: 2026-10-28-ab-cleaning (Spotless Co.)

**Redesigned mid-run at Prosper's request (2026-10-28):** "make a newer design, take inspiration from the new files, change the colours, hero text SEO-optimised always." The first version (bento, cobalt/mint, pale-blue page) was pulled from Metricool before it went out.

Choices (design:design-system, pick): layout `type-giant` (last 4: split-screen, inset-card, editorial-split, dark-mono), sections marquee-ticker → glow-pricing → coverflow-gallery → big-testimonial → faq-glow → word-behind-glass-cta, font `condensed` (Anton caps + Schibsted, Instrument Serif italic accent; prev sans), shape `round` (prev soft), mode `dark`. New colours: violet→magenta→coral hero gradient (#2A0F5C → #5B21B6 → #B4239F → #FF6B4A), coral accent #FF6B4A, lavender #A78BFA, violet-black page #0F0A1A. Frame palette `pal-blush` (last 3: cloud, midnight, sand).
Boards: hero = 04 (giant "SPOTLESS" behind a tilted photo card, glass stat card with avatar stack) + 05 (vivid gradient, stepped condensed caps, 01/07 progress pill) + 01/03 (glass pill nav with underline, toggle CTA with WhatsApp knob, italic accent line). Pricing = 07/08 (ghost word + glow behind glass plan cards, glowing featured middle card with dot grid, Regular/Once-off toggle, horizon arc). Gallery = 10 (coverflow + glass caption plates + glass control bar). FAQ = 09 (dark rows with a coral glow from the left, thin +/−).

## SEO hero (new standing rule, DESIGN-SYSTEM §5)
- `<h1>`: "Home & office cleaning in Cape Town" (only H1 on the page). Eyebrow: "Spotless Co. · Cleaning service in Cape Town". Subline: "Vetted, insured cleaners for homes, flats and offices. Fixed prices from R480 per visit."
- `<title>` "Home & Office Cleaning in Cape Town | Spotless Co." (51 chars); meta description 150 chars. Nav: Home cleaning / Office cleaning / Prices / FAQ. H2s: "Cleaning prices in Cape Town", "Book a cleaner in Cape Town this week". Giant words are aria-hidden or CSS-generated.

## 1. design:design-critique
- vs recent_sites: no other recent site has a gradient hero, a giant word behind a tilted card, glass pricing cards or a coverflow. The dark mechanic site is the nearest, but its hero is copy + a framed photo on black with a stat row/outline cards. This one doesn't look alike.
- Found: giant word ran into the H1 → hero 960px tall, word 268px, H1 on two stepped lines (94px). Photo tag clipped by the B card → removed. B card CTA inherited section padding (.cta clash) → renamed .bcta. FAQ title left an orphan "cleaner" → accent line on its own line at 84px.

## 2. design:ux-copy
- One primary CTA ("Book a clean"), plan-specific CTAs name the plan ("Book a flat clean / home clean / deep clean"). "Free re-clean" and "per visit / per home" used the same way throughout. No banned heading formulas; sublines ≤ 20 words.

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures (decorative "Prices" ghost word moved to CSS content so it isn't read as text), no text < 13px, no targets < 44px.
- Check-by-eye: hero copy sits on the dark violet end of the gradient; B card text on a solid glass body / bottom shade; coverflow captions on glass plates; FAQ text on dark rows. All readable. Slide: B card text on violet gradient, A card unchanged.

## 4. design:design-system (audit)
- All colours in `:root` (incl. named shadow/glow tokens); no raw hex/rgba in rules. Fonts local only. Gutter 56px, sections 112px, radius 28/18 + pills. Must-haves present (nav CTA, end CTA, WhatsApp, Rand prices, "Concept by CAAS Studios"). SEO §5 checked. Queue item records layout, sections, font, shape, mode, ui_ref, ui_sections.
