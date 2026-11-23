import re

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<script src="/js/anti-clone-guard.js?v=20261020"></script>
<!-- TikTok Pixel Base Code -->
<script>
!function(w,d,t){w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=['page','track','identify','instances','debug','on','off','once','ready','alias','group','enableCookie','disableCookie','holdConsent','revokeConsent','grantConsent'],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var r='https://analytics.tiktok.com/i18n/pixel/events.js',o=n&&n.partner;ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=r,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};var s=d.createElement('script');s.type='text/javascript',s.async=!0,s.src=r+'?sdkid='+e+'&lib='+t;var a=d.getElementsByTagName('script')[0];a.parentNode.insertBefore(s,a)},ttq.load('DBD7ASBC77UF91061F1G'),ttq.page()}(window,document,'ttq');
</script>
<script src="../js/tiktok-events.js"></script>
<!-- End TikTok Pixel Base Code -->
<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
  <title>Piscina Splash Fun Redonda Inflável 2400 Litros - Mor - Stone Shop</title>
  <meta name="description" content="Piscina Splash Fun Redonda Inflável 2400 Litros - Mor com 78% OFF. Apenas R$89,90. Frete grátis e lona reforçada de 3 camadas.">
  <link rel="stylesheet" href="../css/style.css?v=1794434281002">
  <!-- TikTok Shop Oficial Favicon -->
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="shortcut icon" type="image/x-icon" href="../favicon.ico">
  <link rel="icon" type="image/png" sizes="32x32" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAAAAAAAAAQCEeRdzAAAFZUlEQVR4nKWXbWwURRjHf7O7d30vxRZaihUIBD+0JCo2pkIBwQBVEmNLMRFikwZCgPClBjTEoOAHoJKgEcKbQVtoQAIUiyKEBEhVAthwRRQiBRG19IW3chRK6e2Ome21XLfX3l35J3t7u/vM/P/PMzPPPCOIAAKhbikSORp4LuCTCVwTiL/dLvddn8+HKdWr0DDC5H4GyJfIAuAlYGgQG0simzvMjhqJ3A38ANx7WgFuoARYCqQ7vknHswakWZY1C1DXv0ApsNkfoYgFjAN2AC/3QeiE83sG8CXwjqZrxVLKOmnJ0AJ0Q8c0zbeQlAGDwiAOJWiiZVo/ISjSdO2oZVr9CBAo8llIvgWiQpELoRGf8az9/7HXS3tLS19CUpFUWpb1tlOE4TDODpdcITYlhdW795CVlUXi8bPMmzePugeN9mTo6afdVwyScinlBOBKMAExSHvMY8MNu5pZz8fFMjExgehpU5k7eRKfHN7buViDR2KotKQa2gnBBCwDsiIdc58leQRExwqKPlrOluM/0vjofl/mqu9XgYXA1kABKcASBgAhpd9ji5E549l1cB9FRUXUNzX210w5Ww60dQmY608uEc94Hb8AXQMpmTZjOmfO17LzwD7Ky8u5dPqss4niUJk0H0GFoekalmnNYYDQpLDD+KjxJtFJSchoF8NSU/lw0RKmRqVTcLqQVkxahMM9QYFhGBWGZVrDgMyBCrCEZgtoP3WB/VVVzNz4KcnxCTZZtEsQhYu2YIlQku3r8MWrtmPCSjhDUhmblUV6chonjx+HOw1oUmIJaTeM092UlX3FxuojLFu2jPxRr5BU1wxCV5tEMKQBI5SAzkziQHfEXG5yCwvJW7yQ7OxsXr+ts6K4mDVHdhFrqv2xs3cpIEaP5di1PylYPJ8XiWJwzGCaRDuPlElPEepJcY+2f4IJ6LKfUrKckpISZgwdbO9MxEGaS+tW2bUKhGoQ4KqHdmjrdyUoRPezGQnGTZ/J+wvn84Ii90ruezy4D3tIrK23LXyGwBLCmfUiggFc7Unr9z4mljcLZzN5+HA7NfJFBZtLS9nU+js+f3w6DB1dCvSB83uVgP8C33QHMS2NrPHjSdAMfHU3WL3vG6paL/BPgEoVdk0bEL3qQQWu3vBvDPd6rYQoN8mDk1SmwXvnFr/U19E9ot1WAqF3TkNNCPuKIJU1ILiuElGDZVp/+HP0E9xrgQetttakjHTciUk8vG37343UkSOIS0iwXXl814th+SKJwVld172GZdlTaG8vAQ3NXPL8xszMTLT0FBat+IDqBSpj+zFmFPlLF5E5ZBjRwOlzHrz0uQn1hmS/aZoY/pBVACt67gcmZVu3MH/ObOLdLt6Y/y4Hx2aw/ugxXC4XudOmkpOTwyCp8fDcZQ6dOEYz/gg4067T986Jf0DZdC3DW8AmYFWg5fmfq1n58Uo2rFljP782KZcpk3J57K8FVNXCmUaq123m4MUzdid+70LhM7UTqj+G42Whsyb4fO1avPVNlK5eRfLIDFu+TXyjnTaPh5Prt1F5spKLnf2Fgmp+qqsWcApoQ1CM5ERnvnsiYsfOrzm3p5K8vDxmJ49GSknTpSvU1NSwwbzKg66u+/dcWTQLTRQFVseGw+hXf23Qqy6s7Wihtmo36/yN1DD0QGjyhwjeC6wHewtQiUXXvrMsazaSXcF2SXvJ9csVlPy2Ite0UGU5qOJE3b4HciM8mAQjVqgGFiC57CQPKiAAF/zVa7hHM2cx/BfYI7btac6Gj4G1wHa7hoOuw+mQIIQKNwFVBKrD6SG12YToP+zT8W0hxHZN07abpqkqaFVFOY/n19Wl6/pNleHCxf9wyvJIDG8F0wAAAABJRU5ErkJggg==">
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
  <link rel="preload" as="image" href="../decalque/decalque-oferta.jpg?v=1111" fetchpriority="high">
  <link rel="preload" as="image" href="../img/banner-1111-modal.webp" fetchpriority="high">
  <!-- Google Fonts: Plus Jakarta Sans & Inter (Oficial TikTok Parity) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
</head>
<body>
  <!-- CRITICAL TIKTOK SPINNER (TRANSLÚCIDO E ULTRA-RÁPIDO) -->
  <div id="tt-instant-loader" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(255,255,255,0.42);backdrop-filter:blur(3.5px);-webkit-backdrop-filter:blur(3.5px);z-index:99999999;display:flex;align-items:center;justify-content:center;transition:opacity 0.12s ease,visibility 0.12s ease;pointer-events:none;">
    <div style="position:relative;width:44px;height:20px;">
      <div style="position:absolute;width:20px;height:20px;border-radius:50%;background:#25F4EE;left:0;animation:ttBallCyan 0.85s cubic-bezier(0.45,0.05,0.55,0.95) infinite;"></div>
      <div style="position:absolute;width:20px;height:20px;border-radius:50%;background:#FE2C55;right:0;animation:ttBallPink 0.85s cubic-bezier(0.45,0.05,0.55,0.95) infinite;"></div>
    </div>
  </div>
  <style>
    @keyframes ttBallCyan{0%{transform:translateX(0) scale(1);z-index:2}50%{transform:translateX(24px) scale(1.12);z-index:2}50.01%{z-index:1}100%{transform:translateX(0) scale(0.88);z-index:1}}
    @keyframes ttBallPink{0%{transform:translateX(0) scale(0.88);z-index:1}50%{transform:translateX(-24px) scale(0.88);z-index:1}50.01%{z-index:2}100%{transform:translateX(0) scale(1.12);z-index:2}}
  </style>
  <script>
    (function(){
      var el = document.getElementById('tt-instant-loader');
      if(!el) return;
      var dismissed = false;
      function dismiss(){
        if(dismissed) return;
        dismissed = true;
        el.style.opacity = '0';
        el.style.visibility = 'hidden';
        setTimeout(function(){ if(el && el.parentNode) el.parentNode.removeChild(el); }, 50);
      }
      if(document.readyState !== 'loading'){
        dismiss();
      } else {
        document.addEventListener('DOMContentLoaded', dismiss, { passive: true });
        window.addEventListener('load', dismiss, { passive: true });
      }
      setTimeout(dismiss, 100);
    })();
  </script>

  <div class="app-container">

    <!-- HEADER -->
    <header class="header">
      <a class="header-back-btn" href="../index.html" aria-label="Voltar">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </a>
      <div class="header-search-wrapper">
        <button class="header-search-icon-btn">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </button>
        <input type="text" class="header-search" placeholder="Pesquisar" readonly onclick="window.location='../index.html'">
      </div>
      <div class="header-icons">
        <button class="header-share-btn" onclick="shareProduct()" aria-label="Compartilhar"><img loading="lazy" decoding="async" src="../img/share-arrow.png" alt="Compartilhar" style="width: 22px; height: 22px; object-fit: contain;"></button>
        <a href="../pages/carrinho.html" class="header-icon-btn" aria-label="Carrinho">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          <span class="cart-badge" style="display:none">0</span>
        </a>
        <button class="header-more-btn" onclick="showMoreOptions()" aria-label="Mais opções">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
            <circle cx="5" cy="12" r="2"></circle>
            <circle cx="12" cy="12" r="2"></circle>
            <circle cx="19" cy="12" r="2"></circle>
          </svg>
        </button>
      </div>
    </header>

    <!-- CONTEÚDO DA PÁGINA -->
    <div class="page-content">

      <!-- SLIDER DE IMAGENS OFICIAIS -->
      <div class="image-slider">
        <div class="slider-track">
          <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-12-1.jpg" alt="Piscina Splash Fun Redonda Inflável 2400 Litros - Mor - 1" onerror="this.style.display='none'">
          <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-12-2.jpg" alt="Piscina Splash Fun Redonda Inflável 2400 Litros - Mor - 2" onerror="this.style.display='none'">
          <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-12-3.jpg" alt="Piscina Splash Fun Redonda Inflável 2400 Litros - Mor - 3" onerror="this.style.display='none'">
          <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-12-4.jpg" alt="Piscina Splash Fun Redonda Inflável 2400 Litros - Mor - 4" onerror="this.style.display='none'">
          <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-12-5.jpg" alt="Piscina Splash Fun Redonda Inflável 2400 Litros - Mor - 5" onerror="this.style.display='none'">
          <img loading="lazy" decoding="async" class="slider-img" src="../img/produto-12-6.jpg" alt="Piscina Splash Fun Redonda Inflável 2400 Litros - Mor - 6" onerror="this.style.display='none'">
        </div>
        <div class="slider-counter">1 / 6</div>
      </div>
      <div class="slider-dots"></div>

      <!-- ABAS DE NAVEGAÇÃO -->
      <nav class="product-tabs">
        <button class="product-tab active" data-tab="visao-geral">Visão geral</button>
        <button class="product-tab" data-tab="avaliacoes">Avaliações</button>
        <button class="product-tab" data-tab="descricao">Descrição</button>
        <button class="product-tab" data-tab="recomendacoes">Recomendações</button>
      </nav>

      <!-- SEÇÃO DE PREÇO / OFERTA RELÂMPAGO -->
      <div class="price-section">
        <div class="discount-badge-white">-78%</div>
        <div class="price-row">
          <span class="price-currency-sign">R$</span>
          <div class="price-current">89<span class="price-cents">,90</span></div>
        </div>
        <div class="price-original">R$ 399,00</div>
        <div class="price-right">
          <div class="timer-row">
            <span class="timer-label">Termina em</span>
            <span class="timer-value oferta-timer">04:00:00</span>
          </div>
        </div>
      </div>

      <!-- INFO DO PRODUTO -->
      <div class="product-info">

        <!-- 1. Parcelamento oficial TikTok Shop -->
        <div class="installment-row" style="display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #161823; cursor: pointer;">
          <div style="display: inline-flex; align-items: center; gap: 5px;">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" style="flex-shrink: 0;">
              <rect x="2" y="4" width="20" height="13.5" rx="2" stroke="#161823" stroke-width="1.8" fill="none"/>
              <line x1="2" y1="8" x2="22" y2="8" stroke="#161823" stroke-width="1.8"/>
              <circle cx="16" cy="14" r="4.2" fill="#fff" stroke="#161823" stroke-width="1.8"/>
              <polyline points="16 11.8 16 14 18 14" stroke="#161823" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="font-weight: 500;">2x R$ 44,95</span>
            <span style="color: #df3564; font-weight: 400; margin-left: 2px;">sem juros</span>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-left: auto;"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </div>

        <!-- 2. Cupons oficiais TikTok Shop -->
        <div class="discount-ticket" style="flex-wrap: nowrap; display: flex; align-items: center; justify-content: space-between; cursor: pointer;">
          <div style="display: flex; align-items: center; gap: 6px; min-width: 0; overflow: hidden; flex: 1;">
            <span class="product-badge-discount" style="display: inline-flex; align-items: center; gap: 4px; background: #fff; border: 1px solid #ffd2d8; color: #d60643; font-size: 11.5px; font-weight: 600; padding: 2.5px 7px; border-radius: 4px; line-height: 1.4;">
              <svg viewBox="0 0 667 534" fill="none" xmlns="http://www.w3.org/2000/svg" width="14" height="11" style="flex-shrink: 0;">
                <path d="M666.666 166.667C640.145 166.667 614.71 177.203 595.956 195.956C577.202 214.71 566.666 240.145 566.666 266.667C566.666 293.189 577.202 318.624 595.956 337.378C614.71 356.131 640.145 366.667 666.666 366.667L666.666 466.667C666.666 484.348 659.642 501.305 647.14 513.808C634.637 526.31 617.681 533.334 600 533.334L466.666 533.334L466.666 470.601C466.666 461.76 463.154 453.281 456.903 447.03C450.652 440.779 442.174 437.267 433.333 437.267C424.492 437.267 416.014 440.779 409.763 447.03C403.512 453.281 400 461.76 400 470.601L400 533.334L66.666 533.334C48.9852 533.334 32.0287 526.31 19.5264 513.808C7.02395 501.305 1.13666e-05 484.348 1.01189e-05 466.667L1.44901e-05 366.666C55.4279 366.576 100.333 266.167 100.333 266.167C100.333 210.718 55.4279 165.758 2.3276e-05 165.668L2.76035e-05 66.667C3.0397e-05 48.9859 7.02397 32.0288 19.5264 19.5264C32.0287 7.02422 48.9852 8.86041e-05 66.666 4.76048e-07L400 1.50465e-05L400 62.7334C400 71.5739 403.512 80.0525 409.763 86.3037C416.014 92.5549 424.492 96.0674 433.333 96.0674C442.174 96.0674 450.652 92.5549 456.903 86.3037C463.154 80.0525 466.666 71.5739 466.666 62.7334L466.666 1.79606e-05L600 2.37888e-05C617.681 0.000113468 634.637 7.02425 647.14 19.5264C659.642 32.0288 666.666 48.9859 666.666 66.667L666.666 166.667Z" fill="#D60643"/>
              </svg>
              <span>78% OFF</span>
            </span>
          </div>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-left: auto;"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </div>

        <!-- Título com Bookmark à direita -->
        <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 8px;">
          <h1 class="product-title" style="font-size: 16px; font-weight: 700; color: #161823; line-height: 1.35; margin: 0; flex: 1;">
            Piscina Splash Fun Redonda Inflável 2400 Litros - Mor
          </h1>
          <button class="bookmark-btn" onclick="toggleBookmark(this)" style="background: none; border: none; padding: 2px 0 0 0; cursor: pointer; color: #161823; display: flex; align-items: center; justify-content: center; flex-shrink: 0;" aria-label="Salvar">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
            </svg>
          </button>
        </div>

        <!-- Avaliação Oficial e Vendidos (Rating Blue #4364db) -->
        <div class="ratings-row" style="display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
          <div class="star-row" style="display: flex; align-items: center; gap: 4px;">
            <svg class="star-icon" viewBox="0 0 24 24" width="13" height="13" fill="#ffb800">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            <span style="font-size: 13px; font-weight: 700; color: #161823;">4.8</span>
            <span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector('.reviews-section')?.scrollIntoView({behavior:'smooth'})">(1.4K)</span>
          </div>
          <span style="color: #e5e5e5; font-size: 12px; margin: 0 1px;">|</span>
          <div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">9.8K vendidos</div>
        </div>

        <!-- BLOCO PRÉ-DESCRIÇÃO OFICIAL TIKTOK SHOP -->
        <div class="product-info-rows">
          <!-- Linha 1: Frete Grátis -->
          <div class="info-row-item" onclick="window.openEnvioModal && window.openEnvioModal()" style="cursor: pointer;">
            <div class="info-row-left">
              <div class="info-row-icon">
                <svg width="20" height="20" viewBox="0 -2 20 20" xmlns="http://www.w3.org/2000/svg">
                  <g transform="translate(-2 -4)">
                    <path d="M9.17,17H13V6a1,1,0,0,0-1-1H5" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                    <path d="M3,13v3a1,1,0,0,0,1,1h.87" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                    <path d="M14.87,17H13V7h4.25a1,1,0,0,1,1,.73L19,10.5l1.24.31a1,1,0,0,1,.76,1V16a1,1,0,0,1-1,1h-.89" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                    <path d="M9,17a2,2,0,1,1-2-2A2,2,0,0,1,9,17Zm8-2a2,2,0,1,0,2,2A2,2,0,0,0,17,15ZM3,9H9" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  </g>
                </svg>
              </div>
              <div class="info-row-text-group" style="display: flex; flex-direction: column; gap: 3px;">
                <span class="info-row-title frete-prazo-dinamico" style="font-size: 13.5px; font-weight: 500; color: #161823;">Receba até sex., 14 de nov – seg., 17 de nov</span>
                <div style="display: flex; align-items: center; gap: 6px;">
                  <span class="badge-frete-gratis" style="background: #e6f9f6; color: #00a699; font-size: 10.5px; font-weight: 700; padding: 1.5px 5.5px; border-radius: 3px; line-height: 1.2;">Frete grátis</span>
                  <span style="font-size: 12px; color: #888;">Taxa de envio: <span style="text-decoration: line-through;">R$ 24,90</span></span>
                </div>
              </div>
            </div>
            <span class="info-row-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-left: auto;"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
          </div>

          <!-- Linha 2: Opções Disponíveis -->
          <div class="info-row-item info-row-opcoes" onclick="handleAddToCart()">
            <div class="info-row-left" style="display:flex; align-items:center;">
              <div class="info-row-icon" style="display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-right:8px;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="3" width="7" height="7" rx="1.5"></rect>
                  <rect x="14" y="3" width="7" height="7" rx="1.5"></rect>
                  <rect x="14" y="14" width="7" height="7" rx="1.5"></rect>
                  <rect x="3" y="14" width="7" height="7" rx="1.5"></rect>
                </svg>
              </div>
              <div class="info-row-opcoes-content" style="display:flex; align-items:center; gap:8px;">
                <div style="display:flex; gap:4px; align-items:center;">
                  <div style="width:34px; height:34px; border-radius:4px; border:1px solid #e8e8e8; background:#f0f0f0; overflow:hidden; flex-shrink:0;">
                    <img loading="lazy" decoding="async" src="../img/produto-12-1.jpg" style="width:100%; height:100%; object-fit:cover; display:block;">
                  </div>
                  <div style="width:34px; height:34px; border-radius:4px; border:1px solid #e8e8e8; background:#f0f0f0; overflow:hidden; flex-shrink:0;">
                    <img loading="lazy" decoding="async" src="../img/produto-12-2.jpg" style="width:100%; height:100%; object-fit:cover; display:block;">
                  </div>
                  <div style="width:34px; height:34px; border-radius:4px; border:1px solid #e8e8e8; background:#f0f0f0; overflow:hidden; flex-shrink:0;">
                    <img loading="lazy" decoding="async" src="../img/produto-12-3.jpg" style="width:100%; height:100%; object-fit:cover; display:block;">
                  </div>
                </div>
                <span class="info-row-title">3 opções disponíveis</span>
              </div>
            </div>
            <span class="info-row-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-left: auto;"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
          </div>

          <!-- Linha 3: Proteção do Cliente -->
          <div class="info-row-item-protection" onclick="window.openProtecaoModal()" style="background:#fff; padding:12px 16px; border-bottom:1px solid #f2f2f2; cursor:pointer;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div class="info-row-left" style="display:flex; align-items:center; gap:7px;">
                <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#8B5E2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  <polyline points="9 12 11 14 15 10"></polyline>
                </svg>
                <span class="info-row-title" style="color:#8B5E2B; font-weight:500; font-size:13.5px;">Proteção do cliente</span>
              </div>
              <span class="info-row-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-left: auto;"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px 12px; margin-top:8px; padding-left:24px; box-sizing:border-box;">
              <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Devolução gratuita</div>
              <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Garantia de pontualidade</div>
              <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Pagamento seguro</div>
              <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Reembolso se algo der errado</div>
            </div>
          </div>
        </div>

        <!-- VÍDEOS DE CRIADORES (CANÔNICO DINÂMICO VIA VIDEOS-CRIADORES.JS) -->
        <div id="creators-section" class="creators-section"></div>

        <!-- AVALIAÇÕES DOS CLIENTES (FOTOS REAIS E COMENTÁRIOS CONTEXTUAIS) -->
        <div class="reviews-section">
          <h3 class="reviews-header">Avaliações dos clientes (1.4K)</h3>
          <div class="reviews-summary">
            <span class="review-avg">4,8</span><span class="review-avg-total">/5</span>
            <div class="review-stars">
              <svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg>
              <svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg>
              <svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg>
              <svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg>
              <svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg>
            </div>
          </div>

          <!-- Card 1 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">R</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">robertdjrbo</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2026-03-09 13:42 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Piscina de excelente qualidade! A facilidade de inflar a borda superior é incrível, enchi em menos de 3 minutos. A lona é muito reforçada com as 3 camadas e a tela interna de poliéster. A criançada está se divertindo demais no quintal! Chegou super rápido em 3 dias. Recomendo demais! 😍✨</p>
            <div class="review-photos">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c1-1.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c1-2.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c1-3.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c1-4.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
            </div>
          </div>

          <!-- Card 2 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">F</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">filipheguita</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2026-03-02 09:24 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Ótima piscina! Deu pra encher a borda com bomba de bicicleta muito rápido. Montagem super prática, muito melhor que aquelas antigas com armação de ferro pesada que enferrujam e têm quina perigosa. A lona reforçada passa muita segurança pras crianças pularem. Entrega rápida, comprei na quinta e chegou no sábado!</p>
            <div class="review-photos">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c2-1.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c2-2.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c2-3.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
            </div>
          </div>

          <!-- Card 3 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">I</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">igor_silva</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2026-02-14 16:51 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Produto de altíssima qualidade! Tamanho ideal para toda a família (2,40m cabe confortavelmente adultos e crianças). A estrutura é sustentada pela própria água e a borda inflável é super macia. Válvula de deságue funciona perfeitamente para esvaziar. Custo-benefício sensacional e entrega nota 10!</p>
            <div class="review-photos">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c3-1.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c3-2.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
            </div>
          </div>

          <!-- Card 4 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">B</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">barbaramurlik</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2026-01-28 14:29 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Recomendo de olhos fechados! Chegou tudo certinho e muito bem embalado. Lona de PVC de 3 camadas bem espessa e resistente, zero risco de rasgar fácil. As crianças estão apaixonadas, virou a atração do verão aqui em casa. Entrega super rápida!</p>
            <div class="review-photos">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c4-1.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c4-2.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
            </div>
          </div>

          <!-- Card 5 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">P</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">patysim</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2026-01-12 10:24 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Chegou muito antes do prazo! Piscina de 2400 litros super reforçada, manual bem explicativo e acompanha kit reparo original da Mor. Fácil de encher, limpar e cuidar. O melhor investimento para os dias de calor no quintal!</p>
            <div class="review-photos">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c5-1.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c5-2.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
              <img loading="lazy" decoding="async" class="review-photo" src="../img/review-12-c5-3.jpg" alt="Foto da avaliação" onclick="openPhotoModal(this.src)">
            </div>
          </div>

          <!-- Card 6 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">N</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">nataliasantosr</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2026-01-05 18:33 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Produto 100% conforme a descrição! Simples e rápido de montar, a borda sobe sozinha conforme vai enchendo com a mangueira. Não tem ferragens para machucar, material firme e seguro. Entrega expressa nota mil!</p>
          </div>

          <!-- Card 7 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">P</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">pedroduarte1984</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2025-12-20 16:25 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Extremamente satisfeito com a compra! Ótimo custo-benefício, loja séria e comprometida. A piscina é espaçosa, material robusto da Mor e as crianças aproveitaram as férias inteiras!</p>
          </div>

          <!-- Card 8 -->
          <div class="review-card">
            <div class="review-header">
              <div class="review-user">
                <div class="review-avatar"><div class="review-avatar-placeholder">A</div></div>
                <div class="review-user-info">
                  <div class="review-user-name">amanda_0liveira23</div>
                  <div class="review-user-stars">★★★★★</div>
                  <div class="review-date">2025-12-11 12:09 · Azul</div>
                </div>
              </div>
            </div>
            <p class="review-comment">Marca Mor é líder por um motivo: a durabilidade dessa Splash Fun é incomparável. Bem larga, acabamento impecável na válvula de deságue e entrega relâmpago. Adoramos!</p>
          </div>

        </div><!-- fim reviews-section -->

        <!-- CARD OFICIAL DA LOJA (MULTI-SELLER PARIDADE TIKTOK SHOP) -->
        <div class="seller-store-card" style="padding: 14px 16px; background: #ffffff; border-top: 8px solid #f1f2f5; border-bottom: 8px solid #f1f2f5; display: flex; flex-direction: column; gap: 10px;">
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 12px;">
              <img src="../img/seller-12.png" alt="Mor Oficial" style="width: 48px; height: 48px; border-radius: 50%; object-fit: cover; border: 1px solid #f0f0f0;">
              <div style="display: flex; flex-direction: column; gap: 2px;">
                <span style="font-size: 15px; font-weight: 700; color: #161823;">Mor Oficial</span>
                <span style="font-size: 11.5px; color: #73747b;">Loja Oficial Verificada</span>
              </div>
            </div>
            <button type="button" onclick="window.location.href='../index.html'" style="background: #fe2c55; color: #ffffff; font-size: 13px; font-weight: 600; border-radius: 20px; padding: 6px 18px; border: none; cursor: pointer;">Visitar</button>
          </div>
          <div style="display: flex; align-items: center; gap: 18px; font-size: 12px; color: #73747b; padding-left: 2px;">
            <span><strong>98%</strong> de avaliações positivas</span>
            <span><strong>99%</strong> envios pontuais</span>
          </div>
        </div>

        <!-- SEÇÃO OFICIAL: SOBRE ESTE PRODUTO -->
        <div class="about-product-section" id="sobre-este-produto">
          <h2 class="about-section-title">Sobre este produto</h2>

          <!-- SUBSEÇÃO 1: DETALHES (PARIDADE OFICIAL TIKTOK SHOP) -->
          <div class="product-details-block">
            <h3 class="about-subtitle">Detalhes</h3>
            <div class="details-attributes-grid">
              <div class="detail-row">
                <span class="detail-label">Marca</span>
                <span class="detail-value">Mor</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Capacidade</span>
                <span class="detail-value">2400 Litros</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Formato</span>
                <span class="detail-value">Redondo</span>
              </div>
              <div class="detail-row">
                <span class="detail-label">Composição/Material</span>
                <span class="detail-value">Lona em PVC laminado com trama de poliéster</span>
              </div>
              <div class="detail-row is-hidden toggleable-row">
                <span class="detail-label">Diâmetro</span>
                <span class="detail-value">2,40 metros</span>
              </div>
              <div class="detail-row is-hidden toggleable-row">
                <span class="detail-label">Altura</span>
                <span class="detail-value">63 centímetros</span>
              </div>
              <div class="detail-row is-hidden toggleable-row">
                <span class="detail-label">Peso Líquido</span>
                <span class="detail-value">5,16 kg</span>
              </div>
              <div class="detail-row is-hidden toggleable-row">
                <span class="detail-label">Conteúdo da Embalagem</span>
                <span class="detail-value">1 Piscina Splash Fun 2400L, 1 Kit Reparo, 1 Válvula de Deságue e Manual</span>
              </div>
              <div class="detail-row is-hidden toggleable-row">
                <span class="detail-label">Referência / Código</span>
                <span class="detail-value">001053</span>
              </div>
              <div class="detail-row is-hidden toggleable-row">
                <span class="detail-label">EAN</span>
                <span class="detail-value">7896020610533</span>
              </div>
              <div class="detail-row is-hidden toggleable-row">
                <span class="detail-label">Garantia</span>
                <span class="detail-value">90 dias pelo fabricante</span>
              </div>
            </div>
            <!-- LINK AZUL VER MAIS ALINHADO À ESQUERDA -->
            <button type="button" class="btn-detalhes-link" id="btn-toggle-detalhes" onclick="toggleProductDetails(this)"><span>Ver mais</span></button>
          </div>

          <!-- SUBSEÇÃO 4: DESCRIÇÃO OFICIAL TIKTOK SHOP (COM FADE-OUT TRANSLÚCIDO E TOGGLE) -->
          <div class="description-section" id="sobre-produto-desc-section">
            <h3 class="about-subtitle">Descrição</h3>
            
            <div class="description-expandable-container" id="desc-expandable-container">
              <div class="description-text" id="desc-content-text">
                Sejam Bem-vindos à Mor Oficial!<br><strong>Piscina Splash Fun Redonda Inflável 2400 Litros - Mor</strong><br><br>Desfrute ao máximo do verão com a incrível Piscina Inflável Splash Fun de 2.400 litros da Mor! Montar sua piscina nunca foi tão fácil e seguro. Sem a necessidade de armações de ferro pesadas ou peças rígidas, ela destaca-se pela lona de PVC super reforçada com laminado duplo e uma trama de poliéster entre as lâminas (tecnologia de 3 camadas), proporcionando resistência superior contra furos e rasgos.<br><br>A inovação continua com a exclusiva ausência de quinas rígidas na estrutura: a única sustentação necessária é o anel inflável na borda superior e a própria água, garantindo total segurança para as crianças brincarem à vontade. Para simplificar ainda mais, a Piscina Inflável acompanha manual detalhado de instruções, válvula de deságue para escoamento rápido, válvula para conexão de filtro e kit reparo original.<br><br>Transforme seu quintal em uma área de lazer completa para relaxar após o trabalho e curtir os fins de semana de sol com a família inteira!<br><br>Destaques Principais:<br>- Capacidade: 2400 Litros<br>- Formato: Redondo (2,40m de diâmetro x 63cm de altura)<br>- Montagem expressa: basta inflar a borda superior e encher de água que ela sobe sozinha<br>- Lona tripla reforçada com tela tramada de poliéster de alta tenacidade<br>- Borda inflável macia: sem ferragens pontiagudas ou quinas perigosas<br>- Acompanha válvula de deságue com encaixe, válvula para filtro e kit reparo original Mor<br><br>Especificações Técnicas:<br>- Marca: Mor<br>- Modelo: Splash Fun 2400L<br>- Referência do Fabricante: 001053<br>- EAN: 7896020610533<br>- Medidas montada: 2,40m x 2,40m x 63cm<br>- Peso: 5,16 Kg<br>- Certificação e Segurança OCP: 00309/2016<br>- Garantia: 90 dias contra defeito de fabricação<br><br>Atenção: Nunca deixe crianças sozinhas perto da água sem a supervisão direta de um adulto.
              </div>
              
              <!-- OVERLAY DE OPACIDADE DESFOCADA (FADE-OUT TRANSLÚCIDO BRANCO) -->
              <div class="desc-fade-overlay" id="desc-fade-overlay"></div>
            </div>

            <!-- BOTÃO TOGGLE VER MAIS ∨ / VER MENOS ⌃ -->
            <button type="button" class="btn-toggle-desc" id="btn-toggle-desc" onclick="toggleDescricaoCompleta()">
              <span id="btn-toggle-desc-text">Ver mais</span>
              <svg class="toggle-icon-desc" id="btn-toggle-desc-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </button>
          </div>

        </div><!-- fim about-product-section -->

        <!-- FAIXA DIVISORA CINZA GROSSA (8PX) OFICIAL TIKTOK -->
        <div class="tt-section-divider-thick"></div>

        <div class="related-section">
          <h3 class="related-title">Você também pode gostar</h3>
          <div class="related-grid">
            <a class="related-card" href="produto-68.html">
              <img loading="lazy" decoding="async" class="related-img" src="../img/produto-68-1.jpg" alt="Jogo de Panelas Cerâmica Kit 5 Peças Antiaderente" onerror="this.src='../img/ranking-top1.webp'">
              <div class="related-info">
                <div class="related-name">Jogo de Panelas Cerâmica Kit 5 Peças Antiaderente Tampa Vidro</div>
                <div class="related-price-row">
                  <span class="related-price">R$ 69,90</span>
                  <span class="related-price-original">R$ 397,86</span>
                </div>
                <div class="related-badges">
                  <span class="related-discount">82% OFF</span>
                  <span class="badge-frete">· Frete grátis</span>
                </div>
                <div class="related-sold">9052 vendido(s)</div>
              </div>
            </a>
            <a class="related-card" href="produto-24.html">
              <img loading="lazy" decoding="async" class="related-img" src="../img/produto-24-1.jpg" alt="Triciclo Infantil 4 em 1 Multifuncional Carrinho de Bebê" onerror="this.src='../img/ranking-top1.webp'">
              <div class="related-info">
                <div class="related-name">Triciclo Infantil 4 em 1 Multifuncional Carrinho de Bebê Com Empurrador</div>
                <div class="related-price-row">
                  <span class="related-price">R$ 159,90</span>
                  <span class="related-price-original">R$ 599,00</span>
                </div>
                <div class="related-badges">
                  <span class="related-discount">73% OFF</span>
                  <span class="badge-frete">· Frete grátis</span>
                </div>
                <div class="related-sold">897 vendido(s)</div>
              </div>
            </a>
          </div>
        </div>

      </div><!-- fim product-info -->
    </div><!-- fim page-content -->

    <!-- BOTTOM BAR -->
    <div class="bottom-bar">
      <div class="store-chat-image-group">
        <div class="store-chat-clickable-loja" onclick="window.location.href='../index.html'"></div>
        <div class="store-chat-clickable-chat" onclick="openSmartChat()"></div>
      </div>
      <button class="btn-add-cart" id="btn-add-cart" onclick="handleAddToCart()" aria-label="Adicionar ao carrinho">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
      </button>
      <button class="btn-buy" id="btn-buy" onclick="handleBuyNow()">
        <span class="btn-line1">Compre</span>
        <span class="btn-line2">R$ 89,90 com cupom</span>
      </button>
    </div>

    <!-- BOTAO VOLTAR AO TOPO (↑) OFICIAL TIKTOK SHOP -->
    <button id="scroll-to-top-btn" class="scroll-to-top-btn" aria-label="Voltar ao topo" onclick="scrollToTop()">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#161823" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
        <line x1="5" y1="5.5" x2="19" y2="5.5"></line>
        <line x1="12" y1="19" x2="12" y2="9"></line>
        <polyline points="7 14 12 9 17 14"></polyline>
      </svg>
    </button>

  </div><!-- fim app-container -->

  <script src="../js/catalogo.js?v=1794434281002"></script>
  <script src="../js/app.js?v=1794434281002"></script>
  <script src="../js/videos-criadores.js?v=1794434281002"></script>

  <script>
  const PRODUTO_ATUAL = {
    id: 12,
    nome: 'Piscina Splash Fun Redonda Inflável 2400 Litros - Mor',
    preco: 89.90,
    precoOriginal: 399.00,
    img: '../img/produto-12-1.jpg',
    imagens: [
      "../img/produto-12-1.jpg",
      "../img/produto-12-2.jpg",
      "../img/produto-12-3.jpg",
      "../img/produto-12-4.jpg",
      "../img/produto-12-5.jpg",
      "../img/produto-12-6.jpg"
    ]
  };

  function handleAddToCart() {
    if (typeof addToCart === 'function') {
      addToCart(PRODUTO_ATUAL);
      if (typeof showToast === 'function') showToast('Produto adicionado ao carrinho!');
    }
  }

  function handleBuyNow() {
    if (typeof handleAddToCartWithVariacoes === 'function' && typeof PRODUTO_ATUAL !== 'undefined') {
      handleAddToCartWithVariacoes(PRODUTO_ATUAL, true);
    } else if (typeof irDiretoAoCheckoutComProduto === 'function' && typeof PRODUTO_ATUAL !== 'undefined') {
      irDiretoAoCheckoutComProduto(PRODUTO_ATUAL, '', 1);
    } else {
      if (typeof PRODUTO_ATUAL !== 'undefined' && typeof addToCart === 'function') addToCart(PRODUTO_ATUAL);
      window.location.href = 'resumo.html';
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

  window.toggleProductDetails = function(btn) {
    if (!btn) return;
    var container = btn.closest('.product-details-block') || btn.parentElement;
    if (!container) return;
    var hiddenRows = container.querySelectorAll('.detail-row.toggleable-row');
    var isExpanded = btn.classList.contains('expanded');
    if (isExpanded) {
      hiddenRows.forEach(function(r) {
        r.classList.add('is-hidden');
        r.style.setProperty('display', 'none', 'important');
      });
      btn.classList.remove('expanded');
      var span = btn.querySelector('span');
      if (span) span.textContent = 'Ver mais';
    } else {
      hiddenRows.forEach(function(r) {
        r.classList.remove('is-hidden');
        r.style.setProperty('display', 'flex', 'important');
      });
      btn.classList.add('expanded');
      var span = btn.querySelector('span');
      if (span) span.textContent = 'Ver menos';
    }
  };

  window.toggleDescricaoCompleta = function() {
    var container = document.getElementById('desc-expandable-container');
    var overlay = document.getElementById('desc-fade-overlay');
    var btnText = document.getElementById('btn-toggle-desc-text');
    var btnIcon = document.getElementById('btn-toggle-desc-icon');
    if (!container) return;
    
    var isExpanded = container.classList.contains('expanded');
    if (isExpanded) {
      container.classList.remove('expanded');
      container.style.maxHeight = '98px';
      if (overlay) overlay.style.display = 'block';
      if (btnText) btnText.textContent = 'Ver mais';
      if (btnIcon) btnIcon.innerHTML = '<polyline points=\"6 9 12 15 18 9\"></polyline>';
    } else {
      container.classList.add('expanded');
      container.style.maxHeight = 'none';
      if (overlay) overlay.style.display = 'none';
      if (btnText) btnText.textContent = 'Ver menos';
      if (btnIcon) btnIcon.innerHTML = '<polyline points=\"6 15 12 9 18 15\"></polyline>';
    }
  };

  window.scrollToTop = function() {
    var sc = document.querySelector('.page-content');
    if (sc) sc.scrollTo({ top: 0, behavior: 'smooth' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  (function initScrollButton() {
    function checkScroll() {
      var btn = document.getElementById('scroll-to-top-btn');
      if (!btn) return;
      var sc = document.querySelector('.page-content');
      var sy = sc && sc.scrollTop ? sc.scrollTop : window.scrollY;
      if (sy > 200) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }
    window.addEventListener('scroll', checkScroll, { passive: true });
    document.addEventListener('DOMContentLoaded', function() {
      var sc = document.querySelector('.page-content');
      if (sc) sc.addEventListener('scroll', checkScroll, { passive: true });
    });
  })();

  function openPhotoModal(src) {
    var modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100vw';
    modal.style.height = '100vh';
    modal.style.background = 'rgba(0,0,0,0.92)';
    modal.style.zIndex = '999999';
    modal.style.display = 'flex';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';
    modal.onclick = function() { modal.remove(); };
    
    var img = document.createElement('img');
    img.src = src;
    img.style.maxWidth = '92vw';
    img.style.maxHeight = '88vh';
    img.style.objectFit = 'contain';
    img.style.borderRadius = '8px';
    modal.appendChild(img);
    document.body.appendChild(modal);
  }
  </script>

</body>
</html>
"""

with open('pages/produto-12.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("pages/produto-12.html gerado com sucesso!")
