# Stone Shop — Manual Mestre (Bruno CTO) — leia INTEIRO antes de mexer em qualquer coisa

> Sempre ativo na pasta `c:\Users\Dell\Downloads\ds`. Única fonte de verdade para qualquer chat novo.
> Site: `https://stoneshopclone.vercel.app` (Vercel) · Repo: GitHub `Brunoh123-arch/stone-shop-clone` (branch `main`).

---

## 1. COMO O PROJETO FUNCIONA

Loja e-commerce estilo **TikTok Shop Brasil**. Modelo Único Permanente:

| Peça | Arquivo |
|---|---|
| Dados de **cada produto** | `data/produtos/produto-[id].json` (NUNCA criar `pages/produto-*.html`) |
| Índice de registro | `data/produtos/index.js` → `'126': () => require('./produto-126.json'),` |
| Renderizador (Vercel Function) | `api/_lib/render-produto.js` injeta o JSON em `templates/produto-modelo.html` |
| Rotas | `/produto-126`, `/produto/126`, `/pages/produto-126` → `api/serve?slug=produto-126` (`vercel.json`) |
| Vitrine / busca / recomendados | `js/catalogo.js` (`CATALOGO_PRODUTOS`) + `index.html` (`#recommended-grid` e `#novos-lancamentos-section` têm cards estáticos HTML — atualizar AMBOS!) |
| Carrossel de criadores | vem do campo `creators` do JSON via `js/videos-criadores-modular.js` (autoplay mudo, IntersectionObserver). Adicionar comentários do nicho em `js/videos-criadores-modular.js` (`contextType`) |
| Anti-clone / cloaker v6.6 | `api/serve.js` (backend) + `js/tiktok-cloaker.js` (frontend) |
| Validador | `node scripts/validar-modelo-unico.js` (**obrigatório antes de todo commit**) |

**Cloaker:** bots de anúncio (TikTok/Google/Meta) passam; scrapers (HTTrack, SaveWeb2Zip, curl, headless) recebem `fake.html`. **Celular real (touch + GPU móvel) tem acesso liberado direto** — nunca redirecionar celular legítimo para `/loja`. Dono do site: `?preview=1`, `?c=1` ou `?owner=1`.

---

## 2. REGRAS DE OURO (violou = refazer)

### 2.1 Navegador / Playwright (Profile 42)
- Toda extração via **Playwright MCP no Chrome oficial, perfil Profile 42** (`kaiobrunocastro12@gmail.com`). Proibido instância anônima/headless genérica.
- Janela **sempre minimizada** (`Browser.setWindowBounds {windowState:'minimized'}`) e **ZERO ÁUDIO**: o usuário assiste Netflix enquanto você trabalha.
  - **NUNCA abrir páginas `/video/...` do TikTok no navegador** (o player toca som e vaza). Para baixar um vídeo use Python: `https://www.tikwm.com/api/?url=<url do vídeo>` → campo `data.play` → baixar MP4 → `ffmpeg` extrai frame → upload em `https://catbox.moe/user/api.php`. 100% silencioso.
  - Para listar vídeos na busca do TikTok via navegador, bloqueie mídia: `page.route('**/*', r => ['media'].includes(r.request().resourceType()) ? r.abort() : r.continue())`. Terminou? `page.goto('about:blank')`.
  - O endpoint de **busca** do tikwm devolve 403 — não tente burlar. Se não achar vídeos suficientes, **avise o usuário** (nunca complete com vídeo de outro produto).

### 2.2 INSPEÇÃO VISUAL É OBRIGATÓRIA (a causa de todos os erros passados)
**Nunca referencie uma imagem sem abri-la com `read_file` e olhar.** Confirme: cor exata da variação (um banner com 4 patinetes NÃO é a cor Azul), produto = o anunciado, avatar = rosto humano brasileiro do gênero certo (logo/cartoon/criança = proibido), unboxing sem marca de outro fabricante legível. Não deduzir cor/gênero pela ordem dos links, pelo número do arquivo ou por par/ímpar.

### 2.3 Mídia pertence a UM produto
- **PROIBIDO reaproveitar MP4/poster/foto de outro produto** (erro real: patinete com vídeo de livro infantil e de chinelo). O validador bloqueia `catbox_id` repetido entre produtos (ids ≥ 125).
- Vídeos de criadores: **8 a 15**, rostos/cenas/MP4 diferentes, do **produto exato**, fonte TikTok. Mínimo absoluto aceitável com aviso: o que for verificável — nunca encher com produto diferente.
- Criadores = **pessoas físicas** (@username de pessoa, rosto humano no avatar). Proibido perfil de loja/marca/logo (ex.: "Achadinhos…", "…Shop", "…Store", "Ruiva Tech").
- **Vídeo da descrição** (`video` no JSON → `#tt-product-video`) é obrigatório e **diferente** dos vídeos do carrossel.
- **Poster = frame real do próprio MP4** (`ffmpeg -ss 0.5 -i x.mp4 -vframes 1`). Proibido usar foto de catálogo como poster. Cache-buster `?v=AAAAMMDD` em posters/avatares.
- Hospedagem: Catbox (`files.catbox.moe`). Arquivo > 500 KB, HTTP 200/206.

### 2.4 Fotos
- **Slider:** 4 a 8 fotos oficiais de catálogo (TikTok Shop; fallback Mercado Livre), fundo branco/arte do vendedor. **PROIBIDO frame de vídeo no slider E nas miniaturas de variação (`variacoes.*.opcoes[].imagem`).**
- **Variações (fidelidade total ao anúncio):** cadastrar as cores/variações reais do anúncio original (se o anúncio tem 5 cores, não capar pra 2), cada cor com sua miniatura 1:1 oficial de catálogo (arquivo diferente por cor, nunca frame de vídeo), trocando o slider ao clicar.
- **Unboxing em avaliações (OBRIGATÓRIO — BLOQUEIA DEPLOY):** mínimo **6 cards de unboxing com foto REAL de comprador** (TikTok Shop; fallback Mercado Livre), ambiente doméstico real, produto/caixa físico visível. **PROIBIDO subir produto novo com 0 ou < 6 fotos de unboxing** (o validador trava como ERRO bloqueante). Proibido: ffmpeg de vídeo, IA, foto de estúdio, foto repetida.
  - **Um comprador = um card.** Todas as fotos do mesmo comprador (mesma sala/chão) ficam no MESMO `photos: [...]`; nunca fatiar em cards de “pessoas diferentes”.
  - **A cor em `variation` tem que bater com a cor do produto na foto.**

### 2.5 Avaliações (texto)
- **Volume e sincronia com vendidos:** no mínimo **20–26 avaliações reais** (com **6 a 10+ cards de unboxing com foto**). **REGRA CRÍTICA:** o número dentro de `reviews_header` (ex.: `"Avaliações dos clientes (386)"`) **TEM QUE SER IDÊNTICO** ao `rating_count` (`"(386)"`), porque `js/app.js` lê `reviews_header` e sobrescreve o contador do topo ao lado de `vendido(s)`!
- Texto real extraído do anúncio (PT-BR); proibido inventar em script. Sem vocabulário Shopee/AliExpress (“moedas”, “qualidade do produto:”).
- Mix ~90% 5★ / 10% 4★. Datas dos últimos 30–45 dias (`dd/mm`). `variation` só com opções que existem na grade do produto (sem “110V” em calçado).
- Nome mascarado (`M**a S**a`) com **gênero coerente com o avatar**. Produto feminino = 100% mulheres.

### 2.6 AVATARES (pastas)
- ✅ **Pode usar (inspecionado):** `img/reviews-avatars/mulheres_validadas/` (mulheres BR), `img/reviews-avatars/mulheres_brasil/`, avatares de criador baixados do próprio TikTok do criador para `img/avatars-<nicho>/`, e arquivos individuais de `img/reviews-avatars/tiktok_cdn_real/` e `tiktok_real/` **depois de abrir e conferir**.
- ❌ **Proibido:** pastas `unique/` e `curated/` (rostos gringos — EXCLUÍDAS do projeto), stock photo, IA, qualquer rosto estrangeiro.
- ❌ **Logos/cartoons conhecidos (bloqueados no validador):** `tt_avatar_5,9,11,12,13,17,19,29,31,37,39,43,57` e `tt_cdn_2,3,4,5,10,13,14,15,19,21,22,23,27,30`. O validador mantém a lista `BAD_AVATARS`; ao achar outro, adicione lá.
- Ainda não existe pasta só de homens validados. Para homem: abra e confira individualmente (`tt_cdn_6`, `tt_cdn_7` já conferidos).

### 2.7 Guia de tamanhos
Só vestuário/calçado: imagem gráfica oficial do vendedor (nunca tabela HTML), espelhada no alternador `[1/X]|[Tamanho]` e no modal. Brinquedo/eletrônico/casa: `"size_guide_html": ""` (omitir tudo).

### 2.8 Loja e limpeza
- Loja é SEMPRE **Stone Shop** (mascote `../logo.png`, selo azul). Proibido card de loja concorrente.
- Proibido: `*_backup`, `*_old`, `*_v2`, scripts/imagens soltos na raiz, lixo de IA. Scripts temporários → apagar após uso (rascunhos ficam em `scratch/` fora do repo).
- **Nunca enviar `localhost`.** Link ao usuário = HTTPS Vercel (ou Cloudflare Tunnel para lives).
- Preço: sweet spot PIX calibrado (ver §5). Sempre `produto_atual.preco` numérico (carrinho/PIX leem esse campo).

---

## 3. PASSO A PASSO PARA CADASTRAR PRODUTO (usuário mandou link/nome)

1. **Extrair** (Profile 42, silencioso): título, specs, fotos HD, variações, reviews com foto (TikTok Shop → fallback Mercado Livre).
2. **Baixar** mídia para `img/` (WebP/JPG): `produto-[id]-slide-N`, `…-var-<cor>`, `review-[id]-<comprador>-N`.
3. **ABRIR CADA IMAGEM (`read_file`)** e anotar o que é de verdade (§2.2). Descartar banner multi-cor, marca de outro fabricante, foto repetida.
4. **Vídeos:** pesquisar criadores reais do produto, baixar via Python/tikwm, frame com ffmpeg, subir no Catbox, baixar avatar do criador e conferir.
5. **Escrever** `data/produtos/produto-[id].json` (schema §4). Descrição/specs **só com o que as imagens/anúncio comprovam** (erro real: prometer Bluetooth/bivolt que o produto não tem).
6. **Registrar:** `data/produtos/index.js` e `js/catalogo.js`.
7. **Validar:** `node scripts/validar-modelo-unico.js` → zero erros; ler os AVISOS e contar ao usuário.
8. **Conferir no navegador do usuário** (celular) antes de dizer “pronto”.
9. **Deploy:** `git add -A; git commit -m "..."; git push origin main; npx vercel --prod --yes` + `npx vercel alias set <url> stoneshopclone.vercel.app`.

---

## 4. SCHEMA DO JSON (`data/produtos/produto-[id].json`) — copie de `produto-126.json`

Campos obrigatórios: `id, title, meta_description, product_title, slider_imgs[{src,alt}], discount_badge, price_int, price_cents, price_original, installment_text, installment_highlight, coupon_main, coupon_bonus, rating_score, rating_count, sold_count, frete_original, reviews_header, reviews_avg, reviews[{name,avatar,stars,date,variation,date_line,comment,photos[]}], details[{label,value,hidden}], video{src,poster,duration,catbox_id}, size_guide_html, description_html, related[{href,img,alt,name,price,price_original,discount,sold}], produto_atual, extra_scripts, creator_context, creators[{name,username,avatar,poster,video,catbox_id,startTime,likes,commentsCount,saves,shares,description}]`.

`produto_atual` (lido pelo carrinho/PIX): `id, nome, preco, preco_antigo, img, imagens[], variacoes:{cor:{com_imagem:true,label:"Cor",opcoes:[{imagem,nome}]}}` (+ `price, precoOrig, installmentText, shipping, store, rating, sales`). **Não usar `preco_avista`** — não é lido.

---

## 5. LISTA OURO NATAL / 13º (125–131) — preço PIX

| ID | Produto | PIX | Status |
|:--:|---|:--:|---|
| 125 | Carrinho Rolimã Girocar / Super Car LED (100 kg) | R$ 84,90 | fila |
| **126** | Patinete Elétrico Infantil Dobrável c/ LED (60W, 8 km/h) | R$ 47,89 | **100% blindado no ar** |
| **127** | Carrinho RC Drift 4x4 Turbo que Solta Fumaça + LED + Kit Pneus & Cones | R$ 49,89 | **100% blindado no ar** |
| **128** | Mesa Dobrável Portátil Vira Maleta 1,80 m Reforçada c/ Alça | R$ 67,89 | **100% blindado no ar** |
| **129** | Escova Elétrica Giratória Sem Fio 9 em 1 c/ Cabo Extensor 137 cm | R$ 29,89 | **100% blindado no ar** |
| **135** | Smartwatch Série 10 W99+ Pro AMOLED NFC ChatGPT | ativo | **no ar** |
| **144** | Câmera Infantil Instantânea que Imprime a Foto na Hora Sem Tinta + 3 Bobinas | R$ 37,89 | **100% blindado no ar** |
| **145** | Combo Mala de Bordo Rígida ABS Giro 360° ANAC + Frasqueira (Kit 2 Peças) | R$ 69,89 | **100% blindado no ar** |
| **146** | Caixa de Som Portátil JBL PartyBox Encore Essential Bluetooth 100W RMS LED IPX4 | R$ 37,90 | **100% blindado no ar** |
| **147** | Triciclo Elétrico Drift Infantil 360° 350W Bateria 36V c/ LED, Chave e Bluetooth | R$ 54,90 | **100% blindado no ar** |
| **148** | Jogo de Panelas Brinox Ceramic Life Smart Plus 8 Peças Vanilla c/ Tampas de Vidro | R$ 49,90 | **100% blindado no ar** |
| **149** | Cortina Cascata Luminosa 3m x 3m 300 LEDs Colorido RGB & Branco Quente USB c/ Controle | R$ 29,89 | **100% blindado no ar** |
| **150** | Fogão 4 Bocas Esmaltec Ideal Super Mesa Inox Acendimento Automático Forno 50L Bivolt | R$ 189,90 | **100% blindado no ar** |
| **151** | Smart TV 32" LG HD LED ThinQ AI HDR10 Processador α5 WebOS Wi-Fi Bluetooth | R$ 279,90 | **100% blindado no ar** |
| **152** | Smartphone Samsung Galaxy A17 5G 128GB 4GB RAM Super AMOLED 6,7" 90Hz 50MP NFC | R$ 279,90 | **100% blindado no ar** |
| **153** | Tablet Samsung Galaxy Tab S10 FE 128GB 8GB RAM 10,9" 90Hz IP68 c/ S-Pen e Capa | R$ 297,90 | **100% blindado no ar** |
| **154** | Máquina de Lavar Roupas Brastemp 13kg Automática Cesto Inox Tira-Manchas Advanced | R$ 397,90 | **100% blindado no ar** |

### 5.1 FILA PRÓXIMOS CAMPEÕES — ORGANIZADA EM 3 LOTES (#155 a #166) — Puxar no Profile 42

| Lote | ID | Produto / Gatilho | PIX | Links Base / Busca (Profile 42) |
|:--:|:--:|---|:--:|---|
| **Lote 1 (Black Urgente)** | **155** | **Combo Bolsa Feminina Luxo Transversal + Relógio Dourado + Carteira + Pulseira (Kit 4 em 1)** | **R$ 49,89** | TT: `https://shop.tiktok.com/br/pdp/1738506652937389299` · `https://shop.tiktok.com/br/pdp/kit-prime-desejado-com-caixa-de-presente-ocasioes-especiais/1733666761179367118` · ML: `MLB50330996` / `MLBU3915875418` |
| **Lote 1 (Black Urgente)** | **156** | **Kit Leve 4 Roupas Femininas Verão/Fim de Ano (4 Vestidos Canelados ou 4 Blusas Caneladas)** | **R$ 54,89** | TT: `https://shop.tiktok.com/br/pdp/1735058119636584400` · `https://shop.tiktok.com/br/pdp/1738105625122538960` |
| **Lote 1 (Black Urgente)** | **157** | **Kit Leve 4 Camisetas Masculinas 100% Algodão Fio 30.1 / Oversized Casual** | **R$ 49,89** | TT: `https://shop.tiktok.com/br/pdp/kit-4-camisetas-masculinas-oversized-100-algodao-streetwear/1737238568108722123` · ML: `MLB-4574806641` / `MLBU4163539189` |
| **Lote 1 (Black Urgente)** | **158** | **Combo Presente Masculino: Relógio Cronógrafo Aço + Carteira Couro + Cinto + Óculos Polarizado (Caixa)** | **R$ 54,89** | Buscar: `kit relogio masculino carteira cinto oculos presente` |
| **Lote 1 (Black Urgente)** | **159** | **Combo 2 Pares Sandália Brilho/Salto Bloco + Bolsa Tiracolo Brinde (Natal & Réveillon)** | **R$ 57,89** | Buscar: `kit 2 sandalia feminina brilho bolsa` |
| **Lote 2 (13º Dia 30/11)** | **160** | **Porta-Joias Rosa Eterna Giratória + Colar Prata 925 "Eu Te Amo em 100 Idiomas" + Sacola** | **R$ 49,89** | Buscar: `porta joias rosa giratoria colar 100 idiomas` |
| **Lote 2 (13º Dia 30/11)** | **161** | **Maleta Completa de Maquiagem Profissional (ou Kit 12 Itens Make + Necessaire Brinde)** | **R$ 47,89** | Buscar: `maleta maquiagem completa profissional` |
| **Lote 2 (13º Dia 30/11)** | **162** | **Kit Leve 4 Conjuntos/Shorts Fitness Empina Bumbum Sem Costura Feminino** | **R$ 49,89** | Buscar: `kit 4 conjunto fitness empina bumbum` / `kit 4 short legging seamless` |
| **Lote 2 (13º Dia 30/11)** | **163** | **Kit Leve 4 Bermudas Masculinas Verão (Elastano / Tactel Praia & Churrasco)** | **R$ 54,89** | Buscar: `kit 4 bermuda masculina elastano verao` |
| **Lote 3 (Dezembro)** | **164** | **Kit Leve 3 Conjuntos Pijama Cetim/Seda Verão (Baby Doll Luxo)** | **R$ 44,89** | Buscar: `kit 3 pijama cetim feminino baby doll` |
| **Lote 3 (Dezembro)** | **165** | **Combo Leve 2 Jogos de Cama Casal 400 Fios Padrão Hotel (8 Peças)** | **R$ 54,89** | Buscar: `kit 2 jogo de cama casal 400 fios hotel` |
| **Lote 3 (Dezembro)** | **166** | **Carrinho Rolimã Girocar / Super Car LED Infantil Suporta 100 kg** | **R$ 64,89** | Buscar: `carrinho rolima girocar led infantil` |

---

## 6. DÍVIDAS TÉCNICAS CONHECIDAS (não esconda do usuário)
- ~42 produtos antigos (< 125) ainda usam avatares de logo/cartoon da lista `BAD_AVATARS` (validador só informa; corrigir 1 a 1 com inspeção visual).
- Scripts antigos em `scripts/` referenciam `reviews-avatars/unique|curated` (pastas já excluídas) — são resíduos de patches únicos; podem ser apagados.
- `js/videos-criadores.js` (7 mil linhas) só atende produtos legados; produto novo usa `creators` no JSON.

---

## 7. COMANDOS
```powershell
node scripts/validar-modelo-unico.js
git add -A; git commit -m "feat/fix: ..."; git push origin main
npx vercel --prod --yes
npx vercel alias set <deployment-url> stoneshopclone.vercel.app
```
(PowerShell: não use `&&`; use `;`.)
