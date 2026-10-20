# Design review: Gloss Bay (car wash), 2026-10-20

Choices: layout `type-giant`, sections `scroller · big-numbers · testimonial · timeline · giant-type CTA`, font `condensed` (Anton + Schibsted), shape `sharp` (3px), mode `tinted` (icy #E4EDF0 page, dark hero), UI board 01 (floating pill nav with an accent underline, a giant display word, a glowing focal photo, a toggle CTA with a phone button, a rotating badge, vertical slide indicators).

## design-system
- Picked `type-giant`. The last 4 posts were editorial-split and photo-overlay ×3. Type, shape and mode all differ from the wedding post (serif/round/light).
- Tokens live only in `:root` (ink, paper, acc, dark, on-dark, --r). Accent changed from the previous post's blush to aqua #38D9E8 with dark ink #04252B on it.
- Audit: no stray hex values in the rules except the WhatsApp green. Must-haves are present: nav CTA, final CTA, WhatsApp button, Rand prices with units, "Concept by CAAS Studios".

## design-critique
- Compared with the last 4 sites (tools/recent_sites.py): no shared hero composition, and no 3-card / 3×2-grid / step-rows pattern. It reads as a different studio style.
- Fixed: the kick line touched the giant word (moved it to 120px and pushed the word down). There was an empty band between the word and the copy, so the copy and rating moved up. The badge text overlapped itself, so it was shortened and re-spaced. In the CTA, the accent "." block overflowed into the label, so it's now a separate square. The process section's two photos repeated hero/card photos, so they were removed.
- Slide 1: the first crop cut through the services headline. It's now two crops (hero + ticker, then the service strip), each ending on a full section.
- Photos: Mercedes and BMW badges were avoided. The interior photo is cropped to the seats and the wax photo to the headlight side. Two photos with a visible badge or plate were dropped.

## ux-copy
- CTA is "Book a bay" everywhere (nav, hero toggle, final CTA). There's one term for the booking unit, "bay".
- Headlines say something specific: "Pick your shine. Pay when it's done.", "Book. Drop. Collect.", "Book a bay." None of the banned formulas are used.
- Every price has a time next to it (20 min, 1 h 30 …). The slide question changed from "Book your wash in 40 seconds" (clashed with the "40 min" stat) to "Skip the Saturday queue."

## accessibility-review
- `tools/a11y_check.py`: 0 contrast failures. The 12px badge text was raised to 13px. Buttons are 48–56px tall.
- Text over the photo (the frame price tag) sits on a 78% dark panel. The white card numbers have a text shadow and were checked in the render.
- Meaning isn't carried by colour alone: the "Most booked" chip has text, and the dark card also has the chip.
