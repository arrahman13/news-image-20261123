[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/arrahman13/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/arrahman13/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World in One Day — Monday 23 November 2026

A one-page newspaper front page summing up Monday 23 November 2026's world
news in a single 1024×1024 image: 35 stories, every one dated that Monday
and named with its outlet — 3 illustrated leads, 13 cards, 19 briefs, a UTC
timeline, a region tally, and a dark world map with numbered pins for all
35 stories. Every story is tagged REPORTED / CLAIM / FORECAST (legend on the
page), and a date-check box lists other days' news that was deliberately
left out.

## How to run

```sh
python3 build_image.py   # renders entry.png (deterministic)
python3 main.py          # copies entry.png into ./output/ (or $MAKEFUN_OUTPUT_DIR)
```

`main.py` only copies the committed `entry.png` and verifies it against the
committed SHA-256; it never renders. All drawing is done in code with Pillow
in `build_image.py` — no photos, no downloads, no network.

## License

MIT — see LICENSE.
