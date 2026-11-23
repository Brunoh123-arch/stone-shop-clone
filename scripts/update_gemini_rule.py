import os

content = """# Regra Global de Extração de Produtos TikTok Shop (Bruno CTO - Modo Zika Blindado)

> trigger: always_on quando o usuário enviar qualquer link do TikTok Shop (`https://shop.tiktok.com/...` ou `vt.tiktok.com/...`)
> Arquivo Mestre de Regras e Diretrizes do Fluxo: `c:\\Users\\Dell\\Downloads\\ds\\GEMINI.md`

Sempre que o usuário enviar um link de produto do TikTok Shop, execute o fluxo completo de forma 100% autônoma, sem pedir permissão e sem enrolação corporativa:

---

### Fluxo de Execução Obrigatório:

#### 1. Extração de Dados Oficiais via Playwright Headless & Sessão Logada:
- **REGRA INEGOCIÁVEL DE SESSÃO / CONTEXTO DE NAVEGAÇÃO (PROIBIDO NAVEGADOR DESLOGADO/INCÓGNITO)**:
  - O TikTok Shop impõe barreiras brutais anti-bot (Captcha UniSec / Slardar e telas de login forçado) em qualquer navegador deslogado, anônimo ou contexto 'limpo'.
  - Toda extração e navegação no TikTok Shop — seja pelo agente principal, scripts ou delegada a subagentes — **DEVE reutilizar estritamente o perfil persistente / sessão / cookies do navegador já logado** (usando a instância do Playwright MCP ativa ou storageState / perfil de usuário configurado).
  - **TERMINANTEMENTE PROIBIDO DISPARAR SUBAGENTES OU SCRIPTS EM NAVEGADOR VIRGEM SEM LOGIN**: Subagentes que abrem instâncias isoladas/sem perfil tomam login wall e captcha imediatamente, destruindo o fluxo de extração e gastando quota à toa. A sessão logada é patrimônio inegociável.
- Puxar o título completo e limpo do produto.
- Puxar o preço promocional, preço original (riscado) e desconto %.
- Puxar contagem real de vendidos (ex: `23.7K vendidos`) e nota média oficial (ex: `4.8`).
- Puxar a contagem oficial de avaliações globais (ex: `(5,7 mil)`).
- Puxar todas as variações (cores e tamanhos com fotos reais).
- Puxar todas as fotos oficiais da galeria em alta resolução (800x800).
- **Extração do Vídeo Oficial do Vendedor (`product_video`)**:
  - Puxar o vídeo demonstrativo do produto inserido na seção oficial de detalhes/descrição do TikTok Shop.
  - Baixar em alta definição para `video/produto-[ID]-demo.mp4`.
  - Extrair poster sincronizado via FFmpeg no frame `00:00:00.2` para `video/produto-[ID]-demo-poster.jpg`.
- **Extração da Tabela de Medidas Gráfica Oficial (`size_chart` / Guia de tamanhos)**:
  - No TikTok Shop, guias de medidas para vestuário e calçados são imagens gráficas oficiais enviadas pelos vendedores (`📐 Tabela de Medidas`).
  - Extrair e baixar a imagem original em alta resolução para `img/guia-tamanhos-[ID].png`.
  - **Fallback Gracioso Obrigatório**: Se o vendedor não disponibilizar imagem gráfica da tabela no anúncio, estruturar uma tabela de texto limpa com as medidas extraídas da descrição técnica.
- Puxar a descrição técnica oficial do vendedor.

#### 2. Extração de MÚLTIPLOS Vídeos de Criadores DIFERENTES (Zero Repetição de Rosto/Cena):
- **Descoberta Automatizada de Criadores Reais do TikTok via Playwright Google**:
  - Buscar no Google via Playwright: `site:tiktok.com "[NOME DO PRODUTO]"` ou termos-chave do nicho.
  - Capturar de 3 a 5 URLs diretas de criadores/afiliadas DIFERENTES testando o produto (pessoas diferentes, roupas diferentes, cenários caseiros distintos).
- **Download Limpo via TikWM API (Zero Marca d'Água do TikTok nos Vídeos)**:
  - Usar endpoint `https://www.tikwm.com/api/?url=<TIKTOK_URL>` para baixar o MP4 em alta definição sem marca d'água flutuante.
  - Baixar o avatar real de cada criador a partir de `data.author.avatar` e salvar em `img/creators-auto/avatar-<unique_id>.jpg`.
  - Capturar contagem de curtidas, comentários e compartilhamentos reais para dar verossimilhança máxima.
- **Posters 100% Sincronizados com o Frame Inicial**:
  - Gerar o poster de cada vídeo extraindo exatamente o frame de `00:00:00.2` do vídeo correspondente via FFmpeg:
    `ffmpeg -y -ss 00:00:00.2 -i "video.mp4" -vframes 1 -q:v 2 "poster.jpg"`
- **PROIBIDO GERAR VÍDEO FAKE COM FOTO TREMENDO / ZOOMPAN**: Usar SEMPRE gravações humanas reais.
- **PROIBIDO SETAS GRÁFICAS E TEXTOS DE MEME NAS THUMBNAILS**: Se o frame inicial de 0.2s contiver setas rosas, adesivos de meme ("POV:", "Achado...") ou textos queimados da edição de terceiros, extraia um frame de corte limpo de unboxing/teste real para o poster.

#### 3. Avaliações dos Clientes com Paridade Oficial TikTok Shop:
- **REGRA DE OURO: ESTRITAMENTE AVALIAÇÕES COM MÍDIAS REAIS DO PRODUTO (ZERO COMENTÁRIOS SEM FOTOS QUE SOAM FAKES)**:
  - Toda avaliação exibida na loja DEVE conter fotos e/ou vídeos REAIS e autênticos do produto comprado, postados por compradores legítimos no TikTok Shop.
  - É TERMINANTEMENTE PROIBIDO inventar, forjar ou injetar avaliações apenas de texto (text-only sem foto) para inflar a lista. Avaliações sem mídia soam artificiais e destroem a credibilidade e a taxa de conversão da loja.
  - Se apenas 3 compradores postaram fotos/vídeos reais do produto no anúncio, a vitrine e o modal de avaliações completas devem exibir ESTRITAMENTE essas 3 avaliações legítimas.
- **Estratégia Obrigatória de Expansão Multi-PDP (Varredura de Anúncios Irmãos via Playwright)**:
  - Quando um anúncio do TikTok Shop tiver poucas avaliações na primeira página ou quando a paginação ('Próximo') for bloqueada por Captcha anti-bot da Bytedance (UniSec Slardar / api-verification.tiktokshop.com), o agente DEVE navegar automaticamente pelas páginas irmãs (/pdp/...) da mesma loja oficial do vendedor no TikTok Shop que comercializam o mesmo produto ou variações dele.
  - Extrair de forma agregada todas as compras verificadas ('Compras verificadas') que contêm fotos e/ou vídeos reais do produto comprado.
  - Baixar TODAS as fotos em alta resolução (800x800) para `img/review-[ID]-c[N]-[M].jpg` usando o sufixo oficial `~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg`.
  - Baixar os avatares das compradoras para `img/reviews-avatars/review-user-[ID]-c[N].jpg` imediatamente enquanto a assinatura da CDN (x-signature / x-expires) estiver ativa, blindando contra expiração de links e ícones de imagem quebrada.
- **Sincronização Absoluta de Métricas e Contagens (Zero Clones e Zero Preenchimento Fake)**:
  - O modal de avaliações completas renderiza ESTRITAMENTE as avaliações autênticas existentes com mídias reais.
  - A contagem de avaliações DEVE bater com a nota oficial e contagem real da vitrine:
    - **Topo da Vitrine** (`.ratings-row`): `⭐ 4.8 (X,X mil) | XX.XK vendidos`.
    - **Título da Seção de Avaliações**: `Avaliações dos clientes (N)`.
- **Avatares Reais dos Compradores (Zero Boneco Cinza e Zero Logotipo de Empresa)**:
  - Baixar os avatares reais de compradores pessoas físicas para `img/reviews-avatars/` ou usar o pool local de pessoas reais brasileiras (`REAL_AVATAR_POOL`).
  - **PROIBIDO LOGOTIPOS DE EMPRESAS/AGÊNCIAS EM AVATARES DE COMPRADOR**: O comprador é sempre pessoa física real.
  - **PROIBIDO HOTLINKING DIRETO DE URLs ASSINADAS DO TIKTOK CDN (`p16-common-sign.tiktokcdn.com`)**: Links com `x-signature` expiram rapidamente; salve tudo localmente.
- **Card Compacto na Vitrine (Página do Produto)**:
  - Avatar 32x32 com foto real da compradora à esquerda.
  - Linha única horizontal: `★★★★★ · [VARIAÇÃO] [Atributo contextual...]` truncado com reticências.
  - Comentário oficial com tipografia limpa logo abaixo.
  - Bloco 70x70 com bordas arredondadas na extrema direita: miniatura da primeira foto com badge numérico `+N` (ex: `+5`). Ao clicar, abre o modal de fotos em tela cheia com todas as fotos legítimas daquela cliente.

#### 4. Carrossel "Vídeos de Criadores" Dinâmico & Precedência no `videos-criadores.js`:
- **Precedência Absoluta e Isolamento Estrito de Condicionais**:
  - Produtos com termos compostos ou palavras coincidentes NUNCA podem ser capturados por condicionais genéricas de palavras soltas.
  - A condicional do produto específico DEVE vir no topo absoluto do encadeamento `if/else`, e a condicional genérica DEVE conter negação explícita.
- **Declaração Canônica no HTML (Zero Injeção Estática Corrupta)**:
  - No HTML da página do produto (`produto-[ID].html`), declare estritamente uma única linha limpa:
    ```html
    <!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP -->
    <div id="creators-section" class="creators-section"></div>
    ```
  - É **TERMINANTEMENTE PROIBIDO** injetar HTML estático com cards hardcoded dentro do HTML da página. O script `videos-criadores.js` é o ÚNICO responsável por instanciar os cards e carrossel dinamicamente em tempo de execução.
- **Dataset Dinâmico Completo**:
  - Título canônico: `Vídeos de criadores (30+)` (ou badge de contagem real).
  - Criadores 100% únicos com handles verossímeis do nicho.
  - Player TikTok modal interativo com curtida, comentário contextual, favoritos e compartilhamento.

#### 5. Formatação Padronizada da Página & Integridade Estrutural do DOM (`Final Depth: 0`):
- **PROIBIÇÃO ABSOLUTA DE CONTAMINAÇÃO CRUZADA DE TEMPLATE (ZERO TEMPLATE BLEED / STATE LEAK)**:
  - Toda página nova deve ter paridade 1:1 rigorosa: `<title>` == `<h1 class="product-title">` == `PRODUTO_ATUAL.nome`.
  - `.description-section`, `PRODUTO_ATUAL.id`, `#creators-section` e detalhes técnicos devem pertencer unicamente ao produto atual.
- Criar `pages/produto-[ID].html` no próximo ID sequencial.
- **Hierarquia Inegociável do DOM (Padrão Oficial TikTok Shop)**:
  ```html
  <div class="app-container">
    <div class="header-search-wrapper">...</div>
    <div class="page-content">
      <!-- 1. Carrossel de Fotos com Contador de Tamanho -->
      <div class="image-slider">
        <div class="slider-track">...</div>
        <div class="slider-counter">1 / 9 Tamanho</div>
      </div>
      <div class="slider-dots"></div>

      <!-- 2. Abas Fixas de Navegação -->
      <nav class="product-tabs">
        <button class="product-tab active" data-tab="visao-geral">Visão geral</button>
        <button class="product-tab" data-tab="avaliacoes">Avaliações</button>
        <button class="product-tab" data-tab="descricao">Descrição</button>
        <button class="product-tab" data-tab="recomendacoes">Recomendações</button>
      </nav>

      <!-- 3. Barra de Preço Promocional TikTok Shop (Rosa Suave / Flash Sale) -->
      <div class="price-section-tt">
        <div class="price-tt-left">
          <div class="price-tt-main">
            <span class="badge-discount-tt">-75%</span>
            <span class="price-tt-current">A partir de R$ 14,90 <svg class="voucher-outline-icon">...</svg></span>
          </div>
          <span class="price-tt-strikethrough">R$ 59,90</span>
        </div>
        <div class="price-tt-right">
          <span class="price-tt-audience">Apenas para novos clientes</span>
          <div class="price-tt-timer">Termina em <strong>12:23:04</strong></div>
        </div>
      </div>

      <!-- 4. Informações do Produto -->
      <div class="product-info">
        <!-- Parcelamento com Desconto de Juros -->
        <div class="installment-row">2x R$ 8,17, com desconto de 34% de juros ></div>

        <!-- Cupom / Desconto Oficial -->
        <div class="discount-ticket">Desconto de 60%, máximo de R$ 20 ></div>

        <!-- Título com Marcador/Bookmark -->
        <div class="product-title-row">
          <h1 class="product-title">Nome do Produto</h1>
          <button class="bookmark-btn">...</button>
        </div>

        <!-- Avaliações e Vendidos -->
        <div class="ratings-row">
          ★ 4.8 (5,7 mil) | 23.7K vendidos
        </div>

        <!-- Linhas de Informações Oficiais -->
        <div class="product-info-rows">
          <!-- Frete Grátis com Valor Riscado e Estimativa -->
          <div class="info-row-item info-row-frete">
            Frete grátis R$ 5,53 (riscado) >
            Receba até sex., 13 de nov – seg., 16 de nov
          </div>

          <!-- Opções Disponíveis com Miniaturas -->
          <div class="info-row-item info-row-opcoes">
            [Grade] [Thumbs] 3 opções disponíveis >
          </div>

          <!-- Proteção do Cliente (Grid 2x2) -->
          <div class="info-row-item-protection">
            Proteção do cliente >
            ✓ Devolução gratuita   ✓ Garantia de pontualidade
            ✓ Pagamento seguro     ✓ Reembolso se algo der errado
          </div>

          <!-- Ofertas Oficial com Card de Cupom -->
          <div class="ofertas-section-tt">
            Ofertas >
            [Voucher Card]: [Envio] R$ 20 de desconto em pedidos acima de R$ 12 [Resgatar]
          </div>
        </div><!-- fim product-info-rows -->

        <!-- Carrossel de Vídeos de Criadores -->
        <div id="creators-section" class="creators-section"></div>

        <!-- Avaliações dos Clientes -->
        <div class="reviews-section">...</div>

        <!-- SEÇÃO: SOBRE ESTE PRODUTO (VÍDEO + GUIA DE TAMANHOS + DESCRIÇÃO EXPANSÍVEL) -->
        <div class="about-product-section" id="sobre-este-produto">
          <h3 class="about-product-title">Sobre este produto</h3>

          <!-- Subseção Vídeo Oficial TikTok Shop com Player Scrubber -->
          <div class="tt-video-wrapper">
            <h4 class="tt-sub-title">Vídeo</h4>
            <div class="tiktok-video-card" onclick="togglePlayProductVideo(this)">
              <video src="../video/produto-[ID]-demo.mp4" poster="../video/produto-[ID]-demo-poster.jpg" playsinline preload="metadata"></video>
              <div class="tt-video-play-overlay">▶</div>
              <div class="tt-video-bar">
                <span class="tt-video-play-btn">▶</span>
                <span class="tt-video-time tt-cur-time">00:00</span>
                <div class="tt-video-track"><div class="tt-video-prog"></div></div>
                <span class="tt-video-time tt-dur-time">0:19</span>
                <span class="tt-video-fullscreen-btn">[ ]</span>
              </div>
            </div>
          </div>

          <!-- Subseção Guia de Tamanhos (Imagem Gráfica Oficial do Vendedor ou Tabela Fallback) -->
          <div class="tt-size-guide-wrapper">
            <h4 class="tt-sub-title">Guia de tamanhos</h4>
            <div class="tt-size-guide-card">
              <img src="../img/guia-tamanhos-[ID].png" alt="Guia de tamanhos" class="tt-size-guide-img">
            </div>
            <!-- Botão Centralizado Ver Mais -->
            <button id="btn-toggle-ver-mais" class="btn-toggle-centered" onclick="window.toggleSobreProdutoDescricao(true)">
              Ver mais ∨
            </button>
          </div>
        </div><!-- fim about-product-section -->

        <!-- Subseção Descrição Técnica (Inicialmente Recolhida display:none) -->
        <div class="description-section" id="sobre-produto-desc-section" style="display: none !important;">
          <h4 class="tt-sub-title">Descrição</h4>
          <div class="description-content">
            <!-- Tópicos objetivos e especificações do produto -->
          </div>
          <!-- Botão Centralizado Ver Menos -->
          <button id="btn-toggle-ver-menos" class="btn-toggle-centered" onclick="window.toggleSobreProdutoDescricao(false)" style="display: none;">
            Ver menos ⌃
          </button>
        </div><!-- fim description-section -->

        <!-- Divisor Grosso de Seção Oficial TikTok Shop -->
        <div class="tt-section-divider-thick"></div>

        <!-- Recomendações / Você também pode gostar -->
        <div class="related-section">...</div>
      </div><!-- fim product-info -->
    </div><!-- fim page-content -->

    <!-- Barra Inferior Fixa -->
    <div class="bottom-bar">
      <!-- Loja, Chat, Carrinho e Botão de Compra com Preço Oficial e Legenda -->
      <button class="btn-buy" onclick="handleBuyNow()">
        <span class="btn-line1">R$ 14,90</span>
        <span class="btn-line2">Apenas para novos clientes</span>
      </button>
    </div>
  </div><!-- fim app-container -->
  ```
- **Validação de Fechamento de Tags**:
  - Toda edição em arquivo HTML DEVE ser auditada via script para garantir profundidade de tags (tag depth) final rigorosamente igual a 0. `reviews-section`, `about-product-section`, `description-section` e `related-section` pertencem OBRIGATORIAMENTE dentro de `.product-info` e `.page-content`.

#### 6. Registro no Catálogo, Vitrine, Cache Buster e Deploy:
- Registrar no topo de `js/catalogo.js` com o novo ID e métricas reais.
- Adicionar o card na grade `#recommended-grid` de `index.html`.
- Atualizar cache buster global (`style.css?v=ts`, `app.js?v=ts`, `videos-criadores.js?v=ts`, `catalogo.js?v=ts`) em todas as páginas HTML via `scripts/update_cache_buster.py`.
- Sincronizar todas as pastas e arquivos para `C:\\Users\\Dell\\Downloads\\stone_shop_clone` via `scripts/sync_to_clone.py`.
- Executar `npx vercel --prod --yes` em `C:\\Users\\Dell\\Downloads\\stone_shop_clone` e vincular o alias oficial:
  `npx vercel alias set <deploy-url> stoneshopclone.vercel.app`.
- **PROIBIDO ENVIAR URL LOCALHOST**: O link de entrega ao usuário deve ser sempre a URL HTTPS de produção `https://stoneshopclone.vercel.app/...`.

#### 7. Checkout & Resumo Blindado (Zero R$ 0,00 e Zero Resumo Vazio):
- **Redirecionamento com Query Params Robustos**: Toda ação de compra rápida via `irDiretoAoCheckoutComProduto` grava no `localStorage` ('famosinhos_checkout_cart') E repassa explicitamente os parâmetros via URL (`pages/resumo.html?produto=ID&preco=X.XX&qty=N&var=LABEL&img=PATH`).
- **Resumo Multi-Tier Fallback no getCart()**:
  1. `localStorage.getItem('famosinhos_checkout_cart')`
  2. `sessionStorage.getItem('famosinhos_checkout_cart')`
  3. `URLSearchParams` (reconstrói item instantaneamente a partir da URL)
  4. `localStorage.getItem('famosinhos_cart')`
  5. Fallback produto catálogo.
- **Auto-Seleção de Opção Única no Modal de Variações**: Se um grupo de variação contiver apenas 1 opção, essa opção DEVE ser auto-selecionada no momento em que o modal abre.

#### 8. Extração e Engenharia Reversa de Concorrentes via Meta Ads Library (Facebook Ads):
- Varredura de anúncios mais escalados via Playwright Headless.
- Download direto de vídeos MP4 e imagens em alta resolução dos servidores de mídia oficiais.
- Desmascaramento de URLs de destino limpas.
- Criação e deploy automático do produto no padrão Stone Shop oficial.
"""

with open('c:/Users/Dell/Downloads/ds/GEMINI.md', 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated ds/GEMINI.md successfully')

clone_path = 'c:/Users/Dell/Downloads/stone_shop_clone/GEMINI.md'
if os.path.exists('c:/Users/Dell/Downloads/stone_shop_clone'):
    with open(clone_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated stone_shop_clone/GEMINI.md successfully')
