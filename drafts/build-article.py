import json, os, re

os.chdir('/root/threadgrab-site')

slug = "microsoft-markitdown-social-content-2026"
date = "2026-06-19"

en_title = "Microsoft markitdown: Social Content to Markdown Workflow"
en_desc  = "Microsoft markitdown converts Office docs, PDFs, and HTML to Markdown. Combine with ThreadGrab for a complete social content to Markdown pipeline."

pt_title = "Microsoft markitdown: Fluxo de Conteudo Social para Markdown"
pt_desc  = "Microsoft markitdown converte documentos Office, PDFs e HTML em Markdown. Use com ThreadGrab para pipeline completo de conteudo social para Markdown."

id_title = "Microsoft markitdown: Alur Konten Sosial ke Markdown"
id_desc  = "Microsoft markitdown mengonversi dokumen Office, PDF, dan HTML ke Markdown. Gabungkan dengan ThreadGrab untuk pipeline konten sosial ke Markdown."

assert 30 <= len(en_title) <= 60
assert 70 <= len(en_desc) <= 155
assert 30 <= len(pt_title) <= 60
assert 70 <= len(pt_desc) <= 155
assert 30 <= len(id_title) <= 60
assert 70 <= len(id_desc) <= 155

print(f"EN t={len(en_title)} d={len(en_desc)}")
print(f"PT t={len(pt_title)} d={len(pt_desc)}")
print(f"ID t={len(id_title)} d={len(id_desc)}")

# Read existing blog index files to understand the structure
en_index = open('en/blog/index.html').read()
pt_index = open('pt/blog/index.html').read()
id_index = open('id/blog/index.html').read()

# Insert new entry at top of post-list in each index
# Pattern: first <li> entry after <ul class="post-list">
en_new_entry = '''        <ul class="post-list">
      <li>
        <a href="/en/blog/''' + slug + '''.html">''' + en_title + '''</a>
        <div class="post-meta">June 19, 2026 &middot; 8 min read &middot; Guide</div>
        <div class="post-desc">''' + en_desc + '''</div>
      </li>
      '''

pt_new_entry = '''        <ul class="post-list">
      <li>
        <a href="/pt/blog/''' + slug + '''.html">''' + pt_title + '''</a>
        <div class="post-meta">19 de Junho, 2026 &middot; 8 min de leitura &middot; Guia</div>
        <div class="post-desc">''' + pt_desc + '''</div>
      </li>
      '''

id_new_entry = '''        <ul class="post-list">
      <li>
        <a href="/id/blog/''' + slug + '''.html">''' + id_title + '''</a>
        <div class="post-meta">19 Juni 2026 &middot; 8 mnt baca &middot; Panduan</div>
        <div class="post-desc">''' + id_desc + '''</div>
      </li>
      '''

# Update index files - insert after '<ul class="post-list">'
en_new_index = en_index.replace('<ul class="post-list">', en_new_entry, 1)
pt_new_index = pt_index.replace('<ul class="post-list">', pt_new_entry, 1)
id_new_index = id_index.replace('<ul class="post-list">', id_new_entry, 1)

open('en/blog/index.html', 'w').write(en_new_index)
print("Updated en/blog/index.html")
open('pt/blog/index.html', 'w').write(pt_new_index)
print("Updated pt/blog/index.html")
open('id/blog/index.html', 'w').write(id_new_index)
print("Updated id/blog/index.html")

# Update state.json - add 3 published entries
state = json.load(open('drafts/state.json'))
new_entries = [
    {
        "slug": slug, "date": date, "published_at": date,
        "type": "guide", "lang": "en",
        "file": f"en/blog/{slug}.html",
        "url": f"https://threadgrab.com/en/blog/{slug}.html",
        "title": en_title, "description": en_desc,
        "heat_source": "⭐ 2026-06-19 daily hot topics — Microsoft markitdown open-source launch (GitHub, June 2026)",
        "status": "published",
        "providers_featured": [], "primary_cta": "Try ThreadGrab"
    },
    {
        "slug": slug, "date": date, "published_at": date,
        "type": "guia", "lang": "pt",
        "file": f"pt/blog/{slug}.html",
        "url": f"https://threadgrab.com/pt/blog/{slug}.html",
        "title": pt_title, "description": pt_desc,
        "heat_source": "⭐ 2026-06-19 daily hot topics — Microsoft markitdown open-source launch",
        "status": "published",
        "providers_featured": [], "primary_cta": "Experimente ThreadGrab"
    },
    {
        "slug": slug, "date": date, "published_at": date,
        "type": "panduan", "lang": "id",
        "file": f"id/blog/{slug}.html",
        "url": f"https://threadgrab.com/id/blog/{slug}.html",
        "title": id_title, "description": id_desc,
        "heat_source": "⭐ 2026-06-19 daily hot topics — Microsoft markitdown open-source launch",
        "status": "published",
        "providers_featured": [], "primary_cta": "Coba ThreadGrab"
    }
]
state['published'].extend(new_entries)
state['recent_topics'].insert(0, slug)
state['last_run'] = 'publish-confirmed'
state['last_published_slug'] = slug
state['last_published_at'] = f"{date}T09:00:00+08:00"
json.dump(state, open('drafts/state.json', 'w'), indent=2, ensure_ascii=False)
print("Updated drafts/state.json")

print("\n=== BUILD SCRIPT COMPLETE ===")
print("Now need to write the 3 HTML article files separately.")
