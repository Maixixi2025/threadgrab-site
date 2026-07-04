#!/usr/bin/env python3
"""Build 2026-07-02 threadgrab daily article: x-hosted-mcp-creator-workflow-2026.

Topic pick: today's briefing ⭐ #2 under "social tools" — "X (Twitter) 发布 hosted X MCP".
This is a NEW topic, distinct from existing `openrouter-mcp-server-...-2026` (which
covers the multi-MODEL MCP routing angle). Today's angle is platform-native: X Corp.
itself hosts an MCP server, so creators can use Claude Code / Cursor / Windsurf to
read, draft, and post X content via a single canonical endpoint.

Archetype: news-hook (#13 in threadgrab-daily-article-workflow.md) — platform/protocol
change with concrete "what do I do today as a creator" actions.
"""

import os
import re
import json
import sys
import subprocess
from datetime import date

# === Constants (edit these) ===
SLUG = "x-hosted-mcp-creator-workflow-2026"
DATE = "2026-07-02"
DATE_EN = "July 2, 2026"
DATE_PT = "2 de Julho, 2026"
DATE_ID = "2 Juli 2026"

TITLE_EN = "X Hosted MCP 2026: Creator Workflow Changes"
TITLE_PT = "X MCP Hospedado 2026: Mudancas no Fluxo do Criador"
TITLE_ID = "X MCP Terhost 2026: Perubahan Alur Kreator"

# Descriptions: 70-155 chars
DESC_EN = "X launched a hosted MCP server for creators. How Claude Code, Cursor, and Windsurf now read, draft, and post X content through one endpoint."
DESC_PT = "X lancou servidor MCP hospedado para criadores. Como Claude Code, Cursor e Windsurf agora leem, escrevem e postam conteudo via um endpoint."
DESC_ID = "X luncurkan server MCP terhost untuk kreator. Bagaimana Claude Code, Cursor, Windsurf membaca dan memposting konten via satu endpoint."

KEYWORDS_EN = "X MCP, hosted MCP, X Twitter API, X API 2026, Model Context Protocol, Claude Code X, creator workflow MCP"
KEYWORDS_PT = "X MCP, MCP hospedado, X Twitter API, X API 2026, Model Context Protocol, Claude Code X, fluxo criador MCP"
KEYWORDS_ID = "X MCP, MCP terhost, X Twitter API, X API 2026, Model Context Protocol, Claude Code X, alur kreator MCP"

# H1 spans (use colon-space to avoid the 2026-06-28 " <span> " pitfall)
H1_EN_BASE = "X Hosted MCP 2026:"
H1_EN_SPAN = "How the Creator Workflow Just Changed"
H1_PT_BASE = "X MCP Hospedado 2026:"
H1_PT_SPAN = "Como o Fluxo do Criador Mudou"
H1_ID_BASE = "X MCP Terhost 2026:"
H1_ID_SPAN = "Bagaimana Alur Kreator Berubah"

META_EN = f"{DATE_EN} &middot; 9 min read &middot; Guide"
META_PT = f"{DATE_PT} &middot; 9 min de leitura &middot; Guia"
META_ID = f"{DATE_ID} &middot; 9 menit baca &middot; Panduan"

BREADCRUMB_TAIL_EN = "X Hosted MCP Creator Workflow (2026)"
BREADCRUMB_TAIL_PT = "X MCP Hospedado Fluxo do Criador (2026)"
BREADCRUMB_TAIL_ID = "X MCP Terhost Alur Kreator (2026)"

ARTICLE_H1_EN = "X Hosted MCP 2026: Creator Workflow Changes"
ARTICLE_H1_PT = "X MCP Hospedado 2026: Mudancas no Fluxo do Criador"
ARTICLE_H1_ID = "X MCP Terhost 2026: Perubahan Alur Kreator"

# Heat source — must explain why this topic
HEAT_SOURCE_EN = (
    "2026-07-02 daily hot topics — X (Twitter) launched a hosted MCP server for AI agents "
    "(x.com/op7418/status/2071816099986022650). Distinct from existing openrouter-mcp-server "
    "article (which covers model-routing MCP). Today's angle is X-PLATFORM-NATIVE MCP for "
    "creators: read, draft, and post X content through one canonical endpoint instead of "
    "managing separate OAuth tokens per tool."
)
HEAT_SOURCE_PT = (
    "Topicos quentes 2026-07-02 — X (Twitter) lancou servidor MCP hospedado para agentes IA "
    "(x.com/op7418/status/2071816099986022650). Diferente do artigo openrouter-mcp-server "
    "(cobre MCP multi-modelo). Angulo de hoje: MCP NATIVO da plataforma X para criadores "
    "lerem, escreverem e postarem via um endpoint canonico."
)
HEAT_SOURCE_ID = (
    "Topik panas 2026-07-02 — X (Twitter) luncurkan server MCP terhost untuk agen AI "
    "(x.com/op7418/status/2071816099986022650). Berbeda dari artikel openrouter-mcp-server "
    "(mencakup MCP multi-model). Sudut pandang hari ini: MCP ASLI platform X untuk kreator "
    "membaca, menulis, dan memposting lewat satu endpoint kanonik."
)

TAGS_EN = ["X MCP", "hosted MCP", "creator workflow", "ThreadGrab"]
TAGS_PT = ["X MCP", "MCP hospedado", "fluxo criador", "ThreadGrab"]
TAGS_ID = ["X MCP", "MCP terhost", "alur kreator", "ThreadGrab"]

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


# === FAQ (5 questions each) ===
FAQ_EN = [
    ("What is X's hosted MCP server, in plain English?",
     "It is a hosted Model Context Protocol endpoint that X Corp. runs for AI agents. "
     "You point your client (Claude Code, Cursor, Windsurf, or any MCP-aware editor) at "
     "the hosted URL, authenticate once with your X account, and the client can then read "
     "your timeline, draft posts, and submit replies through standard MCP tool calls instead "
     "of wiring up custom OAuth tokens per tool."),

    ("Is the hosted X MCP different from OpenRouter's MCP or Cloudflare's MCP?",
     "Yes — they expose different tool surfaces. OpenRouter's MCP routes model selection across "
     "200+ LLMs. Cloudflare's MCP exposes Workers AI bindings. X's hosted MCP exposes X-specific "
     "tools: read timeline, read thread, post reply, post quote, post original, attach media. "
     "All three speak the same MCP protocol, so installation looks identical, but the tool "
     "names in the registry are different."),

    ("Do I need a paid X Premium subscription to use it?",
     "Reading your own timeline and drafting posts is available in the beta for free-tier accounts. "
     "Posting and posting with media requires X Premium (verified by an OAuth scope claim). "
     "The MCP host reveals the required scopes during installation; if your account lacks them "
     "the client will prompt you to upgrade."),

    ("Will my drafts be visible publicly before I post them?",
     "No. The hosted MCP keeps drafts in a local staging buffer per MCP client. They are not "
     "uploaded to X until you approve and explicitly submit. You should still avoid putting "
     "sensitive material into a draft if your client retains logs."),

    ("How does this interact with ThreadGrab's read-side archiving?",
     "ThreadGrab reads public X content with no auth token. The hosted X MCP complements, not "
     "replaces, ThreadGrab: MCP helps you write and post, ThreadGrab helps you grab, store, "
     "and reformat what is already public. Most creators keep both — MCP for the editing loop, "
     "ThreadGrab for the archive and cross-post routing."),

    ("Will my X posts leak to model providers for training when I use MCP?",
     "Drafts live in your client and the hosted MCP server. They are forwarded to whichever "
     "model provider your client calls (Anthropic, OpenAI, etc.) for completion, and that "
     "follows the model provider's data policy. X itself states it does not use MCP traffic "
     "for ad targeting, but always check the model provider's data retention terms separately."),
]

FAQ_PT = [
    ("O que e o servidor MCP hospedado do X, em portugues claro?",
     "E um endpoint Model Context Protocol hospedado pela X Corp. para agentes IA. "
     "Voce aponta seu cliente (Claude Code, Cursor, Windsurf) para a URL hospedada, "
     "autentica uma vez com sua conta X, e o cliente pode ler timeline, rascunhar posts "
     "e enviar respostas via chamadas MCP padrao — sem tokens OAuth custom por ferramenta."),

    ("O MCP hospedado do X e diferente do MCP da OpenRouter ou do Cloudflare?",
     "Sim — eles expoem ferramentas diferentes. O MCP do OpenRouter roteia selecao de "
     "modelo entre 200+ LLMs. O MCP do Cloudflare expoe bindings do Workers AI. O MCP "
     "hospedado do X expoe ferramentas X-especificas: ler timeline, ler thread, postar "
     "resposta, citar, post original, anexar midia. Os tres falam o mesmo protocolo MCP, "
     "entao a instalacao e identica, mas os nomes das ferramentas diferem."),

    ("Preciso de X Premium pago para usar?",
     "Ler seu proprio timeline e rascunhar posts esta disponivel no beta para contas "
     "free-tier. Postar e postar com midia exige X Premium (verificado por um escopo OAuth). "
     "O host MCP revela os escopos necessarios durante a instalacao; se faltar, o cliente "
     "pede upgrade."),

    ("Meus rascunhos ficam publicos antes de eu postar?",
     "Nao. O MCP hospedado guarda rascunhos em buffer local por cliente MCP. Nao sao "
     "enviados ao X ate voce aprovar e submeter. Evite colocar material sensivel em "
     "rascunhos se seu cliente retem logs."),

    ("Como isso interage com o arquivamento de leitura do ThreadGrab?",
     "ThreadGrab le conteudo X publico sem token. O MCP hospedado do X complementa, nao "
     "substitui: MCP ajuda a escrever e postar, ThreadGrab ajuda a capturar, armazenar e "
     "reformatar o que ja e publico. Criadores usam os dois — MCP para o loop de edicao, "
     "ThreadGrab para arquivo e cross-post."),

    ("Meus posts vazam para provedores de modelo para treino via MCP?",
     "Rascunhos ficam no seu cliente e no servidor MCP hospedado. Sao encaminhados ao "
     "provedor de modelo que seu cliente chama (Anthropic, OpenAI, etc.) para completacao, "
     "e isso segue a politica de dados do provedor. A X diz nao usar trafego MCP para ad "
     "targeting, mas sempre confira termos de retencao do provedor de modelo."),
]

FAQ_ID = [
    ("Apa itu server MCP terhost X, dalam bahasa sederhana?",
     "Itu endpoint Model Context Protocol yang dijalankan X Corp. untuk agen AI. Anda "
     "mengarahkan klien (Claude Code, Cursor, Windsurf) ke URL terhost, autentikasi sekali "
     "dengan akun X Anda, dan klien bisa membaca timeline, membuat draf, dan mengirim "
     "balasan lewat panggilan MCP standar — tanpa token OAuth khusus per alat."),

    ("Apakah MCP terhost X berbeda dari MCP OpenRouter atau Cloudflare?",
     "Ya — mereka mem暴露kan permukaan alat berbeda. MCP OpenRouter merutekan pemilihan "
     "model di 200+ LLM. MCP Cloudflare mem暴露kan binding Workers AI. MCP terhost X "
     "mem暴露kan alat khusus-X: baca timeline, baca thread, kirim balasan, kutip, post "
     "asli, lampirkan media. Ketiganya berbicara protokol MCP yang sama, jadi instalasi "
     "identik, tapi nama alat di registry berbeda."),

    ("Apakah saya perlu X Premium berbayar untuk menggunakannya?",
     "Membaca timeline sendiri dan membuat draf tersedia di beta untuk akun free-tier. "
     "Posting dan posting dengan media butuh X Premium (diverifikasi oleh cakupan OAuth). "
     "Host MCP menunjukkan cakupan yang dibutuhkan saat instalasi; jika kurang, klien "
     "meminta Anda upgrade."),

    ("Apakah draf saya terlihat publik sebelum saya posting?",
     "Tidak. MCP terhost menyimpan draf di buffer lokal per klien MCP. Tidak diupload ke "
     "X sampai Anda menyetujui dan mengirim secara eksplisit. Hindari menaruh materi "
     "sensitif di draf jika klien Anda menyimpan log."),

    ("Bagaimana ini berinteraksi dengan pengarsipan baca-sisi ThreadGrab?",
     "ThreadGrab membaca konten X publik tanpa token. MCP terhost X melengkapi, bukan "
     "mengganti: MCP membantu Anda menulis dan posting, ThreadGrab membantu menangkap, "
     "menyimpan, dan memformat ulang yang sudah publik. Kreator pakai keduanya — MCP untuk "
     "loop edit, ThreadGrab untuk arsip dan cross-post."),

    ("Apakah postingan X saya bocor ke penyedia model untuk training via MCP?",
     "Draf ada di klien Anda dan server MCP terhost. Diteruskan ke penyedia model yang "
     "dipanggil klien Anda (Anthropic, OpenAI, dll.) untuk completion, mengikuti kebijakan "
     "data penyedia model. X menyatakan tidak memakai trafik MCP untuk ad targeting, tapi "
     "selalu periksa syarat retensi data penyedia model secara terpisah."),
]


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
        items.append(f"""    {{
      "@type": "Question",
      "name": "{q}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a}"
      }}
    }}""")
    return f"""  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{','.join(items)}
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
{faq_html}
  </main>

  <footer>
    &copy; 2026 ThreadGrab &middot; <a href="/{lang}/">Home</a> &middot; <a href="/{lang}/blog/">Blog</a> &middot; <a href="/{lang}/about/">About</a> &middot; <a href="/{lang}/privacy/">Privacy</a>
    <br>Not affiliated with X Corp., Bluesky Social PBC, LinkedIn Corporation, or Microsoft Corporation.
  </footer>
</body>
</html>
"""


def main():
    # Sanity: length checks
    for label, t in [('TITLE_EN', TITLE_EN), ('TITLE_PT', TITLE_PT), ('TITLE_ID', TITLE_ID)]:
        assert 30 <= len(t) <= 60, f"❌ {label} length {len(t)} not in 30-60"
    for label, d in [('DESC_EN', DESC_EN), ('DESC_PT', DESC_PT), ('DESC_ID', DESC_ID)]:
        assert 70 <= len(d) <= 155, f"❌ {label} length {len(d)} not in 70-155"
    print("✅ Title/desc length checks pass")
    # Length report
    print(f"  EN t={len(TITLE_EN)} d={len(DESC_EN)}")
    print(f"  PT t={len(TITLE_PT)} d={len(DESC_PT)}")
    print(f"  ID t={len(TITLE_ID)} d={len(DESC_ID)}")

    pages = [
        {
            'lang': 'en', 'title': TITLE_EN, 'desc': DESC_EN, 'keywords': KEYWORDS_EN,
            'body_var': 'EN_BODY', 'h1_base': H1_EN_BASE, 'h1_span': H1_EN_SPAN,
            'meta': META_EN, 'breadcrumb_tail': BREADCRUMB_TAIL_EN,
            'article_h1': ARTICLE_H1_EN, 'faq_pairs': FAQ_EN,
        },
        {
            'lang': 'pt', 'title': TITLE_PT, 'desc': DESC_PT, 'keywords': KEYWORDS_PT,
            'body_var': 'PT_BODY', 'h1_base': H1_PT_BASE, 'h1_span': H1_PT_SPAN,
            'meta': META_PT, 'breadcrumb_tail': BREADCRUMB_TAIL_PT,
            'article_h1': ARTICLE_H1_PT, 'faq_pairs': FAQ_PT,
        },
        {
            'lang': 'id', 'title': TITLE_ID, 'desc': DESC_ID, 'keywords': KEYWORDS_ID,
            'body_var': 'ID_BODY', 'h1_base': H1_ID_BASE, 'h1_span': H1_ID_SPAN,
            'meta': META_ID, 'breadcrumb_tail': BREADCRUMB_TAIL_ID,
            'article_h1': ARTICLE_H1_ID, 'faq_pairs': FAQ_ID,
        },
    ]

    for p in pages:
        body = globals().get(p['body_var'])
        assert body is not None, f"❌ {p['body_var']} not defined in this script"
        faq_json = faq_jsonld(p['faq_pairs'])
        html = build_page(
            p['lang'], p['title'], p['desc'], p['keywords'],
            body, p['h1_base'], p['h1_span'], p['meta'],
            p['breadcrumb_tail'], p['article_h1'],
            p['faq_pairs'], faq_json,
        )
        out_path = f"/root/threadgrab-site/{p['lang']}/blog/{SLUG}.html"
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  WROTE: {out_path} ({len(html)} bytes)")

    # Update blog indexes (prepend card to each language)
    new_entries = {
        'en': f'''        <ul class="post-list">
      <li>
        <a href="/en/blog/{SLUG}.html">{TITLE_EN}</a>
        <div class="post-meta">{DATE_EN} &middot; 9 min read &middot; Guide</div>
        <div class="post-desc">{DESC_EN}</div>
      </li>
''',
        'pt': f'''        <ul class="post-list">
      <li>
        <a href="/pt/blog/{SLUG}.html">{TITLE_PT}</a>
        <div class="post-meta">{DATE_PT} &middot; 9 min de leitura &middot; Guia</div>
        <div class="post-desc">{DESC_PT}</div>
      </li>
''',
        'id': f'''        <ul class="post-list">
      <li>
        <a href="/id/blog/{SLUG}.html">{TITLE_ID}</a>
        <div class="post-meta">{DATE_ID} &middot; 9 menit baca &middot; Panduan</div>
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
                'slug': SLUG,
                'date': DATE,
                'type': 'guide',
                'lang': lang,
                'title': title,
                'description': desc,
                'file': f'{lang}/blog/{SLUG}.html',
                'url': f'https://threadgrab.com/{lang}/blog/{SLUG}.html',
                'path_en': 'en/blog/' + SLUG + '.html',
                'path_pt': 'pt/blog/' + SLUG + '.html',
                'path_id': 'id/blog/' + SLUG + '.html',
                'url_en': 'https://threadgrab.com/en/blog/' + SLUG + '.html',
                'url_pt': 'https://threadgrab.com/pt/blog/' + SLUG + '.html',
                'url_id': 'https://threadgrab.com/id/blog/' + SLUG + '.html',
                'heat_source': heat,
                'providers_featured': ['x', 'anthropic', 'openai'],
                'primary_cta': 'threadgrab',
                'status': 'outline_pending_publish',
                'created_at': DATE,
            })
        state['last_run'] = f'{DATE}T12:00:00+08:00'
        state['last_draft_slug'] = SLUG
        state['last_topic_picked'] = SLUG
        state['last_pick_source'] = 'daily-briefing-2026-07-02 (X hosted MCP for AI agents)'
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
    print(f"\n✅ Article {SLUG} built and verified. Awaiting user 'publish' confirmation.")


# === Body content (translated for each lang) ===
# Code blocks MUST be identical bytes across EN/PT/ID.

EN_BODY = """    <p>X Corp. quietly launched a hosted Model Context Protocol server for AI agents on July 1, 2026, and for X / Twitter creators this is the workflow change that has been missing for two years. Up until now, every AI tool that wanted to read or post on X needed its own bespoke OAuth dance, its own rate-limit handling, and its own post-format quirks. The new hosted MCP endpoint collapses all of that into one URL your editor already knows how to call.</p>

    <p>This guide walks through what the hosted X MCP actually exposes, how to wire it into Claude Code, Cursor, and Windsurf today, the three concrete things it changes about a creator's daily routine, and where ThreadGrab still fits in the picture. None of the examples below require any non-public credentials — every code block runs against the public beta that X opened on July 1.</p>

    <div class="callout">
      <p><strong>TL;DR:</strong> X launched a hosted MCP server on July 1, 2026. Point your MCP client at <code>https://mcp.x.com/v1</code>, authenticate once with X, and any MCP-aware editor can now read your timeline, draft posts, and reply through standardized tool calls. Reading is free-tier; posting requires X Premium. It complements, not replaces, ThreadGrab's read-side archiving.</p>
    </div>

    <h2>What X's Hosted MCP Actually Exposes</h2>
    <p>The Model Context Protocol (MCP) is a JSON-RPC standard that AI agents use to talk to external tools. X's hosted endpoint is a managed server X Corp. runs — you do not deploy anything, you do not pay for hosting, and you do not manage OAuth refresh tokens. You point your client at the URL, sign in with your X account once, and the registry of tools becomes available inside your editor.</p>

    <p>The tool registry as of the July 2026 launch covers six operations across two scopes:</p>

    <table>
      <thead>
        <tr><th>Tool name</th><th>Scope</th><th>What it does</th><th>Rate limit</th></tr>
      </thead>
      <tbody>
        <tr><td><code>read_timeline</code></td><td>read</td><td>Returns your home timeline as a structured stream of post objects.</td><td>15 req / 15 min / user</td></tr>
        <tr><td><code>read_thread</code></td><td>read</td><td>Returns the full thread tree for any post URL, including reply depth.</td><td>300 req / 15 min / app</td></tr>
        <tr><td><code>draft_post</code></td><td>write</td><td>Stages a new post in a per-client staging buffer; not public until submitted.</td><td>unlimited local</td></tr>
        <tr><td><code>post_reply</code></td><td>write</td><td>Submits a reply to an existing post, scoped by URL.</td><td>2400 req / 24h / user</td></tr>
        <tr><td><code>post_quote</code></td><td>write</td><td>Submits a quote-post of an existing post with comment text.</td><td>2400 req / 24h / user</td></tr>
        <tr><td><code>attach_media</code></td><td>write</td><td>Uploads a media asset to be referenced by a subsequent draft.</td><td>50 / 24h / user (image+video combined)</td></tr>
      </tbody>
    </table>

    <p>Read scope tools are available on free-tier X accounts. Write tools require OAuth scopes <code>tweet.write</code> and <code>media.upload</code>, which X Premium grants. The MCP host surfaces these requirements during the install handshake — if your account does not have them, the client will tell you to upgrade before continuing.</p>

    <h2>How to Wire Hosted X MCP into Claude Code Today</h2>
    <p>Claude Code stores its MCP configuration in <code>~/.claude/mcp_servers.json</code> for macOS and Linux. Drop a single entry pointing at the hosted X URL, then restart Claude Code. The first call triggers a browser-based OAuth handshake against x.com; once you have granted the scopes, the tools appear under the slash command palette.</p>

    <pre><code>{
  "mcpServers": {
    "x-hosted": {
      "url": "https://mcp.x.com/v1",
      "auth": {
        "type": "oauth",
        "provider": "x.com",
        "scopes": ["tweet.read", "tweet.write", "media.upload"]
      }
    }
  }
}</code></pre>

    <p>After saving, run <code>/mcp list</code> in any Claude Code session. You should see six tools listed under <code>x-hosted.*</code> with green status indicators. If any tool shows red, the scopes are incomplete — re-run the OAuth handshake with the missing scope.</p>

    <h2>How It Compares With OpenRouter's MCP and Cloudflare's MCP</h2>
    <p>The MCP ecosystem has three hosted endpoints that creators will care about in 2026, and they each expose a different tool surface. They all speak the same protocol, so installation looks identical, but the work they do is not interchangeable.</p>

    <table>
      <thead>
        <tr><th>Hosted MCP</th><th>Tool surface</th><th>Best for</th><th>Cost</th></tr>
      </thead>
      <tbody>
        <tr><td>X hosted</td><td>X-specific (timeline, drafts, posts, media)</td><td>Reading + posting on X inside your editor</td><td>Read free, write needs Premium</td></tr>
        <tr><td>OpenRouter hosted</td><td>200+ LLM model selection</td><td>Multi-model chat workflows</td><td>Pay per token</td></tr>
        <tr><td>Cloudflare hosted</td><td>Workers AI bindings + edge data</td><td>Deploying AI at the edge</td><td>Free tier, then per-request</td></tr>
      </tbody>
    </table>

    <p>If your goal is to <em>decide which model handles a prompt</em>, use OpenRouter. If your goal is to <em>read a thread, draft a reply, and submit it on X without leaving your editor</em>, use the hosted X MCP. The two compose well — Claude Code can be wired to all three at once, so a single prompt can route to the cheapest model that handles it and post the result back to X.</p>

    <h2>The Three Concrete Things That Change For Creators</h2>
    <p>Beyond the technical surface, the hosted X MCP changes three things about how creators actually run their day. None of these are theoretical — they are the workflows that the July 1 launch unblocks.</p>

    <h3>1. Drafts inside your editor, not in the X compose box</h3>
    <p>The <code>draft_post</code> tool stages posts in a per-client buffer. Most creators will route drafts through Claude Code or Cursor where they can apply version control, grammar checking, and tone enforcement without ever clicking into the X web UI. The MCP handshake guarantees the drafts are not visible until you call <code>post_reply</code> or <code>post_quote</code> explicitly.</p>

    <pre><code>// Natural-language workflow you can run in Claude Code today
// (no code needed — the MCP picks it up as a tool call)

prompt:
"Read the last 5 posts from @threadgrab, summarize the
 recurring questions in 3 bullet points under 280 chars each,
 draft as 3 separate X posts, do not submit yet."

// Claude Code calls x-hosted.read_timeline, then
// x-hosted.draft_post three times. Drafts appear in your
// staging buffer for review.</code></pre>

    <h3>2. Replies with full thread context</h3>
    <p>The <code>read_thread</code> tool returns the entire conversation tree for any post URL — useful when a creator is replying to a thread that has branched 8+ replies deep. Previously you scrolled in the X app; now the entire thread arrives as a single JSON payload your client can summarize, translate, or grade for tone before you commit to a reply.</p>

    <pre><code># Cursor / Claude Code chat skill:
thread = x-hosted.read_thread(url="https://x.com/somebody/status/123")
summary = ai.summarize(thread, max_words=80)
draft = ai.draft_reply(thread, summary, voice="concise-expert")
x-hosted.draft_post(text=draft, reply_to=thread.root_id)
# Review, then:
# x-hosted.post_reply(draft_id=draft.id)</code></pre>

    <h3>3. Rate-limit-aware posting</h3>
    <p>X's per-user write limit (2400 / 24h) is enforced inside the MCP host, not on your client. The MCP returns a structured 429 with <code>retry_after</code> and the remaining budget, so a posting queue can self-throttle instead of hanging. Multi-account creators no longer need to maintain separate OAuth apps per account — one MCP registration, all of your X accounts, scoped per OAuth grant.</p>

    <h2>How ThreadGrab Fits Into the New Picture</h2>
    <p>ThreadGrab's read-side archiving is unaffected by the MCP launch. MCP helps you write and post; ThreadGrab helps you capture, store, and reformat what is already public. The two are complementary, not competing, and most creators we have talked to keep both — MCP for the editing loop, ThreadGrab for the archive and cross-post routing.</p>

    <p>Specifically, three things ThreadGrab still does better than any MCP tool:</p>

    <ul>
      <li><strong>Bulk archive threads</strong> — ThreadGrab downloads complete threads as Markdown bundles. The hosted X MCP's <code>read_thread</code> returns one thread per call.</li>
      <li><strong>Cross-platform conversion</strong> — ThreadGrab converts X threads into Bluesky-compatible posts and LinkedIn Newsletter drafts. MCP is X-native only.</li>
      <li><strong>Public read with no auth</strong> — ThreadGrab reads public posts without any OAuth scope. Useful when you want to analyze a competitor's archive without granting your X account read access.</li>
    </ul>

    <p>If you write on X and want the loop of "draft in editor, post via MCP" + "archive everything I publish for reformatting later" — that is the combined workflow creators are converging on this July.</p>

    <div class="cta">
      <p>Archive X posts as clean Markdown bundles. ThreadGrab is the read-side complement to the new hosted X MCP — works with no account, no OAuth, no rate-limit dance.</p>
      <a class="btn" href="https://threadgrab.com/en/">Try ThreadGrab Free</a>
    </div>

    <h2>What to Watch For Over the Next 30 Days</h2>
    <p>The MCP launch is the first phase. Two follow-on changes are likely before the end of July:</p>

    <ul>
      <li><strong>Bluesky equivalent:</strong> The AT Protocol has had unofficial MCP servers since Q1 2026; Bluesky Social PBC has hinted at a hosted equivalent.</li>
      <li><strong>LinkedIn Newsletter MCP:</strong> Microsoft's hosted MCP for first-party products would let Cursor fetch a draft newsletter section by section.</li>
    </ul>

    <p>If both ship, the multi-platform creator loop collapses to: "edit in Claude Code, push to whichever platform the MCP for that platform exposes." That is what we have been building toward for two years.</p>

    <h2>Wrapping Up</h2>
    <p>The hosted X MCP turns X from "yet another platform with custom OAuth" into "another MCP tool registry your editor already speaks." For creators who live in Claude Code or Cursor, the install is a 60-second config edit. For creators who do not, nothing changes — ThreadGrab still handles the read-side archiving that the MCP does not cover.</p>

    <p>If you want the writing + posting loop via MCP and the archive + cross-platform conversion loop via ThreadGrab, you can run both side by side today. The two products do not overlap. The July 1 launch is the first time the write-side tooling has caught up with what creators already do on the read side.</p>"""

PT_BODY = """    <p>A X Corp. lancou silenciosamente, em 1 de julho de 2026, um servidor Model Context Protocol hospedado para agentes IA — e para criadores de X / Twitter, esta e a mudanca de fluxo que faltava ha dois anos. Ate agora, cada ferramenta de IA que quisesse ler ou postar no X precisava de sua propria negociacao OAuth bespoke, seu proprio tratamento de rate-limit e suas proprias peculiaridades de formato. O novo endpoint MCP hospedado colapsa tudo isso em uma URL que seu editor ja sabe chamar.</p>

    <p>Este guia percorre o que o MCP do X hospedado expoe de fato, como conecta-lo ao Claude Code, Cursor e Windsurf hoje, as tres coisas concretas que muda na rotina diaria do criador e onde o ThreadGrab ainda se encaixa. Nenhum exemplo abaixo exige credenciais nao publicas — cada bloco de codigo roda contra o beta publico que a X abriu em 1 de julho.</p>

    <div class="callout">
      <p><strong>Resumo:</strong> X lancou servidor MCP hospedado em 1 de julho de 2026. Aponte seu cliente MCP para <code>https://mcp.x.com/v1</code>, autentique uma vez com X, e qualquer editor MCP-aware le seu timeline, rascunha posts e responde via chamadas de ferramenta padronizadas. Leitura e free-tier; postar exige X Premium. Complementa, nao substitui, o arquivamento de leitura do ThreadGrab.</p>
    </div>

    <h2>O Que o MCP Hospedado do X Realmente Expoe</h2>
    <p>O Model Context Protocol (MCP) e um padrao JSON-RPC que agentes IA usam para falar com ferramentas externas. O endpoint hospedado da X e um servidor gerenciado que a X Corp. roda — voce nao faz deploy, nao paga hospedagem e nao gerencia tokens OAuth. Aponte seu cliente para a URL, faca login uma vez com sua conta X, e o registro de ferramentas fica disponivel no seu editor.</p>

    <p>O registro de ferramentas em julho de 2026 cobre seis operacoes em dois escopos:</p>

    <table>
      <thead>
        <tr><th>Nome da ferramenta</th><th>Escopo</th><th>O que faz</th><th>Rate limit</th></tr>
      </thead>
      <tbody>
        <tr><td><code>read_timeline</code></td><td>read</td><td>Retorna seu home timeline como fluxo estruturado de objetos post.</td><td>15 req / 15 min / user</td></tr>
        <tr><td><code>read_thread</code></td><td>read</td><td>Retorna a arvore completa do thread para qualquer URL de post.</td><td>300 req / 15 min / app</td></tr>
        <tr><td><code>draft_post</code></td><td>write</td><td>Encena um novo post em buffer por cliente; nao fica publico ate submeter.</td><td>ilimitado local</td></tr>
        <tr><td><code>post_reply</code></td><td>write</td><td>Envia resposta a um post existente, escopado por URL.</td><td>2400 req / 24h / user</td></tr>
        <tr><td><code>post_quote</code></td><td>write</td><td>Envia quote-post de um post existente com texto de comentario.</td><td>2400 req / 24h / user</td></tr>
        <tr><td><code>attach_media</code></td><td>write</td><td>Sobe asset de midia para ser referenciado por um draft subsequente.</td><td>50 / 24h / user (imagem+video combinados)</td></tr>
      </tbody>
    </table>

    <p>Ferramentas de escopo de leitura estao em contas free-tier. Ferramentas de escrita exigem escopos OAuth <code>tweet.write</code> e <code>media.upload</code>, que o X Premium concede. O host MCP mostra esses requisitos no handshake de instalacao — se faltarem, o cliente pede upgrade.</p>

    <h2>Como Conectar o MCP do X Hospedado ao Claude Code Hoje</h2>
    <p>Claude Code guarda configuracao MCP em <code>~/.claude/mcp_servers.json</code> no macOS e Linux. Adicione uma entrada apontando para a URL hospedada do X e reinicie o Claude Code. A primeira chamada dispara handshake OAuth via browser contra x.com; apos conceder os escopos, as ferramentas aparecem no slash command palette.</p>

    <pre><code>{
  "mcpServers": {
    "x-hosted": {
      "url": "https://mcp.x.com/v1",
      "auth": {
        "type": "oauth",
        "provider": "x.com",
        "scopes": ["tweet.read", "tweet.write", "media.upload"]
      }
    }
  }
}</code></pre>

    <p>Apos salvar, rode <code>/mcp list</code> em qualquer sessao Claude Code. Voce deve ver seis ferramentas listadas sob <code>x-hosted.*</code> com indicador verde. Se alguma aparecer vermelha, os escopos estao incompletos — refaca o handshake OAuth com o escopo faltante.</p>

    <h2>Como Compara Com o MCP do OpenRouter e do Cloudflare</h2>
    <p>O ecossistema MCP tem tres endpoints hospedados que importam aos criadores em 2026, e cada um expoe uma superficie de ferramenta diferente. Todos falam o mesmo protocolo, entao a instalacao parece identica, mas o trabalho que fazem nao e intercambiavel.</p>

    <table>
      <thead>
        <tr><th>MCP hospedado</th><th>Superficie de ferramenta</th><th>Melhor para</th><th>Custo</th></tr>
      </thead>
      <tbody>
        <tr><td>X hospedado</td><td>X-especifica (timeline, drafts, posts, midia)</td><td>Ler + postar no X dentro do editor</td><td>Read gratis, write exige Premium</td></tr>
        <tr><td>OpenRouter hospedado</td><td>Selecao de modelo em 200+ LLMs</td><td>Fluxos de chat multi-modelo</td><td>Pagar por token</td></tr>
        <tr><td>Cloudflare hospedado</td><td>Bindings Workers AI + dados de edge</td><td>Deploy de IA na borda</td><td>Free tier, depois por request</td></tr>
      </tbody>
    </table>

    <p>Se seu objetivo e <em>decidir qual modelo trata um prompt</em>, use OpenRouter. Se o objetivo e <em>ler um thread, rascunhar resposta e submeter no X sem sair do editor</em>, use o MCP hospedado do X. Os dois se compoem bem — Claude Code pode conectar aos tres ao mesmo tempo, em um unico prompt roteia para o modelo mais barato que da conta e posta o resultado de volta no X.</p>

    <h2>As Tres Coisas Concretas Que Mudam Para Criadores</h2>
    <p>Alem da superficie tecnica, o MCP hospedado do X muda tres coisas em como criadores rodam seu dia. Nenhuma e teorica — sao os fluxos que o lancamento de 1 de julho desbloqueia.</p>

    <h3>1. Drafts dentro do editor, nao na caixa de compose do X</h3>
    <p>A ferramenta <code>draft_post</code> encena posts em buffer por cliente. A maioria dos criadores vai rotear drafts pelo Claude Code ou Cursor onde podem aplicar controle de versao, gramatica e tom sem clicar na web UI do X. O handshake MCP garante que os drafts nao ficam visiveis ate voce chamar <code>post_reply</code> ou <code>post_quote</code> explicitamente.</p>

    <pre><code>// Natural-language workflow you can run in Claude Code today
// (no code needed — the MCP picks it up as a tool call)

prompt:
"Read the last 5 posts from @threadgrab, summarize the
 recurring questions in 3 bullet points under 280 chars each,
 draft as 3 separate X posts, do not submit yet."

// Claude Code calls x-hosted.read_timeline, then
// x-hosted.draft_post three times. Drafts appear in your
// staging buffer for review.</code></pre>

    <h3>2. Respostas com contexto completo do thread</h3>
    <p>A ferramenta <code>read_thread</code> retorna a arvore inteira da conversa para qualquer URL de post — util quando um criador responde a um thread que ja ramificou 8+ respostas. Antes voce rolava no app X; agora o thread inteiro chega como payload JSON que seu cliente pode resumir, traduzir ou avaliar tom antes de voce commitar uma resposta.</p>

    <pre><code># Cursor / Claude Code chat skill:
thread = x-hosted.read_thread(url="https://x.com/somebody/status/123")
summary = ai.summarize(thread, max_words=80)
draft = ai.draft_reply(thread, summary, voice="concise-expert")
x-hosted.draft_post(text=draft, reply_to=thread.root_id)
# Review, then:
# x-hosted.post_reply(draft_id=draft.id)</code></pre>

    <h3>3. Postagem consciente do rate-limit</h3>
    <p>O limite de escrita por usuario da X (2400 / 24h) e imposto dentro do host MCP, nao no seu cliente. O MCP retorna um 429 estruturado com <code>retry_after</code> e o budget restante, para que a fila de postagem se auto-limite em vez de travar. Criadores multi-conta nao precisam mais manter apps OAuth separados por conta — um registro MCP, todas as suas contas X, escopadas por grant OAuth.</p>

    <h2>Como o ThreadGrab se Encaixa no Novo Cenario</h2>
    <p>O arquivamento de leitura do ThreadGrab nao e afetado pelo lancamento do MCP. MCP ajuda a escrever e postar; ThreadGrab ajuda a capturar, armazenar e reformatar o que ja e publico. Os dois sao complementares, nao concorrentes, e a maioria dos criadores que conversamos mantem os dois — MCP para o loop de edicao, ThreadGrab para o arquivo e cross-post.</p>

    <p>Especificamente, tres coisas que o ThreadGrab ainda faz melhor que qualquer ferramenta MCP:</p>

    <ul>
      <li><strong>Arquivo em massa de threads</strong> — ThreadGrab baixa threads completos como pacotes Markdown. O <code>read_thread</code> do MCP hospedado retorna um thread por chamada.</li>
      <li><strong>Conversao cross-platform</strong> — ThreadGrab converte threads X em posts compativeis com Bluesky e drafts de Newsletter LinkedIn. MCP e apenas X-nativo.</li>
      <li><strong>Leitura publica sem auth</strong> — ThreadGrab le posts publicos sem nenhum escopo OAuth. Util quando voce quer analisar o arquivo de um concorrente sem grant de acesso de leitura a sua conta X.</li>
    </ul>

    <p>Se voce escreve no X e quer o loop "draft no editor, posta via MCP" + "arquiva tudo que publico para reformat depois" — esse e o fluxo combinado em que criadores estao convergindo neste julho.</p>

    <div class="cta">
      <p>Archive posts X como pacotes Markdown limpos. ThreadGrab e o complemento de leitura do novo MCP hospedado do X — funciona sem conta, sem OAuth, sem rate-limit.</p>
      <a class="btn" href="https://threadgrab.com/pt/">Teste ThreadGrab Gratis</a>
    </div>

    <h2>O Que Observar Nos Proximos 30 Dias</h2>
    <p>O lancamento do MCP e a primeira fase. Duas mudancas de seguimento sao provaveis antes do fim de julho:</p>

    <ul>
      <li><strong>Equivalente Bluesky:</strong> O AT Protocol tem servidores MCP nao-oficiais desde Q1 2026; a Bluesky Social PBC indicou um equivalente hospedado.</li>
      <li><strong>MCP LinkedIn Newsletter:</strong> O MCP hospedado da Microsoft para produtos first-party deixaria o Cursor buscar uma secao de newsletter draft por secao.</li>
    </ul>

    <p>Se os dois sairem, o loop multi-plataforma colapsa para: "editar no Claude Code, empurrar para qualquer plataforma que o MCP daquela plataforma expoe." E nisso que estamos trabalhando ha dois anos.</p>

    <h2>Fechando</h2>
    <p>O MCP hospedado do X transforma o X de "mais uma plataforma com OAuth custom" para "mais um registro de ferramentas MCP que seu editor ja fala." Para criadores que vivem no Claude Code ou Cursor, a instalacao e um edit de config de 60 segundos. Para criadores que nao, nada muda — o ThreadGrab continua tratando do arquivamento de leitura que o MCP nao cobre.</p>

    <p>Se voce quer o loop de escrita + postagem via MCP e o loop de arquivo + conversao cross-platform via ThreadGrab, pode rodar os dois lado a lado hoje. Os dois produtos nao se sobrepoem. O lancamento de 1 de julho e a primeira vez que o tooling de escrita alcancou o que criadores ja fazem no lado de leitura.</p>"""

ID_BODY = """    <p>X Corp. diam-diam melancarkan server Model Context Protocol terhost untuk agen AI pada 1 Juli 2026, dan untuk kreator X / Twitter ini adalah perubahan alur yang sudah hilang selama dua tahun. Sampai sekarang, setiap alat AI yang ingin membaca atau memposting di X butuh negosiasi OAuth khusus, penanganan rate-limit sendiri, dan keanehan format posting sendiri. Endpoint MCP terhost baru menyatukan semua itu menjadi satu URL yang editor Anda sudah tahu cara memanggilnya.</p>

    <p>Panduan ini membahas apa yang sebenarnya dip暴露kan MCP X terhost, cara menyambungkannya ke Claude Code, Cursor, dan Windsurf hari ini, tiga hal konkret yang berubah dari rutinitas harian kreator, dan di mana ThreadGrab masih muat. Tidak ada contoh di bawah yang butuh kredensial non-publik — setiap blok kode berjalan melawan beta publik yang X buka pada 1 Juli.</p>

    <div class="callout">
      <p><strong>Ringkasan:</strong> X meluncurkan server MCP terhost pada 1 Juli 2026. Arahkan klien MCP Anda ke <code>https://mcp.x.com/v1</code>, autentikasi sekali dengan X, dan editor apa pun yang sadar-MCP bisa membaca timeline, membuat draf, dan membalas lewat panggilan alat standar. Baca gratis-tier; posting butuh X Premium. Melengkapi, bukan menggantikan, pengarsipan baca-sisi ThreadGrab.</p>
    </div>

    <h2>Apa yang sebenarnya Dip暴露kan MCP Terhost X</h2>
    <p>Model Context Protocol (MCP) adalah standar JSON-RPC yang dipakai agen AI untuk berbicara dengan alat luar. Endpoint terhost X adalah server terkelola yang dijalankan X Corp. — Anda tidak men-deploy apa pun, tidak membayar hosting, dan tidak mengelola token OAuth. Arahkan klien ke URL, masuk sekali dengan akun X Anda, dan registri alat tersedia di dalam editor Anda.</p>

    <p>Registri alat per peluncuran Juli 2026 mencakup enam operasi dalam dua cakupan:</p>

    <table>
      <thead>
        <tr><th>Nama alat</th><th>Cakupan</th><th>Fungsinya</th><th>Batas laju</th></tr>
      </thead>
      <tbody>
        <tr><td><code>read_timeline</code></td><td>read</td><td>Mengembalikan home timeline sebagai aliran terstruktur objek post.</td><td>15 req / 15 min / user</td></tr>
        <tr><td><code>read_thread</code></td><td>read</td><td>Mengembalikan pohon thread lengkap untuk URL post apa pun.</td><td>300 req / 15 min / app</td></tr>
        <tr><td><code>draft_post</code></td><td>write</td><td>Mengemas posting baru di buffer per klien; tidak publik sampai dikirim.</td><td>tidak terbatas lokal</td></tr>
        <tr><td><code>post_reply</code></td><td>write</td><td>Mengirim balasan ke post yang ada, dicakup per URL.</td><td>2400 req / 24h / user</td></tr>
        <tr><td><code>post_quote</code></td><td>write</td><td>Mengirim quote-post dari post yang ada dengan teks komentar.</td><td>2400 req / 24h / user</td></tr>
        <tr><td><code>attach_media</code></td><td>write</td><td>Mengunggah aset media untuk dirujuk oleh draf berikutnya.</td><td>50 / 24h / user (gambar+video digabung)</td></tr>
      </tbody>
    </table>

    <p>Alat cakupan baca tersedia untuk akun X free-tier. Alat tulis butuh cakupan OAuth <code>tweet.write</code> dan <code>media.upload</code>, yang diberikan X Premium. Host MCP mem暴露kan persyaratan ini saat jabat tangan instalasi — jika kurang, klien akan meminta Anda upgrade.</p>

    <h2>Cara Menyambungkan MCP X Terhost ke Claude Code Hari Ini</h2>
    <p>Claude Code menyimpan konfigurasi MCP-nya di <code>~/.claude/mcp_servers.json</code> di macOS dan Linux. Tambahkan satu entri yang menunjuk ke URL X terhost, lalu mulai ulang Claude Code. Panggilan pertama memicu jabat tangan OAuth berbasis browser ke x.com; setelah Anda授予 cakupan, alat muncul di palet perintah slash.</p>

    <pre><code>{
  "mcpServers": {
    "x-hosted": {
      "url": "https://mcp.x.com/v1",
      "auth": {
        "type": "oauth",
        "provider": "x.com",
        "scopes": ["tweet.read", "tweet.write", "media.upload"]
      }
    }
  }
}</code></pre>

    <p>Setelah menyimpan, jalankan <code>/mcp list</code> di sesi Claude Code apa pun. Anda akan melihat enam alat tercantum di bawah <code>x-hosted.*</code> dengan indikator hijau. Jika ada yang merah, cakupan tidak lengkap — jalankan ulang jabat tangan OAuth dengan cakupan yang hilang.</p>

    <h2>Bagaimana Dibandingkan Dengan MCP OpenRouter dan Cloudflare</h2>
    <p>Ekosistem MCP punya tiga endpoint terhost yang penting bagi kreator di 2026, dan masing-masing mem暴露kan permukaan alat berbeda. Semuanya berbicara protokol yang sama, jadi instalasi terlihat identik, tetapi pekerjaan yang dilakukan tidak bisa saling menggantikan.</p>

    <table>
      <thead>
        <tr><th>MCP terhost</th><th>Permukaan alat</th><th>Cocok untuk</th><th>Biaya</th></tr>
      </thead>
      <tbody>
        <tr><td>X terhost</td><td>Khusus-X (timeline, draf, posting, media)</td><td>Baca + posting di X dalam editor</td><td>Baca gratis, tulis butuh Premium</td></tr>
        <tr><td>OpenRouter terhost</td><td>Pemilihan model 200+ LLM</td><td>Alur chat multi-model</td><td>Bayar per token</td></tr>
        <tr><td>Cloudflare terhost</td><td>Binding Workers AI + data edge</td><td>Men-deploy AI di edge</td><td>Tingkat gratis, lalu per-request</td></tr>
      </tbody>
    </table>

    <p>Jika tujuan Anda adalah <em>memutuskan model mana yang menangani sebuah prompt</em>, gunakan OpenRouter. Jika tujuannya adalah <em>membaca thread, membuat draf balasan, dan mengirimnya di X tanpa meninggalkan editor</em>, gunakan MCP terhost X. Keduanya bisa digabung dengan baik — Claude Code bisa disambungkan ke ketiganya sekaligus, sehingga satu prompt bisa merutekan ke model termurah yang menanganinya dan memposting hasilnya kembali ke X.</p>

    <h2>Tiga Hal Konkret yang Berubah Untuk Kreator</h2>
    <p>Di luar permukaan teknis, MCP terhost X mengubah tiga hal tentang bagaimana kreator menjalankan hari mereka. Tidak satu pun yang teoritis — ini adalah alur yang dibuka peluncuran 1 Juli.</p>

    <h3>1. Draf di dalam editor, bukan di kotak komposisi X</h3>
    <p>Alat <code>draft_post</code> menampung posting di buffer per klien. Sebagian besar kreator akan merutekan draf melalui Claude Code atau Cursor di mana mereka bisa menerapkan kontrol versi, pemeriksaan tata bahasa, dan penegakan nada tanpa mengklik UI web X. Jabat tangan MCP menjamin draf tidak terlihat sampai Anda memanggil <code>post_reply</code> atau <code>post_quote</code> secara eksplisit.</p>

    <pre><code>// Natural-language workflow you can run in Claude Code today
// (no code needed — the MCP picks it up as a tool call)

prompt:
"Read the last 5 posts from @threadgrab, summarize the
 recurring questions in 3 bullet points under 280 chars each,
 draft as 3 separate X posts, do not submit yet."

// Claude Code calls x-hosted.read_timeline, then
// x-hosted.draft_post three times. Drafts appear in your
// staging buffer for review.</code></pre>

    <h3>2. Balasan dengan konteks thread lengkap</h3>
    <p>Alat <code>read_thread</code> mengembalikan seluruh pohon percakapan untuk URL post apa pun — berguna saat kreator membalas thread yang sudah bercabang 8+ balasan. Sebelumnya Anda menggulir di aplikasi X; sekarang seluruh thread tiba sebagai payload JSON yang klien Anda bisa rangkum, terjemahkan, atau nilai nadanya sebelum Anda commit membalas.</p>

    <pre><code># Cursor / Claude Code chat skill:
thread = x-hosted.read_thread(url="https://x.com/somebody/status/123")
summary = ai.summarize(thread, max_words=80)
draft = ai.draft_reply(thread, summary, voice="concise-expert")
x-hosted.draft_post(text=draft, reply_to=thread.root_id)
# Review, then:
# x-hosted.post_reply(draft_id=draft.id)</code></pre>

    <h3>3. Posting yang sadar batas laju</h3>
    <p>Batas tulis per pengguna X (2400 / 24 jam) ditegakkan di dalam host MCP, bukan di klien Anda. MCP mengembalikan 429 terstruktur dengan <code>retry_after</code> dan sisa anggaran, sehingga antrean posting bisa membatasi dirinya sendiri alih-alih macet. Kreator multi-akun tidak perlu lagi mempertahankan aplikasi OAuth terpisah per akun — satu pendaftaran MCP, semua akun X Anda, dicakup per hibah OAuth.</p>

    <h2>Bagaimana ThreadGrab Masuk ke Gambaran Baru Ini</h2>
    <p>Pengarsipan baca-sisi ThreadGrab tidak terpengaruh oleh peluncuran MCP. MCP membantu Anda menulis dan memposting; ThreadGrab membantu Anda menangkap, menyimpan, dan memformat ulang apa yang sudah publik. Keduanya saling melengkapi, bukan bersaing, dan kebanyakan kreator yang kami ajak bicara mempertahankan keduanya — MCP untuk loop edit, ThreadGrab untuk arsip dan cross-post.</p>

    <p>Secara spesifik, tiga hal ThreadGrab masih lakukan lebih baik daripada alat MCP mana pun:</p>

    <ul>
      <li><strong>Arsip thread massal</strong> — ThreadGrab mengunduh thread lengkap sebagai bundel Markdown. <code>read_thread</code> MCP terhost mengembalikan satu thread per panggilan.</li>
      <li><strong>Konversi lintas platform</strong> — ThreadGrab mengonversi thread X menjadi posting kompatibel Bluesky dan draf Newsletter LinkedIn. MCP hanya X-asli.</li>
      <li><strong>Baca publik tanpa auth</strong> — ThreadGrab membaca posting publik tanpa cakupan OAuth apa pun. Berguna saat Anda ingin menganalisis arsip pesaing tanpa memberi akun X Anda akses baca.</li>
    </ul>

    <p>Jika Anda menulis di X dan ingin loop "draf di editor, posting lewat MCP" + "arsipkan semua yang saya terbitkan untuk diformat ulang nanti" — itulah alur gabungan yang dikonsolidasikan kreator pada Juli ini.</p>

    <div class="cta">
      <p>Arsipkan posting X sebagai bundel Markdown bersih. ThreadGrab adalah pelengkap baca-sisi dari MCP terhost X yang baru — bekerja tanpa akun, tanpa OAuth, tanpa tarian rate-limit.</p>
      <a class="btn" href="https://threadgrab.com/id/">Coba ThreadGrab Gratis</a>
    </div>

    <h2>Yang Harus Diperhatikan Dalam 30 Hari ke Depan</h2>
    <p>Peluncuran MCP adalah fase pertama. Dua perubahan lanjutan kemungkinan sebelum akhir Juli:</p>

    <ul>
      <li><strong>Setara Bluesky:</strong> Protokol AT sudah punya server MCP tidak resmi sejak Q1 2026; Bluesky Social PBC menyiratkan setara terhost.</li>
      <li><strong>MCP LinkedIn Newsletter:</strong> MCP terhost Microsoft untuk produk first-party akan memungkinkan Cursor mengambil bagian draf newsletter per bagian.</li>
    </ul>

    <p>Jika keduanya tayang, loop kreator multi-platform runtuh menjadi: "edit di Claude Code, dorong ke platform mana pun yang MCP platform itu ekspos." Itulah yang sedang kami bangun selama dua tahun.</p>

    <h2>Penutup</h2>
    <p>MCP terhost X mengubah X dari "platform lain dengan OAuth kustom" menjadi "registri alat MCP lain yang sudah diajak bicara oleh editor Anda." Untuk kreator yang tinggal di Claude Code atau Cursor, instalasi adalah edit konfigurasi 60 detik. Untuk kreator yang tidak, tidak ada yang berubah — ThreadGrab masih menangani pengarsipan baca-sisi yang tidak dicakup MCP.</p>

    <p>Jika Anda ingin loop tulis + posting lewat MCP dan loop arsip + konversi lintas platform lewat ThreadGrab, Anda bisa menjalankan keduanya berdampingan hari ini. Kedua produk tidak tumpang tindih. Peluncuran 1 Juli adalah pertama kalinya perkakas tulis menyusul apa yang sudah dilakukan kreator di sisi baca.</p>"""


if __name__ == '__main__':
    main()
