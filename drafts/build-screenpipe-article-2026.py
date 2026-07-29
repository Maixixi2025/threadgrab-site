import html
import json
import os
import re

WORKDIR = "/root/threadgrab-site"
OUTDIR = os.path.join(WORKDIR, "drafts", "articles")
DATE_ISO = "2026-07-27"

SLUGS = {
    "en": "screenpipe-social-content-capture-2026",
    "pt": "screenpipe-captura-conteudo-social-2026",
    "id": "screenpipe-capture-konten-sosial-2026",
}

TITLES = {
    "en": "Screenpipe for Social Creators 2026: Capture Workflows",
    "pt": "Screenpipe para Criadores Sociais 2026: Guia de Captura",
    "id": "Screenpipe untuk Kreator Sosial 2026: Panduan Capture",
}

DESCS = {
    "en": "Learn how Screenpipe captures local screen and audio context for X, Bluesky, and LinkedIn workflows and archive the public post as Markdown.",
    "pt": "Aprenda como o Screenpipe captura contexto local de tela e áudio para fluxos de X, Bluesky e LinkedIn e arquive o post público em Markdown.",
    "id": "Pelajari cara Screenpipe menangkap konteks layar dan audio lokal untuk alur X, Bluesky, dan LinkedIn, lalu arsipkan post publik sebagai Markdown.",
}

KEYWORDS = {
    "en": "Screenpipe social creators, screen recording AI memory, X workflow, Bluesky workflow, LinkedIn content, ThreadGrab Markdown archive",
    "pt": "Screenpipe criadores sociais, memória de IA local, fluxo X, fluxo Bluesky, conteúdo LinkedIn, arquivo Markdown ThreadGrab",
    "id": "Screenpipe kreator sosial, memori AI lokal, alur X, alur Bluesky, konten LinkedIn, arsip Markdown ThreadGrab",
}

DATES = {
    "en": "July 27, 2026",
    "pt": "27 de Julho de 2026",
    "id": "27 Juli 2026",
}

LOCALES = {"en": "en_US", "pt": "pt_BR", "id": "id_ID"}

UI = {
    "en": {"home": "Home", "read": "11 min read", "type": "Guide", "about": "About", "privacy": "Privacy", "notaff": "Not affiliated with X Corp., Bluesky Social PBC, LinkedIn Corporation, or Microsoft Corporation."},
    "pt": {"home": "Início", "read": "11 min de leitura", "type": "Guia", "about": "Sobre", "privacy": "Privacidade", "notaff": "Não afiliado a X Corp., Bluesky Social PBC, LinkedIn Corporation ou Microsoft Corporation."},
    "id": {"home": "Beranda", "read": "11 menit baca", "type": "Panduan", "about": "Tentang", "privacy": "Privasi", "notaff": "Tidak berafiliasi dengan X Corp., Bluesky Social PBC, LinkedIn Corporation, atau Microsoft Corporation."},
}

# These blocks are intentionally byte-identical in all three language versions.
CODE_BLOCKS = [
    "npx screenpipe record\nnpx screenpipe setup",
    "claude mcp add screenpipe -- npx -y screenpipe-mcp@latest",
]

BODIES = {
    "en": [
        ("Why Screenpipe matters for social creators", [
            "<p>Social publishing rarely starts in the social editor. A creator researches in a browser, compares posts, listens to a meeting, drafts in a text editor, checks a source, and only then publishes to X, Bluesky, or a LinkedIn Newsletter. The finished post is public, but the reasoning that produced it is usually scattered across tabs, notes, and memory.</p>",
            "<p><a href=\"https://screenpi.pe/\">Screenpipe</a> takes a different approach: it runs on your computer and turns screen and audio activity into a local, searchable memory. Its README describes screen capture, accessibility data, OCR fallback, transcription, speakers, app switches, and agent workflows. That makes it interesting for creators who want to recover research context or trigger an automation without sending every private working note to a hosted AI service.</p>",
            "<p>This is not a replacement for a publishing API, and it is not a license to scrape private material. Think of it as a local capture layer around the editorial workflow. Use it to remember what you saw while researching, produce a repeatable handoff for an agent, and keep the final public artifact portable with ThreadGrab.</p>",
        ]),
        ("What Screenpipe captures — and what it does not", [
            "<p>Screenpipe is designed to capture what happens on a computer: visual context, audio, accessibility-tree text when available, and OCR when structured accessibility data is missing. The project says that data stays on the local machine, while its documentation also lists optional encryption at rest and filters for apps, windows, browser extensions, passwords, and proprietary AI PII models.</p>",
            "<p>That distinction matters for social content. A local recording can help you remember a source page, a product demo, or the exact wording of a draft review. It does not automatically grant permission to republish a paywalled article, a private direct message, a customer call, or a coworker’s screen. Your archive policy still decides what may be retained and what must be deleted.</p>",
            "<div class=\"callout\"><p><strong>Rule of thumb:</strong> capture your own workflow by default. Add an explicit consent step before recording meetings, customer material, or another person’s voice and screen.</p></div>",
        ]),
        ("Screenpipe vs official APIs vs browser capture", [
            "<p>Creators often ask whether a local screen-and-audio tool can replace the X API, Bluesky API, or LinkedIn export. The practical answer is no: the tools solve different problems.</p>",
            "<table><thead><tr><th>Approach</th><th>Best for</th><th>Main trade-off</th></tr></thead><tbody><tr><td>Official API or export</td><td>Structured public data, stable identifiers, repeatable queries</td><td>Access limits, authentication, changing product rules</td></tr><tr><td>Screenpipe</td><td>Local workflow context, research memory, agent triggers</td><td>Storage, privacy controls, visual data is less structured</td></tr><tr><td>Browser capture</td><td>One-off public pages and visual evidence</td><td>Fragile selectors, manual cleanup, unclear retention</td></tr><tr><td>ThreadGrab</td><td>Readable Markdown copies of public social posts</td><td>Only captures content that is publicly reachable</td></tr></tbody></table>",
            "<p>A strong workflow combines them. Use an official API when you need structured records at scale. Use Screenpipe when the important context is the path you took through the research. Use ThreadGrab after publishing to create a clean, human-readable archive of the public post itself.</p>",
        ]),
        ("Install and test a local capture workflow", [
            "<p>The Screenpipe project provides a desktop download and a command-line path. The commands below come from the project README. Start with a short, deliberate test rather than leaving continuous capture on without checking storage and privacy settings.</p>",
            "<pre><code>npx screenpipe record\nnpx screenpipe setup</code></pre>",
            "<p>After setup, ask a narrow question about a recent window of activity. For example, verify that the local index can distinguish a browser research session from a writing session. Confirm where data is stored, which apps are excluded, and how you will delete old recordings before you connect the workflow to an agent.</p>",
            "<p>The README lists typical usage at roughly 5–10% CPU, 0.5–3 GB RAM, and around 20 GB of storage per month, but treat those figures as project-reported guidance rather than a promise for your machine. Video resolution, audio settings, OCR, retention, and workload all change the footprint.</p>",
        ]),
        ("Connect an agent without losing editorial control", [
            "<p>Screenpipe’s README also shows an MCP path for connecting the local memory to an assistant. The point is not to let an agent publish automatically. The point is to let it answer bounded questions such as “what source did I inspect before drafting this thread?” or “summarize the research session from this afternoon.”</p>",
            "<pre><code>claude mcp add screenpipe -- npx -y screenpipe-mcp@latest</code></pre>",
            "<p>Keep the agent’s permissions narrow. A safe first version is read-only search over a selected folder or time range, with the final draft written to a local Markdown file for human review. Only after you can inspect the inputs and outputs should you consider an automation that creates a draft in another tool.</p>",
            "<p>For social creators, the valuable handoff is usually a provenance note: source URL, capture time, claim being used, and the transformation made in the final post. That note is more useful than a vague instruction to “write a viral thread.”</p>",
        ]),
        ("Turn research into one canonical social draft", [
            "<p>Use Screenpipe for context, not as the canonical content database. Once the research session is complete, create a small Markdown source file with the thesis, links, quoted facts, personal observations, and open questions. This gives X Articles, Bluesky long-form posts, and LinkedIn Newsletters one stable argument to adapt.</p>",
            "<ol><li><strong>Capture:</strong> record only the research window or meeting you are allowed to retain.</li><li><strong>Extract:</strong> ask the local agent to list sources, timestamps, and unresolved claims.</li><li><strong>Write:</strong> produce one human-reviewed Markdown draft with links.</li><li><strong>Adapt:</strong> change the opening, length, and call to action per platform without changing the factual core.</li><li><strong>Archive:</strong> save the Markdown source and capture the public URLs after publishing.</li></ol>",
            "<p>This separation prevents a common failure mode: the screen recording becomes the only copy of an idea. A recording is useful evidence, but a reviewed Markdown file is easier to search, diff, quote, migrate, and hand to another editor.</p>",
        ]),
        ("Archive the public result with ThreadGrab", [
            "<p>After the post is live, capture the public version separately. <a href=\"https://threadgrab.com/en/\">ThreadGrab</a> is built for turning public X, Bluesky, and LinkedIn content into readable Markdown. That gives you a portable result even if the platform later changes the editor, hides an old post behind a new navigation path, or makes a long thread hard to read.</p>",
            "<p>Keep three related records: the canonical Markdown draft, the public platform URL, and the ThreadGrab capture timestamp. If a post was derived from a Screenpipe session, store the local session identifier or a short provenance note — not the entire private recording in a public archive.</p>",
            "<p>The archive should preserve attribution and context. Do not strip a correction, a disclosure, a quoted source, or a platform label merely to make the Markdown look cleaner. A useful archive is not just a backup; it is a record of what was actually published.</p>",
        ]),
        ("Privacy, consent, and retention checklist", [
            "<p>Screenpipe’s local-first design reduces one class of exposure, but local does not mean risk-free. A laptop can be lost, a backup can be copied, and an agent can surface sensitive text in the wrong context. Before a creator turns on continuous capture, write down the boundaries.</p>",
            "<ul><li>Exclude password managers, banking, private messages, HR tools, and customer systems.</li><li>Get consent before recording another person’s voice, meeting, or screen.</li><li>Set a retention period and test deletion rather than assuming it works.</li><li>Keep public archives separate from private research recordings.</li><li>Review the project’s current license and commercial terms before using it for a team or client workflow.</li><li>Label AI-assisted material honestly when disclosure affects audience trust or platform compliance.</li></ul>",
            "<p>If you cannot explain who can access a capture, how long it remains, and how to delete it, the workflow is not ready for automation. Start with a short, private experiment and expand only when the policy is clear.</p>",
        ]),
        ("Limits and practical trade-offs", [
            "<p>Screenpipe is compelling when context is the bottleneck, but it adds a new system to maintain. Storage grows over time. OCR and transcription can misread names or URLs. Visual context is harder to query than a structured API response. Continuous capture can also create a large amount of material that nobody reviews.</p>",
            "<p>There is a licensing question too. The repository describes the project as source-available and notes that personal, non-commercial use is permitted while commercial use requires a license; verify the current LICENSE file and commercial terms before deploying it for a client or team. The same careful reading applies to every platform whose content you capture.</p>",
            "<p>The best use case is focused: capture a bounded research workflow, extract the context you need, write a canonical draft, then archive the public result. That is more defensible than recording everything and hoping an agent will find value later.</p>",
        ]),
        ("Frequently asked questions", [
            "<div class=\"faq-item\"><strong>Can Screenpipe replace the X, Bluesky, or LinkedIn API?</strong><p>No. Screenpipe captures local workflow context, while official APIs provide structured platform data. Use each for the job it is designed to do.</p></div>",
            "<div class=\"faq-item\"><strong>Is Screenpipe private because it runs locally?</strong><p>Local-first reduces cloud transmission, but it does not remove device, backup, access, or consent risks. Configure exclusions, retention, and permissions before continuous capture.</p></div>",
            "<div class=\"faq-item\"><strong>Can I use Screenpipe to archive another person’s private posts?</strong><p>Do not assume that technical access is permission. Capture only material you are allowed to retain and republish, and follow platform rules and applicable privacy law.</p></div>",
            "<div class=\"faq-item\"><strong>Why use ThreadGrab after Screenpipe?</strong><p>Screenpipe preserves local process context. ThreadGrab creates a readable Markdown copy of the public social result. Together they separate private research from portable publication archives.</p></div>",
            "<div class=\"faq-item\"><strong>How should a creator start?</strong><p>Run a short local test, exclude sensitive apps, create one Markdown draft, and archive one public post. Add an agent only after you can inspect the inputs and delete the captures.</p></div>",
        ]),
    ],
    "pt": [
        ("Por que o Screenpipe importa para criadores sociais", [
            "<p>A publicação social raramente começa no editor da rede. O criador pesquisa no navegador, compara posts, participa de uma reunião, escreve em um editor de texto, verifica uma fonte e só depois publica no X, Bluesky ou em uma Newsletter do LinkedIn. O post final é público, mas o raciocínio que o produziu costuma ficar espalhado entre abas, notas e memória.</p>",
            "<p>O <a href=\"https://screenpi.pe/\">Screenpipe</a> segue outro caminho: ele roda no computador e transforma atividade de tela e áudio em uma memória local pesquisável. O README do projeto descreve captura de tela, dados de acessibilidade, OCR como fallback, transcrição, identificação de falantes, troca de aplicativos e fluxos com agentes. Isso interessa a criadores que querem recuperar o contexto da pesquisa ou disparar uma automação sem enviar cada nota privada de trabalho para um serviço de IA hospedado.</p>",
            "<p>Ele não substitui uma API de publicação e não é uma licença para raspar material privado. Pense nele como uma camada local de captura ao redor do fluxo editorial. Use-o para lembrar o que viu durante a pesquisa, criar uma passagem repetível para um agente e manter o artefato público final portátil com o ThreadGrab.</p>",
        ]),
        ("O que o Screenpipe captura — e o que não captura", [
            "<p>O Screenpipe foi projetado para capturar o que acontece em um computador: contexto visual, áudio, texto da árvore de acessibilidade quando disponível e OCR quando os dados estruturados não existem. O projeto informa que os dados ficam na máquina local e também lista criptografia opcional em repouso e filtros para aplicativos, janelas, extensões do navegador, senhas e modelos de PII de IA.</p>",
            "<p>Essa diferença importa para o conteúdo social. Uma gravação local pode ajudar a lembrar uma página-fonte, uma demonstração de produto ou a redação exata de uma análise. Ela não dá automaticamente permissão para republicar um artigo pago, uma mensagem privada, uma conversa com cliente ou a tela de um colega. Sua política de arquivo ainda define o que pode ser retido e o que precisa ser apagado.</p>",
            "<div class=\"callout\"><p><strong>Regra prática:</strong> capture seu próprio fluxo por padrão. Inclua uma etapa explícita de consentimento antes de gravar reuniões, material de clientes ou a voz e a tela de outra pessoa.</p></div>",
        ]),
        ("Screenpipe vs APIs oficiais vs captura no navegador", [
            "<p>Criadores costumam perguntar se uma ferramenta local de tela e áudio pode substituir a API do X, do Bluesky ou uma exportação do LinkedIn. Na prática, não: as ferramentas resolvem problemas diferentes.</p>",
            "<table><thead><tr><th>Abordagem</th><th>Melhor para</th><th>Principal troca</th></tr></thead><tbody><tr><td>API ou exportação oficial</td><td>Dados públicos estruturados, identificadores estáveis, consultas repetíveis</td><td>Limites de acesso, autenticação, regras de produto que mudam</td></tr><tr><td>Screenpipe</td><td>Contexto local de trabalho, memória de pesquisa, gatilhos de agente</td><td>Armazenamento, controles de privacidade, dados visuais menos estruturados</td></tr><tr><td>Captura no navegador</td><td>Páginas públicas pontuais e evidência visual</td><td>Seletores frágeis, limpeza manual, retenção pouco clara</td></tr><tr><td>ThreadGrab</td><td>Cópias legíveis em Markdown de posts sociais públicos</td><td>Só captura conteúdo que está publicamente acessível</td></tr></tbody></table>",
            "<p>Um bom fluxo combina as opções. Use uma API oficial quando precisar de registros estruturados em escala. Use o Screenpipe quando o contexto importante for o caminho percorrido na pesquisa. Use o ThreadGrab depois da publicação para criar um arquivo limpo e legível do próprio post público.</p>",
        ]),
        ("Instale e teste um fluxo de captura local", [
            "<p>O projeto Screenpipe oferece um aplicativo para desktop e um caminho pela linha de comando. Os comandos abaixo vêm do README do projeto. Comece com um teste curto e deliberado, em vez de deixar a captura contínua ligada sem verificar armazenamento e configurações de privacidade.</p>",
            "<pre><code>npx screenpipe record\nnpx screenpipe setup</code></pre>",
            "<p>Depois da configuração, faça uma pergunta restrita sobre uma janela recente de atividade. Por exemplo, verifique se o índice local distingue uma sessão de pesquisa no navegador de uma sessão de escrita. Confirme onde os dados são armazenados, quais aplicativos estão excluídos e como você apagará gravações antigas antes de conectar o fluxo a um agente.</p>",
            "<p>O README lista como referência cerca de 5–10% de CPU, 0,5–3 GB de RAM e aproximadamente 20 GB de armazenamento por mês, mas trate esses números como orientação reportada pelo projeto, não como promessa para sua máquina. Resolução de vídeo, áudio, OCR, retenção e carga de trabalho mudam o consumo.</p>",
        ]),
        ("Conecte um agente sem perder o controle editorial", [
            "<p>O README do Screenpipe também mostra um caminho MCP para conectar a memória local a um assistente. A ideia não é deixar um agente publicar sozinho. A ideia é permitir perguntas limitadas, como “qual fonte consultei antes de escrever esta thread?” ou “resuma a sessão de pesquisa desta tarde”.</p>",
            "<pre><code>claude mcp add screenpipe -- npx -y screenpipe-mcp@latest</code></pre>",
            "<p>Mantenha as permissões do agente estreitas. Uma primeira versão segura é a busca somente leitura em uma pasta ou intervalo de tempo selecionado, com o rascunho final escrito em um arquivo Markdown local para revisão humana. Só depois de inspecionar entradas e saídas considere uma automação que crie um rascunho em outra ferramenta.</p>",
            "<p>Para criadores sociais, a passagem mais valiosa costuma ser uma nota de procedência: URL da fonte, hora da captura, afirmação usada e transformação feita no post final. Essa nota é mais útil do que uma instrução vaga para “escrever uma thread viral”.</p>",
        ]),
        ("Transforme a pesquisa em um rascunho social canônico", [
            "<p>Use o Screenpipe para contexto, não como banco de conteúdo canônico. Quando a pesquisa terminar, crie um pequeno arquivo Markdown com tese, links, fatos citados, observações pessoais e perguntas abertas. Assim, X Articles, posts longos do Bluesky e Newsletters do LinkedIn têm um argumento estável para adaptar.</p>",
            "<ol><li><strong>Capture:</strong> grave apenas a janela de pesquisa ou reunião que você tem autorização para reter.</li><li><strong>Extraia:</strong> peça ao agente local uma lista de fontes, horários e afirmações ainda não verificadas.</li><li><strong>Escreva:</strong> produza um rascunho Markdown revisado por uma pessoa e com links.</li><li><strong>Adapte:</strong> mude abertura, tamanho e chamada à ação por plataforma sem mudar o núcleo factual.</li><li><strong>Arquive:</strong> salve a fonte Markdown e capture as URLs públicas depois da publicação.</li></ol>",
            "<p>Essa separação evita uma falha comum: a gravação de tela virar a única cópia da ideia. A gravação é uma evidência útil, mas um arquivo Markdown revisado é mais fácil de pesquisar, comparar, citar, migrar e entregar a outro editor.</p>",
        ]),
        ("Arquive o resultado público com o ThreadGrab", [
            "<p>Depois que o post estiver no ar, capture a versão pública separadamente. O <a href=\"https://threadgrab.com/pt/\">ThreadGrab</a> foi criado para transformar conteúdo público do X, Bluesky e LinkedIn em Markdown legível. Isso fornece um resultado portátil mesmo que a plataforma mude o editor, esconda um post antigo atrás de outra navegação ou torne uma thread longa difícil de ler.</p>",
            "<p>Mantenha três registros relacionados: o rascunho Markdown canônico, a URL pública da plataforma e o horário da captura pelo ThreadGrab. Se o post veio de uma sessão do Screenpipe, guarde o identificador local ou uma breve nota de procedência — não a gravação privada inteira em um arquivo público.</p>",
            "<p>O arquivo deve preservar atribuição e contexto. Não remova uma correção, divulgação, fonte citada ou etiqueta da plataforma só para deixar o Markdown mais bonito. Um bom arquivo não é apenas backup; é um registro do que foi realmente publicado.</p>",
        ]),
        ("Checklist de privacidade, consentimento e retenção", [
            "<p>O desenho local-first do Screenpipe reduz um tipo de exposição, mas não elimina riscos. Um notebook pode ser perdido, um backup pode ser copiado e um agente pode mostrar texto sensível no contexto errado. Antes de ativar captura contínua, escreva os limites.</p>",
            "<ul><li>Exclua gerenciadores de senha, bancos, mensagens privadas, ferramentas de RH e sistemas de clientes.</li><li>Obtenha consentimento antes de gravar voz, reunião ou tela de outra pessoa.</li><li>Defina um prazo de retenção e teste a exclusão, em vez de presumir que funciona.</li><li>Mantenha arquivos públicos separados das gravações privadas de pesquisa.</li><li>Leia a licença e os termos comerciais atuais antes de usar o projeto em um fluxo de equipe ou cliente.</li><li>Identifique material assistido por IA com honestidade quando isso afetar confiança ou conformidade da plataforma.</li></ul>",
            "<p>Se você não consegue explicar quem acessa uma captura, por quanto tempo ela permanece e como apagá-la, o fluxo ainda não está pronto para automação. Comece com um experimento privado curto e só amplie quando a política estiver clara.</p>",
        ]),
        ("Limites e trocas práticas", [
            "<p>O Screenpipe é atraente quando o gargalo é contexto, mas adiciona um sistema para manter. O armazenamento cresce. OCR e transcrição podem interpretar nomes ou URLs de forma errada. Contexto visual é mais difícil de consultar do que uma resposta de API estruturada. Captura contínua também pode criar muito material que ninguém revisa.</p>",
            "<p>Existe ainda uma questão de licença. O repositório descreve o projeto como source-available e informa que o uso pessoal e não comercial é permitido, enquanto o uso comercial exige uma licença; verifique o arquivo LICENSE e os termos comerciais atuais antes de implantá-lo para cliente ou equipe. A mesma leitura cuidadosa vale para cada plataforma cujo conteúdo você captura.</p>",
            "<p>O melhor caso de uso é focado: capture um fluxo de pesquisa delimitado, extraia o contexto necessário, escreva um rascunho canônico e arquive o resultado público. Isso é mais defensável do que gravar tudo esperando que um agente encontre valor depois.</p>",
        ]),
        ("Perguntas frequentes", [
            "<div class=\"faq-item\"><strong>O Screenpipe substitui a API do X, Bluesky ou LinkedIn?</strong><p>Não. O Screenpipe captura o contexto local de trabalho, enquanto APIs oficiais fornecem dados estruturados da plataforma. Use cada ferramenta para a função que ela foi projetada para cumprir.</p></div>",
            "<div class=\"faq-item\"><strong>O Screenpipe é privado por rodar localmente?</strong><p>O modelo local-first reduz o envio para a nuvem, mas não elimina riscos de dispositivo, backup, acesso ou consentimento. Configure exclusões, retenção e permissões antes da captura contínua.</p></div>",
            "<div class=\"faq-item\"><strong>Posso usar o Screenpipe para arquivar posts privados de outra pessoa?</strong><p>Não presuma que acesso técnico é permissão. Capture apenas material que você pode reter e republicar, respeitando regras da plataforma e a legislação de privacidade aplicável.</p></div>",
            "<div class=\"faq-item\"><strong>Por que usar o ThreadGrab depois do Screenpipe?</strong><p>O Screenpipe preserva o contexto local do processo. O ThreadGrab cria uma cópia Markdown legível do resultado social público. Juntos, eles separam pesquisa privada de arquivos portáteis de publicação.</p></div>",
            "<div class=\"faq-item\"><strong>Como um criador deve começar?</strong><p>Faça um teste local curto, exclua aplicativos sensíveis, crie um rascunho Markdown e arquive um post público. Adicione um agente somente depois de inspecionar as entradas e apagar as capturas.</p></div>",
        ]),
    ],
    "id": [
        ("Mengapa Screenpipe penting bagi kreator sosial", [
            "<p>Penerbitan sosial jarang dimulai dari editor media sosial. Kreator meneliti di browser, membandingkan postingan, mengikuti rapat, menulis di editor teks, memeriksa sumber, lalu menerbitkan ke X, Bluesky, atau LinkedIn Newsletter. Postingan akhirnya publik, tetapi alasan dan konteks di baliknya biasanya tersebar di tab, catatan, dan ingatan.</p>",
            "<p><a href=\"https://screenpi.pe/\">Screenpipe</a> memakai pendekatan berbeda: aplikasi ini berjalan di komputer dan mengubah aktivitas layar serta audio menjadi memori lokal yang bisa dicari. README proyek menjelaskan screen capture, data aksesibilitas, fallback OCR, transkripsi, pembicara, perpindahan aplikasi, dan alur kerja agent. Ini menarik bagi kreator yang ingin memulihkan konteks riset atau memicu otomasi tanpa mengirim semua catatan kerja pribadi ke layanan AI yang di-host.</p>",
            "<p>Screenpipe bukan pengganti publishing API dan bukan izin untuk mengambil materi privat. Anggap sebagai lapisan capture lokal di sekitar alur editorial. Gunakan untuk mengingat apa yang dilihat saat riset, membuat handoff yang dapat diulang untuk agent, dan menjaga artefak publik akhir tetap portabel dengan ThreadGrab.</p>",
        ]),
        ("Apa yang ditangkap Screenpipe — dan apa yang tidak", [
            "<p>Screenpipe dirancang untuk menangkap apa yang terjadi di komputer: konteks visual, audio, teks dari accessibility tree jika tersedia, dan OCR ketika data aksesibilitas terstruktur tidak ada. Proyek ini menyatakan data tetap di mesin lokal, serta mencantumkan enkripsi saat tersimpan dan filter untuk aplikasi, window, ekstensi browser, password, serta model PII AI sebagai opsi.</p>",
            "<p>Perbedaan ini penting untuk konten sosial. Rekaman lokal dapat membantu mengingat halaman sumber, demo produk, atau kalimat persis dalam draft review. Rekaman itu tidak otomatis memberi izin untuk menerbitkan ulang artikel berbayar, pesan privat, percakapan pelanggan, atau layar rekan kerja. Kebijakan arsip Anda tetap menentukan apa yang boleh disimpan dan apa yang harus dihapus.</p>",
            "<div class=\"callout\"><p><strong>Aturan praktis:</strong> secara default, tangkap workflow Anda sendiri. Tambahkan langkah consent yang jelas sebelum merekam rapat, materi pelanggan, atau suara dan layar orang lain.</p></div>",
        ]),
        ("Screenpipe vs API resmi vs capture browser", [
            "<p>Kreator sering bertanya apakah alat layar dan audio lokal dapat menggantikan X API, Bluesky API, atau ekspor LinkedIn. Jawaban praktisnya tidak: setiap alat menyelesaikan masalah berbeda.</p>",
            "<table><thead><tr><th>Pendekatan</th><th>Cocok untuk</th><th>Trade-off utama</th></tr></thead><tbody><tr><td>API atau ekspor resmi</td><td>Data publik terstruktur, identifier stabil, query berulang</td><td>Batas akses, autentikasi, aturan produk yang berubah</td></tr><tr><td>Screenpipe</td><td>Konteks workflow lokal, memori riset, pemicu agent</td><td>Penyimpanan, kontrol privasi, data visual lebih sulit distrukturkan</td></tr><tr><td>Capture browser</td><td>Halaman publik satu kali dan bukti visual</td><td>Selector rapuh, pembersihan manual, retensi tidak jelas</td></tr><tr><td>ThreadGrab</td><td>Salinan Markdown yang mudah dibaca dari postingan sosial publik</td><td>Hanya menangkap konten yang dapat diakses publik</td></tr></tbody></table>",
            "<p>Workflow yang kuat menggabungkan semuanya. Gunakan API resmi saat membutuhkan record terstruktur dalam skala besar. Gunakan Screenpipe saat konteks pentingnya adalah jalur riset yang Anda tempuh. Gunakan ThreadGrab setelah publish untuk membuat arsip Markdown yang bersih dan mudah dibaca dari postingan publik.</p>",
        ]),
        ("Instal dan uji workflow capture lokal", [
            "<p>Proyek Screenpipe menyediakan aplikasi desktop dan jalur command line. Perintah di bawah berasal dari README proyek. Mulailah dengan uji singkat dan sengaja, bukan menyalakan capture terus-menerus tanpa mengecek storage dan pengaturan privasi.</p>",
            "<pre><code>npx screenpipe record\nnpx screenpipe setup</code></pre>",
            "<p>Setelah setup, ajukan pertanyaan sempit tentang jendela aktivitas terbaru. Misalnya, pastikan indeks lokal dapat membedakan sesi riset browser dari sesi menulis. Konfirmasi lokasi penyimpanan data, aplikasi yang dikecualikan, dan cara menghapus rekaman lama sebelum menghubungkan workflow ke agent.</p>",
            "<p>README mencantumkan acuan sekitar 5–10% CPU, 0,5–3 GB RAM, dan sekitar 20 GB storage per bulan, tetapi anggap itu sebagai panduan yang dilaporkan proyek, bukan janji untuk mesin Anda. Resolusi video, audio, OCR, retensi, dan beban kerja mengubah penggunaan resource.</p>",
        ]),
        ("Hubungkan agent tanpa kehilangan kontrol editorial", [
            "<p>README Screenpipe juga menunjukkan jalur MCP untuk menghubungkan memori lokal ke assistant. Tujuannya bukan membiarkan agent publish otomatis. Tujuannya adalah menjawab pertanyaan terbatas seperti “sumber apa yang saya lihat sebelum menulis thread ini?” atau “ringkas sesi riset sore ini.”</p>",
            "<pre><code>claude mcp add screenpipe -- npx -y screenpipe-mcp@latest</code></pre>",
            "<p>Jaga izin agent tetap sempit. Versi pertama yang aman adalah pencarian read-only pada folder atau rentang waktu tertentu, dengan draft final ditulis ke file Markdown lokal untuk ditinjau manusia. Hanya setelah Anda bisa memeriksa input dan output, pertimbangkan otomasi yang membuat draft di alat lain.</p>",
            "<p>Bagi kreator sosial, handoff paling bernilai biasanya adalah catatan provenance: URL sumber, waktu capture, klaim yang digunakan, dan transformasi pada postingan final. Catatan ini lebih berguna daripada instruksi samar untuk “tulis thread viral”.</p>",
        ]),
        ("Ubah riset menjadi satu draft sosial kanonis", [
            "<p>Gunakan Screenpipe untuk konteks, bukan sebagai database konten kanonis. Setelah sesi riset selesai, buat file Markdown kecil berisi tesis, link, fakta yang dikutip, observasi pribadi, dan pertanyaan terbuka. Dengan begitu X Articles, postingan panjang Bluesky, dan LinkedIn Newsletter memiliki argumen stabil untuk diadaptasi.</p>",
            "<ol><li><strong>Capture:</strong> rekam hanya jendela riset atau rapat yang boleh Anda simpan.</li><li><strong>Ekstrak:</strong> minta agent lokal membuat daftar sumber, timestamp, dan klaim yang belum selesai diverifikasi.</li><li><strong>Tulis:</strong> buat satu draft Markdown yang sudah ditinjau manusia dan memiliki link.</li><li><strong>Adaptasi:</strong> ubah pembuka, panjang, dan call to action per platform tanpa mengubah inti faktual.</li><li><strong>Arsipkan:</strong> simpan sumber Markdown dan capture URL publik setelah publish.</li></ol>",
            "<p>Pemisahan ini mencegah kegagalan umum: rekaman layar menjadi satu-satunya salinan ide. Rekaman adalah bukti yang berguna, tetapi file Markdown yang sudah ditinjau lebih mudah dicari, dibandingkan, dikutip, dipindahkan, dan diberikan kepada editor lain.</p>",
        ]),
        ("Arsipkan hasil publik dengan ThreadGrab", [
            "<p>Setelah postingan live, capture versi publik secara terpisah. <a href=\"https://threadgrab.com/id/\">ThreadGrab</a> dibuat untuk mengubah konten X, Bluesky, dan LinkedIn yang publik menjadi Markdown yang mudah dibaca. Hasilnya tetap portabel jika platform mengubah editor, menyembunyikan postingan lama di balik navigasi baru, atau membuat thread panjang sulit dibaca.</p>",
            "<p>Simpan tiga record yang terkait: draft Markdown kanonis, URL publik platform, dan timestamp capture ThreadGrab. Jika postingan berasal dari sesi Screenpipe, simpan identifier sesi lokal atau catatan provenance singkat — bukan seluruh rekaman privat di arsip publik.</p>",
            "<p>Arsip harus mempertahankan atribusi dan konteks. Jangan menghapus koreksi, disclosure, sumber yang dikutip, atau label platform hanya agar Markdown terlihat lebih rapi. Arsip yang berguna bukan sekadar backup; ia mencatat apa yang benar-benar diterbitkan.</p>",
        ]),
        ("Checklist privasi, consent, dan retensi", [
            "<p>Desain local-first Screenpipe mengurangi satu jenis paparan, tetapi tidak menghilangkan risiko. Laptop bisa hilang, backup bisa disalin, dan agent bisa menampilkan teks sensitif pada konteks yang salah. Sebelum menyalakan capture terus-menerus, tuliskan batasannya.</p>",
            "<ul><li>Kecualikan password manager, perbankan, pesan privat, alat HR, dan sistem pelanggan.</li><li>Dapatkan consent sebelum merekam suara, rapat, atau layar orang lain.</li><li>Tetapkan masa retensi dan uji penghapusan, jangan hanya menganggapnya bekerja.</li><li>Pisahkan arsip publik dari rekaman riset privat.</li><li>Periksa lisensi dan ketentuan komersial terbaru sebelum memakai proyek untuk workflow tim atau klien.</li><li>Labeli materi yang dibantu AI secara jujur saat hal itu memengaruhi kepercayaan audiens atau kepatuhan platform.</li></ul>",
            "<p>Jika Anda tidak dapat menjelaskan siapa yang bisa mengakses capture, berapa lama ia disimpan, dan bagaimana menghapusnya, workflow belum siap untuk otomasi. Mulai dari eksperimen privat yang singkat dan perluas hanya saat kebijakannya jelas.</p>",
        ]),
        ("Batasan dan trade-off praktis", [
            "<p>Screenpipe menarik ketika bottleneck-nya adalah konteks, tetapi ia menambah sistem yang harus dirawat. Storage bertambah seiring waktu. OCR dan transkripsi bisa salah membaca nama atau URL. Konteks visual lebih sulit di-query daripada respons API terstruktur. Continuous capture juga dapat menghasilkan banyak materi yang tidak pernah ditinjau.</p>",
            "<p>Ada pertanyaan lisensi juga. Repository menjelaskan proyek sebagai source-available dan menyebut penggunaan personal non-komersial diperbolehkan, sementara penggunaan komersial memerlukan lisensi; periksa file LICENSE dan ketentuan komersial terbaru sebelum deployment untuk klien atau tim. Baca juga aturan setiap platform yang kontennya Anda capture.</p>",
            "<p>Use case terbaik bersifat fokus: capture workflow riset yang dibatasi, ekstrak konteks yang dibutuhkan, tulis draft kanonis, lalu arsipkan hasil publik. Ini lebih defensible daripada merekam semuanya dan berharap agent menemukan nilai di kemudian hari.</p>",
        ]),
        ("Pertanyaan yang sering diajukan", [
            "<div class=\"faq-item\"><strong>Apakah Screenpipe menggantikan API X, Bluesky, atau LinkedIn?</strong><p>Tidak. Screenpipe menangkap konteks workflow lokal, sedangkan API resmi menyediakan data platform yang terstruktur. Gunakan masing-masing untuk pekerjaan yang memang dirancang untuknya.</p></div>",
            "<div class=\"faq-item\"><strong>Apakah Screenpipe privat karena berjalan lokal?</strong><p>Model local-first mengurangi pengiriman ke cloud, tetapi tidak menghapus risiko perangkat, backup, akses, atau consent. Atur pengecualian, retensi, dan izin sebelum continuous capture.</p></div>",
            "<div class=\"faq-item\"><strong>Bolehkah memakai Screenpipe untuk mengarsipkan postingan privat orang lain?</strong><p>Jangan menganggap akses teknis sebagai izin. Capture hanya materi yang boleh Anda simpan dan terbitkan ulang, dengan mengikuti aturan platform dan hukum privasi yang berlaku.</p></div>",
            "<div class=\"faq-item\"><strong>Mengapa memakai ThreadGrab setelah Screenpipe?</strong><p>Screenpipe menjaga konteks proses lokal. ThreadGrab membuat salinan Markdown yang mudah dibaca dari hasil sosial publik. Keduanya memisahkan riset privat dari arsip publik yang portabel.</p></div>",
            "<div class=\"faq-item\"><strong>Bagaimana kreator sebaiknya memulai?</strong><p>Jalankan uji lokal singkat, kecualikan aplikasi sensitif, buat satu draft Markdown, dan arsipkan satu postingan publik. Tambahkan agent setelah Anda bisa memeriksa input dan menghapus capture.</p></div>",
        ]),
    ],
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0f0f0f;color:#fff;line-height:1.6}
header{padding:20px 24px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #1a1a1a}
.logo{font-size:1.4rem;font-weight:700;color:#fff;text-decoration:none}.logo span{color:#20d5ec}
.lang-bar{margin-left:auto;display:flex;gap:6px}.lang-bar a{color:#888;text-decoration:none;font-size:.85rem;padding:4px 8px;border-radius:4px}.lang-bar a:hover,.lang-bar a.active{color:#fff;background:#222}
main{max-width:760px;margin:0 auto;padding:40px 20px 60px}.breadcrumb{color:#666;font-size:.85rem;margin-bottom:24px}.breadcrumb a{color:#20d5ec;text-decoration:none}
h1{font-size:clamp(1.7rem,4.5vw,2.4rem);line-height:1.25;margin-bottom:12px}h2{color:#20d5ec;font-size:1.4rem;margin:36px 0 14px;line-height:1.3}
p{color:#ccc;margin-bottom:14px;font-size:1rem}a{color:#20d5ec}ul,ol{color:#ccc;padding-left:22px;margin-bottom:14px}li{margin-bottom:6px;font-size:1rem}
table{width:100%;border-collapse:collapse;margin:20px 0 28px;font-size:.9rem}th,td{padding:10px 12px;text-align:left;border-bottom:1px solid #222;vertical-align:top}th{background:#1a1a1a;color:#20d5ec;font-weight:600}td{color:#ccc}
.callout{background:#11212a;border-left:3px solid #20d5ec;padding:16px 20px;border-radius:4px;margin:20px 0}.callout p{color:#b5dde3;margin-bottom:0}
pre{background:#0a0a0a;border:1px solid #1f1f1f;border-radius:8px;padding:14px 18px;overflow-x:auto;margin:16px 0 20px}pre code{font-family:'SF Mono',Menlo,Consolas,monospace;font-size:.88rem;color:#c5e8ee;white-space:pre}
code:not(pre code){background:#1a1a1a;padding:2px 6px;border-radius:3px;font-size:.9em;color:#20d5ec}.faq-item{background:#1a1a1a;border-radius:8px;padding:16px 20px;margin-bottom:12px}.faq-item strong{color:#20d5ec;display:block;margin-bottom:6px}.faq-item p{color:#ccc;margin-bottom:0;font-size:.95rem}
.cta{background:linear-gradient(135deg,#11212a,#0d1a20);border:1px solid #20d5ec;border-radius:10px;padding:22px 24px;margin:28px 0;text-align:center}.cta p{color:#c5e8ee;margin-bottom:12px}.cta a.btn{display:inline-block;background:#20d5ec;color:#000;font-weight:600;padding:11px 26px;border-radius:8px;text-decoration:none}.cta a.btn:hover{background:#1bc4d4}
footer{text-align:center;padding:40px 24px 24px;color:#444;font-size:.8rem;border-top:1px solid #1a1a1a;margin-top:40px}footer a{color:#666;text-decoration:none;margin:0 8px}footer a:hover{color:#20d5ec}
@media(max-width:640px){main{padding:24px 16px 40px}table{font-size:.8rem}th,td{padding:8px}}
"""


def json_script(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False) + '\n</script>'


def build(lang):
    slug = SLUGS[lang]
    title = TITLES[lang]
    desc = DESCS[lang]
    ui = UI[lang]
    urls = {l: f"https://threadgrab.com/{l}/blog/{SLUGS[l]}.html" for l in SLUGS}
    article_url = urls[lang]

    body_parts = []
    for heading, fragments in BODIES[lang]:
        body_parts.append(f"<h2>{heading}</h2>")
        body_parts.extend(fragments)
    body_parts.append(f'<div class="cta"><p><strong>ThreadGrab</strong></p><p>{html.escape(desc)}</p><a class="btn" href="/{lang}/">{"Try ThreadGrab →" if lang == "en" else "Experimente o ThreadGrab →" if lang == "pt" else "Coba ThreadGrab →"}</a></div>')
    body = "\n".join(body_parts)

    faq_questions = {
        "en": [
            ("Can Screenpipe replace the X, Bluesky, or LinkedIn API?", "No. Screenpipe captures local workflow context, while official APIs provide structured platform data. Use each for the job it is designed to do."),
            ("Is Screenpipe private because it runs locally?", "Local-first reduces cloud transmission, but it does not remove device, backup, access, or consent risks. Configure exclusions, retention, and permissions before continuous capture."),
            ("Can I use Screenpipe to archive another person’s private posts?", "Do not assume that technical access is permission. Capture only material you are allowed to retain and republish, and follow platform rules and applicable privacy law."),
            ("Why use ThreadGrab after Screenpipe?", "Screenpipe preserves local process context. ThreadGrab creates a readable Markdown copy of the public social result. Together they separate private research from portable publication archives."),
            ("How should a creator start?", "Run a short local test, exclude sensitive apps, create one Markdown draft, and archive one public post. Add an agent only after you can inspect the inputs and delete the captures."),
        ],
        "pt": [
            ("O Screenpipe substitui a API do X, Bluesky ou LinkedIn?", "Não. O Screenpipe captura o contexto local de trabalho, enquanto APIs oficiais fornecem dados estruturados da plataforma. Use cada ferramenta para a função que ela foi projetada para cumprir."),
            ("O Screenpipe é privado por rodar localmente?", "O modelo local-first reduz o envio para a nuvem, mas não elimina riscos de dispositivo, backup, acesso ou consentimento. Configure exclusões, retenção e permissões antes da captura contínua."),
            ("Posso usar o Screenpipe para arquivar posts privados de outra pessoa?", "Não presuma que acesso técnico é permissão. Capture apenas material que você pode reter e republicar, respeitando regras da plataforma e a legislação de privacidade aplicável."),
            ("Por que usar o ThreadGrab depois do Screenpipe?", "O Screenpipe preserva o contexto local do processo. O ThreadGrab cria uma cópia Markdown legível do resultado social público. Juntos, eles separam pesquisa privada de arquivos portáteis de publicação."),
            ("Como um criador deve começar?", "Faça um teste local curto, exclua aplicativos sensíveis, crie um rascunho Markdown e arquive um post público. Adicione um agente somente depois de inspecionar as entradas e apagar as capturas."),
        ],
        "id": [
            ("Apakah Screenpipe menggantikan API X, Bluesky, atau LinkedIn?", "Tidak. Screenpipe menangkap konteks workflow lokal, sedangkan API resmi menyediakan data platform yang terstruktur. Gunakan masing-masing untuk pekerjaan yang memang dirancang untuknya."),
            ("Apakah Screenpipe privat karena berjalan lokal?", "Model local-first mengurangi pengiriman ke cloud, tetapi tidak menghapus risiko perangkat, backup, akses, atau consent. Atur pengecualian, retensi, dan izin sebelum continuous capture."),
            ("Bolehkah memakai Screenpipe untuk mengarsipkan postingan privat orang lain?", "Jangan menganggap akses teknis sebagai izin. Capture hanya materi yang boleh Anda simpan dan terbitkan ulang, dengan mengikuti aturan platform dan hukum privasi yang berlaku."),
            ("Mengapa memakai ThreadGrab setelah Screenpipe?", "Screenpipe menjaga konteks proses lokal. ThreadGrab membuat salinan Markdown yang mudah dibaca dari hasil sosial publik. Keduanya memisahkan riset privat dari arsip publik yang portabel."),
            ("Bagaimana kreator sebaiknya memulai?", "Jalankan uji lokal singkat, kecualikan aplikasi sensitif, buat satu draft Markdown, dan arsipkan satu postingan publik. Tambahkan agent setelah Anda bisa memeriksa input dan menghapus capture."),
        ],
    }
    faq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_questions[lang]]
    article_schema = {
        "@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
        "datePublished": DATE_ISO, "dateModified": DATE_ISO,
        "author": {"@type": "Organization", "name": "ThreadGrab", "url": f"https://threadgrab.com/{lang}/"},
        "publisher": {"@type": "Organization", "name": "ThreadGrab", "url": f"https://threadgrab.com/{lang}/"},
        "mainEntityOfPage": article_url, "inLanguage": lang,
    }
    breadcrumb_schema = {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": f"https://threadgrab.com/{lang}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"https://threadgrab.com/{lang}/blog/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": article_url},
        ],
    }
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq}

    safe_title = html.escape(title, quote=True)
    safe_desc = html.escape(desc, quote=True)
    safe_kw = html.escape(KEYWORDS[lang], quote=True)
    active_attr = ' class="active"'
    link_items = []
    for l in ("en", "pt", "id"):
        cls = active_attr if l == lang else ""
        link_items.append(f'<a href="{urls[l]}"{cls}>{l.upper()}</a>')
    lang_links = "".join(link_items)
    cta_text = {"en": "Try ThreadGrab →", "pt": "Experimente o ThreadGrab →", "id": "Coba ThreadGrab →"}[lang]
    meta = f"{DATES[lang]} &middot; {ui['read']} &middot; {ui['type']}"

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <meta name="description" content="{safe_desc}">
  <meta name="keywords" content="{safe_kw}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="ThreadGrab">
  <link rel="canonical" href="{article_url}">
  <link rel="alternate" hreflang="en" href="{urls['en']}">
  <link rel="alternate" hreflang="pt" href="{urls['pt']}">
  <link rel="alternate" hreflang="id" href="{urls['id']}">
  <link rel="alternate" hreflang="x-default" href="{urls['en']}">
  <meta property="og:title" content="{safe_title}">
  <meta property="og:description" content="{safe_desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{article_url}">
  <meta property="og:site_name" content="ThreadGrab">
  <meta property="og:locale" content="{LOCALES[lang]}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{safe_title}">
  <meta name="twitter:description" content="{safe_desc}">
  <meta name="twitter:site" content="@threadgrab">
  <style>{CSS}</style>
  {json_script(article_schema)}
  {json_script(breadcrumb_schema)}
  {json_script(faq_schema)}
</head>
<body>
  <header>
    <a class="logo" href="/{lang}/">Thread<span>Grab</span></a>
    <div class="lang-bar">{lang_links}</div>
  </header>
  <main>
    <div class="breadcrumb"><a href="/{lang}/">{ui['home']}</a> &rsaquo; <a href="/{lang}/blog/">Blog</a> &rsaquo; {safe_title}</div>
    <article>
      <div class="article-meta">{meta}</div>
      <h1>{safe_title}</h1>
      {body}
    </article>
  </main>
  <footer>
    &copy; 2026 ThreadGrab &middot; <a href="/{lang}/">{ui['home']}</a> &middot; <a href="/{lang}/blog/">Blog</a> &middot; <a href="/{lang}/about/">{ui['about']}</a> &middot; <a href="/{lang}/privacy/">{ui['privacy']}</a>
    <br>{ui['notaff']}
  </footer>
</body>
</html>'''


os.makedirs(OUTDIR, exist_ok=True)
for lang in ("en", "pt", "id"):
    title_len = len(TITLES[lang])
    desc_len = len(DESCS[lang])
    assert 30 <= title_len <= 60, (lang, "title", title_len)
    assert 70 <= desc_len <= 155, (lang, "description", desc_len)
    content = build(lang)
    # Defensive checks before writing.
    assert content.count('<link rel="alternate" hreflang=') == 4
    assert content.count('<script type="application/ld+json">') == 3
    assert content.count('<pre><code>') == 2
    assert content.count('`') == 0
    fp = os.path.join(OUTDIR, f"{SLUGS[lang]}.html")
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"wrote {fp} bytes={len(content)} title={title_len} desc={desc_len}")

print("SLUGS", json.dumps(SLUGS, ensure_ascii=False))
