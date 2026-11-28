# Stone Studio (`/importador`) — Pré-Visualizador & Importador Instantâneo ("Zero-Delay")

- **Data:** 2026-11-27
- **Autor:** Bruno (CTO Stone Shop)
- **Status:** Especificação revisada com Motor Zero-Delay, Banco Reserva Instantâneo e Edição Live `0ms`

---

## 1. Objetivo e Experiência "Só Jogar o Link e Pronto"

Construir o **Stone Studio (`/importador`)**, um painel web responsivo (PC + Celular) rodando na máquina local e exposto via **URL pública HTTPS do Cloudflare Tunnel** (nunca enviando `localhost`), onde o operador pode **simplesmente colar um link do TikTok Shop ou Mercado Livre sem tocar em mais nada** e ver a página completa do produto brotar **em poucos segundos** já com título, preço PIX calibrado, fotos `1:1`, variações, avaliações reais, fotos de compradores e vídeos de criadores — podendo clicar em **`+ Mais Vídeos`**, **`+ Mais Comentários`** ou **`+ Mais Fotos de Compradores`** com resposta **instantânea (`0ms`)** e editar **nome, preço, desconto e textos em tempo real** sem recarregar a tela.

### Critérios de Sucesso
1. **Modo "Zero Toque" (Colou o Link → Aparece Tudo Montado):**
   - Nem o preço precisa ser digitado obrigatoriamente: se o operador só colar o link e der Enter, o motor extrai tudo, calcula automaticamente o **Preço PIX Sweet Spot** + ancoragem (`De R$ X por R$ Y`), gera descrição/ficha real, monta avaliações, fotos de unboxing e vídeos de criadores automaticamente.
2. **Arquitetura Zero-Delay (4 Camadas de Velocidade Extrema):**
   - **Fast-Path + Warm Browser (`~2–4s` para primeira tela completa):** Navegador persistente já aquecido em memória + leitura direta do JSON SSR da página exibem o produto montado no celular imediatamente usando URLs diretas no preview enquanto a conversão WebP `1:1` e o upload pro `Catbox` rodam **em paralelo nos bastidores** sem travar a tela.
   - **Banco Reserva Pré-Carregado (`Overfetch Pool` → `0ms` nos botões `+ Mais`):** Na mesma batida inicial, o motor não busca só o mínimo — ele puxa **50–80 avaliações reais**, **20+ fotos de compradores** e **20–25 vídeos de criadores** e guarda o excedente num **Pool Reserva em Memória**. Ao clicar em **`+ Mais Vídeos Criadores`**, **`+ Mais Comentários`** ou **`+ Mais Fotos de Compradores`**, os novos itens entram **instantaneamente (`0ms`)** na página sem esperar nova busca na rede (enquanto o worker reabastece o pool em background se necessário).
   - **Edição Ao Vivo `0ms` via `postMessage` (Estilo Figma/Canva):** Alterar **Nome do Produto**, **Preço PIX**, **Preço Antigo**, **Variações**, **Vendidos** ou ligar/desligar fotos, comentários e vídeos atualiza o DOM do **Celular Ao Vivo no mesmo milissegundo** via `window.postMessage`, sem piscar tela nem dar reload no iframe.
   - **Fila Catbox Assíncrona Transparente:** Enquanto o operador olha a prévia ou ajusta o preço, os workers Python já estão subindo os MP4s aprovados (e os próximos da reserva) para o `Catbox` + extraindo posters `ffmpeg` em paralelo (`4 uploads simultâneos`), exibindo selo `☁️ Catbox Pronto ✓` em cada vídeo.
3. **Trava Inegociável do Validador & Deploy 1-Clique:** Só publica na loja quando `node scripts/validar-modelo-unico.js` aprovar com **ZERO ERROS** (com rollback automático caso falhe). Aprovado, executa `git commit + push + vercel --prod + alias stoneshopclone.vercel.app` e já disponibiliza o produto na vitrine e na central `/videos-ads`.

---

## 2. Arquitetura e Unidades Isoladas

```
[Operador no PC ou Celular via HTTPS Cloudflare Tunnel]
                     │
                     ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ Unidade 1: Web UI Instantânea (importador.html + studio.js)  │
 │  - Input único "Cole o Link e Pronto" (Preço/Opções opcionais│
 │  - Edição Live 0ms (postMessage -> Iframe Celular Ao Vivo)   │
 │  - Botões 0ms: [+ Vídeos] [+ Comentários] [+ Fotos Unboxing] │
 │  - Mesa Visual: clicar p/ remover/trocar qualquer item       │
 └───────────────────────────┬──────────────────────────────────┘
                             │ SSE (Streaming Tempo Real) + REST
                             ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ Unidade 2: Studio Engine (scripts/studio/studio-api.js)      │
 │  - Plugado no server.js local (somente STUDIO_MODE=1 + Token)│
 │  - Gerencia Rascunho Ativo + Pool Reserva (.studio-drafts/)  │
 │  - Renderiza preview oficial via renderProdutoFromData()     │
 │  - Fila paralela em background (WebP 1:1 + ffmpeg + Catbox)  │
 │  - Publicador atômico + validar-modelo-unico.js + Deploy     │
 └──────────────┬──────────────────────────────┬────────────────┘
                │                              │
                ▼                              ▼
 ┌──────────────────────────────┐ ┌─────────────────────────────┐
 │ Unidade 3A: Warm Extractor   │ │ Unidade 3B: Video Pooler    │
 │  - Chrome aquecido s/ áudio  │ │  - Busca paralela 25 vídeos │
 │  - SSR JSON Fast-Path (~2s)  │ │  - Links extras colados     │
 │  - Overfetch: 60+ reviews &  │ │  - Stream imediato p/ tela +│
 │    20+ fotos de compradores  │ │    Upload Catbox 4x paralelo│
 └──────────────────────────────┘ └─────────────────────────────┘
```

### Unidade 1 — Interface Web "Zero Atrito" (`importador.html`, `css/studio-importador.css`, `js/studio-importador.js`)
- **Barra Topo "1-Segundo":**
  - Apenas um campo principal: **`🔗 Cole aqui o link do TikTok Shop ou Mercado Livre...`** + botão **`⚡ Puxar Tudo Agora`**.
  - Campos opcionais expansíveis (não obrigatórios na largada): *Link 2 complementar*, *Preço PIX manual* e *Gênero*.
- **Painel de Edição Instantânea (`0ms` via `postMessage`):**
  - Inputs diretos que refletem na hora dentro do celular ao lado enquanto você digita:
    - **Nome do Produto** (`product_title`)
    - **Preço PIX (`R$`)** e **Preço Antigo (`R$`)** → recalcula automático `% OFF`, `12x` no cartão, `produto_atual.preco` e economia do cupom na mesma hora!
    - **Contador de Vendidos** e **Nota Média** (`4.9`)
    - **Variações** (renomear/adicionar/remover cores, tamanhos `P–XG`, numeração `34–43` ou voltagem `110V/220V`, com preço específico opcional por opção).
- **Botões Instantâneos de Expansão (`0ms` do Pool Reserva):**
  - **`🎬 + Mais Vídeos Criadores`** → puxa instantaneamente mais `3` vídeos já pré-carregados da reserva (`reserve_videos[]`) pro carrossel ao vivo (e dispara reabastecimento silencioso no fundo se a reserva baixar de 5). Também inclui campo para colar links específicos do TikTok se quiser.
  - **`📸 + Mais Fotos de Compradores`** → puxa instantaneamente mais `2` cards reais de unboxing com foto da reserva (`reserve_unboxings[]`) e atualiza as avaliações no celular na hora.
  - **`💬 + Mais Comentários`** → puxa instantaneamente mais `5` avaliações reais em PT-BR da reserva (`reserve_reviews[]`) ou permite editar/escrever um comentário na hora.
- **Descarte em 1 Toque:** Todo slide, miniatura de variação, foto de comprador, comentário e vídeo tem botão `✕` (joga de volta pro fim da reserva ou descarta) e `★` (define foto principal ou vídeo da descrição).

### Unidade 2 — Studio Engine & SSE (`scripts/studio/studio-api.js` + `api/_lib/render-produto.js`)
- **Segurança & Isolamento:**
  - Ativo somente quando `server.js` sobe com `STUDIO_MODE=1`. Protegido por `STUDIO_TOKEN` na URL do Cloudflare Tunnel (`?key=<token>`, persistido em `localStorage`/cookie `HttpOnly`); requisições sem token recebem `401`.
- **Streaming Progressivo (`Server-Sent Events` em `GET /api/studio/stream/:draftId`):**
  - Assim que o link é colado:
    - **`T + 2s` (`event: fast_preview`):** Entrega título, preço calibrado, slides iniciais, variações e primeiras avaliações → o iframe do celular **já abre montado e interativo na tela!**
    - **`T + 6s` (`event: reviews_pool_ready`):** Entrega lote completo de avaliações + fotos reais de unboxing (`ativos` + `reserva`) e injeta no preview sem reload.
    - **`T + 8s` (`event: videos_preview_ready`):** Entrega os vídeos de criadores com posters/streams imediatos na tela (`ativos` + `reserva`), enquanto os workers sobem cada MP4 pro `Catbox` em `4` threads paralelas (`event: video_catbox_done`).
- **Refatoração Limpa em `api/_lib/render-produto.js`:**
  - Extrai `renderProdutoFromData(data, id, options)` mantendo `renderProdutoHtml(id)` 100% idêntico em produção. Quando `options.studioPreview === true`, injeta um micro-listener `window.addEventListener('message', ...)` de ~45 linhas dentro do preview que atualiza título, preços, desconto, galeria, variações, reviews e carrossel de criadores **em `0ms` sem recarregar o iframe**.

### Unidade 3 — Daemon Python Aquecido (`scripts/studio/studio_daemon.py`)
- **Por que um Daemon Persistente em vez de abrir processos soltos:**
  - Importar bibliotecas Python e iniciar o Chromium do zero leva `5–8s` toda vez. O `studio_daemon.py` sobe **junto com o `start-studio.ps1`** e mantém o contexto Playwright já aberto, minimizado e mudo (`--mute-audio` + bloqueio de `media` na rota de rede) pronto para navegar no primeiro milissegundo em que você colar o link!
- **Calibrador Automático de Preço PIX ("Sweet Spot"):**
  - Se o operador não digitar preço manual, calcula automaticamente a partir do preço real extraído do anúncio original:
    - Original até `R$ 80` → PIX `R$ 29,89` a `R$ 37,89`
    - Original `R$ 81–180` → PIX `R$ 47,89` a `R$ 57,89`
    - Original `R$ 181–400` → PIX `R$ 69,89` a `R$ 119,90`
    - Original `> R$ 400` → PIX `R$ 167,90` a `R$ 297,90`
    *(Sempre editável em `0ms` no campo de Preço PIX da tela).*
- **Overfetch de Avaliações & Fotos de Compradores:**
  - No Mercado Livre, pagina automaticamente o endpoint/drawer de opiniões filtrando *"Com fotos"* e *"5 / 4 estrelas"* para trazer até **20+ cards de compradores reais com fotos** + **50+ comentários reais em PT-BR** numa única passada.
  - No TikTok Shop, pagina as avaliações brasileiras com foto do anúncio e higieniza qualquer jargão proibido.
- **Overfetch Paralelo de Vídeos (`ThreadPoolExecutor` 4x):**
  - Coleta até **24 vídeos candidatos** de pessoas físicas no TikTok (filtrando perfis de loja/marca), resolve metadados/capas em paralelo via `tikwm` para exibir na hora na tela e nas reservas, e pré-aquece no `Catbox` (`ffmpeg` poster `0.5s` + compressão se `> 35 MB`) os vídeos ativos + os primeiros da reserva para que até o botão **"Publicar"** seja rápido.
- **Regra Inegociável Anti-CAPTCHA:** Se qualquer página exigir CAPTCHA ou verificação manual, o daemon **para aquela fonte imediatamente** (sem jamais tentar resolver/burlar) e sinaliza na UI.

### Unidade 4 — Launcher Cloudflare First (`scripts/studio/start-studio.ps1` + `npm run studio`)
- Sobe em conjunto:
  1. `node server.js` (`STUDIO_MODE=1`, `STUDIO_TOKEN=<gerado>`)
  2. `python scripts/studio/studio_daemon.py` (navegador aquecido em standby, minimizado e 100% mudo)
  3. `cloudflared tunnel --url http://127.0.0.1:3333` (baixando o binário oficial da Cloudflare em `.studio-bin/` caso não esteja no PATH)
- Imprime e copia automaticamente para o Ctrl+V a URL pública HTTPS:
  `https://<subdominio>.trycloudflare.com/importador?key=<token>`

---

## 3. Fluxo Atômico de Publicação, Validação e Rollback

Quando o operador clicar em **"🚀 Publicar na Loja"**:
1. **Aguarda Finalização de Catbox Pendente (se houver):** Se o operador clicou em *Publicar* em menos de 10 segundos e algum vídeo ativo ainda estiver terminando upload no Catbox na thread paralela, aguarda os segundos restantes com barra de progresso real.
2. **Alocação Automática de Avatares Brasileiros Verificados:** Garante avatares humanos de `img/reviews-avatars/mulheres_validadas/` e `mulheres_brasil/` (ou pool masculino verificado), bloqueando 100% `BAD_AVATARS` e colisões MD5, e crava `reviews_header === rating_count`.
3. **Promoção & Registro Completo:**
   - Copia apenas as mídias ativas para `img/` e `videosprodutos/posters/`.
   - Grava `data/produtos/produto-<id>.json` e atualiza `data/produtos/index.js`, `js/catalogo.js`, `index.html` (`#recommended-grid` + contador de `#categorias-section`) e `data/admin-catalogo-360.json`.
4. **Validação Obrigatória (`validar-modelo-unico.js`) com Rollback Automático:**
   - Roda `node scripts/validar-modelo-unico.js`. Se der qualquer erro, desfaz todas as alterações imediatamente e mostra o item exato na tela (ex.: *"Adicione +1 foto de comprador clicando em `+ Mais Fotos`"*).
5. **Deploy Automático:** Executa `git add` cirúrgico, `git commit`, `git pull --rebase --autostash origin main`, `git push origin main`, `npx vercel --prod --yes` e `npx vercel alias set <url> stoneshopclone.vercel.app`, entregando o link ao vivo da loja e o atalho direto pro `/videos-ads`.

---

## 4. Higiene de Repositório

- `.gitignore` e `.vercelignore` passam a ignorar `.studio-drafts/`, `.studio-chrome-profile/`, `.studio-bin/` (e `docs/` no `.vercelignore` para manter o deploy enxuto).
- Nenhum script temporário na raiz: todo o código do subsistema reside em `importador.html`, `css/studio-importador.css`, `js/studio-importador.js` e `scripts/studio/`.

---

## 5. Plano de Verificação

1. **Latência Inicial (`Fast-Path`):** Colar link real e medir abertura do preview interativo no celular em `< 4s` com título, preço calibrado, fotos e variações.
2. **Latência `0ms` dos Botões `+ Mais` e Edição Live:** Testar clique em `+ Mais Vídeos`, `+ Mais Fotos de Compradores`, `+ Mais Comentários` e digitação em `Nome` / `Preço PIX` verificando atualização instantânea no iframe sem reload.
3. **Zero Áudio:** Confirmar que durante toda a extração e busca de vídeos nenhuma aba toca áudio e nenhuma rota `/video/...` é aberta no navegador.
4. **Trava do Validador & Rollback:** Testar tentativa de publicação inválida confirmando restauração limpa do repo, seguida de publicação válida passando `ZERO ERROS` no `validar-modelo-unico.js`.
