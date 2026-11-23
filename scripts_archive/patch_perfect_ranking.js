const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Ajustar o card do Cupom para não cortar o "109"
const oldCoupon = `<div class="coupon-card" style="position: relative; display: flex; align-items: center; justify-content: space-between; width: 100%; height: 56px; padding: 10px 14px; background: #e8f8f5; border-radius: 8px; overflow: hidden; box-sizing: border-box;">`;
const newCoupon = `<div class="coupon-card" style="position: relative; display: flex; align-items: center; justify-content: space-between; width: 100%; min-height: 62px; height: 62px; padding: 8px 14px; background: #e8f8f5; border-radius: 8px; overflow: hidden; box-sizing: border-box;">`;

html = html.replace(oldCoupon, newCoupon);

// 2. Atualizar as imagens da seção principais-produtos-section para as locais seguras
html = html.replace(
  'src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/ef0c4879de7a44f4955799ce3a17e13e~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"',
  'src="img/ranking-top1.webp"'
);

html = html.replace(
  'src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/66d3a87ec7e8424b94f06ddfd71bc391~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"',
  'src="img/ranking-top2.webp"'
);

html = html.replace(
  'src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/218cb51a37c34fca92f1683be83c4b9a~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"',
  'src="img/ranking-top3.webp"'
);

html = html.replace(
  'src="https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/5135cb7416344aa18e950ceee9ff304d~tplv-o3syd03w52-resize-jpeg:800:800.jpeg"',
  'src="img/ranking-novo.webp"'
);

// Adicionar referrerpolicy="no-referrer" e onerror fallback para nunca quebrar imagem
html = html.replace(
  /<img src="img\/ranking-([^"]+)" alt="([^"]+)" loading="lazy"/g,
  '<img src="img/ranking-$1" alt="$2" loading="lazy" referrerpolicy="no-referrer"'
);

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ index.html ajustado com imagens locais do ranking e cupom perfeito!');
