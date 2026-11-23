const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

// Achar elementos com width fixo grande no index.html
const fixedWidths = html.match(/style="[^"]*width:\s*\d{3,}px[^"]*"/g);
console.log('Fixed widths in index.html:', fixedWidths ? fixedWidths.slice(0, 10) : 'none');

// Checar overflow horizontal no body/container
console.log('Has horizontal scroll prevention:', html.includes('overflow-x'));

// Checar no css/original_index.css
const cssIndex = fs.readFileSync('css/original_index.css', 'utf8');
const lines = cssIndex.split('\n');
console.log('Lines in original_index.css with px widths:');
lines.forEach((l, idx) => {
  if (l.match(/width:\s*[2-9]\d{2,}px/)) {
    console.log((idx+1) + ': ' + l.trim());
  }
});
