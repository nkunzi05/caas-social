# Design review: Greenline Gardens (landscaping & garden care), 2026-10-22

Choices: layout `split-screen`, sections `tabs · before-after-strip · timeline · map-hours · photo-band`, font `serif` (Instrument Serif display + Schibsted body), shape `sharp` (2px radius, hairline rules), mode `tinted` (pale sage page #EEF2E7 with forest sections). UI board 03 (italic accent word over a bold word with a full stop, "02/04" slide counter, dot pagination, lowercase logo with accent dot). Frame palette `butter` (last 3: cloud / sky / espresso; espresso was the dark one, so light now). Accent lime #D4E86A on forest #12301F (previous post cobalt).

## design-system
- Picked `split-screen`: the last 4 were photo-overlay ×2, type-giant, bento. Font, shape and mode all differ from the bakery post (mixed / soft / light).
- Audit: all colours (incl. scrims, glass, WhatsApp green, star) are `:root` tokens; no hex or rgba in the rules or inline styles. Local fonts only, 56px gutter, 104px section padding. Must-haves present: nav CTA, "Book a free garden visit" repeated in hero, plan card, services and final band, WhatsApp buttons (aria-labelled), Rand prices with units, "Concept by CAAS Studios" footer.

## design-critique
- recent_sites.py sheet: none of the last 4 open on a 50/50 solid-panel + photo-collage hero; services are tabs + a typographic price list (not 3 cards), process is a horizontal timeline (not step rows), plus a map/hours block none of them had.
- Fixed: the plan card's lime button had invisible text (class clash `.acc`; renamed); hero left a big empty gap under the CTA (new 2-line headline "Your garden, already done." at 118px); map route line crossed the suburb labels (removed); week labels on the bright deck photo needed a stronger scrim; final-band italic line wrapped mid-phrase (forced its own line).
- Copy too close to earlier posts: "From first visit to first cut" (gym/wedding used the same formula, and it's a banned "From A to B") → "Quote in a day. First cut in five."; "Your first garden visit is on us" (gym: "Your first week is on us") → "Walk your garden with us, free."

## ux-copy
- One term for the action: "garden visit" everywhere ("Book a free garden visit", timeline step 1, hours row; "Free quote visits" renamed). Slide CTAs: A "Book visit", B "Book a free visit".
- Trimmed supporting lines over 14 words (services intro, lawn-care lead); eyebrow shortened to "Southern Suburbs · Cape Town". No banned heading formulas.
- Every price has a unit: R1,450 / month, R2,600 / month, from R1,200, R95 / m².

## accessibility-review
- `tools/a11y_check.py`: 0 contrast failures (first run flagged the A card's ★ at 2.04:1 on white; now a dark amber token, ≥4.5:1). No text under 13px; buttons 48–74px.
- Check by eye: plan card text sits on 78% forest glass; week chips are solid lime; strip labels and the final band sit on a 72% forest scrim; frame labels read on the butter frame; B card copy sits on solid forest below the masked photo.
- No meaning by colour alone: "Most booked" chip has words; the active tab is marked by an underline and darker text.
