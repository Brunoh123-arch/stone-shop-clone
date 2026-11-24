const fs = require('fs');
const path = require('path');

const dir = 'C:\\Users\\Dell\\Downloads\\stone_shop_clone\\pages';
const files = fs.readdirSync(dir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));

const patterns = {};
const samples = {};

files.forEach(f => {
  const content = fs.readFileSync(path.join(dir, f), 'utf8');
  const start = content.indexOf('<div class="price-section"');
  if (start !== -1) {
    const end = content.indexOf('<!-- INFO', start);
    const section = content.slice(start, end !== -1 ? end : start + 600);
    const hasDiscountInRow = section.includes('price-row') && section.indexOf('discount-badge') > section.indexOf('price-row');
    const hasApartir = section.includes('price-label-apartir');
    const hasDiscountDirect = section.includes('discount-badge-white') && !hasDiscountInRow;
    const key = `inRow:${hasDiscountInRow}_hasApartir:${hasApartir}_direct:${hasDiscountDirect}`;
    patterns[key] = (patterns[key] || 0) + 1;
    if (!samples[key]) samples[key] = f;
  } else {
    patterns['no_price_section'] = (patterns['no_price_section'] || 0) + 1;
  }
});

console.log('Patterns:', patterns);
console.log('Samples:', samples);
