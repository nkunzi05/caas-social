# caas-social

Automated Instagram content for **CAAS Studios** (@prosper.builds).

Every weekday at 10:00 (Cape Town time) a scheduled Claude task:
1. takes the next item from `content/queue.json` (alternating concept websites and website tips),
2. designs the slides and renders them to 1080×1350 JPGs,
3. commits them to `posts/`,
4. publishes the carousel to Instagram through Metricool.

The steps it follows are in [`RUNBOOK.md`](RUNBOOK.md). Brand colours and fonts live in `brand/brand.css`.

To change what gets posted, edit `content/queue.json` — reorder, delete or add items.
This repo must stay **public**: Metricool downloads the images from here.
