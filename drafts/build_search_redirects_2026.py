#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the trilingual threadgrab article on search-result redirects (EN/PT/ID).

Topic consumed from the daily briefing 3ea88f8bb2d0 2026-11-20 (item 2, social
tools): "Brave search adds redirect anti-scraping" -> brave.com/blog/google-goto-anti-scraping/

Primary sources verified 2026-11-20 by direct fetch:
  - brave.com/blog/google-goto-anti-scraping/      (HTTP 200, datePublished 2026-11-11)
  - brave.com/blog/search-api-agentic-payments/     (HTTP 200, datePublished 2026-11-12)
  - brave.com/search/api/                          (HTTP 200, pricing JSON-LD)
  - search.agent.s.brave.app/llms.txt               (HTTP 200, agent spec)
  - search.agent.s.brave.app/openapi.json           (HTTP 200, x-payment-info)
  - api-dashboard.search.brave.com/documentation/guides/agent-payments (HTTP 200)
  - github.com/stripe/purl                         (HTTP 200)
  - HN Algolia: SEL "Google confirms deploying goto..." 2026-08-27;
                Brave cloaking post 2026-11-18;
                x402 post 2026-11-13 with 263 points

Run:  python3 drafts/build_search_redirects_2026.py
"""
import json
import os
import re
import sys

ROOT = '/root/threadgrab-site'
os.chdir(ROOT)

DATE_ISO = '2026-11-20'
DATE_EN = 'November 20, 2026'
DATE_PT = '20 de Novembro, 2026'
DATE_ID = '20 November 2026'

# Single-EN-slug pattern (preferred for new articles since 2026-08-19).
SLUG = 'search-result-redirects-cloaking-goto-2026'

READ_MIN = 12

CATEGORY = {
    'en': 'Search &amp; Discovery',
    'pt': 'Busca e Descoberta',
    'id': 'Pencarian dan Penemuan',
}

READ_LABEL = {
    'en': 'min read',
    'pt': 'min de leitura',
    'id': 'menit baca',
}

LOCALE = {'en': 'en_US', 'pt': 'pt_BR', 'id': 'id_ID'}

# ---------------------------------------------------------------- CSS (shared)
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
    h2 { font-size: 1.4rem; margin: 36px 0 16px; }
    h3 { font-size: 1.1rem; margin: 24px 0 12px; }
    p { margin-bottom: 16px; color: #ccc; }
    a { color: #20d5ec; }
    table { width: 100%; border-collapse: collapse; margin: 20px 0 28px; font-size: 0.9rem; }
    th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid #222; }
    th { color: #20d5ec; font-weight: 600; }
    td { color: #ccc; }
    pre { background: #1a1a1a; border-radius: 8px; padding: 16px; overflow-x: auto; margin: 16px 0 24px; }
    pre code { font-family: 'SF Mono', Monaco, monospace; font-size: 0.85rem; color: #e0e0e0; }
    ul { margin: 0 0 16px 20px; color: #ccc; }
    li { margin-bottom: 8px; }
    .faq-item { margin-bottom: 20px; }
    .faq-item h3 { font-size: 1rem; color: #fff; margin-bottom: 6px; }
    .faq-item p { color: #aaa; font-size: 0.95rem; }
    .related { background: #141414; border: 1px solid #1f1f1f; border-radius: 10px; padding: 18px 22px; margin: 28px 0; }
    .related h3 { margin-top: 0; }
    .related ul { list-style: none; padding: 0; margin: 0; }
    .related a { text-decoration: none; }
    .cta { background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); border-radius: 12px; padding: 28px; margin: 32px 0 24px; }
    .cta h3 { margin-top: 0; margin-bottom: 8px; color: #fff; }
    .cta-btn { display: inline-block; margin-top: 12px; padding: 10px 22px; background: #20d5ec; color: #000; font-weight: 600; border-radius: 6px; text-decoration: none; }
    footer { border-top: 1px solid #1a1a1a; padding: 24px; text-align: center; color: #666; font-size: 0.85rem; }
    footer a { color: #888; text-decoration: none; margin: 0 8px; }
    footer a:hover { color: #20d5ec; }
    .sources { color: #777; font-size: 0.88rem; line-height: 1.7; }
    .sources a { color: #20d5ec; }
"""

# ---------------------------------------------------------------- code blocks
# Byte-identical across EN / PT / ID (validator gate: code blocks byte-identical).
# No "<" or ">" characters inside, so the no_raw_lt_in_code gate passes.
CODE1 = """# 1. Resolve the redirect, then archive the destination - never the redirect.
#    A search result link may be a /goto or /go URL. It expires, and it is not
#    the source, so it must never be the thing you store.

curl -sL -o archive/page.html \\
  -w 'resolved_url=%{url_effective}\\nhttp_code=%{http_code}\\nhops=%{num_redirects}\\n' \\
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \\
  "https://example.com/go/abc123"

# 2. Write the resolved URL into a provenance sidecar next to the capture.

printf '%s\\n' \\
  "resolved_url: https://example.com/article-slug" \\
  "captured_at: 2026-11-20T09:00:00Z" \\
  "source_kind: search_result" | tee archive/provenance.yml"""

CODE2 = """# 3. Pay-per-request search: one request, one USDC micropayment on Base.
#    purl is the Stripe CLI wallet; --max-amount is the ceiling in base units,
#    and 5000 base units is the price of one search ($0.005).

purl --max-amount 5000 'https://search.agent.s.brave.app/res/v1/web/search?q=social+archive+markdown'

# 4. Keep your own copy of the thread you found, with the capture time attached.

curl -s "https://threadgrab.com/api/profile/USERNAME" \\
  -H "Accept: application/json" \\
  -o archive/USERNAME-profile.json"""


def load_content(lang):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'content_search_redirects_%s.py' % lang)
    ns = {}
    with open(path, encoding='utf-8') as fh:
        exec(compile(fh.read(), path, 'exec'), ns)
    return ns['CONTENT']


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build_jsonld(lang, c):
    title = c['title']
    desc = c['desc']
    home = 'https://threadgrab.com/%s/' % lang
    url = 'https://threadgrab.com/%s/blog/%s.html' % (lang, SLUG)
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
        "author": {"@type": "Organization", "name": "ThreadGrab", "url": home},
        "publisher": {
            "@type": "Organization",
            "name": "ThreadGrab",
            "url": home,
            "logo": {"@type": "ImageObject", "url": "https://threadgrab.com/og-image.png"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": home},
            {"@type": "ListItem", "position": 2, "name": "Blog",
             "item": "https://threadgrab.com/%s/blog/" % lang},
            {"@type": "ListItem", "position": 3, "name": title, "item": url},
        ],
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in c['faq']
        ],
    }
    return (json.dumps(article, indent=2, ensure_ascii=False),
            json.dumps(crumbs, indent=2, ensure_ascii=False),
            json.dumps(faq, indent=2, ensure_ascii=False))


def build_html(lang, c):
    title = c['title']
    desc = c['desc']
    home = 'https://threadgrab.com/%s/' % lang
    url = 'https://threadgrab.com/%s/blog/%s.html' % (lang, SLUG)
    a_article, a_crumbs, a_faq = build_jsonld(lang, c)
    date_txt = {'en': DATE_EN, 'pt': DATE_PT, 'id': DATE_ID}[lang]

    body = c['body'].replace('__CODE1__', CODE1).replace('__CODE2__', CODE2)

    faq_html = '\n'.join(
        '<div class="faq-item"><h3>' + q + '</h3><p>' + a + '</p></div>'
        for q, a in c['faq'])
    body = body.replace('__FAQ_BLOCK__', faq_html)

    related_html = '\n'.join(
        '<li><a href="' + href + '">' + text + '</a></li>'
        for href, text in c['related'])

    cls_en = 'active' if lang == 'en' else ''
    cls_pt = 'active' if lang == 'pt' else ''
    cls_id = 'active' if lang == 'id' else ''

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="keywords" content="{esc(c['keywords'])}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="ThreadGrab">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="https://threadgrab.com/en/blog/{SLUG}.html">
  <link rel="alternate" hreflang="pt" href="https://threadgrab.com/pt/blog/{SLUG}.html">
  <link rel="alternate" hreflang="id" href="https://threadgrab.com/id/blog/{SLUG}.html">
  <link rel="alternate" hreflang="x-default" href="https://threadgrab.com/en/blog/{SLUG}.html">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="ThreadGrab">
  <meta property="og:locale" content="{LOCALE[lang]}">
  <meta property="article:published_time" content="{DATE_ISO}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <style>
{CSS}  </style>
</head>
<body>
  <header>
    <a class="logo" href="{home}">Thread<span>Grab</span></a>
    <div class="lang-bar">
      <a href="https://threadgrab.com/en/blog/{SLUG}.html" class="{cls_en}">EN</a>
      <a href="https://threadgrab.com/pt/blog/{SLUG}.html" class="{cls_pt}">PT</a>
      <a href="https://threadgrab.com/id/blog/{SLUG}.html" class="{cls_id}">ID</a>
    </div>
  </header>
  <main>
    <div class="breadcrumb">
      <a href="{home}">Home</a> &rsaquo; <a href="/{lang}/blog/">Blog</a> &rsaquo; {esc(title)}
    </div>

    <h1>{esc(title)}</h1>
    <p class="meta">{date_txt} &middot; {READ_MIN} {READ_LABEL[lang]} &middot; {CATEGORY[lang]}</p>

    <script type="application/ld+json">
{a_article}
    </script>

    <script type="application/ld+json">
{a_crumbs}
    </script>

    <script type="application/ld+json">
{a_faq}
    </script>
{body}

    <div class="related"><h3>Related on ThreadGrab</h3><ul>
{related_html}
    </ul></div>

    <div class="cta">
      <h3>{c['cta_title']}</h3>
      <p style="margin-bottom: 8px;">{c['cta_body']}</p>
      <a href="{home}" class="cta-btn">{c['cta_btn']}</a>
    </div>

    <div class="sources">
{c['sources']}
    </div>
  </main>
  <footer>
    <a href="{home}">Home</a>
    <a href="/{lang}/blog/">Blog</a>
    <a href="/{lang}/about/">About</a>
    <a href="/{lang}/privacy/">Privacy</a>
    <span style="margin-left:12px;">&copy; 2026 ThreadGrab</span>
  </footer>
</body>
</html>
'''


def main():
    ok = True
    for lang in ['en', 'pt', 'id']:
        c = load_content(lang)
        t = c['title']
        d = c['desc']
        print('%s: title=%dc desc=%dc' % (lang, len(t), len(d)))
        if not (30 <= len(t) <= 75):
            print('  FAIL title length %s' % lang)
            ok = False
        if not (70 <= len(d) <= 155):
            print('  FAIL desc length %s' % lang)
            ok = False
        html = build_html(lang, c)
        assert '<html lang="%s">' % lang in html
        assert html.count('<link rel="alternate" hreflang=') == 4
        assert html.count('<script type="application/ld+json">') == 3
        assert html.count('<div class="faq-item">') == len(c['faq']) >= 5
        assert len(re.findall(r'<h2>', html)) >= 7
        assert len(re.findall(r'<pre><code>', html)) >= 2
        assert not re.findall(r'[\u4e00-\u9fff]', html), 'CJK found'
        assert not re.findall(r'[\u0400-\u04FF]', html), 'Cyrillic found'
        assert '__CODE' not in html, 'unreplaced code placeholder'
        assert '__FAQ' not in html, 'unreplaced faq placeholder'
        path = '%s/blog/%s.html' % (lang, SLUG)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
        print('  wrote %s (%d bytes)' % (path, len(html)))
    if not ok:
        print('LENGTH GATE FAILED')
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
