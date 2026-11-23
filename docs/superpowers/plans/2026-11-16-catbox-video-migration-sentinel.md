# Catbox Video Migration, Product Namespaces & Sentinel Health-Check Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Organizar os 141 vídeos hospedados no Catbox por namespaces e pastas isoladas por produto, substituir todas as referências locais no código (`js/videos-criadores.js`, `pages/*.html`, `_pages/*.html`, `scripts/data/*.json`) pelos links do Catbox, purgar com segurança cirúrgica os 621.5 MB de arquivos `.mp4` pesados preservando posters e metadados, e entregar o sistema Sentinel (CLI automatizado com teste HTTP 206/200 + visualizador interativo em tempo real integrado no `admin.html`).

**Architecture:**
- **Namespaces Estruturados**: Catálogo canônico em `config/products_video_catalog.json` e organização lógica/física por pasta de produto (`churrasqueira-arke`, `churrasqueira-biscuitt`, `piscina-32`, `praia-32`, `pneu-28`, e produtos individuais `produto-11` a `produto-97`).
- **Migração Idempotente**: Script de substituição com regex exato em `scripts/migrate_replace_catbox_urls.py` que trata caminhos relativos (`../videosprodutos/`, `./videosprodutos/`, `videosprodutos/`), atributos HTML `src="..."`, arrays JavaScript de galerias (`imagens: [...]`), query params de versão (`?v=...`) e propriedades `localVideo`/`video`.
- **Purga Blindada**: Script `scripts/verify_and_purge_heavy_videos.py` com Safety Gates inegociáveis (validação de integridade de 100% dos links Catbox, checagem de zero referências locais restantes no código, geração de manifesto de auditoria `data/purged_videos_manifest.json` com hashes e tamanhos).
- **Sentinel Health-Check**:
  - **CLI (`scripts/sentinel_catbox.py`)**: Multi-threaded (ThreadPoolExecutor), cabeçalho `User-Agent: Mozilla/5.0`, requisição `Range: bytes=0-10`, detecção de status 206/200, medição de latência (ms) e exportação para o asset estático `data/sentinel_health_report.json`.
  - **Admin Panel Visualizer (`admin.html`)**: Nova aba/view `#view-sentinel` carregando diretamente `data/sentinel_health_report.json` via fetch estático (zero risco de timeout serverless), com KPIs em tempo real, filtro por namespace de produto, busca instantânea, status visual (`200 OK` / `206 OK` verde, `Offline` vermelho), latência e player modal preview. Suporta re-varredura ao vivo no browser via CORS nativo do Catbox (`Access-Control-Allow-Origin: *`).

**Tech Stack:** Python 3.13 (ThreadPoolExecutor, urllib/requests, hashlib, json, re), JavaScript ES6+ (Fetch API, IntersectionObserver, HTML5 Video API), Vercel Static Hosting / CDN.

**Nota Importante de Ambiente:** O workspace `c:\Users\Dell\Downloads\ds` NÃO é um repositório git (`.git` inexistente). As tarefas realizam operações diretas em disco com manifestos de auditoria e validação por scripts de teste, sem comandos `git commit`.

---

## Global Constraints

1. **Preservação Sagrada de Imagens e Posters**: É estritamente proibido deletar, alterar ou corromper qualquer poster (`.jpg`, `.png`, `.webp`), capa ou avatar. Apenas os 141 arquivos `.mp4` pesados identificados em `catbox_video_map.json` são elegíveis para purga.
2. **Deduplicação de Hash Catbox**: Em `catbox_video_map.json`, os 141 caminhos locais mapeiam para 136 URLs Catbox únicas porque 5 pares de vídeos possuem conteúdo binário idêntico e a CDN Catbox deduplica por hash MD5. O catálogo e os testes DEVEM reconhecer e suportar essa deduplicação sem falsos-positivos.
3. **Isolamento por Produto (1 Pasta/Namespace por Produto)**: Cada produto possui seu namespace único (`churrasqueira-arke`, `piscina-32`, etc.). Nenhuma mídia de outro nicho pode ser misturada (doutrina de fidelidade `GEMINI.md`).
4. **Substituição Abrangente**: O processo de substituição DEVE atualizar:
   - Atributos `src="..."` de tags `<video>`.
   - Propriedades `video` e `localVideo` em `js/videos-criadores.js`.
   - Arrays JavaScript de sliders em páginas (ex: `imagens: ["../videosprodutos/..."]`).
   - Query strings acopladas a caminhos de vídeo (ex: `?v=20261113_arke_v100`).
5. **Sentinel Estático + Browser Live**: O painel do Admin deve consumir o arquivo estático `data/sentinel_health_report.json` e permitir varredura ao vivo no browser via client-side fetch com `Range: bytes=0-10`, eliminando qualquer dependência de serverless functions que possam sofrer timeout.
6. **Deploy e Cache-Busters**: Execução mandatória de `python scripts/update_cache_buster.py` e verificação de deploy Vercel em `https://stoneshopclone.vercel.app`.

---

## Implementation Tasks

### Task 1: Catálogo Estruturado de Vídeos por Namespace de Produto e Organização

**Files:**
- Create: `config/products_video_catalog.json`
- Create: `scripts/generate_video_catalog.py`
- Create: `tests/test_video_catalog.py`

- [ ] **Step 1: Escrever teste automatizado `tests/test_video_catalog.py`**
  - Validar que o catálogo existe e contém exatamente 141 entradas locais mapeadas para URLs válidas (`https://files.catbox.moe/[a-z0-9]+\.mp4`).
  - Validar que as 136 URLs únicas do Catbox estão atribuídas corretamente (comprovando suporte a deduplicação de hash para os 5 pares idênticos).
  - Validar que cada item contém: `namespace`, `product_id`, `video_id`, `original_path`, `catbox_url`, `poster_path`.
  - Validar que todos os 48 namespaces estão presentes e catalogados.

- [ ] **Step 2: Executar teste para confirmar falha inicial**
  ```powershell
  python tests/test_video_catalog.py
  ```

- [ ] **Step 3: Implementar o script gerador `scripts/generate_video_catalog.py`**
  - Ler `catbox_video_map.json`.
  - Agrupar e classificar os 141 vídeos nos namespaces formais:
    - `churrasqueira-arke` (8 vídeos: `churras-arke-c1.mp4` a `c8.mp4`, prodId: 104)
    - `churrasqueira-biscuitt` (6 vídeos: `churras-biscuitt-c1.mp4` a `c6.mp4`, prodId: 107)
    - `piscina-32` (32 vídeos: `piscina_32/pool_01.mp4` a `pool_32.mp4`, prodId: 13)
    - `praia-32` (32 vídeos: `praia_32/beach_01.mp4` a `beach_32.mp4`, prodId: 18)
    - `pneu-28` (13 vídeos: `videosdoscriadorespneu/WhatsApp Video...mp4`, prodId: 108/pneu)
    - Produtos individuais: `produto-5`, `produto-11`, `produto-14` a `produto-97` (vídeos de criadores e reviews).
  - Identificar os posters correspondentes em `videosprodutos/posters/` e `img/posters-*/`.
  - Exportar `config/products_video_catalog.json` estruturado por produto.

- [ ] **Step 4: Executar o gerador e rodar o teste de validação**
  ```powershell
  python scripts/generate_video_catalog.py
  python tests/test_video_catalog.py
  ```

---

### Task 2: Migração e Substituição de Caminhos Locais por URLs Catbox

**Files:**
- Create: `scripts/migrate_replace_catbox_urls.py`
- Create: `tests/test_url_replacement.py`
- Modify: `js/videos-criadores.js`
- Modify: `pages/*.html`
- Modify: `_pages/*.html`
- Modify: `scripts/data/*.json`

- [ ] **Step 1: Escrever teste de integridade `tests/test_url_replacement.py`**
  - Mapear todos os arquivos de código ativos (`js/videos-criadores.js`, `pages/produto-*.html`, `_pages/produto-*.html`, `scripts/data/*.json`).
  - Buscar referências residuais a `.mp4` locais em `videosprodutos/` ou `videosdoscriadorespneu/` (tanto em tags HTML `<video src="...">`, quanto em objetos JS `video: "..."`, `localVideo: "..."` e arrays `imagens: [...]`).
  - Validar que nenhuma query string antiga (ex: `?v=...`) fica órfã em links locais.

- [ ] **Step 2: Executar o teste para confirmar estado inicial pendente**
  ```powershell
  python tests/test_url_replacement.py
  ```

- [ ] **Step 3: Implementar o script de migração `scripts/migrate_replace_catbox_urls.py`**
  - Carregar `config/products_video_catalog.json` e `catbox_video_map.json`.
  - Executar substituição regex abrangente tratando:
    - `"../videosprodutos/<nome>.mp4(\?v=[^"'\s]+)?"` -> `"https://files.catbox.moe/..."`
    - `"./videosprodutos/<nome>.mp4(\?v=[^"'\s]+)?"` -> `"https://files.catbox.moe/..."`
    - `"videosprodutos/<nome>.mp4(\?v=[^"'\s]+)?"` -> `"https://files.catbox.moe/..."`
    - `"../videosdoscriadorespneu/<nome>.mp4"` -> `"https://files.catbox.moe/..."`
    - `"videosdoscriadorespneu/<nome>.mp4"` -> `"https://files.catbox.moe/..."`
    - Atualização simultânea das chaves `video` e `localVideo` em `js/videos-criadores.js`.
    - Atualização de ocorrências em arrays de sliders `imagens: ["../videosprodutos/video-produto-X.mp4", ...]`.
  - Preservar rigorosamente todos os caminhos de posters e imagens.
  - Imprimir log detalhado de substituições por arquivo modificado.

- [ ] **Step 4: Executar a migração e rodar o teste de validação**
  ```powershell
  python scripts/migrate_replace_catbox_urls.py
  python tests/test_url_replacement.py
  ```

---

### Task 3: Verificação Prévia de Integridade e Purga Segura dos Arquivos Pesados

**Files:**
- Create: `scripts/verify_and_purge_heavy_videos.py`
- Create: `data/purged_videos_manifest.json`
- Create: `tests/test_disk_purge.py`

- [ ] **Step 1: Escrever teste de purga `tests/test_disk_purge.py`**
  - Verificar que nenhum dos 141 arquivos `.mp4` mapeados permanece em disco.
  - Validar que o diretório de posters `videosprodutos/posters/` e as pastas `img/posters-*/` permanecem 100% íntegras com todas as imagens preservadas.
  - Validar que o manifesto `data/purged_videos_manifest.json` existe com 141 entradas detalhando tamanho original em bytes e timestamp da purga.

- [ ] **Step 2: Implementar `scripts/verify_and_purge_heavy_videos.py` com Safety Gates**
  - **Safety Gate 1**: Validar existência e completude de `config/products_video_catalog.json` (141 entradas).
  - **Safety Gate 2**: Executar validação de conectividade via ping HTTP `Range: bytes=0-10` em amostra de verificação dos links Catbox. Se houver falha de rede ou link quebrado, abortar imediatamente sem deletar nada.
  - **Safety Gate 3**: Confirmar que o teste `tests/test_url_replacement.py` passou com zero referências locais pendentes.
  - **Geração de Auditoria**: Calcular SHA256 e tamanho exato de cada um dos 141 arquivos `.mp4`, salvando em `data/purged_videos_manifest.json`.
  - **Execução Seletiva**: Deletar exclusivamente os arquivos `.mp4` mapeados. NUNCA remover diretórios inteiros para não perder posters ou subpastas de imagem.
  - Suportar flag `--dry-run` para simulação prévia e `--execute` para exclusão real.

- [ ] **Step 3: Executar a purga e validar com teste automatizado**
  ```powershell
  python scripts/verify_and_purge_heavy_videos.py --dry-run
  python scripts/verify_and_purge_heavy_videos.py --execute
  python tests/test_disk_purge.py
  ```

---

### Task 4: Ferramenta Sentinel CLI de Health-Check Catbox

**Files:**
- Create: `scripts/sentinel_catbox.py`
- Create: `tests/test_sentinel_cli.py`
- Output: `data/sentinel_health_report.json`

- [ ] **Step 1: Escrever teste unitário `tests/test_sentinel_cli.py`**
  - Testar requisição individual mockada (retornos 200, 206, 404, timeout).
  - Testar conformidade do schema de saída JSON exportado em `data/sentinel_health_report.json`.
  - Testar filtros CLI (`--product`, `--all`).

- [ ] **Step 2: Implementar o Sentinel CLI `scripts/sentinel_catbox.py`**
  - Carregar `config/products_video_catalog.json`.
  - Requisição HTTP concorrente (ThreadPoolExecutor com 15 threads padrão):
    - Headers: `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`, `Range: bytes=0-10`.
    - Timeout: 10s com até 2 retries inteligentes em caso de handshake drop.
  - Métricas registradas:
    - `url`: link Catbox.
    - `status_code`: 206 / 200 (OK) ou código de erro.
    - `latency_ms`: tempo de resposta da CDN em milissegundos.
    - `content_range` / `total_bytes`: tamanho total do arquivo reportado pela CDN.
    - `state`: `HEALTHY`, `SLOW` (>1500ms), `DEAD`.
  - Saída no terminal: Tabela visual resumida com cores e estatísticas agregadas (Total, Operacionais, Taxa de Sucesso, Latência Média).
  - Exportação automática para `data/sentinel_health_report.json`.

- [ ] **Step 3: Executar o teste unitário e rodar a varredura real completa de produção**
  ```powershell
  python tests/test_sentinel_cli.py
  python scripts/sentinel_catbox.py --all
  ```

---

### Task 5: Visualizador Sentinel & Monitor de Vídeos no Admin Panel

**Files:**
- Modify: `admin.html`
- Create: `tests/test_admin_sentinel.py`

- [ ] **Step 1: Escrever teste automatizado `tests/test_admin_sentinel.py`**
  - Validar a presença do botão de navegação `Sentinel CDN` no menu desktop (`desktop-nav`) e no menu lateral/mobile de `admin.html`.
  - Validar que o container `<section id="view-sentinel" class="view-section">` está presente no DOM.
  - Validar elementos da interface: 4 KPI Cards (Total Monitorado, Taxa de Saúde %, Latência Média, Espaço Liberado), filtro por produto, barra de busca instantânea e grid de vídeos.
  - Validar que a função JavaScript `carregarSentinelReport()` consome `data/sentinel_health_report.json`.

- [ ] **Step 2: Executar teste para confirmar ausência inicial**
  ```powershell
  python tests/test_admin_sentinel.py
  ```

- [ ] **Step 3: Implementar a interface do Sentinel no `admin.html`**
  - **Menu de Navegação**:
    - Adicionar item no header desktop: `<button class="nav-btn" onclick="trocarAba('sentinel')"><i class="fas fa-satellite-dish"></i> Sentinel CDN</button>`.
    - Adicionar atalho correspondente na navegação mobile/drawer.
  - **Seção `#view-sentinel`**:
    - **Header & Action Bar**:
      - Título: "Sentinel CDN — Monitor de Saúde de Vídeos Catbox".
      - Subtítulo com timestamp da última varredura.
      - Botão "▶ Varredura Ao Vivo (Browser)" e botão "🔄 Recarregar Relatório".
    - **KPI Cards Modernos**:
      - Total de Vídeos Monitorados (141).
      - Saúde da Rede (% de links 200/206).
      - Latência Média (ms).
      - Armazenamento em Nuvem / Economia Local (~621.5 MB).
    - **Filtros e Controles**:
      - Select dropdown por namespace de produto (Todos, Churrasqueira Arke, Churrasqueira Biscuitt, Piscina 32, Praia 32, Pneu 28, etc.).
      - Input de busca textual em tempo real por URL, nome ou namespace.
      - Barra de progresso para varredura em tempo real no browser.
    - **Grid de Cards de Vídeos**:
      - Poster / thumbnail do vídeo.
      - Badge de status (`206 OK` verde, `Offline` vermelho).
      - Latência (ex: `142ms`).
      - Namespace do produto e ID.
      - Link Catbox com botão de copiar link com 1 clique.
      - Botão "Preview" que abre modal com player nativo `<video controls autoplay>`.
  - **Lógica JavaScript**:
    - Consumo nativo via `fetch('data/sentinel_health_report.json?v=' + Date.now())` com renderização dinâmica rápida dos cards.
    - Suporte a re-varredura local no navegador usando `fetch(url, { headers: { 'Range': 'bytes=0-10' } })` concorrente com fila limitada.

- [ ] **Step 4: Executar testes de validação da interface**
  ```powershell
  python tests/test_admin_sentinel.py
  ```

---

### Task 6: Atualização de Cache Busters, Validação E2E e Deploy de Produção

**Files:**
- Modify: `scripts/update_cache_buster.py`
- Output: Deploy de produção Vercel

- [ ] **Step 1: Rodar a suíte completa de testes automatizados**
  ```powershell
  python tests/test_video_catalog.py
  python tests/test_url_replacement.py
  python tests/test_disk_purge.py
  python tests/test_sentinel_cli.py
  python tests/test_admin_sentinel.py
  ```

- [ ] **Step 2: Atualizar cache busters globais**
  ```powershell
  python scripts/update_cache_buster.py
  ```

- [ ] **Step 3: Teste manual de verificação**
  - Abrir `pages/produto-104.html` (referência canônica) e testar autoplay mudo do carrossel de vídeos com as novas URLs do Catbox.
  - Abrir `admin.html`, acessar a aba "Sentinel CDN", verificar renderização dos 141 vídeos e testar o modal de preview.

- [ ] **Step 4: Deploy de Produção na Vercel**
  ```powershell
  npx vercel --prod --yes
  ```
  - Confirmar que o deploy foi concluído com sucesso no alias de produção `https://stoneshopclone.vercel.app`.
