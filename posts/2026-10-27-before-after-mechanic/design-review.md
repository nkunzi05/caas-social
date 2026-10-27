# Design review: 2026-10-27-before-after-mechanic (Torque Auto)

Choices (design:design-system, pick): layout `dark-mono` (last 4: bento, split-screen, inset-card, editorial-split; type-giant skipped too because the car-wash site used it with a near-identical section mix), sections outline-cards → stat-row → numbered-process → review-cards → faq-accordion → giant-type-cta, font `sans` (prev serif; Schibsted 900 wide caps), shape `soft` (prev sharp), mode `dark` (prev two were light). Accent mustard #F2B705 (prev wine), dark #08090A. Frame palette `pal-sand` (last 3: butter, cloud, midnight). UI board 01 (prev 02): floating pill nav with accent underline, glowing focal photo, giant wide-caps headline, toggle CTA with round phone knob, rotating-text badge, vertical slide indicators, arrow buttons.

## 1. design:design-critique
- recent_sites sheet: the only all-dark page; hero is copy-left + glowing framed photo-right (no full bleed, no bento, no split panel, no inset card); services as outline cards. Not alike any of the last 4.
- Found: rotating badge text overran the circle ("CAPE TOWN" cut) → shortened to "SAME-DAY SERVICE · SALT RIVER ·".
- Found: process heading wrapped with an orphan ("spanner.") → rewritten as "Price first. Spanner second." at 64px.
- Found: after phone headline wrapped to 3 lines and left a gap above the CTA → 46px headline, taller focal photo (370px).

## 2. design:ux-copy
- One term: "quote" everywhere (hero sub said "price" → "Your quote on WhatsApp…"; stats, steps and CTA band all say quote). "Book a service" is the single primary CTA (nav, hero, end band, after phone).
- Supporting lines trimmed to ≤ 14 words (services intro, FAQ lead 17 → 11 words).
- CTAs verb-led: Book a service, Get a quote in 1 hour, Ask on WhatsApp. No banned heading formulas. All prices show units (from / car, / axle, / scan).

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures, no text < 13px, no pills < 44px (nav links raised to 44px targets; BEFORE phone "Read More" darkened to #767676 to pass 4.5:1).
- Most booked card + nav moved from translucent fills to solid tokens so the checker measures them. Check-by-eye: process caption sits on a bottom scrim; BEFORE hero text has a darkened photo; frame labels on sand are dark. All readable.
- "Most booked" uses words, not colour alone. Badge aria-hidden; WhatsApp buttons have aria-labels.

## 4. design:design-system (audit)
- All colours in `:root` (--ink, --ink-2, --ink-3, --paper, --paper-2, --line, --line-2, --acc, --acc-ink, glow/tint tokens, --dark, --glass, --pill, --wa, --wa-ink, --scrim); no hex/rgba in the rules (grep checked).
- Fonts: Schibsted Grotesk only. Gutter 56px, sections 112px. Radius 14/10px (soft).
- Must-haves: nav CTA, CTA repeated in the end band, WhatsApp buttons, Rand prices, footer "Concept by CAAS Studios". Queue item records layout, sections, font, shape, mode.
