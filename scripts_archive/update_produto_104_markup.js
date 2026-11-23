const fs = require('fs');
const path = require('path');

function updateFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  let html = fs.readFileSync(filePath, 'utf8');

  // 1. Substituir bloco price-section e topo do product-info ate ratings-row
  const regexOld = /<!-- SEÇÃO DE PREÇO[\s\S]*?<!-- 3\. Linha 1: Frete grátis/;
  
  const newMarkup = `<!-- SEÇÃO DE PREÇO / OFERTA RELÂMPAGO (TIKTOK SHOP OFICIAL) -->
    <div class="price-section">
      <div class="price-left">
        <div class="price-main-row">
          <span class="discount-badge-white">-67%</span>
          <span class="price-currency">R$</span>
          <div class="price-current"><span class="p-int">19</span><span class="p-dec">,90</span></div>
        </div>
        <div class="price-original-row">
          <span class="price-original">R$ 59,90</span>
        </div>
      </div>
      <div class="price-right">
        <div class="flash-title-row">
          <span class="flash-title">Oferta Relâmpago</span>
          <svg class="flash-bolt-icon" viewBox="0 0 24 24">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
        </div>
        <div class="flash-timer-row">
          <span class="timer-label">Termina em</span>
          <span class="timer-value oferta-timer">10:37:47</span>
        </div>
      </div>
    </div>

    <!-- INFORMAÇÕES DO PRODUTO -->
    <div class="product-info">

      <!-- 1. Linha de Parcelamento Oficial (💳⏰ 2x R$ 11,48 sem juros >) -->
      <div class="installment-row" onclick="handleAddToCart()">
        <div class="installment-left">
          <svg class="installment-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="5" width="20" height="14" rx="2"></rect>
            <line x1="2" y1="10" x2="22" y2="10"></line>
            <circle cx="17" cy="15" r="3.5" fill="#fff" stroke="currentColor" stroke-width="1.5"></circle>
            <polyline points="17 13.5 17 15 18 15" stroke="currentColor" stroke-width="1.5"></polyline>
          </svg>
          <span class="installment-text">2x R$ 11,48 <span class="sem-juros">sem juros</span></span>
        </div>
        <span class="installment-arrow">›</span>
      </div>

      <!-- 2. Título com Bookmark à direita -->
      <div class="product-title-row">
        <h1 class="product-title">Chinelo Feminino Luxo Strass Brilhante Macio Leve</h1>
        <button class="bookmark-btn" onclick="toggleBookmark(this)" aria-label="Salvar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      </div>

      <!-- 3. Avaliações e Vendas (Cores e Tipografia Oficial TikTok) -->
      <div class="ratings-row">
        <svg class="star-icon" viewBox="0 0 24 24">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <span class="rating-score">4.8</span>
        <span class="rating-count" onclick="document.querySelector('.reviews-section')?.scrollIntoView({behavior:'smooth'})">(5,1 mil)</span>
        <span class="ratings-divider">|</span>
        <span class="sold-count">21.3K vendidos</span>
      </div>

      <!-- 3. Linha 1: Frete grátis`;

  if (regexOld.test(html)) {
    html = html.replace(regexOld, newMarkup);
    fs.writeFileSync(filePath, html, 'utf8');
    console.log('✅ ' + filePath + ' atualizado com novo markup!');
  } else {
    console.warn('⚠️ Regex nao encontrou o padrao em ' + filePath);
  }
}

updateFile(path.join(__dirname, '../pages/produto-104.html'));
