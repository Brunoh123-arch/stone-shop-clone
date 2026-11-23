const fs = require('fs');
const path = require('path');

const cssPath = path.join(__dirname, '../css/style.css');
let css = fs.readFileSync(cssPath, 'utf8');

const newPriceCss = `
/* ========================================================================== */
/* 🔥 TIKTOK SHOP OFICIAL: BARRA RELÂMPAGO, PREÇO, PARCELAMENTO & TÍTULO 🔥  */
/* ========================================================================== */

.price-section {
  background: linear-gradient(90deg, #ff4c00 0%, #ff3b00 60%, #ff2a00 100%) !important;
  position: relative !important;
  width: 100% !important;
  min-height: 54px !important;
  aspect-ratio: auto !important;
  padding: 8px 12px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.price-section::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 55%;
  height: 100%;
  background: radial-gradient(circle at 100% 0%, rgba(255, 255, 255, 0.16) 0%, transparent 60%);
  pointer-events: none;
}

.price-left {
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  gap: 2px !important;
  z-index: 2 !important;
  position: static !important;
}

.price-main-row, .price-row {
  display: flex !important;
  align-items: baseline !important;
  gap: 2px !important;
  position: static !important;
}

/* 1. Badge de Desconto: Branco com cantos 4px e texto carmim/framboesa */
.discount-badge-white {
  position: static !important;
  background: #ffffff !important;
  color: #a82d49 !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  padding: 3px 5px !important;
  border-radius: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  box-sizing: border-box !important;
  margin-right: 4px !important;
  align-self: center !important;
}

/* 2. Rótulo "R$" */
.price-currency, .price-label-apartir {
  position: static !important;
  color: #ffffff !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  letter-spacing: -0.2px !important;
  white-space: nowrap !important;
  margin-right: 2px !important;
  display: inline-block !important;
}

/* 3. Preço Principal Grande (Ex: 75,00) */
.price-current {
  position: static !important;
  color: #ffffff !important;
  font-size: 28px !important;
  font-weight: 800 !important;
  line-height: 1 !important;
  letter-spacing: -0.5px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
  display: inline-flex !important;
  align-items: baseline !important;
}

.price-current span, .price-current .p-int {
  font-size: 28px !important;
  font-weight: 800 !important;
  line-height: 1 !important;
}

.price-current .p-dec {
  font-size: 14px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  align-self: flex-start !important;
  padding-top: 2px !important;
}

/* 4. Preço Original Riscado */
.price-original-row {
  display: flex !important;
  align-items: center !important;
  margin-top: 1px !important;
}

.price-original {
  position: static !important;
  color: rgba(255, 255, 255, 0.72) !important;
  font-size: 12.5px !important;
  font-weight: 400 !important;
  line-height: 1 !important;
  text-decoration: line-through !important;
  text-decoration-color: rgba(255, 255, 255, 0.72) !important;
}

/* 5. Lado Direito: Oferta Relâmpago + Timer */
.price-right {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-end !important;
  justify-content: center !important;
  gap: 3px !important;
  z-index: 2 !important;
  position: static !important;
}

.flash-title-row {
  display: flex !important;
  align-items: center !important;
  gap: 3px !important;
  color: #ffffff !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
}

.flash-bolt-icon {
  width: 15px !important;
  height: 15px !important;
  fill: #ffe100 !important;
  filter: drop-shadow(0 0 2px rgba(255, 225, 0, 0.6)) !important;
}

.flash-timer-row, .timer-row {
  position: static !important;
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  line-height: 1 !important;
  margin-top: 1px !important;
}

.timer-label {
  display: inline-block !important;
  color: rgba(255, 255, 255, 0.85) !important;
  font-size: 11.5px !important;
  font-weight: 400 !important;
  letter-spacing: -0.1px !important;
}

.timer-value, .oferta-timer {
  color: #ffffff !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  letter-spacing: 0.2px !important;
}

/* ===== LINHA DE PARCELAMENTO ===== */
.installment-row {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 6px !important;
  margin: 10px 0 !important;
  cursor: pointer !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

.installment-left {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.installment-icon {
  width: 17px !important;
  height: 17px !important;
  color: #161823 !important;
  flex-shrink: 0 !important;
}

.installment-text {
  font-size: 13px !important;
  font-weight: 400 !important;
  color: #161823 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

.installment-text .sem-juros {
  color: #a82d49 !important;
  font-weight: 400 !important;
  margin-left: 3px !important;
}

.installment-arrow {
  color: #73747b !important;
  font-size: 14px !important;
  margin-left: auto !important;
}

/* ===== TÍTULO DO PRODUTO ===== */
.product-title-row {
  display: flex !important;
  align-items: flex-start !important;
  justify-content: space-between !important;
  gap: 12px !important;
  margin: 4px 0 8px 0 !important;
}

.product-title {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  line-height: 1.35 !important;
  color: #161823 !important;
  letter-spacing: -0.15px !important;
  margin: 0 !important;
  flex: 1 !important;
}

.bookmark-btn {
  background: none !important;
  border: none !important;
  padding: 1px 0 0 0 !important;
  cursor: pointer !important;
  color: #161823 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  flex-shrink: 0 !important;
}

.bookmark-btn svg {
  width: 18px !important;
  height: 18px !important;
  stroke: #161823 !important;
  stroke-width: 1.8 !important;
  fill: none !important;
}

/* ===== AVALIAÇÕES E VENDIDOS ===== */
.ratings-row {
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
  margin-bottom: 12px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

.star-icon {
  fill: #f6b100 !important;
  width: 13px !important;
  height: 13px !important;
  flex-shrink: 0 !important;
}

.rating-score {
  font-size: 13px !important;
  font-weight: 700 !important;
  color: #161823 !important;
}

.rating-count {
  font-size: 13px !important;
  font-weight: 400 !important;
  color: #2b5c8f !important;
  cursor: pointer !important;
}

.ratings-divider {
  color: #e5e5e5 !important;
  font-size: 11px !important;
  margin: 0 3px !important;
  user-select: none !important;
}

.sold-count {
  font-size: 13px !important;
  color: #73747b !important;
  font-weight: 400 !important;
}
`;

// Remove previous injection if exists
const marker = '/* 🔥 TIKTOK SHOP OFICIAL: BARRA RELÂMPAGO, PREÇO, PARCELAMENTO & TÍTULO 🔥  */';
if (css.includes(marker)) {
  const parts = css.split(marker);
  css = parts[0];
}

css = css + '\n\n' + newPriceCss;
fs.writeFileSync(cssPath, css, 'utf8');
console.log('✅ css/style.css atualizado com o CSS Oficial TikTok Shop!');
