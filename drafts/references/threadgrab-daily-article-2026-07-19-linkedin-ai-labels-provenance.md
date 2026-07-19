# threadgrab-daily-article-2026-07-19-linkedin-ai-labels-provenance

## Topic

LinkedIn's 2026 AI-content labels and how to archive them with provenance metadata.

## Heat source

briefing-2026-07-19 (The Register, 2026-07-09):
- "25% of long-form social posts on LinkedIn and X are now flagged as AI-generated"
- https://www.theregister.com/ai-and-ml/2026/07/09/ai-slop-writing-has-taken-over-the-internet-particularly-linkedin-and-x/5269525

## Slug

`linkedin-ai-content-label-provenance-2026`

## Article specs

- 8 H2 + 5 H3 FAQ
- 2 byte-identical code blocks across EN/PT/ID (bash curl + Python)
- 1,750 words (EN)
- 7-gate pre-deploy verification: ✓ all pass on all 3 languages
- 3 JSON-LD blocks per lang: Article + BreadcrumbList + FAQPage

## Article structure

1. What LinkedIn's 2026 AI-label actually shows in the feed
2. Why "AI or not" is the wrong question for archivists
3. Three pieces of provenance worth capturing (ai_label_state, ai_label_source, ai_label_confidence)
4. A four-step capture workflow (with curl + Python sidecar code)
5. How threadgrab's Markdown export carries the label through
6. Comparison: X's Grok-label vs Bluesky's no-label
7. What to watch over the next 30 days (C2PA, disputes, retroactivity)
8. FAQ (5 questions)

## Verification (live HTTP 200 + correct content)

| Lang | URL | Live title | Status |
|---|---|---|---|
| EN | https://threadgrab.com/en/blog/linkedin-ai-content-label-provenance-2026.html | LinkedIn AI Labels 2026: Archive Provenance | ✓ 200, 22,995 B |
| PT | https://threadgrab.com/pt/blog/linkedin-ai-content-label-provenance-2026.html | Rótulos de IA do LinkedIn 2026: Procedência no Arquivo | ✓ 200, 23,898 B |
| ID | https://threadgrab.com/id/blog/linkedin-ai-content-label-provenance-2026.html | Label Konten AI LinkedIn 2026: Arsip dengan Provenansi | ✓ 200, 24,039 B |

## Index + sitemap updates

- en/blog/index.html: top entry = new article
- pt/blog/index.html: top entry = new article
- id/blog/index.html: top entry = new article
- sitemap.xml: +3 URL entries (55 → 58)

## Git workflow

- selective `git add` for 8 files (skipped patreon-ai-bot-block drafts + pre-existing dirty tree)
- commit `54738e3` pushed to origin main (42ea450..54738e3)
- Git auto-deploy verified at 60s edge propagation

## state.json

- published[] +3 entries (en/pt/id), 99 → 102
- status: published for all 3 langs
- heat_source: briefing-2026-07-19-the-register-ai-slop-writing-x-linkedin

## Differentiator from existing articles

- ai-social-content-provenance-2026 (preview_pending_publish, on disk): covers creator-side disclosure + binary detection
- linkedin-ai-long-form-rewrite-workflow-2026: covers AI-assisted CREATION
- linkedin-long-form-post-embarrassing-era-2026: covers algorithm era
- linkedin-newsletter-archive-tool-2026: covers newsletter archiving

This article covers the UNIQUE angle of platform-side LABELING (classifier, disclosure, C2PA manifest) and how to capture the label itself as forward-compatible provenance metadata.
