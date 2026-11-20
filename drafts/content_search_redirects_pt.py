# -*- coding: utf-8 -*-
"""PT content for search-result-redirects-cloaking-goto-2026."""

CONTENT = {
    'title': 'Redirecionamentos em Resultados de Busca 2026: GOTO e Cloaking',
    'desc': ("O GOTO do Google e o cloaking do Brave quebraram a raspagem de resultados. O que muda para quem arquiva e por que a busca paga por requisicao."),
    'keywords': ("redirecionamento em resultados de busca, Google GOTO, cloaking do Brave, "
                 "raspagem de SERP, expiracao de URLs de redirecionamento, API de busca x402, "
                 "micropagamentos USDC, busca para agentes de IA, proveniencia de arquivo, "
                 "ThreadGrab"),
    'body': r"""
<p>Dois mecanismos de busca mudaram a forma como funcionam os links de resultado na mesma
semana, e para quem arquiva ou monitora conteudo social isso nao e uma curiosidade. Em
26 de agosto de 2026, o Google comecou a passar os cliques em resultados de busca por
<code>google.com/goto</code> antes de levar o visitante ate a pagina de destino &mdash; um
mecanismo confirmado pela imprensa do setor. Em 11 de novembro de 2026, o Brave Search
publicou sua propria resposta: todo link de resultado agora aponta para uma URL
<code>brave.com/go</code> que e criptografada por link, de modo que o mecanismo de busca
possa ver que um clique veio de uma pagina de resultados sem saber qual resultado foi
clicado.</p>

<p>Os dois movimentos miram diretamente os raspadores automaticos, e os dois tem um efeito
colateral que alcanca quem cria conteudo: <em>um link copiado de uma pagina de resultados
deixou de ser o destino</em>. Ele e um redirecionamento, e um redirecionamento que pode
expirar. Se o seu arquivo guarda esse link, voce guardou um ponteiro para um lugar que voce
nao controla &mdash; ou para nada.</p>

<p>Este artigo trata dessa mudanca e do que um criador deve fazer a respeito. O angulo aqui
nao e "a busca ficou mais dificil de raspar". E mais especifico e mais pratico: um link
encontrado pela busca e um <strong>artefato de transporte</strong>, e a unica coisa que vale
guardar e o destino que voce resolveu a partir dele.</p>

<h2>O que realmente mudou no fim de 2026</h2>
<p>O mecanismo GOTO do Google e o esquema de cloaking do Brave sao relacionados, mas nao
identicos, e a diferenca importa para quem automatiza um laco de busca. Esta e a linha do
tempo real, com as fontes primarias:</p>
<table>
  <tr><th>Data</th><th>Evento</th><th>Fonte</th></tr>
  <tr><td>26 de agosto de 2026</td><td>Google comeca a passar os cliques em resultados de busca por <code>google.com/goto</code> antes do destino</td><td>Reportado no Search Engine Land e acompanhado no Hacker News</td></tr>
  <tr><td>11 de novembro de 2026</td><td>Brave Search publica seu projeto de cloaking: links <code>brave.com/go</code> criptografados, construidos sobre funcoes pseudorandomicas parcialmente oblivious</td><td>Blog de engenharia do Brave</td></tr>
  <tr><td>11 de novembro de 2026</td><td>O Google Search Central alerta que migrar para uma CDN pode bloquear o Googlebot, e explica como evitar isso</td><td>Blog Google Search Central</td></tr>
  <tr><td>12 de novembro de 2026</td><td>A API do Brave Search aceita pagamentos agenticos via o protocolo aberto x402, em USDC na rede Base</td><td>Blog do Brave</td></tr>
  <tr><td>13 de novembro de 2026</td><td>O anuncio do x402 chega a 263 pontos no Hacker News &mdash; o sinal mais claro de que agentes pagadores virou uma preocupacao real de desenvolvedores</td><td>Hacker News</td></tr>
  <tr><td>18 de novembro de 2026</td><td>O texto sobre cloaking do Brave aparece no Hacker News, e o argumento da realocacao dos raspadores vira discussao ampla</td><td>Hacker News</td></tr>
</table>
<p>A propria formulacao do Brave sobre a causa merece leitura atenta, porque nao e simplesmente
"bloqueamos bots". O argumento deles e este: o Google implementou o GOTO, o que tornou mais
dificil raspar os resultados do Google, e o comercio de raspagem nao desapareceu &mdash; ele
mudou de lugar. Boa parte da raspagem que apontava para o Google passou a bater na porta do
Brave, que mantem um indice proprio em vez de revender o de outra pessoa. O Brave relata
<strong>picos de trafego de vários milhares de requisicoes por segundo</strong> como
consequencia direta.</p>
<p>Esse pico tem um custo que recai sobre usuarios comuns. O Brave diz isso sem rodeios: o
trafego extra obrigou a protecao contra bots, ja tensionada, a ficar mais agressiva, e a
conta cai sobre pessoas reais na forma de resultados mais lentos e mais CAPTCHAs. Esse e o
padrao a observar em toda a industria. Defender-se de raspadores nao e de graca, e o preco e
pago por quem nunca programou nada.</p>

<h2>Como funciona o GOTO do Google</h2>
<p>O GOTO e uma camada de redirecionamento entre a pagina de resultados e o destino. A
experiencia do usuario nao muda: clica, chega na pagina. O que muda e que a URL na barra de
endereco, e a URL copiada para a area de transferencia, passa a ser
<code>google.com/goto/...</code> em vez do endereco do proprio site.</p>
<p>Para uma requisicao automatizada, a consequencia e mecanica e imediata. Qualquer pipeline
que copia uma URL de resultado e a guarda &mdash; um caderno de pesquisa, um gerenciador de
citacoes, uma ferramenta de escuta social, um arquivo de encurtadores &mdash; passa a guardar
um redirecionamento hospedado pelo Google em vez de uma referencia a fonte. Para recuperar
a URL real e preciso seguir o redirecionamento, e depois de segui-lo o proprio
redirecionamento nao lhe diz nada alem do fato de que o destino existe hoje.</p>

<h2>A resposta do Brave: cloaking com criptografia por link</h2>
<p>O projeto do Brave e mais interessante do que um redirecionamento comum, e vale
entender porque ele explica para onde a industria esta indo. O esquema se baseia em
<strong>funcoes pseudorandomicas parcialmente oblivious</strong>.</p>
<p>A mecanica, como o Brave descreve: cada link de resultado recebe sua propria chave de
criptografia, e apenas o Brave guarda essas chaves. Quando o seu navegador pede a chave do
link que voce clicou, ele mascara a requisicao com um numero aleatorio que somente o
navegador conhece. Para o Brave, toda requisicao assim parece identica. O Brave consegue
decifrar a requisicao e recuperar o destino, sem descobrir qual resultado especifico da
pagina foi escolhido.</p>
<p>A propriedade de privacidade e genuina e vale ser declarada com precisao: o Brave aprende
<em>de qual pagina de resultados</em> o clique veio e <em>quando</em> aconteceu, mas nao
<em>qual link individual</em> foi seguido. E o "parcialmente" do "parcialmente oblivious".</p>
<p>A propriedade anti-raspagem e aritmetica, nao criptografica. O argumento do Brave e que os
raspadores agora precisam pedir uma chave para cada link que querem, e cada uma dessas
requisicoes pode ser contada por pagina. Uma pessoa abre um link ou dois de uma pagina de
resultados. Um raspador quer todos eles, em todas as paginas. Uma resposta abre um link, e
e ai que a aritmetica do raspador muda: coletar resultados em escala passa a custar mais de
forma mensuravel, sem atrapalhar quem busca de verdade.</p>

<h2>Os efeitos colaterais que ninguem quer</h2>
<p>O Brave e notavelmente honesto sobre os custos do proprio esquema, e os custos nao sao
sutis. O texto lista tres, e criadores precisam conhecer os tres antes de montar um pipeline
sobre resultados de busca:</p>
<table>
  <tr><th>Efeito colateral</th><th>O que o Brave diz</th><th>Por que importa a um arquivo</th></tr>
  <tr><td>Expiracao dos redirecionamentos</td><td>URLs de redirecionamento podem expirar, e portanto nao devem ser tratadas como marcadores nem para armazenamento de longo prazo</td><td>Um link guardado da busca nao e uma citacao duravel. Ele pode apodrecer sem aviso.</td></tr>
  <tr><td>Superficie de phishing</td><td>Um redirecionamento pode virar vetor de phishing, ja que um atacante poderia usar a reputacao de um link <code>brave.com/go</code> para entregar algo malicioso</td><td>Seguir cegamente um redirecionamento de um indice nao revisado e seguir uma URL garantida por terceiros, nao uma que voce escolheu.</td></tr>
  <tr><td>Dependencia de JavaScript</td><td>O esquema oblivious nao roda para quem desativou o JavaScript; nesse caso o Brave volta a um redirecionamento convencional, em que o servidor ve a URL clicada</td><td>A garantia de privacidade e condicional. Um scraper sem JavaScript recebe uma versao mais fraca do esquema.</td></tr>
</table>
<p>As mitigacoes do Brave merecem registro: a possibilidade de repudiar um redirecionamento, uma
contagem de tempo de vida e uma pagina intersticial que alerta o usuario. O tempo de vida e o
detalhe pratico para quem guarda links &mdash; significa que uma URL de redirecionamento tem
um prazo de validade definido, e o seu armazenamento deve levar isso em conta.</p>

<h2>O caminho amigavel para agentes: pagar por requisicao</h2>
<p>Ha um segundo fio, menos_ldscutado, na mesma historia, e ele importa mais para quem e
tecnico do que o esquema de cloaking. Em 12 de novembro de 2026, o Brave adicionou suporte a
pagamentos agenticos na API do Brave Search pelo protocolo aberto <strong>x402</strong>. O
enquadramento importa: em vez de se defender contra agentes que raspam resultados de busca,
o Brave construiu um jeito de agentes <em>pagarem</em> por eles.</p>
<p>Como funciona, verificado contra a propria documentacao de agentes do Brave:</p>
<ul>
  <li>O endpoint e <code>https://search.agent.s.brave.app</code>. Nao ha API key, nem conta, nem cadastro &mdash; o pagamento assinado e a credencial.</li>
  <li>Mande a requisicao sem cabecalho de pagamento e voce recebe <strong>HTTP 402 Payment Required</strong> com corpo vazio. Tudo o que voce precisa esta nos cabecalhos da resposta.</li>
  <li>Assine o que o desafio pede e reenvie exatamente a mesma requisicao com o cabecalho de pagamento anexado. A resposta bem-sucedida traz um cabecalho de recibo.</li>
  <li>O pagamento liquida em USDC na Base, cadeia <code>eip155:8453</code>, a 5000 unidades base por requisicao &mdash; US$ 0,005, ou US$ 5 por 1.000 requisicoes.</li>
  <li>A verificacao vem primeiro, depois a busca roda, depois a liquidacao. Uma busca que falha nunca e cobrada, entao repetir uma busca falha nao custa nada a mais.</li>
</ul>
<p>Dois detalhes sao faceis de errar e valem copiar na exatao. Primeiro, <strong>somente x402
V2</strong> &mdash; um cabecalho V1 <code>X-Payment</code> nao e reconhecido como pagamento e
recebe um 402 frio. Segundo, <strong>envie exatamente um trilho</strong>: um cabecalho de
pagamento ao lado de um <code>Authorization</code>, qualquer que seja seu esquema, e um 400. E
os desafios tem vida curta &mdash; uma oferta x402 e pagavel por 300 segundos, entao vale
buscar um 402 novo em vez de repetir um desafio antigo.</p>
<p>A lista de precos e uniforme. Busca web, contexto para LLM, noticias, imagens, video e os
endpoints locais custam todos US$ 0,005 por requisicao. O mesmo preco vale para a API
comum de credito prepaid, em que o plano publicado do Brave e US$ 5 por 1.000 requisicoes,
ate 50 consultas por segundo, com ate US$ 20 em chamadas gratuitas por mes e sem
assinatura. Para comparacao, a propria avaliacao publicada do Brave coloca seu custo total em
US$ 18 por 1.000 perguntas no FreshQA, contra US$ 49 a US$ 89 dos concorrentes.</p>
<p>Nem todo caminho esta a venda, e as omissoes sao informativas. A Answers API nao e
vendida, porque cobra por consulta e por token, o que um preco fixo unico nao consegue
expressar. Autosuggest e Spellcheck tambem nao sao vendidos: custam menos do que a taxa que um
facilitador cobra para liquidar um pagamento. E o Summarizer nao e vendido porque o Brave o
descontinuou. Um caminho fora da tabela de precos devolve <strong>404</strong>, nunca um 402
pagavel &mdash; distincao util na hora de depurar um cliente.</p>

<h2>O que isso significa para quem cria conteudo social</h2>
<p>Agora a parte que realmente interessa a este publico. Tres consequencias decorrem do que
foi descrito, e apenas uma delas e sobre raspagem.</p>
<p><strong>Um: um link descoberto pela busca nao e uma citacao.</strong> Se voce achou um post
no X, uma thread no Bluesky ou um artigo no LinkedIn atraves de um resultado de busca, a URL
que voce copiou pode ser um redirecionamento que expira. Resolva, e guarde o destino. O
redirecionamento e a prova de como voce encontrou a coisa; o destino e a coisa.</p>

<p><strong>Dois: seu proprio conteudo esta mais dificil de ser descoberto por agentes do que
por pessoas.</strong> Os mecanismos de busca estao adicionando camadas voltadas a maquinas
&mdash; saltos de redirecionamento, links criptografados, pagamento por requisicao &mdash; que
tornam a descoberta automatica de seus posts mais cara e menos confiavel. Isso corta nos dois
sentidos. Reduz o trafego de raspadores que tratam seus posts como materia-prima de
treinamento gratuita, e tambem significa que um agente que teria encontrado seu post pode nao
encontrar. A camada que voce controla e o arquivo, nao o caminho de descoberta.</p>

<p><strong>Tres: a API paga por requisicao e uma opcao legitima, e ela esta precificada como
uma.</strong> Se voce esta construindo um agente que monitora resultados de busca por mencoes
da sua marca ou do seu usuario &mdash; uso legitimo e cada vez mais comum &mdash; voce agora tem
um caminho que nao depende de raspar uma pagina de resultados esperando que ninguem perceba. O
custo e US$ 0,005 por requisicao, e a alternativa e construir contra um esquema de
redirecionamento cujas regras mudam sem aviso.</p>

<h2>Um fluxo de captura seguro para arquivos</h2>
<p>Tres passos que se compose em um unico script. O primeiro e resolver o redirecionamento e
capturar o destino, nunca o redirecionamento. O segundo e gravar a URL resolvida em um
arquivo de proveniencia ao lado da captura, porque um arquivo sem URL de origem nao e um
arquivo, e um boato. O terceiro e manter sua propria copia, com o horario da captura anexado.</p>
<p>Os comandos abaixo sao identicos nas tres versoes de idioma deste artigo, entao voce pode
copia-los direto:</p>
<pre><code>__CODE1__</code></pre>
<p>Repare no que o primeiro comando realmente devolve: <code>%{url_effective}</code> e o
destino depois de todos os saltos, e <code>%{num_redirects}</code> diz quantos saltos foram
necessarios. Uma contagem zero significa que a URL do resultado ja era a fonte. Uma contagem
de dois ou tres significa que o link que voce recebeu era uma cadeia de redirecionamentos
&mdash; exatamente o caso em que guardar a URL original teria sido um erro.</p>
<p>O segundo passo e onde entra o caminho de pagamento por requisicao, se voce usar algum. E o
terceiro e onde entra o arquivo do proprio criador, que e a unica parte deste pipeline que
voce controla por completo:</p>
<pre><code>__CODE2__</code></pre>
<p>A separacao entre esses dois passos e o ponto de todo o exercicio. A busca e uma
<strong>camada de descoberta</strong> &mdash; e como voce encontra as coisas, hoje e
increasingemente cobrada por requisicao de maquina, e suas URLs sao explicitamente indicadas
como inadequadas para armazenamento de longo prazo. O seu arquivo e uma <strong>camada de
posse</strong> &mdash; e o que voce realmente guarda, e nao expira porque um mecanismo de busca
mudou o formato do redirecionamento numa terca-feira.</p>

<h2>Onde isso para</h2>
<p>Vale ser preciso sobre as bordas, porque o marketing em volta costuma exagerar nas duas
direcoes.</p>
<p>O cloaking do Brave nao e um bloqueio geral a bots. E uma camada de redirecionamento com
uma chave por link. Um navegador humano clicando em um link resolve em uma requisicao, como
antes. Um raspador que quer todos os links de uma pagina precisa pedir todas as chaves, e
cada requisicao fica visivel. O que isso muda e o custo, nao a permissao &mdash; e um custo que
consumidores legitimos de alto volume tambem pagam.</p>
<p>Da mesma forma, o endpoint x402 nao e uma API de busca gratuita. E uma API metrada, a
US$ 0,005 por requisicao, com carteira, cadeia, etapa de liquidacao e recibo para conferir. A
API comum de credito prepaid do Brave continua existindo, continua com ate US$ 20 em
chamadas gratuitas por mes, e continua funcionando sem blockchain nenhum. O caminho x402 e
para agentes que querem pagar por requisicao sem abrir conta, nao uma alternativa mais
barata aos planos existentes.</p>
<p>E a tendencia maior nao e de uma so direcao. O Google tem estado ocupado do lado oposto do
mesmo problema: em novembro de 2026 publicou orientacao sobre migrar para uma CDN sem
sobrecarregar a origem nem bloquear o Googlebot, e em outubro adicionou suporte a um controle
compartilhado de treinamento de IA para sites. Os dois movimentos facilitam a um publicador
sinalizar o que deve e o que nao deve ser rastreado. O cloaking de redirecionamento dificulta
raspar resultados em silencio. Sao ferramentas diferentes apontando para a mesma mudanca de
fundo &mdash; a web esta adquirindo controles de acesso voltados a maquinas, e os donos de
conteudo serao convoidados a aderir a alguns deles.</p>

<h2>FAQ</h2>
__FAQ_BLOCK__

<h2>Conclusao</h2>
<p>A manchete desta historia e que dois mecanismos de busca mudaram seus links de resultado. A
historia pratica e que uma URL copiada de uma pagina de resultados de busca ja nao e uma
referencia duravel a nada, e que o acesso de maquinas a busca esta virando uma transacao
cobrada em vez de uma raspagem gratuita.</p>
<p>Para um criador, a resposta as duas e a mesma, e nao e complicada. Resolva o
redirecionamento antes de guardar o link. Trate o destino resolvido como a citacao e o
redirecionamento como um trilho de migalha. Se voce precisa de busca em escala para
monitoramento legitimo, pague por ela em vez de raspar &mdash; a meio centavo por requisicao,
custa menos do que manter um scraper que quebra toda vez que o formato de redirecionamento
muda. E guarde sua propria copia das suas proprias publicações, porque nenhuma engenharia de
camada de busca faz o indice de outra pessoa ser o dono do seu trabalho.</p>
""",
    'faq': [
        ("O que e o redirecionamento GOTO do Google?",
         "GOTO e uma camada de redirecionamento que o Google introduziu no fim de agosto de 2026 e que passa os cliques em resultados de busca por google.com/goto antes de levar o visitante ate a pagina de destino. A experiencia do usuario nao muda, mas a URL copiada da pagina de resultados passa a ser o redirecionamento e nao o endereco do proprio publicador."),
        ("O Brave bloqueou todos os bots na busca?",
         "Nao. O esquema do Brave e uma camada de cloaking, nao um bloqueio geral. Os links de resultado apontam para URLs brave.com/go criptografadas, construidas sobre funcoes pseudorandomicas parcialmente oblivious, de modo que um humano clicando em um link resolve em uma unica requisicao como antes. O que muda e a economia da coleta em massa, porque um raspador precisa pedir uma chave para cada link e cada requisicao pode ser contada por pagina."),
        ("Os links de redirecionamento da busca expiram?",
         "Sim, e o Brave diz isso de forma explicita no proprio texto de engenharia: URLs de redirecionamento podem expirar, e portanto nao devem ser tratadas como marcadores nem para armazenamento de longo prazo. Por isso a implementacao do Brave inclui uma contagem de tempo de vida no redirecionamento. Resolva sempre o redirecionamento e guarde a URL de destino."),
        ("Quanto custa a API de busca do Brave com x402 por requisicao?",
         "5000 unidades base de USDC na Base, o que equivale a US$ 0,005 por requisicao, ou US$ 5 por 1.000 requisicoes. Busca web, contexto para LLM, noticias, imagens, video e os endpoints locais tem todos o mesmo preco. As taxas de gas sao cobertas por um periodo limitado. A API comum de credito prepaid tambem custa US$ 5 por 1.000 requisicoes e inclui ate US$ 20 em chamadas gratuitas por mes."),
        ("Preciso de carteira para usar a API de agentes do Brave Search?",
         "Precisa, se voce usar o endpoint x402, porque o pagamento assinado e a credencial e nao ha API key nem conta. O Brave roda seu proprio facilitador aceitando USDC na Base, e clientes como o purl da Stripe fazem a assinatura. Se voce nao quiser administrar uma carteira, a API padrao do Brave Search com cartao de credito prepaid continua funcionando e continua com chamadas gratuitas mensais."),
        ("Devo arquivar a URL de redirecionamento da busca ou a URL final da pagina?",
         "Arquive a URL final da pagina e mantenha o redirecionamento como trilho de migalha em um arquivo de proveniencia, se quiser registrar como o item foi descoberto. Uma URL de redirecionamento e um artefato de transporte com validade limitada e nao e a fonte. Use a URL resolvida como citacao e registre o horario da captura ao lado dela."),
    ],
    'related': [
        ('/pt/blog/search-traffic-decline-social-archive-2026.html',
         'Queda da Busca 2026: Arquivar e o Seguro do Criador'),
        ('/pt/blog/crawlie-seo-crawler-tools-2026.html',
         'Crawlie e Ferramentas de Crawler SEO 2026: 5 Comparadas'),
        ('/pt/blog/coalizao-spur-telemetria-conteudo-2026.html',
         'Coalizao SPUR 2026: Telemetria de Conteudo para Publicadores'),
        ('/pt/blog/social-content-ownership-local-archiving-2026.html',
         'Posse de Conteudo Social &amp; Arquivamento Local 2026'),
        ('/pt/blog/x-to-markdown-3-methods-2026.html',
         'X para Markdown 2026: 3 Maneiras de Salvar Threads do X'),
    ],
    'cta_title': 'Arquive o destino, nao o redirecionamento',
    'cta_body': ('O ThreadGrab salva threads publicas do X, posts do Bluesky e artigos do LinkedIn '
                 'como Markdown e JSON limpos, com o horario da captura anexado. A sua propria '
                 'copia, no seu proprio disco, sem depender do que a busca faz com seus links.'),
    'cta_btn': 'Testar o ThreadGrab &rarr;',
    'sources': r"""
<p><strong>Fontes primarias</strong></p>
<ul>
<li><a href="https://brave.com/blog/google-goto-anti-scraping/">Brave Search &mdash; How Google's anti-scraping move became our problem (and how we solved it in a user-first way), 11 nov 2026</a></li>
<li><a href="https://brave.com/blog/search-api-agentic-payments/">Brave Search &mdash; The Brave Search API now accepts agentic payments via the x402 protocol, 12 nov 2026</a></li>
<li><a href="https://search.agent.s.brave.app/llms.txt">Endpoint de agentes do Brave Search &mdash; llms.txt: o proxy pago por requisicao, tabela de precos, trilhos e tabela de erros</a></li>
<li><a href="https://search.agent.s.brave.app/openapi.json">Endpoint de agentes do Brave Search &mdash; documento OpenAPI 3.1 com x-payment-info por caminho</a></li>
<li><a href="https://api-dashboard.search.brave.com/documentation/guides/agent-payments">Brave Search API &mdash; guia de pagamentos agenticos (documentacao do proxy x402)</a></li>
<li><a href="https://brave.com/search/api/">Brave Search API &mdash; planos e precos (Search Plan US$ 5/1.000 requisicoes, ate US$ 20 de chamadas gratuitas mensais)</a></li>
<li><a href="https://developers.google.com/search/blog/2026/11/crawling-cdn">Google Search Central &mdash; Moving to a CDN without overwhelming your origin (or blocking Googlebot), 11 nov 2026</a></li>
<li><a href="https://developers.google.com/search/blog/2026/10/ai-training-control">Google Search Central &mdash; Supporting a shared AI training control for websites, 30 out 2026</a></li>
<li><a href="https://github.com/stripe/purl">Stripe &mdash; purl, a carteira de linha de comando usada para assinar pagamentos x402</a></li>
<li><a href="https://searchengineland.com/google-confirms-deploying-goto-url-redirects-to-search-results-links-485926">Search Engine Land &mdash; Google confirms deploying goto URL redirects to search results links, 26 ago 2026 (bloqueia clientes scriptados; abre normalmente no navegador)</a></li>
</ul>
""",
}
