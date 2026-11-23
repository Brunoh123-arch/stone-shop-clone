import os

os.makedirs('templates/components', exist_ok=True)

with open('templates/produto-canonical-template.html', 'r', encoding='utf-8') as f:
    full_template = f.read()

# Let's define the components cleanly

# 1. head.html
c_head = '''<head>
  <script src="/js/anti-clone-guard.js?v=20261020"></script>
  <!-- TikTok Pixel Base Code -->
  <script>
  !function(w,d,t){w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=['page','track','identify','instances','debug','on','off','once','ready','alias','group','enableCookie','disableCookie','holdConsent','revokeConsent','grantConsent'],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var r='https://analytics.tiktok.com/i18n/pixel/events.js',o=n&&n.partner;ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=r,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};var s=d.createElement('script');s.type='text/javascript',s.async=!0,s.src=r+'?sdkid='+e+'&lib='+t;var a=d.getElementsByTagName('script')[0];a.parentNode.insertBefore(s,a)},ttq.load('DBD7ASBC77UF91061F1G'),ttq.page()}(window,document,'ttq');
  </script>
  <script src="../js/tiktok-events.js"></script>
  <!-- End TikTok Pixel Base Code -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
  <title>{{TITLE}}</title>
  <meta name="description" content="{{DESCRIPTION_META}}">
  <link rel="stylesheet" href="../css/style.css?v=1794709455554">
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="shortcut icon" type="image/x-icon" href="../favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
  <link rel="preload" as="image" href="{{PRELOAD_IMAGE}}" fetchpriority="high">
  <link rel="preload" as="image" href="../decalque/decalque-oferta.jpg?v=1111" fetchpriority="high">
  <!-- Google Fonts: Plus Jakarta Sans & Inter (Oficial TikTok Parity) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
</head>'''

# 2. loader.html
c_loader = '''  <!-- CRITICAL TIKTOK SPINNER -->
  <div id="tt-instant-loader" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:#fff;z-index:99999999;display:flex;align-items:center;justify-content:center;transition:opacity 0.08s ease,visibility 0.08s ease;pointer-events:none;">
    <div style="position:relative;width:42px;height:42px;">
      <div style="position:absolute;width:18px;height:18px;border-radius:50%;background:#00f2fe;left:2px;top:12px;animation:tt-bounce-cyan 0.7s infinite ease-in-out alternate;mix-blend-mode:multiply;"></div>
      <div style="position:absolute;width:18px;height:18px;border-radius:50%;background:#fe2c55;right:2px;top:12px;animation:tt-bounce-red 0.7s infinite ease-in-out alternate;mix-blend-mode:multiply;"></div>
    </div>
  </div>
  <style>
    @keyframes tt-bounce-cyan{0%{transform:translateX(0) scale(0.9);z-index:2;}100%{transform:translateX(18px) scale(1.15);z-index:1;}}
    @keyframes tt-bounce-red{0%{transform:translateX(0) scale(1.15);z-index:1;}100%{transform:translateX(-18px) scale(0.9);z-index:2;}}
  </style>
  <script>
    (function(){
      var l=document.getElementById('tt-instant-loader');
      function hide(){
        if(!l)return;
        l.style.opacity='0';
        l.style.visibility='hidden';
        setTimeout(function(){if(l&&l.parentNode)l.parentNode.removeChild(l);},100);
      }
      if(document.readyState==='complete'||document.readyState==='interactive'){
        setTimeout(hide, 40);
      }else{
        document.addEventListener('DOMContentLoaded', hide);
        window.addEventListener('load', hide);
        setTimeout(hide, 150);
      }
    })();
  </script>'''

# 3. header.html
c_header = '''  <!-- HEADER OFICIAL TIKTOK SHOP (CANÔNICO PRODUTO-104) -->
  <header class="header">
    <div class="header-left">
      <button class="header-btn" onclick="history.back()" aria-label="Voltar">
        <svg viewBox="0 0 24 24" class="header-icon" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>
    </div>
    <div class="header-right">
      <button class="header-btn" aria-label="Compartilhar" onclick="if(navigator.share){navigator.share({title:document.title,url:location.href})}else{navigator.clipboard.writeText(location.href);alert('Link copiado!')}">
        <svg viewBox="0 0 24 24" class="header-icon" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="18" cy="5" r="3"></circle>
          <circle cx="6" cy="12" r="3"></circle>
          <circle cx="18" cy="19" r="3"></circle>
          <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
          <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
        </svg>
      </button>
      <button class="header-btn cart-btn" onclick="window.location.href='../resumo.html'" aria-label="Carrinho">
        <svg viewBox="0 0 24 24" class="header-icon" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
        <span class="cart-badge" id="cart-badge">0</span>
      </button>
    </div>
  </header>'''

# 4. slider.html
c_slider = '''    <!-- SLIDER DE IMAGENS -->
    <div class="image-slider">
      <img src="../decalque/decalque-oferta.jpg?v=1111" alt="Oferta Especial" class="slider-decalque" fetchpriority="high">
      <div class="slider-images" id="slider-images">
        {{SLIDER_IMAGES}}
      </div>
      <div class="slider-counter" id="slider-counter">{{SLIDER_COUNTER}}</div>
    </div>'''

# 5. tabs.html
c_tabs = '''    <!-- ABAS DE NAVEGAÇÃO -->
    <nav class="product-tabs">
      <a href="#visao-geral" class="tab-item active">Visão geral</a>
      <a href="#avaliacoes-secao" class="tab-item">Avaliações</a>
      <a href="#sobre-este-produto" class="tab-item">Descrição</a>
      <a href="#recomendacoes" class="tab-item">Recomendações</a>
    </nav>'''

# 6. pricing.html
c_pricing = '''    <!-- SEÇÃO DE PREÇO / OFERTA RELÂMPAGO -->
    <div class="price-section" id="visao-geral">
      <div class="price-top">
        <div class="price-left">
          <div class="price-row">
            <span class="price-currency">R$</span>
            <span class="price-current-int">{{PRICE_CURRENT_INT}}</span>
            <span class="price-current-cents">{{PRICE_CURRENT_CENTS}}</span>
            <span class="discount-badge">{{DISCOUNT_PERCENT}}</span>
          </div>
          <div class="price-original-row">
            <span class="price-original-text">De </span>
            <span class="price-original">{{PRICE_ORIGINAL}}</span>
          </div>
        </div>
      </div>
      <div class="bonus-discount-tag" id="bonus-discount-tag">
        <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="bonus-tag-icon"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
        <span>Desconto de R$ 10,00 aplicado</span>
      </div>
    </div>'''

# 7. product_info.html
c_prod_info = '''    <!-- INFORMAÇÕES DO PRODUTO -->
    <div class="product-info">
      <!-- 1. Parcelamento oficial TikTok Shop -->
      <div class="installment-block">
        <span class="installment-text">{{INSTALLMENT_TEXT}}</span>
      </div>

      <!-- 2. Cupons oficiais TikTok Shop -->
      <div class="voucher-discount-block">
        <div class="voucher-ticket">
          <span class="voucher-badge-text">{{DISCOUNT_BADGE_TICKET}}</span>
          <span class="voucher-desc">Cupom da Loja Aplicado</span>
        </div>
      </div>

      <!-- Título com Bookmark à direita -->
      <div class="product-title-row">
        <h1 class="product-title">{{PRODUCT_TITLE}}</h1>
        <button class="bookmark-btn" onclick="toggleBookmark(this)" aria-label="Favoritar">
          <svg viewBox="0 0 24 24" class="bookmark-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      </div>

      <!-- Avaliações e Vendas -->
      <div class="rating-sold-row">
        <div class="rating-pill">
          <span class="rating-star">★</span>
          <span class="rating-score">{{RATING_AVG}}</span>
          <span class="rating-count">({{RATING_COUNT}})</span>
        </div>
        <div class="sold-pill">
          <span class="sold-count">{{SOLD_COUNT}}</span>
        </div>
      </div>

      <!-- BLOCO PRÉ-DESCRIÇÃO OFICIAL TIKTOK SHOP -->
      <div class="product-pre-desc-block">
        <!-- Linha 1: Frete Grátis -->
        <div class="pre-desc-row shipping-row">
          <div class="pre-desc-left">
            <span class="pre-desc-label">Envio</span>
            <div class="pre-desc-content">
              <div class="shipping-lead">
                <span class="shipping-tag-free">Frete Grátis</span>
                <span class="shipping-estimate">Receba em 4 a 7 dias úteis</span>
              </div>
            </div>
          </div>
          <div class="pre-desc-arrow">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </div>

        <!-- Linha 2: Proteção do Cliente -->
        <div class="pre-desc-row protection-row" onclick="openProtectionModal()">
          <div class="pre-desc-left">
            <span class="pre-desc-label">Serviço</span>
            <div class="pre-desc-content">
              <div class="protection-pills-flow">
                <span class="protection-pill-item">
                  <svg viewBox="0 0 24 24" width="12" height="12" fill="#00b67a"><path d="M12 2L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-3zm-2 16l-4-4 1.41-1.41L10 15.17l6.59-6.59L18 10l-8 8z"/></svg>
                  Garantia Stone Shop
                </span>
                <span class="protection-pill-item">
                  <svg viewBox="0 0 24 24" width="12" height="12" fill="#00b67a"><path d="M12 2L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-3zm-2 16l-4-4 1.41-1.41L10 15.17l6.59-6.59L18 10l-8 8z"/></svg>
                  Devolução em 7 dias
                </span>
                <span class="protection-pill-item">
                  <svg viewBox="0 0 24 24" width="12" height="12" fill="#00b67a"><path d="M12 2L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-3zm-2 16l-4-4 1.41-1.41L10 15.17l6.59-6.59L18 10l-8 8z"/></svg>
                  Reembolso Rápido
                </span>
              </div>
            </div>
          </div>
          <div class="pre-desc-arrow">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </div>
      </div>

      <!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP -->
      <div class="creators-section" id="creators-section"></div>

      <!-- AVALIAÇÕES DOS CLIENTES -->
      <div class="reviews-section" id="avaliacoes-secao">
        <div class="reviews-header-row">
          <h2 class="reviews-title">Avaliações de clientes ({{RATING_COUNT}})</h2>
          <div class="reviews-rating-badge">
            <span class="reviews-score-num">{{RATING_AVG}}</span>
            <span class="reviews-score-star">★</span>
            <span class="reviews-score-max">/5</span>
          </div>
        </div>
        <div class="reviews-filter-pills">
          <span class="rev-pill active">Todas</span>
          <span class="rev-pill">Com fotos (48)</span>
          <span class="rev-pill">Entrega rápida</span>
          <span class="rev-pill">Qualidade excelente</span>
        </div>
        <div class="reviews-list">
          {{REVIEWS_BLOCK}}
        </div>
      </div>
    </div>'''

# 8. description.html
c_description = '''    <!-- SEÇÃO OFICIAL: SOBRE ESTE PRODUTO -->
    <div class="about-product-section" id="sobre-este-produto">
      <h2 class="about-section-title">Sobre este produto</h2>

      <!-- SUBSEÇÃO 1: DETALHES (PARIDADE OFICIAL TIKTOK SHOP - SEM TABELA HTML) -->
      <div class="product-details-block">
        <h3 class="about-subtitle">Detalhes</h3>
        <div class="details-attributes-grid">
          {{DETALHES_GRID}}
        </div>
        <button class="details-toggle-btn" onclick="toggleProductDetails(this)">
          <span>Ver mais</span>
          <svg viewBox="0 0 24 24" class="toggle-arrow" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </button>
      </div>

      <!-- SUBSEÇÃO 2: VÍDEO OFICIAL TIKTOK SHOP -->
      {{PRODUCT_VIDEO_BLOCK}}

      <!-- SUBSEÇÃO 3: DESCRIÇÃO OFICIAL TIKTOK SHOP -->
      <div class="description-section" id="sobre-produto-desc-section">
        <h3 class="about-subtitle">Descrição</h3>
        <div class="desc-expandable-wrapper" id="desc-expandable-container">
          <div class="desc-content-inner">
            {{DESCRICAO_HTML}}
          </div>
          <div class="desc-fade-overlay" id="desc-fade-overlay"></div>
        </div>
        <button class="desc-toggle-expand-btn" id="btn-toggle-desc" onclick="toggleDescricaoCompleta()">
          <span id="btn-toggle-desc-text">Ver mais</span>
          <svg viewBox="0 0 24 24" class="desc-toggle-arrow" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
      </div>
    </div>'''

# 9. bottom_bar.html
c_bottom_bar = '''  <!-- BOTTOM BAR OFICIAL TIKTOK SHOP (CANÔNICA PRODUTO 104) -->
  <div class="bottom-bar">
    <div class="bottom-actions-left">
      <button class="bottom-action-btn" onclick="window.location.href='../loja.html'" aria-label="Loja">
        <svg viewBox="0 0 24 24" class="bottom-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        <span class="bottom-action-label">Loja</span>
      </button>
      <button class="bottom-action-btn" onclick="alert('Suporte Stone Shop disponível 24h via WhatsApp')" aria-label="Chat">
        <svg viewBox="0 0 24 24" class="bottom-icon" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
        <span class="bottom-action-label">Chat</span>
      </button>
    </div>
    <div class="bottom-actions-right">
      <button class="bottom-btn btn-cart" onclick="addToCart(PRODUTO_ATUAL)">Adicionar</button>
      <button class="bottom-btn btn-buy" onclick="handleBuyNow()">
        <span class="buy-label">Compre agora</span>
        <span class="buy-price" id="btn-buy-price">{{BTN_BUY_PRICE}}</span>
      </button>
    </div>
  </div>'''

# 10. modals.html
c_modals = '''  <!-- MODAL PROTEÇÃO DO CLIENTE -->
  <div id="protection-modal" class="tt-modal-backdrop" onclick="closeProtectionModal(event)">
    <div class="tt-modal-sheet" onclick="event.stopPropagation()">
      <div class="tt-modal-header">
        <h3 class="tt-modal-title">Proteção do Cliente</h3>
        <button class="tt-modal-close" onclick="closeProtectionModal()">&times;</button>
      </div>
      <div class="tt-modal-body">
        <div class="protection-feature-item">
          <div class="prot-icon">🛡️</div>
          <div class="prot-text">
            <strong>Garantia Stone Shop Oficial</strong>
            <p>Seu pagamento fica 100% retido e protegido até você receber o produto e confirmar que está tudo perfeito.</p>
          </div>
        </div>
        <div class="protection-feature-item">
          <div class="prot-icon">📦</div>
          <div class="prot-text">
            <strong>Devolução sem complicações</strong>
            <p>Até 7 dias após o recebimento para solicitar troca ou devolução gratuita direto pelo site.</p>
          </div>
        </div>
        <div class="protection-feature-item">
          <div class="prot-icon">⚡</div>
          <div class="prot-text">
            <strong>Reembolso Rápido via Pix</strong>
            <p>Estorno instantâneo para pagamentos feitos no Pix se houver qualquer divergência no pedido.</p>
          </div>
        </div>
      </div>
      <button class="tt-modal-confirm-btn" onclick="closeProtectionModal()">Entendido</button>
    </div>
  </div>

  <!-- MODAL DE ZOOM DE FOTOS DE AVALIAÇÃO -->
  <div id="review-modal" class="tt-modal-backdrop" onclick="closeReviewModal(event)" style="display:none;background:rgba(0,0,0,0.9);z-index:999999;">
    <div style="position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center;">
      <button onclick="closeReviewModal()" style="position:absolute;top:20px;right:20px;background:none;border:none;color:#fff;font-size:32px;cursor:pointer;z-index:10;">&times;</button>
      <img id="review-modal-img" src="" alt="Foto expandida da avaliação" style="max-width:90%;max-height:85vh;object-fit:contain;border-radius:8px;">
    </div>
  </div>'''

# 11. scripts.html
c_scripts = '''  <!-- SCRIPTS GLOBAIS -->
  <script>
    const PRODUTO_ATUAL = {{PRODUTO_ATUAL_JS}};
    window.PRODUTO_ATUAL = PRODUTO_ATUAL;

    function handleBuyNow() {
      if (typeof handleAddToCartWithVariacoes === 'function' && typeof PRODUTO_ATUAL !== 'undefined') {
        handleAddToCartWithVariacoes(PRODUTO_ATUAL, true);
      } else if (typeof irDiretoAoCheckoutComProduto === 'function' && typeof PRODUTO_ATUAL !== 'undefined') {
        irDiretoAoCheckoutComProduto(PRODUTO_ATUAL, '', 1);
      } else {
        if (typeof PRODUTO_ATUAL !== 'undefined') addToCart(PRODUTO_ATUAL);
        window.location.href = '../resumo.html';
      }
    }

    function toggleBookmark(btn) {
      const svg = btn.querySelector('svg');
      if (svg.getAttribute('fill') === 'currentColor') {
        svg.setAttribute('fill', 'none');
      } else {
        svg.setAttribute('fill', 'currentColor');
      }
    }

    function openProtectionModal() {
      const m = document.getElementById('protection-modal');
      if (m) m.classList.add('is-active');
    }
    function closeProtectionModal(e) {
      if (e && e.target !== e.currentTarget && !e.target.classList.contains('tt-modal-close') && !e.target.classList.contains('tt-modal-confirm-btn')) return;
      const m = document.getElementById('protection-modal');
      if (m) m.classList.remove('is-active');
    }

    function openReviewModal(src) {
      const m = document.getElementById('review-modal');
      const img = document.getElementById('review-modal-img');
      if (m && img) {
        img.src = src;
        m.style.display = 'flex';
      }
    }
    function closeReviewModal(e) {
      const m = document.getElementById('review-modal');
      if (m) m.style.display = 'none';
    }

    window.toggleDescricaoCompleta = function() {
      var container = document.getElementById('desc-expandable-container');
      var btn = document.getElementById('btn-toggle-desc');
      var text = document.getElementById('btn-toggle-desc-text');
      if (!container || !btn) return;

      var isExpanded = container.classList.contains('is-expanded');
      if (isExpanded) {
        container.classList.remove('is-expanded');
        btn.classList.remove('is-expanded');
        if (text) text.textContent = 'Ver mais';
      } else {
        container.classList.add('is-expanded');
        btn.classList.add('is-expanded');
        if (text) text.textContent = 'Ver menos';
      }
    };

    window.toggleProductDetails = function(btn) {
      var hiddenRows = document.querySelectorAll('.details-attributes-grid .toggleable-row');
      var span = btn.querySelector('span');
      var isExpanding = false;
      hiddenRows.forEach(function(row) {
        if (row.classList.contains('is-hidden')) {
          row.classList.remove('is-hidden');
          row.style.setProperty('display', 'flex', 'important');
          isExpanding = true;
        } else {
          row.classList.add('is-hidden');
          row.style.setProperty('display', 'none', 'important');
        }
      });
      if (span) {
        span.innerText = isExpanding ? 'Ver menos' : 'Ver mais';
      }
    };
  </script>
  <script src="/tracker.js"></script>
  <script src="../js/app.js?v=20261121_app_v1"></script>
  <script src="../js/videos-criadores-v3.js?v=20261121_prod_v3"></script>'''

components = {
    'head.html': c_head,
    'loader.html': c_loader,
    'header.html': c_header,
    'slider.html': c_slider,
    'tabs.html': c_tabs,
    'pricing.html': c_pricing,
    'product_info.html': c_prod_info,
    'description.html': c_description,
    'bottom_bar.html': c_bottom_bar,
    'modals.html': c_modals,
    'scripts.html': c_scripts
}

for filename, content in components.items():
    path = os.path.join('templates', 'components', filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created component: {path}")

# Now assemble master template: templates/produto.template.html
master_template = '''<!DOCTYPE html>
<html lang="pt-BR">
<!-- @include "components/head.html" -->
<body>
<!-- @include "components/loader.html" -->
  <div class="app-container">
<!-- @include "components/header.html" -->
    <div class="page-content">
<!-- @include "components/slider.html" -->
<!-- @include "components/tabs.html" -->
<!-- @include "components/pricing.html" -->
<!-- @include "components/product_info.html" -->
<!-- @include "components/description.html" -->
    </div>
  </div>
<!-- @include "components/bottom_bar.html" -->
<!-- @include "components/modals.html" -->
<!-- @include "components/scripts.html" -->
</body>
</html>'''

with open('templates/produto.template.html', 'w', encoding='utf-8') as f:
    f.write(master_template)

print("Master template assembled at templates/produto.template.html!")
