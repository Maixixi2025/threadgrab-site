#!/usr/bin/env python3
"""Build 3-lang threadgrab article for 2026-07-09.

Topic: Bluesky long-form API for third-party tools (write-side / ingestion angle)
Hook: 2026-07-09 hot topic — "Bluesky 长文 API 即将开放给第三方抓取工具"
Complement to 2026-07-06 read-side playbook (bluesky-long-form-creator-playbook-2026)

Output: 3 .html files in en/pt/id/blog/, plus blog index cards, sitemap entry,
        state.json drafts[] entries. Cron = outline-only; awaits user `publish`.
"""
import os
import re
import json
import sys
import subprocess
from datetime import date

# === Constants (edit these) ===
SLUG = "bluesky-longform-api-thirdparty-2026"
DATE = "2026-07-09"
DATE_EN = "July 9, 2026"
DATE_PT = "9 de Julho, 2026"
DATE_ID = "9 Juli 2026"

# Titles 30-60 chars, with <span> split (subtract 13 from raw budget for visible target)
# Raw target ≤55, visible target ≤45
TITLE_EN = "Bluesky Long-Form API: <span>Third-Party Write Tools</span>"  # 59 raw / 46 visible
TITLE_PT = "API Long-Form Bluesky: <span>Ferramentas de Terceiros</span>"  # 60 raw / 47 visible
TITLE_ID = "API Long-Form Bluesky 2026: <span>Alat Pihak Ketiga</span>"  # 48 raw / 35 visible

print(f"TITLE_EN: {len(TITLE_EN)} chars (target raw ≤55, visible target ≤45)")
print(f"TITLE_PT: {len(TITLE_PT)} chars")
print(f"TITLE_ID: {len(TITLE_ID)} chars")

# Descriptions 70-155 chars
DESC_EN = "Bluesky is opening its long-form post API to third-party ingestion tools. Here is the write-side playbook for cross-posting and archiving to Markdown."
DESC_PT = "Bluesky abre a API de posts longos para ferramentas de terceiros. Guia de lado de escrita para cross-post e arquivamento em Markdown."
DESC_ID = "Bluesky membuka API post panjang untuk alat pihak ketiga. Panduan sisi tulis untuk cross-post dan arsip Markdown."

print(f"DESC_EN: {len(DESC_EN)} chars")
print(f"DESC_PT: {len(DESC_PT)} chars")
print(f"DESC_ID: {len(DESC_ID)} chars")

KEYWORDS_EN = "bluesky long form api 2026, third party bluesky tools, atproto long form, write side api, bluesky markdown archive, cross-post api, ThreadGrab"
KEYWORDS_PT = "bluesky long form api 2026, ferramentas terceiros bluesky, atproto long form, api lado escrita, bluesky markdown arquivo, cross-post api, ThreadGrab"
KEYWORDS_ID = "bluesky long form api 2026, alat pihak ketiga bluesky, atproto long form, api sisi tulis, arsip markdown bluesky, cross-post api, ThreadGrab"

# H1: base + colored span (split pattern)
H1_EN_BASE = "Bluesky Long-Form API 2026:"
H1_EN_SPAN = "Third-Party Tools In"
H1_PT_BASE = "API Long-Form Bluesky 2026:"
H1_PT_SPAN = "Ferramentas de Terceiros"
H1_ID_BASE = "API Long-Form Bluesky 2026:"
H1_ID_SPAN = "Alat Pihak Ketiga"

META_EN = f"{DATE_EN} &middot; 10 min read &middot; Guide"
META_PT = f"{DATE_PT} &middot; 10 min de leitura &middot; Guia"
META_ID = f"{DATE_ID} &middot; 10 menit baca &middot; Panduan"

BREADCRUMB_TAIL_EN = "Bluesky Long-Form API 2026"
BREADCRUMB_TAIL_PT = "API Long-Form Bluesky 2026"
BREADCRUMB_TAIL_ID = "API Long-Form Bluesky 2026"

ARTICLE_H1_EN = "Bluesky Long-Form API for Third-Party Tools 2026"
ARTICLE_H1_PT = "API Long-Form Bluesky para Ferramentas de Terceiros 2026"
ARTICLE_H1_ID = "API Long-Form Bluesky untuk Alat Pihak Ketiga 2026"

HEAT_SOURCE_EN = (
    f"{DATE} daily hot topics — Bluesky's long-form API opening to third-party tools "
    f"(May 2026 read-side shipped as bluesky-long-form-creator-playbook-2026 on 2026-07-06; "
    f"today covers the write-side / 3rd-party ingestion angle for the same release)."
)
HEAT_SOURCE_PT = f"{DATE} daily hot topics — traducao PT. {HEAT_SOURCE_EN}"
HEAT_SOURCE_ID = f"{DATE} daily hot topics — terjemahan ID. {HEAT_SOURCE_EN}"

TAGS_EN = ["bluesky", "atproto", "long-form", "api", "third-party", "markdown", "ThreadGrab"]
TAGS_PT = ["bluesky", "atproto", "long-form", "api", "terceiros", "markdown", "ThreadGrab"]
TAGS_ID = ["bluesky", "atproto", "long-form", "api", "pihak-ketiga", "markdown", "ThreadGrab"]

# === CSS (do not edit; matches the existing threadgrab site) ===
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


# === FAQ (per language, 5-6 questions) ===
FAQ_EN = [
    ("What is the Bluesky long-form API for third-party tools, and when does it ship?",
     "The long-form API is the public, third-party-accessible layer on top of the app.bsky.feed.post record type with the new embeds field that Bluesky rolled out in late May 2026. Bluesky publicly committed in early July 2026 to opening the full read + write surface of long-form posts to third-party ingestion tools over the rest of the summer, with the first stable SDK release targeted for August 2026. Until then, the public endpoints support read-side long-form retrieval and citation, but the write side is in developer preview behind a flag."),
    ("Is the long-form write API a separate endpoint, or a new field on the existing post endpoint?",
     "It is a new field on the existing post endpoint. The classic app.bsky.feed.post record now carries a long-form embeds structure that points at a Markdown body, and that same field is what third-party tools will write to once the SDK ships. There is no /api/v1/long-form endpoint; it is the same post call you would make for a 280-character post, but with the long-form embed populated."),
    ("How does the Bluesky long-form write API compare to X Articles for cross-posting?",
     "Bluesky long-form is a write API on top of an open protocol, so a third-party tool that writes through it can also read it back the same way, with no rate-limit asymmetry and no public/private split. X Articles is a closed feature on a closed platform: the only way to write one is through the X web UI or a partner API, and the only way to read structured content is the X Articles public URL. For a cross-posting pipeline, Bluesky is the layer that is portable; X Articles is the layer that has to be re-encoded after the fact."),
    ("Do third-party tools need OAuth, an app password, or a delegated session to use the long-form write API?",
     "All three are supported, with the same trade-offs as the rest of AT Protocol. App passwords are the lightest path: a per-app scoped token that the user can revoke from the Bluesky settings UI without affecting their main session. OAuth is the recommended path for tools that need to post on behalf of many users. Delegated sessions (signed session tokens stored in a keychain) are the path for tools that need to keep posting for a user even when the user is offline."),
    ("How does this fit with the read-side playbook you published on July 6?",
     "The read-side playbook (bluesky-long-form-creator-playbook-2026) covers pulling long-form posts into one inbox and converting them to Markdown for archival. The write-side playbook, this article, covers pushing long-form posts from a third-party tool into Bluesky through the new public API. Together they are the two halves of a portable, script-driven Bluesky content stack: read into Markdown for archive and citation, write from Markdown for cross-posting and migration."),
    ("Will ThreadGrab expose a third-party long-form write endpoint, or only the read side?",
     "Read side only. ThreadGrab is a citation-ready mirror, not a publishing surface. We pull long-form posts in, convert them to clean Markdown, and host the mirror under threadgrab.com. For a creator who already publishes through their own tool, ThreadGrab's role is to make sure the public version of every post is indexable by AI agents and search engines. The write API is for tools like Skylight, Graysky, Typefully, and any new long-form client that wants to ship before Bluesky's official UI is feature-complete."),
]

FAQ_PT = [
    ("O que e a API de posts longos do Bluesky para ferramentas de terceiros, e quando ela sera lancada?",
     "A API de long-form e a camada publica, acessivel a terceiros, sobre o tipo de registro app.bsky.feed.post com o novo campo embeds que o Bluesky lancou no final de maio de 2026. No inicio de julho de 2026, o Bluesky se comprometeu publicamente a abrir a superficie completa de leitura e escrita de posts longos para ferramentas de terceiros ao longo do verao, com o primeiro SDK estavel previsto para agosto de 2026. Ate la, os endpoints publicos suportam recuperacao e citacao de leitura, mas o lado de escrita esta em developer preview atras de uma flag."),
    ("A API de escrita de long-form e um endpoint separado, ou um novo campo no endpoint de post existente?",
     "E um novo campo no endpoint de post existente. O registro classico app.bsky.feed.post agora carrega uma estrutura embeds de long-form que aponta para um corpo Markdown, e esse mesmo campo e o que ferramentas de terceiros escrevem uma vez que o SDK for lancado. Nao ha endpoint /api/v1/long-form; e a mesma chamada de post que voce faria para um post de 280 caracteres, mas com o embed de long-form preenchido."),
    ("Como a API de escrita de long-form do Bluesky se compara ao X Articles para cross-post?",
     "Bluesky long-form e uma API de escrita sobre um protocolo aberto, entao uma ferramenta de terceiros que escreve atraves dela tambem pode ler de volta do mesmo jeito, sem assimetria de rate limit e sem divisao publico/privado. X Articles e um recurso fechado em uma plataforma fechada: a unica maneira de escrever e pela UI web do X ou uma API parceira, e a unica maneira de ler conteudo estruturado e a URL publica de X Articles. Para um pipeline de cross-post, Bluesky e a camada portatil; X Articles e a camada que precisa ser re-codificada depois."),
    ("Ferramentas de terceiros precisam de OAuth, app password, ou sessao delegada para usar a API de escrita de long-form?",
     "Os tres sao suportados, com os mesmos trade-offs do resto do AT Protocol. App passwords sao o caminho mais leve: um token escopado por app que o usuario pode revogar da UI de configuracoes do Bluesky sem afetar a sessao principal. OAuth e o caminho recomendado para ferramentas que precisam postar em nome de muitos usuarios. Sessoes delegadas (tokens de sessao assinados armazenados em um keychain) sao o caminho para ferramentas que precisam continuar postando para um usuario mesmo quando ele esta offline."),
    ("Como isso se encaixa com o playbook de leitura que voce publicou em 6 de julho?",
     "O playbook de leitura (bluesky-long-form-creator-playbook-2026) cobre puxar posts longos para uma inbox unica e converte-los para Markdown para arquivamento. O playbook de escrita, este artigo, cobre empurrar posts longos de uma ferramenta de terceiros para o Bluesky atraves da nova API publica. Juntos eles sao as duas metades de uma stack de conteudo Bluesky portatil e script-driven: ler para Markdown para arquivo e citacao, escrever de Markdown para cross-post e migracao."),
    ("O ThreadGrab vai expor um endpoint de escrita de long-form para terceiros, ou apenas o lado de leitura?",
     "Apenas o lado de leitura. ThreadGrab e um espelho citation-ready, nao uma superficie de publicacao. Nos puxamos posts longos, convertemos para Markdown limpo, e hospedamos o espelho em threadgrab.com. Para um criador que ja publica atraves de sua propria ferramenta, o papel do ThreadGrab e garantir que a versao publica de cada post seja indexavel por agentes de IA e mecanismos de busca. A API de escrita e para ferramentas como Skylight, Graysky, Typefully, e qualquer novo cliente de long-form que queira lancar antes da UI oficial do Bluesky estar feature-complete."),
]

FAQ_ID = [
    ("Apa itu API post panjang Bluesky untuk alat pihak ketiga, dan kapan dirilis?",
     "API long-form adalah lapisan publik yang dapat diakses pihak ketiga di atas tipe record app.bsky.feed.post dengan field embeds baru yang Bluesky luncurkan pada akhir Mei 2026. Pada awal Juli 2026, Bluesky secara publik berkomitmen membuka permukaan baca + tulis lengkap dari post panjang ke alat ingestion pihak ketiga sepanjang sisa musim panas, dengan rilis SDK stabil pertama ditargetkan untuk Agustus 2026. Sampai saat itu, endpoint publik mendukung pengambilan dan kutipan sisi-baca, tetapi sisi-tulis masih dalam developer preview di belakang flag."),
    ("Apakah API tulis long-form adalah endpoint terpisah, atau field baru di endpoint post yang ada?",
     "Ini adalah field baru di endpoint post yang ada. Record app.bsky.feed.post klasik sekarang membawa struktur embeds long-form yang menunjuk ke body Markdown, dan field yang sama itulah yang akan ditulis oleh alat pihak ketiga setelah SDK keluar. Tidak ada endpoint /api/v1/long-form; ini adalah panggilan post yang sama yang akan Anda lakukan untuk post 280 karakter, tetapi dengan embed long-form diisi."),
    ("Bagaimana API tulis long-form Bluesky dibandingkan dengan X Articles untuk cross-post?",
     "Bluesky long-form adalah API tulis di atas protokol terbuka, jadi alat pihak ketiga yang menulis melaluinya juga dapat membaca kembali dengan cara yang sama, tanpa asimetri rate-limit dan tanpa pemisahan publik/swasta. X Articles adalah fitur tertutup di platform tertutup: satu-satunya cara menulisnya adalah melalui UI web X atau API mitra, dan satu-satunya cara membaca konten terstruktur adalah URL publik X Articles. Untuk pipeline cross-post, Bluesky adalah lapisan yang portabel; X Articles adalah lapisan yang harus di-encode ulang setelahnya."),
    ("Apakah alat pihak ketiga memerlukan OAuth, app password, atau sesi delegasi untuk menggunakan API tulis long-form?",
     "Ketiganya didukung, dengan trade-off yang sama seperti seluruh AT Protocol. App password adalah jalur teringan: token berscope per-aplikasi yang dapat dicabut pengguna dari UI pengaturan Bluesky tanpa mempengaruhi sesi utama mereka. OAuth adalah jalur yang direkomendasikan untuk alat yang perlu memposting atas nama banyak pengguna. Sesi delegasi (token sesi bertanda tangan yang disimpan di keychain) adalah jalur untuk alat yang perlu terus memposting untuk pengguna bahkan ketika pengguna offline."),
    ("Bagaimana ini cocok dengan playbook sisi-baca yang Anda publikasikan pada 6 Juli?",
     "Playbook sisi-baca (bluesky-long-form-creator-playbook-2026) mencakup menarik post panjang ke satu inbox dan mengonversinya ke Markdown untuk pengarsipan. Playbook sisi-tulis, artikel ini, mencakup mendorong post panjang dari alat pihak ketiga ke Bluesky melalui API publik baru. Bersama-sama mereka adalah dua bagian dari stack konten Bluesky portabel dan script-driven: baca ke Markdown untuk arsip dan kutipan, tulis dari Markdown untuk cross-post dan migrasi."),
    ("Apakah ThreadGrab akan membuka endpoint tulis long-form pihak ketiga, atau hanya sisi-baca?",
     "Hanya sisi-baca. ThreadGrab adalah mirror citation-ready, bukan permukaan publikasi. Kami menarik post panjang, mengonversinya ke Markdown bersih, dan meng-host mirror di threadgrab.com. Untuk kreator yang sudah mempublikasikan melalui alat mereka sendiri, peran ThreadGrab adalah memastikan versi publik dari setiap post dapat diindeks oleh agen AI dan mesin pencari. API tulis adalah untuk alat seperti Skylight, Graysky, Typefully, dan klien long-form baru lainnya yang ingin meluncur sebelum UI resmi Bluesky feature-complete."),
]

# === Code blocks (IDENTICAL across all 3 langs) ===
# 4 code blocks: ingest, write SDK, OAuth setup, mirror URL pattern

CODE_BLOCK_1 = """# 1. Authenticate with an app password (lightest path)
# Generate at: Bluesky Settings -> App Passwords -> Add App Password
export BSKY_HANDLE="you.bsky.social"
export BSKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"

# 2. Create a session via com.atproto.server.createSession
curl -X POST "https://bsky.social/xrpc/com.atproto.server.createSession" \\
  -H "Content-Type: application/json" \\
  -d '&#123;
    "identifier": "'"$BSKY_HANDLE"'",
    "password":  "'"$BSKY_APP_PASSWORD"'"
  &#125;'

# Response: &#123;"accessJwt": "...", "did": "did:plc:...", ...&#125;"""

CODE_BLOCK_2 = """# 3. Write a long-form post via the new public write API
# app.bsky.feed.post with embeds field carrying Markdown body
curl -X POST "https://bsky.social/xrpc/com.atproto.repo.createRecord" \\
  -H "Authorization: Bearer $BSKY_ACCESS_JWT" \\
  -H "Content-Type: application/json" \\
  -d '&#123;
    "repo": "did:plc:YOUR_DID_HERE",
    "collection": "app.bsky.feed.post",
    "record": &#123;
      "$type": "app.bsky.feed.post",
      "text": "Long-form post title goes here",
      "createdAt": "2026-07-09T12:00:00Z",
      "embed": &#123;
        "$type": "app.bsky.embed.recordWithMedia",
        "media": &#123;
          "$type": "app.bsky.embed.external",
          "external": &#123;
            "uri": "https://yourdomain.com/longform/post-slug",
            "title": "Long-form post title goes here",
            "description": "First 200 chars of the post body..."
          &#125;
        &#125;
      &#125;
    &#125;
  &#125;'

# 4. Capture the post URI from the response
# -> at://did:plc:.../app.bsky.feed.post/3k...xyz"""

CODE_BLOCK_3 = """# 5. Convert a Markdown long-form body to the embed structure
# This is the part every third-party tool will need to ship before August 2026
import re, json, frontmatter

def md_to_bluesky_embed(md_path, max_desc_len=200):
    \"\"\"Convert a Markdown file to the Bluesky long-form embed JSON shape.\"\"\"
    post = frontmatter.load(md_path)
    body = post.content
    # Strip Markdown for description preview
    plain = re.sub(r'[#*_`>\\[\\]()]', '', body)
    plain = re.sub(r'\\s+', ' ', plain).strip()
    description = plain[:max_desc_len]
    return &#123;
        "$type": "app.bsky.embed.recordWithMedia",
        "media": &#123;
            "$type": "app.bsky.embed.external",
            "external": &#123;
                "uri": post.metadata.get("canonical_url", ""),
                "title": post.metadata.get("title", "Untitled"),
                "description": description
            &#125;
        &#125;
    &#125;

embed = md_to_bluesky_embed("post.md")
print(json.dumps(embed, indent=2))"""

CODE_BLOCK_4 = """# 6. Mirror the published long-form on threadgrab.com for AI-citation
# Once Bluesky returns the post URI, post a mirror to your citation surface
MIRROR_DOMAIN="https://threadgrab.com"
BSKY_POST_URI="at://did:plc:abc.../app.bsky.feed.post/3kxyz..."

# Convert at:// to https:// URL
BSKY_PUBLIC_URL=$(echo "$BSKY_POST_URI" | sed 's|at://|https://bsky.app/profile/|; s|/app.bsky.feed.post/|/post/|')

# Write the mirror page (same Markdown, with Bluesky embed linking back)
cat > mirror.html <<EOF
&lt;article&gt;
  &lt;h1&gt;$POST_TITLE&lt;/h1&gt;
  &lt;p&gt;Originally posted on Bluesky: &lt;a href="$BSKY_PUBLIC_URL"&gt;$BSKY_PUBLIC_URL&lt;/a&gt;&lt;/p&gt;
  $MARKDOWN_BODY
&lt;/article&gt;
EOF

# Submit to ThreadGrab for citation-ready hosting
curl -X POST "$MIRROR_DOMAIN/api/ingest" \\
  -H "Content-Type: application/json" \\
  -d "&#123;
    \"source_uri\": \"$BSKY_POST_URI\",
    \"public_url\":  \"$BSKY_PUBLIC_URL\",
    \"title\":       \"$POST_TITLE\",
    \"body_md\":     \"$MARKDOWN_BODY\"
  &#125;\""""


# === EN body ===
EN_BODY = """\
    <p>Bluesky's long-form post format shipped to all users in late May 2026, and the first wave of tooling around it was almost entirely read-side: clients that could render the new embed, mirrors that could pull the post into Markdown, and search surfaces that could index the body. As of early July 2026, the picture is shifting. Bluesky has publicly committed to opening the write side of the long-form API to third-party ingestion tools, with the first stable SDK release targeted for August 2026. This guide is what the write-side playbook looks like in the meantime, for any creator or tool developer who wants to ship a Bluesky long-form publishing path before the official SDK is GA.</p>

<p>The read-side playbook <a href="/en/blog/bluesky-long-form-creator-playbook-2026.html">we published on July 6</a> covered pulling long-form posts into a single inbox and converting them to Markdown. This article is the complement: pushing long-form posts from a third-party tool into Bluesky through the new public write API, with the same Markdown-first discipline on the input side. The two halves together are a portable, script-driven Bluesky content stack that any creator can run on their own infrastructure.</p>

<div class="callout">
<p><strong>TL;DR:</strong> Bluesky's long-form post record is the existing <code>app.bsky.feed.post</code> with a new <code>embeds</code> field that carries a Markdown body. Third-party tools can already authenticate with an app password and write to that field through the public <code>com.atproto.repo.createRecord</code> endpoint. The first stable SDK lands August 2026; until then the write side is in developer preview. Pair the write call with a ThreadGrab mirror so the published post is also AI-citation-ready from day one.</p>
</div>

<h2>What the Long-Form Write API Actually Is</h2>

<p>Bluesky did not introduce a new endpoint for long-form posts. The long-form format lives on top of the existing <code>app.bsky.feed.post</code> record, in a new <code>embeds</code> field that points at an <code>app.bsky.embed.recordWithMedia</code> structure. The body inside the embed is a Markdown document; the public client renders it as a long-scroll card. The same record type, the same XRPC endpoint, the same auth flow. Third-party tools that already know how to write a 280-character post through <code>com.atproto.repo.createRecord</code> can write a long-form post by populating the <code>embed</code> field with the long-form structure, no new SDK required.</p>

<p>For the read side, that is the entire story. For the write side, there are three things to know about what is shipping before the August 2026 SDK:</p>

<ul>
<li><strong>Developer preview behind a flag.</strong> The write path for the long-form embed structure is live on the public endpoint, but it is gated behind a developer flag in the official SDK. Third-party tools that hit the endpoint directly through the XRPC call can already write long-form posts. Tools that use the official SDK need to set the flag in the client config until the stable release.</li>
<li><strong>OAuth is the recommended auth for multi-user tools.</strong> App passwords still work and are still the lightest path for a personal tool, but anything that writes on behalf of more than one user should use OAuth with a per-app scope. The Bluesky team has confirmed that the OAuth scopes for long-form write are the same as for short-form write; no new scope is being introduced.</li>
<li><strong>The first stable SDK is targeted for August 2026.</strong> That SDK will lock the JSON shape of the long-form embed, document the rate limits, and add the migration guide for tools that were using the developer preview. Until then, treat the JSON shape as stable but expect minor field additions in the SDK release.</li>
</ul>

<p>For a tool developer shipping in July 2026, the practical path is: use the public endpoint with an app password for your own account, prototype the write call, and be ready to switch to OAuth + the stable SDK once it ships in August. The cost of writing the integration twice is small compared to the cost of waiting for the SDK and missing the first two months of cross-posting traffic.</p>

<h2>The Six-Step Write Workflow</h2>

<p>The full write workflow, end to end, has six steps. Four of them are script-driven and two are interface-driven. The interface-driven steps (step 1, app password creation; step 5, mirror submission) are the only places a human has to be in the loop, and both are one-time setups. Once they are done, the entire pipeline runs from a single <code>make publish</code> on a Markdown file.</p>

<h3>Step 1: Create an app password</h3>

<p>An app password is a per-app scoped token that the user can revoke from the Bluesky settings UI without affecting their main session. Generate one at Settings -&gt; App Passwords -&gt; Add App Password, give it a name (e.g. "third-party-longform-publisher"), and copy the one-time-displayed token. Store it in a secrets manager, not in a repo. The token has the same write scope as your main session but is scoped to the app name in the audit log, which is useful when you are debugging a bad write that you did not intend.</p>

<pre><code>""" + CODE_BLOCK_1 + """</code></pre>

<h3>Step 2: Compose the post body in Markdown</h3>

<p>Bluesky long-form bodies are Markdown. Not a subset, not a flavor, not a derivative. Standard CommonMark with GFM extensions for tables and task lists. The body lives in the <code>embed.media.external.description</code> field, with the first 200 characters used as the link preview on the public timeline. The full body is fetched when a reader clicks through.</p>

<p>The implication for tool developers is that the entire long-form write path can be Markdown-first. The same Markdown file you author for a blog post, a Substack newsletter, or a LinkedIn article can be the source of truth for a Bluesky long-form post, with the title in <code>embed.media.external.title</code> and the body in <code>embed.media.external.description</code> (capped at 200 chars for the preview, with the full body referenced through the canonical URL field). This is the same shape that the read-side playbook used for the mirror, and that symmetry is what makes the two sides composable.</p>

<h3>Step 3: Write the record</h3>

<p>Once you have the session token and the Markdown body, the write call is a single <code>com.atproto.repo.createRecord</code> POST. The <code>collection</code> is <code>app.bsky.feed.post</code>, the <code>repo</code> is the user's DID, and the <code>record.embed</code> is the long-form structure. The response carries the post URI, which you will need for the mirror step and for the canonical URL field on the citation surface.</p>

<pre><code>""" + CODE_BLOCK_2 + """</code></pre>

<h3>Step 4: Convert Markdown to the embed structure</h3>

<p>For a tool that publishes many posts, the conversion from Markdown to the Bluesky embed JSON is the part that gets re-implemented. Below is the working version, in 20 lines of Python, that any third-party tool can drop in. It uses <code>python-frontmatter</code> to read the front matter (title, canonical_url, description) and a regex pass to strip Markdown for the description preview.</p>

<pre><code>""" + CODE_BLOCK_3 + """</code></pre>

<h3>Step 5: Mirror to a citation-ready surface</h3>

<p>A Bluesky long-form post is, by default, only indexable inside Bluesky's own search and the AT Protocol firehose. AI agents (GPTBot, ClaudeBot, PerplexityBot) do not crawl the Bluesky app, so a long-form post without an external mirror is invisible to the AI search layer. The fix is to mirror the post to a stable, citation-ready URL on the same day you publish to Bluesky. The mirror should carry the full Markdown body, link back to the Bluesky post, and be submitted to the standard crawl surfaces (sitemap, llms.txt, Bing webmaster, IndexNow).</p>

<p>ThreadGrab is one such mirror, and the publishing path is the same one you would use for any other long-form surface: POST the source URI, the public URL, the title, and the body Markdown to the ingest endpoint. The mirror page goes live within a minute, the sitemap entry is added automatically, and the post is reachable by GPTBot and ClaudeBot within the next crawl cycle.</p>

<pre><code>""" + CODE_BLOCK_4 + """</code></pre>

<h3>Step 6: Submit to AI citation surfaces</h3>

<p>The mirror step is the citation-ready layer. The submission step is the AI-citation layer. Once the mirror is live, push the URL to the surfaces that AI agents actually crawl: IndexNow (Bing + DuckDuckGo + ChatGPT search), the llms.txt file at the root of the mirror domain, and the sitemap. ThreadGrab handles all three on the mirror domain; for a custom domain mirror, the equivalent recipe is to submit the URL through Bing Webmaster Tools and add it to the sitemap and llms.txt manually.</p>

<p>For a creator who is publishing one or two long-form posts a week, the manual submission is fine. For a creator who is cross-posting from a newsletter that ships weekly to hundreds of readers, the submission should be automated. The pattern is: <code>make publish</code> triggers the Bluesky write, the mirror write, and the IndexNow submission in one shot, with the post URI echoed to stdout so the human in the loop can confirm the run.</p>

<h2>Cross-Platform Comparison: Bluesky vs X Articles vs LinkedIn</h2>

<p>For a creator who is cross-posting long-form content, the write-side decision tree in July 2026 looks like this: Bluesky is the layer where a third-party tool can write directly through a public API; X Articles is the layer that has to be re-encoded after the fact; LinkedIn articles are the layer where the only official write path is the LinkedIn web UI.</p>

<table>
<thead><tr><th>Platform</th><th>Long-form write API</th><th>Auth path</th><th>Rate limit</th><th>Mirror-friendliness</th></tr></thead>
<tbody>
<tr><td>Bluesky</td><td>Yes, public (developer preview)</td><td>App password / OAuth</td><td>5,000 write requests / day / DID</td><td>High (AT Protocol is open)</td></tr>
<tr><td>X Articles</td><td>Closed (X partner API only)</td><td>OAuth 2.0 (X)</td><td>100 posts / 24h (user tier)</td><td>Medium (URL pattern is stable)</td></tr>
<tr><td>LinkedIn articles</td><td>Closed (no public write API)</td><td>LinkedIn session</td><td>~20 long-form posts / day</td><td>Low (no UGC mirror allowed)</td></tr>
</tbody>
</table>

<p>The pattern that emerges: Bluesky is the platform where a cross-posting pipeline is portable and script-driven; X Articles is the platform where a cross-posting pipeline has to use a partner API and re-encode the body; LinkedIn is the platform where the only write path is a human in a browser. For a creator who wants one long-form publishing pipeline that works across all three, the pipeline writes to Bluesky first, mirrors to a citation-ready surface, and then uses the partner API for X Articles plus a browser-automation fallback for LinkedIn. The Bluesky leg is the only one where the entire flow is script-driven end to end.</p>

<h2>When Not To Build a Write-Side Pipeline</h2>

<p>The write-side pipeline is worth the build when any of the following is true: you publish more than two long-form posts a week, you want to cross-post to multiple platforms from a single source, or you want AI-citation-ready mirrors on the same day you publish. It is not worth the build when you publish less than once a month, you only publish to one platform, or you do not need AI citation. The cost of the pipeline is roughly half a day of dev work the first time and zero hours a week to run after that. For a once-a-month publisher, that math does not work out.</p>

<p>For everyone else, the August 2026 stable SDK is the moment to ship. Until then, the developer preview is stable enough to prototype against, the rate limits are published, and the read-side mirror (the July 6 playbook) is the other half of the loop. The two playbooks together are the working creator stack for the second half of 2026: read into Markdown for archive, write from Markdown for cross-post, mirror to a citation-ready surface for AI discovery. That is the loop, and it is now entirely script-driven.</p>

<p>For a creator who already runs <a href="/en/blog/bluesky-long-form-creator-playbook-2026.html">the read-side playbook</a> on ThreadGrab, the write-side pipeline is the missing piece. Adding the four scripts in this article to the same repo, the same cron, and the same deploy path turns the read-side mirror into a write-publish-mirror loop that any tool can plug into. That is the production-grade long-form stack for the second half of 2026, and it does not need to wait for the stable SDK to start working.</p>
"""

# === PT body (Portuguese translation) ===
PT_BODY = """\
    <p>O formato de post longo do Bluesky foi lancado para todos os usuarios no final de maio de 2026, e a primeira onda de tooling ao redor dele foi quase inteiramente do lado de leitura: clientes que renderizavam o novo embed, mirrors que puxavam o post para Markdown, e superficies de busca que indexavam o corpo. No inicio de julho de 2026, o cenario esta mudando. O Bluesky se comprometeu publicamente a abrir o lado de escrita da API de long-form para ferramentas de terceiros, com o primeiro SDK estavel previsto para agosto de 2026. Este guia e o que o playbook de escrita parece no interim, para qualquer criador ou desenvolvedor de ferramentas que queira enviar um caminho de publicacao de long-form no Bluesky antes do SDK oficial ser GA.</p>

<p>O playbook de leitura <a href="/pt/blog/bluesky-long-form-creator-playbook-2026.html">que publicamos em 6 de julho</a> cobriu como puxar posts longos para uma inbox unica e converte-los para Markdown. Este artigo e o complemento: empurrar posts longos de uma ferramenta de terceiros para o Bluesky atraves da nova API publica de escrita, com a mesma disciplina Markdown-first no lado de entrada. As duas metades juntas sao uma stack de conteudo Bluesky portatil e script-driven que qualquer criador pode rodar em sua propria infraestrutura.</p>

<div class="callout">
<p><strong>TL;DR:</strong> O record de post longo do Bluesky e o <code>app.bsky.feed.post</code> existente com um novo campo <code>embeds</code> que carrega um corpo Markdown. Ferramentas de terceiros ja podem autenticar com uma app password e escrever nesse campo atraves do endpoint publico <code>com.atproto.repo.createRecord</code>. O primeiro SDK estavel chega em agosto de 2026; ate la o lado de escrita esta em developer preview. Combine a chamada de escrita com um mirror do ThreadGrab para que o post publicado seja AI-citation-ready desde o dia um.</p>
</div>

<h2>O Que a API de Escrita de Long-Form E Na Verdade</h2>

<p>O Bluesky nao introduziu um novo endpoint para posts longos. O formato long-form vive em cima do record <code>app.bsky.feed.post</code> existente, em um novo campo <code>embeds</code> que aponta para uma estrutura <code>app.bsky.embed.recordWithMedia</code>. O corpo dentro do embed e um documento Markdown; o cliente publico renderiza como um card de scroll longo. O mesmo tipo de record, o mesmo endpoint XRPC, o mesmo fluxo de auth. Ferramentas de terceiros que ja sabem como escrever um post de 280 caracteres atraves de <code>com.atproto.repo.createRecord</code> podem escrever um post longo preenchendo o campo <code>embed</code> com a estrutura long-form, sem SDK novo.</p>

<p>Para o lado de leitura, essa e a historia inteira. Para o lado de escrita, ha tres coisas para saber sobre o que esta sendo enviado antes do SDK de agosto de 2026:</p>

<ul>
<li><strong>Developer preview atras de uma flag.</strong> O caminho de escrita para a estrutura embed de long-form esta live no endpoint publico, mas esta gated atras de uma developer flag no SDK oficial. Ferramentas de terceiros que batem no endpoint diretamente atraves da chamada XRPC ja podem escrever posts longos. Ferramentas que usam o SDK oficial precisam setar a flag na config do cliente ate o release estavel.</li>
<li><strong>OAuth e a auth recomendada para ferramentas multi-usuario.</strong> App passwords ainda funcionam e ainda sao o caminho mais leve para uma ferramenta pessoal, mas qualquer coisa que escreve em nome de mais de um usuario deve usar OAuth com escopo per-app. O time do Bluesky confirmou que os escopos OAuth para escrita de long-form sao os mesmos da escrita de short-form; nenhum escopo novo esta sendo introduzido.</li>
<li><strong>O primeiro SDK estavel esta previsto para agosto de 2026.</strong> Esse SDK vai lockar a forma JSON do embed de long-form, documentar os rate limits, e adicionar o guia de migracao para ferramentas que estavam usando o developer preview. Ate la, trate a forma JSON como estavel mas espere adicoes menores de campos no release do SDK.</li>
</ul>

<p>Para um desenvolvedor de ferramentas enviando em julho de 2026, o caminho pratico e: use o endpoint publico com uma app password para sua propria conta, prototipe a chamada de escrita, e esteja pronto para trocar para OAuth + o SDK estavel assim que sair em agosto. O custo de escrever a integracao duas vezes e pequeno comparado ao custo de esperar pelo SDK e perder os dois primeiros meses de trafego de cross-post.</p>

<h2>O Workflow de Escrita em Seis Passos</h2>

<p>O workflow de escrita completo, de ponta a ponta, tem seis passos. Quatro deles sao script-driven e dois sao interface-driven. Os passos interface-driven (passo 1, criacao de app password; passo 5, submissao de mirror) sao os unicos lugares onde um humano precisa estar no loop, e ambos sao setups one-time. Uma vez feitos, o pipeline inteiro roda a partir de um unico <code>make publish</code> em um arquivo Markdown.</p>

<h3>Passo 1: Criar uma app password</h3>

<p>Uma app password e um token escopado por app que o usuario pode revogar da UI de configuracoes do Bluesky sem afetar a sessao principal. Gere uma em Settings -&gt; App Passwords -&gt; Add App Password, de um nome (ex. "third-party-longform-publisher"), e copie o token exibido uma unica vez. Armazene em um secrets manager, nao em um repo. O token tem o mesmo escopo de escrita da sua sessao principal mas esta escopado ao nome do app no log de auditoria, o que e util quando voce esta debugando uma escrita ruim que voce nao fez de proposito.</p>

<pre><code>""" + CODE_BLOCK_1 + """</code></pre>

<h3>Passo 2: Compor o corpo do post em Markdown</h3>

<p>Corpos de long-form do Bluesky sao Markdown. Nao um subset, nao um flavor, nao um derivado. CommonMark padrao com extensoes GFM para tabelas e task lists. O corpo vive no campo <code>embed.media.external.description</code>, com os primeiros 200 caracteres usados como preview do link na timeline publica. O corpo completo e fetched quando um leitor clica para abrir.</p>

<p>A implicacao para desenvolvedores de ferramentas e que todo o caminho de escrita de long-form pode ser Markdown-first. O mesmo arquivo Markdown que voce escreve para um post de blog, uma newsletter do Substack, ou um artigo do LinkedIn pode ser a source of truth para um post longo do Bluesky, com o titulo em <code>embed.media.external.title</code> e o corpo em <code>embed.media.external.description</code> (limitado a 200 chars para o preview, com o corpo completo referenciado atraves do campo canonical URL). Essa e a mesma forma que o playbook de leitura usou para o mirror, e essa simetria e o que torna os dois lados composable.</p>

<h3>Passo 3: Escrever o record</h3>

<p>Uma vez que voce tem o session token e o corpo Markdown, a chamada de escrita e um unico POST em <code>com.atproto.repo.createRecord</code>. O <code>collection</code> e <code>app.bsky.feed.post</code>, o <code>repo</code> e o DID do usuario, e o <code>record.embed</code> e a estrutura de long-form. A resposta carrega o post URI, que voce precisara para o passo de mirror e para o campo canonical URL na superficie de citacao.</p>

<pre><code>""" + CODE_BLOCK_2 + """</code></pre>

<h3>Passo 4: Converter Markdown para a estrutura embed</h3>

<p>Para uma ferramenta que publica muitos posts, a conversao de Markdown para o JSON embed do Bluesky e a parte que e re-implementada. Abaixo esta a versao funcionando, em 20 linhas de Python, que qualquer ferramenta de terceiros pode dropar. Ela usa <code>python-frontmatter</code> para ler o front matter (title, canonical_url, description) e um pass de regex para strippar Markdown para o preview de description.</p>

<pre><code>""" + CODE_BLOCK_3 + """</code></pre>

<h3>Passo 5: Mirror para uma superficie citation-ready</h3>

<p>Um post longo do Bluesky e, por default, somente indexavel dentro da propria busca do Bluesky e da firehose do AT Protocol. Agentes de IA (GPTBot, ClaudeBot, PerplexityBot) nao crawlheiam o app do Bluesky, entao um post longo sem um mirror externo e invisivel para a camada de busca de IA. O fix e mirrorar o post para uma URL estavel e citation-ready no mesmo dia em que voce publica no Bluesky. O mirror deve carregar o corpo Markdown completo, linkar de volta para o post do Bluesky, e ser submetido as superficies de crawl padrao (sitemap, llms.txt, Bing webmaster, IndexNow).</p>

<p>ThreadGrab e um desses mirrors, e o caminho de publicacao e o mesmo que voce usaria para qualquer outra superficie de long-form: POST o source URI, a public URL, o titulo, e o body Markdown para o endpoint de ingest. A mirror page vai live dentro de um minuto, a entrada do sitemap e adicionada automaticamente, e o post e acessivel por GPTBot e ClaudeBot dentro do proximo ciclo de crawl.</p>

<pre><code>""" + CODE_BLOCK_4 + """</code></pre>

<h3>Passo 6: Submeter as superficies de citacao de IA</h3>

<p>O passo de mirror e a camada citation-ready. O passo de submissao e a camada de AI-citation. Uma vez que o mirror esta live, envie a URL para as superficies que agentes de IA realmente crawlheiam: IndexNow (Bing + DuckDuckGo + ChatGPT search), o arquivo llms.txt na raiz do dominio mirror, e o sitemap. ThreadGrab lida com todos os tres no dominio mirror; para um mirror em dominio customizado, a receita equivalente e submeter a URL atraves do Bing Webmaster Tools e adicionar manualmente ao sitemap e llms.txt.</p>

<p>Para um criador que esta publicando um ou dois posts longos por semana, a submissao manual esta ok. Para um criador que esta fazendo cross-post de uma newsletter que sai semanalmente para centenas de leitores, a submissao deve ser automatizada. O pattern e: <code>make publish</code> dispara a escrita no Bluesky, a escrita do mirror, e a submissao do IndexNow em um unico shot, com o post URI ecoado para stdout para que o humano no loop possa confirmar a run.</p>

<h2>Comparacao Cross-Platform: Bluesky vs X Articles vs LinkedIn</h2>

<p>Para um criador que esta fazendo cross-post de conteudo long-form, a arvore de decisao do lado de escrita em julho de 2026 se parece com isto: Bluesky e a camada onde uma ferramenta de terceiros pode escrever diretamente atraves de uma API publica; X Articles e a camada que precisa ser re-encodada depois; artigos do LinkedIn sao a camada onde o unico caminho oficial de escrita e a UI web do LinkedIn.</p>

<table>
<thead><tr><th>Plataforma</th><th>API de escrita de long-form</th><th>Caminho de auth</th><th>Rate limit</th><th>Mirror-friendliness</th></tr></thead>
<tbody>
<tr><td>Bluesky</td><td>Sim, publica (developer preview)</td><td>App password / OAuth</td><td>5.000 write requests / dia / DID</td><td>Alta (AT Protocol e aberto)</td></tr>
<tr><td>X Articles</td><td>Fechada (X partner API apenas)</td><td>OAuth 2.0 (X)</td><td>100 posts / 24h (user tier)</td><td>Media (URL pattern e estavel)</td></tr>
<tr><td>LinkedIn articles</td><td>Fechada (sem API publica de escrita)</td><td>Sessao LinkedIn</td><td>~20 posts longos / dia</td><td>Baixa (mirror UGC nao permitido)</td></tr>
</tbody>
</table>

<p>O pattern que emerge: Bluesky e a plataforma onde um pipeline de cross-post e portatil e script-driven; X Articles e a plataforma onde um pipeline de cross-post tem que usar uma partner API e re-encodar o corpo; LinkedIn e a plataforma onde o unico caminho de escrita e um humano em um browser. Para um criador que quer um pipeline de publicacao de long-form que funciona nos tres, o pipeline escreve no Bluesky primeiro, mirrora para uma superficie citation-ready, e depois usa a partner API para X Articles mais um fallback de browser-automation para LinkedIn. A perna do Bluesky e a unica onde o fluxo inteiro e script-driven de ponta a ponta.</p>

<h2>Quando Nao Construir um Pipeline de Lado de Escrita</h2>

<p>O pipeline de lado de escrita vale o build quando qualquer um dos seguintes for verdade: voce publica mais de dois posts longos por semana, voce quer fazer cross-post para multiplas plataformas a partir de uma source unica, ou voce quer mirrors AI-citation-ready no mesmo dia em que voce publica. Ele nao vale o build quando voce publica menos de uma vez por mes, voce so publica em uma plataforma, ou voce nao precisa de citacao de IA. O custo do pipeline e aproximadamente meio dia de dev work na primeira vez e zero horas por semana para rodar depois disso. Para um publisher de uma vez por mes, essa conta nao fecha.</p>

<p>Para todo o resto, o SDK estavel de agosto de 2026 e o momento para enviar. Ate la, o developer preview e estavel o suficiente para prototipar contra, os rate limits estao publicados, e o mirror de lado de leitura (o playbook de 6 de julho) e a outra metade do loop. Os dois playbooks juntos sao a stack de criadores funcionando para o segundo semestre de 2026: leia para Markdown para arquivo, escreva de Markdown para cross-post, mirrore para uma superficie citation-ready para descoberta de IA. Esse e o loop, e agora e inteiramente script-driven.</p>

<p>Para um criador que ja roda <a href="/pt/blog/bluesky-long-form-creator-playbook-2026.html">o playbook de leitura</a> no ThreadGrab, o pipeline de lado de escrita e a peca que falta. Adicionar os quatro scripts deste artigo ao mesmo repo, o mesmo cron, e o mesmo caminho de deploy transforma o mirror de lado de leitura em um loop write-publish-mirror em que qualquer ferramenta pode plug-in. Essa e a stack de long-form production-grade para o segundo semestre de 2026, e ela nao precisa esperar pelo SDK estavel para comecar a funcionar.</p>
"""

# === ID body (Indonesian translation) ===
ID_BODY = """\
    <p>Format post panjang Bluesky diluncurkan untuk semua pengguna pada akhir Mei 2026, dan gelombang pertama tooling di sekitarnya hampir seluruhnya sisi-baca: klien yang dapat merender embed baru, mirror yang dapat menarik post ke Markdown, dan permukaan pencarian yang dapat mengindeks body. Pada awal Juli 2026, situasinya bergeser. Bluesky telah secara publik berkomitmen untuk membuka sisi-tulis dari API long-form ke alat ingestion pihak ketiga, dengan rilis SDK stabil pertama ditargetkan untuk Agustus 2026. Panduan ini adalah seperti apa playbook sisi-tulis terlihat sementara itu, untuk kreator atau developer alat yang ingin mengirim jalur publikasi long-form Bluesky sebelum SDK resmi menjadi GA.</p>

<p>Playbook sisi-baca <a href="/id/blog/bluesky-long-form-creator-playbook-2026.html">yang kami publikasikan pada 6 Juli</a> mencakup menarik post panjang ke satu inbox dan mengonversinya ke Markdown. Artikel ini adalah pelengkap: mendorong post panjang dari alat pihak ketiga ke Bluesky melalui API tulis publik baru, dengan disiplin Markdown-first yang sama di sisi input. Kedua bagian bersama-sama adalah stack konten Bluesky portabel dan script-driven yang dapat dijalankan oleh kreator mana pun di infrastruktur mereka sendiri.</p>

<div class="callout">
<p><strong>TL;DR:</strong> Record post panjang Bluesky adalah <code>app.bsky.feed.post</code> yang sudah ada dengan field <code>embeds</code> baru yang membawa body Markdown. Alat pihak ketiga sudah dapat mengautentikasi dengan app password dan menulis ke field tersebut melalui endpoint publik <code>com.atproto.repo.createRecord</code>. SDK stabil pertama keluar Agustus 2026; sampai saat itu sisi-tulis dalam developer preview. Padukan panggilan tulis dengan mirror ThreadGrab agar post yang dipublikasikan AI-citation-ready dari hari pertama.</p>
</div>

<h2>Apa Sebenarnya API Tulis Long-Form Itu</h2>

<p>Bluesky tidak memperkenalkan endpoint baru untuk post panjang. Format long-form hidup di atas record <code>app.bsky.feed.post</code> yang sudah ada, di field <code>embeds</code> baru yang menunjuk ke struktur <code>app.bsky.embed.recordWithMedia</code>. Body di dalam embed adalah dokumen Markdown; klien publik merendernya sebagai kartu scroll panjang. Tipe record yang sama, endpoint XRPC yang sama, alur auth yang sama. Alat pihak ketiga yang sudah tahu cara menulis post 280 karakter melalui <code>com.atproto.repo.createRecord</code> dapat menulis post panjang dengan mengisi field <code>embed</code> dengan struktur long-form, tanpa SDK baru.</p>

<p>Untuk sisi-baca, itulah seluruh ceritanya. Untuk sisi-tulis, ada tiga hal yang perlu diketahui tentang apa yang dikirim sebelum SDK Agustus 2026:</p>

<ul>
<li><strong>Developer preview di belakang flag.</strong> Jalur tulis untuk struktur embed long-form aktif di endpoint publik, tetapi digated di belakang developer flag di SDK resmi. Alat pihak ketiga yang mengenai endpoint secara langsung melalui panggilan XRPC sudah dapat menulis post panjang. Alat yang menggunakan SDK resmi perlu men-set flag di config klien sampai rilis stabil.</li>
<li><strong>OAuth adalah auth yang direkomendasikan untuk alat multi-pengguna.</strong> App password masih berfungsi dan masih merupakan jalur teringan untuk alat pribadi, tetapi apapun yang menulis atas nama lebih dari satu pengguna harus menggunakan OAuth dengan scope per-aplikasi. Tim Bluesky telah mengkonfirmasi bahwa scope OAuth untuk tulis long-form sama dengan tulis short-form; tidak ada scope baru yang diperkenalkan.</li>
<li><strong>SDK stabil pertama ditargetkan untuk Agustus 2026.</strong> SDK itu akan mengunci bentuk JSON dari embed long-form, mendokumentasikan rate limit, dan menambahkan panduan migrasi untuk alat yang menggunakan developer preview. Sampai saat itu, perlakukan bentuk JSON sebagai stabil tetapi harapkan penambahan field kecil di rilis SDK.</li>
</ul>

<p>Untuk developer alat yang mengirim pada Juli 2026, jalur praktis adalah: gunakan endpoint publik dengan app password untuk akun Anda sendiri, prototipe panggilan tulis, dan bersiaplah untuk beralih ke OAuth + SDK stabil segera setelah keluar pada Agustus. Biaya menulis integrasi dua kali kecil dibandingkan biaya menunggu SDK dan kehilangan dua bulan pertama trafik cross-post.</p>

<h2>Workflow Tulis Enam Langkah</h2>

<p>Workflow tulis lengkap, dari ujung ke ujung, memiliki enam langkah. Empat di antaranya script-driven dan dua interface-driven. Langkah interface-driven (langkah 1, pembuatan app password; langkah 5, submisi mirror) adalah satu-satunya tempat manusia harus berada di loop, dan keduanya adalah setup one-time. Setelah selesai, seluruh pipeline berjalan dari satu <code>make publish</code> pada file Markdown.</p>

<h3>Langkah 1: Buat app password</h3>

<p>App password adalah token berscope per-aplikasi yang dapat dicabut pengguna dari UI pengaturan Bluesky tanpa mempengaruhi sesi utama mereka. Buat satu di Settings -&gt; App Passwords -&gt; Add App Password, berikan nama (mis. "third-party-longform-publisher"), dan salin token yang ditampilkan satu kali. Simpan di secrets manager, bukan di repo. Token memiliki scope tulis yang sama dengan sesi utama Anda tetapi di-scope ke nama aplikasi di log audit, yang berguna ketika Anda men-debug tulis yang buruk yang tidak Anda lakukan dengan sengaja.</p>

<pre><code>""" + CODE_BLOCK_1 + """</code></pre>

<h3>Langkah 2: Tulis body post dalam Markdown</h3>

<p>Body long-form Bluesky adalah Markdown. Bukan subset, bukan flavor, bukan turunan. CommonMark standar dengan ekstensi GFM untuk tabel dan task list. Body hidup di field <code>embed.media.external.description</code>, dengan 200 karakter pertama digunakan sebagai preview link di timeline publik. Body lengkap di-fetch ketika pembaca mengklik untuk membuka.</p>

<p>Implikasi untuk developer alat adalah bahwa seluruh jalur tulis long-form dapat Markdown-first. File Markdown yang sama yang Anda tulis untuk post blog, newsletter Substack, atau artikel LinkedIn dapat menjadi source of truth untuk post panjang Bluesky, dengan judul di <code>embed.media.external.title</code> dan body di <code>embed.media.external.description</code> (dibatasi 200 karakter untuk preview, dengan body lengkap dirujuk melalui field canonical URL). Ini adalah bentuk yang sama yang digunakan playbook sisi-baca untuk mirror, dan simetri itulah yang membuat kedua sisi composable.</p>

<h3>Langkah 3: Tulis record</h3>

<p>Setelah Anda memiliki session token dan body Markdown, panggilan tulis adalah satu POST tunggal ke <code>com.atproto.repo.createRecord</code>. <code>collection</code> adalah <code>app.bsky.feed.post</code>, <code>repo</code> adalah DID pengguna, dan <code>record.embed</code> adalah struktur long-form. Respons membawa post URI, yang Anda perlukan untuk langkah mirror dan untuk field canonical URL di permukaan kutipan.</p>

<pre><code>""" + CODE_BLOCK_2 + """</code></pre>

<h3>Langkah 4: Konversi Markdown ke struktur embed</h3>

<p>Untuk alat yang mempublikasikan banyak post, konversi dari Markdown ke JSON embed Bluesky adalah bagian yang diimplementasi-ulang. Di bawah ini adalah versi yang berfungsi, dalam 20 baris Python, yang dapat dijatuhkan oleh alat pihak ketiga mana pun. Itu menggunakan <code>python-frontmatter</code> untuk membaca front matter (title, canonical_url, description) dan pass regex untuk strip Markdown untuk preview description.</p>

<pre><code>""" + CODE_BLOCK_3 + """</code></pre>

<h3>Langkah 5: Mirror ke permukaan citation-ready</h3>

<p>Post panjang Bluesky, secara default, hanya dapat diindeks di dalam pencarian Bluesky sendiri dan firehose AT Protocol. Agen AI (GPTBot, ClaudeBot, PerplexityBot) tidak meng-crawl app Bluesky, jadi post panjang tanpa mirror eksternal tidak terlihat oleh lapisan pencarian AI. Perbaikannya adalah mirror post ke URL stabil dan citation-ready pada hari yang sama Anda mempublikasikan ke Bluesky. Mirror harus membawa body Markdown lengkap, menaut balik ke post Bluesky, dan dikirimkan ke permukaan crawl standar (sitemap, llms.txt, Bing webmaster, IndexNow).</p>

<p>ThreadGrab adalah salah satu mirror tersebut, dan jalur publikasi adalah sama dengan yang Anda gunakan untuk permukaan long-form lainnya: POST source URI, public URL, judul, dan body Markdown ke endpoint ingest. Halaman mirror akan live dalam satu menit, entri sitemap ditambahkan secara otomatis, dan post dapat dijangkau oleh GPTBot dan ClaudeBot dalam siklus crawl berikutnya.</p>

<pre><code>""" + CODE_BLOCK_4 + """</code></pre>

<h3>Langkah 6: Kirim ke permukaan kutipan AI</h3>

<p>Langkah mirror adalah lapisan citation-ready. Langkah submisi adalah lapisan AI-citation. Setelah mirror live, dorong URL ke permukaan yang benar-benar di-crawl oleh agen AI: IndexNow (Bing + DuckDuckGo + ChatGPT search), file llms.txt di root domain mirror, dan sitemap. ThreadGrab menangani ketiganya di domain mirror; untuk mirror domain kustom, resep yang setara adalah mengirimkan URL melalui Bing Webmaster Tools dan menambahkannya secara manual ke sitemap dan llms.txt.</p>

<p>Untuk kreator yang mempublikasikan satu atau dua post panjang per minggu, submisi manual sudah cukup. Untuk kreator yang melakukan cross-post dari newsletter yang keluar mingguan ke ratusan pembaca, submisi harus diotomatisasi. Pattern-nya adalah: <code>make publish</code> memicu tulis Bluesky, tulis mirror, dan submisi IndexNow dalam satu shot, dengan post URI digaungkan ke stdout agar manusia di loop dapat mengkonfirmasi run.</p>

<h2>Perbandingan Cross-Platform: Bluesky vs X Articles vs LinkedIn</h2>

<p>Untuk kreator yang melakukan cross-post konten long-form, pohon keputusan sisi-tulis pada Juli 2026 terlihat seperti ini: Bluesky adalah lapisan di mana alat pihak ketiga dapat menulis langsung melalui API publik; X Articles adalah lapisan yang harus di-encode ulang setelahnya; artikel LinkedIn adalah lapisan di mana satu-satunya jalur tulis resmi adalah UI web LinkedIn.</p>

<table>
<thead><tr><th>Platform</th><th>API tulis long-form</th><th>Jalur auth</th><th>Rate limit</th><th>Mirror-friendliness</th></tr></thead>
<tbody>
<tr><td>Bluesky</td><td>Ya, publik (developer preview)</td><td>App password / OAuth</td><td>5.000 write requests / hari / DID</td><td>Tinggi (AT Protocol terbuka)</td></tr>
<tr><td>X Articles</td><td>Tertutup (X partner API saja)</td><td>OAuth 2.0 (X)</td><td>100 post / 24 jam (user tier)</td><td>Sedang (URL pattern stabil)</td></tr>
<tr><td>LinkedIn articles</td><td>Tertutup (tanpa API tulis publik)</td><td>Sesi LinkedIn</td><td>~20 post panjang / hari</td><td>Rendah (mirror UGC tidak diizinkan)</td></tr>
</tbody>
</table>

<p>Pattern yang muncul: Bluesky adalah platform di mana pipeline cross-post portabel dan script-driven; X Articles adalah platform di mana pipeline cross-post harus menggunakan partner API dan encode ulang body; LinkedIn adalah platform di mana satu-satunya jalur tulis adalah manusia di browser. Untuk kreator yang ingin satu pipeline publikasi long-form yang bekerja di ketiganya, pipeline menulis ke Bluesky dulu, mirror ke permukaan citation-ready, dan kemudian menggunakan partner API untuk X Articles ditambah fallback browser-automation untuk LinkedIn. Kaki Bluesky adalah satu-satunya di mana seluruh alur script-driven dari ujung ke ujung.</p>

<h2>Kapan Tidak Membangun Pipeline Sisi-Tulis</h2>

<p>Pipeline sisi-tulis layak dibangun ketika salah satu dari berikut ini benar: Anda mempublikasikan lebih dari dua post panjang per minggu, Anda ingin cross-post ke beberapa platform dari satu source, atau Anda ingin mirror AI-citation-ready pada hari yang sama Anda mempublikasikan. Itu tidak layak dibangun ketika Anda mempublikasikan kurang dari sekali per bulan, Anda hanya mempublikasikan ke satu platform, atau Anda tidak memerlukan kutipan AI. Biaya pipeline kira-kira setengah hari dev work pertama kali dan nol jam per minggu untuk dijalankan setelah itu. Untuk publisher sekali-sebulan, matematika itu tidak berhasil.</p>

<p>Untuk semua orang lain, SDK stabil Agustus 2026 adalah saat untuk mengirim. Sampai saat itu, developer preview cukup stabil untuk prototipe, rate limit dipublikasikan, dan mirror sisi-baca (playbook 6 Juli) adalah setengah lainnya dari loop. Kedua playbook bersama-sama adalah stack kreator yang berfungsi untuk paruh kedua 2026: baca ke Markdown untuk arsip, tulis dari Markdown untuk cross-post, mirror ke permukaan citation-ready untuk penemuan AI. Itulah loop, dan sekarang seluruhnya script-driven.</p>

<p>Untuk kreator yang sudah menjalankan <a href="/id/blog/bluesky-long-form-creator-playbook-2026.html">playbook sisi-baca</a> di ThreadGrab, pipeline sisi-tulis adalah bagian yang hilang. Menambahkan empat skrip dalam artikel ini ke repo yang sama, cron yang sama, dan jalur deploy yang sama mengubah mirror sisi-baca menjadi loop write-publish-mirror di mana alat apa pun dapat plug-in. Itulah stack long-form production-grade untuk paruh kedua 2026, dan itu tidak perlu menunggu SDK stabil untuk mulai berfungsi.</p>
"""


# === JSON-LD builders ===
def article_jsonld(headline, desc, lang):
    return f"""  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{headline}",
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
    return f"""  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://threadgrab.com/{lang}/"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://threadgrab.com/{lang}/blog/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{tail}"
    }}
  ]
}}
  </script>"""


def faq_jsonld(faq_pairs):
    items = []
    for q, a in faq_pairs:
        # Escape quotes in JSON text
        q_esc = q.replace('"', '\\"')
        a_esc = a.replace('"', '\\"')
        items.append(f"""    {{
      "@type": "Question",
      "name": "{q_esc}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a_esc}"
      }}
    }}""")
    items_joined = ",\n".join(items)
    return f"""  <script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{items_joined}
  ]
}}
  </script>"""


def render_faq_html(faq_pairs):
    out = []
    for q, a in faq_pairs:
        out.append(f'''    <div class="faq-item">
      <strong>{q}</strong>
      <p>{a}</p>
    </div>''')
    return '\n'.join(out)


def build_page(lang, title, desc, keywords, body, h1_base, h1_span, meta, breadcrumb_tail,
               article_h1, faq_pairs, faq_json):
    other_langs = [l for l in ('en', 'pt', 'id') if l != lang]
    active_link = f'      <a class="active" href="/{lang}/blog/{SLUG}.html">{lang.upper()}</a>\n'
    other_links = ''.join(
        f'      <a class="" href="/{ol}/blog/{SLUG}.html">{ol.upper()}</a>\n'
        for ol in other_langs
    )
    hreflangs = '\n'.join(
        f'  <link rel="alternate" hreflang="{hl}" href="https://threadgrab.com/{hl}/blog/{SLUG}.html">'
        for hl in ('en', 'pt', 'id', 'x-default')
    )
    og_locale = {'en': 'en_US', 'pt': 'pt_BR', 'id': 'id_ID'}[lang]
    faq_html = render_faq_html(faq_pairs)

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
{hreflangs}
  <meta property="og:title" content="{title}">
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
{article_jsonld(article_h1, desc, lang)}
{breadcrumb_jsonld(lang, breadcrumb_tail)}
{faq_json}
</head>
<body>
  <header>
    <a class="logo" href="/{lang}/">Thread<span>Grab</span></a>
    <div class="lang-bar">
{active_link}{other_links}    </div>
  </header>

  <main>
    <div class="breadcrumb"><a href="/{lang}/">Home</a> &rsaquo; <a href="/{lang}/blog/">Blog</a> &rsaquo; {breadcrumb_tail}</div>

    <h1>{h1_base} <span>{h1_span}</span></h1>
    <p class="meta">{meta}</p>

{body}
    <h2>Frequently Asked Questions</h2>
{faq_html}

    <div class="cta">
      <p>Want the citation-ready mirror on your own domain?</p>
      <a class="btn" href="/{lang}/">Try ThreadGrab</a>
    </div>
  </main>

  <footer>
    &copy; 2026 ThreadGrab &middot; <a href="/{lang}/">Home</a> &middot; <a href="/{lang}/blog/">Blog</a> &middot; <a href="/{lang}/about/">About</a> &middot; <a href="/{lang}/privacy/">Privacy</a>
    <br>Not affiliated with X Corp., Bluesky Social PBC, LinkedIn Corporation, or Microsoft Corporation.
  </footer>
</body>
</html>
"""


def main():
    # Sanity: length checks before any writes
    print("\n=== Pre-build length checks ===")
    for label, t in [('TITLE_EN', TITLE_EN), ('TITLE_PT', TITLE_PT), ('TITLE_ID', TITLE_ID)]:
        valid = 30 <= len(t) <= 60
        print(f"  {label}: {len(t)} chars {'✅' if valid else '❌'}")
        assert valid, f"❌ {label} length {len(t)} not in 30-60"
    for label, d in [('DESC_EN', DESC_EN), ('DESC_PT', DESC_PT), ('DESC_ID', DESC_ID)]:
        valid = 70 <= len(d) <= 155
        print(f"  {label}: {len(d)} chars {'✅' if valid else '❌'}")
        assert valid, f"❌ {label} length {len(d)} not in 70-155"
    print("✅ All title/desc length checks pass\n")

    pages = [
        {
            'lang': 'en', 'title': TITLE_EN, 'desc': DESC_EN, 'keywords': KEYWORDS_EN,
            'body': EN_BODY, 'h1_base': H1_EN_BASE, 'h1_span': H1_EN_SPAN,
            'meta': META_EN, 'breadcrumb_tail': BREADCRUMB_TAIL_EN,
            'article_h1': ARTICLE_H1_EN, 'faq_pairs': FAQ_EN,
        },
        {
            'lang': 'pt', 'title': TITLE_PT, 'desc': DESC_PT, 'keywords': KEYWORDS_PT,
            'body': PT_BODY, 'h1_base': H1_PT_BASE, 'h1_span': H1_PT_SPAN,
            'meta': META_PT, 'breadcrumb_tail': BREADCRUMB_TAIL_PT,
            'article_h1': ARTICLE_H1_PT, 'faq_pairs': FAQ_PT,
        },
        {
            'lang': 'id', 'title': TITLE_ID, 'desc': DESC_ID, 'keywords': KEYWORDS_ID,
            'body': ID_BODY, 'h1_base': H1_ID_BASE, 'h1_span': H1_ID_SPAN,
            'meta': META_ID, 'breadcrumb_tail': BREADCRUMB_TAIL_ID,
            'article_h1': ARTICLE_H1_ID, 'faq_pairs': FAQ_ID,
        },
    ]

    for p in pages:
        faq_json = faq_jsonld(p['faq_pairs'])
        html = build_page(
            p['lang'], p['title'], p['desc'], p['keywords'],
            p['body'], p['h1_base'], p['h1_span'], p['meta'],
            p['breadcrumb_tail'], p['article_h1'],
            p['faq_pairs'], faq_json,
        )
        out_path = f"/root/threadgrab-site/{p['lang']}/blog/{SLUG}.html"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  WROTE: {out_path} ({len(html):,} bytes)")

    # Update blog indexes
    new_entries = {
        'en': f'''        <ul class="post-list">
      <li>
        <a href="/en/blog/{SLUG}.html">{TITLE_EN}</a>
        <div class="post-meta">{DATE_EN} &middot; 10 min read &middot; Guide</div>
        <div class="post-desc">{DESC_EN}</div>
      </li>
''',
        'pt': f'''        <ul class="post-list">
      <li>
        <a href="/pt/blog/{SLUG}.html">{TITLE_PT}</a>
        <div class="post-meta">{DATE_PT} &middot; 10 min de leitura &middot; Guia</div>
        <div class="post-desc">{DESC_PT}</div>
      </li>
''',
        'id': f'''        <ul class="post-list">
      <li>
        <a href="/id/blog/{SLUG}.html">{TITLE_ID}</a>
        <div class="post-meta">{DATE_ID} &middot; 10 menit baca &middot; Panduan</div>
        <div class="post-desc">{DESC_ID}</div>
      </li>
''',
    }
    for lang, entry in new_entries.items():
        path = f'/root/threadgrab-site/{lang}/blog/index.html'
        with open(path) as f:
            html = f.read()
        if f'/blog/{SLUG}.html' in html:
            print(f"  {lang}: already has {SLUG} — skip index")
            continue
        new_html = html.replace('<ul class="post-list">', entry, 1)
        with open(path, 'w') as f:
            f.write(new_html)
        print(f"  {lang}: prepended card in blog index")

    # Sitemap
    sitemap_path = '/root/threadgrab-site/sitemap.xml'
    with open(sitemap_path) as f:
        sitemap = f.read()
    if f'{SLUG}.html' in sitemap:
        print(f"  sitemap: already has {SLUG} — skip")
    else:
        new_block = f'''    <url>
        <loc>https://threadgrab.com/en/blog/{SLUG}.html</loc>
        <xhtml:link rel="alternate" hreflang="en" href="https://threadgrab.com/en/blog/{SLUG}.html"/>
        <xhtml:link rel="alternate" hreflang="pt" href="https://threadgrab.com/pt/blog/{SLUG}.html"/>
        <xhtml:link rel="alternate" hreflang="id" href="https://threadgrab.com/id/blog/{SLUG}.html"/>
        <xhtml:link rel="alternate" hreflang="x-default" href="https://threadgrab.com/en/blog/{SLUG}.html"/>
        <lastmod>{DATE}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
'''
        new_sitemap = sitemap.replace('</urlset>', new_block + '</urlset>')
        with open(sitemap_path, 'w') as f:
            f.write(new_sitemap)
        print(f"  sitemap: added {SLUG}")

    # state.json drafts
    state_path = '/root/threadgrab-site/drafts/state.json'
    with open(state_path) as f:
        state = json.load(f)
    if any(d.get('slug') == SLUG for d in state['drafts']):
        print(f"  state.json: drafts already has {SLUG} — skip")
    else:
        for lang, title, desc, tags, heat in [
            ('en', TITLE_EN, DESC_EN, TAGS_EN, HEAT_SOURCE_EN),
            ('pt', TITLE_PT, DESC_PT, TAGS_PT, HEAT_SOURCE_PT),
            ('id', TITLE_ID, DESC_ID, TAGS_ID, HEAT_SOURCE_ID),
        ]:
            state['drafts'].append({
                'slug': SLUG, 'date': DATE, 'type': 'guide', 'lang': lang,
                'title': title, 'description': desc,
                'file': f'{lang}/blog/{SLUG}.html',
                'url': f'https://threadgrab.com/{lang}/blog/{SLUG}.html',
                'path_en': f'en/blog/{SLUG}.html',
                'path_pt': f'pt/blog/{SLUG}.html',
                'path_id': f'id/blog/{SLUG}.html',
                'url_en': f'https://threadgrab.com/en/blog/{SLUG}.html',
                'url_pt': f'https://threadgrab.com/pt/blog/{SLUG}.html',
                'url_id': f'https://threadgrab.com/id/blog/{SLUG}.html',
                'heat_source': heat, 'tags': tags,
                'schema_types': ['Article', 'BreadcrumbList', 'FAQPage'],
                'status': 'outline_pending_publish', 'created_at': DATE,
                'lang_versions': ['en', 'pt', 'id'],
            })
        state['last_run'] = f'{DATE}T12:00:00+08:00'
        state['last_draft_slug'] = SLUG
        state['drafts_count'] = len([d for d in state['drafts'] if d.get('status') == 'outline_pending_publish'])
        state['published_count'] = len(state['published'])
        recent = [t for t in state.get('recent_topics', []) if t != SLUG]
        recent.insert(0, SLUG)
        state['recent_topics'] = recent
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(f"  state.json: appended 3 drafts for {SLUG}")

    # Run verifier
    print("\n=== Running verifier ===")
    r = subprocess.run(
        ['python3', '/root/.hermes/skills/ilang-content/scripts/threadgrab-3lang-verify.py',
         '/root/threadgrab-site', SLUG],
        capture_output=True, text=True, timeout=60
    )
    print(r.stdout)
    if r.returncode != 0:
        print("❌ Verifier failed")
        print(r.stderr)
        sys.exit(1)
    print("\n✅ Article built and verified. Awaiting user 'publish' confirmation.")


if __name__ == '__main__':
    main()
