"""7-gate validation + cross-language identity checks for the writemark article.

Cloned from drafts/validate-screenpipe-article-2026.py — only SLUGS, EXPECTED_TITLE,
EXPECTED_CANONICAL differ. The 7 gates are:

  G1 title: visible text 30-60 chars + matches expected
  G2 desc:  70-155 chars
  G3 hreflang: en/pt/id/x-default present, x-default → EN canonical
  G4 og:locale: matches lang
  G5 canonical: matches lang
  G6 jsonld: 3 blocks, types = [Article, BreadcrumbList, FAQPage]
  G7 FAQ: >= 3 mainEntity

Plus cross-language:
  - code blocks byte-identical
  - hreflang mutual verification (each lang's hreflang for OTHER langs uses
    that lang's actual canonical, not a stale URL)
"""
import os, re, json

WORKDIR = '/root/threadgrab-site'
os.chdir(WORKDIR)

SLUGS = {
    'en': 'writemark-markdown-inline-editor-2026',
    'pt': 'writemark-editor-markdown-embutido-2026',
    'id': 'writemark-editor-markdown-sebaris-2026',
}
EXPECTED_TITLE = {
    'en': 'Writemark 2026: Embed Markdown Editor Anywhere',
    'pt': 'Writemark 2026: Editor Markdown Embutido',
    'id': 'Writemark 2026: Editor Markdown Sebaris',
}
EXPECTED_CANONICAL = {l: f'https://threadgrab.com/{l}/blog/{SLUGS[l]}.html' for l in SLUGS}
EXPECTED_LOCALE = {'en': 'en_US', 'pt': 'pt_BR', 'id': 'id_ID'}

errors = []
for lang, slug in SLUGS.items():
    fp = f'drafts/articles/{slug}.html'
    print(f'\n=== {lang.upper()} : {fp} ===')
    if not os.path.exists(fp):
        errors.append(f'[{lang}] file missing')
        continue
    content = open(fp).read()
    title_m = re.search(r'<title>(.*?)</title>', content)
    if not title_m:
        errors.append(f'[{lang}] G1 no title')
    else:
        vis = re.sub(r'<[^>]+>', '', title_m.group(1)).replace('&amp;','&').strip()
        if vis != EXPECTED_TITLE[lang]:
            errors.append(f'[{lang}] G1 title mismatch {vis!r} vs {EXPECTED_TITLE[lang]!r}')
        if not (30 <= len(vis) <= 60):
            errors.append(f'[{lang}] G1 title len {len(vis)}')
        print(f'  G1 title {len(vis)} ({vis})')

    desc_m = re.search(r'<meta name="description" content="(.*?)"', content)
    if not desc_m:
        errors.append(f'[{lang}] G2 no desc')
    else:
        d = desc_m.group(1).replace('&amp;','&')
        if not (70 <= len(d) <= 155):
            errors.append(f'[{lang}] G2 desc len {len(d)}')
        print(f'  G2 desc {len(d)}')

    hreflangs = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', content)
    hl_set = {h for h,_ in hreflangs}
    if hl_set != {'en','pt','id','x-default'}:
        errors.append(f'[{lang}] G3 hreflang set {hl_set}')
    xdef = next((h for h in hreflangs if h[0]=='x-default'), None)
    if xdef and xdef[1] != EXPECTED_CANONICAL['en']:
        errors.append(f'[{lang}] G3 x-default {xdef[1]}')
    print(f'  G3 hreflang ok')

    og_m = re.search(r'<meta property="og:locale" content="([^"]+)"', content)
    if not og_m or og_m.group(1) != EXPECTED_LOCALE[lang]:
        errors.append(f'[{lang}] G4 og:locale {og_m.group(1) if og_m else None}')
    print(f'  G4 og:locale {og_m.group(1)}')

    can = re.search(r'<link rel="canonical" href="([^"]+)"', content)
    if not can or can.group(1) != EXPECTED_CANONICAL[lang]:
        errors.append(f'[{lang}] G5 canonical {can.group(1) if can else None}')
    print(f'  G5 canonical {can.group(1)}')

    blocks = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL)
    if len(blocks) != 3:
        errors.append(f'[{lang}] G6 count {len(blocks)}')
    types=[]
    for b in blocks:
        try:
            d=json.loads(b); types.append(d.get('@type'))
        except Exception as e: errors.append(f'[{lang}] json parse: {e}')
    if types != ['Article','BreadcrumbList','FAQPage']:
        errors.append(f'[{lang}] G6 types {types}')
    print(f'  G6 jsonld {types}')

    faq_block = next((b for b in blocks if '"FAQPage"' in b), None)
    if faq_block:
        d=json.loads(faq_block)
        n=len(d.get('mainEntity',[]))
        if n < 3:
            errors.append(f'[{lang}] G7 FAQ {n}')
        print(f'  G7 faq {n}')

# Cross-language: code-block identity
print('\n=== Cross-lang code identity ===')
en=open(f'drafts/articles/{SLUGS["en"]}.html').read()
pt=open(f'drafts/articles/{SLUGS["pt"]}.html').read()
idc=open(f'drafts/articles/{SLUGS["id"]}.html').read()
en_c=re.findall(r'<pre><code>(.*?)</code></pre>',en,re.DOTALL)
pt_c=re.findall(r'<pre><code>(.*?)</code></pre>',pt,re.DOTALL)
id_c=re.findall(r'<pre><code>(.*?)</code></pre>',idc,re.DOTALL)
print(f'  blocks EN={len(en_c)} PT={len(pt_c)} ID={len(id_c)}')
for a,b,lab in [(en_c,pt_c,'EN-PT'),(en_c,id_c,'EN-ID'),(pt_c,id_c,'PT-ID')]:
    if a==b:
        print(f'  {lab} identical')
    else:
        for j,(x,y) in enumerate(zip(a,b)):
            if x!=y:
                errors.append(f'[cross] {lab} block {j} differ: en={x!r} vs pt={y!r}')

# Cross-language: hreflang mutual verification
print('\n=== Cross-lang hreflang ===')
for lang,slug in SLUGS.items():
    text=open(f'drafts/articles/{slug}.html').read()
    h=dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"',text))
    if SLUGS['pt'] not in h.get('pt',''):
        errors.append(f'[{lang}] hreflang pt slug')
    if SLUGS['id'] not in h.get('id',''):
        errors.append(f'[{lang}] hreflang id slug')
    if SLUGS['en'] not in h.get('en',''):
        errors.append(f'[{lang}] hreflang en slug')
    if lang != 'en' and h.get('x-default') != EXPECTED_CANONICAL['en']:
        errors.append(f'[{lang}] x-default wrong')
    print(f'  {lang} hreflang pt={SLUGS["pt"] in h.get("pt","")} id={SLUGS["id"] in h.get("id","")} en={SLUGS["en"] in h.get("en","")}')

print('\n'+'='*60)
if errors:
    print(f'❌ {len(errors)} ERRORS:')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('✅ ALL 7 GATES PASS + cross-lang verification')