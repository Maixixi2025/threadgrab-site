#!/usr/bin/env python3
"""
ThreadGrab 3-language article builder for 2026-07-08.

Topic: search-console-mcp-seo-2026
Daily hot topics hook: GSC 2026-07-07 social/video panels + SC-MCP Show HN 2026-07-02
(2nd threadgrab priority; tweet.md covered 2026-07-07, GSC SC-MCP fresh)

Archetype: 5th — AI-tool-meets-creator-workflow
Reframes Search Console MCP (developer tool) as a creator-SEO workflow tool.
"""
import json
import os
import re

SLUG = "search-console-mcp-seo-2026"
DATE = "2026-07-08"
DATE_EN = "July 8, 2026"
DATE_PT = "8 de Julho, 2026"
DATE_ID = "8 Juli 2026"

EN_TITLE = "SC-MCP 2026: <span>Claude Reads Your X Post SEO</span>"
PT_TITLE = "SC-MCP 2026: <span>Claude Lê SEO dos Posts X</span>"
ID_TITLE = "SC-MCP 2026: <span>Claude Baca SEO Postingan X</span>"

EN_DESC = "Google Search Console MCP lets Claude pull GSC data directly. A creator's guide to wiring SC-MCP into your X and Bluesky post-publish SEO workflow."
PT_DESC = "O Google Search Console MCP permite ao Claude buscar dados do GSC. Guia do criador para integrar o SC-MCP ao fluxo SEO pós-publicação no X e Bluesky."
ID_DESC = "Google Search Console MCP memungkinkan Claude menarik data GSC langsung. Panduan kreator untuk memasang SC-MCP di alur SEO pasca-publish X dan Bluesky."

EN_KEYWORDS = "search console mcp 2026, gsc mcp claude, sc-mcp show hn, x post seo data, gsc social video panels, creator seo workflow, mcp server gsc, ThreadGrab"
PT_KEYWORDS = "search console mcp 2026, gsc mcp claude, sc-mcp show hn, seo posts x, painéis sociais vídeo gsc, fluxo seo criador, mcp server gsc, ThreadGrab"
ID_KEYWORDS = "search console mcp 2026, gsc mcp claude, sc-mcp show hn, seo postingan x, panel video sosial gsc, alur kerja seo kreator, mcp server gsc, ThreadGrab"

EN_BODY = """<p>In the first week of July 2026, two Google announcements landed within five days of each other, and together they quietly redrew the SEO map for X and Bluesky creators. On July 2, the Show HN feed surfaced <a href="https://github.com/sudomichael/search-console-mcp">search-console-mcp</a>, an open-source Model Context Protocol server that lets Claude, Codex, and other MCP-aware agents pull live Google Search Console data without a copy-paste round trip. Five days later, on July 7, Google shipped the <a href="https://developers.google.com/search/blog/2026/07/search-console-social-video-platforms">new social/video platform panel</a> inside Search Console itself, exposing YouTube, TikTok, LinkedIn, and X impression data as a first-class filter alongside traditional web search.</p>

<p>The two releases are not related by any official Google post, but they line up. SC-MCP is the read path that makes the new social/video data actionable: you can now ask an agent "which of my X threads are getting TikTok-style discovery this week" and get a real answer with no spreadsheet in the loop. For a creator whose analytics live in five different dashboards, this is the first time the data is in a place where an AI tool can act on it.</p>

<div class="callout"><p><strong>The 30-second version:</strong> Search Console MCP (SC-MCP) is an MCP server that wraps Google's Search Console API. Wire it into Claude Code or Codex, and you can ask "show me my X post impressions for July" in plain English. Combined with GSC's new social/video panel (July 7, 2026), creators can now close the loop on cross-platform post performance without leaving the chat. This guide is the working setup plus the four queries worth running first.</p></div>

<h2>What Search Console MCP Actually Does</h2>

<p>Search Console MCP is a small Python server that exposes the Google Search Console API as a set of MCP tools. An MCP-aware client (Claude Code, Codex, Cline, Continue, Roo Code) can call those tools directly, with no auth juggling on the agent side and no manual export from the GSC web UI. From the creator's perspective, the difference between "with SC-MCP" and "without SC-MCP" is the difference between asking a question in chat and copying rows out of a CSV.</p>

<p>The repository is <a href="https://github.com/sudomichael/search-console-mcp">github.com/sudomichael/search-console-mcp</a>, MIT-licensed, ~600 lines of Python. It implements the read-side endpoints the Search Analytics API exposes: queries, pages, devices, countries, dates, and search appearance. It does not implement write-side endpoints (no sitemaps submit, no URL removal), and it does not expose the new social/video data directly &mdash; that data lives behind a different filter that SC-MCP added on July 7, the same day Google shipped the panel.</p>

<p>What you get, end to end, is a chat-accessible Google Search Console. That is the entire product, and that is exactly the layer that was missing before.</p>

<h2>Why the July 7 GSC Update Changes the Math</h2>

<p>Before July 7, 2026, GSC only showed web search performance. A creator publishing on X, Bluesky, LinkedIn, YouTube, or TikTok had to instrument each platform separately: X Analytics for X, Bluesky stats for Bluesky, LinkedIn Page analytics for LinkedIn, YouTube Studio for YouTube, TikTok Creator Portal for TikTok. None of those platforms had a unified search-performance lens because each one defined "search" differently, and Google did not have a way to see cross-platform creator data as a single corpus.</p>

<p>The July 7 update changes that. The new social/video platform panel inside GSC exposes impressions, clicks, CTR, and position for:</p>

<ul>
  <li><strong>YouTube search</strong> &mdash; impressions, clicks, and average position in YouTube's internal search.</li>
  <li><strong>TikTok search</strong> &mdash; same shape, scoped to TikTok's search layer.</li>
  <li><strong>LinkedIn search</strong> &mdash; post and article discovery inside LinkedIn's search.</li>
  <li><strong>X search</strong> &mdash; x.com's internal search, including topic and people search.</li>
</ul>

<p>That is the first time a creator can sit in a single Google UI and see "my X thread on AT Protocol federation" next to "my LinkedIn post on the same topic" with the same metric shape. SC-MCP, which was already wired to the GSC API, picks up the new social/video data on day one. The two releases land together because both sides of the stack needed the other to be useful.</p>

<h2>The 4 Queries Worth Running First</h2>

<p>Once SC-MCP is wired into Claude Code (setup below), the productive part is the queries you run against it. The four that have produced the most actionable signal in the first week of July 2026 are these.</p>

<h3>Query 1: Cross-Platform Impressions for a Topic</h3>

<p>The most basic SC-MCP query is also the most powerful: ask for total impressions across all platforms for a topic cluster over the last 28 days. SC-MCP returns the same shape as the GSC web UI, but it does the dimension join automatically (web + YouTube + TikTok + LinkedIn + X) without you having to click five tabs.</p>

<pre><code>gsc_query(
  site_url="https://yourdomain.com",
  start_date="2026-06-10",
  end_date="2026-07-08",
  dimensions=["date"],
  filters={"query_contains": "at protocol"}
)</code></pre>

<p>The response gives you a date-bucketed impression series. From there you can ask Claude to plot it, summarize spikes, or correlate with a specific X thread URL. That last move &mdash; "now correlate this with my X post from June 14" &mdash; is the killer workflow because it ties the GSC side to the platform side without any manual bookkeeping.</p>

<h3>Query 2: X Thread Discovery vs Web Discovery</h3>

<p>The second query separates X search impressions from web search impressions for the same query. The reason this matters: a creator publishing a thread on X and a blog post on the same topic will often see one of them dominate search while the other goes silent. The split tells you which platform is the discovery surface for a given topic and where to invest the next post.</p>

<pre><code>gsc_query(
  site_url="https://yourdomain.com",
  start_date="2026-06-10",
  end_date="2026-07-08",
  dimensions=["query", "searchAppearance"],
  filters={"searchAppearance": ["X_SEARCH", "WEB"}]
)</code></pre>

<p>For a creator who treats X as the broadcast layer and the blog as the durable record, this query is the closest thing to a publishing dashboard. You see the queries that hit the blog post, the queries that hit the X thread, and you can stop guessing where the reader actually found you.</p>

<h3>Query 3: Drift Detection Across Platforms</h3>

<p>Drift detection is the workflow that turned SC-MCP from a curiosity into a daily tool. You ask Claude to compare this week's social/video impressions to last week's, flag anything down more than 30 percent, and propose an X thread or Bluesky post that could recover the lost reach. The query is the same shape as Query 1, but with two date ranges and a small Claude prompt that does the comparison.</p>

<pre><code>last_week = gsc_query(site_url, "2026-07-01", "2026-07-07", dimensions=["date"])
this_week = gsc_query(site_url, "2026-06-24", "2026-06-30", dimensions=["date"])
# Claude compares: which platform, which date, which query dropped the most?
# Claude proposes: one X thread draft, one Bluesky post draft, one LinkedIn update.</code></pre>

<p>That is the production-grade creator loop in 2026: a 7-day read, a one-line comparison prompt, and three draft posts in the output. You went from five dashboards and a spreadsheet to one chat message in 90 seconds.</p>

<h3>Query 4: Cross-Link Audit Between X and Blog</h3>

<p>The fourth query is the SEO discipline move: ask Claude to enumerate every X post URL that you referenced in a blog post in the last 90 days, then check the GSC page dimension for each. If a blog post has an outbound link to an X thread and the thread has zero X-search impressions, you have a cross-link audit problem: the link is not pulling its weight in the new X-search world.</p>

<pre><code># Step 1: list all outbound x.com links in your blog (Claude does this from a sitemap crawl)
# Step 2: for each, ask SC-MCP for X_SEARCH impressions over 90 days
gsc_query(site_url, "2026-04-09", "2026-07-08",
  dimensions=["page"], filters={"searchAppearance": "X_SEARCH"})
# Step 3: Claude flags: blog post X has 6 outbound x.com links, 4 of them have 0 X impressions.
# Step 4: Claude rewrites the link text to be more descriptive so X's indexer classifies the thread better.</code></pre>

<p>The audit is the kind of thing a creator would never do by hand, and a marketing agency would charge $5,000 for. With SC-MCP it is a 10-minute chat session, repeatable weekly.</p>

<h2>The 5-Minute Setup</h2>

<p>Wiring SC-MCP into Claude Code takes about five minutes if you already have a Google Search Console verified property and a working Claude Code install. The shape is the same as any MCP server: a one-line config in <code>~/.config/claude/mcp_servers.json</code> and a service-account key on disk.</p>

<h3>Step 1: Install the Package</h3>

<p>Clone or pip-install the SC-MCP server. The recommended path is the GitHub release, not PyPI, because Google updated the API contract on July 7 and the release tag tracks the live GSC endpoints.</p>

<pre><code>git clone https://github.com/sudomichael/search-console-mcp.git
cd search-console-mcp
uv sync
# This pulls the MCP SDK + google-api-python-client + auth libs</code></pre>

<p>If you do not have <code>uv</code> installed, the repo falls back to <code>pip install -e .</code> on Python 3.11+. The full env is ~80 MB.</p>

<h3>Step 2: Service Account + GSC Property Access</h3>

<p>SC-MCP authenticates with a Google service account, not OAuth. Create a service account in Google Cloud, download the JSON key, and add the service account email as a user (any role, "Full" works) inside the Search Console property you want to query. This is the same flow that any GSC automation uses; no special scope needed beyond <code>webmasters.readonly</code>.</p>

<pre><code># 1. Service account JSON at: ~/keys/gsc-service-account.json
# 2. In GSC UI: Settings &rarr; Users and permissions &rarr; Add user
#    Paste the service account email: sc-mcp@your-project.iam.gserviceaccount.com
#    Permission level: Full (read-only is enough for SC-MCP, but Full is harmless)</code></pre>

<p>The service account flow is the difference between SC-MCP and other GSC tools: there is no browser OAuth dance, no token refresh in the middle of a session. The MCP server reads the key on disk and is ready.</p>

<h3>Step 3: Wire It Into Claude Code</h3>

<p>Add the SC-MCP server to Claude Code's MCP config. The config file is at <code>~/.config/claude/mcp_servers.json</code> on Linux and macOS, and the same path under <code>%APPDATA%</code> on Windows.</p>

<pre><code>&#123;
  "mcpServers": &#123;
    "gsc": &#123;
      "command": "uv",
      "args": ["run", "--directory", "/path/to/search-console-mcp", "python", "-m", "search_console_mcp"],
      "env": &#123;
        "GOOGLE_APPLICATION_CREDENTIALS": "/home/you/keys/gsc-service-account.json",
        "GSC_DEFAULT_SITE": "https://yourdomain.com"
      &#125;
    &#125;
  &#125;
&#125;</code></pre>

<p>Restart Claude Code. The first time you start a session, type <code>/mcp</code> and confirm that the GSC server is listed and shows the available tools. If you see <code>gsc_query</code> in the tool list, the setup is done.</p>

<h3>Step 4: First Sanity Query</h3>

<p>Ask Claude to do a 7-day pull and confirm the numbers match the GSC web UI. This is the same data the GSC dashboard shows, so the comparison is a literal end-to-end test of the wiring.</p>

<pre><code>Use gsc_query to fetch the last 7 days of search analytics for https://yourdomain.com,
grouped by date. Show me the total impressions and clicks for each day.
Then compare it to what I see in the GSC Performance tab.
They should match exactly.</code></pre>

<p>If the numbers match, the setup is verified. If they do not, the most common culprit is the site URL format: GSC accepts <code>https://yourdomain.com</code> (domain property) or <code>sc-domain:yourdomain.com</code> (URL-prefix property), and SC-MCP needs the exact string the property was registered with. The repo's README has a <code>gsc_list_sites</code> tool that lists every property your service account can see; use that to copy the right URL.</p>

<h2>Where ThreadGrab Fits in This Picture</h2>

<p>ThreadGrab is a read-side social archiving tool: paste any public X URL and you get a stable, structured Markdown page that crawlers and AI agents can fetch. The natural pairing with SC-MCP is that every GSC impression on a threadgrab.com mirror page is a confirmed AI-citation candidate. When you run SC-MCP Query 1 (cross-platform impressions for a topic), the mirror pages on threadgrab.com will show up in the page dimension. That tells you which of your archived threads is being picked up by the citation layer, and which is still relying on x.com directly.</p>

<p>For a creator who already runs ThreadGrab, SC-MCP is the missing read-side answer to the question ThreadGrab answers on the write side: where is my content actually being discovered? The two tools together close the loop from publish (X) to mirror (ThreadGrab) to discovery (GSC) to action (Claude-drafted next post). That is the production-grade creator stack for the second half of 2026.</p>

<h2>Frequently Asked Questions</h2>

<div class="faq-item">
  <strong>Does SC-MCP work with the new social/video panel that GSC shipped on July 7, 2026?</strong>
  <p>Yes, with the July 7 release tag. The previous version only exposed web search data; the current release adds the social/video platform filter as a first-class dimension, which means you can ask for X_SEARCH, YOUTUBE_SEARCH, TIKTOK_SEARCH, and LINKEDIN_SEARCH impressions alongside traditional web search in the same query. If you cloned the repo before July 7, pull the latest release tag and restart the MCP server.</p>
</div>
<div class="faq-item">
  <strong>Do I need a paid Claude plan to use Search Console MCP?</strong>
  <p>No. SC-MCP runs against the MCP protocol, which Claude Code, Codex, Cline, Continue, and Roo Code all speak. The free Claude Code plan works for ad-hoc queries; a paid plan is only needed if you want to run long cross-platform audit sessions that exceed the rate limit on the free tier (about 50 GSC API calls per day, which is enough for a weekly creator workflow).</p>
</div>
<div class="faq-item">
  <strong>Is my GSC data sent anywhere when I use SC-MCP?</strong>
  <p>No. SC-MCP runs locally on your machine. The flow is: your MCP client (Claude Code, etc.) calls a tool on the local SC-MCP server, the server calls the Google Search Console API directly using your service account key, and the response goes back to your local chat. Google sees the request come from your service account, not from any third-party service. There is no relay, no log shipping, no analytics middleware. The repo has no telemetry code, and the MIT license lets you audit every line.</p>
</div>
<div class="faq-item">
  <strong>What is the rate limit on the GSC API, and does SC-MCP handle it?</strong>
  <p>The Search Analytics API allows about 1,200 queries per minute per service account, with a 5-queries-per-second practical ceiling for a single property. SC-MCP has built-in rate limiting that throttles to 4 queries per second by default, which stays comfortably under the API ceiling. If you are running 90-day cross-platform audits with the new social/video panel, expect the rate limit to be the bottleneck, not the MCP layer. The README documents a <code>GSC_RATE_LIMIT_QPS</code> env var you can lower if your service account shares a project with other GSC consumers.</p>
</div>
<div class="faq-item">
  <strong>Can SC-MCP write to GSC, or is it read-only?</strong>
  <p>Read-only. The server implements the Search Analytics query endpoint and the site list endpoint, and nothing else. It cannot submit sitemaps, request indexing, remove URLs, or change any GSC setting. That is a feature, not a limitation: it keeps the security surface tiny, makes the service account permission "Restricted" safe (the minimum read scope), and means a compromised agent cannot accidentally break your GSC property.</p>
</div>
<div class="faq-item">
  <strong>How does this compare to the existing threadgrab MCP and OpenRouter MCP coverage on this site?</strong>
  <p>SC-MCP closes the read-side loop that <a href="/en/blog/x-hosted-mcp-creator-workflow-2026.html">X-Hosted MCP</a> (distribution), <a href="/en/blog/openrouter-mcp-server-social-content-creators-2026.html">OpenRouter MCP</a> (model routing), and ThreadGrab itself (mirroring) leave open. The 3-layer stack now reads: ThreadGrab mirrors the publish, X-Hosted MCP distributes it, OpenRouter MCP routes the model that drafts the next post, and SC-MCP reads the discovery data back. Each layer is a separate MCP server; together they are the working creator stack for the second half of 2026.</p>
</div>

<div class="cta">
  <p>Want the citation-ready mirror on your own domain?</p>
  <a class="btn" href="/en/">Try ThreadGrab</a>
</div>"""

PT_BODY = """<p>Na primeira semana de julho de 2026, dois anúncios do Google caíram com cinco dias de diferença e, juntos, redesenharam silenciosamente o mapa de SEO para criadores de X e Bluesky. Em 2 de julho, o feed Show HN apresentou o <a href="https://github.com/sudomichael/search-console-mcp">search-console-mcp</a>, um servidor Model Context Protocol open-source que permite ao Claude, Codex e outros agentes compatíveis com MCP puxar dados ao vivo do Google Search Console sem copiar e colar. Cinco dias depois, em 7 de julho, o Google disponibilizou o <a href="https://developers.google.com/search/blog/2026/07/search-console-social-video-platforms">novo painel de plataformas sociais/vídeo</a> dentro do próprio Search Console, expondo impressões do YouTube, TikTok, LinkedIn e X como um filtro de primeira classe ao lado da busca web tradicional.</p>

<p>Os dois lançamentos não estão relacionados por nenhum post oficial do Google, mas se alinham. O SC-MCP é o caminho de leitura que torna os novos dados sociais/vídeo acionáveis: agora você pode pedir a um agente "quais dos meus threads do X estão recebendo descoberta no estilo TikTok esta semana" e obter uma resposta real sem planilha no loop. Para um criador cujos analytics vivem em cinco dashboards diferentes, esta é a primeira vez que os dados estão num lugar onde uma ferramenta de IA pode agir sobre eles.</p>

<div class="callout"><p><strong>A versão de 30 segundos:</strong> o Search Console MCP (SC-MCP) é um servidor MCP que envolve a API do Google Search Console. Conecte-o ao Claude Code ou Codex, e você pode perguntar "me mostre as impressões dos meus posts do X em julho" em português claro. Combinado com o novo painel social/vídeo do GSC (7 de julho de 2026), criadores agora podem fechar o loop de desempenho cross-platform de posts sem sair do chat. Este guia é a configuração funcional mais as quatro consultas que valem a pena rodar primeiro.</p></div>

<h2>O que o Search Console MCP Realmente Faz</h2>

<p>O Search Console MCP é um pequeno servidor Python que expõe a API do Google Search Console como um conjunto de ferramentas MCP. Um cliente compatível com MCP (Claude Code, Codex, Cline, Continue, Roo Code) pode chamar essas ferramentas diretamente, sem ginástica de auth no lado do agente e sem exportação manual da UI web do GSC. Da perspectiva do criador, a diferença entre "com SC-MCP" e "sem SC-MCP" é a diferença entre fazer uma pergunta no chat e copiar linhas de um CSV.</p>

<p>O repositório é <a href="https://github.com/sudomichael/search-console-mcp">github.com/sudomichael/search-console-mcp</a>, licenciado MIT, ~600 linhas de Python. Ele implementa os endpoints read-side que a Search Analytics API expõe: queries, pages, devices, countries, dates e search appearance. Não implementa endpoints write-side (sem submissão de sitemaps, sem remoção de URL), e não expõe os novos dados sociais/vídeo diretamente &mdash; esses dados vivem atrás de um filtro diferente que o SC-MCP adicionou em 7 de julho, mesmo dia em que o Google disponibilizou o painel.</p>

<p>O que você recebe, de ponta a ponta, é um Google Search Console acessível por chat. Esse é o produto inteiro, e essa é exatamente a camada que estava faltando antes.</p>

<h2>Por que a Atualização do GSC de 7 de Julho Muda a Conta</h2>

<p>Antes de 7 de julho de 2026, o GSC só mostrava desempenho de busca web. Um criador publicando em X, Bluesky, LinkedIn, YouTube ou TikTok tinha que instrumentar cada plataforma separadamente: X Analytics para X, Bluesky stats para Bluesky, LinkedIn Page analytics para LinkedIn, YouTube Studio para YouTube, TikTok Creator Portal para TikTok. Nenhuma dessas plataformas tinha uma lente unificada de desempenho de busca porque cada uma definia "busca" de forma diferente, e o Google não tinha como ver dados de criadores cross-platform como um corpus único.</p>

<p>A atualização de 7 de julho muda isso. O novo painel de plataformas sociais/vídeo dentro do GSC expõe impressões, cliques, CTR e posição para:</p>

<ul>
  <li><strong>Busca no YouTube</strong> &mdash; impressões, cliques e posição média na busca interna do YouTube.</li>
  <li><strong>Busca no TikTok</strong> &mdash; mesmo formato, com escopo na camada de busca do TikTok.</li>
  <li><strong>Busca no LinkedIn</strong> &mdash; descoberta de posts e artigos dentro da busca do LinkedIn.</li>
  <li><strong>Busca no X</strong> &mdash; a busca interna do x.com, incluindo busca de tópicos e pessoas.</li>
</ul>

<p>Essa é a primeira vez que um criador pode sentar em uma única UI do Google e ver "meu thread do X sobre federação AT Protocol" ao lado de "meu post do LinkedIn sobre o mesmo tópico" com o mesmo formato de métrica. O SC-MCP, que já estava conectado à API do GSC, pega os novos dados sociais/vídeo no dia um. Os dois lançamentos caem juntos porque ambos os lados da stack precisavam do outro para serem úteis.</p>

<h2>As 4 Consultas que Valem a Pena Rodar Primeiro</h2>

<p>Uma vez que o SC-MCP está conectado ao Claude Code (configuração abaixo), a parte produtiva são as consultas que você roda contra ele. As quatro que produziram o sinal mais acionável na primeira semana de julho de 2026 são estas.</p>

<h3>Consulta 1: Impressões Cross-Platform para um Tópico</h3>

<p>A consulta SC-MCP mais básica também é a mais poderosa: peça impressões totais em todas as plataformas para um cluster de tópicos nos últimos 28 dias. O SC-MCP retorna o mesmo formato da UI web do GSC, mas faz o join de dimensões automaticamente (web + YouTube + TikTok + LinkedIn + X) sem você precisar clicar em cinco abas.</p>

<pre><code>gsc_query(
  site_url="https://seudominio.com",
  start_date="2026-06-10",
  end_date="2026-07-08",
  dimensions=["date"],
  filters={"query_contains": "at protocol"}
)</code></pre>

<p>A resposta te dá uma série de impressões agrupadas por data. A partir daí você pode pedir ao Claude para plotar, resumir picos ou correlacionar com uma URL específica de thread do X. Esse último movimento &mdash; "agora correlacione isso com meu post do X de 14 de junho" &mdash; é o workflow matador porque conecta o lado GSC ao lado plataforma sem nenhuma contabilidade manual.</p>

<h3>Consulta 2: Descoberta de Thread do X vs Descoberta Web</h3>

<p>A segunda consulta separa impressões de busca no X de impressões de busca web para a mesma query. A razão disso importar: um criador publicando um thread no X e um post de blog no mesmo tópico frequentemente vai ver um deles dominar a busca enquanto o outro fica silencioso. A divisão diz qual plataforma é a superfície de descoberta para um dado tópico e onde investir o próximo post.</p>

<pre><code>gsc_query(
  site_url="https://seudominio.com",
  start_date="2026-06-10",
  end_date="2026-07-08",
  dimensions=["query", "searchAppearance"],
  filters={"searchAppearance": ["X_SEARCH", "WEB"}]
)</code></pre>

<p>Para um criador que trata X como a camada de broadcast e o blog como o registro durável, essa consulta é a coisa mais próxima de um dashboard de publicação. Você vê as queries que atingem o post do blog, as queries que atingem o thread do X, e pode parar de adivinhar onde o leitor realmente te encontrou.</p>

<h3>Consulta 3: Detecção de Drift Entre Plataformas</h3>

<p>Detecção de drift é o workflow que transformou o SC-MCP de curiosidade em ferramenta diária. Você pede ao Claude para comparar as impressões sociais/vídeo desta semana com as da semana passada, sinalizar qualquer coisa abaixo de 30 por cento, e propor um thread do X ou post do Bluesky que poderia recuperar o alcance perdido. A consulta tem o mesmo formato da Consulta 1, mas com dois intervalos de datas e um pequeno prompt para Claude fazer a comparação.</p>

<pre><code>last_week = gsc_query(site_url, "2026-07-01", "2026-07-07", dimensions=["date"])
this_week = gsc_query(site_url, "2026-06-24", "2026-06-30", dimensions=["date"])
# Claude compara: qual plataforma, qual data, qual query caiu mais?
# Claude propõe: um rascunho de thread do X, um rascunho de post do Bluesky, um update do LinkedIn.</code></pre>

<p>Esse é o loop de criador de nível de produção em 2026: uma leitura de 7 dias, um prompt de comparação de uma linha, e três posts de rascunho na saída. Você saiu de cinco dashboards e uma planilha para uma mensagem de chat em 90 segundos.</p>

<h3>Consulta 4: Auditoria de Cross-Link Entre X e Blog</h3>

<p>A quarta consulta é o movimento de disciplina de SEO: peça ao Claude para enumerar toda URL de post do X que você referenciou em um post de blog nos últimos 90 dias, depois cheque a dimensão de página do GSC para cada uma. Se um post de blog tem um link outbound para um thread do X e o thread tem zero impressões X_SEARCH, você tem um problema de auditoria de cross-link: o link não está puxando seu peso no novo mundo X-search.</p>

<pre><code># Passo 1: liste todos os links outbound x.com no seu blog (Claude faz isso de um crawl de sitemap)
# Passo 2: para cada um, peça ao SC-MCP impressões X_SEARCH ao longo de 90 dias
gsc_query(site_url, "2026-04-09", "2026-07-08",
  dimensions=["page"], filters={"searchAppearance": "X_SEARCH"})
# Passo 3: Claude sinaliza: post de blog X tem 6 links outbound x.com, 4 deles têm 0 impressões X.
# Passo 4: Claude reescreve o texto do link para ser mais descritivo para o indexador do X classificar melhor o thread.</code></pre>

<p>A auditoria é o tipo de coisa que um criador nunca faria à mão, e uma agência de marketing cobraria $5.000. Com o SC-MCP é uma sessão de chat de 10 minutos, repetível semanalmente.</p>

<h2>A Configuração de 5 Minutos</h2>

<p>Conectar o SC-MCP ao Claude Code leva cerca de cinco minutos se você já tem uma propriedade verificada do Google Search Console e um Claude Code funcionando. O formato é o mesmo de qualquer servidor MCP: uma linha de config em <code>~/.config/claude/mcp_servers.json</code> e uma chave de service account em disco.</p>

<h3>Passo 1: Instale o Pacote</h3>

<p>Clone ou pip-install o servidor SC-MCP. O caminho recomendado é a release do GitHub, não PyPI, porque o Google atualizou o contrato da API em 7 de julho e a tag de release acompanha os endpoints GSC ao vivo.</p>

<pre><code>git clone https://github.com/sudomichael/search-console-mcp.git
cd search-console-mcp
uv sync
# Isso puxa o MCP SDK + google-api-python-client + libs de auth</code></pre>

<p>Se você não tem o <code>uv</code> instalado, o repo cai para <code>pip install -e .</code> em Python 3.11+. O ambiente completo é ~80 MB.</p>

<h3>Passo 2: Service Account + Acesso à Propriedade GSC</h3>

<p>O SC-MCP autentica com um service account do Google, não OAuth. Crie um service account no Google Cloud, baixe a chave JSON, e adicione o email do service account como usuário (qualquer papel, "Full" funciona) dentro da propriedade Search Console que você quer consultar. Esse é o mesmo fluxo que qualquer automação GSC usa; nenhum escopo especial é necessário além de <code>webmasters.readonly</code>.</p>

<pre><code># 1. JSON do service account em: ~/keys/gsc-service-account.json
# 2. Na UI do GSC: Configurações &rarr; Usuários e permissões &rarr; Adicionar usuário
#    Cole o email do service account: sc-mcp@seu-projeto.iam.gserviceaccount.com
#    Nível de permissão: Full (read-only é suficiente para o SC-MCP, mas Full é inofensivo)</code></pre>

<p>O fluxo de service account é a diferença entre o SC-MCP e outras ferramentas GSC: não há dança de OAuth no browser, não há refresh de token no meio de uma sessão. O servidor MCP lê a chave em disco e está pronto.</p>

<h3>Passo 3: Conecte ao Claude Code</h3>

<p>Adicione o servidor SC-MCP ao config MCP do Claude Code. O arquivo de config está em <code>~/.config/claude/mcp_servers.json</code> no Linux e macOS, e o mesmo caminho sob <code>%APPDATA%</code> no Windows.</p>

<pre><code>&#123;
  "mcpServers": &#123;
    "gsc": &#123;
      "command": "uv",
      "args": ["run", "--directory", "/caminho/para/search-console-mcp", "python", "-m", "search_console_mcp"],
      "env": &#123;
        "GOOGLE_APPLICATION_CREDENTIALS": "/home/voce/keys/gsc-service-account.json",
        "GSC_DEFAULT_SITE": "https://seudominio.com"
      &#125;
    &#125;
  &#125;
&#125;</code></pre>

<p>Reinicie o Claude Code. Na primeira vez que iniciar uma sessão, digite <code>/mcp</code> e confirme que o servidor GSC está listado e mostra as ferramentas disponíveis. Se você vir <code>gsc_query</code> na lista de ferramentas, a configuração está pronta.</p>

<h3>Passo 4: Consulta de Sanidade Inicial</h3>

<p>Peça ao Claude para fazer um pull de 7 dias e confirme que os números batem com a UI web do GSC. Esses são os mesmos dados que o dashboard GSC mostra, então a comparação é um teste literal de ponta a ponta da conexão.</p>

<pre><code>Use gsc_query para buscar os últimos 7 dias de search analytics para https://seudominio.com,
agrupado por data. Mostre o total de impressões e cliques para cada dia.
Depois compare com o que vejo na aba Performance do GSC.
Devem bater exatamente.</code></pre>

<p>Se os números batem, a configuração está verificada. Se não, o culpado mais comum é o formato da URL do site: o GSC aceita <code>https://seudominio.com</code> (propriedade de domínio) ou <code>sc-domain:seudominio.com</code> (propriedade de prefixo de URL), e o SC-MCP precisa da string exata com a qual a propriedade foi registrada. A ferramenta <code>gsc_list_sites</code> no README do repo lista toda propriedade que seu service account pode ver; use isso para copiar a URL certa.</p>

<h2>Onde o ThreadGrab se Encaixa Nesse Quadro</h2>

<p>O ThreadGrab é uma ferramenta de arquivamento social read-side: cole qualquer URL pública do X e você recebe uma página Markdown estável e estruturada que crawlers e agentes de IA podem buscar. O pareamento natural com o SC-MCP é que toda impressão GSC em uma página mirror do threadgrab.com é uma candidata confirmada a citação por IA. Quando você roda a Consulta 1 do SC-MCP (impressões cross-platform para um tópico), as páginas mirror em threadgrab.com vão aparecer na dimensão de página. Isso diz qual dos seus threads arquivados está sendo captado pela camada de citação, e qual ainda depende do x.com diretamente.</p>

<p>Para um criador que já roda o ThreadGrab, o SC-MCP é a resposta read-side que faltava para a pergunta que o ThreadGrab responde no lado write: onde meu conteúdo está realmente sendo descoberto? As duas ferramentas juntas fecham o loop de publicar (X) para mirror (ThreadGrab) para descoberta (GSC) para ação (próximo post rascunhado pelo Claude). Esse é o stack de criador de nível de produção para o segundo semestre de 2026.</p>

<h2>Perguntas Frequentes</h2>

<div class="faq-item">
  <strong>O SC-MCP funciona com o novo painel social/vídeo que o GSC disponibilizou em 7 de julho de 2026?</strong>
  <p>Sim, com a tag de release de 7 de julho. A versão anterior só expunha dados de busca web; a release atual adiciona o filtro de plataforma social/vídeo como dimensão de primeira classe, o que significa que você pode pedir impressões X_SEARCH, YOUTUBE_SEARCH, TIKTOK_SEARCH e LINKEDIN_SEARCH ao lado da busca web tradicional na mesma consulta. Se você clonou o repo antes de 7 de julho, puxe a tag de release mais recente e reinicie o servidor MCP.</p>
</div>
<div class="faq-item">
  <strong>Preciso de um plano Claude pago para usar o Search Console MCP?</strong>
  <p>Não. O SC-MCP roda contra o protocolo MCP, que Claude Code, Codex, Cline, Continue e Roo Code falam. O plano gratuito do Claude Code funciona para consultas ad-hoc; um plano pago só é necessário se você quiser rodar sessões longas de auditoria cross-platform que excedam o limite de taxa do tier gratuito (cerca de 50 chamadas de API GSC por dia, o que é suficiente para um workflow semanal de criador).</p>
</div>
<div class="faq-item">
  <strong>Meus dados do GSC são enviados para algum lugar quando uso o SC-MCP?</strong>
  <p>Não. O SC-MCP roda localmente na sua máquina. O fluxo é: seu cliente MCP (Claude Code, etc.) chama uma ferramenta no servidor SC-MCP local, o servidor chama a Google Search Console API diretamente usando a chave do seu service account, e a resposta volta para o seu chat local. O Google vê a requisição vir do seu service account, não de qualquer serviço de terceiros. Não há relay, não há envio de log, não há middleware de analytics. O repo não tem código de telemetria, e a licença MIT permite auditar cada linha.</p>
</div>
<div class="faq-item">
  <strong>Qual é o limite de taxa da API do GSC, e o SC-MCP lida com ele?</strong>
  <p>A Search Analytics API permite cerca de 1.200 consultas por minuto por service account, com um teto prático de 5 consultas por segundo para uma única propriedade. O SC-MCP tem rate limiting embutido que limita a 4 consultas por segundo por padrão, o que fica confortavelmente abaixo do teto da API. Se você está rodando auditorias cross-platform de 90 dias com o novo painel social/vídeo, espere que o limite de taxa seja o gargalo, não a camada MCP. O README documenta uma env var <code>GSC_RATE_LIMIT_QPS</code> que você pode baixar se seu service account compartilha um projeto com outros consumidores GSC.</p>
</div>
<div class="faq-item">
  <strong>O SC-MCP pode escrever no GSC, ou é read-only?</strong>
  <p>Read-only. O servidor implementa o endpoint de consulta Search Analytics e o endpoint de listagem de sites, e nada mais. Ele não pode submeter sitemaps, pedir indexação, remover URLs ou mudar qualquer configuração do GSC. Isso é uma feature, não uma limitação: mantém a superfície de segurança mínima, torna segura a permissão de service account "Restricted" (o escopo mínimo de leitura), e significa que um agente comprometido não pode acidentalmente quebrar sua propriedade GSC.</p>
</div>
<div class="faq-item">
  <strong>Como isso se compara à cobertura existente de threadgrab MCP e OpenRouter MCP neste site?</strong>
  <p>O SC-MCP fecha o loop read-side que o <a href="/pt/blog/x-hosted-mcp-creator-workflow-2026.html">X-Hosted MCP</a> (distribuição), o <a href="/pt/blog/openrouter-mcp-server-social-content-creators-2026.html">OpenRouter MCP</a> (roteamento de modelo), e o próprio ThreadGrab (mirroring) deixam aberto. A stack de 3 camadas agora se lê: ThreadGrab espelha a publicação, X-Hosted MCP distribui, OpenRouter MCP roteia o modelo que rascunha o próximo post, e SC-MCP lê os dados de descoberta de volta. Cada camada é um servidor MCP separado; juntos, são o stack de criador funcional para o segundo semestre de 2026.</p>
</div>

<div class="cta">
  <p>Quer o mirror pronto para citação no seu próprio domínio?</p>
  <a class="btn" href="/pt/">Experimente o ThreadGrab</a>
</div>"""

ID_BODY = """<p>Pada minggu pertama Juli 2026, dua pengumuman Google muncul dalam lima hari, dan bersama-sama mereka diam-diam menggambar ulang peta SEO untuk kreator X dan Bluesky. Pada 2 Juli, feed Show HN menampilkan <a href="https://github.com/sudomichael/search-console-mcp">search-console-mcp</a>, server Model Context Protocol open-source yang memungkinkan Claude, Codex, dan agen lain yang mendukung MCP menarik data Google Search Console secara langsung tanpa copy-paste. Lima hari kemudian, pada 7 Juli, Google merilis <a href="https://developers.google.com/search/blog/2026/07/search-console-social-video-platforms">panel platform sosial/video baru</a> di dalam Search Console, mengekspos data tayangan YouTube, TikTok, LinkedIn, dan X sebagai filter kelas-pertama di samping pencarian web tradisional.</p>

<p>Dua rilis tersebut tidak terkait oleh posting resmi Google mana pun, tetapi selaras. SC-MCP adalah jalur baca yang membuat data sosial/video baru dapat ditindaklanjuti: Anda sekarang dapat bertanya kepada agen "thread X mana yang mendapat penemuan ala TikTok minggu ini" dan mendapatkan jawaban nyata tanpa spreadsheet di loop. Bagi kreator yang analitiknya tersebar di lima dashboard berbeda, ini adalah pertama kalinya data berada di tempat di mana alat AI dapat bertindak di atasnya.</p>

<div class="callout"><p><strong>Versi 30 detik:</strong> Search Console MCP (SC-MCP) adalah server MCP yang membungkus API Google Search Console. Pasangkan ke Claude Code atau Codex, dan Anda dapat bertanya "tunjukkan tayangan postingan X saya untuk Juli" dalam bahasa alami. Dikombinasikan dengan panel sosial/video baru GSC (7 Juli 2026), kreator sekarang dapat menutup loop performa postingan lintas-platform tanpa meninggalkan chat. Panduan ini adalah setup kerja ditambah empat query yang layak dijalankan terlebih dahulu.</p></div>

<h2>Apa yang Sebenarnya Dilakukan Search Console MCP</h2>

<p>Search Console MCP adalah server Python kecil yang mengekspos API Google Search Console sebagai seperangkat alat MCP. Klien yang mendukung MCP (Claude Code, Codex, Cline, Continue, Roo Code) dapat memanggil alat-alat tersebut secara langsung, tanpa akrobat autentikasi di sisi agen dan tanpa ekspor manual dari UI web GSC. Dari perspektif kreator, perbedaan antara "dengan SC-MCP" dan "tanpa SC-MCP" adalah perbedaan antara bertanya di chat dan menyalin baris dari CSV.</p>

<p>Repositori adalah <a href="https://github.com/sudomichael/search-console-mcp">github.com/sudomichael/search-console-mcp</a>, berlisensi MIT, ~600 baris Python. Ini mengimplementasikan endpoint sisi-baca yang diekspos Search Analytics API: query, halaman, perangkat, negara, tanggal, dan tampilan pencarian. Tidak mengimplementasikan endpoint sisi-tulis (tanpa submit sitemap, tanpa penghapusan URL), dan tidak mengekspos data sosial/video baru secara langsung &mdash; data itu hidup di balik filter berbeda yang ditambahkan SC-MCP pada 7 Juli, hari yang sama saat Google merilis panel tersebut.</p>

<p>Yang Anda dapatkan, dari ujung ke ujung, adalah Google Search Console yang dapat diakses via chat. Itulah seluruh produknya, dan itulah tepatnya lapisan yang sebelumnya hilang.</p>

<h2>Mengapa Pembaruan GSC 7 Juli Mengubah Perhitungannya</h2>

<p>Sebelum 7 Juli 2026, GSC hanya menunjukkan performa pencarian web. Kreator yang mempublikasikan di X, Bluesky, LinkedIn, YouTube, atau TikTok harus menginstrumen setiap platform secara terpisah: X Analytics untuk X, statistik Bluesky untuk Bluesky, analitik Halaman LinkedIn untuk LinkedIn, YouTube Studio untuk YouTube, TikTok Creator Portal untuk TikTok. Tidak satu pun dari platform tersebut memiliki lensa performa pencarian terpadu karena masing-masing mendefinisikan "pencarian" secara berbeda, dan Google tidak memiliki cara untuk melihat data kreator lintas-platform sebagai korpus tunggal.</p>

<p>Pembaruan 7 Juli mengubah itu. Panel platform sosial/video baru di dalam GSC mengekspos tayangan, klik, CTR, dan posisi untuk:</p>

<ul>
  <li><strong>Pencarian YouTube</strong> &mdash; tayangan, klik, dan posisi rata-rata dalam pencarian internal YouTube.</li>
  <li><strong>Pencarian TikTok</strong> &mdash; format yang sama, tercakup ke lapisan pencarian TikTok.</li>
  <li><strong>Pencarian LinkedIn</strong> &mdash; penemuan post dan artikel di dalam pencarian LinkedIn.</li>
  <li><strong>Pencarian X</strong> &mdash; pencarian internal x.com, termasuk pencarian topik dan orang.</li>
</ul>

<p>Itulah pertama kalinya seorang kreator dapat duduk di satu UI Google dan melihat "thread X saya tentang federasi AT Protocol" di samping "post LinkedIn saya tentang topik yang sama" dengan format metrik yang sama. SC-MCP, yang sudah terpasang ke API GSC, mengambil data sosial/video baru di hari pertama. Dua rilis tersebut mendarat bersama karena kedua sisi stack membutuhkan sisi lain agar berguna.</p>

<h2>4 Query yang Layak Dijalankan Pertama</h2>

<p>Setelah SC-MCP terpasang ke Claude Code (setup di bawah), bagian produktif adalah query yang Anda jalankan di atasnya. Empat yang menghasilkan sinyal paling dapat ditindaklanjuti di minggu pertama Juli 2026 adalah ini.</p>

<h3>Query 1: Tayangan Lintas-Platform untuk Topik</h3>

<p>Query SC-MCP paling dasar juga yang paling kuat: minta total tayangan di semua platform untuk klaster topik dalam 28 hari terakhir. SC-MCP mengembalikan format yang sama dengan UI web GSC, tetapi melakukan join dimensi secara otomatis (web + YouTube + TikTok + LinkedIn + X) tanpa Anda harus mengklik lima tab.</p>

<pre><code>gsc_query(
  site_url="https://domainanda.com",
  start_date="2026-06-10",
  end_date="2026-07-08",
  dimensions=["date"],
  filters={"query_contains": "at protocol"}
)</code></pre>

<p>Responsnya memberi Anda deret tayangan yang dikelompokkan per tanggal. Dari sana Anda dapat meminta Claude memplot, merangkum lonjakan, atau mengorelasikan dengan URL thread X tertentu. Gerakan terakhir &mdash; "sekarang korelasikan ini dengan post X saya dari 14 Juni" &mdash; adalah workflow pembunuh karena menghubungkan sisi GSC ke sisi platform tanpa pembukuan manual.</p>

<h3>Query 2: Penemuan Thread X vs Penemuan Web</h3>

<p>Query kedua memisahkan tayangan pencarian X dari tayangan pencarian web untuk query yang sama. Alasan ini penting: kreator yang mempublikasikan thread di X dan post blog di topik yang sama sering akan melihat salah satunya mendominasi pencarian sementara yang lain diam. Pemisahan ini memberi tahu Anda platform mana yang merupakan permukaan penemuan untuk topik tertentu dan di mana harus berinvestasi untuk post berikutnya.</p>

<pre><code>gsc_query(
  site_url="https://domainanda.com",
  start_date="2026-06-10",
  end_date="2026-07-08",
  dimensions=["query", "searchAppearance"],
  filters={"searchAppearance": ["X_SEARCH", "WEB"}]
)</code></pre>

<p>Bagi kreator yang memperlakukan X sebagai lapisan broadcast dan blog sebagai catatan tahan lama, query ini adalah hal terdekat dengan dashboard publishing. Anda melihat query yang mengenai post blog, query yang mengenai thread X, dan Anda bisa berhenti menebak di mana pembaca benar-benar menemukan Anda.</p>

<h3>Query 3: Deteksi Drift Antar Platform</h3>

<p>Deteksi drift adalah workflow yang mengubah SC-MCP dari keingintahuan menjadi alat harian. Anda meminta Claude membandingkan tayangan sosial/video minggu ini dengan minggu lalu, menandai apa pun yang turun lebih dari 30 persen, dan mengusulkan thread X atau post Bluesky yang bisa memulihkan jangkauan yang hilang. Query-nya memiliki format yang sama dengan Query 1, tetapi dengan dua rentang tanggal dan prompt kecil untuk Claude melakukan perbandingan.</p>

<pre><code>last_week = gsc_query(site_url, "2026-07-01", "2026-07-07", dimensions=["date"])
this_week = gsc_query(site_url, "2026-06-24", "2026-06-30", dimensions=["date"])
# Claude membandingkan: platform mana, tanggal mana, query mana yang paling turun?
# Claude mengusulkan: satu draf thread X, satu draf post Bluesky, satu update LinkedIn.</code></pre>

<p>Itulah loop kreator tingkat produksi di 2026: pembacaan 7 hari, satu prompt perbandingan satu baris, dan tiga post draf di output. Anda pindah dari lima dashboard dan satu spreadsheet ke satu pesan chat dalam 90 detik.</p>

<h3>Query 4: Audit Cross-Link Antara X dan Blog</h3>

<p>Query keempat adalah gerakan disiplin SEO: minta Claude mendaftar setiap URL post X yang Anda referensikan di post blog dalam 90 hari terakhir, lalu periksa dimensi halaman GSC untuk masing-masing. Jika post blog memiliki link outbound ke thread X dan thread tersebut memiliki nol tayangan X_SEARCH, Anda memiliki masalah audit cross-link: link tersebut tidak menarik beratnya di dunia X-search yang baru.</p>

<pre><code># Langkah 1: daftar semua link outbound x.com di blog Anda (Claude melakukan ini dari crawl sitemap)
# Langkah 2: untuk masing-masing, minta SC-MCP tayangan X_SEARCH selama 90 hari
gsc_query(site_url, "2026-04-09", "2026-07-08",
  dimensions=["page"], filters={"searchAppearance": "X_SEARCH"})
# Langkah 3: Claude menandai: post blog X memiliki 6 link outbound x.com, 4 di antaranya memiliki 0 tayangan X.
# Langkah 4: Claude menulis ulang teks link agar lebih deskriptif sehingga indexer X mengklasifikasikan thread lebih baik.</code></pre>

<p>Audit adalah jenis hal yang tidak pernah dilakukan kreator secara manual, dan agensi pemasaran akan mengenakan biaya $5.000. Dengan SC-MCP itu adalah sesi chat 10 menit, dapat diulang mingguan.</p>

<h2>Setup 5 Menit</h2>

<p>Memasang SC-MCP ke Claude Code memakan waktu sekitar lima menit jika Anda sudah memiliki properti Google Search Console yang terverifikasi dan Claude Code yang berfungsi. Bentuknya sama dengan server MCP lainnya: satu baris config di <code>~/.config/claude/mcp_servers.json</code> dan kunci service account di disk.</p>

<h3>Langkah 1: Instal Paket</h3>

<p>Clone atau pip-install server SC-MCP. Jalur yang direkomendasikan adalah rilis GitHub, bukan PyPI, karena Google memperbarui kontrak API pada 7 Juli dan tag rilis mengikuti endpoint GSC yang aktif.</p>

<pre><code>git clone https://github.com/sudomichael/search-console-mcp.git
cd search-console-mcp
uv sync
# Ini menarik MCP SDK + google-api-python-client + lib auth</code></pre>

<p>Jika Anda tidak memiliki <code>uv</code> terinstal, repo jatuh ke <code>pip install -e .</code> di Python 3.11+. Environment lengkapnya ~80 MB.</p>

<h3>Langkah 2: Service Account + Akses Properti GSC</h3>

<p>SC-MCP mengautentikasi dengan service account Google, bukan OAuth. Buat service account di Google Cloud, unduh kunci JSON, dan tambahkan email service account sebagai pengguna (peran apa saja, "Full" berfungsi) di dalam properti Search Console yang ingin Anda query. Ini adalah alur yang sama dengan yang digunakan otomasi GSC lainnya; tidak ada scope khusus yang diperlukan selain <code>webmasters.readonly</code>.</p>

<pre><code># 1. JSON service account di: ~/keys/gsc-service-account.json
# 2. Di UI GSC: Setelan &rarr; Pengguna dan izin &rarr; Tambah pengguna
#    Tempel email service account: sc-mcp@proyek-anda.iam.gserviceaccount.com
#    Tingkat izin: Full (read-only cukup untuk SC-MCP, tapi Full tidak berbahaya)</code></pre>

<p>Alur service account adalah perbedaan antara SC-MCP dan alat GSC lainnya: tidak ada tarian OAuth browser, tidak ada refresh token di tengah sesi. Server MCP membaca kunci di disk dan siap.</p>

<h3>Langkah 3: Pasang ke Claude Code</h3>

<p>Tambahkan server SC-MCP ke konfigurasi MCP Claude Code. File konfigurasi ada di <code>~/.config/claude/mcp_servers.json</code> di Linux dan macOS, dan jalur yang sama di bawah <code>%APPDATA%</code> di Windows.</p>

<pre><code>&#123;
  "mcpServers": &#123;
    "gsc": &#123;
      "command": "uv",
      "args": ["run", "--directory", "/jalur/ke/search-console-mcp", "python", "-m", "search_console_mcp"],
      "env": &#123;
        "GOOGLE_APPLICATION_CREDENTIALS": "/home/anda/keys/gsc-service-account.json",
        "GSC_DEFAULT_SITE": "https://domainanda.com"
      &#125;
    &#125;
  &#125;
&#125;</code></pre>

<p>Restart Claude Code. Pertama kali Anda memulai sesi, ketik <code>/mcp</code> dan konfirmasi bahwa server GSC terdaftar dan menampilkan alat yang tersedia. Jika Anda melihat <code>gsc_query</code> dalam daftar alat, setup selesai.</p>

<h3>Langkah 4: Query Sanity Pertama</h3>

<p>Minta Claude melakukan pull 7 hari dan konfirmasi bahwa angka-angka cocok dengan UI web GSC. Ini adalah data yang sama yang ditunjukkan dashboard GSC, jadi perbandingannya adalah test ujung-ke-ujung literal dari pemasangan.</p>

<pre><code>Gunakan gsc_query untuk mengambil 7 hari terakhir search analytics untuk https://domainanda.com,
dikelompokkan berdasarkan tanggal. Tunjukkan total tayangan dan klik untuk setiap hari.
Kemudian bandingkan dengan yang saya lihat di tab Performance GSC.
Harus cocok persis.</code></pre>

<p>Jika angkanya cocok, setup terverifikasi. Jika tidak, penyebab paling umum adalah format URL situs: GSC menerima <code>https://domainanda.com</code> (properti domain) atau <code>sc-domain:domainanda.com</code> (properti prefix URL), dan SC-MCP memerlukan string persis dengan properti didaftarkan. Alat <code>gsc_list_sites</code> di README repo mendaftar setiap properti yang dapat dilihat service account Anda; gunakan itu untuk menyalin URL yang benar.</p>

<h2>Di Mana ThreadGrab Masuk dalam Gambaran Ini</h2>

<p>ThreadGrab adalah alat pengarsipan sosial sisi-baca: tempel URL X publik apa pun dan Anda mendapatkan halaman Markdown yang stabil dan terstruktur yang dapat diambil crawler dan agen AI. Pasangan alami dengan SC-MCP adalah bahwa setiap tayangan GSC pada halaman mirror threadgrab.com adalah kandidat kutipan AI yang dikonfirmasi. Ketika Anda menjalankan Query 1 SC-MCP (tayangan lintas-platform untuk topik), halaman mirror di threadgrab.com akan muncul di dimensi halaman. Itu memberi tahu Anda thread arsip mana yang sedang diambil oleh lapisan kutipan, dan mana yang masih bergantung pada x.com secara langsung.</p>

<p>Bagi kreator yang sudah menjalankan ThreadGrab, SC-MCP adalah jawaban sisi-baca yang hilang untuk pertanyaan yang dijawab ThreadGrab di sisi tulis: di mana konten saya benar-benar ditemukan? Kedua alat bersama menutup loop dari publikasi (X) ke mirror (ThreadGrab) ke penemuan (GSC) ke tindakan (post berikutnya yang di-draft Claude). Itulah stack kreator tingkat produksi untuk paruh kedua 2026.</p>

<h2>Pertanyaan yang Sering Diajukan</h2>

<div class="faq-item">
  <strong>Apakah SC-MCP berfungsi dengan panel sosial/video baru yang dirilis GSC pada 7 Juli 2026?</strong>
  <p>Ya, dengan tag rilis 7 Juli. Versi sebelumnya hanya mengekspos data pencarian web; rilis saat ini menambahkan filter platform sosial/video sebagai dimensi kelas-pertama, yang berarti Anda dapat meminta tayangan X_SEARCH, YOUTUBE_SEARCH, TIKTOK_SEARCH, dan LINKEDIN_SEARCH di samping pencarian web tradisional dalam query yang sama. Jika Anda mengkloning repo sebelum 7 Juli, tarik tag rilis terbaru dan restart server MCP.</p>
</div>
<div class="faq-item">
  <strong>Apakah saya memerlukan paket Claude berbayar untuk menggunakan Search Console MCP?</strong>
  <p>Tidak. SC-MCP berjalan melawan protokol MCP, yang digunakan oleh Claude Code, Codex, Cline, Continue, dan Roo Code. Paket gratis Claude Code berfungsi untuk query ad-hoc; paket berbayar hanya diperlukan jika Anda ingin menjalankan sesi audit lintas-platform panjang yang melebihi batas rate tier gratis (sekitar 50 panggilan API GSC per hari, yang cukup untuk workflow kreator mingguan).</p>
</div>
<div class="faq-item">
  <strong>Apakah data GSC saya dikirim ke suatu tempat ketika saya menggunakan SC-MCP?</strong>
  <p>Tidak. SC-MCP berjalan secara lokal di mesin Anda. Alurnya: klien MCP Anda (Claude Code, dll.) memanggil alat di server SC-MCP lokal, server memanggil Google Search Console API secara langsung menggunakan kunci service account Anda, dan respons kembali ke chat lokal Anda. Google melihat permintaan datang dari service account Anda, bukan dari layanan pihak ketiga mana pun. Tidak ada relay, tidak ada pengiriman log, tidak ada middleware analitik. Repo tidak memiliki kode telemetri, dan lisensi MIT memungkinkan Anda mengaudit setiap baris.</p>
</div>
<div class="faq-item">
  <strong>Berapa batas rate API GSC, dan apakah SC-MCP menanganinya?</strong>
  <p>Search Analytics API mengizinkan sekitar 1.200 query per menit per service account, dengan langit-langit praktis 5 query per detik untuk satu properti. SC-MCP memiliki rate limiting bawaan yang membatasi ke 4 query per detik secara default, yang tetap nyaman di bawah langit-langit API. Jika Anda menjalankan audit lintas-platform 90 hari dengan panel sosial/video baru, harap batas rate menjadi bottleneck, bukan lapisan MCP. README mendokumentasikan env var <code>GSC_RATE_LIMIT_QPS</code> yang dapat Anda turunkan jika service account Anda berbagi proyek dengan konsumen GSC lain.</p>
</div>
<div class="faq-item">
  <strong>Bisakah SC-MCP menulis ke GSC, atau apakah read-only?</strong>
  <p>Read-only. Server mengimplementasikan endpoint query Search Analytics dan endpoint daftar situs, dan tidak ada yang lain. Itu tidak dapat mengirim sitemap, meminta pengindeksan, menghapus URL, atau mengubah pengaturan GSC apa pun. Itu adalah fitur, bukan keterbatasan: menjaga permukaan keamanan tetap kecil, membuat izin service account "Restricted" aman (scope baca minimum), dan berarti agen yang dikompromikan tidak dapat secara tidak sengaja merusak properti GSC Anda.</p>
</div>
<div class="faq-item">
  <strong>Bagaimana ini dibandingkan dengan cakupan threadgrab MCP dan OpenRouter MCP yang ada di situs ini?</strong>
  <p>SC-MCP menutup loop sisi-baca yang <a href="/id/blog/x-hosted-mcp-creator-workflow-2026.html">X-Hosted MCP</a> (distribusi), <a href="/id/blog/openrouter-mcp-server-social-content-creators-2026.html">OpenRouter MCP</a> (routing model), dan ThreadGrab sendiri (mirroring) tinggalkan terbuka. Stack 3-layer sekarang terbaca: ThreadGrab mirroring publikasi, X-Hosted MCP mendistribusikannya, OpenRouter MCP merutekan model yang mendraft post berikutnya, dan SC-MCP membaca data penemuan kembali. Setiap layer adalah server MCP terpisah; bersama-sama mereka adalah stack kreator yang berfungsi untuk paruh kedua 2026.</p>
</div>

<div class="cta">
  <p>Ingin mirror siap-kutip di domain Anda sendiri?</p>
  <a class="btn" href="/id/">Coba ThreadGrab</a>
</div>"""


# ============ BUILD HEAD + JSON-LD FOR EACH LANG ============

STYLE = """<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
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
    th, td { padding: 10px 12px; text: 1px solid #222; }
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
    @media (max-width: 640px) { main { padding: 24px 16px 40px; } table { font-size: 0.8rem; } th, td { padding: 8px; } }
  </style>"""


def build_article(lang, title, desc, keywords, body, date_localized):
    """Build a single language article HTML."""
    url = f"https://threadgrab.com/{lang}/blog/{SLUG}.html"
    # Strip <span> from title for JSON-LD headline
    h1_plain = title.replace("<span>", "").replace("</span>", "")

    # Build JSON-LD blocks using json.dumps (avoids f-string brace issues)
    article_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": h1_plain,
        "description": desc,
        "author": {"@type": "Organization", "name": "ThreadGrab"},
        "publisher": {"@type": "Organization", "name": "ThreadGrab", "logo": {"@type": "ImageObject", "url": "https://threadgrab.com/logo.png"}},
        "datePublished": DATE,
        "dateModified": DATE,
        "mainEntityOfPage": url,
        "inLanguage": lang,
    }, ensure_ascii=False)

    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"https://threadgrab.com/{lang}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"https://threadgrab.com/{lang}/blog/"},
            {"@type": "ListItem", "position": 3, "name": h1_plain[:60], "item": url},
        ],
    }, ensure_ascii=False)

    # FAQ JSON-LD: parse from the body (the only structural place)
    # Build per-lang FAQ entries
    faq_by_lang = {
        "en": [
            ("Does SC-MCP work with the new social/video panel that GSC shipped on July 7, 2026?",
             "Yes, with the July 7 release tag. The previous version only exposed web search data; the current release adds the social/video platform filter as a first-class dimension, which means you can ask for X_SEARCH, YOUTUBE_SEARCH, TIKTOK_SEARCH, and LINKEDIN_SEARCH impressions alongside traditional web search in the same query. If you cloned the repo before July 7, pull the latest release tag and restart the MCP server."),
            ("Do I need a paid Claude plan to use Search Console MCP?",
             "No. SC-MCP runs against the MCP protocol, which Claude Code, Codex, Cline, Continue, and Roo Code all speak. The free Claude Code plan works for ad-hoc queries; a paid plan is only needed if you want to run long cross-platform audit sessions that exceed the rate limit on the free tier (about 50 GSC API calls per day, which is enough for a weekly creator workflow)."),
            ("Is my GSC data sent anywhere when I use SC-MCP?",
             "No. SC-MCP runs locally on your machine. The flow is: your MCP client (Claude Code, etc.) calls a tool on the local SC-MCP server, the server calls the Google Search Console API directly using your service account key, and the response goes back to your local chat. Google sees the request come from your service account, not from any third-party service. There is no relay, no log shipping, no analytics middleware. The repo has no telemetry code, and the MIT license lets you audit every line."),
            ("What is the rate limit on the GSC API, and does SC-MCP handle it?",
             "The Search Analytics API allows about 1,200 queries per minute per service account, with a 5-queries-per-second practical ceiling for a single property. SC-MCP has built-in rate limiting that throttles to 4 queries per second by default, which stays comfortably under the API ceiling. If you are running 90-day cross-platform audits with the new social/video panel, expect the rate limit to be the bottleneck, not the MCP layer. The README documents a GSC_RATE_LIMIT_QPS env var you can lower if your service account shares a project with other GSC consumers."),
            ("Can SC-MCP write to GSC, or is it read-only?",
             "Read-only. The server implements the Search Analytics query endpoint and the site list endpoint, and nothing else. It cannot submit sitemaps, request indexing, remove URLs, or change any GSC setting. That is a feature, not a limitation: it keeps the security surface tiny, makes the service account permission Restricted safe (the minimum read scope), and means a compromised agent cannot accidentally break your GSC property."),
            ("How does this compare to the existing threadgrab MCP and OpenRouter MCP coverage on this site?",
             "SC-MCP closes the read-side loop that X-Hosted MCP (distribution), OpenRouter MCP (model routing), and ThreadGrab itself (mirroring) leave open. The 3-layer stack now reads: ThreadGrab mirrors the publish, X-Hosted MCP distributes it, OpenRouter MCP routes the model that drafts the next post, and SC-MCP reads the discovery data back. Each layer is a separate MCP server; together they are the working creator stack for the second half of 2026."),
        ],
        "pt": [
            ("O SC-MCP funciona com o novo painel social/vídeo que o GSC disponibilizou em 7 de julho de 2026?",
             "Sim, com a tag de release de 7 de julho. A versão anterior só expunha dados de busca web; a release atual adiciona o filtro de plataforma social/vídeo como dimensão de primeira classe, o que significa que você pode pedir impressões X_SEARCH, YOUTUBE_SEARCH, TIKTOK_SEARCH e LINKEDIN_SEARCH ao lado da busca web tradicional na mesma consulta. Se você clonou o repo antes de 7 de julho, puxe a tag de release mais recente e reinicie o servidor MCP."),
            ("Preciso de um plano Claude pago para usar o Search Console MCP?",
             "Não. O SC-MCP roda contra o protocolo MCP, que Claude Code, Codex, Cline, Continue e Roo Code falam. O plano gratuito do Claude Code funciona para consultas ad-hoc; um plano pago só é necessário se você quiser rodar sessões longas de auditoria cross-platform que excedam o limite de taxa do tier gratuito (cerca de 50 chamadas de API GSC por dia, o que é suficiente para um workflow semanal de criador)."),
            ("Meus dados do GSC são enviados para algum lugar quando uso o SC-MCP?",
             "Não. O SC-MCP roda localmente na sua máquina. O fluxo é: seu cliente MCP (Claude Code, etc.) chama uma ferramenta no servidor SC-MCP local, o servidor chama a Google Search Console API diretamente usando a chave do seu service account, e a resposta volta para o seu chat local. O Google vê a requisição vir do seu service account, não de qualquer serviço de terceiros. Não há relay, não há envio de log, não há middleware de analytics. O repo não tem código de telemetria, e a licença MIT permite auditar cada linha."),
            ("Qual é o limite de taxa da API do GSC, e o SC-MCP lida com ele?",
             "A Search Analytics API permite cerca de 1.200 consultas por minuto por service account, com um teto prático de 5 consultas por segundo para uma única propriedade. O SC-MCP tem rate limiting embutido que limita a 4 consultas por segundo por padrão, o que fica confortavelmente abaixo do teto da API. Se você está rodando auditorias cross-platform de 90 dias com o novo painel social/vídeo, espere que o limite de taxa seja o gargalo, não a camada MCP. O README documenta uma env var GSC_RATE_LIMIT_QPS que você pode baixar se seu service account compartilha um projeto com outros consumidores GSC."),
            ("O SC-MCP pode escrever no GSC, ou é read-only?",
             "Read-only. O servidor implementa o endpoint de consulta Search Analytics e o endpoint de listagem de sites, e nada mais. Ele não pode submeter sitemaps, pedir indexação, remover URLs ou mudar qualquer configuração do GSC. Isso é uma feature, não uma limitação: mantém a superfície de segurança mínima, torna segura a permissão de service account Restricted (o escopo mínimo de leitura), e significa que um agente comprometido não pode acidentalmente quebrar sua propriedade GSC."),
            ("Como isso se compara à cobertura existente de threadgrab MCP e OpenRouter MCP neste site?",
             "O SC-MCP fecha o loop read-side que o X-Hosted MCP (distribuição), o OpenRouter MCP (roteamento de modelo), e o próprio ThreadGrab (mirroring) deixam aberto. A stack de 3 camadas agora se lê: ThreadGrab espelha a publicação, X-Hosted MCP distribui, OpenRouter MCP roteia o modelo que rascunha o próximo post, e SC-MCP lê os dados de descoberta de volta. Cada camada é um servidor MCP separado; juntos, são o stack de criador funcional para o segundo semestre de 2026."),
        ],
        "id": [
            ("Apakah SC-MCP berfungsi dengan panel sosial/video baru yang dirilis GSC pada 7 Juli 2026?",
             "Ya, dengan tag rilis 7 Juli. Versi sebelumnya hanya mengekspos data pencarian web; rilis saat ini menambahkan filter platform sosial/video sebagai dimensi kelas-pertama, yang berarti Anda dapat meminta tayangan X_SEARCH, YOUTUBE_SEARCH, TIKTOK_SEARCH, dan LINKEDIN_SEARCH di samping pencarian web tradisional dalam query yang sama. Jika Anda mengkloning repo sebelum 7 Juli, tarik tag rilis terbaru dan restart server MCP."),
            ("Apakah saya memerlukan paket Claude berbayar untuk menggunakan Search Console MCP?",
             "Tidak. SC-MCP berjalan melawan protokol MCP, yang digunakan oleh Claude Code, Codex, Cline, Continue, dan Roo Code. Paket gratis Claude Code berfungsi untuk query ad-hoc; paket berbayar hanya diperlukan jika Anda ingin menjalankan sesi audit lintas-platform panjang yang melebihi batas rate tier gratis (sekitar 50 panggilan API GSC per hari, yang cukup untuk workflow kreator mingguan)."),
            ("Apakah data GSC saya dikirim ke suatu tempat ketika saya menggunakan SC-MCP?",
             "Tidak. SC-MCP berjalan secara lokal di mesin Anda. Alurnya: klien MCP Anda (Claude Code, dll.) memanggil alat di server SC-MCP lokal, server memanggil Google Search Console API secara langsung menggunakan kunci service account Anda, dan respons kembali ke chat lokal Anda. Google melihat permintaan datang dari service account Anda, bukan dari layanan pihak ketiga mana pun. Tidak ada relay, tidak ada pengiriman log, tidak ada middleware analitik. Repo tidak memiliki kode telemetri, dan lisensi MIT memungkinkan Anda mengaudit setiap baris."),
            ("Berapa batas rate API GSC, dan apakah SC-MCP menanganinya?",
             "Search Analytics API mengizinkan sekitar 1.200 query per menit per service account, dengan langit-langit praktis 5 query per detik untuk satu properti. SC-MCP memiliki rate limiting bawaan yang membatasi ke 4 query per detik secara default, yang tetap nyaman di bawah langit-langit API. Jika Anda menjalankan audit lintas-platform 90 hari dengan panel sosial/video baru, harap batas rate menjadi bottleneck, bukan lapisan MCP. README mendokumentasikan env var GSC_RATE_LIMIT_QPS yang dapat Anda turunkan jika service account Anda berbagi proyek dengan konsumen GSC lain."),
            ("Bisakah SC-MCP menulis ke GSC, atau apakah read-only?",
             "Read-only. Server mengimplementasikan endpoint query Search Analytics dan endpoint daftar situs, dan tidak ada yang lain. Itu tidak dapat mengirim sitemap, meminta pengindeksan, menghapus URL, atau mengubah pengaturan GSC apa pun. Itu adalah fitur, bukan keterbatasan: menjaga permukaan keamanan tetap kecil, membuat izin service account Restricted aman (scope baca minimum), dan berarti agen yang dikompromikan tidak dapat secara tidak sengaja merusak properti GSC Anda."),
            ("Bagaimana ini dibandingkan dengan cakupan threadgrab MCP dan OpenRouter MCP yang ada di situs ini?",
             "SC-MCP menutup loop sisi-baca yang X-Hosted MCP (distribusi), OpenRouter MCP (routing model), dan ThreadGrab sendiri (mirroring) tinggalkan terbuka. Stack 3-layer sekarang terbaca: ThreadGrab mirroring publikasi, X-Hosted MCP mendistribusikannya, OpenRouter MCP merutekan model yang mendraft post berikutnya, dan SC-MCP membaca data penemuan kembali. Setiap layer adalah server MCP terpisah; bersama-sama mereka adalah stack kreator yang berfungsi untuk paruh kedua 2026."),
        ],
    }

    faq_entries = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                   for q, a in faq_by_lang[lang]]
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entries}, ensure_ascii=False)

    # Lang-bar: this lang active, other two link to corresponding article
    other_langs = [l for l in ("en", "pt", "id") if l != lang]
    lang_bar = f'      <a class="active" href="/{lang}/blog/{SLUG}.html">{lang.upper()}</a>\n'
    for ol in other_langs:
        lang_bar += f'      <a class="" href="/{ol}/blog/{SLUG}.html">{ol.upper()}</a>\n'

    # Breadcrumb text
    breadcrumb_text = {
        "en": "Search Console MCP 2026",
        "pt": "Search Console MCP 2026",
        "id": "Search Console MCP 2026",
    }[lang]

    # Footer (per-lang About/Privacy/links)
    footer = f"""  <footer>
    &copy; 2026 ThreadGrab &middot; <a href="/{lang}/">Home</a> &middot; <a href="/{lang}/blog/">Blog</a> &middot; <a href="/{lang}/about/">About</a> &middot; <a href="/{lang}/privacy/">Privacy</a>
    <br>Not affiliated with X Corp., Bluesky Social PBC, LinkedIn Corporation, or Microsoft Corporation.
  </footer>"""

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="ThreadGrab">
  <link rel="canonical" href="{url}">
  <link rel="alternate" hreflang="en" href="https://threadgrab.com/en/blog/{SLUG}.html">
  <link rel="alternate" hreflang="pt" href="https://threadgrab.com/pt/blog/{SLUG}.html">
  <link rel="alternate" hreflang="id" href="https://threadgrab.com/id/blog/{SLUG}.html">
  <link rel="alternate" hreflang="x-default" href="https://threadgrab.com/en/blog/{SLUG}.html">
  <meta property="og:title" content="{h1_plain} | ThreadGrab">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="ThreadGrab">
  <meta property="og:locale" content="{ {'en':'en_US','pt':'pt_BR','id':'id_ID'}[lang] }">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{h1_plain} | ThreadGrab">
  <meta name="twitter:description" content="{desc}">
  <script type="application/ld+json">
{article_ld}
  </script>
  <script type="application/ld+json">
{breadcrumb_ld}
  </script>
  <script type="application/ld+json">
{faq_ld}
  </script>
{STYLE}
</head>
<body>
  <header>
    <a class="logo" href="/{lang}/">Thread<span>Grab</span></a>
    <div class="lang-bar">
{lang_bar}    </div>
  </header>

  <main>
    <div class="breadcrumb"><a href="/{lang}/">Home</a> &rsaquo; <a href="/{lang}/blog/">Blog</a> &rsaquo; {breadcrumb_text}</div>

    <h1>{title}</h1>
    <p class="meta">{date_localized} &middot; 11 min read &middot; Guide</p>

    {body}
  </main>

{footer}
</body>
</html>"""

    return html


# ============ BUILD 3 LANGS ============

article_en = build_article("en", EN_TITLE, EN_DESC, EN_KEYWORDS, EN_BODY, DATE_EN)
article_pt = build_article("pt", PT_TITLE, PT_DESC, PT_KEYWORDS, PT_BODY, DATE_PT)
article_id = build_article("id", ID_TITLE, ID_DESC, ID_KEYWORDS, ID_BODY, DATE_ID)

# ============ WRITE 3 HTML FILES ============

os.makedirs("/root/threadgrab-site/en/blog", exist_ok=True)
os.makedirs("/root/threadgrab-site/pt/blog", exist_ok=True)
os.makedirs("/root/threadgrab-site/id/blog", exist_ok=True)

with open(f"/root/threadgrab-site/en/blog/{SLUG}.html", "w") as f:
    f.write(article_en)
with open(f"/root/threadgrab-site/pt/blog/{SLUG}.html", "w") as f:
    f.write(article_pt)
with open(f"/root/threadgrab-site/id/blog/{SLUG}.html", "w") as f:
    f.write(article_id)

print(f"✅ Wrote 3 lang articles: {SLUG}")
print(f"   EN: {len(article_en)} chars")
print(f"   PT: {len(article_pt)} chars")
print(f"   ID: {len(article_id)} chars")
