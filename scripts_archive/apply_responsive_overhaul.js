const fs = require('fs');
const path = require('path');

const responsiveCss = `
/* ========================================================================== */
/* 📱 OVERHAUL DE RESPONSIVIDADE BLINDADA (MOBILE-FIRST FLUIDO 320px - 1440px) */
/* ========================================================================== */

html, body {
  overflow-x: hidden !important;
  width: 100% !important;
  max-width: 100vw !important;
  background-color: #f0f2f5 !important;
}

.app-container, .container, #root {
  width: 100% !important;
  max-width: 480px !important;
  margin: 0 auto !important;
  min-height: 100vh !important;
  background-color: #ffffff !important;
  position: relative !important;
  box-sizing: border-box !important;
  overflow-x: hidden !important;
}

@media (min-width: 481px) {
  .app-container {
    box-shadow: 0 0 30px rgba(0, 0, 0, 0.08) !important;
  }
}

.header {
  position: fixed !important;
  top: 0 !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  width: 100% !important;
  max-width: 480px !important;
  height: 52px !important;
  padding: 0 clamp(8px, 2.5vw, 16px) !important;
  display: flex !important;
  align-items: center !important;
  gap: clamp(6px, 2vw, 10px) !important;
  background: #ffffff !important;
  border-bottom: 1px solid #f0f0f0 !important;
  z-index: 100 !important;
  box-sizing: border-box !important;
}

.header-back-btn {
  flex-shrink: 0 !important;
  min-width: 28px !important;
  padding: 4px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.header-search-wrapper {
  flex: 1 !important;
  min-width: 0 !important;
  position: relative !important;
}

.header-search {
  width: 100% !important;
  height: 36px !important;
  background: #f1f1f2 !important;
  border: none !important;
  border-radius: 6px !important;
  padding: 0 12px 0 34px !important;
  font-size: clamp(13px, 3.5vw, 14.5px) !important;
  color: #161823 !important;
  box-sizing: border-box !important;
}

.header-search-icon-btn {
  position: absolute !important;
  left: 8px !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: none !important;
  border: none !important;
  padding: 0 !important;
  color: #73747b !important;
}

.header-icons {
  display: flex !important;
  align-items: center !important;
  gap: clamp(6px, 2vw, 12px) !important;
  flex-shrink: 0 !important;
}

.header-icon-btn, .header-share-btn, .header-more-btn {
  padding: 4px !important;
  background: none !important;
  border: none !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
}

.store-section {
  padding: clamp(10px, 3vw, 16px) !important;
  margin-top: 0 !important;
  background: #ffffff !important;
  border-bottom: 1px solid #f0f0f0 !important;
  box-sizing: border-box !important;
}

.store-section > div {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: clamp(8px, 2.5vw, 16px) !important;
  width: 100% !important;
}

.store-section .store-left, .store-section > div > div:first-child {
  display: flex !important;
  align-items: center !important;
  gap: clamp(8px, 2vw, 12px) !important;
  min-width: 0 !important;
  flex: 1 !important;
}

.store-section img {
  width: clamp(48px, 13vw, 58px) !important;
  height: clamp(48px, 13vw, 58px) !important;
  border-radius: 50% !important;
  object-fit: cover !important;
  flex-shrink: 0 !important;
}

.store-section h2 {
  font-size: clamp(14px, 4vw, 16px) !important;
  font-weight: 700 !important;
  color: #161823 !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.badge-loja-estrela {
  font-size: clamp(10px, 2.8vw, 11px) !important;
  padding: 1px 5px !important;
  border-radius: 3px !important;
}

.store-buttons, .store-section > div > div:last-child {
  display: flex !important;
  flex-direction: column !important;
  gap: 5px !important;
  flex-shrink: 0 !important;
}

.store-buttons button, .store-section button {
  height: clamp(28px, 7vw, 32px) !important;
  padding: 0 clamp(10px, 3vw, 18px) !important;
  font-size: clamp(11.5px, 3vw, 13px) !important;
  border-radius: 16px !important;
  white-space: nowrap !important;
}

.coupons-container {
  display: flex !important;
  gap: 8px !important;
  padding: 8px clamp(10px, 3vw, 16px) !important;
  overflow-x: auto !important;
  -webkit-overflow-scrolling: touch !important;
  scrollbar-width: none !important;
  box-sizing: border-box !important;
}
.coupons-container::-webkit-scrollbar { display: none !important; }

.coupon-card-official {
  flex-shrink: 0 !important;
  min-width: clamp(200px, 60vw, 260px) !important;
  max-width: 90vw !important;
  box-sizing: border-box !important;
}

.nav-tabs {
  display: flex !important;
  justify-content: space-around !important;
  border-bottom: 1px solid #f0f0f0 !important;
  padding: 0 clamp(8px, 2vw, 16px) !important;
  background: #ffffff !important;
  box-sizing: border-box !important;
}

.nav-tab {
  padding: 12px clamp(6px, 2vw, 14px) !important;
  font-size: clamp(13px, 3.8vw, 15px) !important;
  font-weight: 500 !important;
  color: #73747b !important;
  white-space: nowrap !important;
}

.nav-tab.active {
  color: #161823 !important;
  font-weight: 700 !important;
  border-bottom: 2px solid #161823 !important;
}

#principais-produtos-section {
  padding: clamp(10px, 3vw, 16px) !important;
  box-sizing: border-box !important;
}

#principais-produtos-section > div:last-child {
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  gap: clamp(4px, 1.8vw, 8px) !important;
  box-sizing: border-box !important;
}

.principais-prod-title {
  font-size: clamp(11px, 2.9vw, 13px) !important;
  line-height: 1.3 !important;
  min-height: 2.6em !important;
  display: -webkit-box !important;
  -webkit-line-clamp: 2 !important;
  -webkit-box-orient: vertical !important;
  overflow: hidden !important;
  word-break: break-word !important;
  margin: 4px 0 !important;
}

.principais-price-stack {
  display: flex !important;
  flex-direction: column !important;
  gap: 1px !important;
  margin-bottom: 2px !important;
}

.principais-price-cur {
  font-size: clamp(13px, 3.8vw, 16px) !important;
  font-weight: 700 !important;
  white-space: nowrap !important;
}

.principais-price-old {
  font-size: clamp(9.5px, 2.6vw, 11px) !important;
  white-space: nowrap !important;
}

.principais-sales-txt {
  font-size: clamp(9.5px, 2.6vw, 11px) !important;
  white-space: nowrap !important;
}

.badge-frete-gratis {
  font-size: clamp(8.5px, 2.3vw, 10px) !important;
  padding: 1px 3px !important;
  white-space: nowrap !important;
}

#novos-lancamentos-section {
  padding: clamp(10px, 3vw, 16px) !important;
  box-sizing: border-box !important;
}

#novos-lancamentos-section a {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: clamp(8px, 2.5vw, 14px) !important;
  box-sizing: border-box !important;
}

#novos-lancamentos-section img {
  width: clamp(70px, 18vw, 88px) !important;
  height: clamp(70px, 18vw, 88px) !important;
  border-radius: 8px !important;
  flex-shrink: 0 !important;
}

#recommended-grid {
  display: grid !important;
  grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  gap: clamp(6px, 2vw, 10px) !important;
  padding: 0 clamp(8px, 2vw, 12px) 16px clamp(8px, 2vw, 12px) !important;
  box-sizing: border-box !important;
  width: 100% !important;
}

.product-card-rec {
  min-width: 0 !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-between !important;
}

.product-card-rec img {
  width: 100% !important;
  aspect-ratio: 1 / 1 !important;
  object-fit: cover !important;
}

.product-card-rec .product-name {
  font-size: clamp(11.5px, 3.2vw, 13px) !important;
  line-height: 1.35 !important;
  height: 2.7em !important;
  display: -webkit-box !important;
  -webkit-line-clamp: 2 !important;
  -webkit-box-orient: vertical !important;
  overflow: hidden !important;
}

.home-bottom-bar, .bottom-nav {
  position: fixed !important;
  bottom: 0 !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  width: 100% !important;
  max-width: 480px !important;
  box-sizing: border-box !important;
  z-index: 999 !important;
}
`;

// 1. Atualizar index.html
const indexPath = path.join(__dirname, '../index.html');
let indexHtml = fs.readFileSync(indexPath, 'utf8');

// Remover padding-top duplicado no #root
indexHtml = indexHtml.replace(/padding-top:\s*56px;/g, 'padding-top: 0px;');

// Injetar CSS responsivo antes de </style>
const styleEndTag = '</style>';
if (indexHtml.includes(styleEndTag)) {
  const parts = indexHtml.split(styleEndTag);
  // Remove anterior se já existir
  const cleanPart = parts[0].split('/* ========================================================================== */\n/* 📱 OVERHAUL DE RESPONSIVIDADE BLINDADA')[0];
  indexHtml = cleanPart + '\n' + responsiveCss + '\n' + styleEndTag + parts.slice(1).join(styleEndTag);
  fs.writeFileSync(indexPath, indexHtml, 'utf8');
  console.log('✅ index.html atualizado com responsividade total fluida!');
}

// 2. Atualizar css/style.css para que as outras páginas também herdem
const styleCssPath = path.join(__dirname, '../css/style.css');
let styleCss = fs.readFileSync(styleCssPath, 'utf8');
const cleanStyle = styleCss.split('/* ========================================================================== */\n/* 📱 OVERHAUL DE RESPONSIVIDADE BLINDADA')[0];
styleCss = cleanStyle + '\n\n' + responsiveCss;
fs.writeFileSync(styleCssPath, styleCss, 'utf8');
console.log('✅ css/style.css atualizado com regras de responsividade!');
