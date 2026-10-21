# Design review: Rise Bakehouse (artisan bakery), 2026-10-21

Choices: layout `bento`, sections `menu-list · bento-features · founder-quote · faq-accordion · split-form`, font `mixed` (bold Schibsted + Instrument Serif italic accent word), shape `soft` (14px tiles, full pills), mode `light` (warm paper #FBF7F0), UI board 02 (hairline split nav with centred wordmark, avatar stack, clipped-corner info card, circular rotating-text badge with an accent dot). Frame palette `espresso` (dark frame; last 3 were sand / none / sky). Accent cobalt #2547C4 + butter #F4C64E (previous post aqua; the 2026-10-15 bakery used terracotta, so avoided).

## design-system
- Picked `bento`: the last 4 were photo-overlay ×3 and type-giant. Font, shape and mode all differ from the car-wash post (condensed / sharp / tinted).
- Audit: colours only as `:root` tokens (incl. `--wa` for the WhatsApp green); no raw hex in rules. Local fonts only, 56px gutter, 104px section padding. Must-haves present: nav CTA, repeated final CTA ("Pre-order for tomorrow"), WhatsApp buttons, Rand prices with units, "Concept by CAAS Studios" footer.

## design-critique
- recent_sites.py sheet: the four previous sites all open on a dark full-bleed photo/display hero; this one opens on a light 6-tile bento grid with no photo overlay. No 3-card row, no dark 3×2 grid, no step rows, so the section order is new as well. Also checked against the 2026-10-15 bakery (serif editorial, terracotta): different headline, location (Sea Point), accent and structure.
- Fixed: the after phone had a big empty band above the CTA (taller bento tiles, shorter phone); the hours tile wrapped to 2 lines (nowrap, 26px); the slide question wrapped tightly onto the tags (62px, phone 866px); the baker quote left an orphan "in." (shorter quote).
- BEFORE phone is a plausible Arial template (welcome line over a dimmed photo, About Us, grey boxes, "contact us", Read More, © 2019) — forgettable, not broken. AFTER clearly wins.

## ux-copy
- One term for the action: "Pre-order for tomorrow" in nav, hero, phone and final form; "pre-order" everywhere (never "order online"/"reserve").
- Headlines are specific: "Warm loaves by half past six.", "Tonight's bake, priced before you walk in.", "Slow dough. Early ovens.", "Your loaf, waiting at 6:30." None of the banned formulas.
- Trimmed two supporting lines over 14 words (hero subline, menu intro). Every price has a unit (/ loaf, each, / slab, / 20 cm, extra; delivery R35 per order).

## accessibility-review
- `tools/a11y_check.py`: 0 contrast failures (first run flagged the BEFORE phone's 13px contact line 4.48:1 and the "Read More" button 2.66:1; darkened both). No text under 13px, buttons 46–58px, FAQ toggles and time chips 44px.
- Check by eye: rotating badge text is white on a solid ink circle; frame labels (eyebrow, question, Before/After tags, sig) read on the espresso frame; the BEFORE welcome line sits on a 60%-dimmed photo. Photo labels sit on solid paper pills.
- No meaning by colour alone: "Most ordered" / "Sells out by 10" chips carry words; the open FAQ row has a − sign.
