# Design review: 2026-10-23-monitor-dentist (Brightside Dental)

Choices (design:design-system, pick): layout `inset-card` (last 4: photo-overlay, type-giant, bento, split-screen), sections price-table → gallery-masonry → review-cards → accordion → split-form, font `sans` (prev serif), shape `round` (prev sharp), mode `light` (prev tinted). Accent coral #FF8A5B (prev lime), dark teal #0D3B39. UI board 01 (prev 03): floating glass pill nav with accent underline, toggle-style CTA with round phone button, rotating-text badge; plus inset-card dot counter "01 / 03" and a clipped-corner slots card. Siteinspire: Deakin Dental (health category) picked; the live site could not be opened this run, so only the clean clinical-light mood was used.

## 1. design:design-critique
- recent_sites sheet: hero is an inset rounded card with floating pill nav (none of the last 4), sans-only type, price comparison table and masonry gallery are new patterns. Not alike.
- Found: final dark split-form CTA echoed the bakery's dark form tile → recoloured to a pale coral panel with teal accent line.
- Found: empty 200px row in the masonry grid → grid set to 2 × 290px rows. Book headline broke "check-/up" → rewritten to 3 lines. Visit section overflowed the 1280 page (1334px) → fixed grid min. Hero headline squeezed by -0.055em tracking / wrapped to 3 lines → -0.045em, wider column.
- Swapped the open-mouth close-up out of the tall "first visit" panel (too clinical for a kids-first brand) to a small gallery tile; tools photo there instead. Dropped the waiting-room photo (its sign quotes song lyrics).

## 2. design:ux-copy
- CTAs all verb-led and use one term, "check-up": Book a check-up / Book a family check-up / Book my check-up / WhatsApp us.
- Prices lead was 17 words → "Every quote in writing first. Pay per visit, or join the Family Plan." (13).
- "Parents talk. Here's what they say." (generic) → "Nervous kids. Happy parents."
- Chip "New patients this week" → "Taking new patients"; strip "From 3 yrs / first visit is on us" → "Age 3+ / Kids' first check-up is free".
- Removed a real medical-aid brand name from a review. All prices show units (/ visit, / set, / tooth, / session, / month).

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures, no text < 13px, no pills < 44px.
- Check-by-eye items: hero nav sits on a dark glass pill; hero copy on a left-to-right dark scrim (≥ 0.62 alpha); slide title over blurred, darkened photo; base band text on white. All readable in the render.
- "Most chosen" plan marked with words, not colour only. Decorative rotating badge SVG set aria-hidden.

## 4. design:design-system (audit)
- All hex values live in `:root` (--ink, --ink-2, --ink-3, --paper, --card, --line, --acc, --acc-ink, --acc-soft, --dark, --dark-2, --on-dark, --on-dark-2, --wa, --wa-ink, scrims); rules use var(--…) only.
- Fonts: Schibsted Grotesk only (sans). Gutter 56px, sections 100–110px.
- Must-haves: nav CTA, CTA repeated at the end (split form), WhatsApp buttons, Rand prices, footer "Concept by CAAS Studios". Queue item records layout, sections, font, shape, mode.
