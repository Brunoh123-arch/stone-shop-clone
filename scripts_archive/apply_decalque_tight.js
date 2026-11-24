const fs = require('fs');
const path = 'C:/Users/Dell/Downloads/stone_shop_clone/css/style.css';
let css = fs.readFileSync(path, 'utf8');

const decalquePriceCss = `/* ===== PRICE SECTION (DECALQUE OFICIAL COM ALINHAMENTO COLADO) ===== */
.price-section {
  background-image: url('../decalque/decalque-oferta.jpg') !important;
  background-size: 100% 100% !important;
  background-repeat: no-repeat !important;
  background-position: center center !important;
  position: relative !important;
  width: 100% !important;
  aspect-ratio: 1320 / 180 !important;
  overflow: hidden !important;
  box-sizing: border-box !important;
  display: block !important;
  height: auto !important;
  min-height: unset !important;
  padding: 0 !important;
}

.price-section::before, .price-section::after {
  display: none !important;
}

/* 1. Caixinha de desconto branca do decalque */
.discount-badge-white {
  position: absolute !important;
  left: 3.8% !important;
  top: 13.5% !important;
  width: 9.8% !important;
  height: 38% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  background: transparent !important;
  color: #a82d49 !important;
  font-size: clamp(12px, 3.4vw, 15px) !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  text-align: center !important;
  box-sizing: border-box !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* 2. PREÇO COLADO DO LADO DA CAIXINHA (SEM BURACO!) */
.price-row, .price-combined {
  position: absolute !important;
  left: 14.2% !important;
  top: 12% !important;
  height: 40% !important;
  display: flex !important;
  align-items: baseline !important;
  gap: 3px !important;
  line-height: 1 !important;
  z-index: 2 !important;
  margin: 0 !important;
  padding: 0 !important;
}

.price-currency-sign, .price-label-apartir {
  position: static !important;
  color: #ffffff !important;
  font-size: clamp(12px, 3.3vw, 14.5px) !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  margin: 0 !important;
  padding: 0 !important;
  align-self: baseline !important;
}

.price-current, .price-main-val {
  position: static !important;
  color: #ffffff !important;
  font-size: clamp(18px, 6.0vw, 28px) !important;
  font-weight: 800 !important;
  letter-spacing: -0.5px !important;
  line-height: 1 !important;
  margin: 0 !important;
  padding: 0 !important;
  display: inline-flex !important;
  align-items: baseline !important;
}

.price-current span, .price-cents-val, .price-current .price-cents {
  font-size: clamp(12px, 3.6vw, 15px) !important;
  font-weight: 700 !important;
  line-height: 1 !important;
  margin-left: 0.5px !important;
  color: #ffffff !important;
}

/* 3. Preço original riscado abaixo da caixinha de desconto */
.price-original {
  position: absolute !important;
  left: 3.8% !important;
  top: 56% !important;
  color: rgba(255, 255, 255, 0.75) !important;
  font-size: clamp(10px, 2.7vw, 13px) !important;
  text-decoration: line-through !important;
  font-weight: 400 !important;
  line-height: 1 !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* 4. Timer do lado direito */
.price-right {
  display: block !important;
  position: static !important;
}

.timer-row {
  position: absolute !important;
  right: 5.5% !important;
  top: 61% !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
  line-height: 1 !important;
  margin: 0 !important;
}

.timer-label {
  display: inline-block !important;
  color: rgba(255, 255, 255, 0.88) !important;
  font-size: clamp(10.5px, 2.7vw, 14px) !important;
  font-weight: 400 !important;
  letter-spacing: -0.2px !important;
}

.timer-value {
  color: #ffffff !important;
  font-size: clamp(11px, 2.8vw, 14.5px) !important;
  font-weight: 700 !important;
  font-variant-numeric: tabular-nums !important;
  letter-spacing: 0.2px !important;
}
`;

const p1 = css.indexOf('/* ===== PRICE SECTION');
const p2 = css.indexOf('/* ===== PRODUCT INFO ===== */');

if (p1 !== -1 && p2 !== -1) {
  css = css.slice(0, p1) + decalquePriceCss + '\n\n' + css.slice(p2);
  console.log('Decalque price section injected successfully.');
} else {
  console.error('Could not find markers');
}

fs.writeFileSync(path, css, 'utf8');
console.log('Saved style.css successfully.');
