# threadgrab-daily-article-2026-07-28-writemark.md

**Run date:** 2026-07-28
**Cron:** threadgrab-daily-article (autonomous)
**Heat source:** ⭐ 2026-07-28 daily briefing social #1 — Writemark (Show HN 2026-07-25, 53 points) zero-dependency web component for inline Markdown editing, highly relevant for threadgrab social creator + Markdown archive use case

## What was drafted

Trilingual article (EN/PT/ID) on embedding the Writemark web component on X, Bluesky, and LinkedIn archive pages, with a comparison table against EasyMDE / Toast UI / CodeMirror / Notion embeds, two canonical code snippets, and a FAQ on persistence + privacy.

- **EN slug:** `writemark-markdown-inline-editor-2026` (EN uses "Inline Editor")
- **PT slug:** `writemark-editor-markdown-embutido-2026` (PT uses "embutido" = embedded)
- **ID slug:** `writemark-editor-markdown-sebaris-2026` (ID uses "sebaris" = inline)

## QA results

| Lang | Title (raw) | Title (visible) | Desc chars | H2 | FAQ | hreflang | JSON-LD | Code blocks |
|---|---|---|---|---|---|---|---|---|
| EN | 59 | 46 | 148 | 8 | 6 | 4 (en/pt/id/x-default) | 3 | 2 |
| PT | 53 | 40 | 144 | 8 | 6 | 4 | 3 | 2 |
| ID | 52 | 39 | 149 | 8 | 6 | 4 | 3 | 2 |

All 7 gates pass. Code blocks byte-identical across the three language versions. hreflang mutual verification passes (each lang's hreflang for OTHER langs uses that lang's actual canonical, not a stale URL).

## Coverage / pitfalls (new)

### 1. Code-block content must be canonical commands, not localized prose

The first build crashed the byte-identity check (skill pitfall #4) because both code blocks contained prose that was translated into PT/ID. The screenpipe reference article had its code blocks (`npx screenpipe record`, `claude mcp add screenpipe`) byte-identical EN/PT/ID because they were pure commands/install snippets.

**Writemark's two snippets:**
1. The `<writemark>` install pattern (`<script type="module" src="..."><writemark>...`)
2. The `<writemark data-author="reader-corrections">` example

The install pattern is HTML/JS — it is already English. The example block contained prose ("The original post was published on X on July 28, 2026 and archived in Markdown with [ThreadGrab]") that I translated to PT and ID. **Fix:** rewrite the example block to use the canonical install snippet shape with a short, English, machine-translatable placeholder line ("Post published on X on 2026-07-28, archived as Markdown via [ThreadGrab]"). Code is the lingua franca; prose inside a code block must be English to satisfy the cross-language identity rule.

**Validation recipe (added to validate-writemark-article-2026.py):**
```python
en_c=re.findall(r'<pre><code>(.*?)</code></pre>',en,re.DOTALL)
pt_c=re.findall(r'<pre><code>(.*?)</code></pre>',pt,re.DOTALL)
id_c=re.findall(r'<pre><code>(.*?)</code></pre>',idc,re.DOTALL)
assert en_c == pt_c == id_c, "code blocks must be byte-identical"
```

### 2. Slug divergence for the noun "inline editor"

Three distinct slugs because the EN compound "inline editor" doesn't translate naturally:
- EN keeps "inline editor" (the term is widely used in web-component docs).
- PT translates to `editor embutido` (literally "embedded editor") because the more literal `editor em linha` is uncommon in Brazilian PT dev jargon.
- ID translates to `editor sebaris` (literally "one-line editor") because `editor inline` is also uncommon in ID dev jargon, and `sebaris` matches how Atlassian / Slack localizations handle inline-edit affordances.

The Writemark brand keyword stays in all three slugs so the search signal is preserved.

### 3. Description length passed first try (no trim cycle)

Per skill pitfall #1, EN copy is usually 5-10 chars longer than PT/ID. This time EN came in at 148 chars and ID at 149 chars (essentially equal — Indonesian naturally uses the same length range for this kind of description because of "untuk penyuntingan Markdown sebaris" being a longer natural-language equivalent of "for inline Markdown editing"). PT was 144 chars. All three landed in the 70-155 ideal range on the first attempt. Validation runs in the same write step caught the gate before any wasted rebuild.

## Discoverability updates

- `en/blog/index.html`, `pt/blog/index.html`, `id/blog/index.html` — new entry prepended (newest-first), screenpipe card pushed to position 2
- `sitemap.xml` — three new `<url>` entries (en + pt + id) with `lastmod 2026-07-28` and full hreflang cross-links. XML re-parsed cleanly: 70 url entries (45 EN, 11 PT, 11 ID blog posts + 3 homepages)
- `llms.txt` — three new bullet entries inserted before the "## What ThreadGrab does" anchor
- `drafts/state.json` — 3 new entries prepended (one per lang, total 123), `recent_topics` updated, `last_run = 2026-07-28`

## Status

- **DRAFT stage** — articles live in `drafts/articles/`. They have not been published to `en/blog/`, `pt/blog/`, `id/blog/` and the Cloudflare Pages project `threadgrab` has not been re-deployed.
- Preview URL: not generated (publish step pending user reply)
- Pending user reply: `publish` to move drafts to public blog directories and (with `CLOUDFLARE_API_TOKEN`) deploy via `wrangler pages deploy . --project-name=threadgrab`.

## Reference file

This file: `/root/threadgrab-site/drafts/references/threadgrab-daily-article-2026-07-28-writemark.md`

## Validator

`/root/threadgrab-site/drafts/validate-writemark-article-2026.py` — runs all 7 gates plus cross-language identity checks (code blocks + hreflang mutual verification). Cloned from `validate-screenpipe-article-2026.py`; only SLUGS, EXPECTED_TITLE, EXPECTED_CANONICAL differ.