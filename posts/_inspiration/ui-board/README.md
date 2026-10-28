# UI inspiration board (from Prosper, 2026-10-16)

Hero / landing-page styles Prosper wants the posts to draw from.

**Since 2026-10-28 (Prosper): headers and hero sections take their theme from 01 and 03 together** (dark stage, focal subject floating on a matching dark ground with a coloured glow, pill nav, italic-over-bold headline, counter/arrows/dots, rotating badge). 02 stays only as a reference for lower sections. Borrow the *design language and UI details* only.
Never copy their names, logos, wording, artwork or exact layout. Every business stays invented, with fresh copy and our own Unsplash photos.

## 01-dark-neon-agency.jpg: dark hero with a glowing focal object
- Near-black canvas that warms into a deep violet/magenta glow behind one big focal object (in our posts: a cut-out product or tool photo, or a strong photo with a coloured glow behind it).
- Small wide caps line ("WE ARE") above a giant, wide, uppercase display word (Schibsted Grotesk 800, tight, all caps).
- Floating pill nav bar (dark glass, rounded), active link marked with a short accent underline, "Start a project" as a lighter pill inside the bar.
- Toggle-style CTA: a grey pill with a round icon button (phone) attached on the right.
- Circular rotating-text badge ("SCROLL TO EXPLORE · ") with an arrow in the middle, at the bottom of the hero.
- Small vertical slide indicators on the right edge, ← → arrows bottom right, social icons bottom left.

## 02-editorial-serif-cream.jpg: editorial serif on warm cream
- Warm cream/paper background, thin hairline rules separating nav, hero and footer.
- Split nav: links left, serif wordmark centred, links + black "Log in" pill right.
- Huge 3-line UPPERCASE serif headline (Instrument Serif, tight leading).
- Avatar stack (3 overlapping circles) + a small caps community line ("JOIN OUR 150K+ …"), under a hairline rule.
- Soft pastel pill CTA (lilac) with a ↗ arrow.
- Info card with one clipped corner: small thumbnail + 2 lines of text + outline pill tags.
- Big rounded-corner portrait image on the right, with a black circular rotating-text badge ("Subscribe to … newsletter") overlapping its left edge, with an accent dot in the centre.

## 03-dark-cutout-script.jpg: dark cut-out subject + script accent word
- Dark espresso/charcoal background matching the photo's backdrop, so the subject looks cut out and floats (choose photos shot on a plain dark background).
- A small handwritten/italic accent word in orange (use Instrument Serif italic in the accent colour) sitting above a big bold sans word ending with a full stop ("pure / cuteness.").
- Slide counter "02/04" in the accent colour beside a short 3–4 line description.
- Thin outline arrows far left/right, dot pagination at the bottom with the active dot in the accent colour.
- Minimal nav: lowercase logo letter with an accent-coloured dot, 3 small links, two-line hamburger on the right; tiny © line bottom left.

---

# Board additions (from Prosper, 2026-10-28): 04–10
Use these together with 01 + 03 for the **header and hero**, and as the theme for the matching **lower sections** (pricing, FAQ, galleries). Same rules: borrow design language only. Never copy names, logos, wording, artwork, or any photo of a real person (several boards show athletes and musicians: we always use our own Unsplash photos of anonymous people at work).

## Heroes
### 04-giant-word-behind-subject.jpg: giant word with the subject in front of it
- A huge thin-to-regular sans word ("MOVE FASTER" style) spans the full width; the photo subject overlaps it, so part of the word sits behind the subject (layer: word → subject → small UI).
- Tiny two-line labels pinned to the corners and above the word; a two-line statement in light grey bottom-left ("GAME ON, / PLAY HARD").
- Small floating glass cards on the photo: a featured item card with thumbnail, and a big stat card ("18K+") with an avatar stack.
- Section after it: a giant two-tone headline (grey + black words) with a tilted, rounded photo card cutting through the middle of it, round stat bubble, "#01" note card, ‹ › carousel buttons; facilities as rounded photo cards with glass captions.
### 05-sport-gradient-cutout.jpg: cut-out subject on a vivid gradient
- Violet → orange → pink gradient ground; a cut-out subject in motion breaks out of the frame edge.
- Massive condensed caps title (Anton), often stepped over two lines (second line indented).
- Vertical progress pill "01 / 07" at the right edge; small description bottom-left; glass info tiles with a small accent dot; a column of rounded photo thumbnails on the right.
### 06-dark-circle-statue.jpg: duotone subject on a big circle
- Charcoal ground, one big accent circle (plus a smaller one cut by the bottom edge) behind a duotone/tinted subject that overlaps the circle.
- Small caps eyebrow, one bold caps word, two-line description, round outline arrow button + "See more" label, "01 —— 03" progress line bottom-left. Minimal nav, small geometric logo mark.

## Pricing sections
### 07-pricing-word-behind-glass.jpg
- Black page, floating pill nav with the active item, a giant white word ("Pricing") that sits *behind* three frosted-glass plan cards (the word blurs where the cards overlap).
- Middle plan's button is solid white, the others outline; check-circle feature rows; a toggle switch ("Billed yearly") under the cards.
### 08-pricing-glow-featured.jpg
- Rating pill on top, two-line caps headline with a soft gradient, Month/Year segmented toggle with a glowing active pill.
- Three dark cards; the featured middle card glows in the accent colour (dot-grid texture, light from the bottom); price big + unit small and grey; a glowing horizon arc under the cards.

## FAQ sections
### 09-faq-glow-accordion.jpg
- Huge thin "FAQ" title. Each question is a dark rounded row with a warm accent glow bleeding in from the left edge, caps questions, a thin + / − on the right; the open row shows a small answer paragraph.

## Galleries / carousels
### 10-coverflow-glass-player.jpg
- Coverflow carousel: centre card large and sharp, side cards smaller and angled back, glass caption plates under each card, warm blurred background from the main photo.
- A long glass control bar under it (prev / pause / next, mini thumbnail + title, icons). For our sites: a gallery of jobs/rooms/dishes with a glass caption bar, or a "before / after" coverflow.

## How to use them (per post)
- Hero: combine 01 + 03 with ONE of 04 / 05 / 06 (rotate, record e.g. `"ui_ref": "03+01+05"`). 04 suits light/tinted pages, 05 bold sports/fitness/youth brands, 06 dark premium brands.
- Lower sections: when the section mix has pricing, FAQ or a gallery, theme it from 07/08, 09 or 10 (record `"ui_sections": ["08","09"]`). Keep contrast rules: text on glass/glow still needs a solid enough shade to pass `tools/a11y_check.py`.
