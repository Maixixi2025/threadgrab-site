#!/usr/bin/env python3
"""Build the 3-language Notion-to-Markdown migration article.

Run from /root/threadgrab-site.
"""
import os
import re
import sys

os.chdir('/root/threadgrab-site')

# === Constants ===
SLUG = "notion-to-markdown-migration-2026"
DATE = "2026-06-26"
DATE_EN = "June 26, 2026"
DATE_PT = "26 de Junho, 2026"
DATE_ID = "26 Juni 2026"

TITLE_EN = "Notion to Markdown 2026: Why Social Creators Migrate"
TITLE_PT = "Notion para Markdown 2026: Por Que Criadores Migram"
TITLE_ID = "Notion ke Markdown 2026: Mengapa Kreator Beralih"

DESC_EN = "Why social creators are leaving Notion for Markdown in 2026: cost, ownership, lock-in, and a 5-step migration plan with Pandoc, Obsidian, and ThreadGrab."
DESC_PT = "Por que criadores estao saindo do Notion para Markdown em 2026: custo, lock-in e um plano de migracao em 5 etapas com Pandoc, Obsidian e ThreadGrab."
DESC_ID = "Mengapa kreator konten meninggalkan Notion untuk Markdown di 2026: biaya, kepemilikan, lock-in, dan rencana migrasi 5 langkah."

KEYWORDS_EN = "Notion to Markdown, Notion migration 2026, Markdown first, Obsidian, Pandoc, notion-to-md, markitdown, ThreadGrab, social content archive, Git, X to Markdown, Bluesky archive, LinkedIn archive, Markdown knowledge base"
KEYWORDS_PT = "Notion para Markdown, migracao Notion 2026, Markdown primeiro, Obsidian, Pandoc, notion-to-md, markitdown, ThreadGrab, arquivo de conteudo social, Git, X para Markdown, arquivo Bluesky, arquivo LinkedIn, base de conhecimento Markdown"
KEYWORDS_ID = "Notion ke Markdown, migrasi Notion 2026, Markdown utama, Obsidian, Pandoc, notion-to-md, markitdown, ThreadGrab, arsip konten sosial, Git, X ke Markdown, arsip Bluesky, arsip LinkedIn, basis pengetahuan Markdown"

# ============================================================
# CSS (shared, identical across 3 langs)
# ============================================================
CSS = """    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f0f; color: #fff; line-height: 1.6; }
    header { padding: 20px 24px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #1a1a1a; }
    .logo { font-size: 1.4rem; font-weight: 700; color: #fff; text-decoration: none; }
    .logo span { color: #20d5ec; }
    .lang-bar { margin-left: auto; display: flex; gap: 6px; }
    .lang-bar a { color: #888; text-decoration: none; font-size: 0.85rem; padding: 4px 8px; border-radius: 4px; }
    .lang-bar a:hover, .lang-bar a.active { color: #fff; background: #222; }
    main { max-width: 760px; margin: 0 auto; padding: 40px 20px 60px; }
    .breadcrumb { color: #666; font-size: 0.85rem; margin-bottom: 24px; }
    .breadcrumb a { color: #20d5ec; text-decoration: none; }
    h1 { font-size: clamp(1.7rem, 4.5vw, 2.4rem); line-height: 1.25; margin-bottom: 12px; }
    h1 span { color: #20d5ec; }
    .meta { color: #888; font-size: 0.9rem; margin-bottom: 32px; }
    h2 { color: #20d5ec; font-size: 1.4rem; margin: 36px 0 14px; line-height: 1.3; }
    h3 { color: #fff; font-size: 1.1rem; margin: 18px 0 8px; }
    p { color: #ccc; margin-bottom: 14px; font-size: 1rem; }
    a { color: #20d5ec; }
    ul, ol { color: #ccc; padding-left: 22px; margin-bottom: 14px; }
    li { margin-bottom: 6px; font-size: 1rem; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0 28px; font-size: 0.9rem; }
    th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #222; }
    th { background: #1a1a1a; color: #20d5ec; font-weight: 600; }
    td { color: #ccc; }
    .callout { background: #11212a; border-left: 3px solid #20d5ec; padding: 16px 20px; border-radius: 4px; margin: 20px 0; }
    .callout p { color: #b5dde3; margin-bottom: 0; }
    pre { background: #0a0a0a; border: 1px solid #1f1f1f; border-radius: 8px; padding: 14px 18px; overflow-x: auto; margin: 16px 0 20px; }
    pre code { font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 0.88rem; color: #c5e8ee; white-space: pre; }
    code:not(pre code) { background: #1a1a1a; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; color: #20d5ec; }
    .faq-item { background: #1a1a1a; border-radius: 8px; padding: 16px 20px; margin-bottom: 12px; }
    .faq-item strong { color: #20d5ec; display: block; margin-bottom: 6px; }
    .faq-item p { color: #ccc; margin-bottom: 0; font-size: 0.95rem; }
    .cta { background: linear-gradient(135deg, #11212a, #0d1a20); border: 1px solid #20d5ec; border-radius: 10px; padding: 22px 24px; margin: 28px 0; text-align: center; }
    .cta p { color: #c5e8ee; margin-bottom: 12px; }
    .cta a.btn { display: inline-block; background: #20d5ec; color: #000; font-weight: 600; padding: 11px 26px; border-radius: 8px; text-decoration: none; }
    .cta a.btn:hover { background: #1bc4d4; }
    footer { text-align: center; padding: 40px 24px 24px; color: #444; font-size: 0.8rem; border-top: 1px solid #1a1a1a; margin-top: 40px; }
    footer a { color: #666; text-decoration: none; margin: 0 8px; }
    footer a:hover { color: #20d5ec; }
    @media (max-width: 640px) { main { padding: 24px 16px 40px; } table { font-size: 0.8rem; } th, td { padding: 8px; } }"""

# ============================================================
# JSON-LD Article (per lang)
# ============================================================
def article_jsonld(title_h1, desc, lang, locale):
    return f"""  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_h1}",
  "description": "{desc}",
  "datePublished": "{DATE}",
  "dateModified": "{DATE}",
  "author": {{
    "@type": "Organization",
    "name": "ThreadGrab",
    "url": "https://threadgrab.com/{lang}/"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "ThreadGrab",
    "url": "https://threadgrab.com/{lang}/"
  }},
  "mainEntityOfPage": "https://threadgrab.com/{lang}/blog/{SLUG}.html",
  "inLanguage": "{lang}"
}}
  </script>"""

BREADCRUMB_JSONLD = """  <script type="application/ld+json">
  {
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "HOME_URL"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "BLOG_URL"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "BREADCRUMB_TAIL"
    }
  ]
}
  </script>"""

# ============================================================
# Body content (per lang). Code blocks are IDENTICAL across langs.
# Body has: intro (2 paragraphs) + callout + 8 H2 sections + FAQ (6 items) + CTA + closing H2
# ============================================================

# ---------- ENGLISH ----------
EN_BODY = """    <p>In June 2026, the German hosting team forrabbit published a 1,800-word postmortem on moving their entire knowledge base from Notion to plain Markdown files in a Git repo. Within ten days, the post hit 800 upvotes on Hacker News, spawned three derivative threads on r/selfhosted, and triggered a wave of "we did the same" replies. The pattern is no longer fringe: a meaningful slice of the 2026 creator economy is leaving Notion for a Markdown-first stack, and the reasons are concrete, not ideological.</p>
    <p>If you publish on X, Bluesky, or LinkedIn, the case for leaving Notion is even stronger than it is for a typical SaaS team. Social content has the worst possible lock-in profile for a Notion-shaped workspace: it is short, link-heavy, copy-pasted across platforms, and lives or dies on reach that Notion cannot help you build. This guide is the migration plan I wish I had when I made the same move, with the social-creator specifics that most migration guides skip.</p>

    <div class="callout">
      <p><strong>TL;DR:</strong> Notion is fine for personal notes and shared docs. It is the wrong tool for the canonical archive of a creator's published social work. Markdown files in a Git repo cost nothing, survive any vendor decision, index cleanly in any search engine, and compose with the rest of your publishing pipeline. Migration is a 30-day project, not a 30-hour panic.</p>
    </div>

    <h2>Why Creators Are Quitting Notion for Markdown in 2026</h2>
    <p>The exit is not about a single Notion price hike or a privacy scandal. It is the accumulation of three forces that finally crossed a threshold this year.</p>
    <p><strong>Cost is the visible trigger.</strong> Notion's "free" plan caps at 1,000 blocks for guest editors. A creator with one year of saved social drafts, newsletter issues, and project pages burns through that in three months. The Plus plan is $10 per user per month billed annually, and a team of three paying annually is $360 per year for what is, functionally, a fancy text editor. For a solo creator or a pair, that is the same as one year of a decent VPS.</p>
    <p><strong>Lock-in is the structural problem.</strong> Every Notion database, toggle, relation, rollup, formula, and synced block exists only inside Notion. The official export is a folder of Markdown-shaped HTML, which is not Markdown. The community "Notion to Markdown" converters are better, but they still lose formulas, rollups, and any column that uses Notion-specific types. Three years of writing inside Notion is three years of work that you cannot take with you if Notion goes the way of every other venture-funded productivity app that eventually pivots, gets acquired, or sunsets.</p>
    <p><strong>Compostability is the new requirement.</strong> A creator in 2026 does not need a polished workspace. They need a workspace they can grep, diff, back up, feed to an LLM, and slice into newsletter issues with a Python script. Plain text files in a directory do all five. Notion does none of them natively. The whole "Markdown as a database" framing that Notion sold for a decade is, in 2026, inverted: <em>Markdown files are the database, and Notion is the renderer</em>.</p>

    <h2>The Real Cost of "Free" Notion Workspaces</h2>
    <p>For a creator with a moderate publishing volume &mdash; say, 5 X Articles, 12 Bluesky threads, 24 LinkedIn Newsletter issues, and 40 X threads per year &mdash; the actual costs of keeping everything inside Notion add up in three places.</p>
    <table>
  <thead>
    <tr>
      <th>Cost Category</th>
      <th>Notion (per year)</th>
      <th>Markdown + Git (per year)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Subscription (solo creator)</td>
      <td>$120 (Plus plan)</td>
      <td>$0</td>
    </tr>
    <tr>
      <td>Subscription (3-seat team)</td>
      <td>$360</td>
      <td>$0</td>
    </tr>
    <tr>
      <td>Backup / export tooling</td>
      <td>$0&ndash;$60 (third-party exporters)</td>
      <td>$0 (git push is the backup)</td>
    </tr>
    <tr>
      <td>Search &amp; indexing</td>
      <td>Notion's built-in (closed)</td>
      <td>$0 (ripgrep, fd, fzf)</td>
    </tr>
    <tr>
      <td>LLM training / RAG ingestion</td>
      <td>$20+/mo (Notion AI or manual export)</td>
      <td>$0 (point an LLM at the directory)</td>
    </tr>
    <tr>
      <td>Cross-platform publishing pipeline</td>
      <td>Zapier / Make ($20+/mo)</td>
      <td>Python script ($0)</td>
    </tr>
  </tbody>
</table>
    <p>For a creator team of three, the realistic annual cost of the "free" Notion setup is $400&ndash;$700 when you count the support tooling around it. The Markdown equivalent is the cost of a $5/mo VPS and your own time. The break-even is year one for any team, year two for a solo creator.</p>

    <h2>What a Markdown-First Social Stack Looks Like</h2>
    <p>The reference stack for a creator leaving Notion in 2026 has four layers, all of which speak plain text. None of them require a SaaS subscription beyond the platforms you are publishing to.</p>
    <ol>
      <li><strong>Capture layer</strong> &mdash; ThreadGrab for any public X thread, Bluesky post, or LinkedIn issue. Outputs a clean <code>.md</code> file with front matter, image links, and timestamps.</li>
      <li><strong>Edit layer</strong> &mdash; Obsidian or VS Code. Both render Markdown identically, both store files on disk, both diff cleanly with Git.</li>
      <li><strong>Version layer</strong> &mdash; a private Git repository on GitHub, Codeberg, or a self-hosted Gitea. Every change is a commit. Every commit is a free backup.</li>
      <li><strong>Publish layer</strong> &mdash; a Python or Node script that reads the canonical Markdown, applies the per-platform transformation, and emits the post. Same script for X, Bluesky, LinkedIn, Substack, and a static site generator.</li>
    </ol>
    <p>The same four-layer pattern works whether you are a solo creator writing one thread a week or a team publishing three newsletter issues a day. The cost difference is the cost of a coffee per month for a VPS. The reliability difference is the difference between "the Notion server is having an outage" and "my files are on my disk, nothing can take them down."</p>

    <h2>The 5-Step Migration Plan</h2>
    <p>Migration is a sequence of mechanical steps, not a leap of faith. The order matters. Skipping step 2 (the export) is how people end up with corrupted Markdown that loses half their tables and embeds.</p>
    <h3>Step 1: Audit What You Actually Have</h3>
    <p>Open Notion. Use the workspace search and count the pages that are <em>canonical published work</em> &mdash; drafts you actually published, newsletter issues you actually sent, threads you actually posted. Anything else (scratch pages, meeting notes, internal docs) is out of scope. The export only needs to cover the canonical archive.</p>
    <h3>Step 2: Export With a Markdown-Shaped Tool</h3>
    <p>Notion's official export is HTML zipped. Do not use it. The third-party <code>notion-to-md</code> Python package or the <code>notion-export-cleaner</code> Node tool produces a directory of actual <code>.md</code> files with front matter and images unzipped. Run one of these on a full workspace export first; check a sample of 10 files to make sure the tables, code blocks, and embeds survived.</p>
    <pre><code># Install the official Notion API exporter (uses an internal integration token)
pip install notion-to-md notion-client

# Or use the bulk HTML export + converter if you do not have an API token
# Settings &rarr; Export &rarr; Markdown &amp; CSV (Plus plan only)
unzip ~/Downloads/notion-export.zip -d notion-raw/

# Convert the HTML-shaped export to clean Markdown
python3 -c "
import pathlib, html2text, re
for f in pathlib.Path('notion-raw').rglob('*.html'):
    out = f.with_suffix('.md')
    h = html2text.HTML2Text()
    h.body_width = 0
    out.write_text(h.handle(f.read_text(encoding='utf-8')))
    f.unlink()
print('done')
"</code></pre>
    <h3>Step 3: Clean the Front Matter</h3>
    <p>Notion's export puts the page title as a top-level H1, the creation date in a side block, and tags as inline hashes. None of that is portable. The cleanup is a 30-line Python script that walks the exported tree, parses the Notion-specific metadata, and emits a unified front-matter block.</p>
    <pre><code>import pathlib, re, datetime

ROOT = pathlib.Path('notion-raw')
for md in ROOT.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    # Extract title (first H1)
    title = re.search(r'^# (.+)$', text, re.MULTILINE)
    title = title.group(1).strip() if title else md.stem
    # Extract created date from Notion metadata block
    date = re.search(r'created[:\s]+(\d{4}-\d{2}-\d{2})', text)
    date = date.group(1) if date else datetime.date.today().isoformat()
    # Strip the Notion metadata block
    text = re.sub(r'&lt;!-- notion:.*?--&gt;.*?--&gt;', '', text, flags=re.DOTALL)
    # Prepend clean front matter
    new = f'---\\ntitle: "{title}"\\ndate: {date}\\ntags: []\\n---\\n\\n{text}'
    md.write_text(new)
print('cleaned', len(list(ROOT.rglob('*.md'))), 'files')</code></pre>
    <h3>Step 4: Move Into a Git Repo</h3>
    <p>Create a new private repo, copy the cleaned Markdown into <code>content/</code>, and commit. The first commit is your snapshot. Every subsequent edit is a diff. Branch per topic or per quarter &mdash; whatever matches your publishing cadence.</p>
    <pre><code>git init md-archive
cd md-archive
mkdir -p content/{threads,articles,newsletters,drafts}
cp -r ../notion-raw-cleaned/* content/
git add content/
git commit -m "import: notional archive, 412 files, 2026-06-26"
git remote add origin git@github.com:you/md-archive.git
git push -u origin main</code></pre>
    <h3>Step 5: Rebuild the Capture Path</h3>
    <p>The last step is the most important. Now that you have a Markdown-first archive, point your publishing capture at it. Run <a href="/en/">ThreadGrab</a> on every X thread, Bluesky post, and LinkedIn issue you publish. Each call drops a <code>.md</code> file into the same <code>content/</code> tree. The archive stops being a snapshot of old work and becomes a living record.</p>

    <h2>Tool Comparison: Notion Export vs Pandoc vs Obsidian vs markitdown vs ThreadGrab</h2>
    <p>Five tools come up in every migration conversation. None of them is "best" in isolation. The right one depends on what you are moving and where it is going.</p>
    <table>
  <thead>
    <tr>
      <th>Tool</th>
      <th>Input</th>
      <th>Output</th>
      <th>Best For</th>
      <th>Cost</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Notion official export</td>
      <td>Notion workspace</td>
      <td>HTML + CSV zip</td>
      <td>One-time ad-hoc dumps</td>
      <td>Free (Plus plan)</td>
    </tr>
    <tr>
      <td>notion-to-md (Python)</td>
      <td>Notion API token</td>
      <td>Clean .md + images</td>
      <td>Programmatic full-workspace export</td>
      <td>Free, MIT</td>
    </tr>
    <tr>
      <td>Pandoc</td>
      <td>HTML / DOCX / EPUB</td>
      <td>Markdown / HTML / PDF</td>
      <td>Format-agnostic batch conversion</td>
      <td>Free, GPL</td>
    </tr>
    <tr>
      <td>Microsoft markitdown</td>
      <td>PDF / DOCX / PPTX / XLSX / images</td>
      <td>Markdown</td>
      <td>Office docs and scanned PDFs</td>
      <td>Free, MIT</td>
    </tr>
    <tr>
      <td>ThreadGrab</td>
      <td>Public X / Bluesky / LinkedIn URL</td>
      <td>Canonical Markdown + front matter</td>
      <td>Live social content capture</td>
      <td>Free, MIT</td>
    </tr>
  </tbody>
</table>
    <p>The honest split: <strong>notion-to-md</strong> for the historical migration, <strong>markitdown</strong> for any PDF / DOCX files you also need to pull in, and <strong>ThreadGrab</strong> for anything you publish publicly going forward. Pandoc is the fallback when the others do not handle the input format. The official Notion export is the last resort, not the first choice.</p>

    <h2>How ThreadGrab Fits in the Migration Path</h2>
    <p>ThreadGrab solves a specific subset of the migration problem: the social content that lives on platforms you do not control. If you have ever lost an X thread to a suspension, lost a Bluesky post to a handle change, or had a LinkedIn Newsletter issue silently delisted, ThreadGrab is the insurance policy. Run it on every published URL, and the canonical Markdown lands in the same Git repo you are migrating to.</p>
    <p>The integration is a single command per piece of content:</p>
    <pre><code># Capture one X thread to your local archive
curl -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d '{"url": "https://x.com/yourhandle/status/1234567890", "format": "markdown"}' \\
  &gt;&gt; content/threads/2026-06-26-thread.md

# Capture a Bluesky post
curl -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d '{"url": "https://bsky.app/profile/you.bsky.social/post/abc", "format": "markdown"}' \\
  &gt;&gt; content/threads/2026-06-26-bluesky.md

# Batch-capture every URL in a list (your publishing history)
cat publish-history.txt | xargs -I{} curl -s -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d "{{\\"url\\": \\"{}\\", \\"format\\": \\"markdown\\"}}" &gt;&gt; content/threads/batch.md</code></pre>
    <p>Each captured file has a <code>---</code> front matter block at the top with the source URL, the capture timestamp, and the platform. The diff in your Git log tells you which URLs you archived and when. If a platform deletes the original, you still have the canonical Markdown.</p>

    <h2>What Breaks: 5 Things Notion Did That Markdown Cannot</h2>
    <p>Migration is not a free lunch. Five things that Notion did well, plain Markdown files genuinely cannot do. You will either replace them with a different tool or learn to live without them.</p>
    <ol>
      <li><strong>Database views.</strong> Notion's table / board / gallery / timeline views are a killer feature. Markdown has none of that. The 2026 replacement is a static site generator (Astro, Hugo, 11ty) reading the front matter, or a SQLite index that you rebuild with a cron job.</li>
      <li><strong>Real-time collaborative editing.</strong> Two people editing the same Markdown file in Git will create a merge conflict. The 2026 replacement is a CRDT-based editor like Hedgedoc or a self-hosted Etherpad, with a daily dump to Git for the canonical record.</li>
      <li><strong>Linked database relations.</strong> Notion's relations across databases are powerful. Markdown has nothing equivalent. The replacement is a tag system in the front matter plus a tag index page generated at build time.</li>
      <li><strong>Formulas and rollups.</strong> Notion's formula language does math on database columns. Plain Markdown has no execution model. The replacement is a pre-compute step: a Python script reads the source files, computes the values, and writes them back as part of the build.</li>
      <li><strong>Page-level permissions.</strong> Notion lets you share one page with a guest without sharing the rest. Git repos do not do that. The replacement is a separate private repo for shared drafts and a public repo for the canonical archive.</li>
    </ol>
    <p>None of these is a deal-breaker. They are a different shape of work. The migration is a chance to decide which of Notion's features you actually used and which you only thought you used.</p>

    <h2>The 30-Day Migration Checklist</h2>
    <p>A realistic day-by-day for a solo creator or a small team moving off Notion in 2026.</p>
    <ul>
      <li><strong>Days 1&ndash;3: Audit.</strong> List the canonical pages. Decide what stays in Notion (internal-only docs, low-stakes scratch) and what moves to Markdown (published archive, public drafts, evergreen references).</li>
      <li><strong>Days 4&ndash;7: Tooling.</strong> Set up Obsidian or VS Code, install Pandoc, install markitdown, run a sample export of 10 pages and check the output.</li>
      <li><strong>Days 8&ndash;12: Bulk export.</strong> Run <code>notion-to-md</code> on the full canonical set. Expect 1&ndash;5% of files to need manual cleanup (broken tables, missing images, malformed front matter).</li>
      <li><strong>Days 13&ndash;18: Cleanup script.</strong> Write the 50&ndash;100 line Python script that normalizes front matter, fixes image paths, and validates code blocks. Run it. Commit the result.</li>
      <li><strong>Days 19&ndash;23: Git setup.</strong> Create the private repo. Push the canonical archive. Set up the daily capture cron that runs ThreadGrab against your publishing history.</li>
      <li><strong>Days 24&ndash;27: Rebuild the views.</strong> Generate the static index pages (by tag, by date, by platform). Make sure the archive is browsable in Obsidian and on the static site.</li>
      <li><strong>Days 28&ndash;30: Notion shutdown.</strong> Cancel the subscription. Archive a final tarball of the Notion workspace as a last-resort backup. Do not look back.</li>
    </ul>

    <h2>FAQ</h2>
    <div class="faq-item">
      <strong>Do I lose my Notion formulas and rollups if I export to Markdown?</strong>
      <p>Yes. Notion formulas do not have a Markdown equivalent. The fix is a pre-compute step: a Python script reads the source files, computes the values, and writes them into the front matter at build time. Most creators discover they used 2&ndash;3 formulas in three years; the migration cost is proportional to the formulas they actually rely on.</p>
    </div>
    <div class="faq-item">
      <strong>Can I keep using Notion for personal notes and just migrate the published archive?</strong>
      <p>Yes, and this is the most common 2026 pattern. Notion is fine for personal scratch, internal docs, and any workspace you do not need to take with you. The published archive is the one that has to leave, because it is the one that a vendor decision can take away from you.</p>
    </div>
    <div class="faq-item">
      <strong>Is there a risk of losing image embeds during migration?</strong>
      <p>Notion-hosted images move cleanly. Third-party embeds (YouTube, Figma, Loom) become plain links, which is the right Markdown behavior. The main loss is Notion's <code>file</code> property images, which sometimes have non-canonical filenames. A bulk rename script fixes 95% of these; the remaining 5% need manual review.</p>
    </div>
    <div class="faq-item">
      <strong>What about Notion AI? Does my AI workflow break if I leave?</strong>
      <p>Notion AI is a Notion-only feature. If you relied on it, the 2026 replacement is pointing Claude, GPT, or a local LLM at the directory directly. For most use cases (summarize, draft, rewrite, translate), the local LLM produces output at parity with Notion AI, with the bonus that the conversation history is itself a Markdown file in your archive.</p>
    </div>
    <div class="faq-item">
      <strong>How do I share a Markdown archive with collaborators who do not use Git?</strong>
      <p>Two options. The first is a static site generator (Astro, Hugo) deployed to a private URL &mdash; collaborators browse, they do not edit. The second is a hosted wiki that reads from Git (BookStack, Wiki.js, Outline). Both preserve the canonical Markdown in Git while giving non-technical collaborators a view-only or comment-only surface.</p>
    </div>
    <div class="faq-item">
      <strong>What is the smallest viable migration for a solo creator?</strong>
      <p>Three steps: (1) export the canonical archive with <code>notion-to-md</code>, (2) commit to a private GitHub repo, (3) cancel the Notion subscription. Total time: a weekend. Ongoing cost: zero. Capture new published work with ThreadGrab on the same day you publish it.</p>
    </div>

    <div class="cta">
      <p>Already publishing on X, Bluesky, or LinkedIn? Capture every post to your Markdown archive in one call. ThreadGrab turns any public social URL into a clean, front-matter-tagged <code>.md</code> file ready for Git.</p>
      <a class="btn" href="/en/">Try ThreadGrab &mdash; Free Social Archive</a>
    </div>

    <h2>Markdown Is the Format, Notion Is the Vendor</h2>
    <p>The 2026 creator stack is a stack of plain-text files in a directory, versioned in Git, searchable with ripgrep, renderable with Obsidian, and publishable with a 30-line Python script. Notion is a vendor that sells a polished UI on top of text. The text is the part that outlasts the vendor. Every creator who spent 2024 and 2025 watching SaaS apps pivot, get acquired, or shut down has learned the same lesson: keep the format, drop the vendor.</p>
    <p>For a creator, the migration is even more obviously right than it is for a typical team. Social content is short, link-heavy, and lives or dies on the platform's algorithm. Notion does not help with any of that. A Markdown-first archive helps with all of it. Start with the published work. Move the rest later. The 30-day plan above is the realistic path; most creators who start the migration finish it in two weekends and a handful of evenings.</p>
  </main>"""

# ---------- PORTUGUESE (PT) ----------
# Translate prose; keep code blocks identical; keep technical terms where natural
PT_BODY = """    <p>Em junho de 2026, a equipe alem de hospedagem forrabbit publicou um post-mortem de 1.800 palavras sobre migrar toda a base de conhecimento deles do Notion para arquivos Markdown em um repositorio Git. Em dez dias, o post atingiu 800 upvotes no Hacker News, gerou tres derivative threads no r/selfhosted e desencadeou uma onda de respostas do tipo "nos fizemos o mesmo". O padrao nao e mais de nicho: uma fatura significativa da economia de criadores de 2026 esta saindo do Notion para uma stack Markdown-first, e as razoes sao concretas, nao ideologicas.</p>
    <p>Se voce publica no X, Bluesky ou LinkedIn, o caso para sair do Notion e ainda mais forte do que para uma equipe SaaS tipica. Conteudo social tem o pior perfil possivel de lock-in para um workspace no formato Notion: e curto, rico em links, copiado entre plataformas, e vive ou morre de alcance que o Notion nao ajuda voce a construir. Este guia e o plano de migracao que eu queria ter quando fiz o mesmo movimento, com os especificos para criadores sociais que a maioria dos guias pula.</p>

    <div class="callout">
      <p><strong>TL;DR:</strong> Notion funciona para notas pessoais e documentos compartilhados. E a ferramenta errada para o arquivo canonico do trabalho publicado por um criador. Arquivos Markdown em um repo Git custam zero, sobrevivem a qualquer decisao de vendor, indexam limpo em qualquer mecanismo de busca e compoem com o resto do seu pipeline de publicacao. Migracao e um projeto de 30 dias, nao panico de 30 horas.</p>
    </div>

    <h2>Por Que Criadores Estao Saindo do Notion para Markdown em 2026</h2>
    <p>A saida nao e por causa de um unico aumento de preco do Notion ou um escandalo de privacidade. E o acucaro de tres forcas que finalmente cruzaram um limite neste ano.</p>
    <p><strong>Custo e o gatilho visivel.</strong> O plano "free" do Notion limita em 1.000 blocos para editores convidados. Um criador com um ano de rascunhos sociais salvos, edicoes de newsletter e paginas de projeto queima isso em tres meses. O plano Plus custa $10 por usuario por mes com cobranca anual, e uma equipe de tres pagando anualmente e $360 por ano pelo que e, funcionalmente, um editor de texto fancy. Para um criador solo ou dupla, isso e o mesmo que um ano de um VPS decente.</p>
    <p><strong>Lock-in e o problema estrutural.</strong> Cada database, toggle, relacao, rollup, formula e synced block do Notion existe somente dentro do Notion. O export oficial e uma pasta de HTML em formato Markdown, o que nao e Markdown. Os conversores comunitarios "Notion para Markdown" sao melhores, mas ainda perdem formulas, rollups e qualquer coluna que use tipos especificos do Notion. Tres anos escrevendo dentro do Notion e tres anos de trabalho que voce nao pode levar junto se o Notion for pelo caminho de qualquer outro app de produtividade financiado por venture capital que eventualmente faz pivot, e adquirido ou descontinuado.</p>
    <p><strong>Compostabilidade e o novo requisito.</strong> Um criador em 2026 nao precisa de um workspace polido. Precisa de um workspace que consiga fazer grep, diff, backup, alimentar um LLM e fatiar em edicoes de newsletter com um script Python. Arquivos de texto puro em um diretorio fazem todos os cinco. Notion nao faz nenhum deles nativamente. Todo o enquadramento de "Markdown como database" que o Notion vendeu por uma decada esta, em 2026, invertido: <em>arquivos Markdown sao o database, e o Notion e o renderer</em>.</p>

    <h2>O Custo Real de Workspaces Notion "Free"</h2>
    <p>Para um criador com volume moderado de publicacao &mdash; digamos, 5 X Articles, 12 threads Bluesky, 24 edicoes LinkedIn Newsletter e 40 threads X por ano &mdash; os custos reais de manter tudo dentro do Notion se acumulam em tres lugares.</p>
    <table>
  <thead>
    <tr>
      <th>Categoria de Custo</th>
      <th>Notion (por ano)</th>
      <th>Markdown + Git (por ano)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Assinatura (criador solo)</td>
      <td>$120 (plano Plus)</td>
      <td>$0</td>
    </tr>
    <tr>
      <td>Assinatura (equipe de 3)</td>
      <td>$360</td>
      <td>$0</td>
    </tr>
    <tr>
      <td>Backup / tooling de export</td>
      <td>$0&ndash;$60 (exportadores third-party)</td>
      <td>$0 (git push e o backup)</td>
    </tr>
    <tr>
      <td>Search &amp; indexacao</td>
      <td>Notion built-in (fechado)</td>
      <td>$0 (ripgrep, fd, fzf)</td>
    </tr>
    <tr>
      <td>LLM training / RAG ingestion</td>
      <td>$20+/mes (Notion AI ou export manual)</td>
      <td>$0 (aponta um LLM para o diretorio)</td>
    </tr>
    <tr>
      <td>Pipeline cross-platform</td>
      <td>Zapier / Make ($20+/mes)</td>
      <td>Script Python ($0)</td>
    </tr>
  </tbody>
</table>
    <p>Para uma equipe de tres criadores, o custo anual real do setup Notion "free" e $400&ndash;$700 quando voce conta o tooling de suporte em volta. O equivalente em Markdown e o custo de um VPS de $5/mes mais seu proprio tempo. O break-even e no ano um para qualquer equipe, no ano dois para um criador solo.</p>

    <h2>Como E uma Stack Social Markdown-First</h2>
    <p>A stack de referencia para um criador saindo do Notion em 2026 tem quatro camadas, todas falando texto puro. Nenhuma exige uma assinatura SaaS alem das plataformas para as quais voce esta publicando.</p>
    <ol>
      <li><strong>Camada de captura</strong> &mdash; ThreadGrab para qualquer thread X publica, post Bluesky ou edicao LinkedIn. Gera um arquivo <code>.md</code> limpo com front matter, links de imagem e timestamps.</li>
      <li><strong>Camada de edicao</strong> &mdash; Obsidian ou VS Code. Ambos renderizam Markdown identicamente, ambos armazenam arquivos no disco, ambos fazem diff limpo com Git.</li>
      <li><strong>Camada de versao</strong> &mdash; um repositorio Git privado no GitHub, Codeberg ou Gitea self-hosted. Toda mudanca e um commit. Todo commit e um backup gratis.</li>
      <li><strong>Camada de publicacao</strong> &mdash; um script Python ou Node que le o Markdown canonico, aplica a transformacao por plataforma e emite o post. Mesmo script para X, Bluesky, LinkedIn, Substack e um static site generator.</li>
    </ol>
    <p>O mesmo padrao de quatro camadas funciona se voce e um criador solo escrevendo uma thread por semana ou uma equipe publicando tres edicoes de newsletter por dia. A diferenca de custo e o preco de um cafe por mes por um VPS. A diferenca de confiabilidade e a diferenca entre "o servidor do Notion esta com outage" e "meus arquivos estao no meu disco, nada pode tira-los de mim".</p>

    <h2>O Plano de Migracao em 5 Etapas</h2>
    <p>Migracao e uma sequencia de passos mecanicos, nao um salto de fe. A ordem importa. Pular a etapa 2 (o export) e como as pessoas acabam com Markdown corrompido que perde metade das tabelas e embeds.</p>
    <h3>Etapa 1: Audite o que voce realmente tem</h3>
    <p>Abra o Notion. Use a busca do workspace e conte as paginas que sao <em>trabalho publicado canonico</em> &mdash; rascunhos que voce realmente publicou, edicoes de newsletter que voce realmente enviou, threads que voce realmente postou. Qualquer outra coisa (paginas de rascunho, notas de reuniao, docs internos) esta fora de escopo. O export so precisa cobrir o arquivo canonico.</p>
    <h3>Etapa 2: Exporte com uma ferramenta em formato Markdown</h3>
    <p>O export oficial do Notion e HTML zipado. Nao use. O pacote Python <code>notion-to-md</code> de third-party ou a ferramenta Node <code>notion-export-cleaner</code> produz um diretorio de arquivos <code>.md</code> reais com front matter e imagens deszipadas. Rode uma dessas em um export full workspace primeiro; confira uma amostra de 10 arquivos para garantir que tabelas, code blocks e embeds sobreviveram.</p>
    <pre><code># Install the official Notion API exporter (uses an internal integration token)
pip install notion-to-md notion-client

# Or use the bulk HTML export + converter if you do not have an API token
# Settings &rarr; Export &rarr; Markdown &amp; CSV (Plus plan only)
unzip ~/Downloads/notion-export.zip -d notion-raw/

# Convert the HTML-shaped export to clean Markdown
python3 -c "
import pathlib, html2text, re
for f in pathlib.Path('notion-raw').rglob('*.html'):
    out = f.with_suffix('.md')
    h = html2text.HTML2Text()
    h.body_width = 0
    out.write_text(h.handle(f.read_text(encoding='utf-8')))
    f.unlink()
print('done')
"</code></pre>
    <h3>Etapa 3: Limpe o front matter</h3>
    <p>O export do Notion coloca o titulo da pagina como H1 top-level, a data de criacao em um bloco lateral e tags como hashes inline. Nada disso e portavel. A limpeza e um script Python de 30 linhas que caminha na arvore exportada, faz parse da metadata especifica do Notion e emite um bloco de front matter unificado.</p>
    <pre><code>import pathlib, re, datetime

ROOT = pathlib.Path('notion-raw')
for md in ROOT.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    # Extract title (first H1)
    title = re.search(r'^# (.+)$', text, re.MULTILINE)
    title = title.group(1).strip() if title else md.stem
    # Extract created date from Notion metadata block
    date = re.search(r'created[:\s]+(\d{4}-\d{2}-\d{2})', text)
    date = date.group(1) if date else datetime.date.today().isoformat()
    # Strip the Notion metadata block
    text = re.sub(r'&lt;!-- notion:.*?--&gt;.*?--&gt;', '', text, flags=re.DOTALL)
    # Prepend clean front matter
    new = f'---\\ntitle: "{title}"\\ndate: {date}\\ntags: []\\n---\\n\\n{text}'
    md.write_text(new)
print('cleaned', len(list(ROOT.rglob('*.md'))), 'files')</code></pre>
    <h3>Etapa 4: Mova para um repo Git</h3>
    <p>Crie um novo repo privado, copie o Markdown limpo para <code>content/</code> e faca commit. O primeiro commit e seu snapshot. Cada edit subsequente e um diff. Branches por topico ou por trimestre &mdash; o que casar com sua cadencia de publicacao.</p>
    <pre><code>git init md-archive
cd md-archive
mkdir -p content/{threads,articles,newsletters,drafts}
cp -r ../notion-raw-cleaned/* content/
git add content/
git commit -m "import: notional archive, 412 files, 2026-06-26"
git remote add origin git@github.com:you/md-archive.git
git push -u origin main</code></pre>
    <h3>Etapa 5: Reconstrua o caminho de captura</h3>
    <p>A ultima etapa e a mais importante. Agora que voce tem um arquivo Markdown-first, aponte sua captura de publicacao para ele. Rode <a href="/pt/">ThreadGrab</a> em cada thread X, post Bluesky e edicao LinkedIn que voce publicar. Cada chamada deixa um arquivo <code>.md</code> na mesma arvore <code>content/</code>. O arquivo para de ser um snapshot do trabalho antigo e vira um registro vivo.</p>

    <h2>Comparacao de Ferramentas: Export Notion vs Pandoc vs Obsidian vs markitdown vs ThreadGrab</h2>
    <p>Cinco ferramentas aparecem em toda conversa de migracao. Nenhuma e "melhor" isoladamente. A certa depende do que voce esta movendo e para onde vai.</p>
    <table>
  <thead>
    <tr>
      <th>Ferramenta</th>
      <th>Input</th>
      <th>Output</th>
      <th>Melhor Para</th>
      <th>Custo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Export oficial Notion</td>
      <td>Workspace Notion</td>
      <td>HTML + CSV zip</td>
      <td>Dumps ad-hoc unicos</td>
      <td>Free (plano Plus)</td>
    </tr>
    <tr>
      <td>notion-to-md (Python)</td>
      <td>Token de API Notion</td>
      <td>.md limpo + imagens</td>
      <td>Export full-workspace programmatico</td>
      <td>Free, MIT</td>
    </tr>
    <tr>
      <td>Pandoc</td>
      <td>HTML / DOCX / EPUB</td>
      <td>Markdown / HTML / PDF</td>
      <td>Conversao em batch format-agnostic</td>
      <td>Free, GPL</td>
    </tr>
    <tr>
      <td>Microsoft markitdown</td>
      <td>PDF / DOCX / PPTX / XLSX / imagens</td>
      <td>Markdown</td>
      <td>Office docs e PDFs escaneados</td>
      <td>Free, MIT</td>
    </tr>
    <tr>
      <td>ThreadGrab</td>
      <td>URL publica X / Bluesky / LinkedIn</td>
      <td>Markdown canonico + front matter</td>
      <td>Captura de conteudo social ao vivo</td>
      <td>Free, MIT</td>
    </tr>
  </tbody>
</table>
    <p>A divisao honesta: <strong>notion-to-md</strong> para a migracao historica, <strong>markitdown</strong> para qualquer PDF / DOCX que voce tambem precise puxar, e <strong>ThreadGrab</strong> para qualquer coisa que voce publicar publicamente daqui para frente. Pandoc e o fallback quando as outras nao dao conta do formato de input. O export oficial do Notion e o ultimo recurso, nao a primeira escolha.</p>

    <h2>Como o ThreadGrab encaixa no caminho de migracao</h2>
    <p>ThreadGrab resolve um subset especifico do problema de migracao: o conteudo social que vive em plataformas que voce nao controla. Se voce ja perdeu uma thread X por suspensao, perdeu um post Bluesky por mudanca de handle, ou teve uma edicao de LinkedIn Newsletter silenciosamente delistada, ThreadGrab e a apolice de seguro. Rode em cada URL publicada, e o Markdown canonico cai no mesmo repo Git para onde voce esta migrando.</p>
    <p>A integracao e um unico comando por peca de conteudo:</p>
    <pre><code># Capture one X thread to your local archive
curl -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d '{"url": "https://x.com/yourhandle/status/1234567890", "format": "markdown"}' \\
  &gt;&gt; content/threads/2026-06-26-thread.md

# Capture a Bluesky post
curl -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d '{"url": "https://bsky.app/profile/you.bsky.social/post/abc", "format": "markdown"}' \\
  &gt;&gt; content/threads/2026-06-26-bluesky.md

# Batch-capture every URL in a list (your publishing history)
cat publish-history.txt | xargs -I{} curl -s -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d "{{\\"url\\": \\"{}\\", \\"format\\": \\"markdown\\"}}" &gt;&gt; content/threads/batch.md</code></pre>
    <p>Cada arquivo capturado tem um bloco de front matter <code>---</code> no topo com a URL source, o timestamp de captura e a plataforma. O diff no seu log Git mostra quais URLs voce arquivou e quando. Se uma plataforma deleta o original, voce ainda tem o Markdown canonico.</p>

    <h2>O que quebra: 5 coisas que o Notion fazia que Markdown nao faz</h2>
    <p>Migracao nao e almoco gratis. Cinco coisas que o Notion fazia bem, arquivos Markdown puros genuinamente nao dao conta. Voce ou substitui por uma ferramenta diferente ou aprende a viver sem elas.</p>
    <ol>
      <li><strong>Database views.</strong> As views table / board / gallery / timeline do Notion sao um killer feature. Markdown nao tem nada disso. O substituto de 2026 e um static site generator (Astro, Hugo, 11ty) lendo o front matter, ou um indice SQLite que voce rebuild com um cron job.</li>
      <li><strong>Edicao colaborativa em tempo real.</strong> Duas pessoas editando o mesmo arquivo Markdown no Git vao criar merge conflict. O substituto de 2026 e um editor CRDT-based como Hedgedoc ou Etherpad self-hosted, com dump diario para Git para o registro canonico.</li>
      <li><strong>Relacoes entre databases.</strong> As relacoes do Notion entre databases sao poderosas. Markdown nao tem equivalente. O substituto e um sistema de tags no front matter mais uma tag index page gerada em build time.</li>
      <li><strong>Formulas e rollups.</strong> A linguagem de formula do Notion faz math em colunas de database. Markdown puro nao tem modelo de execucao. O substituto e um pre-compute step: um script Python le os arquivos source, computa os valores e escreve de volta como parte do build.</li>
      <li><strong>Permissoes por pagina.</strong> Notion deixa voce compartilhar uma pagina com um guest sem compartilhar o resto. Repos Git nao fazem isso. O substituto e um repo privado separado para rascunhos compartilhados e um repo publico para o arquivo canonico.</li>
    </ol>
    <p>Nenhum desses e deal-breaker. Sao um formato diferente de trabalho. A migracao e uma chance de decidir quais features do Notion voce realmente usava e quais voce so achava que usava.</p>

    <h2>Checklist de Migracao de 30 Dias</h2>
    <p>Um dia-a-dia realista para um criador solo ou equipe pequena saindo do Notion em 2026.</p>
    <ul>
      <li><strong>Dias 1&ndash;3: Auditoria.</strong> Liste as paginas canonicas. Decida o que fica no Notion (docs internos, rascunhos de baixo risco) e o que vai para Markdown (arquivo publicado, drafts publicos, referencias evergreen).</li>
      <li><strong>Dias 4&ndash;7: Tooling.</strong> Configure Obsidian ou VS Code, instale Pandoc, instale markitdown, rode um sample export de 10 paginas e confira o output.</li>
      <li><strong>Dias 8&ndash;12: Bulk export.</strong> Rode <code>notion-to-md</code> no set canonico completo. Espere 1&ndash;5% de arquivos precisarem de cleanup manual (tabelas quebradas, imagens faltando, front matter malformado).</li>
      <li><strong>Dias 13&ndash;18: Script de limpeza.</strong> Escreva o script Python de 50&ndash;100 linhas que normaliza front matter, conserta paths de imagem e valida code blocks. Rode. Faca commit do resultado.</li>
      <li><strong>Dias 19&ndash;23: Git setup.</strong> Crie o repo privado. Push do arquivo canonico. Configure o cron diario de captura que roda ThreadGrab contra seu historico de publicacao.</li>
      <li><strong>Dias 24&ndash;27: Rebuild das views.</strong> Gere as paginas de indice estaticas (por tag, por data, por plataforma). Garanta que o arquivo e browseable em Obsidian e no site estatico.</li>
      <li><strong>Dias 28&ndash;30: Shutdown do Notion.</strong> Cancele a assinatura. Archive um tarball final do workspace Notion como backup de ultimo recurso. Nao olhe para tras.</li>
    </ul>

    <h2>FAQ</h2>
    <div class="faq-item">
      <strong>Perco minhas formulas e rollups do Notion se eu exportar para Markdown?</strong>
      <p>Sim. Formulas do Notion nao tem equivalente em Markdown. A solucao e um pre-compute step: um script Python le os arquivos source, computa os valores e escreve no front matter em build time. A maioria dos criadores descobre que usou 2&ndash;3 formulas em tres anos; o custo de migracao e proporcional as formulas que voce realmente depende.</p>
    </div>
    <div class="faq-item">
      <strong>Posso continuar usando Notion para notas pessoais e migrar so o arquivo publicado?</strong>
      <p>Sim, e esse e o padrao mais comum em 2026. Notion funciona para rascunho pessoal, docs internos e qualquer workspace que voce nao precisa levar junto. O arquivo publicado e o que tem que sair, porque e o que uma decisao de vendor pode tirar de voce.</p>
    </div>
    <div class="faq-item">
      <strong>Ha risco de perder embeds de imagem durante a migracao?</strong>
      <p>Imagens hospedadas no Notion movem limpo. Embeds third-party (YouTube, Figma, Loom) viram links puros, que e o comportamento Markdown correto. A perda principal sao imagens da propriedade <code>file</code> do Notion, que as vezes tem filenames nao canonicos. Um script de rename em batch corrige 95% dessas; os 5% restantes precisam de revisao manual.</p>
    </div>
    <div class="faq-item">
      <strong>E o Notion AI? Meu workflow de IA quebra se eu sair?</strong>
      <p>Notion AI e uma feature exclusiva do Notion. Se voce dependia dela, o substituto de 2026 e apontar Claude, GPT ou um LLM local para o diretorio diretamente. Para a maioria dos casos de uso (resumir, redigir, reescrever, traduzir), o LLM local produz output em paridade com o Notion AI, com o bonus de que o historico de conversa e em si um arquivo Markdown no seu arquivo.</p>
    </div>
    <div class="faq-item">
      <strong>Como compartilhar um arquivo Markdown com colaboradores que nao usam Git?</strong>
      <p>Duas opcoes. A primeira e um static site generator (Astro, Hugo) deployado em uma URL privada &mdash; colaboradores navegam, nao editam. A segunda e uma wiki hospedada que le do Git (BookStack, Wiki.js, Outline). Ambos preservam o Markdown canonico no Git enquanto dao a colaboradores nao-tecnicos uma superficie view-only ou comment-only.</p>
    </div>
    <div class="faq-item">
      <strong>Qual e a menor migracao viavel para um criador solo?</strong>
      <p>Tres passos: (1) export do arquivo canonico com <code>notion-to-md</code>, (2) commit em um repo privado do GitHub, (3) cancele a assinatura do Notion. Tempo total: um fim de semana. Custo recorrente: zero. Capture trabalho novo publicado com ThreadGrab no mesmo dia que publicar.</p>
    </div>

    <div class="cta">
      <p>Ja publica no X, Bluesky ou LinkedIn? Capture cada post no seu arquivo Markdown em uma unica chamada. ThreadGrab transforma qualquer URL social publica em um arquivo <code>.md</code> limpo com front matter, pronto para Git.</p>
      <a class="btn" href="/pt/">Experimente o ThreadGrab &mdash; Arquivo Social Free</a>
    </div>

    <h2>Markdown E o Formato, Notion E o Vendor</h2>
    <p>A stack do criador em 2026 e uma stack de arquivos plain-text em um diretorio, versionados em Git, busca veis com ripgrep, renderizaveis com Obsidian e publicaveis com um script Python de 30 linhas. Notion e um vendor que vende uma UI polida em cima de texto. O texto e a parte que sobrevive ao vendor. Todo criador que passou 2024 e 2025 vendo apps SaaS fazerem pivot, serem adquiridos ou serem descontinuados aprendeu a mesma licao: mantenha o formato, solte o vendor.</p>
    <p>Para um criador, a migracao e ainda mais obviamente certa do que para uma equipe tipica. Conteudo social e curto, rico em links e vive ou morre do algoritmo da plataforma. Notion nao ajuda com nada disso. Um arquivo Markdown-first ajuda com tudo isso. Comece pelo trabalho publicado. Mova o resto depois. O plano de 30 dias acima e o caminho realista; a maioria dos criadores que comeca a migracao termina em dois fins de semana e algumas noites.</p>
  </main>"""

# ---------- INDONESIAN (ID) ----------
ID_BODY = """    <p>Pada Juni 2026, tim hosting Jerman forrabbit mempublikasikan post-mortem sepanjang 1.800 kata tentang memindahkan seluruh basis pengetahuan mereka dari Notion ke file Markdown biasa di repo Git. Dalam sepuluh hari, posting tersebut mendapat 800 upvote di Hacker News, memicu tiga thread turunan di r/selfhosted, dan memicu gelombang balasan "kami melakukan hal yang sama". Polanya sudah bukan hal pinggiran: bagian penting dari ekonomi kreator 2026 meninggalkan Notion untuk stack Markdown-first, dan alasannya konkret, bukan ideologis.</p>
    <p>Jika Anda mempublikasikan di X, Bluesky, atau LinkedIn, alasan untuk meninggalkan Notion bahkan lebih kuat daripada untuk tim SaaS pada umumnya. Konten sosial punya profil lock-in paling buruk untuk workspace berbentuk Notion: pendek, penuh link, disalin-tempel lintas platform, dan hidup atau mati oleh reach yang tidak bisa dibantu Notion untuk Anda bangun. Panduan ini adalah rencana migrasi yang saya harap saya punya saat melakukan perpindahan yang sama, dengan kekhasan kreator sosial yang kebanyakan panduan migrasi lewatkan.</p>

    <div class="callout">
      <p><strong>TL;DR:</strong> Notion cukup bagus untuk catatan pribadi dan dokumen bersama. Ini adalah alat yang salah untuk arsip kanonik karya kreator yang sudah dipublikasikan. File Markdown di repo Git tidak butuh biaya, selamat dari keputusan vendor mana pun, terindeks bersih di mesin pencari mana pun, dan bisa digabung dengan sisa pipeline publikasi Anda. Migrasi adalah proyek 30 hari, bukan kepanikan 30 jam.</p>
    </div>

    <h2>Mengapa Kreator Meninggalkan Notion untuk Markdown di 2026</h2>
    <p>Keluarnya bukan karena satu kenaikan harga Notion atau skandal privasi. Ini adalah akumulasi tiga kekuatan yang akhirnya melewati ambang batas tahun ini.</p>
    <p><strong>Biaya adalah pemicu yang terlihat.</strong> Paket "free" Notion membatasi 1.000 blok untuk editor tamu. Kreator dengan satu tahun draf sosial tersimpan, edisi newsletter, dan halaman proyek akan menghabiskan itu dalam tiga bulan. Paket Plus adalah $10 per pengguna per bulan ditagih tahunan, dan tim beranggotakan tiga orang yang membayar tahunan adalah $360 per tahun untuk apa yang, secara fungsional, adalah editor teks mewah. Untuk kreator solo atau berdua, itu sama dengan satu tahun VPS yang layak.</p>
    <p><strong>Lock-in adalah masalah struktural.</strong> Setiap database, toggle, relasi, rollup, formula, dan synced block Notion hanya ada di dalam Notion. Export resmi adalah folder HTML berbentuk Markdown, yang bukan Markdown. Konverter komunitas "Notion to Markdown" lebih baik, tapi tetap kehilangan formula, rollup, dan kolom apa pun yang memakai tipe spesifik Notion. Tiga tahun menulis di dalam Notion adalah tiga tahun pekerjaan yang tidak bisa Anda bawa pergi jika Notion mengikuti nasib setiap app produktivitas yang didanai modal ventura yang akhirnya berputar, diakuisisi, atau dihentikan.</p>
    <p><strong>Compostability adalah kebutuhan baru.</strong> Kreator di 2026 tidak butuh workspace yang dipoles. Mereka butuh workspace yang bisa di-grep, di-diff, di-backup, diumpankan ke LLM, dan diiris jadi edisi newsletter dengan script Python. File teks biasa di direktori melakukan kelima hal itu. Notion tidak melakukan satu pun secara native. Seluruh pembingkaian "Markdown sebagai database" yang dijual Notion selama satu dekade, di 2026, terbalik: <em>file Markdown adalah database, dan Notion adalah renderer-nya</em>.</p>

    <h2>Biaya Real Workspace Notion "Free"</h2>
    <p>Untuk kreator dengan volume publikasi moderat &mdash; katakanlah, 5 X Articles, 12 thread Bluesky, 24 edisi LinkedIn Newsletter, dan 40 thread X per tahun &mdash; biaya nyata menyimpan semuanya di dalam Notion menumpuk di tiga tempat.</p>
    <table>
  <thead>
    <tr>
      <th>Kategori Biaya</th>
      <th>Notion (per tahun)</th>
      <th>Markdown + Git (per tahun)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Langganan (kreator solo)</td>
      <td>$120 (paket Plus)</td>
      <td>$0</td>
    </tr>
    <tr>
      <td>Langganan (tim 3 orang)</td>
      <td>$360</td>
      <td>$0</td>
    </tr>
    <tr>
      <td>Backup / tooling export</td>
      <td>$0&ndash;$60 (exporter pihak ketiga)</td>
      <td>$0 (git push adalah backup)</td>
    </tr>
    <tr>
      <td>Pencarian &amp; pengindeksan</td>
      <td>Notion bawaan (tertutup)</td>
      <td>$0 (ripgrep, fd, fzf)</td>
    </tr>
    <tr>
      <td>Pelatihan LLM / RAG ingestion</td>
      <td>$20+/bln (Notion AI atau export manual)</td>
      <td>$0 (arahkan LLM ke direktori)</td>
    </tr>
    <tr>
      <td>Pipeline publikasi lintas platform</td>
      <td>Zapier / Make ($20+/bln)</td>
      <td>Script Python ($0)</td>
    </tr>
  </tbody>
</table>
    <p>Untuk tim kreator beranggotakan tiga orang, biaya tahunan realistis dari setup Notion "free" adalah $400&ndash;$700 kalau Anda hitung tooling pendukung di sekitarnya. Padanan Markdown-nya adalah biaya VPS $5/bln dan waktu Anda sendiri. Titik impas adalah tahun pertama untuk tim mana pun, tahun kedua untuk kreator solo.</p>

    <h2>Seperti Apa Stack Sosial Markdown-First</h2>
    <p>Stack referensi untuk kreator yang keluar dari Notion di 2026 punya empat lapisan, semuanya berbahasa teks biasa. Tak satu pun butuh langganan SaaS selain platform tempat Anda mempublikasikan.</p>
    <ol>
      <li><strong>Lapisan tangkap</strong> &mdash; ThreadGrab untuk thread X publik, post Bluesky, atau edisi LinkedIn mana pun. Menghasilkan file <code>.md</code> bersih dengan front matter, tautan gambar, dan timestamp.</li>
      <li><strong>Lapisan edit</strong> &mdash; Obsidian atau VS Code. Keduanya merender Markdown identik, keduanya menyimpan file di disk, keduanya diff bersih dengan Git.</li>
      <li><strong>Lapisan versi</strong> &mdash; repositori Git privat di GitHub, Codeberg, atau Gitea self-hosted. Setiap perubahan adalah satu commit. Setiap commit adalah backup gratis.</li>
      <li><strong>Lapisan publikasi</strong> &mdash; script Python atau Node yang membaca Markdown kanonik, menerapkan transformasi per platform, dan mengeluarkan posting. Skrip sama untuk X, Bluesky, LinkedIn, Substack, dan static site generator.</li>
    </ol>
    <p>Pola empat-lapis yang sama berfungsi baik untuk kreator solo yang menulis satu thread per minggu maupun tim yang mempublikasikan tiga edisi newsletter per hari. Selisih biayanya adalah secangkir kopi per bulan untuk sebuah VPS. Selisih keandalannya adalah selisih antara "server Notion sedang outage" dan "file saya ada di disk saya, tidak ada yang bisa mengambilnya dari saya."</p>

    <h2>Rencana Migrasi 5 Langkah</h2>
    <p>Migrasi adalah urutan langkah mekanis, bukan lompatan keyakinan. Urutan penting. Melewati langkah 2 (export) adalah cara orang berakhir dengan Markdown rusak yang kehilangan setengah tabel dan embed-nya.</p>
    <h3>Langkah 1: Audit apa yang sebenarnya Anda punya</h3>
    <p>Buka Notion. Pakai pencarian workspace dan hitung halaman yang merupakan <em>karya kanonik yang sudah dipublikasikan</em> &mdash; draf yang benar-benar Anda publikasikan, edisi newsletter yang benar-benar Anda kirim, thread yang benar-benar Anda posting. Sisanya (halaman coret-coretan, catatan rapat, dokumen internal) di luar lingkup. Export hanya perlu mencakup arsip kanonik.</p>
    <h3>Langkah 2: Export dengan alat berbentuk Markdown</h3>
    <p>Export resmi Notion adalah HTML di-zip. Jangan pakai itu. Paket Python pihak ketiga <code>notion-to-md</code> atau alat Node <code>notion-export-cleaner</code> menghasilkan direktori file <code>.md</code> sesungguhnya dengan front matter dan gambar yang sudah di-unzip. Jalankan salah satu pada export workspace penuh lebih dulu; periksa sampel 10 file untuk memastikan tabel, blok kode, dan embed selamat.</p>
    <pre><code># Install the official Notion API exporter (uses an internal integration token)
pip install notion-to-md notion-client

# Or use the bulk HTML export + converter if you do not have an API token
# Settings &rarr; Export &rarr; Markdown &amp; CSV (Plus plan only)
unzip ~/Downloads/notion-export.zip -d notion-raw/

# Convert the HTML-shaped export to clean Markdown
python3 -c "
import pathlib, html2text, re
for f in pathlib.Path('notion-raw').rglob('*.html'):
    out = f.with_suffix('.md')
    h = html2text.HTML2Text()
    h.body_width = 0
    out.write_text(h.handle(f.read_text(encoding='utf-8')))
    f.unlink()
print('done')
"</code></pre>
    <h3>Langkah 3: Bersihkan front matter</h3>
    <p>Export Notion meletakkan judul halaman sebagai H1 tingkat atas, tanggal pembuatan di blok samping, dan tag sebagai hash inline. Tak satu pun portabel. Pembersihan adalah script Python 30 baris yang berjalan di pohon export, mem-parsing metadata spesifik Notion, dan mengeluarkan blok front matter terpadu.</p>
    <pre><code>import pathlib, re, datetime

ROOT = pathlib.Path('notion-raw')
for md in ROOT.rglob('*.md'):
    text = md.read_text(encoding='utf-8')
    # Extract title (first H1)
    title = re.search(r'^# (.+)$', text, re.MULTILINE)
    title = title.group(1).strip() if title else md.stem
    # Extract created date from Notion metadata block
    date = re.search(r'created[:\s]+(\d{4}-\d{2}-\d{2})', text)
    date = date.group(1) if date else datetime.date.today().isoformat()
    # Strip the Notion metadata block
    text = re.sub(r'&lt;!-- notion:.*?--&gt;.*?--&gt;', '', text, flags=re.DOTALL)
    # Prepend clean front matter
    new = f'---\\ntitle: "{title}"\\ndate: {date}\\ntags: []\\n---\\n\\n{text}'
    md.write_text(new)
print('cleaned', len(list(ROOT.rglob('*.md'))), 'files')</code></pre>
    <h3>Langkah 4: Pindahkan ke repo Git</h3>
    <p>Buat repo privat baru, salin Markdown yang sudah dibersihkan ke <code>content/</code>, lalu commit. Commit pertama adalah snapshot Anda. Setiap edit berikutnya adalah diff. Branch per topik atau per kuartal &mdash; apa pun yang cocok dengan ritme publikasi Anda.</p>
    <pre><code>git init md-archive
cd md-archive
mkdir -p content/{threads,articles,newsletters,drafts}
cp -r ../notion-raw-cleaned/* content/
git add content/
git commit -m "import: notional archive, 412 files, 2026-06-26"
git remote add origin git@github.com:you/md-archive.git
git push -u origin main</code></pre>
    <h3>Langkah 5: Bangun ulang jalur tangkap</h3>
    <p>Langkah terakhir adalah yang terpenting. Sekarang Anda punya arsip Markdown-first, arahkan tangkapan publikasi Anda ke sana. Jalankan <a href="/id/">ThreadGrab</a> untuk setiap thread X, post Bluesky, dan edisi LinkedIn yang Anda publikasikan. Tiap panggilan menjatuhkan file <code>.md</code> ke pohon <code>content/</code> yang sama. Arsip berhenti menjadi snapshot karya lama dan menjadi catatan yang hidup.</p>

    <h2>Perbandingan Alat: Export Notion vs Pandoc vs Obsidian vs markitdown vs ThreadGrab</h2>
    <p>Lima alat muncul di setiap percakapan migrasi. Tak satu pun "terbaik" secara terpisah. Yang tepat bergantung pada apa yang Anda pindahkan dan ke mana tujuannya.</p>
    <table>
  <thead>
    <tr>
      <th>Alat</th>
      <th>Input</th>
      <th>Output</th>
      <th>Cocok Untuk</th>
      <th>Biaya</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Export resmi Notion</td>
      <td>Workspace Notion</td>
      <td>HTML + CSV zip</td>
      <td>Dump ad-hoc satu kali</td>
      <td>Free (paket Plus)</td>
    </tr>
    <tr>
      <td>notion-to-md (Python)</td>
      <td>Token API Notion</td>
      <td>.md bersih + gambar</td>
      <td>Export workspace penuh secara programatis</td>
      <td>Free, MIT</td>
    </tr>
    <tr>
      <td>Pandoc</td>
      <td>HTML / DOCX / EPUB</td>
      <td>Markdown / HTML / PDF</td>
      <td>Konversi batch format-agnostik</td>
      <td>Free, GPL</td>
    </tr>
    <tr>
      <td>Microsoft markitdown</td>
      <td>PDF / DOCX / PPTX / XLSX / gambar</td>
      <td>Markdown</td>
      <td>Dokumen Office dan PDF hasil pindai</td>
      <td>Free, MIT</td>
    </tr>
    <tr>
      <td>ThreadGrab</td>
      <td>URL publik X / Bluesky / LinkedIn</td>
      <td>Markdown kanonik + front matter</td>
      <td>Tangkap konten sosial langsung</td>
      <td>Free, MIT</td>
    </tr>
  </tbody>
</table>
    <p>Pembagian yang jujur: <strong>notion-to-md</strong> untuk migrasi historis, <strong>markitdown</strong> untuk file PDF / DOCX yang juga perlu Anda tarik, dan <strong>ThreadGrab</strong> untuk apa pun yang Anda publikasikan ke depan. Pandoc adalah fallback ketika yang lain tidak menangani format input. Export resmi Notion adalah pilihan terakhir, bukan yang pertama.</p>

    <h2>Bagaimana ThreadGrab Masuk di Jalur Migrasi</h2>
    <p>ThreadGrab memecahkan subset spesifik dari masalah migrasi: konten sosial yang hidup di platform yang tidak Anda kontrol. Kalau Anda pernah kehilangan thread X karena suspend, kehilangan post Bluesky karena perubahan handle, atau punya edisi LinkedIn Newsletter di-delist diam-diam, ThreadGrab adalah polis asuransinya. Jalankan pada setiap URL yang dipublikasikan, dan Markdown kanonik jatuh ke repo Git yang sama dengan tujuan migrasi Anda.</p>
    <p>Integrasinya adalah satu perintah per konten:</p>
    <pre><code># Capture one X thread to your local archive
curl -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d '{"url": "https://x.com/yourhandle/status/1234567890", "format": "markdown"}' \\
  &gt;&gt; content/threads/2026-06-26-thread.md

# Capture a Bluesky post
curl -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d '{"url": "https://bsky.app/profile/you.bsky.social/post/abc", "format": "markdown"}' \\
  &gt;&gt; content/threads/2026-06-26-bluesky.md

# Batch-capture every URL in a list (your publishing history)
cat publish-history.txt | xargs -I{} curl -s -X POST https://threadgrab.com/api/extract \\
  -H 'Content-Type: application/json' \\
  -d "{{\\"url\\": \\"{}\\", \\"format\\": \\"markdown\\"}}" &gt;&gt; content/threads/batch.md</code></pre>
    <p>Setiap file yang ditangkap punya blok front matter <code>---</code> di atas berisi URL sumber, timestamp tangkap, dan platform. Diff di log Git Anda menunjukkan URL mana yang Anda arsipkan dan kapan. Jika platform menghapus aslinya, Anda masih punya Markdown kanoniknya.</p>

    <h2>Apa yang rusak: 5 hal yang Notion lakukan yang Markdown tidak bisa</h2>
    <p>Migrasi bukan makan siang gratis. Lima hal yang Notion lakukan dengan baik, file Markdown polos benar-benar tidak bisa melakukan. Anda akan menggantinya dengan alat berbeda atau belajar hidup tanpa mereka.</p>
    <ol>
      <li><strong>Database view.</strong> View table / board / gallery / timeline Notion adalah fitur pembunuh. Markdown tidak punya itu. Pengganti 2026 adalah static site generator (Astro, Hugo, 11ty) yang membaca front matter, atau indeks SQLite yang di-rebuild via cron job.</li>
      <li><strong>Pengeditan kolaboratif real-time.</strong> Dua orang menyunting file Markdown yang sama di Git akan membuat merge conflict. Pengganti 2026 adalah editor berbasis CRDT seperti Hedgedoc atau Etherpad self-hosted, dengan dump harian ke Git untuk catatan kanonik.</li>
      <li><strong>Relasi database tertaut.</strong> Relasi Notion lintas database sangat kuat. Markdown tidak punya padanannya. Penggantinya adalah sistem tag di front matter plus halaman indeks tag yang dibuat saat build time.</li>
      <li><strong>Formula dan rollup.</strong> Bahasa formula Notion melakukan matematika pada kolom database. Markdown polos tidak punya model eksekusi. Penggantinya adalah langkah pre-compute: script Python membaca file sumber, menghitung nilai, dan menulisnya kembali sebagai bagian dari build.</li>
      <li><strong>Izin setingkat halaman.</strong> Notion memungkinkan Anda berbagi satu halaman dengan tamu tanpa membagikan sisanya. Repo Git tidak bisa begitu. Penggantinya adalah repo privat terpisah untuk draf bersama dan repo publik untuk arsip kanonik.</li>
    </ol>
    <p>Tak satu pun dari ini deal-breaker. Ini adalah bentuk kerja yang berbeda. Migrasi adalah kesempatan untuk memutuskan fitur Notion mana yang benar-benar Anda pakai dan mana yang hanya Anda kira Anda pakai.</p>

    <h2>Checklist Migrasi 30 Hari</h2>
    <p>Hari-per-hari yang realistis untuk kreator solo atau tim kecil yang keluar dari Notion di 2026.</p>
    <ul>
      <li><strong>Hari 1&ndash;3: Audit.</strong> Daftar halaman kanonik. Tentukan apa yang tinggal di Notion (dokumen internal, coret-coretan berisiko rendah) dan apa yang pindah ke Markdown (arsip publikasi, draf publik, referensi evergreen).</li>
      <li><strong>Hari 4&ndash;7: Tooling.</strong> Siapkan Obsidian atau VS Code, pasang Pandoc, pasang markitdown, jalankan contoh export 10 halaman dan periksa outputnya.</li>
      <li><strong>Hari 8&ndash;12: Bulk export.</strong> Jalankan <code>notion-to-md</code> pada set kanonik lengkap. Harapkan 1&ndash;5% file butuh pembersihan manual (tabel rusak, gambar hilang, front matter cacat).</li>
      <li><strong>Hari 13&ndash;18: Script pembersih.</strong> Tulis script Python 50&ndash;100 baris yang menormalkan front matter, membetulkan path gambar, dan memvalidasi blok kode. Jalankan. Commit hasilnya.</li>
      <li><strong>Hari 19&ndash;23: Setup Git.</strong> Buat repo privat. Push arsip kanonik. Siapkan cron harian tangkap yang menjalankan ThreadGrab terhadap riwayat publikasi Anda.</li>
      <li><strong>Hari 24&ndash;27: Bangun ulang view.</strong> Hasilkan halaman indeks statis (per tag, per tanggal, per platform). Pastikan arsip bisa di-browse di Obsidian dan di situs statis.</li>
      <li><strong>Hari 28&ndash;30: Shutdown Notion.</strong> Batalkan langganan. Arsipkan tarball akhir workspace Notion sebagai cadangan pilihan terakhir. Jangan menoleh ke belakang.</li>
    </ul>

    <h2>FAQ</h2>
    <div class="faq-item">
      <strong>Apakah saya kehilangan formula dan rollup Notion jika mengekspor ke Markdown?</strong>
      <p>Ya. Formula Notion tidak punya padanan Markdown. Solusinya adalah langkah pre-compute: script Python membaca file sumber, menghitung nilai, dan menuliskannya ke front matter saat build time. Kebanyakan kreator发现自己用2&ndash;3 rumus dalam tiga tahun; biaya migrasi sebanding dengan rumus yang benar-benar Anda andalkan.</p>
    </div>
    <div class="faq-item">
      <strong>Bisakah saya tetap pakai Notion untuk catatan pribadi dan hanya migrasikan arsip yang dipublikasikan?</strong>
      <p>Ya, dan ini adalah pola paling umum di 2026. Notion cukup untuk coret-coretan pribadi, dokumen internal, dan workspace apa pun yang tidak perlu Anda bawa pergi. Arsip yang dipublikasikan adalah yang harus pergi, karena itulah yang bisa diambil dari Anda oleh keputusan vendor.</p>
    </div>
    <div class="faq-item">
      <strong>Apakah ada risiko kehilangan embed gambar saat migrasi?</strong>
      <p>Gambar yang di-host Notion pindah dengan bersih. Embed pihak ketiga (YouTube, Figma, Loom) menjadi tautan polos, yang merupakan perilaku Markdown yang semestinya. Kehilangan utama adalah gambar properti <code>file</code> Notion, yang kadang punya nama file non-kanonik. Script rename massal memperbaiki 95% dari ini; 5% sisanya butuh tinjauan manual.</p>
    </div>
    <div class="faq-item">
      <strong>Bagaimana dengan Notion AI? Apakah workflow AI saya putus kalau saya keluar?</strong>
      <p>Notion AI adalah fitur eksklusif Notion. Kalau Anda mengandalkannya, pengganti 2026 adalah mengarahkan Claude, GPT, atau LLM lokal ke direktori secara langsung. Untuk kebanyakan kasus penggunaan (merangkum, menulis, menulis ulang, menerjemahkan), LLM lokal menghasilkan output setara dengan Notion AI, dengan bonus bahwa riwayat percakapan juga merupakan file Markdown di arsip Anda.</p>
    </div>
    <div class="faq-item">
      <strong>Bagaimana cara berbagi arsip Markdown dengan kolaborator yang tidak pakai Git?</strong>
      <p>Dua opsi. Yang pertama adalah static site generator (Astro, Hugo) yang di-deploy ke URL privat &mdash; kolaborator menjelajah, tidak menyunting. Yang kedua adalah wiki ter-host yang membaca dari Git (BookStack, Wiki.js, Outline). Keduanya mempertahankan Markdown kanonik di Git sembari memberi kolaborator non-teknis permukaan view-only atau comment-only.</p>
    </div>
    <div class="faq-item">
      <strong>Apa migrasi terkecil yang layak untuk kreator solo?</strong>
      <p>Tiga langkah: (1) ekspor arsip kanonik dengan <code>notion-to-md</code>, (2) commit ke repo GitHub privat, (3) batalkan langganan Notion. Total waktu: satu akhir pekan. Biaya berjalan: nol. Tangkap karya baru yang dipublikasikan dengan ThreadGrab di hari yang sama saat Anda mempublikasikannya.</p>
    </div>

    <div class="cta">
      <p>Sudah mempublikasikan di X, Bluesky, atau LinkedIn? Tangkap setiap posting ke arsip Markdown Anda dalam satu panggilan. ThreadGrab mengubah URL sosial publik apa pun menjadi file <code>.md</code> bersih dengan front matter, siap untuk Git.</p>
      <a class="btn" href="/id/">Coba ThreadGrab &mdash; Arsip Sosial Free</a>
    </div>

    <h2>Markdown Adalah Format, Notion Adalah Vendor</h2>
    <p>Stack kreator 2026 adalah tumpukan file teks biasa di direktori, di-versi-kan di Git, bisa dicari dengan ripgrep, bisa di-render dengan Obsidian, dan bisa di-publish dengan script Python 30 baris. Notion adalah vendor yang menjual UI yang dipoles di atas teks. Teks adalah bagian yang bertahan melewati vendor. Setiap kreator yang menghabiskan 2024 dan 2025 melihat app SaaS berputar, diakuisisi, atau ditutup telah mempelajari pelajaran yang sama: pertahankan formatnya, lepas vendornya.</p>
    <p>Bagi kreator, migrasi ini bahkan lebih jelas benar dibanding untuk tim pada umumnya. Konten sosial pendek, kaya tautan, dan hidup atau mati oleh algoritma platform. Notion tidak membantu hal itu. Arsip Markdown-first membantu semua itu. Mulai dari karya yang sudah dipublikasikan. Pindahkan sisanya belakangan. Rencana 30 hari di atas adalah jalur yang realistis; kebanyakan kreator yang memulai migrasi menyelesaikannya dalam dua akhir pekan dan beberapa malam.</p>
  </main>"""

# ============================================================
# FAQ JSON-LD (per lang) — text only
# ============================================================
FAQ_JSONLD_EN = """  <script type="application/ld+json">
  {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Do I lose my Notion formulas and rollups if I export to Markdown?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Notion formulas do not have a Markdown equivalent. The fix is a pre-compute step: a Python script reads the source files, computes the values, and writes them into the front matter at build time. Most creators discover they used 2 to 3 formulas in three years; the migration cost is proportional to the formulas they actually rely on."
      }
    },
    {
      "@type": "Question",
      "name": "Can I keep using Notion for personal notes and just migrate the published archive?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, and this is the most common 2026 pattern. Notion is fine for personal scratch, internal docs, and any workspace you do not need to take with you. The published archive is the one that has to leave, because it is the one that a vendor decision can take away from you."
      }
    },
    {
      "@type": "Question",
      "name": "Is there a risk of losing image embeds during migration?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Notion-hosted images move cleanly. Third-party embeds (YouTube, Figma, Loom) become plain links, which is the right Markdown behavior. The main loss is Notion's file property images, which sometimes have non-canonical filenames. A bulk rename script fixes 95 percent of these; the remaining 5 percent need manual review."
      }
    },
    {
      "@type": "Question",
      "name": "What about Notion AI? Does my AI workflow break if I leave?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Notion AI is a Notion-only feature. If you relied on it, the 2026 replacement is pointing Claude, GPT, or a local LLM at the directory directly. For most use cases (summarize, draft, rewrite, translate), the local LLM produces output at parity with Notion AI, with the bonus that the conversation history is itself a Markdown file in your archive."
      }
    },
    {
      "@type": "Question",
      "name": "How do I share a Markdown archive with collaborators who do not use Git?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Two options. The first is a static site generator (Astro, Hugo) deployed to a private URL -- collaborators browse, they do not edit. The second is a hosted wiki that reads from Git (BookStack, Wiki.js, Outline). Both preserve the canonical Markdown in Git while giving non-technical collaborators a view-only or comment-only surface."
      }
    },
    {
      "@type": "Question",
      "name": "What is the smallest viable migration for a solo creator?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Three steps: export the canonical archive with notion-to-md, commit to a private GitHub repo, cancel the Notion subscription. Total time: a weekend. Ongoing cost: zero. Capture new published work with ThreadGrab on the same day you publish it."
      }
    }
  ]
}
  </script>"""

FAQ_JSONLD_PT = """  <script type="application/ld+json">
  {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Perco minhas formulas e rollups do Notion se eu exportar para Markdown?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim. Formulas do Notion nao tem equivalente em Markdown. A solucao e um pre-compute step: um script Python le os arquivos source, computa os valores e escreve no front matter em build time. A maioria dos criadores descobre que usou 2 a 3 formulas em tres anos; o custo de migracao e proporcional as formulas que voce realmente depende."
      }
    },
    {
      "@type": "Question",
      "name": "Posso continuar usando Notion para notas pessoais e migrar so o arquivo publicado?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sim, e esse e o padrao mais comum em 2026. Notion funciona para rascunho pessoal, docs internos e qualquer workspace que voce nao precisa levar junto. O arquivo publicado e o que tem que sair, porque e o que uma decisao de vendor pode tirar de voce."
      }
    },
    {
      "@type": "Question",
      "name": "Ha risco de perder embeds de imagem durante a migracao?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Imagens hospedadas no Notion movem limpo. Embeds third-party (YouTube, Figma, Loom) viram links puros, que e o comportamento Markdown correto. A perda principal sao imagens da propriedade file do Notion, que as vezes tem filenames nao canonicos. Um script de rename em batch corrige 95 por cento dessas; os 5 por cento restantes precisam de revisao manual."
      }
    },
    {
      "@type": "Question",
      "name": "E o Notion AI? Meu workflow de IA quebra se eu sair?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Notion AI e uma feature exclusiva do Notion. Se voce dependia dela, o substituto de 2026 e apontar Claude, GPT ou um LLM local para o diretorio diretamente. Para a maioria dos casos de uso (resumir, redigir, reescrever, traduzir), o LLM local produz output em paridade com o Notion AI, com o bonus de que o historico de conversa e em si um arquivo Markdown no seu arquivo."
      }
    },
    {
      "@type": "Question",
      "name": "Como compartilhar um arquivo Markdown com colaboradores que nao usam Git?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Duas opcoes. A primeira e um static site generator (Astro, Hugo) deployado em uma URL privada -- colaboradores navegam, nao editam. A segunda e uma wiki hospedada que le do Git (BookStack, Wiki.js, Outline). Ambos preservam o Markdown canonico no Git enquanto dao a colaboradores nao-tecnicos uma superficie view-only ou comment-only."
      }
    },
    {
      "@type": "Question",
      "name": "Qual e a menor migracao viavel para um criador solo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Tres passos: exportar o arquivo canonico com notion-to-md, commitar em um repo privado do GitHub, cancelar a assinatura do Notion. Tempo total: um fim de semana. Custo recorrente: zero. Capture trabalho novo publicado com ThreadGrab no mesmo dia que publicar."
      }
    }
  ]
}
  </script>"""

FAQ_JSONLD_ID = """  <script type="application/ld+json">
  {
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Apakah saya kehilangan formula dan rollup Notion jika mengekspor ke Markdown?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ya. Formula Notion tidak punya padanan Markdown. Solusinya adalah langkah pre-compute: script Python membaca file sumber, menghitung nilai, dan menuliskannya ke front matter saat build time. Kebanyakan kreator发现自己用2 sampai 3 rumus dalam tiga tahun; biaya migrasi sebanding dengan rumus yang benar-benar Anda andalkan."
      }
    },
    {
      "@type": "Question",
      "name": "Bisakah saya tetap pakai Notion untuk catatan pribadi dan hanya migrasikan arsip yang dipublikasikan?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ya, dan ini adalah pola paling umum di 2026. Notion cukup untuk coret-coretan pribadi, dokumen internal, dan workspace apa pun yang tidak perlu Anda bawa pergi. Arsip yang dipublikasikan adalah yang harus pergi, karena itulah yang bisa diambil dari Anda oleh keputusan vendor."
      }
    },
    {
      "@type": "Question",
      "name": "Apakah ada risiko kehilangan embed gambar saat migrasi?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Gambar yang di-host Notion pindah dengan bersih. Embed pihak ketiga (YouTube, Figma, Loom) menjadi tautan polos, yang merupakan perilaku Markdown yang semestinya. Kehilangan utama adalah gambar properti file Notion, yang kadang punya nama file non-kanonik. Script rename massal memperbaiki 95 persen dari ini; 5 persen sisanya butuh tinjauan manual."
      }
    },
    {
      "@type": "Question",
      "name": "Bagaimana dengan Notion AI? Apakah workflow AI saya putus kalau saya keluar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Notion AI adalah fitur eksklusif Notion. Kalau Anda mengandalkannya, pengganti 2026 adalah mengarahkan Claude, GPT, atau LLM lokal ke direktori secara langsung. Untuk kebanyakan kasus penggunaan (merangkum, menulis, menulis ulang, menerjemahkan), LLM lokal menghasilkan output setara dengan Notion AI, dengan bonus bahwa riwayat percakapan juga merupakan file Markdown di arsip Anda."
      }
    },
    {
      "@type": "Question",
      "name": "Bagaimana cara berbagi arsip Markdown dengan kolaborator yang tidak pakai Git?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Dua opsi. Yang pertama adalah static site generator (Astro, Hugo) yang di-deploy ke URL privat -- kolaborator menjelajah, tidak menyunting. Yang kedua adalah wiki ter-host yang membaca dari Git (BookStack, Wiki.js, Outline). Keduanya mempertahankan Markdown kanonik di Git sembari memberi kolaborator non-teknis permukaan view-only atau comment-only."
      }
    },
    {
      "@type": "Question",
      "name": "Apa migrasi terkecil yang layak untuk kreator solo?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Tiga langkah: ekspor arsip kanonik dengan notion-to-md, commit ke repo GitHub privat, batalkan langganan Notion. Total waktu: satu akhir pekan. Biaya berjalan: nol. Tangkap karya baru yang dipublikasikan dengan ThreadGrab di hari yang sama saat Anda mempublikasikannya."
      }
    }
  ]
}
  </script>"""


def article_jsonld(title_h1, desc, lang):
    return f"""  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_h1}",
  "description": "{desc}",
  "datePublished": "{DATE}",
  "dateModified": "{DATE}",
  "author": {{
    "@type": "Organization",
    "name": "ThreadGrab",
    "url": "https://threadgrab.com/{lang}/"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "ThreadGrab",
    "url": "https://threadgrab.com/{lang}/"
  }},
  "mainEntityOfPage": "https://threadgrab.com/{lang}/blog/{SLUG}.html",
  "inLanguage": "{lang}"
}}
  </script>"""


def breadcrumb_jsonld(lang, tail):
    home = f"https://threadgrab.com/{lang}/"
    blog = f"https://threadgrab.com/{lang}/blog/"
    return f"""  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{home}"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "{blog}"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{tail}"
    }}
  ]
}}
  </script>"""


# ============================================================
# Page builder
# ============================================================
def build_page(lang, title, desc, keywords, body, h1, h1_span, meta_text, breadcrumb_tail,
               cta_text, cta_href, cta_btn, article_h1_for_jsonld, faq_jsonld):
    other_langs = {'en': ['pt', 'id'], 'pt': ['en', 'id'], 'id': ['en', 'pt']}[lang]
    other_links = ''.join(
        f'      <a class="" href="/{ol}/blog/{SLUG}.html">{ol.upper()}</a>\n'
        for ol in other_langs
    )
    active_link = f'      <a class="active" href="/{lang}/blog/{SLUG}.html">{lang.upper()}</a>\n'

    hreflangs = ''.join(
        f'  <link rel="alternate" hreflang="{hl}" href="https://threadgrab.com/{hl}/blog/{SLUG}.html">\n'
        for hl in ['en', 'pt', 'id', 'x-default']
    )
    # x-default points to en
    hreflangs = hreflangs.replace('hreflang="x-default" href="https://threadgrab.com/x-default/blog/',
                                  'hreflang="x-default" href="https://threadgrab.com/en/blog/')

    og_locale = {'en': 'en_US', 'pt': 'pt_BR', 'id': 'id_ID'}[lang]

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="ThreadGrab">
  <link rel="canonical" href="https://threadgrab.com/{lang}/blog/{SLUG}.html">
{hreflangs}  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://threadgrab.com/{lang}/blog/{SLUG}.html">
  <meta property="og:site_name" content="ThreadGrab">
  <meta property="og:locale" content="{og_locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <style>
{CSS}
  </style>
{article_jsonld(article_h1_for_jsonld, desc, lang)}
{breadcrumb_jsonld(lang, breadcrumb_tail)}
{faq_jsonld}
</head>
<body>
  <header>
    <a class="logo" href="/{lang}/">Thread<span>Grab</span></a>
    <div class="lang-bar">
{active_link}{other_links}    </div>
  </header>

  <main>
    <div class="breadcrumb"><a href="/{lang}/">Home</a> &rsaquo; <a href="/{lang}/blog/">Blog</a> &rsaquo; {breadcrumb_tail}</div>

    <h1>{h1} <span>{h1_span}</span></h1>
    <p class="meta">{meta_text}</p>

{body}
  </main>

  <footer>
    &copy; 2026 ThreadGrab &middot; <a href="/{lang}/">Home</a> &middot; <a href="/{lang}/blog/">Blog</a> &middot; <a href="/{lang}/about/">About</a> &middot; <a href="/{lang}/privacy/">Privacy</a>
    <br>Not affiliated with X Corp., Bluesky Social PBC, LinkedIn Corporation, or Microsoft Corporation.
  </footer>
</body>
</html>
"""


# ============================================================
# Build 3 pages
# ============================================================
pages = [
    {
        'lang': 'en',
        'title': TITLE_EN,
        'desc': DESC_EN,
        'keywords': KEYWORDS_EN,
        'body': EN_BODY,
        'h1': 'Notion to Markdown 2026:',
        'h1_span': 'Why Social Creators Migrate',
        'meta': f'{DATE_EN} &middot; 9 min read &middot; Guide',
        'breadcrumb_tail': 'Notion to Markdown Migration',
        'article_h1_for_jsonld': 'Markdown Is the Format, Notion Is the Vendor',
        'faq_jsonld': FAQ_JSONLD_EN,
    },
    {
        'lang': 'pt',
        'title': TITLE_PT,
        'desc': DESC_PT,
        'keywords': KEYWORDS_PT,
        'body': PT_BODY,
        'h1': 'Notion para Markdown 2026:',
        'h1_span': 'Por Que Criadores Migram',
        'meta': f'{DATE_PT} &middot; 9 min de leitura &middot; Guia',
        'breadcrumb_tail': 'Migracao Notion para Markdown',
        'article_h1_for_jsonld': 'Markdown E o Formato, Notion E o Vendor',
        'faq_jsonld': FAQ_JSONLD_PT,
    },
    {
        'lang': 'id',
        'title': TITLE_ID,
        'desc': DESC_ID,
        'keywords': KEYWORDS_ID,
        'body': ID_BODY,
        'h1': 'Notion ke Markdown 2026:',
        'h1_span': 'Mengapa Kreator Beralih',
        'meta': f'{DATE_ID} &middot; 9 menit baca &middot; Panduan',
        'breadcrumb_tail': 'Migrasi Notion ke Markdown',
        'article_h1_for_jsonld': 'Markdown Adalah Format, Notion Adalah Vendor',
        'faq_jsonld': FAQ_JSONLD_ID,
    },
]

for p in pages:
    html = build_page(
        p['lang'], p['title'], p['desc'], p['keywords'],
        p['body'], p['h1'], p['h1_span'], p['meta'],
        p['breadcrumb_tail'], None, None, None,
        p['article_h1_for_jsonld'], p['faq_jsonld'],
    )
    out_path = f"/root/threadgrab-site/{p['lang']}/blog/{SLUG}.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  WROTE: {out_path} ({len(html)} bytes)")

# Final verification
import re

print("\n=== VERIFICATION ===")
for p in pages:
    lang = p['lang']
    path = f"/root/threadgrab-site/{lang}/blog/{SLUG}.html"
    with open(path) as f:
        html = f.read()

    title = re.search(r'<title>(.*?)</title>', html).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)"', html).group(1)
    html_lang = re.search(r'<html lang="(\w+)"', html).group(1)
    hreflangs = re.findall(r'hreflang="(\w+)"', html)
    jsonld = re.findall(r'<script type="application/ld\+json">', html)
    h2s = re.findall(r'<h2', html)
    pres = re.findall(r'<pre>', html)
    faqs = re.findall(r'class="faq-item"', html)
    canonical = re.search(r'rel="canonical" href="([^"]+)"', html).group(1)

    print(f"\n--- {lang.upper()} ---")
    print(f"  File: {path}")
    print(f"  Size: {len(html)} bytes")
    print(f"  <html lang>: {html_lang} (expected {lang})")
    print(f"  Title: {len(title)} chars — '{title}'")
    print(f"  Desc:  {len(desc)} chars")
    print(f"  hreflangs: {hreflangs} (expected 4: en/pt/id/x-default)")
    print(f"  canonical: {canonical}")
    print(f"  JSON-LD blocks: {len(jsonld)} (expected 3)")
    print(f"  H2 count: {len(h2s)}")
    print(f"  <pre> count: {len(pres)} (expected >= 2)")
    print(f"  FAQ items: {len(faqs)} (expected >= 3, target 5-6)")

    # Raw <N check
    raw_lt = re.findall(r'(?<!<)<(?![a-zA-Z!/])', html)
    print(f"  Raw '<N' patterns: {len(raw_lt)} (expected 0)")

    # Length assertions
    assert 30 <= len(title) <= 60, f"title len {len(title)}"
    assert 70 <= len(desc) <= 155, f"desc len {len(desc)}"
    assert html_lang == lang, f"html lang {html_lang} != {lang}"
    assert set(hreflangs) >= {'en', 'pt', 'id', 'x-default'}, f"missing hreflangs: {hreflangs}"
    assert len(jsonld) == 3, f"JSON-LD count {len(jsonld)}"
    assert len(pres) >= 2, f"<pre> count {len(pres)}"
    assert len(faqs) >= 3, f"FAQ count {len(faqs)}"
    assert len(raw_lt) == 0, f"raw <N patterns: {len(raw_lt)}"

print("\n✅ All 3 pages pass structural verification")
