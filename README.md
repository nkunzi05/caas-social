# caas-social

Automated Instagram content for **CAAS Studios** (@prosper.builds).

Every weekday at 10:00 (Cape Town time) a scheduled Claude task:
1. takes the next item from `content/queue.json` (rotating four formats: A vs B comparison, photo landing page, before vs after, and a 4-slide homepage showcase carousel),
2. pulls free Unsplash photos for that industry into `stock/` (via the "Fetch stock photos" GitHub workflow), designs the post from the approved examples in `posts/_examples/` and renders it to a 1080×1350 JPG,
3. commits them to `posts/`,
4. publishes the carousel to Instagram through Metricool.

The steps it follows are in [`RUNBOOK.md`](RUNBOOK.md). Brand colours and fonts live in `brand/brand.css`.

To change what gets posted, edit `content/queue.json` — reorder, delete or add items.
This repo must stay **public**: Metricool downloads the images from here.
