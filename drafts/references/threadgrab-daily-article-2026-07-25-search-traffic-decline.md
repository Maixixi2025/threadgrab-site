# threadgrab daily article: Search Traffic Decline 2026

**Date:** 2026-07-25 (Saturday)
**Slug:** `search-traffic-decline-social-archive-2026`
**Deployment:** `04652f38` (wrangler pages deploy)
**Files:** 7 new uploaded (3 article files + 3 blog indexes + state.json)

## Topic
NiemanLab search traffic decline story (publishers consider opting out of Google). Framed for social content creators: platform diversification + Markdown archiving as insurance against search-driven traffic volatility.

## Source
daily-briefing-2026-07-25: SEO section #1 — "publishers consider opting out of Google" (NiemanLab, 37p HN). Not covered on threadgrab before.

## Stats
- **EN:** 7 H2 sections, 5 FAQ, 3 JSON-LD blocks, title=51/60, desc=153/155
- **PT:** 6 H2 sections, 5 FAQ, 3 JSON-LD blocks, title=59/60, desc=155/155
- **ID:** 6 H2 sections, 5 FAQ, 3 JSON-LD blocks, title=54/60, desc=141/155

## Pitfalls encountered
1. **Title-length drift on translation** — EN at 51 was fine, but PT auto-expanded to 70 and ID to 74 from longer Portuguese/Indonesian phrases. Required title rewrites for all 3.
2. **f-string backslash issue** — building lang-bar with `\"` inside f-string caused `SyntaxError`. Fixed by extracting `make_lang_bar()` to a separate function using conditional variables.
3. **og:description drift from meta description** — after patching `meta name="description"`, `og:description` and `twitter:description` still held the old longer version. Required second patch pass across all 4 description locations.
4. **CF edge propagation for subdirectories** — EN went live immediately but PT/ID served fallback redirect page for ~10 seconds longer before propagating.
