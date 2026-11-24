const fs = require('fs');
const path = 'C:/Users/Dell/Downloads/stone_shop_clone/css/style.css';
let css = fs.readFileSync(path, 'utf8');

const newPriceCss = `/* ===== PRICE SECTION / OFERTA RELÂMPAGO TIKTOK SHOP OFICIAL (100% IDÊNTICO AO PRINT 2) ===== */
.price-section {
  background: linear-gradient(100deg, #ff4c00 0%, #ff5700 50%, #ff6400 100%) !important;
  position: relative !important;
  width: 100% !important;
  min-height: 52px !important;
  height: 52px !important;
  aspect-ratio: auto !important;
  padding: 0 14px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  box-sizing: border-box !important;
  overflow: hidden !important;
}

.price-section::after {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 45% !important;
  background: radial-gradient(circle at 85% 30%, rgba(255, 255, 255, 0.16) 0%, transparent 60%) !important;
  pointer-events: none !important;
}

.price-left {
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  gap: 1px !important;
  position: static !important;
  z-index: 2 !important;
}

.price-row {
  display: flex !important;
  align-items: baseline !important;
  gap: 5px !important;
  position: static !important;
  line-height: 1 !important;
}

.discount-badge-white {
  position: static !important;
  background: #ffffff !important;
  color: #b51842 !important; /* Carmim TikTok Shop oficial */
  font-size: 13px !important;
  font-weight: 700 !important;
  padding: 1.5px 5px !important;
  border-radius: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  line-height: 1.1 !important;
  align-self: center !important;
  width: auto !important;
  height: auto !important;
  margin: 0 !important;
  box-sizing: border-box !important;
}

.price-currency-sign, .price-label-apartir {
  position: static !important;
  color: #ffffff !important;
  font-size: 13.5px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  margin: 0 !important;
  padding: 0 !important;
  align-self: baseline !important;
  letter-spacing: -0.2px !important;
}

.price-current {
  position: static !important;
  color: #ffffff !important;
  font-size: 26px !important;
  font-weight: 800 !important;
  line-height: 1 !important;
  letter-spacing: -0.5px !important;
  margin: 0 !important;
  padding: 0 !important;
  display: inline-flex !important;
  align-items: baseline !important;
}

.price-current span, .price-current .price-cents {
  font-size: 14.5px !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  margin-left: 0.5px !important;
  color: #ffffff !important;
}

.price-original {
  position: static !important;
  color: rgba(255, 255, 255, 0.72) !important;
  font-size: 11.5px !important;
  font-weight: 400 !important;
  text-decoration: line-through !important;
  line-height: 1.1 !important;
  margin-top: 2px !important;
  margin-left: 1px !important;
}

.price-right {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-end !important;
  justify-content: center !important;
  gap: 2px !important;
  position: static !important;
  z-index: 2 !important;
}

.oferta-header {
  display: flex !important;
  align-items: center !important;
  gap: 3px !important;
}

.oferta-title {
  color: #ffffff !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  letter-spacing: -0.2px !important;
  line-height: 1.2 !important;
}

.oferta-bolt {
  display: inline-block !important;
  vertical-align: middle !important;
}

.timer-row {
  position: static !important;
  display: flex !important;
  align-items: center !important;
  gap: 4px !important;
  line-height: 1 !important;
  margin: 0 !important;
}

.timer-label {
  color: rgba(255, 255, 255, 0.9) !important;
  font-size: 11.5px !important;
  font-weight: 500 !important;
  letter-spacing: -0.2px !important;
}

.timer-value {
  color: #ffffff !important;
  font-size: 12px !important;
  font-weight: 700 !important;
  font-variant-numeric: tabular-nums !important;
  letter-spacing: 0.2px !important;
}
`;

const p1 = css.indexOf('/* ===== PRICE SECTION (decalque oficial) ===== */');
const p2 = css.indexOf('/* ===== PRODUCT INFO ===== */');

if (p1 !== -1 && p2 !== -1) {
  css = css.slice(0, p1) + newPriceCss + '\n\n' + css.slice(p2);
  console.log('Main price section replaced successfully.');
} else {
  console.error('Could not find markers p1 or p2');
}

// Remove conflicting media query rules that set .price-current { left: 36.2% ... }
const pMedia = css.indexOf('/* Preço Principal Grande */');
if (pMedia !== -1) {
  const pMediaEnd = css.indexOf('/* 5. Container do Timer (Lado Direito) */', pMedia);
  if (pMediaEnd !== -1) {
    css = css.slice(0, pMedia) + css.slice(pMediaEnd);
    console.log('Removed conflicting media query rules.');
  }
}

fs.writeFileSync(path, css, 'utf8');
console.log('Saved style.css successfully.');
