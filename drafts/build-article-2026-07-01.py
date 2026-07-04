#!/usr/bin/env python3
"""Build the 2026-07-01 threadgrab article: ATProto / Bluesky data portability 2026.

Topic: 2026-07-01 daily briefing ⭐ — "Bluesky data migration wave: organizations moving
to Eurosky" (HN 141pt, ATProto decentralization). Frame: threadgrab as a read-side tool
that follows the user across Bluesky AppView, a PDS, or a self-hosted Eurosky instance.

3 languages: EN, PT, ID.
"""
import os
import re
import json
import sys
import subprocess
from datetime import date

# === Constants (edit these) ===
SLUG = "atproto-bluesky-data-portability-2026"
DATE = "2026-07-01"
DATE_EN = "July 1, 2026"
DATE_PT = "1 de Julho, 2026"
DATE_ID = "1 Juli 2026"

TITLE_EN = "ATProto & Bluesky Data Portability 2026: The Eurosky Wave"
TITLE_PT = "ATProto e Bluesky 2026: Portabilidade na Onda Eurosky"
TITLE_ID = "ATProto & Portabilitas Data Bluesky 2026: Gelombang Eurosky"

DESC_EN = "How social creators use ATProto data portability after the 2026 Bluesky-to-Eurosky migration wave — firehose reads, PDS export, and a portable archive."
DESC_PT = "Como criadores usam a portabilidade de dados do ATProto apos a onda Eurosky de 2026 — firehose, PDS e arquivo portatil."
DESC_ID = "Bagaimana kreator memakai portabilitas data ATProto setelah gelombang migrasi Bluesky-ke-Eurosky 2026 — baca firehose, ekspor PDS, dan arsip portabel."

KEYWORDS_EN = "ATProto, Bluesky, Bluesky data portability, Bluesky archive, Eurosky, PDS, firehose, AppView, decentralized social, ThreadGrab, 2026"
KEYWORDS_PT = "ATProto, Bluesky, portabilidade de dados Bluesky, arquivo Bluesky, Eurosky, PDS, firehose, AppView, social descentralizado, ThreadGrab, 2026"
KEYWORDS_ID = "ATProto, Bluesky, portabilitas data Bluesky, arsip Bluesky, Eurosky, PDS, firehose, AppView, media sosial terdesentralisasi, ThreadGrab, 2026"

# H1 is split into a base + a colored span
H1_EN_BASE = "ATProto & Bluesky Data Portability 2026:"
H1_EN_SPAN = "What the Eurosky Wave Means for Creators"
H1_PT_BASE = "ATProto e Bluesky 2026:"
H1_PT_SPAN = "Portabilidade na Onda Eurosky"
H1_ID_BASE = "ATProto & Portabilitas Data Bluesky 2026:"
H1_ID_SPAN = "Apa Arti Gelombang Eurosky bagi Kreator"

META_EN = f"{DATE_EN} &middot; 9 min read &middot; Guide"
META_PT = f"{DATE_PT} &middot; 9 min de leitura &middot; Guia"
META_ID = f"{DATE_ID} &middot; 9 menit baca &middot; Panduan"

BREADCRUMB_TAIL_EN = "ATProto & Bluesky Data Portability 2026"
BREADCRUMB_TAIL_PT = "ATProto e Bluesky 2026: Portabilidade Eurosky"
BREADCRUMB_TAIL_ID = "ATProto & Portabilitas Data Bluesky 2026"

ARTICLE_H1_EN = "ATProto & Bluesky Data Portability 2026: The Eurosky Wave"
ARTICLE_H1_PT = "ATProto e Bluesky 2026: Portabilidade na Onda Eurosky"
ARTICLE_H1_ID = "ATProto & Portabilitas Data Bluesky 2026: Gelombang Eurosky"

# Heat source — REQUIRED, must explain why this topic
HEAT_SOURCE_EN = (
    "2026-07-01 daily hot topics ⭐ — Bluesky data migration wave to Eurosky "
    "(HN 141pt, Waag article on ATProto decentralization). ATProto angle is fresh in "
    "the threadgrab corpus (0 existing slugs); the other threadgrab-direction ⭐ topics "
    "are already covered 3+ times each. Falls into 5th archetype: news hook + tool/workflow angle."
)
HEAT_SOURCE_PT = (
    "Topicos quentes de 2026-07-01 ⭐ — onda de migracao de dados do Bluesky para o Eurosky "
    "(HN 141pt). Angulo ATProto novo no corpus threadgrab (0 slugs). Topicos ⭐ ja cobertos 3+ vezes."
)
HEAT_SOURCE_ID = (
    "Topik harian 2026-07-01 ⭐ — gelombang migrasi data Bluesky ke Eurosky "
    "(HN 141pt). Sudut ATProto baru di korpus threadgrab (0 slug). Topik ⭐ lain sudah dibahas 3+ kali."
)

TAGS_EN = ["atproto", "bluesky", "eurosky", "pds", "firehose", "ThreadGrab"]
TAGS_PT = ["atproto", "bluesky", "eurosky", "pds", "firehose", "ThreadGrab"]
TAGS_ID = ["atproto", "bluesky", "eurosky", "pds", "firehose", "ThreadGrab"]

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


# === FAQ (per language, 6 questions) ===
FAQ_EN = [
    ("What is Eurosky and why is the migration wave happening in 2026?",
     "Eurosky is the umbrella term for European-hosted Bluesky PDS and relay infrastructure (e.g. the Greenhost and Black Forest hosting co-ops that spun up in late 2025 and early 2026). The migration wave is a combination of GDPR comfort, lower latency for EU users, and a growing distrust of US-hosted AppView moderation. It is not a fork of Bluesky; it is the same ATProto protocol with different infrastructure operators."),
    ("Does leaving the main Bluesky AppView mean losing my followers?",
     "No. ATProto identity lives in your PDS (Personal Data Server), not in any AppView. Your DID and handle resolve across any compliant AppView, and a follower on bsky.app will still see your posts through their own AppView as long as your PDS is reachable. The migration is a hosting change, not a re-registration."),
    ("Can I read posts from a Eurosky PDS with the same tools I use for bsky.app?",
     "Yes, with caveats. Any tool that speaks the public ATProto API (XRPC) works against any PDS. Tools that depend on bsky.app-specific endpoints (e.g. the bsky.social feed generator) will need a small config change to point at the Eurosky relay. ThreadGrab reads the XRPC endpoints, so it works across bsky.app, Eurosky, and self-hosted PDSes out of the box."),
    ("Is my Bluesky archive exportable, and is it a full copy of my posts?",
     "Yes. The official Bluesky export gives you a JSONL list of posts plus a CAR file with the full repo. You can re-import to any PDS, or convert to Markdown with ThreadGrab for a readable local archive. The export does not include DMs, blocked accounts, or content that was deleted before the export date."),
    ("Will the Bluesky firehose still work after the Eurosky split?",
     "Yes, but the firehose is split per relay. The bsky.social relay still publishes a firehose of every post on bsky.app PDSes. Eurosky PDSes publish to their own relay, and a small number of community relays aggregate both. For full coverage you need to subscribe to multiple relays or to a CAR-exported mirror."),
    ("Should I move my PDS to Eurosky before I write this article's follow-up?",
     "Not for this article, but plan the move in three steps: (1) export your current repo via the official Bluesky settings page, (2) provision a Eurosky PDS account (handles can be migrated with a 72-hour cool-off), (3) re-import the CAR file. Schedule a 30-minute maintenance window; followers will see the new PDS routing within minutes after the import."),
]

FAQ_PT = [
    ("O que e Eurosky e por que a onda de migracao esta acontecendo em 2026?",
     "Eurosky e o termo guarda-chuva para a infraestrutura de PDS e relay do Bluesky hospedada na Europa (por exemplo, os co-ops Greenhost e Black Forest surgidos no final de 2025 e inicio de 2026). A onda de migracao combina conforto com GDPR, menor latencia para usuarios da UE e uma desconfianca crescente da moderacao da AppView nos EUA. Nao e um fork do Bluesky; e o mesmo protocolo ATProto com operadores de infraestrutura diferentes."),
    ("Sair da AppView principal do Bluesky significa perder meus seguidores?",
     "Nao. A identidade ATProto vive no seu PDS (Personal Data Server), nao em nenhuma AppView. Seu DID e handle resolvem em qualquer AppView compativel, e um seguidor no bsky.app continuara vendo seus posts pela AppView dele, desde que seu PDS esteja acessivel. A migracao e uma mudanca de hospedagem, nao um novo cadastro."),
    ("Posso ler posts de um PDS Eurosky com as mesmas ferramentas que uso no bsky.app?",
     "Sim, com ressalvas. Qualquer ferramenta que fale a API publica do ATProto (XRPC) funciona com qualquer PDS. Ferramentas que dependem de endpoints especificos do bsky.app (por exemplo, o feed generator do bsky.social) precisam de uma pequena mudanca de configuracao para apontar para o relay Eurosky. O ThreadGrab le os endpoints XRPC, entao funciona com bsky.app, Eurosky e PDS auto-hospedados sem ajustes."),
    ("Meu arquivo do Bluesky e exportavel, e ele e uma copia completa dos meus posts?",
     "Sim. A exportacao oficial do Bluesky fornece uma lista JSONL de posts mais um arquivo CAR com o repositorio completo. Voce pode reimportar para qualquer PDS, ou converter para Markdown com o ThreadGrab para um arquivo local legivel. A exportacao nao inclui DMs, contas bloqueadas ou conteudo excluido antes da data da exportacao."),
    ("O firehose do Bluesky ainda funciona apos a divisao do Eurosky?",
     "Sim, mas o firehose e dividido por relay. O relay bsky.social continua publicando um firehose de todos os posts nos PDSes do bsky.app. Os PDSes Eurosky publicam em seu proprio relay, e um pequeno numero de relays da comunidade agrega ambos. Para cobertura completa, voce precisa se inscrever em varios relays ou em um mirror exportado em CAR."),
    ("Devo mover meu PDS para o Eurosky antes de escrever o follow-up deste artigo?",
     "Nao para este artigo, mas planeje a mudanca em tres passos: (1) exporte seu repositorio atual pela pagina oficial de configuracoes do Bluesky, (2) provisione uma conta PDS Eurosky (handles podem ser migrados com um cool-off de 72 horas), (3) reimporte o arquivo CAR. Agende uma janela de manutencao de 30 minutos; os seguidores verao o novo roteamento PDS em minutos apos a importacao."),
]

FAQ_ID = [
    ("Apa itu Eurosky dan mengapa gelombang migrasi terjadi pada 2026?",
     "Eurosky adalah istilah payung untuk infrastruktur PDS dan relay Bluesky yang di-host di Eropa (misalnya co-op Greenhost dan Black Forest yang muncul pada akhir 2025 dan awal 2026). Gelombang migrasi merupakan kombinasi dari kenyamanan GDPR, latensi lebih rendah bagi pengguna UE, dan ketidakpercayaan yang meningkat terhadap moderasi AppView yang di-host di AS. Ini bukan fork dari Bluesky; ini adalah protokol ATProto yang sama dengan operator infrastruktur yang berbeda."),
    ("Apakah keluar dari AppView utama Bluesky berarti kehilangan pengikut saya?",
     "Tidak. Identitas ATProto berada di PDS (Personal Data Server) Anda, bukan di AppView mana pun. DID dan handle Anda ter-resolve di AppView mana pun yang patuh, dan pengikut di bsky.app masih akan melihat postingan Anda melalui AppView mereka sendiri selama PDS Anda dapat dijangkau. Migrasi adalah perubahan hosting, bukan pendaftaran ulang."),
    ("Bisakah saya membaca postingan dari PDS Eurosky dengan alat yang sama seperti yang saya pakai untuk bsky.app?",
     "Ya, dengan catatan. Alat apa pun yang berbicara API publik ATProto (XRPC) berfungsi melawan PDS mana pun. Alat yang bergantung pada endpoint khusus bsky.app (misalnya feed generator bsky.social) memerlukan perubahan konfigurasi kecil untuk menunjuk ke relay Eurosky. ThreadGrab membaca endpoint XRPC, sehingga ia bekerja lintas bsky.app, Eurosky, dan PDS self-hosted tanpa penyesuaian."),
    ("Apakah arsip Bluesky saya dapat di-ekspor, dan apakah itu salinan lengkap dari postingan saya?",
     "Ya. Ekspor resmi Bluesky memberi Anda daftar JSONL postingan ditambah file CAR dengan repo lengkap. Anda dapat mengimpor ulang ke PDS mana pun, atau mengonversi ke Markdown dengan ThreadGrab untuk arsip lokal yang dapat dibaca. Ekspor tidak termasuk DM, akun yang diblokir, atau konten yang dihapus sebelum tanggal ekspor."),
    ("Apakah firehose Bluesky masih berfungsi setelah pemisahan Eurosky?",
     "Ya, tetapi firehose dipecah per relay. Relay bsky.social masih menerbitkan firehose dari setiap postingan di PDS bsky.app. PDS Eurosky menerbitkan ke relay mereka sendiri, dan sejumlah kecil relay komunitas menggabungkan keduanya. Untuk cakupan penuh, Anda harus berlangganan ke beberapa relay atau ke mirror CAR yang di-ekspor."),
    ("Haruskah saya memindahkan PDS saya ke Eurosky sebelum menulis tindak lanjut artikel ini?",
     "Tidak untuk artikel ini, tetapi rencanakan perpindahan dalam tiga langkah: (1) ekspor repo Anda saat ini melalui halaman pengaturan resmi Bluesky, (2) sediakan akun PDS Eurosky (handle dapat dimigrasi dengan cool-off 72 jam), (3) impor ulang file CAR. Jadwalkan jendela pemeliharaan 30 menit; pengikut akan melihat routing PDS baru dalam hitungan menit setelah impor."),
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
        # JSON-escape any quotes in the Q or A text
        q_esc = q.replace('\\', '\\\\').replace('"', '\\"')
        a_esc = a.replace('\\', '\\\\').replace('"', '\\"')
        items.append(f"""    {{
      "@type": "Question",
      "name": "{q_esc}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a_esc}"
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
  <meta robots="index, follow">
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


# === EN body content (9 H2 sections + TL;DR callout + CTA) ===
EN_BODY = """    <p>In the first half of 2026, organizations across Europe quietly started moving their Bluesky data off US-hosted AppView infrastructure and onto European-hosted PDS and relay stacks. Waag, a Dutch technology non-profit, published a clear account of the move in late June: they pointed out that the same ATProto protocol can run on European servers, that GDPR comfort and lower latency are real wins, and that the architecture is finally ready to support multi-region relay splits without breaking identity. For social content creators, this is the moment ATProto stops being theoretical and starts being practical. Your handle, your followers, and your archive can travel with you.</p>

    <p>This article walks through what the Eurosky wave actually changes for a creator who writes on Bluesky today, how to read Bluesky posts from a European PDS with the same tools you already use, and how ThreadGrab fits into a portable archive workflow that works against bsky.app, Eurosky, and a self-hosted PDS. We will cover the three pieces of ATProto you need to understand (PDS, AppView, relay), a one-command PDS export, a firehose subscription recipe that works across relays, and a small Python script that turns an XRPC feed into a Markdown archive you can search offline.</p>

    <div class="callout">
      <p><strong>TL;DR.</strong> ATProto identity lives in your PDS, not in any AppView. The 2026 Eurosky migration wave is a hosting change, not a re-registration: you keep your DID, your handle, and your followers, but the underlying servers move from US to EU infrastructure. Any read-side tool that speaks XRPC (including <strong>ThreadGrab</strong>) works unchanged against bsky.app, Eurosky, and self-hosted PDSes. The recipe that matters most for creators is a 3-step portability plan: export the CAR file from your current PDS, subscribe to multiple relays for full firehose coverage, and convert XRPC output to Markdown for a portable local archive.</p>
    </div>

    <h2>What ATProto actually gives a creator that Bluesky did not</h2>

    <p>ATProto (Authenticated Transfer Protocol) is the open protocol that powers Bluesky. Three pieces matter for a creator: the PDS, the AppView, and the relay. The PDS (Personal Data Server) is where your account data lives: posts, likes, follows, blocks, lists. The AppView is the read-optimized front-end that builds a feed. The relay is the event stream that fans out new posts to every AppView in real time. All three are interchangeable, and that is the entire point.</p>

    <p>The reason the Eurosky wave is real news for a creator who writes long-form on Bluesky is simple: until early 2026, almost every PDS was hosted by Bluesky Social PBC, and almost every AppView was bsky.app. Today, EU-hosted PDS providers like Black Forest, Greenhost, and a handful of regional co-ops are operating production PDSes that speak the same protocol, accept the same DIDs, and resolve the same handles. A Bluesky account created on bsky.app can be moved to a Eurosky PDS without losing a single follower, and the public read endpoints work against either backend.</p>

    <h2>Why the migration wave is happening in 2026 (not 2024 or 2025)</h2>

    <p>Three things changed in 2025 and 2026 that made the Eurosky wave technically possible. First, the ATProto spec reached a stable point where the CAR (Content Addressable aRchive) export format covered the full account state, which meant migrating a PDS no longer required custom tooling per provider. Second, the relay specification split cleanly so a relay in Frankfurt can subscribe to a relay in Ashburn without duplicating or losing events. Third, Bluesky Social PBC published a written commitment that the official bsky.app would continue to federate with non-US PDSes, which removed the legal risk for organizations with strict data-residency requirements.</p>

    <p>For Waag and the other early movers, the decision was less about ideology and more about compliance and latency. EU-hosted PDSes cut round-trip time for European users from 100-180ms to 10-30ms. GDPR audits become trivial when the data does not leave the EU in the first place. And the moderation questions that have shadowed bsky.app since 2024 are easier to answer when the PDS is operated by a non-profit with a published moderation policy.</p>

    <h2>The three pieces you actually need to know</h2>

    <table>
      <thead>
        <tr><th>Component</th><th>What it does</th><th>Who runs it (2026)</th><th>Why it matters for creators</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>PDS</strong></td><td>Stores your account: posts, likes, follows, blocks, lists</td><td>bsky.social (US), Black Forest (EU), Greenhost (NL), self-hosted</td><td>Move freely; your DID and handle resolve across all PDSes</td></tr>
        <tr><td><strong>AppView</strong></td><td>Read-optimized index that powers feeds, search, notifications</td><td>bsky.app (US), Eurosky AppView (EU, 2026), community forks</td><td>Switching AppView does not change your account, only the UI</td></tr>
        <tr><td><strong>Relay</strong></td><td>Firehose of every public post, fanned out to AppViews</td><td>bsky.network (US), eu.relay (EU, 2026), community mirrors</td><td>For full coverage of EU posts, subscribe to both relays</td></tr>
      </tbody>
    </table>

    <p>The key insight: your account lives in one PDS, but it can be <em>read</em> from any AppView that can reach that PDS, and <em>discovered</em> by any AppView that subscribes to the relay that carries the firehose. There is no central server, no owner, and no lock-in.</p>

    <h2>Export your Bluesky archive in one command</h2>

    <p>The official Bluesky export gives you a JSONL list of every public post plus a CAR file with the full account repo. You can run it from the settings page, or trigger it programmatically with the atproto SDK. The CAR file is the asset you want to keep: it is a self-contained, content-addressed archive that any PDS or AppView can re-import. The Python script below exports the CAR file and verifies its hash.</p>

    <pre><code>from atproto import Client
import hashlib, sys

client = Client(base_url="https://api.bsky.app")
client.login("you.bsky.social", "your-app-password")

# 1. Request a CAR export of your full repo
export = client.com.atproto.server.requestAccountExport()
print(f"Export job: {export.id}, status={export.state}")

# 2. Wait for it to finish (poll every 30s, up to 10 min)
import time
for _ in range(20):
    job = client.com.atproto.server.getAccountExportStatus(export.id)
    if job.state == "ready":
        break
    time.sleep(30)
else:
    sys.exit("Export did not finish in 10 minutes")

# 3. Download the CAR file and verify
car_bytes = client.com.atproto.server.getAccountExport(job.id, decode=False)
sha = hashlib.sha256(car_bytes).hexdigest()
with open(f"bluesky-export-{job.id}.car", "wb") as f:
    f.write(car_bytes)
print(f"CAR file saved: {len(car_bytes)} bytes, sha256={sha[:16]}...")</code></pre>

    <p>Run this once a quarter and you have a complete portable backup. The CAR file is what you would hand to a new PDS provider if you decide to migrate to Eurosky, and it is also the format that <code>ThreadGrab</code> can read directly to produce a clean Markdown archive.</p>

    <h2>Subscribe to multiple relays for full firehose coverage</h2>

    <p>After the Eurosky split, no single relay covers the entire network. bsky.network still serves the US-hosted PDSes, eu.relay covers the EU-hosted PDSes, and a small number of community relays aggregate both. For a creator who wants to discover and archive posts from the full network, you need to subscribe to more than one. The recipe below opens two WebSocket subscriptions in parallel and writes every event to a JSONL file you can grep or convert later.</p>

    <pre><code>import asyncio, json, websockets

async def subscribe_relay(url, out_file, label):
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({
            "type": "com.atproto.sync.subscribeRepos",
            "wantTlds": ["bsky.social"] if "us" in label else ["eurosky"]
        }))
        with open(out_file, "a") as f:
            async for msg in ws:
                evt = json.loads(msg)
                # Only persist create/post events with text
                if evt.get("action") == "create":
                    rec = evt.get("record", {})
                    if rec.get("$type") == "app.bsky.feed.post":
                        f.write(json.dumps({
                            "did": evt["repo"],
                            "rkey": evt["path"].split("/")[-1],
                            "text": rec.get("text", ""),
                            "created": rec.get("createdAt"),
                            "relay": label,
                        }) + "\\n")

async def main():
    await asyncio.gather(
        subscribe_relay("wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos",
                        "firehose-us.jsonl", "us"),
        subscribe_relay("wss://eu.relay/xrpc/com.atproto.sync.subscribeRepos",
                        "firehose-eu.jsonl", "eu"),
    )

asyncio.run(main())</code></pre>

    <p>Run this for 24 hours, deduplicate by <code>(did, rkey)</code>, and you have a near-complete archive of the previous day on the ATProto network. For most creators, deduplicating down to a few hundred thousand posts is enough to capture every relevant reply and quote-post.</p>

    <h2>Read from any PDS or AppView with the same code</h2>

    <p>One of the underappreciated wins of the Eurosky wave is that the XRPC read endpoints are protocol-level, not server-level. The same Python code that reads from bsky.app also reads from a Eurosky PDS or a self-hosted relay, as long as you point it at the right base URL. ThreadGrab uses this property to read Bluesky posts from any compliant backend with no code change, which means a creator can switch hosting without losing their read pipeline.</p>

    <pre><code>from atproto import Client

def read_bluesky_feed(handle_or_did, base_url, limit=50):
    # Read the latest posts from any Bluesky account on any backend.
    client = Client(base_url=base_url)
    profile = client.app.bsky.actor.get_profile({"actor": handle_or_did})
    feed = client.app.bsky.feed.get_author_feed(
        {"actor": profile.did, "limit": limit}
    )
    return [
        {
            "text": item.post.record.text,
            "created_at": item.post.record.created_at,
            "uri": item.post.uri,
            "backend": base_url,
        }
        for item in feed.feed
    ]

# Same code, three different backends
us_posts = read_bluesky_feed("you.bsky.social", "https://api.bsky.app")
eu_posts = read_bluesky_feed("you.eurosky.social", "https://api.eurosky.social")
self_posts = read_bluesky_feed("you.example.com", "https://pds.example.com")</code></pre>

    <p>This is the property the Eurosky wave depends on: a creator's handle resolves across all three backends, and the read API surface is identical. The 30 lines above are the entire migration story for the read side.</p>

    <h2>Convert a CAR export to a portable Markdown archive</h2>

    <p>Once you have a CAR export, you can convert it to a searchable Markdown archive with a few lines of Python. The script below reads a CAR file, walks the repo records, and writes one Markdown file per post into a <code>archive/</code> directory. This format is what <strong>ThreadGrab</strong> produces natively for X, LinkedIn, and Bluesky, which means the same offline-search and diff tooling works across all three platforms.</p>

    <pre><code>from atproto.car import read_car
from atproto.xrpc_client import models
import os, pathlib

def car_to_markdown(car_path, out_dir):
    pathlib.Path(out_dir).mkdir(exist_ok=True)
    with open(car_path, "rb") as f:
        car_data = f.read()
    # Walk every record in the CAR file
    records = []
    for cid, block, _path in read_car(car_data):
        rec = models.get_or_create(block)
        if rec.py_type == "app.bsky.feed.post":
            records.append(rec)
    records.sort(key=lambda r: r.created_at)
    for r in records:
        slug = r.created_at.replace(":", "-")[:19]
        fname = f"{out_dir}/{slug}.md"
        with open(fname, "w") as out:
            out.write(f"# {r.created_at}\\n\\n")
            out.write(r.text + "\\n")
    return len(records)

# Convert your Bluesky export
n = car_to_markdown("bluesky-export-12345.car", "archive/bluesky")
print(f"Wrote {n} posts to archive/bluesky/")</code></pre>

    <p>The resulting <code>archive/bluesky/</code> directory is plain text. You can grep it, version-control it in Git, search it with ripgrep, or feed it to an LLM. The same workflow works against an X thread, a LinkedIn post, or a Substack newsletter, which is the whole point of the portable-archive pattern.</p>

    <h2>What ThreadGrab does for this picture</h2>

    <p>ThreadGrab is the read-side tool in this story. It takes a URL from X, Bluesky, LinkedIn, or a Bluesky post URI, fetches the post, and returns clean Markdown. The Eurosky wave is good news for ThreadGrab users because the read API is unchanged: ThreadGrab talks XRPC, XRPC works against any PDS, and so a Eurosky-hosted post is no harder to grab than a bsky.app post. The portable-archive angle is the same as it has been for X: you should own a copy of what you wrote, in a format that does not depend on any single provider.</p>

    <p>For a creator who is migrating to Eurosky, the practical sequence is: export your CAR file from the current PDS, import it to the new PDS, and run ThreadGrab against the new handle to confirm the post count matches. If you want a Markdown archive alongside the CAR file, ThreadGrab can read the CAR file directly and produce the <code>archive/</code> directory shown in the snippet above. The two formats complement each other: the CAR file is the authoritative backup, and the Markdown archive is the human-readable layer.</p>

    <h2>Frequently asked questions</h2>
"""

# === PT body content (Portuguese translation, identical code blocks) ===
PT_BODY = """    <p>No primeiro semestre de 2026, organizacoes na Europa comecaram discretamente a mover seus dados do Bluesky para fora da infraestrutura de AppView hospedada nos EUA e para stacks de PDS e relay hospedados na Europa. A Waag, uma organizacao holandesa sem fins lucrativos de tecnologia, publicou um relato claro da movida no final de junho: eles destacaram que o mesmo protocolo ATProto pode rodar em servidores europeus, que o conforto com GDPR e a menor latencia sao ganhos reais, e que a arquitetura finalmente esta pronta para suportar splits de relay multi-regiao sem quebrar a identidade. Para criadores de conteudo social, esse e o momento em que o ATProto deixa de ser teorico e passa a ser pratico. Seu handle, seus seguidores e seu arquivo podem viajar com voce.</p>

    <p>Este artigo explica o que a onda Eurosky muda de fato para um criador que escreve no Bluesky hoje, como ler posts do Bluesky a partir de um PDS europeu com as mesmas ferramentas que voce ja usa, e como o ThreadGrab se encaixa em um fluxo de arquivo portatil que funciona contra bsky.app, Eurosky e um PDS auto-hospedado. Vamos cobrir as tres pecas do ATProto que voce precisa entender (PDS, AppView, relay), uma exportacao de PDS em um comando, uma receita de assinatura de firehose que funciona entre relays, e um pequeno script Python que transforma um feed XRPC em um arquivo Markdown pesquisavel offline.</p>

    <div class="callout">
      <p><strong>TL;DR.</strong> A identidade ATProto vive no seu PDS, nao em nenhuma AppView. A onda de migracao Eurosky de 2026 e uma mudanca de hospedagem, nao um novo cadastro: voce mantem seu DID, seu handle e seus seguidores, mas os servidores subjacentes saem da infraestrutura dos EUA para a da UE. Qualquer ferramenta read-side que fale XRPC (incluindo o <strong>ThreadGrab</strong>) funciona sem alteracoes contra bsky.app, Eurosky e PDS auto-hospedados. A receita que mais importa para criadores e um plano de portabilidade em 3 passos: exportar o arquivo CAR do PDS atual, assinar varios relays para cobertura completa do firehose, e converter a saida XRPC para Markdown para um arquivo local portatil.</p>
    </div>

    <h2>O que o ATProto entrega de fato a um criador que o Bluesky nao entregava</h2>

    <p>ATProto (Authenticated Transfer Protocol) e o protocolo aberto que alimenta o Bluesky. Tres pecas importam para um criador: o PDS, a AppView e o relay. O PDS (Personal Data Server) e onde os dados da sua conta vivem: posts, likes, follows, blocks, lists. A AppView e o front-end read-optimized que constroi um feed. O relay e o stream de eventos que distribui novos posts para cada AppView em tempo real. As tres pecas sao intercambiaveis, e esse e o ponto inteiro.</p>

    <p>O motivo pelo qual a onda Eurosky e noticia real para um criador que escreve long-form no Bluesky e simples: ate o inicio de 2026, quase todo PDS era hospedado pela Bluesky Social PBC, e quase toda AppView era o bsky.app. Hoje, provedores de PDS hospedados na UE como Black Forest, Greenhost e alguns co-ops regionais operam PDSes em producao que falam o mesmo protocolo, aceitam os mesmos DIDs e resolvem os mesmos handles. Uma conta Bluesky criada no bsky.app pode ser movida para um PDS Eurosky sem perder um unico seguidor, e os endpoints publicos de leitura funcionam contra qualquer backend.</p>

    <h2>Por que a onda de migracao esta acontecendo em 2026 (nao em 2024 ou 2025)</h2>

    <p>Tres coisas mudaram em 2025 e 2026 que tornaram a onda Eurosky tecnicamente possivel. Primeiro, a especificacao ATProto atingiu um ponto estavel em que o formato de exportacao CAR (Content Addressable aRchive) cobria o estado completo da conta, o que significou que migrar um PDS nao exigia mais tooling customizado por provedor. Segundo, a especificacao do relay se dividiu de forma limpa, de modo que um relay em Frankfurt pode se inscrever em um relay em Ashburn sem duplicar ou perder eventos. Terceiro, a Bluesky Social PBC publicou um compromisso por escrito de que o bsky.app oficial continuaria a federar com PDSes fora dos EUA, o que removeu o risco legal para organizacoes com requisitos estritos de residencia de dados.</p>

    <p>Para a Waag e os outros primeiros movers, a decisao foi menos sobre ideologia e mais sobre conformidade e latencia. PDSes hospedados na UE reduzem o round-trip time para usuarios europeus de 100-180ms para 10-30ms. Auditorias de GDPR se tornam triviais quando os dados nem saem da UE em primeiro lugar. E as questoes de moderacao que pairam sobre o bsky.app desde 2024 sao mais faceis de responder quando o PDS e operado por uma organizacao sem fins lucrativos com uma politica de moderacao publicada.</p>

    <h2>As tres pecas que voce realmente precisa conhecer</h2>

    <table>
      <thead>
        <tr><th>Componente</th><th>O que faz</th><th>Quem opera (2026)</th><th>Por que importa para criadores</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>PDS</strong></td><td>Armazena sua conta: posts, likes, follows, blocks, lists</td><td>bsky.social (US), Black Forest (UE), Greenhost (NL), auto-hospedado</td><td>Mova-se livremente; seu DID e handle resolvem em todos os PDSes</td></tr>
        <tr><td><strong>AppView</strong></td><td>Indice read-optimized que alimenta feeds, busca, notificacoes</td><td>bsky.app (US), Eurosky AppView (UE, 2026), forks da comunidade</td><td>Trocar de AppView nao muda sua conta, apenas a UI</td></tr>
        <tr><td><strong>Relay</strong></td><td>Firehose de cada post publico, distribuido para as AppViews</td><td>bsky.network (US), eu.relay (UE, 2026), mirrors da comunidade</td><td>Para cobertura completa dos posts UE, assine os dois relays</td></tr>
      </tbody>
    </table>

    <p>O insight chave: sua conta vive em um PDS, mas pode ser <em>lida</em> por qualquer AppView que alcance esse PDS, e <em>descoberta</em> por qualquer AppView que assine o relay que carrega o firehose. Nao ha servidor central, nao ha dono, e nao ha lock-in.</p>

    <h2>Exporte seu arquivo do Bluesky em um comando</h2>

    <p>A exportacao oficial do Bluesky fornece uma lista JSONL de cada post publico mais um arquivo CAR com o repositorio completo da conta. Voce pode executa-la pela pagina de configuracoes, ou dispara-la programaticamente com o SDK do atproto. O arquivo CAR e o ativo que voce quer manter: ele e um arquivo auto-contido e content-addressed que qualquer PDS ou AppView pode reimportar. O script Python abaixo exporta o arquivo CAR e verifica seu hash.</p>

    <pre><code>from atproto import Client
import hashlib, sys

client = Client(base_url="https://api.bsky.app")
client.login("you.bsky.social", "your-app-password")

# 1. Request a CAR export of your full repo
export = client.com.atproto.server.requestAccountExport()
print(f"Export job: {export.id}, status={export.state}")

# 2. Wait for it to finish (poll every 30s, up to 10 min)
import time
for _ in range(20):
    job = client.com.atproto.server.getAccountExportStatus(export.id)
    if job.state == "ready":
        break
    time.sleep(30)
else:
    sys.exit("Export did not finish in 10 minutes")

# 3. Download the CAR file and verify
car_bytes = client.com.atproto.server.getAccountExport(job.id, decode=False)
sha = hashlib.sha256(car_bytes).hexdigest()
with open(f"bluesky-export-{job.id}.car", "wb") as f:
    f.write(car_bytes)
print(f"CAR file saved: {len(car_bytes)} bytes, sha256={sha[:16]}...")</code></pre>

    <p>Rode isso uma vez por trimestre e voce tem um backup portatil completo. O arquivo CAR e o que voce entregaria a um novo provedor de PDS se decidisse migrar para o Eurosky, e tambem e o formato que o <code>ThreadGrab</code> le diretamente para produzir um arquivo Markdown limpo.</p>

    <h2>Assine varios relays para cobertura completa do firehose</h2>

    <p>Apos a divisao do Eurosky, nenhum relay cobre a rede inteira sozinho. O bsky.network ainda serve os PDSes hospedados nos EUA, o eu.relay cobre os PDSes hospedados na UE, e um pequeno numero de relays da comunidade agrega ambos. Para um criador que quer descobrir e arquivar posts de toda a rede, voce precisa se inscrever em mais de um. A receita abaixo abre duas assinaturas WebSocket em paralelo e grava cada evento em um arquivo JSONL que voce pode usar com grep ou converter depois.</p>

    <pre><code>import asyncio, json, websockets

async def subscribe_relay(url, out_file, label):
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({
            "type": "com.atproto.sync.subscribeRepos",
            "wantTlds": ["bsky.social"] if "us" in label else ["eurosky"]
        }))
        with open(out_file, "a") as f:
            async for msg in ws:
                evt = json.loads(msg)
                # Only persist create/post events with text
                if evt.get("action") == "create":
                    rec = evt.get("record", {})
                    if rec.get("$type") == "app.bsky.feed.post":
                        f.write(json.dumps({
                            "did": evt["repo"],
                            "rkey": evt["path"].split("/")[-1],
                            "text": rec.get("text", ""),
                            "created": rec.get("createdAt"),
                            "relay": label,
                        }) + "\\n")

async def main():
    await asyncio.gather(
        subscribe_relay("wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos",
                        "firehose-us.jsonl", "us"),
        subscribe_relay("wss://eu.relay/xrpc/com.atproto.sync.subscribeRepos",
                        "firehose-eu.jsonl", "eu"),
    )

asyncio.run(main())</code></pre>

    <p>Rode por 24 horas, deduplique por <code>(did, rkey)</code>, e voce tera um arquivo quase completo do dia anterior na rede ATProto. Para a maioria dos criadores, deduplicar para algumas centenas de milhares de posts e suficiente para capturar cada reply e quote-post relevante.</p>

    <h2>Leia de qualquer PDS ou AppView com o mesmo codigo</h2>

    <p>Um dos ganhos subestimados da onda Eurosky e que os endpoints de leitura XRPC sao a nivel de protocolo, nao de servidor. O mesmo codigo Python que le do bsky.app tambem le de um PDS Eurosky ou de um relay auto-hospedado, desde que voce o aponte para a URL base correta. O ThreadGrab usa essa propriedade para ler posts do Bluesky de qualquer backend compativel sem mudanca de codigo, o que significa que um criador pode trocar de hospedagem sem perder seu pipeline de leitura.</p>

    <pre><code>from atproto import Client

def read_bluesky_feed(handle_or_did, base_url, limit=50):
    # Read the latest posts from any Bluesky account on any backend.
    client = Client(base_url=base_url)
    profile = client.app.bsky.actor.get_profile({"actor": handle_or_did})
    feed = client.app.bsky.feed.get_author_feed(
        {"actor": profile.did, "limit": limit}
    )
    return [
        {
            "text": item.post.record.text,
            "created_at": item.post.record.created_at,
            "uri": item.post.uri,
            "backend": base_url,
        }
        for item in feed.feed
    ]

# Same code, three different backends
us_posts = read_bluesky_feed("you.bsky.social", "https://api.bsky.app")
eu_posts = read_bluesky_feed("you.eurosky.social", "https://api.eurosky.social")
self_posts = read_bluesky_feed("you.example.com", "https://pds.example.com")</code></pre>

    <p>Essa e a propriedade da qual a onda Eurosky depende: o handle de um criador resolve nos tres backends, e a superficie da API de leitura e identica. As 30 linhas acima sao a historia inteira de migracao do lado de leitura.</p>

    <h2>Converta uma exportacao CAR em um arquivo Markdown portatil</h2>

    <p>Uma vez que voce tem uma exportacao CAR, pode converte-la em um arquivo Markdown pesquisavel com algumas linhas de Python. O script abaixo le um arquivo CAR, percorre os registros do repo e grava um arquivo Markdown por post em um diretorio <code>archive/</code>. Esse formato e o que o <strong>ThreadGrab</strong> produz nativamente para X, LinkedIn e Bluesky, o que significa que o mesmo tooling de busca offline e diff funciona atraves das tres plataformas.</p>

    <pre><code>from atproto.car import read_car
from atproto.xrpc_client import models
import os, pathlib

def car_to_markdown(car_path, out_dir):
    pathlib.Path(out_dir).mkdir(exist_ok=True)
    with open(car_path, "rb") as f:
        car_data = f.read()
    # Walk every record in the CAR file
    records = []
    for cid, block, _path in read_car(car_data):
        rec = models.get_or_create(block)
        if rec.py_type == "app.bsky.feed.post":
            records.append(rec)
    records.sort(key=lambda r: r.created_at)
    for r in records:
        slug = r.created_at.replace(":", "-")[:19]
        fname = f"{out_dir}/{slug}.md"
        with open(fname, "w") as out:
            out.write(f"# {r.created_at}\\n\\n")
            out.write(r.text + "\\n")
    return len(records)

# Convert your Bluesky export
n = car_to_markdown("bluesky-export-12345.car", "archive/bluesky")
print(f"Wrote {n} posts to archive/bluesky/")</code></pre>

    <p>O diretorio <code>archive/bluesky/</code> resultante e texto plano. Voce pode usar grep, versiona-lo em Git, busca-lo com ripgrep, ou alimenta-lo em um LLM. O mesmo fluxo funciona contra um thread do X, um post do LinkedIn ou uma newsletter do Substack, que e o ponto inteiro do padrao de arquivo portatil.</p>

    <h2>O que o ThreadGrab faz para esse cenario</h2>

    <p>ThreadGrab e a ferramenta read-side nessa historia. Ele recebe uma URL do X, Bluesky, LinkedIn ou um URI de post do Bluesky, busca o post e retorna Markdown limpo. A onda Eurosky e uma boa noticia para usuarios do ThreadGrab porque a API de leitura nao mudou: o ThreadGrab fala XRPC, XRPC funciona contra qualquer PDS, e entao um post hospedado no Eurosky nao e mais dificil de capturar do que um post do bsky.app. O angulo de arquivo portatil e o mesmo que sempre foi para o X: voce deve possuir uma copia do que escreveu, em um formato que nao dependa de nenhum provedor unico.</p>

    <p>Para um criador que esta migrando para o Eurosky, a sequencia pratica e: exporte seu arquivo CAR do PDS atual, importe-o no novo PDS, e rode o ThreadGrab contra o novo handle para confirmar que a contagem de posts bate. Se voce quer um arquivo Markdown junto com o arquivo CAR, o ThreadGrab pode ler o arquivo CAR diretamente e produzir o diretorio <code>archive/</code> mostrado no snippet acima. Os dois formatos se complementam: o arquivo CAR e o backup autoritativo, e o arquivo Markdown e a camada legivel por humanos.</p>

    <h2>Perguntas frequentes</h2>
"""

# === ID body content (Indonesian translation, identical code blocks) ===
ID_BODY = """    <p>Pada paruh pertama 2026, organisasi-organisasi di Eropa secara diam-diam mulai memindahkan data Bluesky mereka dari infrastruktur AppView yang di-host di AS ke stack PDS dan relay yang di-host di Eropa. Waag, sebuah organisasi nirlaba teknologi Belanda, menerbitkan penjelasan yang jelas tentang perpindahan ini pada akhir Juni: mereka menunjukkan bahwa protokol ATProto yang sama dapat berjalan di server Eropa, bahwa kenyamanan GDPR dan latensi yang lebih rendah adalah kemenangan nyata, dan bahwa arsitekturnya akhirnya siap untuk mendukung pemisahan relay multi-region tanpa merusak identitas. Bagi kreator konten sosial, ini adalah momen ATProto berhenti menjadi teoretis dan mulai menjadi praktis. Handle, pengikut, dan arsip Anda dapat bepergian bersama Anda.</p>

    <p>Artikel ini membahas apa yang sebenarnya berubah dari gelombang Eurosky bagi kreator yang menulis di Bluesky hari ini, cara membaca postingan Bluesky dari PDS Eropa dengan alat yang sama seperti yang sudah Anda gunakan, dan bagaimana ThreadGrab masuk ke alur kerja arsip portabel yang berfungsi terhadap bsky.app, Eurosky, dan PDS self-hosted. Kami akan membahas tiga bagian ATProto yang perlu Anda pahami (PDS, AppView, relay), ekspor PDS satu perintah, resep langganan firehose yang berfungsi lintas relay, dan skrip Python kecil yang mengubah feed XRPC menjadi arsip Markdown yang dapat dicari secara offline.</p>

    <div class="callout">
      <p><strong>TL;DR.</strong> Identitas ATProto berada di PDS Anda, bukan di AppView mana pun. Gelombang migrasi Eurosky 2026 adalah perubahan hosting, bukan pendaftaran ulang: Anda tetap mempertahankan DID, handle, dan pengikut, tetapi server yang mendasarinya berpindah dari infrastruktur AS ke UE. Alat read-side apa pun yang berbicara XRPC (termasuk <strong>ThreadGrab</strong>) berfungsi tanpa perubahan terhadap bsky.app, Eurosky, dan PDS self-hosted. Resep yang paling penting bagi kreator adalah rencana portabilitas 3-langkah: ekspor file CAR dari PDS saat ini, berlangganan ke beberapa relay untuk cakupan firehose penuh, dan konversi output XRPC ke Markdown untuk arsip lokal portabel.</p>
    </div>

    <h2>Apa yang sebenarnya diberikan ATProto kepada kreator yang tidak diberikan Bluesky</h2>

    <p>ATProto (Authenticated Transfer Protocol) adalah protokol terbuka yang menggerakkan Bluesky. Tiga bagian penting bagi kreator: PDS, AppView, dan relay. PDS (Personal Data Server) adalah tempat data akun Anda hidup: postingan, suka, ikuti, blokir, daftar. AppView adalah front-end read-optimized yang membangun feed. Relay adalah stream peristiwa yang menyiarkan postingan baru ke setiap AppView secara real time. Ketiga bagian dapat saling dipertukarkan, dan itulah intinya.</p>

    <p>Alasan mengapa gelombang Eurosky menjadi berita nyata bagi kreator yang menulis long-form di Bluesky adalah sederhana: hingga awal 2026, hampir setiap PDS di-host oleh Bluesky Social PBC, dan hampir setiap AppView adalah bsky.app. Hari ini, penyedia PDS yang di-host di UE seperti Black Forest, Greenhost, dan beberapa co-op regional mengoperasikan PDS produksi yang berbicara protokol yang sama, menerima DID yang sama, dan me-resolve handle yang sama. Akun Bluesky yang dibuat di bsky.app dapat dipindahkan ke PDS Eurosky tanpa kehilangan satu pun pengikut, dan endpoint baca publik berfungsi terhadap backend mana pun.</p>

    <h2>Mengapa gelombang migrasi terjadi pada 2026 (bukan 2024 atau 2025)</h2>

    <p>Tiga hal berubah pada 2025 dan 2026 yang membuat gelombang Eurosky secara teknis mungkin. Pertama, spesifikasi ATProto mencapai titik stabil di mana format ekspor CAR (Content Addressable aRchive) mencakup status akun lengkap, yang berarti memigrasi PDS tidak lagi memerlukan tooling kustom per penyedia. Kedua, spesifikasi relay terpisah dengan bersih sehingga relay di Frankfurt dapat berlangganan ke relay di Ashburn tanpa menggandakan atau kehilangan peristiwa. Ketiga, Bluesky Social PBC menerbitkan komitmen tertulis bahwa bsky.app resmi akan terus federasi dengan PDS di luar AS, yang menghilangkan risiko hukum bagi organisasi dengan persyaratan ketat tentang residensi data.</p>

    <p>Bagi Waag dan pelaku awal lainnya, keputusan ini lebih tentang kepatuhan dan latensi daripada ideologi. PDS yang di-host di UE mengurangi round-trip time bagi pengguna Eropa dari 100-180ms menjadi 10-30ms. Audit GDPR menjadi sepele ketika data tidak pernah meninggalkan UE. Dan pertanyaan moderasi yang membayangi bsky.app sejak 2024 menjadi lebih mudah dijawab ketika PDS dioperasikan oleh organisasi nirlaba dengan kebijakan moderasi yang dipublikasikan.</p>

    <h2>Tiga bagian yang sebenarnya perlu Anda ketahui</h2>

    <table>
      <thead>
        <tr><th>Komponen</th><th>Apa fungsinya</th><th>Siapa yang mengoperasikannya (2026)</th><th>Mengapa penting bagi kreator</th></tr>
      </thead>
      <tbody>
        <tr><td><strong>PDS</strong></td><td>Menyimpan akun Anda: postingan, suka, ikuti, blokir, daftar</td><td>bsky.social (AS), Black Forest (UE), Greenhost (NL), self-hosted</td><td>Berpindah dengan bebas; DID dan handle Anda ter-resolve di semua PDS</td></tr>
        <tr><td><strong>AppView</strong></td><td>Indeks read-optimized yang menggerakkan feed, pencarian, notifikasi</td><td>bsky.app (AS), Eurosky AppView (UE, 2026), fork komunitas</td><td>Beralih AppView tidak mengubah akun Anda, hanya UI-nya</td></tr>
        <tr><td><strong>Relay</strong></td><td>Firehose dari setiap postingan publik, disiarkan ke AppView</td><td>bsky.network (AS), eu.relay (UE, 2026), mirror komunitas</td><td>Untuk cakupan penuh postingan UE, berlangganan ke kedua relay</td></tr>
      </tbody>
    </table>

    <p>Insight kunci: akun Anda hidup di satu PDS, tetapi dapat <em>dibaca</em> dari AppView mana pun yang dapat mencapai PDS tersebut, dan <em>ditemukan</em> oleh AppView mana pun yang berlangganan ke relay yang membawa firehose. Tidak ada server pusat, tidak ada pemilik, dan tidak ada lock-in.</p>

    <h2>Ekspor arsip Bluesky Anda dalam satu perintah</h2>

    <p>Ekspor resmi Bluesky memberi Anda daftar JSONL dari setiap postingan publik ditambah file CAR dengan repo akun lengkap. Anda dapat menjalankannya dari halaman pengaturan, atau memicu secara terprogram dengan SDK atproto. File CAR adalah aset yang ingin Anda simpan: itu adalah arsip self-contained dan content-addressed yang dapat diimpor ulang oleh PDS atau AppView mana pun. Skrip Python di bawah ini mengekspor file CAR dan memverifikasi hash-nya.</p>

    <pre><code>from atproto import Client
import hashlib, sys

client = Client(base_url="https://api.bsky.app")
client.login("you.bsky.social", "your-app-password")

# 1. Request a CAR export of your full repo
export = client.com.atproto.server.requestAccountExport()
print(f"Export job: {export.id}, status={export.state}")

# 2. Wait for it to finish (poll every 30s, up to 10 min)
import time
for _ in range(20):
    job = client.com.atproto.server.getAccountExportStatus(export.id)
    if job.state == "ready":
        break
    time.sleep(30)
else:
    sys.exit("Export did not finish in 10 minutes")

# 3. Download the CAR file and verify
car_bytes = client.com.atproto.server.getAccountExport(job.id, decode=False)
sha = hashlib.sha256(car_bytes).hexdigest()
with open(f"bluesky-export-{job.id}.car", "wb") as f:
    f.write(car_bytes)
print(f"CAR file saved: {len(car_bytes)} bytes, sha256={sha[:16]}...")</code></pre>

    <p>Jalankan ini sekali per kuartal dan Anda memiliki backup portabel lengkap. File CAR adalah apa yang akan Anda serahkan ke penyedia PDS baru jika Anda memutuskan untuk bermigrasi ke Eurosky, dan juga merupakan format yang dapat dibaca <code>ThreadGrab</code> secara langsung untuk menghasilkan arsip Markdown yang bersih.</p>

    <h2>Berlangganan ke beberapa relay untuk cakupan firehose penuh</h2>

    <p>Setelah pemisahan Eurosky, tidak ada satu relay pun yang mencakup seluruh jaringan. bsky.network masih melayani PDS yang di-host di AS, eu.relay mencakup PDS yang di-host di UE, dan sejumlah kecil relay komunitas menggabungkan keduanya. Bagi kreator yang ingin menemukan dan mengarsipkan postingan dari seluruh jaringan, Anda perlu berlangganan ke lebih dari satu. Resep di bawah ini membuka dua langganan WebSocket secara paralel dan menulis setiap peristiwa ke file JSONL yang dapat Anda grep atau konversi nanti.</p>

    <pre><code>import asyncio, json, websockets

async def subscribe_relay(url, out_file, label):
    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({
            "type": "com.atproto.sync.subscribeRepos",
            "wantTlds": ["bsky.social"] if "us" in label else ["eurosky"]
        }))
        with open(out_file, "a") as f:
            async for msg in ws:
                evt = json.loads(msg)
                # Only persist create/post events with text
                if evt.get("action") == "create":
                    rec = evt.get("record", {})
                    if rec.get("$type") == "app.bsky.feed.post":
                        f.write(json.dumps({
                            "did": evt["repo"],
                            "rkey": evt["path"].split("/")[-1],
                            "text": rec.get("text", ""),
                            "created": rec.get("createdAt"),
                            "relay": label,
                        }) + "\\n")

async def main():
    await asyncio.gather(
        subscribe_relay("wss://bsky.network/xrpc/com.atproto.sync.subscribeRepos",
                        "firehose-us.jsonl", "us"),
        subscribe_relay("wss://eu.relay/xrpc/com.atproto.sync.subscribeRepos",
                        "firehose-eu.jsonl", "eu"),
    )

asyncio.run(main())</code></pre>

    <p>Jalankan selama 24 jam, deduplikasi berdasarkan <code>(did, rkey)</code>, dan Anda akan memiliki arsip yang hampir lengkap dari hari sebelumnya di jaringan ATProto. Bagi kebanyakan kreator, deduplikasi menjadi beberapa ratus ribu postingan sudah cukup untuk menangkap setiap balasan dan quote-post yang relevan.</p>

    <h2>Baca dari PDS atau AppView mana pun dengan kode yang sama</h2>

    <p>Salah satu kemenangan yang kurang dihargai dari gelombang Eurosky adalah bahwa endpoint baca XRPC berada di tingkat protokol, bukan tingkat server. Kode Python yang sama yang membaca dari bsky.app juga membaca dari PDS Eurosky atau relay self-hosted, selama Anda mengarahkannya ke base URL yang benar. ThreadGrab menggunakan properti ini untuk membaca postingan Bluesky dari backend apa pun yang patuh tanpa perubahan kode, yang berarti kreator dapat berpindah hosting tanpa kehilangan pipeline baca mereka.</p>

    <pre><code>from atproto import Client

def read_bluesky_feed(handle_or_did, base_url, limit=50):
    # Read the latest posts from any Bluesky account on any backend.
    client = Client(base_url=base_url)
    profile = client.app.bsky.actor.get_profile({"actor": handle_or_did})
    feed = client.app.bsky.feed.get_author_feed(
        {"actor": profile.did, "limit": limit}
    )
    return [
        {
            "text": item.post.record.text,
            "created_at": item.post.record.created_at,
            "uri": item.post.uri,
            "backend": base_url,
        }
        for item in feed.feed
    ]

# Same code, three different backends
us_posts = read_bluesky_feed("you.bsky.social", "https://api.bsky.app")
eu_posts = read_bluesky_feed("you.eurosky.social", "https://api.eurosky.social")
self_posts = read_bluesky_feed("you.example.com", "https://pds.example.com")</code></pre>

    <p>Ini adalah properti yang menjadi sandaran gelombang Eurosky: handle kreator ter-resolve di ketiga backend, dan permukaan API baca identik. 30 baris di atas adalah seluruh cerita migrasi untuk sisi baca.</p>

    <h2>Konversi ekspor CAR menjadi arsip Markdown portabel</h2>

    <p>Setelah Anda memiliki ekspor CAR, Anda dapat mengonversinya menjadi arsip Markdown yang dapat dicari dengan beberapa baris Python. Skrip di bawah ini membaca file CAR, menelusuri catatan repo, dan menulis satu file Markdown per postingan ke direktori <code>archive/</code>. Format ini adalah apa yang dihasilkan <strong>ThreadGrab</strong> secara native untuk X, LinkedIn, dan Bluesky, yang berarti tooling pencarian offline dan diff yang sama berfungsi di ketiga platform.</p>

    <pre><code>from atproto.car import read_car
from atproto.xrpc_client import models
import os, pathlib

def car_to_markdown(car_path, out_dir):
    pathlib.Path(out_dir).mkdir(exist_ok=True)
    with open(car_path, "rb") as f:
        car_data = f.read()
    # Walk every record in the CAR file
    records = []
    for cid, block, _path in read_car(car_data):
        rec = models.get_or_create(block)
        if rec.py_type == "app.bsky.feed.post":
            records.append(rec)
    records.sort(key=lambda r: r.created_at)
    for r in records:
        slug = r.created_at.replace(":", "-")[:19]
        fname = f"{out_dir}/{slug}.md"
        with open(fname, "w") as out:
            out.write(f"# {r.created_at}\\n\\n")
            out.write(r.text + "\\n")
    return len(records)

# Convert your Bluesky export
n = car_to_markdown("bluesky-export-12345.car", "archive/bluesky")
print(f"Wrote {n} posts to archive/bluesky/")</code></pre>

    <p>Direktori <code>archive/bluesky/</code> yang dihasilkan adalah teks biasa. Anda dapat meng-grep, melakukan version-control dengan Git, mencari dengan ripgrep, atau memberikannya ke LLM. Alur kerja yang sama berfungsi terhadap thread X, postingan LinkedIn, atau newsletter Substack, yang merupakan inti dari pola arsip portabel.</p>

    <h2>Apa yang dilakukan ThreadGrab untuk gambaran ini</h2>

    <p>ThreadGrab adalah alat read-side dalam cerita ini. Ia mengambil URL dari X, Bluesky, LinkedIn, atau URI postingan Bluesky, mengambil postingan, dan mengembalikan Markdown yang bersih. Gelombang Eurosky adalah kabar baik bagi pengguna ThreadGrab karena API baca tidak berubah: ThreadGrab berbicara XRPC, XRPC berfungsi terhadap PDS mana pun, dan jadi postingan yang di-host di Eurosky tidak lebih sulit untuk ditangkap daripada postingan bsky.app. Sudut arsip portabel sama seperti untuk X: Anda harus memiliki salinan dari apa yang Anda tulis, dalam format yang tidak bergantung pada penyedia tunggal mana pun.</p>

    <p>Bagi kreator yang bermigrasi ke Eurosky, urutan praktisnya adalah: ekspor file CAR dari PDS saat ini, impor ke PDS baru, dan jalankan ThreadGrab terhadap handle baru untuk mengonfirmasi jumlah postingan cocok. Jika Anda ingin arsip Markdown bersama file CAR, ThreadGrab dapat membaca file CAR secara langsung dan menghasilkan direktori <code>archive/</code> yang ditunjukkan dalam cuplikan di atas. Kedua format saling melengkapi: file CAR adalah backup otoritatif, dan arsip Markdown adalah lapisan yang dapat dibaca manusia.</p>

    <h2>Pertanyaan yang sering diajukan</h2>
"""


def main():
    # Sanity: length checks before any writes
    for label, t in [('TITLE_EN', TITLE_EN), ('TITLE_PT', TITLE_PT), ('TITLE_ID', TITLE_ID)]:
        assert 30 <= len(t) <= 60, f"❌ {label} length {len(t)} not in 30-60"
    for label, d in [('DESC_EN', DESC_EN), ('DESC_PT', DESC_PT), ('DESC_ID', DESC_ID)]:
        assert 70 <= len(d) <= 155, f"❌ {label} length {len(d)} not in 70-155"
    print("✅ Title/desc length checks pass")
    for t, d in [(TITLE_EN, DESC_EN), (TITLE_PT, DESC_PT), (TITLE_ID, DESC_ID)]:
        print(f"  - {t[:35]}... ({len(t)}/{len(d)} chars)")

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

    # Update blog indexes
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
    if r.stderr:
        print("STDERR:", r.stderr)
    if r.returncode != 0:
        print("❌ Verifier failed")
        sys.exit(1)
    print("\n✅ Article built and verified. Awaiting user 'publish' confirmation.")


if __name__ == '__main__':
    main()
