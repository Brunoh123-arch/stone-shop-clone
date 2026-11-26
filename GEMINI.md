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
| Vitrine / busca / recomendados | `js/catalogo.js` (`CATALOGO_PRODUTOS`) + `index.html` |
| Carrossel de criadores | vem do campo `creators` do JSON (autoplay mudo, IntersectionObserver). `js/videos-criadores.js` só serve produtos legados |
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
- **Slider:** 4 a 8 fotos oficiais de catálogo (TikTok Shop; fallback Mercado Livre), fundo branco/arte do vendedor. Proibido frame de vídeo no slider.
- **Variações:** cada cor com sua miniatura 1:1 (arquivo diferente por cor), trocando o slider ao clicar.
- **Unboxing em avaliações:** foto REAL de comprador (TikTok Shop; fallback Mercado Livre), ambiente doméstico real, produto/caixa físico visível. Proibido: ffmpeg de vídeo, IA, foto de estúdio, foto repetida.
  - **Um comprador = um card.** Todas as fotos do mesmo comprador (mesma sala/chão) ficam no MESMO `photos: [...]`; nunca fatiar em cards de “pessoas diferentes”.
  - **A cor em `variation` tem que bater com a cor do produto na foto.**

### 2.5 Avaliações (texto)
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
| **126** | Patinete Elétrico Infantil Dobrável c/ LED (60W, 8 km/h) | R$ 97,00 | **no ar** — pendência: só 2 criadores verificados (faltam vídeos do modelo exato) e 5 unboxings reais |
| 127 | Carrinho RC Drift 4x4 (fumaça + 2 baterias) | R$ 74,90 | fila |
| 128 | Mesa dobrável maleta 1,80 m | R$ 89,90 | fila |
| 129 | Escova elétrica giratória 9 em 1 c/ extensor | R$ 64,90 | fila |
| 130 | Colar Prata 925 c/ rosa giratória + sacola | R$ 74,90 | fila |
| 131 | Kit 2 jogos de cama casal 400 fios | R$ 69,90 | fila |

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
