#!/usr/bin/env python3
"""Regenerate threadgrab.com sitemap.xml from ground truth (repo files + each page's own hreflang).

Fixes the 2026-08-16 regression where sitemap dropped ID/PT coverage (130 missing URLs).
Ground-truth model: one <url> entry per content piece (canonical + hreflang alternates),
built by clustering each article's self-declared canonical/hreflang variant set.
"""
import os, re, subprocess, sys

ROOT = '/root/threadgrab-site'
DOMAIN = 'https://threadgrab.com'
TODAY = '2026-08-16'

def git_lastmod(relpath):
    try:
        r = subprocess.run(
            ['git', '-C', ROOT, 'log', '-1', '--format=%cd', '--date=short', '--', relpath],
            capture_output=True, text=True, timeout=10)
        d = r.stdout.strip()
        if re.match(r'^\d{4}-\d{2}-\d{2}$', d):
            return d
    except Exception:
        pass
    return TODAY

def xml_escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# ---- 1. Cluster articles into content groups (mutual-links model) ----
# Two real pages are the SAME content iff they MUTUALLY reference each other via
# hreflang (en<->pt<->id trilingual cross-links). A one-way reference (e.g. an EN
# page whose localized slugs don't exist on disk) is NOT a mutual link, so the
# EN page and the one-way-referencing ID/PT pages stay in separate clusters.
REAL_BLOG_RE = re.compile(rf'{DOMAIN}/(en|id|pt)/blog/([^/]+\.html)$')
page_urls = []            # all real article page urls
mutual_of = {}            # page_url -> set of real page urls it mutually links to
for lang in ['en', 'id', 'pt']:
    blog_dir = os.path.join(ROOT, lang, 'blog')
    for f in sorted(os.listdir(blog_dir)):
        if not f.endswith('.html') or f == 'index.html':
            continue
        url = f'{DOMAIN}/{lang}/blog/{f}'
        with open(os.path.join(blog_dir, f), encoding='utf-8') as fh:
            c = fh.read()
        canon_m = re.search(r'<link rel="canonical" href="([^"]+)"', c)
        decl = {canon_m.group(1) if canon_m else url}
        for hl, href in re.findall(r'<link rel="alternate" hreflang="(en|pt|id)" href="([^"]+)"', c):
            decl.add(href)
        # real URLs this page declares
        real_decl = {v for v in decl if REAL_BLOG_RE.match(v)}
        page_urls.append(url)
        mutual_of[url] = (real_decl - {url})  # candidate mutual partners (minus self)

# Build mutual pairs: both directions must list each other
mutual_pairs = set()
for a in page_urls:
    for b in mutual_of[a]:
        if a in mutual_of.get(b, set()):
            mutual_pairs.add(frozenset((a, b)))

# Union-find over mutual pairs
parent = {u: u for u in page_urls}
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[rb] = ra
for pair in mutual_pairs:
    a, b = tuple(pair)
    union(a, b)

# Group page urls by root
groups = {}
for u in page_urls:
    groups.setdefault(find(u), []).append(u)

def lang_of(url):
    if '/en/' in url: return 'en'
    if '/pt/' in url: return 'pt'
    return 'id'

def ordered_variants(variants):
    """Return variant URLs ordered en, pt, id (site convention)."""
    out = []
    for pref in ['/en/', '/pt/', '/id/']:
        for v in sorted(variants):
            if pref in v:
                out.append(v)
    return out

def cluster_loc(pages):
    """<loc>: the 'primary' variant. Prefer en; else the group's single real page."""
    en = [v for v in pages if '/en/' in v]
    if en:
        # For a trilingual group the en variant is the primary; for a standalone
        # EN page it is itself the only loc.
        return en[0]
    return sorted(pages)[0]

entry_blocks = []
seen_locs = set()

# Article clusters
for root_node, pages in groups.items():
    real_variants = set(pages)
    loc = cluster_loc(sorted(real_variants))
    ov = ordered_variants(real_variants)
    if not ov:
        continue
    lastmod = git_lastmod(loc.replace(DOMAIN + '/', ''))
    lines = ['  <url>', f'    <loc>{xml_escape(loc)}</loc>']
    for v in ov:
        lines.append(f'    <xhtml:link rel="alternate" hreflang="{lang_of(v)}" href="{xml_escape(v)}"/>')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{xml_escape(loc)}"/>')
    lines.append(f'    <lastmod>{lastmod}</lastmod>')
    lines.append('    <changefreq>monthly</changefreq>')
    lines.append('    <priority>0.8</priority>')
    lines.append('  </url>')
    entry_blocks.append('\n'.join(lines))
    seen_locs.add(loc)

# ---- 2. Language roots ----
for lang in ['en', 'pt', 'id']:
    loc = f'{DOMAIN}/{lang}/'
    ov = [f'{DOMAIN}/{l}/' for l in ['en', 'pt', 'id']]
    lines = ['  <url>', f'    <loc>{loc}</loc>']
    for l in ['en', 'pt', 'id']:
        lines.append(f'    <xhtml:link rel="alternate" hreflang="{l}" href="{DOMAIN}/{l}/"/>')
    lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/en/"/>')
    lines.append(f'    <lastmod>{TODAY}</lastmod>')
    lines.append('    <changefreq>weekly</changefreq>')
    lines.append('    <priority>1.0</priority>')
    lines.append('  </url>')
    entry_blocks.append('\n'.join(lines))
    seen_locs.add(loc)

# ---- 3. About + Privacy pages (per language) ----
for lang in ['en', 'pt', 'id']:
    for page in ['about', 'privacy']:
        fp = os.path.join(ROOT, lang, f'{page}.html')
        if not os.path.isfile(fp):
            continue
        loc = f'{DOMAIN}/{lang}/{page}.html'
        lastmod = git_lastmod(f'{lang}/{page}.html')
        # hreflang to same-page in other languages if those files exist
        alts = []
        for l2 in ['en', 'pt', 'id']:
            if os.path.isfile(os.path.join(ROOT, l2, f'{page}.html')):
                alts.append(f'    <xhtml:link rel="alternate" hreflang="{l2}" href="{DOMAIN}/{l2}/{page}.html"/>')
        lines = ['  <url>', f'    <loc>{xml_escape(loc)}</loc>'] + alts
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/en/{page}.html"/>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append('    <changefreq>monthly</changefreq>')
        lines.append('    <priority>0.5</priority>')
        lines.append('  </url>')
        entry_blocks.append('\n'.join(lines))
        seen_locs.add(loc)

# ---- 4. Assemble ----
header = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
          '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
footer = '</urlset>\n'
sitemap = header + '\n'.join(entry_blocks) + '\n' + footer

out = os.path.join(ROOT, 'sitemap.xml')
with open(out, 'w', encoding='utf-8') as f:
    f.write(sitemap)

print(f"Written {out}")
print(f"Total <url> entries: {len(entry_blocks)}")
print(f"Article groups: {len(groups)}")
# Verify no duplicate locs
dupes = len(seen_locs), len(entry_blocks)
print(f"unique locs / entries: {dupes}")
