const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('>>> [BRUNO CTO] ELIMINANDO TODOS OS BUGS IDENTIFICADOS <<<');

// 1. CORRIGIR O VAZAMENTO DE TEXTO DO BADGE DE DESCONTO
// Remove qualquer texto escapado 'class="product-badge-discount">'
html = html.replace(/<div class="home-discount-badge">[\s\S]*?<\/div>/g, '');
html = html.replace(/class="product-badge-discount">/g, '');

// 2. GARANTIR QUE OS BADGES DE CADA CARD TENHAM APENAS O BADGE OFICIAL DE FRETE GRÁTIS
// No print oficial, a lista de produtos tem APENAS o badge 'Frete grátis' (sem o badge vermelho de desconto)
html = html.replace(/<div class="card-badges-row">[\s\S]*?<\/div>/g, `
                      <div class="card-badges-row">
                        <span class="badge-frete-gratis">Frete grátis</span>
                      </div>`);

// 3. BLINDAR O CSS COM MÁXIMA ESPECIFICIDADE E ZERO CONFLITO
const fixStyles = `
    /* === CORREÇÃO FINAL ULTRA-BLINDADA TIKTOK SHOP === */
    /* Garante que o body e o root nunca fiquem cortados */
    html, body {
      margin: 0 !important;
      padding: 0 !important;
      background: #f8f8f8 !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }

    #root {
      max-width: 480px !important;
      margin: 0 auto !important;
      background: #f8f8f8 !important;
      padding-top: 50px !important;
      min-height: 100vh !important;
      position: relative !important;
    }

    .header {
      position: fixed !important;
      top: 0 !important;
      left: 50% !important;
      transform: translateX(-50%) !important;
      width: 100% !important;
      max-width: 480px !important;
      height: 50px !important;
      background: #fff !important;
      z-index: 9999 !important;
      border-bottom: 1px solid #f0f0f0 !important;
    }

    /* Loja e Cupons SEMPRE VISÍVEIS NO TOPO */
    .store-section {
      background: #fff !important;
      padding: 12px 16px 6px 16px !important;
      display: block !important;
    }

    .badge-loja-estrela {
      display: inline-flex !important;
      align-items: center !important;
      background: #faeed7 !important;
      color: #8c5b08 !important;
      font-size: 10.5px !important;
      font-weight: 600 !important;
      padding: 2px 6px !important;
      border-radius: 4px !important;
    }

    .coupons-container {
      background: #fff !important;
      padding: 0 16px 10px 16px !important;
      display: block !important;
    }

    .coupon-card-official {
      background: #eafbf7 !important;
      border: 1px solid #d4f4ed !important;
      border-radius: 8px !important;
      padding: 10px 14px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
    }

    .coupon-title {
      font-size: 13.5px !important;
      font-weight: 700 !important;
      color: #161823 !important;
    }

    .coupon-sub {
      font-size: 11px !important;
      color: #6b7280 !important;
      margin-top: 2px !important;
    }

    .coupon-resgatado-txt {
      font-size: 13px !important;
      font-weight: 600 !important;
      color: #20b5a6 !important;
    }

    /* Sub-barra de ordenação (Aba Produtos) */
    .subfilter-produtos-bar {
      display: none;
      align-items: center;
      justify-content: space-between;
      padding: 10px 16px !important;
      background: #fff !important;
      border-bottom: 1px solid #f2f2f2 !important;
    }

    .subfilter-items {
      display: flex !important;
      align-items: center !important;
      gap: 12px !important;
    }

    .subfilter-item {
      font-size: 13px !important;
      color: #4b4d53 !important;
      cursor: pointer !important;
      font-weight: 500 !important;
    }

    .subfilter-item.active {
      color: #161823 !important;
      font-weight: 700 !important;
    }

    .subfilter-divider {
      color: #e5e5e5 !important;
      font-size: 11px !important;
    }

    /* Badge Frete Grátis Oficial */
    .badge-frete-gratis {
      display: inline-flex !important;
      align-items: center !important;
      background: #e6f9f6 !important;
      color: #00a699 !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      padding: 1.5px 5px !important;
      border-radius: 3px !important;
      line-height: 1.2 !important;
      border: none !important;
    }

    /* Linha de Avaliação: estrela amarela + nota + pipe + vendas */
    .card-rating-row {
      display: flex !important;
      align-items: center !important;
      gap: 3px !important;
      font-size: 11px !important;
      color: #8a8b91 !important;
      margin-top: 2px !important;
    }

    .star-yellow {
      color: #ffaa00 !important;
      font-size: 11px !important;
    }

    .rating-pipe {
      color: #d1d5db !important;
      margin: 0 1px !important;
    }

    /* BOTÃO UNIFICADO OFICIAL [ 🛒 | Comprar ] */
    .unified-buy-btn {
      display: flex !important;
      align-items: stretch !important;
      background: #fe2c55 !important;
      border-radius: 6px !important;
      overflow: hidden !important;
      height: 30px !important;
      box-shadow: 0 1px 3px rgba(254,44,85,0.2) !important;
      flex-shrink: 0 !important;
      cursor: pointer !important;
      text-decoration: none !important;
    }

    .unified-buy-btn .btn-cart-part {
      background: #fdf0f3 !important;
      padding: 0 8px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
    }

    .unified-buy-btn .btn-txt-part {
      background: #fe2c55 !important;
      color: #fff !important;
      font-size: 12px !important;
      font-weight: 700 !important;
      padding: 0 10px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      white-space: nowrap !important;
    }

    /* OCULTAR O BOTÃO COMPRAR NA GRADE DE 2 COLUNAS DA HOME */
    #recommended-grid:not(.produtos-layout-list) .unified-buy-btn,
    #principais-produtos-section .unified-buy-btn {
      display: none !important;
    }

    /* ========================================================
       MODO LISTA EMPILHADA CANÔNICA (ABA PRODUTOS)
       ======================================================== */
    #recommended-grid.produtos-layout-list {
      display: flex !important;
      flex-direction: column !important;
      gap: 0 !important;
      background: #fff !important;
      padding: 0 !important;
    }

    #recommended-grid.produtos-layout-list .product-card-rec {
      display: block !important;
      background: #fff !important;
      border: none !important;
      border-radius: 0 !important;
      padding: 12px 16px !important;
      border-bottom: 1px solid #f5f5f5 !important;
      width: 100% !important;
      box-sizing: border-box !important;
    }

    #recommended-grid.produtos-layout-list .card-inner-box {
      display: flex !important;
      flex-direction: row !important;
      align-items: center !important;
      gap: 12px !important;
      width: 100% !important;
    }

    #recommended-grid.produtos-layout-list .card-thumb-img {
      width: 108px !important;
      height: 108px !important;
      min-width: 108px !important;
      max-width: 108px !important;
      aspect-ratio: 1 / 1 !important;
      object-fit: cover !important;
      border-radius: 8px !important;
      background: #f7f7f7 !important;
      flex-shrink: 0 !important;
    }

    #recommended-grid.produtos-layout-list .card-details-col {
      flex: 1 !important;
      min-width: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      height: 108px !important;
      padding: 2px 0 !important;
    }

    #recommended-grid.produtos-layout-list .product-name {
      font-size: 13.5px !important;
      font-weight: 500 !important;
      color: #161823 !important;
      line-height: 1.3 !important;
      margin: 0 0 3px 0 !important;
      display: -webkit-box !important;
      -webkit-line-clamp: 2 !important;
      -webkit-box-orient: vertical !important;
      overflow: hidden !important;
      height: auto !important;
      max-height: 35px !important;
    }

    #recommended-grid.produtos-layout-list .card-badges-row {
      display: flex !important;
      align-items: center !important;
      margin-bottom: 2px !important;
    }

    #recommended-grid.produtos-layout-list .card-bottom-action-row {
      display: flex !important;
      align-items: flex-end !important;
      justify-content: space-between !important;
      width: 100% !important;
      margin-top: auto !important;
    }

    #recommended-grid.produtos-layout-list .price-stack-col {
      display: flex !important;
      flex-direction: column !important;
    }

    #recommended-grid.produtos-layout-list .price-current-txt {
      font-size: 16.5px !important;
      font-weight: 700 !important;
      color: #fe2c55 !important;
      line-height: 1 !important;
      display: flex !important;
      align-items: baseline !important;
      gap: 1px !important;
    }

    #recommended-grid.produtos-layout-list .price-current-txt .currency {
      font-size: 11px !important;
      font-weight: 700 !important;
      color: #fe2c55 !important;
      margin-right: 1px !important;
    }

    #recommended-grid.produtos-layout-list .price-old-txt {
      font-size: 11px !important;
      color: #8a8b91 !important;
      text-decoration: line-through !important;
      margin-top: 2px !important;
      line-height: 1 !important;
      display: block !important;
    }
`;

html = html.replace('</head>', `<style>\n${fixStyles}\n</style>\n</head>`);

// 4. ATUALIZAR FUNÇÃO switchTab PARA RESETAR SCROLL E CONTROLAR ELEMENTOS COM PRECISÃO
const fixedSwitchTab = `
    function switchTab(btn, tab) {
      document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const mainSec = document.getElementById('principais-produtos-section');
      const novosSec = document.getElementById('novos-lancamentos-section');
      const recSec = document.getElementById('produtos-recomendados-section');
      const catSec = document.getElementById('categorias-section');
      const subBar = document.getElementById('subfilter-produtos-bar');
      const grid = document.getElementById('recommended-grid');
      const divider = document.querySelector('.divider-home-rec');

      // Garante que o scroll volte ao topo na troca de aba
      window.scrollTo(0, 0);

      if (tab === 'home') {
        if (mainSec) mainSec.style.display = 'block';
        if (novosSec) novosSec.style.display = 'block';
        if (recSec) recSec.style.display = 'block';
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'none';
        if (divider) divider.style.display = 'flex';
        if (grid) grid.classList.remove('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
      } else if (tab === 'produtos') {
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) recSec.style.display = 'block';
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'flex';
        if (divider) divider.style.display = 'none';
        if (grid) grid.classList.add('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
      } else if (tab === 'categorias') {
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) recSec.style.display = 'none';
        if (catSec) catSec.style.display = 'block';
        if (subBar) subBar.style.display = 'none';
      }
    }
`;

const swStart = html.indexOf('function switchTab');
const swEnd = html.indexOf('function filterByCategory');
if (swStart !== -1 && swEnd !== -1) {
  html = html.slice(0, swStart) + fixedSwitchTab + '\n\n    ' + html.slice(swEnd);
  console.log('✅ switchTab atualizado.');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('>>> [BRUNO CTO] BUGS ELIMINADOS COM SUCESSO! <<<');
