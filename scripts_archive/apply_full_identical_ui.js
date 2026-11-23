const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('Iniciando aplicação da UI 100% idêntica aos prints oficiais...');

// 1. CSS OFICIAL TIKTOK SHOP PERFEITO
const customStyles = `
    /* === CSS OFICIAL TIKTOK SHOP IDENTICO AOS PRINTS === */
    .badge-loja-estrela {
      display: inline-flex;
      align-items: center;
      background: #faeed7 !important;
      color: #8c5b08 !important;
      font-size: 10.5px !important;
      font-weight: 600 !important;
      padding: 2px 6px !important;
      border-radius: 4px !important;
      line-height: 1.2 !important;
    }

    /* Cupom Oficial */
    .coupons-container {
      margin-top: 10px;
      margin-bottom: 2px;
      padding: 0 16px;
    }

    .coupon-card-official {
      background: #eafbf7;
      border: 1px solid #d4f4ed;
      border-radius: 8px;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: relative;
    }

    .coupon-title {
      font-size: 13.5px;
      font-weight: 700;
      color: #161823;
      line-height: 1.2;
    }

    .coupon-sub {
      font-size: 11px;
      color: #6b7280;
      margin-top: 3px;
    }

    .coupon-resgatado-txt {
      font-size: 13px;
      font-weight: 600;
      color: #20b5a6;
      flex-shrink: 0;
    }

    /* Badge Frete Grátis Oficial */
    .badge-frete-gratis,
    .product-badge {
      display: inline-flex !important;
      align-items: center !important;
      background: #e6f9f6 !important;
      color: #00a699 !important;
      font-size: 10.5px !important;
      font-weight: 700 !important;
      padding: 1px 5px !important;
      border-radius: 3px !important;
      border: none !important;
      line-height: 1.3 !important;
    }

    /* Divisor com degradê rosa oficial (Print 4) */
    .divider-home-rec {
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 12px !important;
      font-size: 13.5px !important;
      font-weight: 600 !important;
      color: #161823 !important;
      margin: 14px 0 16px 0 !important;
      text-align: center !important;
    }

    .divider-home-rec::before {
      content: '' !important;
      height: 1.5px !important;
      flex: 1 !important;
      max-width: 36px !important;
      background: linear-gradient(to right, transparent, #fe2c55) !important;
    }

    .divider-home-rec::after {
      content: '' !important;
      height: 1.5px !important;
      flex: 1 !important;
      max-width: 36px !important;
      background: linear-gradient(to left, transparent, #fe2c55) !important;
    }

    /* Sub-barra de ordenação da aba Produtos (Print 1) */
    .subfilter-produtos-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 16px;
      background: #fafafa;
      border-bottom: 1px solid #f0f0f0;
      margin-bottom: 8px;
    }

    .subfilter-items {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .subfilter-item {
      font-size: 13px;
      color: #4b4d53;
      cursor: pointer;
      font-weight: 500;
    }

    .subfilter-item.active {
      color: #161823;
      font-weight: 700;
    }

    .subfilter-divider {
      color: #e5e5e5;
      font-size: 11px;
    }

    .subfilter-view-toggle {
      cursor: pointer;
      display: flex;
      align-items: center;
      color: #757575;
    }

    /* LAYOUT EMPILHADO DA ABA PRODUTOS (Print 1) */
    .produtos-layout-list {
      display: flex !important;
      flex-direction: column !important;
      gap: 16px !important;
      background: #fff !important;
      padding: 0 0 16px 0 !important;
    }

    .produtos-layout-list .product-card-rec {
      display: flex !important;
      flex-direction: row !important;
      align-items: center !important;
      background: #fff !important;
      border: none !important;
      border-radius: 0 !important;
      padding: 0 0 12px 0 !important;
      border-bottom: 1px solid #f7f7f8 !important;
      gap: 12px !important;
      width: 100% !important;
      text-decoration: none !important;
      color: inherit !important;
      height: auto !important;
    }

    .produtos-layout-list .product-card-rec > div {
      display: flex !important;
      flex-direction: row !important;
      width: 100% !important;
      border: none !important;
      border-radius: 0 !important;
      padding: 0 !important;
      gap: 12px !important;
      align-items: center !important;
    }

    .produtos-layout-list .product-card-rec img {
      width: 112px !important;
      height: 112px !important;
      min-width: 112px !important;
      max-width: 112px !important;
      aspect-ratio: 1/1 !important;
      object-fit: cover !important;
      border-radius: 8px !important;
      background: #f7f7f7 !important;
      flex-shrink: 0 !important;
    }

    .produtos-layout-list .product-card-rec .product-info-wrap {
      flex: 1 !important;
      min-width: 0 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      height: 112px !important;
      padding: 2px 0 !important;
    }

    .produtos-layout-list .product-card-rec .product-name {
      font-size: 13.5px !important;
      font-weight: 500 !important;
      color: #161823 !important;
      line-height: 1.3 !important;
      margin: 0 0 4px 0 !important;
      display: -webkit-box !important;
      -webkit-line-clamp: 2 !important;
      -webkit-box-orient: vertical !important;
      overflow: hidden !important;
      height: auto !important;
      max-height: 36px !important;
    }

    /* Linha de Avaliação: estrela amarela pequena + 4.7 | 9017 vendidos */
    .product-rating-row {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 11px;
      color: #8a8b91;
      margin-top: 3px;
    }

    .star-yellow {
      color: #ffaa00;
      font-size: 11px;
    }

    /* Linha de Preço e Botão Comprar Integrado */
    .price-and-action-row {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      width: 100%;
      margin-top: auto;
    }

    .price-stack {
      display: flex;
      flex-direction: column;
    }

    .price-current {
      font-size: 16px;
      font-weight: 700;
      color: #fe2c55;
      line-height: 1.1;
      display: flex;
      align-items: baseline;
      gap: 2px;
    }

    .price-current .currency {
      font-size: 12px;
      font-weight: 700;
      color: #fe2c55;
    }

    .price-old-striked {
      font-size: 11px;
      color: #8a8b91;
      text-decoration: line-through;
      line-height: 1.1;
      margin-top: 2px;
    }

    /* Botão Unificado [ 🛒 | Comprar ] Oficial */
    .unified-buy-btn {
      display: flex;
      align-items: stretch;
      background: #fe2c55;
      border-radius: 6px;
      overflow: hidden;
      height: 30px;
      box-shadow: 0 1px 3px rgba(254,44,85,0.2);
      flex-shrink: 0;
      cursor: pointer;
      text-decoration: none;
    }

    .unified-buy-btn .btn-cart-part {
      background: #fdf0f3;
      padding: 0 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: none;
      outline: none;
    }

    .unified-buy-btn .btn-txt-part {
      background: #fe2c55;
      color: #fff;
      font-size: 12px;
      font-weight: 700;
      padding: 0 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: none;
      outline: none;
      white-space: nowrap;
    }

    /* Oculta o botão no modo grade padrão da Home */
    #recommended-grid:not(.produtos-layout-list) .unified-buy-btn {
      display: none !important;
    }
`;

// Substituir ou injetar os estilos
if (!html.includes('badge-loja-estrela')) {
  html = html.replace('</head>', `<style>\n${customStyles}\n</style>\n</head>`);
} else {
  // Atualizar os estilos existentes
  html = html.replace('</head>', `<style>\n${customStyles}\n</style>\n</head>`);
}

console.log('✅ Estilos CSS aplicados com sucesso!');
fs.writeFileSync('index.html', html, 'utf8');
