# -*- coding: utf-8 -*-
"""ID content for search-result-redirects-cloaking-goto-2026."""

CONTENT = {
    'title': 'Redirect Hasil Pencarian 2026: GOTO, Cloaking, Bayar per Request',
    'desc': ("GOTO Google dan cloaking Brave merusak scraping SERP. Apa dampaknya bagi kreator yang mengarsipkan karyanya, dan kenapa pencarian berbayar."),
    'keywords': ("redirect hasil pencarian, Google GOTO, cloaking Brave, scraping SERP, "
                 "kedaluwarsa URL redirect, API pencarian x402, micropayment USDC, pencarian "
                 "agen AI, provenance arsip, ThreadGrab"),
    'body': r"""
<p>Dua mesin pencari mengubah cara tautan hasil mereka bekerja dalam minggu yang sama, dan
bagi siapa pun yang mengarsipkan atau memantau konten sosial, itu bukan hal yang sekadar
menarik untuk dippingelajari. Pada 26 Agustus 2026, Google mulai mengalirkan klik pada hasil
pencarian melalui <code>google.com/goto</code> sebelum mengarahkan pengunjung ke halaman
tujuan &mdash; sebuah mekanisme yang dikonfirmasi oleh persaan industri. Pada 11 November
2026, Brave Search mempublikasikan jawabannya sendiri: setiap tautan hasil kini menunjuk ke
URL <code>brave.com/go</code> yang terenkripsi per tautan, sehingga mesin pencari bisa tahu
bahwa sebuah klik berasal dari halaman hasil tanpa mengetahui tautan mana yang diklik.</p>

<p>Kedua langkah itu memang menyasar bot otomatis, dan keduanya punya efek samping
yang langsung menimpa kreator: <em>tautan yang disalin dari halaman hasil tidak lagi
menjadi tujuan</em>. Yang ada adalah sebuah redirect, dan redirect bisa kedaluwarsa. Kalau
arsip Anda menyimpan tautan itu, Anda menyimpan penunjuk ke tempat yang tidak lagi Anda
kendalikan &mdash; atau ke mana pun tidak.</p>

<p>Artikel ini membahas perubahan itu dan apa yang sebaiknya dilakukan seorang kreator.
Sudut pandang di sini bukan "pencarian jadi lebih sulit di-scrape." Lebih sempit dan lebih
praktis: tautan yang Anda temukan lewat pencarian adalah <strong>artefak transportsi</strong>,
dan satu-satunya hal yang layak disimpan adalah tujuan yang Anda resolve darinya.</p>

<h2>Apa yang Benar-Benar Berubah di Akhir 2026</h2>
<p>Mekanisme GOTO dari Google dan skema cloaking dari Brave memang terkait, tapi tidak
identik, dan perbedaan itu penting bagi siapa pun yang mengotomasi loop pengambilan data.
Berikut kronologi sebenarnya, lengkap dengan sumber primer:</p>
<table>
  <tr><th>Tanggal</th><th>Peristiwa</th><th>Sumber</th></tr>
  <tr><td>26 Agustus 2026</td><td>Google mulai mengalirkan klik hasil pencarian melalui <code>google.com/goto</code> sebelum tujuan</td><td>Dilaporkan Search Engine Land dan dilacak di Hacker News</td></tr>
  <tr><td>11 November 2026</td><td>Brave Search mempublikasikan desain cloaking-nya: tautan <code>brave.com/go</code> terenkripsi, dibangun di atas fungsi pseudorandom partially oblivious</td><td>Blog engineers Brave</td></tr>
  <tr><td>11 November 2026</td><td>Google Search Central memperingatkan bahwa pindah ke CDN bisa memblokir Googlebot, dan menjelaskan cara menghindarinya</td><td>Blog Google Search Central</td></tr>
  <tr><td>12 November 2026</td><td>API Brave Search menerima pembayaran agentik lewat protokol terbuka x402, dalam USDC di jaringan Base</td><td>Blog Brave</td></tr>
  <tr><td>13 November 2026</td><td>Pengumuman x402 mencapai 263 poin di Hacker News &mdash; sinyal terkuat bahwa agen yang membayar menjadi perhatian pengembang yang nyata</td><td>Hacker News</td></tr>
  <tr><td>18 November 2026</td><td>Tulisan cloaking Brave muncul di Hacker News, dan argumen pemindahan beban scraping menjadi perbincangan luas</td><td>Hacker News</td></tr>
</table>
<p>Cara Brave sendiri membingkai sebabnya layak dibaca dengan cermat, karena ini bukan
sekadar "kami memblokir bot." Argumen mereka berjalan begini: Google menerapkan GOTO, yang
membuat scraping hasil Google lebih sulit, dan bisnis scraping tidak hilang &mdash; ia pindah
tempat. Sebagian besar scraping yang tadinya mengarah ke Google kini datang ke pintu Brave,
karena Brave memiliki indeks sendiri alih-alih menjual ulang milik orang lain. Brave
melaporkan <strong>lonjakan trafik beberapa ribu permintaan per detik</strong> sebagai
dampak langsungnya.</p>

<p>Lonjakan itu punya biaya yang jatuh ke pengguna biasa. Brave menyatakannya lugas: trafik
tambahan memaksa perlindungan bot yang sudah tegang untuk menjadi lebih agresif, dan tagihan
itu jatuh ke orang sungguhan dalam bentuk hasil pencarian yang lebih lambat dan lebih banyak
CAPTCHA. Inilah pola yang perlu diamati di seluruh industri. Membela diri dari scraper tidak
gratis, dan biayanya dibayar oleh manusia yang tidak pernah melakukan skrip apa pun.</p>

<h2>Cara Kerja GOTO dari Google</h2>
<p>GOTO adalah lapisan redirect antara halaman hasil dan halaman tujuan. Pengalaman pengguna
tidak berubah: klik, sampai di halaman. Yang berubah adalah URL di bilah alamat, dan URL
yang tersalin ke papan klip, menjadi <code>google.com/goto/...</code> dan bukan alamat milik
penerbit itu sendiri.</p>

<p>Untuk permintaan otomatis, konsekuensinya mekanis dan langsung. Pipeline apa pun yang
menyalin URL hasil lalu menyimpannya &mdash; buku catatan riset, pengelola sitasi, alat
monitoring sosial, arsip pemendek tautan &mdash; kini menyimpan redirect yang di-host Google
alih-alih rujukan ke sumbernya. Untuk mendapatkan URL asli, Anda harus mengikuti redirect
itu, dan setelah mengikutinya, redirect itu sendiri tidak memberi Anda informasi apa pun
selain fakta bahwa tujuan tersebut ada hari ini.</p>

<h2>Jawaban Brave: Cloaking dengan Enkripsi per Tautan</h2>
<p>Desain Brave lebih menarik daripada redirect biasa, dan layak dipahami karena itulah yang
memperjelas arah yang sedang dilalui industri. Skemanya dibangun di atas <strong>fungsi
pseudorandom partially oblivious</strong>.</p>

<p>Mekanismenya, sebagaimana dijelaskan Brave: setiap tautan hasil mendapat kunci enkripsi
sendiri, dan hanya Brave yang memegang kunci-kunci itu. Ketika peramban Anda meminta kunci
untuk tautan yang Anda klik, ia menyamarkan permintaan dengan angka acak yang hanya diketahui
peramban itu sendiri. Bagi Brave, setiap permintaan seperti itu tampak identik. Brave bisa
mendekripsi permintaan dan mendapatkan tujuan, tanpa mengetahui tautan mana secara spesifik
dari halaman tersebut yang dipilih.</p>

<p>Properti privasi itu nyata dan layak dinyatakan secara akurat: Brave mempelajari
<em>dari halaman hasil mana</em> klik itu datang dan <em>kapan</em> itu terjadi, tetapi tidak
<em>tautan individual mana</em> yang diikuti. Itulah makna "partially" pada "partially
oblivious".</p>

<p>Properti anti-scraping-nya adalah aritmetika, bukan kriptografi. Argumen Brave adalah bahwa
scraper kini harus meminta kunci untuk setiap tautan yang ia inginkan, dan setiap permintaan
tersebut bisa dihitung per halaman. Seorang manusia membuka satu atau dua tautan dari
sebuah halaman hasil. Scraper ingin semuanya, di setiap halaman. Satu jawaban membuka satu
tautan, dan di situlah aritmetika scraper berubah: pemanenan hasil dalam skala menjadi
jauh lebih mahal tanpa mengganggu manusia yang benar-benar mencari.</p>

<h2>Efek Samping yang Tidak Diinginkan Siapa Pun</h2>
<p>Brave sangat terbuka soal biaya skema mereka sendiri, dan biaya-biaya itu tidak halus.
Tulisan mereka menyebutkannya, dan kreator perlu mengetahui ketiganya sebelum membangun
pipeline di atas hasil pencarian:</p>
<table>
  <tr><th>Efek samping</th><th>Yang kata Brave</th><th>Mengapa penting bagi arsip</th></tr>
  <tr><td>Kedaluwarsa redirect</td><td>URL redirect bisa kedaluwarsa, jadi tidak boleh dipercaya sebagai bookmark maupun untuk penyimpanan jangka panjang</td><td>Tautan hasil pencarian yang disimpan bukan rujukan yang awet. Ia bisa lapuk tanpa pemberitahuan.</td></tr>
  <tr><td>Permukaan phishing</td><td>Sebuah redirect bisa menjadi vektor phishing, sebab penyerang bisa memanfaatkan reputasi tautan <code>brave.com/go</code> untuk membawa sesuatu yang berbahaya</td><td>Mengikuti redirect buta dari indeks yang tidak diaudit berarti mengikuti URL yang dijamin pihak ketiga, bukan URL pilihan Anda sendiri.</td></tr>
  <tr><td>Ketergantungan JavaScript</td><td>Skema oblivious tidak berjalan bagi pengguna yang menonaktifkan JavaScript; dalam kasus itu Brave memakai redirect konvensional, sehingga server melihat URL yang diklik</td><td>Jaminan privasi bersifat bersyarat. Scraper tanpa JavaScript mendapat versi yang lebih lemah dari skema tersebut.</td></tr>
</table>
<p>Mitigasi Brave layak dicatat: kemampuan untuk menyangkal sebuah redirect, hitungan waktu
hidup, dan halaman interstisial yang memperingatkan pengguna. Waktu hidup inilah detail
praktis bagi siapa pun yang menyimpan tautan &mdash; artinya URL redirect punya masa simpan
yang ditentukan, dan penyimpanan Anda harus memperhitungkannya.</p>

<h2>Jalur Ramah Agen: Bayar per Permintaan</h2>
<p>Ada benang kedua yang lebih jarang dibahas dalam cerita yang sama, dan untuk audiens teknis
hal itu lebih penting daripada skema cloaking itu sendiri. Pada 12 November 2026, Brave
menambahkan dukungan pembayaran agentik ke API Brave Search melalui protokol terbuka
<strong>x402</strong>. Bingkai ini penting: alih-alih mempertahankan diri dari agen yang
meng-scrape hasil pencarian, Brave membangun cara bagi agen untuk <em>membayar</em>
mendapatkannya.</p>

<p>Cara kerjanya, diverifikasi terhadap dokumentasi agen Brave sendiri:</p>
<ul>
  <li>Endpoint-nya adalah <code>https://search.agent.s.brave.app</code>. Tidak ada API key, tidak ada akun, tidak ada pendaftaran &mdash; pembayaran yang ditandatangani adalah kredensialnya.</li>
  <li>Kirim permintaan tanpa header pembayaran dan Anda mendapat <strong>HTTP 402 Payment Required</strong> dengan body kosong. Semua yang Anda perlukan ada di header respons.</li>
  <li>Tandatangani sesuai tantangan yang diminta, lalu kirim ulang permintaan yang persis sama dengan header pembayaran yang dilampirkan. Respons sukses membawa header bukti pembayaran.</li>
  <li>Pembayaran diselesaikan dalam USDC di Base, rantai <code>eip155:8453</code>, sebesar 5000 unit dasar per permintaan &mdash; $0,005, atau $5 per 1.000 permintaan.</li>
  <li>Verifikasi berjalan lebih dulu, lalu pencarian dijalankan, lalu penyelesaian pembayaran terjadi. Pencarian yang gagal tidak pernah ditagih, jadi mengulangi pencarian yang gagal tidak menambah biaya.</li>
</ul>
<p>Ada dua detail yang mudah salah dan layak disalin persis. Pertama, <strong>x402 V2
saja</strong> &mdash; header V1 <code>X-Payment</code> tidak dikenali sebagai pembayaran dan
mendapat 402 kosong. Kedua, <strong>kirim tepat satu rail</strong>: header pembayaran di
samping header <code>Authorization</code>, skema apa pun itu, akan menghasilkan 400. Dan
tantangannya berumur pendek &mdash; satu penawaran x402 hanya bisa dibayar selama 300 detik,
jadi ambil 402 yang baru alih-alih mengulang tantangan lama.</p>

<p>Daftar harganya seragam. Pencarian web, konteks LLM, berita, gambar, video, dan endpoint
lokal semuanya berada di $0,005 per permintaan. Harga yang sama berlaku untuk API kredit
prabayar biasa, di mana paket resmi Brave adalah $5 per 1.000 permintaan, hingga 50 kueri
per detik, dengan hingga $20 panggilan gratis setiap bulan dan tanpa langganan. Sebagai
pembanding, evaluasi resmi Brave menempatkan biaya totalnya di $18 per 1.000 pertanyaan pada
FreshQA, melawan $49 sampai $89 untuk pesaing.</p>

<p>Tidak semua jalur dijual, dan kekurangannya informatif. Answers API tidak dijual, karena
ia menagih per kueri dan per token, yang tidak dapat diekspresikan oleh satu harga tetap.
Autosuggest dan Spellcheck juga tidak dijual: biayanya lebih rendah dari fee yang diambil
fasilitator untuk menyelesaikan satu pembayaran. Dan Summarizer tidak dijual karena Brave
telah menonaktifkannya. Jalur di luar tabel harga mengembalikan <strong>404</strong>, bukan
402 yang bisa dibayar &mdash; perbedaan yang berguna saat menelusuri bug di sebuah klien.</p>

<h2>Apa Artinya Ini bagi Kreator Konten Sosial</h2>
<p>Sekarang bagian yang benar-benar penting bagi publik ini. Tiga hal mengikuti dari penjelasan
di atas, dan hanya satu yang tentang scraping.</p>

<p><strong>Satu: tautan yang ditemukan lewat pencarian bukan sitasi.</strong> Kalau Anda
menemukan sebuah post di X, thread di Bluesky, atau artikel di LinkedIn lewat hasil
pencarian, URL yang Anda salin bisa jadi redirect yang kedaluwarsa. Resolve dulu, lalu
simpan tujuannya. Redirect adalah bukti bagaimana Anda menemukan barang itu; tujuannya
adalah barang itu sendiri.</p>

<p><strong>Dua: konten Anda sendiri kini lebih sulit ditemukan oleh agen daripada oleh
manusia.</strong> Mesin pencari sedang menambahkan lapisan khusus mesin &mdash; lompatan
redirect, tautan terenkripsi, pembayaran per permintaan &mdash; yang membuat penemuan
otomatis post Anda lebih mahal dan kurang andal. Ini memotong dua arah. Ini mengurangi
trafik scraper yang memperlakukan post Anda sebagai bahan latihan gratis, dan ini juga
berarti agen yang tadinya menemukan post Anda mungkin tidak menemukannya. Lapisan yang Anda
kendalikan adalah arsip, bukan jalur penemuan.</p>

<p><strong>Tiga: API bayar-per-permalink adalah pilihan yang sah, dan harganya memang
seperti itu.</strong> Kalau Anda membangun agen yang memantau hasil pencarian untuk sebutan
merek atau nama akun Anda &mdash; penggunaan yang sah dan makin umum &mdash; kini ada jalur
yang tidak mengharuskan Anda meng-scrape halaman hasil dan berharap tidak ada yang sadar.
Harganya $0,005 per permintaan, dan alternatifnya adalah membangun di atas skema redirect
yang aturannya bisa berubah tanpa pemberitahuan.</p>

<h2>Alur Capture yang Aman untuk Arsip</h2>
<p>Tiga langkah yang menyatu dalam satu skrip. Langkah pertama: resolve redirect dan ambil
tujuannya, jangan pernah redirect-nya. Langkah kedua: tulis URL hasil resolve ke file
provenance di samping capture, karena berkas tanpa URL asal bukan arsip, melainkan rumor.
Langkah ketiga: simpan salinan Anda sendiri, dengan waktu capture menempel padanya.</p>
<p>Perintah di bawah ini identik di ketiga versi bahasa artikel ini, jadi Anda bisa langsung
menyalinnya:</p>
<pre><code>__CODE1__</code></pre>
<p>Perhatikan apa yang sebenarnya dikembalikan perintah pertama: <code>%{url_effective}</code>
adalah tujuan setelah semua lompatan, dan <code>%{num_redirects}</code> memberi tahu berapa
lompatan yang diperlukan. Hitungan nol berarti URL hasil itu memang sudah menjadi sumber.
Hitungan dua atau tiga berarti tautan yang Anda terima adalah rantai redirect &mdash; persis
kasus di mana menyimpan URL asli akan jadi kesalahan.</p>
<p>Langkah kedua adalah tempat jalur bayar-per-permalink masuk, jika Anda memakainya. Dan
langkah ketiga adalah tempat arsip kreator masuk, yaitu satu-satunya bagian dari pipeline ini
yang sepenuhnya Anda kendalikan:</p>
<pre><code>__CODE2__</code></pre>
<p>Pemisahan antara kedua langkah itu adalah inti dari seluruh latihan ini. Pencarian adalah
<strong>lapisan penemuan</strong> &mdash; itu cara Anda menemukan sesuatu, dan kini makin
dibayar per permintaan mesin, serta URL-nya secara eksplisit dinyatakan tidak layak untuk
penyimpanan jangka panjang. Arsip Anda adalah <strong>lapisan kepemilikan</strong> &mdash;
itulah yang benar-benar Anda simpan, dan tidak kedaluwarsa hanya karena mesin pencari
mengubah format redirect pada hari Selasa.</p>

<h2>Di Mana Ini Berhenti</h2>
<p>Perlu ketepatan soal batas-batasnya, karena marketing di sekeliling cenderung berlebihan ke
dua arah.</p>

<p>Cloaking Brave bukan blokir total terhadap bot. Itu lapisan redirect dengan satu kunci per
tautan. Peramban manusia yang mengeklik satu tautan me-resolve-nya dalam satu permintaan,
persis seperti sebelumnya. Scraper yang ingin semua tautan di satu halaman harus meminta
semua kunci, dan setiap permintaan itu terlihat. Yang berubah adalah biaya, bukan izin
&mdash; dan biaya itu juga dibayar konsumen sah berkolume tinggi.</p>

<p>OTOS: endpoint x402 itu API pencarian berbayar, bukan gratis. Ini API bermeter, $0,005
per permintaan, dengan dompet, rantai, tahap penyelesaian, dan bukti pembayaran untuk
direkonsiliasi. API kredit prabayar biasa Brave tetap ada, tetap menyertakan hingga $20
pemanggilan gratis per bulan, dan tetap bekerja tanpa blockchain sama sekali. Jalur x402
untuk agen yang ingin membayar per permintaan tanpa membuka akun, bukan alternatif lebih
murah dari paket yang sudah ada.</p>

<p>Dan tren yang lebih luas tidak bergerak satu arah. Google justru sibuk di sisi berlawanan
masalah yang sama: pada November 2026 menerbitkan panduan tentang pindah ke CDN tanpa
membebani origin atau memblokir Googlebot, dan pada Oktober menambahkan dukungan untuk
kontrol pelatihan AI bersama untuk situs web. Kedua langkah memudahkan pemilik konten untuk
menyatakan apa yang boleh dan tidak boleh dirayapi. Cloaking redirect
membuat hasil pencarian lebih sulit di-scrape secara diam-diam. Keduanya adalah alat berbeda
yang mengarah ke perubahan latar yang sama &mdash; web sedang memperoleh kontrol akses
untuk mesin, dan pemilik konten akan diminta ikut serta dalam sebagian dari .</p>

<h2>FAQ</h2>
__FAQ_BLOCK__

<h2>Kesimpulan</h2>
<p>Manchete cerita ini adalah dua mesin pencari mengubah tautan hasil mereka. Cerita
praktisnya adalah URL yang disalin dari halaman hasil pencarian tidak lagi menjadi rujukan
yang awet, dan akses mesin ke pencarian sedang berubah menjadi transaksi yang dibayar
alih-alih scraping gratis.</p>
<p>Untuk kreator, jawaban atas keduanya sama dan tidak rumit. Resolve redirect sebelum Anda
menyimpan tautan. Perlakukan tujuan hasil resolve sebagai sitasi, dan redirect sebagai breadcrumbs.
Kalau Anda butuh pencarian berskala besar untuk monitoring yang sah, bayar untuk itu alih-alih
meng-scrape &mdash; pada setengah sen per permintaan, lebih murah daripada mempertahankan
scraper yang rusak setiap kali format redirect berubah. Dan simpan salinan Anda sendiri atas
publikasi Anda sendiri, karena tidak ada rekayasa lapisan pencarian yang membuat indeks orang
lain menjadi pemilik karya Anda.</p>
""",
    'faq': [
        ("Apa itu redirect GOTO dari Google?",
         "GOTO adalah lapisan redirect yang diperkenalkan Google pada akhir Agustus 2026, yang mengalirkan klik pada hasil pencarian lewat google.com/goto sebelum mengarahkan pengunjung ke halaman tujuan. Pengalaman pengguna tidak berubah, tetapi URL yang disalin dari halaman hasil kini adalah redirect-nya, bukan alamat milik penerbit."),
        ("Apakah Brave memblokir semua bot di Brave Search?",
         "Tidak. Skema Brave adalah lapisan cloaking, bukan blokir total. Tautan hasil menunjuk ke URL brave.com/go terenkripsi yang dibangun di atas fungsi pseudorandom partially oblivious, sehingga manusia yang mengeklik satu tautan me-resolve-nya dalam satu permintaan seperti sebelumnya. Yang berubah adalah ekonomi pemanenan massal, sebab scraper harus meminta kunci untuk setiap tautan dan setiap permintaan bisa dihitung per halaman."),
        ("Apakah tautan redirect hasil pencarian kedaluwarsa?",
         "Ya, dan Brave menyatakannya secara eksplisit di tulisan engineers mereka sendiri: URL redirect bisa kedaluwarsa, jadi tidak boleh dipercaya sebagai bookmark maupun untuk penyimpanan jangka panjang. Karena itu implementasi Brave menyertakan hitungan waktu hidup pada redirect tersebut. Selalu resolve redirect dan simpan URL tujuan."),
        ("Berapa biaya API pencarian Brave dengan x402 per permintaan?",
         "5000 unit dasar USDC di Base, setara $0,005 per permintaan, atau $5 per 1.000 permintaan. Pencarian web, konteks LLM, berita, gambar, video, dan endpoint lokal semuanya memiliki harga yang sama. Biaya gas ditanggung untuk periode terbatas. API kredit prabayar biasa juga $5 per 1.000 permintaan dan menyertakan hingga $20 panggilan gratis setiap bulan."),
        ("Apakah saya butuh dompet untuk memakai API agen Brave Search?",
         "Butuh, kalau Anda memakai endpoint x402, sebab pembayaran yang ditandatangani adalah kredensialnya dan tidak ada API key maupun akun. Brave menjalankan fasilitator sendiri yang menerima USDC di Base, dan klien seperti purl dari Stripe menangani penandatanganan. Kalau Anda tidak ingin mengelola dompet, API Brave Search standar dengan kartu kredit prabayar tetap bekerja dan tetap menyediakan panggilan gratis bulanan."),
        ("Haruskah saya mengarsipkan URL redirect hasil pencarian atau URL halaman akhir?",
         "Arsipkan URL halaman akhir, dan simpan redirect sebagai breadcrumbs di file provenance bila Anda ingin mencatat bagaimana item itu ditemukan. URL redirect adalah artefak transportsi dengan masa simpan terbatas dan bukan sumbernya. Gunakan URL hasil resolve sebagai sitasi dan catat waktu capture di sampingnya."),
    ],
    'related': [
        ('/id/blog/search-traffic-decline-social-archive-2026.html',
         'Penurunan Pencarian 2026: Mengarsipkan Adalah Asuransi Kreator'),
        ('/id/blog/crawlie-seo-crawler-tools-2026.html',
         'Crawlie &amp; Alat Crawler SEO 2026: 5 Dibandingkan'),
        ('/id/blog/koalisi-spur-telemetri-konten-2026.html',
         'Koalisi SPUR 2026: Telemetri Konten untuk Penerbit'),
        ('/id/blog/social-content-ownership-local-archiving-2026.html',
         'Kepemilikan Konten Sosial &amp; Pengarsipan Lokal 2026'),
        ('/id/blog/x-to-markdown-3-methods-2026.html',
         'X ke Markdown 2026: 3 Cara Menyimpan Thread X'),
    ],
    'cta_title': 'Arsipkan tujuan, bukan redirect-nya',
    'cta_body': ('ThreadGrab menyimpan thread X publik, kiriman Bluesky, dan artikel LinkedIn '
                 'sebagai Markdown dan JSON yang bersih, dengan waktu tangkapan menempel '
                 'padanya. Salinan Anda sendiri, di disk Anda sendiri, tidak bergantung pada '
                 'apa yang mesin pencari lakukan pada tautan hasilnya.'),
    'cta_btn': 'Coba ThreadGrab &rarr;',
    'sources': r"""
<p><strong>Sumber primer</strong></p>
<ul>
<li><a href="https://brave.com/blog/google-goto-anti-scraping/">Brave Search &mdash; How Google's anti-scraping move became our problem (and how we solved it in a user-first way), 11 Nov 2026</a></li>
<li><a href="https://brave.com/blog/search-api-agentic-payments/">Brave Search &mdash; The Brave Search API now accepts agentic payments via the x402 protocol, 12 Nov 2026</a></li>
<li><a href="https://search.agent.s.brave.app/llms.txt">Endpoint agen Brave Search &mdash; llms.txt: proxy bayar-per-permalink, tabel harga, rail, dan tabel galat</a></li>
<li><a href="https://search.agent.s.brave.app/openapi.json">Endpoint agen Brave Search &mdash; dokumen OpenAPI 3.1 dengan x-payment-info per jalur</a></li>
<li><a href="https://api-dashboard.search.brave.com/documentation/guides/agent-payments">Brave Search API &mdash; panduan pembayaran agen (dokumentasi proxy x402)</a></li>
<li><a href="https://brave.com/search/api/">Brave Search API &mdash; paket dan harga (Search Plan $5/1.000 permintaan, hingga $20 panggilan gratis bulanan)</a></li>
<li><a href="https://developers.google.com/search/blog/2026/11/crawling-cdn">Google Search Central &mdash; Moving to a CDN without overwhelming your origin (or blocking Googlebot), 11 Nov 2026</a></li>
<li><a href="https://developers.google.com/search/blog/2026/10/ai-training-control">Google Search Central &mdash; Supporting a shared AI training control for websites, 30 Okt 2026</a></li>
<li><a href="https://github.com/stripe/purl">Stripe &mdash; purl, dompet command line untuk menandatangani pembayaran x402</a></li>
<li><a href="https://searchengineland.com/google-confirms-deploying-goto-url-redirects-to-search-results-links-485926">Search Engine Land &mdash; Google confirms deploying goto URL redirects to search results links, 26 Agu 2026 (memblokir klien skrip; terbuka normal di peramban)</a></li>
</ul>
""",
}
