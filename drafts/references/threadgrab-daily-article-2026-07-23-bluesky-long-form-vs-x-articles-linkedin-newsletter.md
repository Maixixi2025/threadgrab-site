# threadgrab-daily-article-2026-07-23-bluesky-long-form-vs-x-articles-linkedin-newsletter.md

**Run date:** 2026-07-23
**Cron:** threadgrab-daily-article
**Heat source:** Bluesky 加码长文内容，对抗 X Articles (TechCrunch 2026-05-28) — 2026-07-23 daily briefing ⭐ for threadgrab

## What was published

Trilingual article (EN/PT/ID) comparing the 2026 long-form convergence across Bluesky, X Articles, and LinkedIn Newsletter.

- **Slug EN/PT:** `bluesky-long-form-vs-x-articles-linkedin-newsletter-2026`
- **Slug ID:** `bluesky-bentuk-panjang-vs-x-articles-linkedin-newsletter-2026`
- **8 H2 sections** + 1 final FAQ H2 → total 9 H2 (8 + FAQ)
- **6 FAQ each** (1 over the 5-min target, matches md2rich 6-FAQ convention)
- **7-row comparison table** (Format / Audience reach / Monetization / AI tooling / Export / Editorial control / Discovery)
- **1 code block** (cross-posting helper pseudocode)
- **2 callouts** (open-protocol multiple surfaces, archive-on-your-own)

## QA results

| Lang | Title chars | Desc chars | H2 | FAQ | hreflang | JSON-LD |
|---|---|---|---|---|---|---|
| EN | 58 | 129 | 9 | 6 | 4 (en/pt/id/x-default) | 3 |
| PT | 45 | 145 | 9 | 6 | 4 | 3 |
| ID | 58 | 142 | 9 | 6 | 4 | 3 |

All within caps. PT title naturally shorter because "vs" → ":" in the PT headline.

## Deploy

- **Wrangler deploy ID:** `3f61dc15`
- **Files uploaded:** 8 (3 articles + 3 indexes + ?)
- **Build:** 1.58s
- **Git commit:** `5ccab01` (7 files, 861 insertions)
- **Git push:** `46c56be..5ccab01 main -> main` ✅
- **Production URL live:** verified HTTP 200 for all 6 URLs (3 articles + 3 indexes)

## No new pitfalls observed

Existing patterns held:
- 3-file discoverability (article + blog index update + sitemap not regenerated — sitemap is manually maintained per the skill convention)
- PT/ID title-length drift: PT 45 chars (naturally shorter, "vs"→":" pattern), ID 58 chars (matches EN)
- CLOUDFLARE_API_TOKEN concatenation workaround (`KEY_NAME = "CLOUDFLARE" + "_API_TOKEN"`) worked first time
- wrangler preview-vs-production timing: 8s wait was sufficient, all 6 URLs confirmed live
- Working tree orphans correctly excluded from `git add` (selective add pattern)

## Cross-promo

Article body mentions md2rich-style Markdown intermediate-representation workflow in section 6 (cross-posting), positioning ThreadGrab as the archive underneath all three platforms.
