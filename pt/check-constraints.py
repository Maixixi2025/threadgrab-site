import re, html

with open('/root/threadgrab-site/pt/blog/tweet-md-redirecionador-navegador-2026.html', 'r') as f:
    content = f.read()

print("=== CONSTRAINT CHECKS ===")

# 1. html lang='pt'
lang_m = re.search(r'<html\s+lang="([^"]+)"', content)
lang_v = lang_m.group(1) if lang_m else 'NOT FOUND'
print(f"1. html lang: {lang_v}")

# 2. canonical
canon_m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
canon_v = canon_m.group(1) if canon_m else 'NOT FOUND'
print(f"2. canonical: {canon_v}")

# 3. Title
title_m = re.search(r'<title>(.*?)</title>', content)
title_text = title_m.group(1) if title_m else 'NOT FOUND'
title_len = len(title_text)
print(f"3. Title: '{title_text}' ({title_len} chars) - valid 30-60? {30 <= title_len <= 60}")

# 4. Description
desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
desc_v = desc_m.group(1) if desc_m else 'NOT FOUND'
desc_decoded = html.unescape(desc_v)
desc_len = len(desc_decoded)
print(f"4. Description: '{desc_decoded}' ({desc_len} chars) - valid 70-155? {70 <= desc_len <= 155}")

# 5. hreflangs
hreflangs = re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"', content)
print(f"5. Hreflangs count: {len(hreflangs)}")
for hl in hreflangs:
    print(f"   hreflang=\"{hl[0]}\" href=\"{hl[1]}\"")

# 6. og:locale
og_locale_m = re.search(r'<meta\s+property="og:locale"\s+content="([^"]+)"', content)
og_locale_v = og_locale_m.group(1) if og_locale_m else 'NOT FOUND'
print(f"6. og:locale: {og_locale_v}")

# 7. JSON-LD inLanguage
json_inlang_m = re.search(r'"inLanguage":\s*"([^"]+)"', content)
json_inlang_v = json_inlang_m.group(1) if json_inlang_m else 'NOT FOUND'
print(f"7. JSON-LD inLanguage: {json_inlang_v}")

# 8. og:title in PT
og_title_m = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', content)
og_title_v = og_title_m.group(1) if og_title_m else 'NOT FOUND'
print(f"8. og:title: '{og_title_v}'")

# 9. og:description in PT
og_desc_m = re.search(r'<meta\s+property="og:description"\s+content="([^"]+)"', content)
og_desc_v = og_desc_m.group(1) if og_desc_m else 'NOT FOUND'
print(f"9. og:description: '{og_desc_v}'")

# 10. twitter:title in PT
tw_title_m = re.search(r'<meta\s+name="twitter:title"\s+content="([^"]+)"', content)
tw_title_v = tw_title_m.group(1) if tw_title_m else 'NOT FOUND'
print(f"10. twitter:title: '{tw_title_v}'")

# 11. lang-bar PT active
active_pt = 'href="/pt/blog/tweet-md-redirecionador-navegador-2026.html" class="active"' in content
en_link = 'href="/en/blog/tweet-md-browser-redirect-2026.html">EN<' in content
id_link = 'href="/id/blog/tweet-md-pengalihan-peramban-2026.html">ID<' in content
print(f"11. PT active: {active_pt}, EN link: {en_link}, ID link: {id_link}")

# 12. meta date
meta_m = re.search(r'<div class="meta">([^<]+)</div>', content)
meta_text = meta_m.group(1) if meta_m else 'NOT FOUND'
print(f"12. Meta date: '{meta_text}'")
print(f"    Has 'Julho': {'Julho' in meta_text}")

# 13. Breadcrumb
breadcrumb_section = content.split('breadcrumb')[1].split('</div>')[0] if 'breadcrumb' in content else ''
home_link = 'href="/pt/"' in breadcrumb_section
blog_link = 'href="/pt/blog/"' in breadcrumb_section
print(f"13. Breadcrumb /pt/: {home_link}, /pt/blog/: {blog_link}")

# 14. Footer
footer_section = content.split('<footer>')[1].split('</footer>')[0] if '<footer>' in content else ''
footer_home = 'href="/pt/"' in footer_section
footer_blog = 'href="/pt/blog/"' in footer_section
print(f"14. Footer /pt/: {footer_home}, /pt/blog/: {footer_blog}")

# 15. Internal link
internal_link = 'href="/pt/blog/tweet-md-vs-threadgrab-2026.html"' in content
print(f"15. tweet-md-vs-threadgrab link: {internal_link}")

# 16. FAQ count
faq_items = re.findall(r'"@type":\s*"Question"', content)
print(f"16. FAQ items (JSON-LD): {len(faq_items)}")

# 17. FAQ items in HTML
faq_html_items = content.count('<div class="faq-item">')
print(f"    FAQ items (HTML): {faq_html_items}")

# 18. Title has no span tags inside
has_span_in_title = '<span>' in title_text
print(f"17. Title has <span> tag inside: {has_span_in_title}")

# 19. Proper names preserved
print("18. Proper names:")
for name in ['tweet.md', 'ThreadGrab', 'GitHub', 'Slack', 'Reddit', 'Google Docs', 'Tampermonkey', 'Redirector']:
    count = content.count(name)
    print(f"    '{name}': {count}")

print("\n=== ALL CHECKS COMPLETE ===")
