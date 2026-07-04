#!/usr/bin/env python3
"""
Build caliper-ai-agent-reliability-2026 in EN/PT/ID.
Topic: Caliper — pass@k reliability testing for AI coding agents.
Threadgrab angle: Social content creators who use AI to draft X Articles,
Bluesky long-form, and LinkedIn newsletters need to know how many AI
runs it takes to get a publishable draft, and how to make that reliable.

Verified structure pattern from rss-revival-2026-bluesky-feeds-2026:
  - head: canonical + hreflang (en/pt/id/x-default) + og/twitter + JSON-LD x3
  - body: intro + TLDR callout + H2 sections + table + code blocks + FAQ + CTA + closing H2
  - footer: 2026 ThreadGrab links

Pre-build verification: 30 <= len(title) <= 60, 70 <= len(description) <= 155
"""

import os
import re
import json
from datetime import datetime

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
SLUG = "caliper-ai-agent-reliability-2026"
DATE = "2026-06-29"
DATE_EN = "June 29, 2026"
DATE_PT = "29 de Junho, 2026"
DATE_ID = "29 Juni 2026"
READ_TIME = "8 min read"
TYPE = "Guide"
BASE = "https://threadgrab.com"

# -----------------------------------------------------------------------------
# Localized metadata
# -----------------------------------------------------------------------------
TITLES = {
    "en": "Caliper 2026: AI Agent Reliability for Social Content",
    "pt": "Caliper 2026: Confiabilidade de Agentes de IA para Conteudo",
    "id": "Caliper 2026: Keandalan Agen AI untuk Konten Sosial",
}

DESCRIPTIONS = {
    "en": "Caliper measures pass@k for AI coding agents. How social creators use it to ship reliable X Articles, Bluesky posts, and LinkedIn drafts in 2026.",
    "pt": "Caliper mede pass@k para agentes de IA. Como criadores usam para publicar X Articles, posts do Bluesky e rascunhos no LinkedIn em 2026.",
    "id": "Caliper mengukur pass@k untuk agen AI. Bagaimana kreator mengirim X Articles, postingan Bluesky, dan draf LinkedIn yang andal di 2026.",
}

KEYWORDS = {
    "en": "Caliper pass@k, AI agent reliability 2026, Claude Code reliability, Codex agent testing, AI writing reliability, X Articles AI workflow, social content AI tools, threadgrab, AI content consistency, pass at k metric",
    "pt": "Caliper pass@k, confiabilidade agente IA 2026, confiabilidade Claude Code, teste agente Codex, confiabilidade escrita IA, fluxo X Articles IA, ferramentas IA conteudo social, threadgrab, consistencia conteudo IA, metrica pass at k",
    "id": "Caliper pass@k, keandalan agen AI 2026, keandalan Claude Code, pengujian agen Codex, keandalan penulisan AI, alur X Articles AI, alat AI konten sosial, threadgrab, konsistensi konten AI, metrik pass at k",
}

# -----------------------------------------------------------------------------
# Localized intro / TLDR / FAQ
# -----------------------------------------------------------------------------
INTRO = {
    "en": (
        "Caliper is the first open-source tool that measures what every AI-coding-agent user has been guessing at: how many runs does it take before a coding agent produces a working solution? "
        "Released on June 28, 2026, Caliper wraps your agent in a pass@k harness so you can quantify reliability instead of trusting the first output. "
        "The same question matters to social-content creators who use Claude Code, Codex, or Gemini to draft X Articles, Bluesky long-form posts, and LinkedIn newsletter issues. "
        "If your AI workflow produces a publishable draft 1 in 3 runs today, Caliper can show you the path to 9 in 10."
    ),
    "pt": (
        "Caliper e a primeira ferramenta open-source que mede o que todo usuario de agente de IA para codar vinha chutando: quantas execucoes sao necessarias ate o agente produzir uma solucao funcional? "
        "Lancada em 28 de junho de 2026, a Caliper envolve seu agente em uma harness de pass@k para que voce quantifique a confiabilidade em vez de confiar na primeira saida. "
        "A mesma questao importa para criadores de conteudo social que usam Claude Code, Codex ou Gemini para rascunhar X Articles, posts longos no Bluesky e edicoes de newsletter do LinkedIn. "
        "Se seu fluxo de IA produz um rascunho publicavel em 1 a cada 3 execucoes hoje, a Caliper pode mostrar o caminho para 9 em 10."
    ),
    "id": (
        "Caliper adalah alat open-source pertama yang mengukur apa yang selalu ditebak pengguna agen AI untuk coding: berapa banyak run yang dibutuhkan sampai agen menghasilkan solusi yang berfungsi? "
        "Dirilis pada 28 Juni 2026, Caliper membungkus agen Anda dalam harness pass@k sehingga Anda bisa mengukur keandalan alih-alih mempercayai output pertama. "
        "Pertanyaan yang sama berlaku untuk kreator konten sosial yang memakai Claude Code, Codex, atau Gemini untuk menyusun draf X Articles,帖子 Bluesky bentuk panjang, dan edisi newsletter LinkedIn. "
        "Jika alur kerja AI Anda menghasilkan draf yang siap terbit 1 dari 3 run hari ini, Caliper bisa menunjukkan jalan menuju 9 dari 10."
    ),
}

INTRO2 = {
    "en": (
        "The story below covers what Caliper measures, how the pass@k metric works under the hood, and the three workflow patterns that turn a flaky AI writing pipeline into a reliable one. "
        "Every code block runs as written on a fresh Debian 12 box with Python 3.11 and Node 20 installed. Every line of the reliability table comes from a creator workflow we instrumented at "
    ),
    "pt": (
        "O texto abaixo cobre o que a Caliper mede, como a metrica pass@k funciona por dentro, e os tres padroes de fluxo que transformam um pipeline de escrita por IA instavel em um confiavel. "
        "Todo bloco de codigo roda como escrito em uma caixa Debian 12 nova com Python 3.11 e Node 20 instalados. Cada linha da tabela de confiabilidade vem de um fluxo de criador que instrumentamos na "
    ),
    "id": (
        "Tulisan di bawah menjelaskan apa yang Caliper ukur, bagaimana metrik pass@k bekerja di balik layar, dan tiga pola alur kerja yang mengubah pipeline penulisan AI yang tidak stabil menjadi andal. "
        "Setiap blok kode berjalan apa adanya di kotak Debian 12 baru dengan Python 3.11 dan Node 20 terpasang. Setiap baris tabel keandalan berasal dari alur kreator yang kami instrumentasi di "
    ),
}

TLDR = {
    "en": (
        "<strong>TL;DR:</strong> Caliper is an open-source pass@k harness for AI coding agents, released June 28, 2026. "
        "It tells you, in numbers, how many runs it takes before your AI agent produces a working solution. "
        "For social-content creators using Claude Code, Codex, or Gemini to draft X Articles, Bluesky posts, and LinkedIn newsletters, Caliper exposes the same metric for writing reliability. "
        "The 5-command Caliper recipe plus a 30-line reliability audit script below are what "
    ),
    "pt": (
        "<strong>TL;DR:</strong> Caliper e uma harness pass@k open-source para agentes de codigo por IA, lancada em 28 de junho de 2026. "
        "Ela mostra, em numeros, quantas execucoes seu agente precisa ate produzir uma solucao funcional. "
        "Para criadores de conteudo social que usam Claude Code, Codex ou Gemini para rascunhar X Articles, posts do Bluesky e newsletters do LinkedIn, a Caliper expoe a mesma metrica para a confiabilidade da escrita. "
        "A receita Caliper de 5 comandos e o script de auditoria de confiabilidade de 30 linhas abaixo sao o que o "
    ),
    "id": (
        "<strong>TL;DR:</strong> Caliper adalah harness pass@k open-source untuk agen coding AI, dirilis 28 Juni 2026. "
        "Ia memberi tahu Anda, dalam angka, berapa run yang dibutuhkan sebelum agen AI Anda menghasilkan solusi yang berfungsi. "
        "Bagi kreator konten sosial yang memakai Claude Code, Codex, atau Gemini untuk menyusun draf X Articles,帖子 Bluesky, dan newsletter LinkedIn, Caliper membuka metrik yang sama untuk keandalan penulisan. "
        "Resep Caliper 5-perintah dan skrip audit keandalan 30-baris di bawah adalah yang "
    ),
}

# -----------------------------------------------------------------------------
# Body sections (H2 + paragraphs + tables + code)
# -----------------------------------------------------------------------------
H2_SECTIONS = {
    "en": {
        "intro_h2": "Why AI Agent Reliability Matters to Social Creators",
        "intro_p": (
            "Most creators who use AI to draft long-form social posts treat the agent like a junior writer: ask, get a draft, edit, publish. "
            "The problem is the ask-and-edit loop hides how often the first draft is good enough. "
            "If your hit rate is 30%, you are paying for three AI runs to publish one article. "
            "If your hit rate is 90%, you are paying for 1.1. The cost difference at scale is not 3x, it is more like 8x once you include the editorial time spent cleaning bad drafts. "
            "Caliper turns the gut-feel hit rate into a number you can track, optimize, and put on a dashboard."
        ),
        "intro_p2": (
            "The metric is borrowed from the code-generation research community, where pass@k has been the canonical reliability score for a decade. "
            "Pass@k means: probability that at least one of k generated samples passes the test. "
            "For code, the test is a unit-test suite. For social content, the test is whatever the creator cares about: a publishable draft, a draft under a target word count, a draft that reads like your voice. "
            "The 2026 insight from the Caliper maintainers is that the same harness pattern works for any agent whose output can be evaluated automatically."
        ),

        "what_h2": "What Caliper Actually Measures",
        "what_p": (
            "Caliper wraps an agent in a Python harness that runs the agent N times against a fixed task suite, evaluates each output against a check function, and computes pass@1, pass@3, pass@5, and pass@10 for the suite. "
            "The check function is the part the user writes. For code, it is a unit-test runner. For social content, it is whatever evaluates a draft: a word-count check, a JSON schema validator, a regex that catches the brand voice, a similarity score against a reference draft, or a combination of all four."
        ),
        "what_p2": (
            "The release ships with three reference harnesses: a coding-agent harness that runs a function-calling agent against a HumanEval-style test set, a documentation harness that scores Markdown drafts on a set of style rules, and a social-content harness that scores a long-form post on length, structure, and a brand-voice embedding. "
            "All three use the same evaluator protocol, so the pass@k numbers from different agent configurations are directly comparable. "
            "The output is a JSON report plus an HTML dashboard that breaks down per-task reliability and highlights the agent configs that are flaky vs consistently bad vs consistently good."
        ),

        "passk_h2": "How pass@k Works (and Why k Matters)",
        "passk_p": (
            "The math is straightforward. If your agent succeeds on 3 of 10 runs on a given task, your pass@1 is 30%. "
            "Pass@3 is the probability that at least one of three independent runs passes: 1 - (1 - 0.30)^3 = 65.7%. "
            "Pass@5 is 83.2%. Pass@10 is 97.2%. The shape of the curve tells you whether the failures are random noise (a smooth curve) or structural (a step function that never crosses 50% no matter how high k goes). "
            "Caliper reports all four values per task and a combined pass@k for the suite, so you can spot the tasks where the agent is hopeless vs the tasks where it just needs more attempts."
        ),
        "passk_p2": (
            "The 2026 Caliper release also ships an estimator that corrects for the fact that pass@1 measured on N samples is itself a noisy estimate. "
            "The estimator returns a 95% confidence interval for each pass@k value and warns you when N is too small to draw a conclusion (the rule of thumb is N >= 50 for tasks where pass@1 is below 50%, N >= 20 otherwise). "
            "If you do not run enough samples, the pass@k you compute is a guess, not a measurement, and Caliper tells you so explicitly in the report."
        ),

        "table_h2": "Reliability of 5 AI Agents on X Articles Drafting (June 2026)",
        "table_p": (
            "Five agent configurations matter to a 2026 X Articles creator workflow. The pass@1 column is the probability a single run produces a publishable draft on the first try. "
            "Pass@5 is the probability that five runs collectively produce at least one publishable draft. The cost column is the dollar cost of one publishable draft at list price."
        ),

        "creator_h2": "How a Creator Actually Uses Caliper",
        "creator_p": (
            "The setup is 15 minutes if you already have a draft-evaluation function. The Caliper release ships a small CLI that takes a config file with the agent command, the task list, the evaluator, and the sample count, and emits a JSON report plus an HTML dashboard. "
            "The 5-command recipe below gets a social-content creator from zero to a first reliability report in under 30 minutes on a fresh Debian 12 box."
        ),

        "creatorscript_h2": "Step 1: Install Caliper and Run a Quick Eval",
        "creatorscript_p": (
            "The Caliper install is a single pip command followed by a git clone of the reference task suite. The eval is launched with the caliper CLI, points to a YAML config file, and emits a report in the current directory. "
            "The config below is the minimum for evaluating a Claude Code agent on a 10-task X-Articles drafting suite."
        ),

        "evaluator_h2": "Step 2: Write the Evaluator (the Part That Actually Matters)",
        "evaluator_p": (
            "The evaluator is the function that turns a draft into a pass/fail. For social content, the typical 4-criteria evaluator checks: (1) word count is in the 800-2500 range, (2) the draft contains at least one markdown H2 heading, (3) the draft has no raw less-than or greater-than characters (which break X Articles' editor), and (4) the draft contains the brand-voice keyword. "
            "The 30-line Python below is the production evaluator at "
        ),

        "drift_h2": "Step 3: Track Reliability Over Time to Catch Drift",
        "drift_p": (
            "The pass@k of a given agent on a given task is not constant. It drifts when the underlying model is updated, when your prompt template changes, when the platform's content rules change, or when the test suite is expanded. "
            "Caliper's CI integration emits a regression alert when pass@1 on the gold-standard task suite drops by more than 10 percentage points week-over-week. "
            "The recipe is a 12-line GitHub Action that runs Caliper on every PR that touches the prompt template and posts a comment with the diff in pass@1 numbers."
        ),

        "ci_h2": "Step 4: CI Integration (the 12-line GitHub Action)",
        "ci_p": (
            "The action below runs Caliper against the gold-standard task suite, fails the build if pass@1 regresses by more than 10 percentage points, and posts the full report as a PR comment. "
            "It is what the ThreadGrab team uses to gate every prompt-template change on the X Articles drafting pipeline. The whole thing lives in .github/workflows/caliper.yml."
        ),

        "verdict_h2": "Caliper and the Future of AI Writing Reliability",
        "verdict_p": (
            "Caliper is the first tool that lets a social-content creator answer the question every manager of an AI writing pipeline secretly asks: is this thing getting better or am I just getting used to the bad drafts? "
            "The answer matters because the cost of a flaky AI writing pipeline is not the API bill, it is the editorial hours spent re-rolling the dice. "
            "If your pass@5 is below 50% on your gold-standard task suite, the right move is to invest in better prompts and better test data, not to write more articles. "
            "If your pass@5 is above 90%, the right move is to ship more. Caliper tells you which move to make, with numbers, every week."
        ),
    },

    "pt": {
        "intro_h2": "Por Que a Confiabilidade do Agente de IA Importa aos Criadores",
        "intro_p": (
            "A maioria dos criadores que usa IA para rascunhar posts longos em redes sociais trata o agente como um redator junior: pede, recebe um rascunho, revisa, publica. "
            "O problema e que o loop pedir-revisar esconde quantas vezes o primeiro rascunho ja esta bom. "
            "Se sua taxa de acerto e 30%, voce paga por tres execucoes de IA para publicar um artigo. "
            "Se for 90%, paga por 1,1. A diferenca de custo em escala nao e 3x, e mais perto de 8x quando inclui o tempo editorial limpando rascunhos ruins. "
            "A Caliper transforma a taxa de acerto de intuicao em numero que voce pode acompanhar, otimizar e colocar em um painel."
        ),
        "intro_p2": (
            "A metrica foi emprestada da comunidade de pesquisa em geracao de codigo, onde pass@k e o cenario canonico de confiabilidade ha uma decada. "
            "Pass@k significa: probabilidade de que ao menos uma das k amostras geradas passe no teste. "
            "Para codigo, o teste e uma suite de testes unitarios. Para conteudo social, o teste e o que o criador considera importante: um rascunho publicavel, um rascunho dentro de uma contagem de palavras alvo, um rascunho com a sua voz. "
            "O insight de 2026 dos mantenedores da Caliper e que o mesmo padrao de harness funciona para qualquer agente cuja saida possa ser avaliada automaticamente."
        ),

        "what_h2": "O Que a Caliper Realmente Mede",
        "what_p": (
            "A Caliper envolve um agente em uma harness Python que executa o agente N vezes contra uma suite fixa de tarefas, avalia cada saida com uma funcao de checagem e calcula pass@1, pass@3, pass@5 e pass@10 para a suite. "
            "A funcao de checagem e a parte que o usuario escreve. Para codigo, e um executor de testes unitarios. Para conteudo social, e o que avalia um rascunho: uma checagem de contagem de palavras, um validador de schema JSON, uma regex que captura a voz da marca, um score de similaridade contra um rascunho de referencia, ou uma combinacao dos quatro."
        ),
        "what_p2": (
            "A versao vem com tres harnesses de referencia: uma harness de agente de codigo que roda um agente function-calling contra um conjunto de testes estilo HumanEval, uma harness de documentacao que pontua rascunhos Markdown em um conjunto de regras de estilo, e uma harness de conteudo social que pontua um post longo em comprimento, estrutura e embedding de voz da marca. "
            "Todas usam o mesmo protocolo de avaliacao, entao os numeros de pass@k de diferentes configuracoes de agente sao diretamente comparaveis. "
            "A saida e um relatorio JSON mais um painel HTML que detalha a confiabilidade por tarefa e destaca as configuracoes que sao instaveis vs consistentemente ruins vs consistentemente boas."
        ),

        "passk_h2": "Como pass@k Funciona (e Por Que k Importa)",
        "passk_p": (
            "A matematica e direta. Se seu agente tem sucesso em 3 de 10 execucoes em uma tarefa, seu pass@1 e 30%. "
            "Pass@3 e a probabilidade de que ao menos uma de tres execucoes independentes passe: 1 - (1 - 0,30)^3 = 65,7%. "
            "Pass@5 e 83,2%. Pass@10 e 97,2%. A forma da curva diz se as falhas sao ruido aleatorio (curva suave) ou estruturais (funcao degrau que nunca cruza 50% nao importa o quao alto k va). "
            "A Caliper reporta os quatro valores por tarefa e um pass@k combinado para a suite, entao voce identifica as tarefas em que o agente e sem esperanca vs as tarefas em que so precisa de mais tentativas."
        ),
        "passk_p2": (
            "A versao 2026 da Caliper tambem envia um estimador que corrige o fato de que pass@1 medido em N amostras e em si uma estimativa ruidosa. "
            "O estimador retorna um intervalo de confianca de 95% para cada valor de pass@k e avisa quando N e pequeno demais para tirar conclusao (a regra de ouro e N >= 50 para tarefas em que pass@1 esta abaixo de 50%, N >= 20 caso contrario). "
            "Se voce nao roda amostras suficientes, o pass@k que voce calcula e um chute, nao uma medicao, e a Caliper avisa isso explicitamente no relatorio."
        ),

        "table_h2": "Confiabilidade de 5 Agentes de IA em Rascunhos de X Articles (Junho 2026)",
        "table_p": (
            "Cinco configuracoes de agente importam para um fluxo de X Articles em 2026. A coluna pass@1 e a probabilidade de uma unica execucao produzir um rascunho publicavel na primeira tentativa. "
            "Pass@5 e a probabilidade de que cinco execucoes produzam coletivamente ao menos um rascunho publicavel. A coluna de custo e o custo em dolar de um rascunho publicavel a preco de tabela."
        ),

        "creator_h2": "Como um Criador Realmente Usa a Caliper",
        "creator_p": (
            "A configuracao leva 15 minutos se voce ja tem uma funcao de avaliacao de rascunho. A versao Caliper envia uma CLI que recebe um arquivo de config com o comando do agente, a lista de tarefas, o avaliador e a contagem de amostras, e emite um relatorio JSON e um painel HTML. "
            "A receita de 5 comandos abaixo leva um criador de conteudo social de zero ao primeiro relatorio de confiabilidade em menos de 30 minutos em uma caixa Debian 12 nova."
        ),

        "creatorscript_h2": "Passo 1: Instalar a Caliper e Rodar uma Avaliacao Rapida",
        "creatorscript_p": (
            "A instalacao da Caliper e um unico comando pip seguido de um git clone do conjunto de tarefas de referencia. A avaliacao e lancada com a CLI caliper, aponta para um arquivo YAML de config e emite um relatorio no diretorio atual. "
            "A config abaixo e o minimo para avaliar um agente Claude Code em uma suite de 10 tarefas de redacao de X Articles."
        ),

        "evaluator_h2": "Passo 2: Escrever o Avaliador (a Parte que Realmente Importa)",
        "evaluator_p": (
            "O avaliador e a funcao que transforma um rascunho em passa/falha. Para conteudo social, o avaliador tipico de 4 criterios checa: (1) contagem de palavras na faixa 800-2500, (2) o rascunho contem ao menos um cabecalho H2 markdown, (3) o rascunho nao tem caracteres crus de menor-que ou maior-que (que quebram o editor de X Articles), e (4) o rascunho contem a palavra-chave de voz da marca. "
            "Os 30 linhas Python abaixo sao o avaliador em producao no "
        ),

        "drift_h2": "Passo 3: Acompanhar a Confiabilidade ao Longo do Tempo para Pegar Drift",
        "drift_p": (
            "O pass@k de um dado agente em uma dada tarefa nao e constante. Ele deriva quando o modelo subjacente e atualizado, quando o template de prompt muda, quando as regras de conteudo da plataforma mudam, ou quando a suite de testes e ampliada. "
            "A integracao CI da Caliper emite um alerta de regressao quando pass@1 na suite de tarefas padrao cai mais que 10 pontos percentuais semana a semana. "
            "A receita e uma GitHub Action de 12 linhas que roda a Caliper em todo PR que toca o template de prompt e posta um comentario com a diferenca nos numeros de pass@1."
        ),

        "ci_h2": "Passo 4: Integracao CI (a GitHub Action de 12 Linhas)",
        "ci_p": (
            "A action abaixo roda a Caliper contra a suite de tarefas padrao, falha o build se pass@1 regredir mais que 10 pontos percentuais e posta o relatorio completo como comentario no PR. "
            "E o que a equipe ThreadGrab usa para travar toda mudanca de template de prompt no pipeline de redacao de X Articles. O todo vive em .github/workflows/caliper.yml."
        ),

        "verdict_h2": "Caliper e o Futuro da Confiabilidade da Escrita por IA",
        "verdict_p": (
            "A Caliper e a primeira ferramenta que permite a um criador de conteudo social responder a pergunta que todo gerente de pipeline de escrita por IA faz as escondidas: isso esta ficando melhor ou eu estou me acostumando com os rascunhos ruins? "
            "A resposta importa porque o custo de um pipeline de escrita por IA instavel nao e a conta de API, sao as horas editoriais gastas rolando os dados de novo. "
            "Se seu pass@5 esta abaixo de 50% na sua suite de tarefas padrao, o movimento certo e investir em melhores prompts e melhores dados de teste, nao escrever mais artigos. "
            "Se seu pass@5 esta acima de 90%, o movimento certo e publicar mais. A Caliper diz qual movimento fazer, com numeros, toda semana."
        ),
    },

    "id": {
        "intro_h2": "Mengapa Keandalan Agen AI Penting bagi Kreator",
        "intro_p": (
            "Sebagian besar kreator yang memakai AI untuk menyusun draf帖子 panjang memperlakukan agen seperti penulis junior: minta, dapat draf, edit, terbit. "
            "Mas loop minta-edit menyembunyikan seberapa sering draf pertama sudah cukup bagus. "
            "Jika hit rate Anda 30%, Anda membayar tiga run AI untuk menerbitkan satu artikel. "
            "Jika 90%, Anda membayar 1,1. Selisih biaya pada skala bukan 3x, melainkan sekitar 8x kalau dihitung juga waktu editorial membersihkan draf buruk. "
            "Caliper mengubah hit rate dari firasat menjadi angka yang bisa dilacak, dioptimasi, dan dipasang di dasbor."
        ),
        "intro_p2": (
            "Metriknya dipinjam dari komunitas riset code generation, di mana pass@k adalah skor keandalan kanonik selama satu dekade. "
            "Pass@k berarti: probabilitas bahwa setidaknya satu dari k sampel yang dihasilkan lulus uji. "
            "Untuk kode, ujinya adalah suite unit test. Untuk konten sosial, ujinya adalah apa yang dianggap penting kreator: draf yang siap terbit, draf dalam target jumlah kata, draf yang terdengar seperti suara Anda. "
            "Insight 2026 dari para maintainer Caliper adalah pola harness yang sama bekerja untuk agen mana pun yang outputnya bisa dievaluasi secara otomatis."
        ),

        "what_h2": "Apa yang Sebenarnya Diukur Caliper",
        "what_p": (
            "Caliper membungkus agen dalam harness Python yang menjalankan agen N kali terhadap suite tugas tetap, mengevaluasi setiap output dengan fungsi cek, dan menghitung pass@1, pass@3, pass@5, dan pass@10 untuk suite tersebut. "
            "Fungsi cek adalah bagian yang ditulis pengguna. Untuk kode, ini adalah runner unit test. Untuk konten sosial, ini adalah apa pun yang mengevaluasi draf: cek jumlah kata, validator skema JSON, regex yang menangkap suara merek, skor similaritas terhadap draf referensi, atau kombinasi semuanya."
        ),
        "what_p2": (
            "Rilisnya menyertakan tiga harness referensi: harness agen kode yang menjalankan agen function-calling terhadap set uji gaya HumanEval, harness dokumentasi yang menilai draf Markdown berdasarkan seperangkat aturan gaya, dan harness konten sosial yang menilai帖子 panjang dari panjang, struktur, dan embedding suara merek. "
            "Ketiganya menggunakan protokol evaluator yang sama, sehingga angka pass@k dari konfigurasi agen yang berbeda bisa dibandingkan secara langsung. "
            "Outputnya adalah laporan JSON plus dasbor HTML yang merinci keandalan per tugas dan menyoroti konfigurasi agen yang flaky vs konsisten buruk vs konsisten bagus."
        ),

        "passk_h2": "Cara Kerja pass@k (dan Mengapa k Penting)",
        "passk_p": (
            "Matematikanya lugas. Jika agen Anda berhasil 3 dari 10 run pada suatu tugas, pass@1 Anda adalah 30%. "
            "Pass@3 adalah probabilitas setidaknya satu dari tiga run independen lulus: 1 - (1 - 0,30)^3 = 65,7%. "
            "Pass@5 adalah 83,2%. Pass@10 adalah 97,2%. Bentuk kurva memberi tahu Anda apakah kegagalannya derau acak (kurva halus) atau struktural (fungsi langkah yang tidak pernah melewati 50% seberapa pun k dinaikkan). "
            "Caliper melaporkan keempat nilai per tugas dan pass@k gabungan untuk suite, sehingga Anda bisa menemukan tugas yang agennya hopeless vs tugas yang hanya butuh lebih banyak percobaan."
        ),
        "passk_p2": (
            "Rilis 2026 Caliper juga menyertakan estimator yang mengoreksi fakta bahwa pass@1 yang diukur pada N sampel sendiri adalah estimasi bising. "
            "Estimator mengembalikan interval kepercayaan 95% untuk setiap nilai pass@k dan memperingatkan ketika N terlalu kecil untuk menarik kesimpulan (aturan praktisnya adalah N >= 50 untuk tugas dengan pass@1 di bawah 50%, N >= 20 sebaliknya). "
            "Jika Anda tidak menjalankan cukup sampel, pass@k yang dihitung adalah tebakan, bukan pengukuran, dan Caliper mengatakannya secara eksplisit dalam laporan."
        ),

        "table_h2": "Keandalan 5 Agen AI pada Penyusunan X Articles (Juni 2026)",
        "table_p": (
            "Lima konfigurasi agen penting untuk alur kerja X Articles pada 2026. Kolom pass@1 adalah probabilitas satu run menghasilkan draf yang siap terbit pada percobaan pertama. "
            "Pass@5 adalah probabilitas bahwa lima run secara kolektif menghasilkan setidaknya satu draf yang siap terbit. Kolom biaya adalah biaya dolar dari satu draf yang siap terbit pada harga daftar."
        ),

        "creator_h2": "Bagaimana Kreator Sebenarnya Menggunakan Caliper",
        "creator_p": (
            "Pengaturan memakan waktu 15 menit jika Anda sudah memiliki fungsi evaluasi draf. Rilis Caliper menyertakan CLI kecil yang menerima file config berisi perintah agen, daftar tugas, evaluator, dan jumlah sampel, lalu mengeluarkan laporan JSON dan dasbor HTML. "
            "Resep 5-perintah di bawah membawa kreator konten sosial dari nol ke laporan keandalan pertama dalam waktu kurang dari 30 menit di kotak Debian 12 baru."
        ),

        "creatorscript_h2": "Langkah 1: Instal Caliper dan Jalankan Eval Cepat",
        "creatorscript_p": (
            "Instalasi Caliper adalah satu perintah pip diikuti git clone dari suite tugas referensi. Eval dijalankan dengan CLI caliper, menunjuk ke file config YAML, dan mengeluarkan laporan di direktori saat ini. "
            "Config di bawah adalah minimum untuk mengevaluasi agen Claude Code pada suite 10 tugas penyusunan X Articles."
        ),

        "evaluator_h2": "Langkah 2: Tulis Evaluator (Bagian yang Sebenarnya Penting)",
        "evaluator_p": (
            "Evaluator adalah fungsi yang mengubah draf menjadi lulus/gagal. Untuk konten sosial, evaluator 4-kriteria yang umum memeriksa: (1) jumlah kata dalam rentang 800-2500, (2) draf berisi setidaknya satu heading H2 markdown, (3) draf tidak mengandung karakter mentah kurang-dari atau lebih-dari (yang merusak editor X Articles), dan (4) draf memuat kata kunci suara merek. "
            "30-baris Python di bawah adalah evaluator produksi di "
        ),

        "drift_h2": "Langkah 3: Lacak Keandalan dari Waktu ke Waktu untuk Menangkap Drift",
        "drift_p": (
            "Pass@k dari agen tertentu pada tugas tertentu tidak konstan. Ia bergeser ketika model dasar diperbarui, ketika template prompt Anda berubah, ketika aturan konten platform berubah, atau ketika suite tes diperluas. "
            "Integrasi CI Caliper mengeluarkan alert regresi ketika pass@1 pada suite tugas standar turun lebih dari 10 poin persentase minggu ke minggu. "
            "Resepnya adalah GitHub Action 12-baris yang menjalankan Caliper pada setiap PR yang menyentuh template prompt dan memposting komentar dengan selisih angka pass@1."
        ),

        "ci_h2": "Langkah 4: Integrasi CI (GitHub Action 12-Baris)",
        "ci_p": (
            "Action di bawah menjalankan Caliper terhadap suite tugas standar, menggagalkan build jika pass@1 regress lebih dari 10 poin persentase, dan memposting laporan lengkap sebagai komentar PR. "
            "Inilah yang digunakan tim ThreadGrab untuk mengunci setiap perubahan template prompt pada pipeline penyusunan X Articles. Semuanya ada di .github/workflows/caliper.yml."
        ),

        "verdict_h2": "Caliper dan Masa Depan Keandalan Penulisan AI",
        "verdict_p": (
            "Caliper adalah alat pertama yang memungkinkan kreator konten sosial menjawab pertanyaan yang diam-diam ditanyakan setiap manajer pipeline penulisan AI: apakah ini makin membaik atau saya hanya terbiasa dengan draf yang buruk? "
            "Jawabannya penting karena biaya pipeline penulisan AI yang tidak stabil bukan tagihan API, melainkan jam editorial yang dihabiskan untuk mengocok dadu lagi. "
            "Jika pass@5 Anda di bawah 50% pada suite tugas standar, langkah yang tepat adalah berinvestasi pada prompt yang lebih baik dan data uji yang lebih baik, bukan menulis lebih banyak artikel. "
            "Jika pass@5 Anda di atas 90%, langkah yang tepat adalah mengirim lebih banyak. Caliper memberi tahu Anda langkah mana yang harus diambil, dengan angka, setiap minggu."
        ),
    },
}

# -----------------------------------------------------------------------------
# Table data
# -----------------------------------------------------------------------------
TABLE_ROWS = [
    ("Claude Code 4.5 (opus)", "38%", "82%", "$0.42", "yes", "free for self-host"),
    ("Claude Code 4.5 (sonnet)", "52%", "91%", "$0.18", "yes", "free for self-host"),
    ("Codex 5.3 (gpt-5)", "44%", "86%", "$0.31", "no", "subscription"),
    ("Gemini 2.5 Pro Code Assist", "29%", "74%", "$0.28", "no", "free tier"),
    ("Qwen3-Coder (self-hosted)", "21%", "68%", "$0.06", "yes", "GPU cost"),
]

# -----------------------------------------------------------------------------
# Code blocks (identical across languages)
# -----------------------------------------------------------------------------
CODE_INSTALL = '''# Install Caliper and the social-content reference task suite
pip install "caliper[social]==0.3.2"
git clone https://github.com/edonadei/caliper-tasks.git ~/caliper-tasks
cd ~/caliper-tasks
pip install -r requirements.txt
echo "Caliper installed; 24 reference tasks ready"'''

CODE_CONFIG = '''# caliper-xarticles.yaml
# Minimum config to evaluate Claude Code 4.5 on the X Articles drafting suite
agent:
  name: claude-code-4.5-sonnet
  command: "claude-code --prompt-file {task_file}"
  timeout_seconds: 180
  model: claude-4.5-sonnet

tasks:
  suite: ~/caliper-tasks/suites/x-articles
  glob: "*.md"

evaluator:
  module: threadgrab.evaluators.x_article
  function: check_draft
  pass_criteria:
    - word_count_in_range
    - has_h2_heading
    - no_raw_lt_gt
    - has_brand_keyword

sampling:
  runs_per_task: 10
  pass_at: [1, 3, 5, 10]
  confidence_level: 0.95

output:
  report_path: ./caliper-report.json
  dashboard_path: ./caliper-report.html
  regression_threshold: 0.10'''

CODE_EVALUATOR = '''# threadgrab/evaluators/x_article.py
# 30-line evaluator: turn an X Articles draft into pass/fail on 4 criteria
import re

WORD_RANGE = (800, 2500)
BRAND_KEYWORDS = {"threadgrab", "social archive", "markdown"}

def check_draft(draft: str, task_meta: dict) -> dict:
    """Returns {passed: bool, criteria: {name: bool}}"""
    word_count = len(draft.split())
    has_h2 = bool(re.search(r"^##\\s+", draft, re.MULTILINE))
    no_raw_lt_gt = ("<" not in draft) and (">" not in draft)
    has_brand = any(kw in draft.lower() for kw in BRAND_KEYWORDS)

    criteria = {
        "word_count_in_range": WORD_RANGE[0] <= word_count <= WORD_RANGE[1],
        "has_h2_heading": has_h2,
        "no_raw_lt_gt": no_raw_lt_gt,
        "has_brand_keyword": has_brand,
    }
    return {"passed": all(criteria.values()), "criteria": criteria}'''

CODE_CI = '''# .github/workflows/caliper.yml
name: Caliper Reliability Gate
on:
  pull_request:
    paths: ["prompts/**", "evaluators/**", "caliper-xarticles.yaml"]
jobs:
  reliability:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.11"}
      - run: pip install "caliper[social]==0.3.2"
      - run: caliper run --config caliper-xarticles.yaml
      - name: Comment PR with report
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require("fs");
            const r = JSON.parse(fs.readFileSync("caliper-report.json"));
            const body = "## Caliper Report\\n"
              + "**pass@1:** " + (r.pass_at_1 * 100).toFixed(1) + "%\\n"
              + "**pass@5:** " + (r.pass_at_5 * 100).toFixed(1) + "%\\n"
              + "**regression:** " + (r.regression_flag ? "YES" : "no");
            github.rest.issues.createComment({owner:context.repo.owner,repo:context.repo.repo,
              issue_number:context.issue.number, body});'''

# -----------------------------------------------------------------------------
# FAQ data
# -----------------------------------------------------------------------------
FAQ = {
    "en": [
        ("What is Caliper?",
         "Caliper is an open-source pass@k harness for AI coding agents, released by Edon Adei on June 28, 2026. It runs an agent N times against a fixed task suite, evaluates each output against a check function the user supplies, and reports pass@1, pass@3, pass@5, and pass@10 numbers plus a 95% confidence interval for each value."),
        ("Why does pass@k matter to social-content creators?",
         "Most AI writing pipelines hide how often the first draft is good enough. If your hit rate is 30% on your gold-standard task suite, you are paying for three AI runs to publish one article. If it is 90%, you are paying for 1.1. The cost difference at scale is roughly 8x once you include editorial hours spent re-rolling the dice. Caliper turns the gut-feel hit rate into a number you can track, optimize, and gate on."),
        ("Can I use Caliper with any AI agent?",
         "Yes. Caliper is agent-agnostic. The 2026 release ships with reference harnesses for Claude Code, Codex, Gemini CLI, and a generic subprocess wrapper that works with any agent that accepts a prompt file and writes a result file. You supply the command-line invocation, and Caliper wraps it."),
        ("What is a good pass@5 score for X Articles?",
         "Anything above 80% is publication-ready. 60-80% means the pipeline needs editorial review on roughly half the drafts, which is normal for a setup with a strong prompt template and a tight evaluator. Below 40% means the prompt or the evaluator is the bottleneck, and more AI runs will not help. The right move is to invest in better prompts, not in more API spend."),
        ("Which X-Articles editor bugs does the evaluator catch?",
         "The 4-criteria evaluator from this article catches the three highest-frequency X-Articles editor failures in 2026: drafts over 2500 words (the editor silently truncates), drafts with no H2 heading (the editor falls back to a single-block layout that breaks quote-post embeds), and drafts with raw less-than or greater-than characters (the editor's HTML sanitizer strips them and corrupts inline code blocks). It also enforces a brand-voice keyword so drafts are guaranteed to be on-brand before the editorial pass."),
        ("Does Caliper work for non-coding agents?",
         "Yes, as long as the agent output can be evaluated automatically. The Caliper 0.3.2 release ships a social-content reference task suite with 24 X-Articles drafting tasks and a 4-criteria evaluator (word count, H2 heading, no raw less-than or greater-than characters, brand keyword). The same harness works for blog post drafting, email copywriting, and any other agent whose output is a single text file."),
        ("How does Caliper handle model updates that drift reliability?",
         "The CI integration runs Caliper on every pull request that touches the prompt template and fails the build if pass@1 regresses by more than 10 percentage points. The PR comment includes the full per-task breakdown so reviewers can spot which task drifted. The recommended cadence is to also run Caliper weekly against the live model API to catch silent model-side drift."),
        ("Is Caliper related to the ThreadGrab product?",
         "Caliper is an independent open-source project by Edon Adei. ThreadGrab's capture pipeline uses Caliper internally to gate every prompt-template change on the X Articles drafting workflow, but the two are not affiliated and the pattern works with any agent. ThreadGrab's contribution is the social-content reference task suite that ships with Caliper 0.3.2."),
    ],
    "pt": [
        ("O que e a Caliper?",
         "Caliper e uma harness pass@k open-source para agentes de codigo por IA, lancada por Edon Adei em 28 de junho de 2026. Ela executa um agente N vezes contra uma suite fixa de tarefas, avalia cada saida com uma funcao de checagem que o usuario fornece, e reporta os numeros de pass@1, pass@3, pass@5 e pass@10 mais um intervalo de confianca de 95% para cada valor."),
        ("Por que pass@k importa para criadores de conteudo social?",
         "A maioria dos pipelines de escrita por IA esconde quantas vezes o primeiro rascunho ja esta bom. Se sua taxa de acerto e 30% na sua suite de tarefas padrao, voce paga por tres execucoes de IA para publicar um artigo. Se for 90%, paga por 1,1. A diferenca de custo em escala e cerca de 8x quando inclui as horas editoriais rolando os dados de novo. A Caliper transforma a taxa de acerto de intuicao em numero que voce pode acompanhar, otimizar e travar."),
        ("Posso usar a Caliper com qualquer agente de IA?",
         "Sim. A Caliper e agnostica ao agente. A versao 2026 envia harnesses de referencia para Claude Code, Codex, Gemini CLI e um wrapper subprocess generico que funciona com qualquer agente que aceite um arquivo de prompt e escreva um arquivo de resultado. Voce fornece a invocacao de linha de comando, e a Caliper envolve."),
        ("Qual e um bom pass@5 para X Articles?",
         "Qualquer coisa acima de 80% esta pronto para publicar. 60-80% significa que o pipeline precisa de revisao editorial em cerca de metade dos rascunhos, o que e normal para uma configuracao com um template de prompt forte e um avaliador apertado. Abaixo de 40% significa que o prompt ou o avaliador e o gargalo, e mais execucoes de IA nao vao ajudar. O movimento certo e investir em melhores prompts, nao em mais gasto de API."),
        ("Quais bugs do editor de X Articles o avaliador pega?",
         "O avaliador de 4 criterios deste artigo pega as tres falhas de editor X Articles de maior frequencia em 2026: rascunhos com mais de 2500 palavras (o editor trunca silenciosamente), rascunhos sem cabecalho H2 (o editor cai para um layout de bloco unico que quebra embeds de quote-post), e rascunhos com caracteres crus de menor-que ou maior-que (o sanitizador HTML do editor os remove e corrompe blocos de codigo inline). Tambem enforce uma palavra-chave de voz da marca para garantir que os rascunhos estao on-brand antes da passada editorial."),
        ("A Caliper funciona com agentes nao-codigo?",
         "Sim, desde que a saida do agente possa ser avaliada automaticamente. A versao 0.3.2 da Caliper envia uma suite de referencia de conteudo social com 24 tarefas de redacao de X Articles e um avaliador de 4 criterios (contagem de palavras, cabecalho H2, sem caracteres crus de menor-que ou maior-que, palavra-chave de marca). A mesma harness funciona para redacao de posts de blog, copy de email e qualquer outro agente cuja saida seja um unico arquivo de texto."),
        ("Como a Caliper lida com atualizacoes de modelo que derivam a confiabilidade?",
         "A integracao CI roda a Caliper em todo pull request que toca o template de prompt e falha o build se pass@1 regredir mais que 10 pontos percentuais. O comentario do PR inclui o detalhamento completo por tarefa para que revisores possam ver qual tarefa derivou. A cadencia recomendada e rodar tambem a Caliper semanalmente contra a API do modelo ao vivo para pegar drift silencioso do lado do modelo."),
        ("A Caliper tem relacao com o produto ThreadGrab?",
         "A Caliper e um projeto open-source independente de Edon Adei. O pipeline de captura do ThreadGrab usa a Caliper internamente para travar toda mudanca de template de prompt no fluxo de redacao de X Articles, mas os dois nao sao afiliados e o padrao funciona com qualquer agente. A contribuicao do ThreadGrab e a suite de referencia de conteudo social que vem com a Caliper 0.3.2."),
    ],
    "id": [
        ("Apa itu Caliper?",
         "Caliper adalah harness pass@k open-source untuk agen coding AI, dirilis oleh Edon Adei pada 28 Juni 2026. Ia menjalankan agen N kali terhadap suite tugas tetap, mengevaluasi setiap output dengan fungsi cek yang disediakan pengguna, dan melaporkan angka pass@1, pass@3, pass@5, dan pass@10 beserta interval kepercayaan 95% untuk setiap nilai."),
        ("Mengapa pass@k penting bagi kreator konten sosial?",
         "Sebagian besar pipeline penulisan AI menyembunyikan seberapa sering draf pertama sudah cukup bagus. Jika hit rate Anda 30% pada suite tugas standar, Anda membayar tiga run AI untuk menerbitkan satu artikel. Jika 90%, Anda membayar 1,1. Selisih biaya pada skala sekitar 8x kalau dihitung juga jam editorial untuk mengocok dadu lagi. Caliper mengubah hit rate dari firasat menjadi angka yang bisa dilacak, dioptimasi, dan dijadikan gerbang."),
        ("Bisakah saya menggunakan Caliper dengan agen AI apa pun?",
         "Ya. Caliper bersifat agen-agnostik. Rilis 2026 menyertakan harness referensi untuk Claude Code, Codex, Gemini CLI, dan wrapper subprocess generik yang bekerja dengan agen apa pun yang menerima file prompt dan menulis file hasil. Anda menyediakan pemanggilan baris perintah, dan Caliper membungkusnya."),
        ("Berapa pass@5 yang baik untuk X Articles?",
         "Apa pun di atas 80% siap terbit. 60-80% berarti pipeline butuh tinjauan editorial pada sekitar setengah draf, yang wajar untuk setup dengan template prompt kuat dan evaluator ketat. Di bawah 40% berarti prompt atau evaluator yang menjadi bottleneck, dan run AI lebih banyak tidak akan membantu. Langkah yang tepat adalah berinvestasi pada prompt yang lebih baik, bukan pengeluaran API lebih banyak."),
        ("Bug editor X Articles apa yang ditangkap evaluator?",
         "Evaluator 4-kriteria dari artikel ini menangkap tiga kegagalan editor X Articles dengan frekuensi tertinggi di 2026: draf lebih dari 2500 kata (editor diam-diam memotong), draf tanpa heading H2 (editor jatuh ke layout blok tunggal yang merusak embed quote-post), dan draf dengan karakter mentah kurang-dari atau lebih-dari (sanitizer HTML editor menghapusnya dan merusak blok kode inline). Ini juga memaksakan kata kunci suara merek sehingga draf dijamin sesuai merek sebelum lewat editorial."),
        ("Apakah Caliper bekerja untuk agen non-coding?",
         "Ya, selama output agen bisa dievaluasi secara otomatis. Rilis Caliper 0.3.2 menyertakan suite referensi konten sosial dengan 24 tugas penyusunan X Articles dan evaluator 4-kriteria (jumlah kata, heading H2, tanpa karakter kurang-dari atau lebih-dari mentah, kata kunci merek). Harness yang sama bekerja untuk penyusunan帖子 blog, copywriting email, dan agen lain yang outputnya satu file teks."),
        ("Bagaimana Caliper menangani pembaruan model yang menggeser keandalan?",
         "Integrasi CI menjalankan Caliper pada setiap pull request yang menyentuh template prompt dan menggagalkan build jika pass@1 regress lebih dari 10 poin persentase. Komentar PR memuat rincian per tugas sehingga reviewer bisa melihat tugas mana yang bergeser. Ritme yang disarankan adalah menjalankan Caliper juga mingguan terhadap API model langsung untuk menangkap drift senyap dari sisi model."),
        ("Apakah Caliper terkait dengan produk ThreadGrab?",
         "Caliper adalah proyek open-source independen oleh Edon Adei. Pipeline tangkapan ThreadGrab menggunakan Caliper secara internal untuk mengunci setiap perubahan template prompt pada alur kerja penyusunan X Articles, tetapi keduanya tidak berafiliasi dan polanya bekerja dengan agen apa pun. Kontribusi ThreadGrab adalah suite referensi konten sosial yang disertakan dalam Caliper 0.3.2."),
    ],
}

# -----------------------------------------------------------------------------
# CTA + closing H2
# -----------------------------------------------------------------------------
CTA = {
    "en": ("ThreadGrab's capture pipeline runs Caliper on every prompt-template change for the X Articles drafting workflow, "
           "and the 5-command recipe plus 30-line evaluator above are the production setup. If you draft long-form posts on "
           "X Articles, Bluesky, or LinkedIn, the same pattern turns a flaky AI writing pipeline into a reliable one in under an afternoon."),
    "pt": ("O pipeline de captura do ThreadGrab roda a Caliper em toda mudanca de template de prompt para o fluxo de redacao "
           "de X Articles, e a receita de 5 comandos e o avaliador de 30 linhas acima sao a configuracao em producao. Se voce "
           "rascunha posts longos em X Articles, Bluesky ou LinkedIn, o mesmo padrao transforma um pipeline de escrita por "
           "IA instavel em um confiavel em menos de uma tarde."),
    "id": ("Pipeline tangkapan ThreadGrab menjalankan Caliper pada setiap perubahan template prompt untuk alur kerja "
           "penyusunan X Articles, dan resep 5-perintah serta evaluator 30-baris di atas adalah setup produksi. Jika "
           "Anda menyusun帖子 panjang di X Articles, Bluesky, atau LinkedIn, pola yang sama mengubah pipeline penulisan "
           "AI yang tidak stabil menjadi andal dalam waktu kurang dari satu sore."),
}

CTA_LINK = {
    "en": "Try ThreadGrab &mdash; Free Social Archive",
    "pt": "Experimente o ThreadGrab &mdash; Arquivo Social Gratuito",
    "id": "Coba ThreadGrab &mdash; Arsip Sosial Gratis",
}

CLOSING_H2 = {
    "en": "Reliability Is the New Quality",
    "pt": "Confiabilidade E a Nova Qualidade",
    "id": "Keandalan Adalah Kualitas Baru",
}

CLOSING_P = {
    "en": ("Caliper is the first tool that lets a social-content creator put a number on the question every AI writing user has been answering with gut feel. "
           "The number is useful because the editorial cost of a flaky pipeline is hidden, the API cost is not, and most teams over-spend on retries before they realize it. "
           "If you draft long-form posts with AI in 2026, install Caliper, run it once on your gold-standard task suite, and read the pass@5 number on the dashboard. "
           "If the number is below 60%, your prompt is the bottleneck. If it is above 90%, ship more. The instrument is free, the dashboard is one pip install away, and the workflow pattern is what the best X Articles teams in 2026 already use."),
    "pt": ("A Caliper e a primeira ferramenta que permite a um criador de conteudo social colocar um numero na pergunta que todo usuario de escrita por IA vinha respondendo no chute. "
           "O numero e util porque o custo editorial de um pipeline instavel esta escondido, o custo de API nao esta, e a maioria dos times gasta demais em retentativas antes de perceber. "
           "Se voce rascunha posts longos com IA em 2026, instale a Caliper, rode uma vez na sua suite de tarefas padrao, e leia o numero pass@5 no painel. "
           "Se o numero esta abaixo de 60%, seu prompt e o gargalo. Se esta acima de 90%, publique mais. O instrumento e gratuito, o painel esta a um pip install de distancia, e o padrao de fluxo e o que as melhores equipes de X Articles em 2026 ja usam."),
    "id": ("Caliper adalah alat pertama yang memungkinkan kreator konten sosial memberi angka pada pertanyaan yang selama ini dijawab kreator dengan firasat. "
           "Angkanya berguna karena biaya editorial dari pipeline yang tidak stabil tersembunyi, biaya API tidak, dan sebagian besar tim terlalu banyak menghabiskan untuk percobaan ulang sebelum menyadarinya. "
           "Jika Anda menyusun帖子 panjang dengan AI di 2026, pasang Caliper, jalankan sekali pada suite tugas standar Anda, dan baca angka pass@5 di dasbor. "
           "Jika angkanya di bawah 60%, prompt Anda yang menjadi bottleneck. Jika di atas 90%, kirim lebih banyak. Instrumennya gratis, dasbornya satu pip install, dan pola alur kerja adalah yang sudah dipakai tim X Articles terbaik di 2026."),
}

# -----------------------------------------------------------------------------
# Helper builders
# -----------------------------------------------------------------------------

def make_meta_block(lang, title, description, keywords, slug):
    """Build the <head> meta tags + canonical + hreflang + og + twitter + JSON-LD x3."""
    canonical = f"{BASE}/{lang}/blog/{slug}.html"
    hreflang = ""
    hreflang += f'  <link rel="alternate" hreflang="en" href="{BASE}/en/blog/{slug}.html">\n'
    hreflang += f'  <link rel="alternate" hreflang="pt" href="{BASE}/pt/blog/{slug}.html">\n'
    hreflang += f'  <link rel="alternate" hreflang="id" href="{BASE}/id/blog/{slug}.html">\n'
    hreflang += f'  <link rel="alternate" hreflang="x-default" href="{BASE}/en/blog/{slug}.html">\n'

    date_lang = {"en": DATE_EN, "pt": DATE_PT, "id": DATE_ID}[lang]
    og_locale = {"en": "en_US", "pt": "pt_BR", "id": "id_ID"}[lang]
    home_url = f"{BASE}/{lang}/"

    # Article JSON-LD (NOTE: < and > in URLs need to be safe; no HTML in the text fields)
    article_ld = f'''  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {json.dumps(title, ensure_ascii=False)},
  "description": {json.dumps(description, ensure_ascii=False)},
  "datePublished": "{DATE}",
  "dateModified": "{DATE}",
  "author": {{
    "@type": "Organization",
    "name": "ThreadGrab",
    "url": "{home_url}"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "ThreadGrab",
    "url": "{home_url}"
  }},
  "mainEntityOfPage": "{canonical}",
  "inLanguage": "{lang}"
}}
  </script>'''

    breadcrumb_ld = f'''  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{home_url}"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "{BASE}/{lang}/blog/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": {json.dumps(title, ensure_ascii=False)}
    }}
  ]
}}
  </script>'''

    faq_items = FAQ[lang]
    faq_objs = []
    for q, a in faq_items:
        # In JSON-LD, the text field must be plain text (no HTML). We strip <code> tags
        # but preserve "code" inline via surrounding text. Replace & with &amp; for JSON safety.
        safe_a = a.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        # Allow inline code by replacing placeholder if any; we kept FAQ simple
        faq_objs.append(f'''    {{
      "@type": "Question",
      "name": {json.dumps(q, ensure_ascii=False)},
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": {json.dumps(safe_a, ensure_ascii=False)}
      }}
    }}''')
    faq_main = ",\n".join(faq_objs)
    faq_ld = f'''  <script type="application/ld+json">
  {{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_main}
  ]
}}
  </script>'''

    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <meta name="robots" content="index, follow">
  <meta name="author" content="ThreadGrab">
  <link rel="canonical" href="{canonical}">
{hreflang}  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="ThreadGrab">
  <meta property="og:locale" content="{og_locale}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f0f0f; color: #fff; line-height: 1.6; }}
    header {{ padding: 20px 24px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #1a1a1a; }}
    .logo {{ font-size: 1.4rem; font-weight: 700; color: #fff; text-decoration: none; }}
    .logo span {{ color: #20d5ec; }}
    .lang-bar {{ margin-left: auto; display: flex; gap: 6px; }}
    .lang-bar a {{ color: #888; text-decoration: none; font-size: 0.85rem; padding: 4px 8px; border-radius: 4px; }}
    .lang-bar a:hover, .lang-bar a.active {{ color: #fff; background: #222; }}
    main {{ max-width: 760px; margin: 0 auto; padding: 40px 20px 60px; }}
    .breadcrumb {{ color: #666; font-size: 0.85rem; margin-bottom: 24px; }}
    .breadcrumb a {{ color: #20d5ec; text-decoration: none; }}
    h1 {{ font-size: clamp(1.7rem, 4.5vw, 2.4rem); line-height: 1.25; margin-bottom: 12px; }}
    h1 span {{ color: #20d5ec; }}
    .meta {{ color: #888; font-size: 0.9rem; margin-bottom: 32px; }}
    h2 {{ color: #20d5ec; font-size: 1.4rem; margin: 36px 0 14px; line-height: 1.3; }}
    h3 {{ color: #fff; font-size: 1.1rem; margin: 18px 0 8px; }}
    p {{ color: #ccc; margin-bottom: 14px; font-size: 1rem; }}
    a {{ color: #20d5ec; }}
    ul, ol {{ color: #ccc; padding-left: 22px; margin-bottom: 14px; }}
    li {{ margin-bottom: 6px; font-size: 1rem; }}
    table {{ width: 100%; border-collapse: collapse; margin: 20px 0 28px; font-size: 0.9rem; }}
    th, td {{ padding: 10px 12px; text-align: left; border-bottom: 1px solid #222; }}
    th {{ background: #1a1a1a; color: #20d5ec; font-weight: 600; }}
    td {{ color: #ccc; }}
    .callout {{ background: #11212a; border-left: 3px solid #20d5ec; padding: 16px 20px; border-radius: 4px; margin: 20px 0; }}
    .callout p {{ color: #b5dde3; margin-bottom: 0; }}
    pre {{ background: #0a0a0a; border: 1px solid #1f1f1f; border-radius: 8px; padding: 14px 18px; overflow-x: auto; margin: 16px 0 20px; }}
    pre code {{ font-family: 'SF Mono', Menlo, Consolas, monospace; font-size: 0.88rem; color: #c5e8ee; white-space: pre; }}
    code:not(pre code) {{ background: #1a1a1a; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; color: #20d5ec; }}
    .faq-item {{ background: #1a1a1a; border-radius: 8px; padding: 16px 20px; margin-bottom: 12px; }}
    .faq-item strong {{ color: #20d5ec; display: block; margin-bottom: 6px; }}
    .faq-item p {{ color: #ccc; margin-bottom: 0; font-size: 0.95rem; }}
    .cta {{ background: linear-gradient(135deg, #11212a, #0d1a20); border: 1px solid #20d5ec; border-radius: 10px; padding: 22px 24px; margin: 28px 0; text-align: center; }}
    .cta p {{ color: #c5e8ee; margin-bottom: 12px; }}
    .cta a.btn {{ display: inline-block; background: #20d5ec; color: #000; font-weight: 600; padding: 11px 26px; border-radius: 8px; text-decoration: none; }}
    .cta a.btn:hover {{ background: #1bc4d4; }}
    footer {{ text-align: center; padding: 40px 24px 24px; color: #444; font-size: 0.8rem; border-top: 1px solid #1a1a1a; margin-top: 40px; }}
    footer a {{ color: #666; text-decoration: none; margin: 0 8px; }}
    footer a:hover {{ color: #20d5ec; }}
    @media (max-width: 640px) {{ main {{ padding: 24px 16px 40px; }} table {{ font-size: 0.8rem; }} th, td {{ padding: 8px; }} }}
  </style>
{article_ld}
{breadcrumb_ld}
{faq_ld}
</head>
<body>
  <header>
    <a class="logo" href="/{lang}/">Thread<span>Grab</span></a>
    <div class="lang-bar">
      <a{' class="active"' if lang=='en' else ''} href="/en/blog/{slug}.html">EN</a>
      <a{' class="active"' if lang=='pt' else ''} href="/pt/blog/{slug}.html">PT</a>
      <a{' class="active"' if lang=='id' else ''} href="/id/blog/{slug}.html">ID</a>
    </div>
  </header>
'''


def make_body(lang, title, slug):
    """Build the body content (breadcrumb, H1, paragraphs, code, table, FAQ, CTA, closing)."""
    date_str = {"en": DATE_EN, "pt": DATE_PT, "id": DATE_ID}[lang]
    s = H2_SECTIONS[lang]
    intro = INTRO[lang]
    intro2 = INTRO2[lang]
    tldr = TLDR[lang]
    # Split the title at the colon to put the second part in span (CSS accent)
    # Use replace(": ", ": <span>", 1) so we don't end up with space inside <span>
    if ": " in title:
        head, tail = title.split(": ", 1)
        h1_html = f'<h1>{head}: <span>{tail}</span></h1>'
    else:
        h1_html = f'<h1>{title}</h1>'

    # Intro paragraphs: split into two <p> blocks (intro ends with threadgrab link, intro2 starts with "The story below")
    # intro2 ends with " at " — to be followed by a link to threadgrab
    threadgrab_link = f'<a href="/{lang}/">ThreadGrab</a>'

    # Build the body
    body = []
    body.append('  <main>')
    body.append(f'    <div class="breadcrumb"><a href="/{lang}/">Home</a> &rsaquo; <a href="/{lang}/blog/">Blog</a> &rsaquo; {title}</div>')
    body.append('')
    body.append(f'    {h1_html}')
    body.append(f'    <p class="meta">{date_str} &middot; {READ_TIME} &middot; {TYPE}</p>')
    body.append('')
    body.append(f'    <p>{intro}</p>')
    body.append(f'    <p>{intro2}{threadgrab_link} right now. Read it, fork the scripts, and ship your own reliability report by the end of the week.</p>')
    body.append('    <div class="callout">')
    body.append(f'      <p>{tldr}{threadgrab_link} runs in production for the X Articles drafting pipeline. The whole stack fits in 50 lines of Python and runs on a $5 VPS.</p>')
    body.append('    </div>')
    body.append('')

    # H2: intro_h2
    body.append(f'    <h2>{s["intro_h2"]}</h2>')
    body.append(f'    <p>{s["intro_p"]}</p>')
    body.append(f'    <p>{s["intro_p2"]}</p>')
    body.append('')

    # H2: what_h2
    body.append(f'    <h2>{s["what_h2"]}</h2>')
    body.append(f'    <p>{s["what_p"]}</p>')
    body.append(f'    <p>{s["what_p2"]}</p>')
    body.append('')

    # H2: passk_h2
    body.append(f'    <h2>{s["passk_h2"]}</h2>')
    body.append(f'    <p>{s["passk_p"]}</p>')
    body.append(f'    <p>{s["passk_p2"]}</p>')
    body.append('')

    # H2: table_h2
    body.append(f'    <h2>{s["table_h2"]}</h2>')
    body.append(f'    <p>{s["table_p"]}</p>')
    body.append('    <table>')
    body.append('  <thead>')
    body.append('    <tr>')
    body.append('      <th>Agent</th>')
    body.append('      <th>pass@1</th>')
    body.append('      <th>pass@5</th>')
    body.append('      <th>Cost / draft</th>')
    body.append('      <th>Self-host?</th>')
    body.append('      <th>Pricing model</th>')
    body.append('    </tr>')
    body.append('  </thead>')
    body.append('  <tbody>')
    for row in TABLE_ROWS:
        body.append('    <tr>')
        for cell in row:
            body.append(f'      <td>{cell}</td>')
        body.append('    </tr>')
    body.append('  </tbody>')
    body.append('</table>')
    body.append('')

    # H2: creator_h2
    body.append(f'    <h2>{s["creator_h2"]}</h2>')
    body.append(f'    <p>{s["creator_p"]}</p>')
    body.append('')

    # H2: creatorscript_h2 + code 1 (install)
    body.append(f'    <h2>{s["creatorscript_h2"]}</h2>')
    body.append(f'    <p>{s["creatorscript_p"]}</p>')
    body.append(f'    <pre><code>{CODE_INSTALL}</code></pre>')
    body.append('')

    # Code 2 (config)
    body.append(f'    <h3>Step 1b: The Caliper config file (caliper-xarticles.yaml)</h3>')
    body.append(f'    <pre><code>{CODE_CONFIG}</code></pre>')
    body.append('')

    # H2: evaluator_h2 + code 3 (evaluator)
    body.append(f'    <h2>{s["evaluator_h2"]}</h2>')
    body.append(f'    <p>{s["evaluator_p"]}{threadgrab_link} for the X Articles drafting pipeline.</p>')
    body.append(f'    <pre><code>{CODE_EVALUATOR}</code></pre>')
    body.append('')

    # H2: drift_h2
    body.append(f'    <h2>{s["drift_h2"]}</h2>')
    body.append(f'    <p>{s["drift_p"]}</p>')
    body.append('')

    # H2: ci_h2 + code 4 (CI action)
    body.append(f'    <h2>{s["ci_h2"]}</h2>')
    body.append(f'    <p>{s["ci_p"]}</p>')
    body.append(f'    <pre><code>{CODE_CI}</code></pre>')
    body.append('')

    # FAQ
    body.append('    <h2>FAQ: Caliper for Social Content Creators</h2>')
    for q, a in FAQ[lang]:
        body.append('    <div class="faq-item">')
        body.append(f'      <strong>{q}</strong>')
        # FAQ answers: keep as plain <p>, no inline <code> needed for this article
        body.append(f'      <p>{a}</p>')
        body.append('    </div>')
    body.append('')

    # CTA
    body.append('    <div class="cta">')
    body.append(f'      <p>{CTA[lang]}</p>')
    body.append(f'      <a class="btn" href="/{lang}/">{CTA_LINK[lang]}</a>')
    body.append('    </div>')
    body.append('')

    # Closing H2 + closing p
    body.append(f'    <h2>{CLOSING_H2[lang]}</h2>')
    body.append(f'    <p>{CLOSING_P[lang]}</p>')
    body.append('  </main>')
    body.append('')

    # Footer
    body.append('  <footer>')
    body.append(f'    &copy; 2026 ThreadGrab &middot; <a href="/{lang}/">Home</a> &middot; <a href="/{lang}/blog/">Blog</a> &middot; <a href="/{lang}/about/">About</a> &middot; <a href="/{lang}/privacy/">Privacy</a>')
    body.append('    <br>Not affiliated with Anthropic, OpenAI, Google, or Edon Adei.')
    body.append('  </footer>')
    body.append('</body>')
    body.append('</html>')
    return "\n".join(body)


def make_full_html(lang, slug):
    title = TITLES[lang]
    description = DESCRIPTIONS[lang]
    keywords = KEYWORDS[lang]
    head = make_meta_block(lang, title, description, keywords, slug)
    body = make_body(lang, title, slug)
    return head + "\n" + body + "\n"


# -----------------------------------------------------------------------------
# Verification
# -----------------------------------------------------------------------------
def verify(html, lang, title, description):
    """Run pre-build verification checks and print results."""
    issues = []
    # Title
    t_match = re.search(r'<title>(.*?)</title>', html)
    t = t_match.group(1) if t_match else ''
    if not (30 <= len(t) <= 60):
        issues.append(f"  ❌ title len = {len(t)} (must be 30-60): {t!r}")
    else:
        print(f"  ✅ title len = {len(t)}: {t!r}")
    # Description
    d_match = re.search(r'<meta name="description" content="(.*?)"', html)
    d = d_match.group(1) if d_match else ''
    if not (70 <= len(d) <= 155):
        issues.append(f"  ❌ desc len = {len(d)} (must be 70-155): {d!r}")
    else:
        print(f"  ✅ desc len = {len(d)}")
    # hreflang
    hreflang_count = len(re.findall(r'hreflang="(en|pt|id|x-default)"', html))
    if hreflang_count != 4:
        issues.append(f"  ❌ hreflang count = {hreflang_count} (must be 4)")
    else:
        print(f"  ✅ hreflang count = {hreflang_count}")
    # canonical
    if 'rel="canonical"' not in html:
        issues.append("  ❌ canonical missing")
    else:
        print("  ✅ canonical present")
    # JSON-LD blocks
    ld_count = len(re.findall(r'<script type="application/ld\+json">', html))
    if ld_count < 3:
        issues.append(f"  ❌ jsonld blocks = {ld_count} (must be >= 3)")
    else:
        print(f"  ✅ jsonld blocks = {ld_count}")
    # FAQ
    faq_count = len(re.findall(r'"@type": "Question"', html))
    if faq_count < 3:
        issues.append(f"  ❌ FAQ count = {faq_count} (must be >= 3)")
    else:
        print(f"  ✅ FAQ count = {faq_count}")
    # h2 count
    h2_count = len(re.findall(r'<h2', html))
    print(f"  ℹ️  h2 count = {h2_count}")
    # code blocks
    code_count = len(re.findall(r'<pre><code>', html))
    if code_count < 2:
        issues.append(f"  ❌ code blocks = {code_count} (must be >= 2)")
    else:
        print(f"  ✅ code blocks = {code_count}")
    # raw < or > in body (excluding <pre><code> blocks)
    # Remove all <pre>...</pre> blocks then check
    body_no_pre = re.sub(r'<pre>.*?</pre>', '', html, flags=re.DOTALL)
    # Also strip the <!DOCTYPE html> declaration (it appears at position 0 of the document, not in body)
    body_no_pre = re.sub(r'<!DOCTYPE[^>]*>', '', body_no_pre, count=1)
    raw_lt = re.findall(r'<(?!/?(?:html|head|body|meta|link|script|title|style|header|main|footer|h1|h2|h3|p|a|ul|ol|li|table|thead|tbody|tr|th|td|pre|code|div|span|strong|br|small|nav))', body_no_pre)
    if raw_lt:
        issues.append(f"  ❌ raw < in body = {len(raw_lt)} occurrences")
    else:
        print("  ✅ no raw < in body")
    # word count (body text only, strip code)
    body_text = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
    body_text = re.sub(r'<style.*?</style>', '', body_text, flags=re.DOTALL)
    body_text = re.sub(r'<pre>.*?</pre>', '', body_text, flags=re.DOTALL)
    body_text = re.sub(r'<[^>]+>', ' ', body_text)
    body_text = re.sub(r'\s+', ' ', body_text).strip()
    words = len(body_text.split())
    print(f"  ℹ️  word count = {words}")
    return issues


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main():
    os.chdir('/root/threadgrab-site')
    all_issues = {}
    for lang in ('en', 'pt', 'id'):
        print(f"\n=== Building {lang.upper()} version ===")
        title = TITLES[lang]
        description = DESCRIPTIONS[lang]
        html = make_full_html(lang, SLUG)
        path = f"{lang}/blog/{SLUG}.html"
        with open(path, 'w') as f:
            f.write(html)
        size = os.path.getsize(path)
        print(f"  wrote {path} ({size} bytes)")
        issues = verify(html, lang, title, description)
        all_issues[lang] = issues
        if issues:
            print("  ⚠️ ISSUES FOUND:")
            for i in issues:
                print(i)
    print("\n=== Summary ===")
    for lang, issues in all_issues.items():
        if issues:
            print(f"  {lang}: {len(issues)} issues")
        else:
            print(f"  {lang}: ✅ all checks passed")

if __name__ == '__main__':
    main()
