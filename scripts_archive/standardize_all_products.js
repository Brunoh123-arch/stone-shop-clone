const fs = require('fs');
const path = require('path');

const dir = 'C:\\Users\\Dell\\Downloads\\stone_shop_clone\\pages';
const files = fs.readdirSync(dir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));

let updatedCount = 0;

files.forEach(f => {
  const filePath = path.join(dir, f);
  let html = fs.readFileSync(filePath, 'utf8');

  // Regex para achar a price-section inteira
  const startIdx = html.indexOf('<div class="price-section"');
  if (startIdx === -1) return;

  // Acha o fim da price-section procurando pelo próximo comentário de seção (<!-- INFO ou <!-- INFORMAÇÕES)
  const infoMatch = html.slice(startIdx).match(/<!--\s*INFO/i);
  if (!infoMatch) return;
  const endIdx = startIdx + infoMatch.index;

  const sectionRaw = html.slice(startIdx, endIdx);

  // Extrair Desconto
  let discount = '-50%';
  const discM = sectionRaw.match(/class=["']discount-badge-white["'][^>]*>([^<]+)</i);
  if (discM) {
    discount = discM[1].trim();
  }

  // Extrair Preço Atual
  let priceStr = '0,00';
  const curM = sectionRaw.match(/class=["']price-current["'][^>]*>([\s\S]*?)<\/div>/i);
  if (curM) {
    // Limpa tags e R$
    priceStr = curM[1].replace(/<[^>]*>/g, '').replace(/R\$\s*/gi, '').trim();
  }

  let intPart = '0';
  let centsPart = '00';
  if (priceStr.includes(',')) {
    const parts = priceStr.split(',');
    intPart = parts[0].trim();
    centsPart = parts[1].trim().slice(0, 2);
  } else if (priceStr.includes('.')) {
    const parts = priceStr.split('.');
    intPart = parts[0].trim();
    centsPart = parts[1].trim().slice(0, 2);
  } else {
    intPart = priceStr.trim();
  }

  // Extrair Preço Original
  let origPrice = 'R$ 0,00';
  const origM = sectionRaw.match(/class=["']price-original["'][^>]*>([\s\S]*?)<\/div>/i);
  if (origM) {
    origPrice = origM[1].replace(/<[^>]*>/g, '').trim();
    if (!origPrice.startsWith('R$')) origPrice = 'R$ ' + origPrice;
  }

  // Extrair Timer
  let timerVal = '04:00:00';
  const timerM = sectionRaw.match(/class=["'][^"']*oferta-timer[^"']*["'][^>]*>([^<]+)</i);
  if (timerM) {
    timerVal = timerM[1].trim();
  }

  const newSection = `    <!-- SEÇÃO DE PREÇO / OFERTA RELÂMPAGO (COM O DECALQUE OFICIAL) -->
    <div class="price-section">
      <div class="discount-badge-white">${discount}</div>
      <div class="price-row">
        <span class="price-currency-sign">R$</span>
        <div class="price-current">${intPart}<span class="price-cents">,${centsPart}</span></div>
      </div>
      <div class="price-original">${origPrice}</div>
      <div class="price-right">
        <div class="timer-row">
          <span class="timer-label">Termina em</span>
          <span class="timer-value oferta-timer">${timerVal}</span>
        </div>
      </div>
    </div>\n\n    `;

  html = html.slice(0, startIdx) + newSection + html.slice(endIdx);
  fs.writeFileSync(filePath, html, 'utf8');
  updatedCount++;
});

console.log(`Successfully standardized price section in ${updatedCount} products!`);
