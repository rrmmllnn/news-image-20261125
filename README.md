# The Day in 24 Hours — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/rrmmllnn/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/rrmmllnn/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image that sums up Wednesday 25 November 2026 as a 24-hour news wire:
a masthead naming the day, three large drawn scenes for the day's biggest
stories — tankers burning in the Strait of Hormuz, Asia's chip sell-off,
and Pakistan's first astronaut aboard Shenzhou-24 — and a two-column wire
with the rest of the day in order.

- 26 dated stories, 8 regions (Middle East, East Asia, South Asia, Pacific,
  Europe, North America, Africa, Latin America)
- Every story happened, or was first reported, on 25 November 2026; the
  date is checked in a box on the poster itself
- Lead times are exact UTC (Shenzhou-24 lift-off 00:18 GMT, docking
  03:56 GMT); the wire is ordered by time of day, not by fake minute stamps
- Sources: Reuters, AP, Nature, Just Security, Xinhua, Eurostat

## Files

- `entry.png` — the poster, 1024×1024
- `draw_timeline.py` — draws the poster with Pillow (local build step only)
- `main.py` — standard-library entry point: copies `entry.png` to the
  output directory, byte for byte

## Reproduce

```sh
python3 draw_timeline.py        # renders entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
cmp entry.png out/entry.png     # identical
```

Verified 26 November 2026: `draw_timeline.py` run twice gives the same
`entry.png` bytes (SHA-256 `9371333a…358f1fb`, 148,389 bytes, 1024×1024),
and `main.py` copies it byte-identically to the output directory.

MIT licensed.
