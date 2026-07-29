# threadgrab-daily-article-2026-07-27-screenpipe.md

**Run date:** 2026-07-27
**Cron:** threadgrab-daily-article (autonomous)
**Heat source:** ⭐ 2026-07-27 daily briefing social #3 — Screenpipe (YC S26) Launch HN, 84p hot; local screen+audio memory for X/Bluesky/LinkedIn workflows

## What was drafted

Trilingual article (EN/PT/ID) on running Screenpipe as a local capture layer for social creators and then archiving the public result with ThreadGrab.

- **EN slug:** `screenpipe-social-content-capture-2026`
- **PT slug:** `screenpipe-captura-conteudo-social-2026` (PT verb form, ID-independent choice)
- **ID slug:** `screenpipe-capture-konten-sosial-2026` (ID uses the imported `capture` cognate)

## QA results

| Lang | Title chars | Desc chars | H2 | FAQ | hreflang | JSON-LD | Code blocks |
|---|---|---|---|---|---|---|---|
| EN | 54 | 140 | 9 | 5 | 4 (en/pt/id/x-default) | 3 | 2 |
| PT | 55 | 139 | 9 | 5 | 4 | 3 | 2 |
| ID | 53 | 145 | 9 | 5 | 4 | 3 | 2 |

All 7 gates pass. Code blocks byte-identical across the three language versions. hreflang mutual verification passes.

## Coverage / pitfalls (new)

### 1. PT/ID slug divergence for verb-noun compounds

The English title uses the noun phrase "Capture Workflows." PT uses the verb form "Guia de Captura" (capture guide). ID uses the borrowed verb `Capture` directly because the Indonesian lexicon already adopts the English noun; using `Panduan Tangkap Layar` would lose the Screenpipe brand keyword. Plan three distinct slugs when the title contains an English verb that's product-relevant.

### 2. `f-string ... \" ... \" ...` syntax trap

Python 3.11 f-strings do not allow backslashes in the expression part. The first build crashed with `SyntaxError: f-string expression part cannot include a backslash (line 306, column 107)` because the `lang_bar` was being generated with a conditional class attribute that embedded `\"`. Fix: precompute the attribute string outside the f-string and substitute the variable. Captured here for future cron use.

### 3. Description length required two trim cycles

EN description came in at 164 chars (over the 155 cap), then 156 after removing "the final" — still over. Final EN: 140 chars by trimming "Then" and "with ThreadGrab" while keeping the primary keyword "Screenpipe" near the front. Both PT (139) and ID (145) cleared the 70-155 range on the first rewrite because their languages are more compact. **Always validate description length in the same write step.**

### 4. Two code blocks used as canonical examples

The article includes two `<pre><code>` blocks drawn directly from the project README: the `npx screenpipe record / setup` pair and the `claude mcp add screenpipe -- npx -y screenpipe-mcp@latest` invocation. Both are kept byte-identical across EN/PT/ID per the cross-language identity rule.

## Discoverability updates

- `en/blog/index.html`, `pt/blog/index.html`, `id/blog/index.html` — new entry prepended (newest-first)
- `sitemap.xml` — three new `<url>` entries (en + pt + id) with `lastmod 2026-07-27` and full hreflang cross-links
- `llms.txt` — three new bullet entries inserted before the "## What ThreadGrab does" anchor
- `drafts/state.json` — 3 new entries appended (one per lang, total 120), `recent_topics` updated, `last_run = 2026-07-27`

## Status

- **DRAFT stage** — articles live in `drafts/articles/`. They have not been published to `en/blog/`, `pt/blog/`, `id/blog/` and the Cloudflare Pages project `threadgrab` has not been re-deployed.
- Preview URL: not generated (publish step pending user reply)
- Pending user reply: `publish` to move drafts to public blog directories and (with `CLOUDFLARE_API_TOKEN`) deploy via `wrangler pages deploy . --project-name=threadgrab`.

## Reference file

This file: `/root/threadgrab-site/drafts/references/threadgrab-daily-article-2026-07-27-screenpipe.md`
