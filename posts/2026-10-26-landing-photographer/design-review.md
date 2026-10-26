# Design review: 2026-10-26-landing-photographer (Frame Nine)

Choices (design:design-system, pick): layout `editorial-split` (last 4: type-giant, bento, split-screen, inset-card), sections numbered-rows → photo-facts → pull-quote → menu-list (dark) → step-timeline → photo-band, font `serif` (prev sans), shape `sharp` (prev round), mode `light` (prev light; 2 in a row is the max). Accent wine #7A2338 (prev coral), dark #231B19, blush #EAD3D8 as second accent. Frame palette `pal-midnight` (last 3: espresso, butter, cloud; dark frame every ~3rd). UI board 02 (prev 01): split nav with centred serif wordmark, hairline rules, huge uppercase serif headline, avatar stack + small caps line, clipped-corner info card, black rotating-text badge overlapping the portrait.

## 1. design:design-critique
- recent_sites sheet: only site with a paper hero, uncropped tall portrait and no overlay; services as hairline numbered rows (no cards, no grid). Not alike any of the last 4.
- Found: row titles ("Full-day weddings", "Engagement shoots") wrapped to 2 lines → narrower number/price/thumb columns, 42px titles.
- Found: couple-bouquet photo used 3 times → portraits row uses camera-hands.
- Found: empty gap under the hero CTAs → portrait 800 → 740px, proof row no longer pushed down.
- Slide: tile buttons rendered as blue underlined links and the price collided with the button → white, nowrap, price stacked; info card widened so "Bo-Kaap" doesn't break.

## 2. design:ux-copy
- "Four ways to work together." (generic) → "How much of the day should I keep?"; "Four steps to your gallery." → "One call, one day, one gallery."
- Hero subline was 18 words → 12 ("Honest photos of your wedding: the nerves, the laughing, the last dance.").
- Slide tile CTAs "See the day" → "See full days"; "Plan yours" kept (short, verb-led).
- One term: "date" everywhere (Check your date ×4, badge "Check yours", band "Is your date still open?"); "photos" not "photographs". All prices show units (/ wedding, / 2 hours, / hour, / album, from).

## 3. design:accessibility-review
- tools/a11y_check.py: 0 contrast failures, no text < 13px, no pills < 44px.
- Check-by-eye: band copy sits on a left dark scrim (0.82); slide tiles have top + bottom scrims (0.8) behind titles, prices and buttons; frame labels on midnight are light. All readable in the render.
- "Most booked" marked with words. Rotating badge aria-hidden. Buttons are <a> with text.

## 4. design:design-system (audit)
- All colours live in `:root` (--ink, --ink-2, --ink-3, --paper, --card, --line, --line-dark, --acc, --acc-ink, --acc-2, --acc-2-ink, --dark, --on-dark, --on-dark-2, --wa, --wa-ink, scrims); no hex/rgba in the rules (grep checked).
- Fonts: Instrument Serif display + Schibsted body. Gutter 64px, sections 110px. Radius 2px (sharp).
- Must-haves: nav CTA, CTA repeated in the price list and the end band, WhatsApp buttons, Rand prices, footer "Concept by CAAS Studios". Queue item records layout, sections, font, shape, mode.
