# -*- coding: utf-8 -*-
"""EN content for search-result-redirects-cloaking-goto-2026."""

CONTENT = {
    'title': 'Search Result Redirects 2026: GOTO, Cloaking, Agent Pay',
    'desc': ("Google's GOTO and Brave's cloaking broke SERP scraping. What it means for creators archiving their posts, and why pay-per-request search wins."),
    'keywords': ("search result redirects, Google GOTO, Brave search cloaking, SERP "
                 "scraping, redirect URL expiry, x402 search API, USDC micropayments, "
                 "AI agent search, archive provenance, ThreadGrab"),
    'body': r"""
<p>Two search engines changed how their result links work in the same week, and for anyone
who archives or monitors social content, that is not a curiosity. On 26 August 2026, Google
began routing clicks on search results through <code>google.com/goto</code> before sending a
visitor to the destination page &mdash; a scheme confirmed in the industry press. On
11 November 2026, Brave Search published its own answer: every result link now points at a
<code>brave.com/go</code> URL that is encrypted per link, so the search engine can see that a
click came from a results page without learning which result was clicked.</p>

<p>Both moves are aimed squarely at automated scrapers, and both have a side effect that lands
directly on creators: <em>a link copied from a results page is no longer the destination</em>.
It is a redirect, and a redirect that may expire. If your archive stores that link, you have
archived a pointer to a place you no longer control &mdash; or to nothing at all.</p>

<p>This article is about that shift, and about what a creator should do about it. The angle
here is not "search got harder to scrape." It is narrower and more practical: a link you
found through search is now a <strong>transport artifact</strong>, and the only thing worth
keeping is the destination you resolved from it.</p>

<h2>What Actually Changed in Late 2026</h2>
<p>Google's GOTO mechanism and Brave's cloaking scheme are related but not identical, and the
difference matters for anyone automating a fetch loop. Here is the timeline as it actually
happened, with the primary sources:</p>
<table>
  <tr><th>Date</th><th>Event</th><th>Source</th></tr>
  <tr><td>26 August 2026</td><td>Google begins routing search-result clicks through <code>google.com/goto</code> before the destination</td><td>Reported in Search Engine Land and tracked on Hacker News</td></tr>
  <tr><td>11 November 2026</td><td>Brave Search publishes its cloaking design: encrypted <code>brave.com/go</code> links built on partially oblivious pseudorandom functions</td><td>Brave engineering blog</td></tr>
  <tr><td>11 November 2026</td><td>Google Search Central warns that moving to a CDN can block Googlebot, and explains how to avoid it</td><td>Google Search Central blog</td></tr>
  <tr><td>12 November 2026</td><td>Brave Search API adds agentic payments via the open x402 protocol, in USDC on Base</td><td>Brave blog</td></tr>
  <tr><td>13 November 2026</td><td>The x402 announcement reaches 263 points on Hacker News &mdash; the clearest signal that agents-as-payers is a live developer concern</td><td>Hacker News</td></tr>
  <tr><td>18 November 2026</td><td>Brave's cloaking post surfaces on Hacker News, and the scraper-relocation argument becomes widely discussed</td><td>Hacker News</td></tr>
</table>
<p>Brave's own framing of the cause is worth reading carefully, because it is not simply
"we blocked bots." Their argument runs like this: Google implemented GOTO, which made scraping
Google's results harder, and the scraping trade did not disappear &mdash; it relocated. A good
share of the scraping that used to target Google now arrives at Brave's door, since Brave
maintains an independent index rather than reselling someone else's. Brave reports
<strong>traffic spikes of several thousand requests per second</strong> as a direct
consequence.</p>
<p>That spike has a cost that lands on ordinary users. Brave states it plainly: the extra
traffic forced already-stretched bot protection to become more aggressive, and the bill falls
on real people as slower results and more CAPTCHAs. This is the pattern to watch across the
whole industry. Defending against scrapers is not free, and it is paid for by the humans who
never scripted anything.</p>

<h2>How Google's GOTO Works</h2>
<p>GOTO is a redirect layer between the results page and the destination. The user experience
is unchanged: click, land on the page. What changes is that the URL in the address bar, and
the URL in your clipboard, is <code>google.com/goto/...</code> rather than the publisher's
own URL.</p>
<p>For a scripted fetch, the consequence is mechanical and immediate. Any pipeline that
copies a result URL and stores it &mdash; a research notebook, a citation manager, a social
listening tool, a link shortener archive &mdash; is now storing a Google-hosted redirect
rather than a reference to the source. To recover the real URL you have to follow the
redirect, and once you have followed it, the redirect itself has told you nothing except
that the destination exists today.</p>

<h2>Brave's Answer: Cloaking With Per-Link Encryption</h2>
<p>Brave's design is more interesting than a plain redirect, and it is worth understanding
because it explains where the industry is heading. The scheme is built on
<strong>partially oblivious pseudorandom functions</strong>.</p>
<p>The mechanics, as Brave describes them: each result link gets its own encryption key, and
only Brave holds those keys. When your browser asks for the key for the link you clicked, it
first disguises the request with a random number that only the browser knows. To Brave, every
such request looks identical. Brave can decrypt the request and recover the destination,
without learning which particular result on the page was chosen.</p>
<p>The privacy property is genuine and worth stating accurately: Brave learns <em>which
results page</em> a click came from and <em>when</em> it happened, but not <em>which
individual link</em> was followed. That is the "partially" in partially oblivious.</p>
<p>The anti-scraping property is arithmetic, not cryptography. Brave's argument is that
scrapers must now request a key for every link they want, and each such request is countable
per page. A human opens a link or two from a results page. A scraper wants all of them, on
every page. One answer opens one link, and that is where the scraper's economics change:
bulk result harvesting becomes measurably more expensive without obstructing real searchers.</p>

<h2>The Side Effects Nobody Wants</h2>
<p>Brave is unusually candid about the costs of its own scheme, and the costs are not subtle.
Their post lists them, and creators should know all three before they build a pipeline on top
of search results:</p>
<table>
  <tr><th>Side effect</th><th>What Brave says</th><th>Why it matters to an archive</th></tr>
  <tr><td>Redirect expiry</td><td>Redirect URLs might expire, so they should not be trusted as bookmarks or for long-term storage</td><td>A stored search link is not a durable citation. It can rot without notice.</td></tr>
  <tr><td>Phishing surface</td><td>A redirect can become a vector for phishing, since an attacker could use the reputation of a <code>brave.com/go</code> link to deliver something harmful</td><td>Blindly following a redirect from an unvetted index means following a URL that a third party vouched for, not one you chose.</td></tr>
  <tr><td>JavaScript dependency</td><td>The oblivious scheme cannot run for users with JavaScript disabled; in that case Brave falls back to a conventional redirect where the server can see the URL clicked</td><td>The privacy guarantee is conditional. A headless scraper that disables JavaScript gets a weaker version of the scheme.</td></tr>
</table>
<p>Brave's mitigations are worth noting: the ability to repudiate a redirect, a time-to-live
count, and an interstitial page that alerts the user. The time-to-live is the practical
detail for anyone storing links &mdash; it means a redirect URL has a defined shelf life, and
your storage should assume it.</p>

<h2>The Agent-Friendly Path: Pay Per Request</h2>
<p>There is a second, less discussed thread in the same story, and it matters more for
technical audiences than the cloaking scheme does. On 12 November 2026, Brave added support
for agentic payments to the Brave Search API through the open <strong>x402</strong> protocol.
The framing matters: instead of defending against agents that scrape search results, Brave
built a way for agents to <em>pay</em> for them.</p>
<p>How it works, verified against Brave's own agent documentation:</p>
<ul>
  <li>The endpoint is <code>https://search.agent.s.brave.app</code>. There is no API key, no account, and no signup &mdash; the signed payment is the credential.</li>
  <li>Send the request with no payment header and you get <strong>HTTP 402 Payment Required</strong> with an empty body. Everything you need is in the response headers.</li>
  <li>Sign what the challenge asks, then retry the identical request with the payment header attached. The successful response carries a receipt header.</li>
  <li>Payment settles in USDC on Base, chain <code>eip155:8453</code>, at 5000 base units per request &mdash; $0.005, or $5 per 1,000 requests.</li>
  <li>Verification happens first, then the search runs, then settlement occurs. A failed search is never charged, so retrying a failed search costs nothing extra.</li>
</ul>
<p>Two details are easy to get wrong and worth copying exactly. First, <strong>x402 V2 only</strong>
&mdash; a V1 <code>X-Payment</code> header is not recognised as a payment and gets a cold 402.
Second, <strong>send exactly one rail</strong>: a payment header alongside an
<code>Authorization</code> header, whatever its scheme, is a 400. And the challenges are
short-lived &mdash; an x402 offer is payable for 300 seconds, so you fetch a fresh 402 rather
than replaying an old challenge.</p>
<p>The price list is uniform. Web search, LLM context, news, images, video, and the local
endpoints all sit at $0.005 per request. The same price applies to the ordinary
prepaid-credit API, where Brave's published plan is $5 per 1,000 requests, up to 50 queries
per second, with up to $20 in free calls every month and no subscription. For comparison,
Brave's own published evaluation puts its all-in cost at $18 per 1,000 questions on FreshQA,
against $49 to $89 for competitors.</p>
<p>Not every path is for sale, and the omissions are informative. The Answers API is not sold,
because it bills per query and per token, which a single fixed price cannot express.
Autosuggest and Spellcheck are not sold either: they cost less than the fee a facilitator
takes to settle one payment. And the Summarizer is not sold because Brave has deprecated it.
A path outside the price table returns a <strong>404</strong>, never a payable 402 &mdash;
which is a useful distinction when you are debugging a client.</p>

<h2>What This Means for Social Content Creators</h2>
<p>Now the part that actually concerns this audience. Three things follow from the above, and
only one of them is about scraping.</p>
<p><strong>One: a search-discovered link is not a citation.</strong> If you found a post on X,
a Bluesky thread, or a LinkedIn article through a search result, the URL you copied may be a
redirect that expires. Resolve it, then store the destination. The redirect is evidence of
how you found the thing; the destination is the thing.</p>
<p><strong>Two: your own content is now harder to be discovered by agents than by people.</strong>
Search engines are adding machine-facing layers &mdash; redirect hops, encrypted links,
per-request payment &mdash; that make automated discovery of your posts more expensive and
less reliable. That cuts both ways. It reduces the scraper traffic that treats your posts as
free training material, and it also means an agent that would have found your post may not.
The layer you control is the archive, not the discovery path.</p>
<p><strong>Three: the pay-per-request API is a legitimate option, and it is priced like one.</strong>
If you are building an agent that monitors search results for mentions of your brand or your
handle &mdash; a legitimate and increasingly common use &mdash; you now have a path that does
not involve scraping a results page and hoping nobody notices. The cost is $0.005 per
request, and the alternative is to build against a redirect scheme whose rules change without
notice.</p>

<h2>An Archive-Safe Capture Workflow</h2>
<p>Three steps, and they compose into one script. Step one is to resolve the redirect and
capture the destination, never the redirect. Step two is to write the resolved URL into a
provenance sidecar next to the capture, because a file with no source URL is not an archive,
it is a rumour. Step three is to keep your own copy, with the capture time attached.</p>
<p>The commands below are identical across all three language versions of this article, so
you can copy them directly:</p>
<pre><code>__CODE1__</code></pre>
<p>Note what the first command actually returns: <code>%{url_effective}</code> is the
destination after every hop, and <code>%{num_redirects}</code> tells you how many hops it
took. A hop count of zero means the result URL was already the source. A hop count of two or
three means the link you were given was a redirect chain &mdash; which is exactly the case
where storing the original URL would have been a mistake.</p>
<p>Step two is where the pay-per-request path fits, if you are using one. And step three is
where a creator's own archive comes in, which is the only part of this pipeline you fully
control:</p>
<pre><code>__CODE2__</code></pre>
<p>The separation between those two steps is the point of the whole exercise. Search is a
<strong>discovery layer</strong> &mdash; it is how you find things, it is now increasingly
metered per machine request, and its URLs are explicitly documented as unsuitable for
long-term storage. Your archive is a <strong>possession layer</strong> &mdash; it is what you
actually keep, and it does not expire because a search engine changed its redirect format on a
Tuesday.</p>

<h2>Where This Stops</h2>
<p>It is worth being precise about the edges, because the marketing around this tends to
overreach in both directions.</p>
<p>Brave's cloaking is not a blanket block on bots. It is a redirect layer with a per-link key.
A human browser clicking a link resolves it in one request, exactly as before. A scraper that
wants every link on a page has to request every key, and each request is visible. What this
changes is cost, not permission &mdash; and it is a cost that legitimate high-volume consumers
also pay.</p>
<p>Likewise, the x402 endpoint is not a free search API. It is a metered one, at $0.005 per
request, with a wallet, a chain, a settlement step, and a receipt to reconcile. Brave's
ordinary prepaid-credit API still exists, still includes up to $20 in monthly free calls, and
still works without a blockchain at all. The x402 path is for agents that want to pay per
request without an account, not a cheaper alternative to the existing plans.</p>
<p>And the wider trend is not one-directional. Google has been busy on the opposite side of the
same problem: in November 2026 it published guidance on moving to a CDN without
overwhelming the origin or blocking Googlebot, and in October it added support for a shared
AI training control for websites. Both moves make it easier for a publisher to signal what
should and should not be crawled. Redirect cloaking makes it harder to scrape results
silently. These are different tools pointed at the same underlying shift &mdash; the web is
acquiring machine-facing access controls, and content owners will be asked to opt in to some
of them.</p>

<h2>FAQ</h2>
__FAQ_BLOCK__

<h2>Bottom Line</h2>
<p>The headline of this story is that two search engines changed their result links. The
practical story is that a URL copied from a search results page is no longer a durable
reference to anything, and that machine access to search is becoming a metered transaction
rather than a free scrape.</p>
<p>For a creator, the response to both is the same and it is not complicated. Resolve the
redirect before you store the link. Treat the resolved destination as the citation and the
redirect as a breadcrumb. If you need search at scale for legitimate monitoring, pay for it
rather than scraping it &mdash; at five tenths of a cent a request, it is cheaper than
maintaining a scraper that breaks every time a redirect format changes. And keep your own copy
of your own posts, because no amount of search-layer engineering makes someone else's index
the owner of your work.</p>
""",
    'faq': [
        ("What is Google's GOTO redirect?",
         "GOTO is a redirect layer Google introduced in late August 2026 that routes clicks on search results through google.com/goto before sending the visitor to the destination page. The user experience is unchanged, but the URL copied from the results page is now the redirect rather than the publisher's own address."),
        ("Did Brave block all bots on Brave Search?",
         "No. Brave's scheme is a cloaking layer rather than a blanket block. Result links point at encrypted brave.com/go URLs built on partially oblivious pseudorandom functions, so a human clicking one link resolves it in a single request exactly as before. What changes is the economics for bulk harvesting, because a scraper must request a key for every link it wants and each request is countable per page."),
        ("Do search result redirect links expire?",
         "Yes, and Brave says so explicitly in its own engineering post: redirect URLs might expire, so they should not be trusted as bookmarks or for long-term storage. Brave's implementation includes a time-to-live count on the redirect for that reason. Always resolve the redirect and store the destination URL instead."),
        ("How much does the Brave Search x402 API cost per request?",
         "5000 base units of USDC on Base, which is $0.005 per request, or $5 per 1,000 requests. Web search, LLM context, news, images, video, and the local endpoints are all priced at the same rate. Gas fees are covered for a limited time. The ordinary prepaid-credit API is also $5 per 1,000 requests and includes up to $20 in free calls every month."),
        ("Do I need a wallet to use the Brave Search agent API?",
         "Yes, if you use the x402 endpoint, because a signed payment is the credential and there is no API key or account. Brave runs its own facilitator accepting USDC on Base, and clients such as purl from Stripe handle the signing. If you do not want to manage a wallet, the standard Brave Search API with a prepaid credit card still works and still includes free monthly calls."),
        ("Should I archive the search redirect URL or the final page URL?",
         "Archive the final page URL, and keep the redirect as a breadcrumb in a provenance sidecar if you want to record how the item was discovered. A redirect URL is a transport artifact with a limited shelf life, and it is not the source. Use the resolved URL as the citation and record the capture time alongside it."),
    ],
    'related': [
        ('/en/blog/search-traffic-decline-social-archive-2026.html',
         'Search Decline 2026: Archiving Is Creator Insurance'),
        ('/en/blog/crawlie-seo-crawler-tools-2026.html',
         'Crawlie &amp; SEO Crawler Tools 2026: 5 Compared'),
        ('/en/blog/spur-coalition-content-telemetry-2026.html',
         'SPUR Coalition 2026: Content Telemetry for Publishers'),
        ('/en/blog/social-content-ownership-local-archiving-2026.html',
         'Social Content Ownership &amp; Archiving 2026'),
        ('/en/blog/x-to-markdown-3-methods-2026.html',
         'X to Markdown 2026: 3 Ways to Save X Threads'),
    ],
    'cta_title': 'Archive the destination, not the redirect',
    'cta_body': ('ThreadGrab saves public X threads, Bluesky posts and LinkedIn articles as clean '
                 'Markdown and JSON, with the capture time attached. Your own copy, on your own '
                 'disk, unaffected by what a search engine does to its result links.'),
    'cta_btn': 'Try ThreadGrab &rarr;',
    'sources': r"""
<p><strong>Primary sources</strong></p>
<ul>
<li><a href="https://brave.com/blog/google-goto-anti-scraping/">Brave Search &mdash; How Google's anti-scraping move became our problem (and how we solved it in a user-first way), 11 Nov 2026</a></li>
<li><a href="https://brave.com/blog/search-api-agentic-payments/">Brave Search &mdash; The Brave Search API now accepts agentic payments via the x402 protocol, 12 Nov 2026</a></li>
<li><a href="https://search.agent.s.brave.app/llms.txt">Brave Search agent endpoint &mdash; llms.txt: the pay-per-request proxy, price table, rails and error table</a></li>
<li><a href="https://search.agent.s.brave.app/openapi.json">Brave Search agent endpoint &mdash; OpenAPI 3.1 document with x-payment-info per path</a></li>
<li><a href="https://api-dashboard.search.brave.com/documentation/guides/agent-payments">Brave Search API &mdash; Agent payments guide (x402 proxy documentation)</a></li>
<li><a href="https://brave.com/search/api/">Brave Search API &mdash; plans and pricing (Search Plan $5/1,000 requests, up to $20 monthly free calls)</a></li>
<li><a href="https://developers.google.com/search/blog/2026/11/crawling-cdn">Google Search Central &mdash; Moving to a CDN without overwhelming your origin (or blocking Googlebot), 11 Nov 2026</a></li>
<li><a href="https://developers.google.com/search/blog/2026/10/ai-training-control">Google Search Central &mdash; Supporting a shared AI training control for websites, 30 Oct 2026</a></li>
<li><a href="https://github.com/stripe/purl">Stripe &mdash; purl, the CLI wallet used to sign x402 payments</a></li>
<li><a href="https://searchengineland.com/google-confirms-deploying-goto-url-redirects-to-search-results-links-485926">Search Engine Land &mdash; Google confirms deploying goto URL redirects to search results links, 26 Aug 2026 (blocks scripted clients; opens normally in a browser)</a></li>
</ul>
""",
}
