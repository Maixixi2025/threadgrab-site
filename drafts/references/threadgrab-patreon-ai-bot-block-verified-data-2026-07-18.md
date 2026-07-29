# threadgrab Patreon AI-Bot-Block Article — Verified Data (2026-07-18)

## Source

- **Article:** Patreon stops asking AI bots not to scrape — and starts blocking them
- **Outlet:** TechCrunch
- **Author:** Sarah Perez (Consumer News Editor)
- **Published:** 2026-07-17 15:21:17 +00:00
- **URL:** https://techcrunch.com/2026/07/17/patreon-stops-asking-ai-bots-not-to-scrape-and-starts-blocking-them/
- **Verified via:** direct urllib.request fetch 2026-07-18, 234KB HTML, JSON-LD `NewsArticle` block parsed cleanly + 4,366-char entry-content extracted

## Key facts (verbatim or close paraphrase from source)

1. **Policy shift:** Patreon switched from asking AI bots to stop scraping via robots.txt to actively blocking them. They extended their existing Cloudflare partnership to use Cloudflare's **AI Crawl Control** technology.

2. **Test result:** In Patreon's pre-launch testing, "individual AI training crawlers' weekly attempts went from thousands of attempts to zero" once the new block went live. This is the proof point for "robots.txt is not enforcement."

3. **Background:** Patreon's paywall already locked most creator content from crawlers. New discovery surfaces (redesigned Home Feed, "Quips" tweet-like short posts) increased crawler exposure and triggered the policy upgrade.

4. **Cloudflare technology:**
   - **AI Crawl Control** — fingerprint-and-behavior filter that inspects requests and blocks training crawlers at the edge before they hit origin.
   - **Pay Per Crawl marketplace** — opt-in revenue path letting publishers charge AI bots per scrape.
   - **July 2026 default-block policy** for "mixed-use" crawlers (those that both index for search and train models) on any page that hosts ads.

5. **Allowed bots:** Patreon will still allow bots that index pages and organize information that sends users back to the platform (legitimate search-indexing crawlers).

6. **Patreon product chief Drew Rowny quote:** "Consent shouldn't depend on whether a scraper chooses to behave."

7. **Partners/affects:** Cloudflare (technology partner); Patreon product chief Drew Rowny (named speaker).

## Compliance-strategy framework (author-derived)

The 5 strategies distilled from Patreon's enforcement pattern + Cloudflare's policy model:

1. Treat robots.txt as advisory, never as authorization
2. Maintain a per-platform opt-out registry (Patreon, Substack, Beehiiv enforce; list changes monthly)
3. Distinguish search-index crawlers (allowed) from training crawlers (blocked or Pay Per Crawl)
4. Switch from frequency-based throttling to behavior-based throttling (Cloudflare looks at request shape, not rate)
5. Keep an audit trail that survives a takedown request (append-only JSONL keyed by intent + policy-check)

## ThreadGrab product framing (article's call-to-action)

Three product changes referenced in the article:

- **/api/policy** — exposed endpoint that returns the current platform-domain-to-policy-version registry
- **/api/audit** — exposed endpoint for per-fetch audit-log query (date + intent)
- **MCP endpoint default** — `archive_for_user` classification by default for agent-driven fetches

## Article structure (verified post-write)

| Lang | Slug | Title (visible) | Title chars | Desc chars | H2 | H3 | FAQ | <p> | code |
|---|---|---|---|---|---|---|---|---|---|
| en | patreon-ai-bot-block-compliance-threadgrab-2026 | Patreon AI Bot Block: 5 Compliance Strategies | 45 | 126 | 10 | 0 | 5 | 25 | 3 |
| pt | patreon-bloqueio-bot-ia-conformidade-threadgrab-2026 | Patreon Bloqueia Bots IA: 5 Estratégias de Conformidade | 55 | 117 | 10 | 0 | 5 | 25 | 3 |
| id | patreon-blokir-bot-ai-kepatuhan-threadgrab-2026 | Patreon Blokir Bot AI: 5 Strategi Kepatuhan | 43 | 107 | 10 | 0 | 5 | 25 | 3 |

All 7 gates pass for each language. All 3 code blocks byte-identical across EN/PT/ID. All 3 hreflang pairs mutually consistent.

## Topic selection rationale

- Briefing date: 2026-07-18, item 1 under 📱 社交工具 (threadgrab / md2rich) section: ⭐ Patreon 转向封锁 AI bot (2026-07-17 TechCrunch)
- Picked over alternative threadgrab items because:
  1. Freshest verifiable source (2026-07-17, 1 day before cron run)
  2. Direct threadgrab angle: scrapers need compliance posture for creator platforms
  3. Concrete factual data (Cloudflare AI Crawl Control, Pay Per Crawl, Drew Rowny quote) for the 5-strategy framework
  4. Not yet covered in `state.published[]` (verified — no prior Patreon slug in 99 published entries)

## Cluster cross-link candidates (for future articles)

If a follow-up article runs in the next 30 days, cluster candidates:
- 2026-07-13 tweet-md-browser-redirect (X to markdown redirect) — parallel "platform-aware tool" angle
- 2026-07-10 linkedin-ai-long-form-rewrite (LinkedIn compliance) — same creator-platform AI-detection theme
- 2026-07-12 ai-writing-tropes-tropes-fyi (AI writing patterns) — same AI-detection/trust framing
- 2026-07-17 bluesky-starter-packs (creator growth) — creator-platform growth parallel

This article is the 4th of the cluster on creator-platform compliance + AI-detection; the existing 3 above provide 2-way cross-link material.

## Known gaps

- **Patreon API endpoint** not explicitly tested in the article. The Cloudflare AI Crawl Control is referenced via the source's reporting, but the actual API integration is the user's responsibility.
- **Substack / Beehiiv policy enforcement** mentioned in Strategy 2 but not independently verified. Cited as "growing list" per TechCrunch's framing.
- **Pay Per Crawl pricing** not quoted in the article — the marketplace exists but per-request pricing is not publicly itemized.
