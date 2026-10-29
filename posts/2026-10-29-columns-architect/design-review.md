# Design review: 2026-10-29-columns-architect (Lineform Studio)

Choices (design:design-system, pick): layout `split-screen` (last 4: inset-card, editorial-split, dark-mono, type-giant), sections service-tabs → photo-facts → horizontal-timeline → founder-quote → map-hours → photo-band CTA, font `mixed` (bold Schibsted headline + Instrument Serif italic accent; prev condensed), shape `sharp` (3px, hairlines; prev round), mode `tinted` (pale blueprint-blue page #E8EDF3; prev two were dark).
New colours: "blueprint" palette: electric blueprint blue #5B8CFF (accent), deep cobalt #2147C2 (accent text on paper), ink-navy #0B1019 stage. Last 3 accents were burgundy, mustard, coral.
Boards: hero = 03 (italic "drawn to fit." over the bold H1 with a full stop, logo letter + accent dot, thin outline arrows, vertical indicators) + 01 (glass nav with accent underline, blue glow behind the house, toggle CTA with round knob, rotating-text badge) + 06 (duotone house on a big accent circle, smaller circle cut by the edge, 01 —— 03 progress line). No pricing/FAQ/gallery sections, so no ui_sections. Siteinspire skipped (previous columns/monitor post used one; every other post).

## SEO hero (DESIGN-SYSTEM §5)
- `<h1>` "Residential architects in Cape Town." (only H1). Eyebrow "Lineform Studio · Architects in Cape Town". Subline names new homes / extensions / renovations + council approval + "Concept designs from R18 500".
- `<title>` "Residential Architects in Cape Town | Lineform Studio" (53 chars); meta description 158 chars. Nav: New homes / Extensions / Renovations / Fees / Projects. H2 "Architectural services in Cape Town", "Book a site visit with a Cape Town architect". Badge and map are aria-hidden.

## 1. design:design-critique
- vs recent_sites: no recent site has a split dark hero with a duotone subject on a circle, tabs, a horizontal timeline or a map block. Found: the first ending (split section with a short form + "… this week" headline) repeated the dentist site's ending → replaced with a photo-band CTA (glass panel over the full-colour house) and a new H2.
- Found: the same drafting photo was used in a hero tile and the founder quote → hero tile now shows the Sea Point townhouse. The hand-drafting photo with a brand logo on the shirt was dropped at photo selection.

## 2. design:ux-copy
- One action term throughout: "site visit" (nav, tabs panel, hero toggle, CTA band, hours). CTAs verb-led: "Book a site visit", "Book a free site visit", "See fee breakdown". All prices carry units (/ home, / project, of build cost). No banned heading formulas.
- Changed "94% approved first time" → "94% plans approved first time" (said what was approved).

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures. Rotating badge text was 11.5px → 13px; now no text < 13px and no targets < 44px.
- Check-by-eye: nav and tile captions on dark glass, CTA copy on an 80% navy glass panel, timeline text on the near-solid paper grid. All readable in the render. Icon-only links (WhatsApp, arrows) have aria-labels; decorative badge/map are aria-hidden.

## 4. design:design-system (audit)
- All colours are `:root` tokens (incl. glass, glow, scrim, grid, mask); scripted check found no raw hex/rgba in rules or inline styles. Fonts local only. Gutter 56px, sections 112px, radius 3px. Must-haves present: nav CTA, end CTA, WhatsApp (hero + CTA band), Rand prices, footer "Concept by CAAS Studios". Queue item records layout, sections, font, shape, mode, ui_ref.
