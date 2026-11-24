const fs = require('fs');
const path = require('path');

const dir = 'C:\\Users\\Dell\\Downloads\\stone_shop_clone\\pages';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let updatedCount = 0;

const newBuyNowCode = `function handleBuyNow() {
  if (typeof handleAddToCartWithVariacoes === 'function' && typeof PRODUTO_ATUAL !== 'undefined') {
    handleAddToCartWithVariacoes(PRODUTO_ATUAL, true);
  } else if (typeof irDiretoAoCheckoutComProduto === 'function' && typeof PRODUTO_ATUAL !== 'undefined') {
    irDiretoAoCheckoutComProduto(PRODUTO_ATUAL, '', 1);
  } else {
    if (typeof PRODUTO_ATUAL !== 'undefined') addToCart(PRODUTO_ATUAL);
    window.location.href = 'resumo.html';
  }
}`;

files.forEach(f => {
  const filePath = path.join(dir, f);
  let html = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // Replace function handleBuyNow() { ... }
  if (html.includes('function handleBuyNow')) {
    html = html.replace(/function\s+handleBuyNow\s*\(\)\s*\{[\s\S]*?\n\}/g, newBuyNowCode);
    changed = true;
  }

  // Also replace any standalone window.location.href = '...carrinho.html' inside handleBuyNow if left
  if (html.includes("window.location.href = 'carrinho.html'") || html.includes('window.location.href = "../pages/carrinho.html"')) {
    // Only in product pages
    if (f.startsWith('produto-') || f === 'template-produto.html') {
      html = html.replace(/window\.location\.href\s*=\s*['"](\.\.\/pages\/)?carrinho\.html['"];?/g, (match, p1, offset, full) => {
        // Only if it's inside a script block for buying
        const before = full.slice(Math.max(0, offset - 100), offset);
        if (before.includes('handleBuyNow') || before.includes('buyNow') || before.includes('comprar')) {
          return "window.location.href = 'resumo.html';";
        }
        return match;
      });
      changed = true;
    }
  }

  if (changed) {
    fs.writeFileSync(filePath, html, 'utf8');
    updatedCount++;
  }
});

console.log(`Updated handleBuyNow in ${updatedCount} files.`);
