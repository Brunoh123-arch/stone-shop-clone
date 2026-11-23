const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('>>> [BRUNO CTO] POLIMENTO FINAL DE PRECISÃO CIRÚRGICA <<<');

// 1. AJUSTAR O PADDING-TOP DO ROOT E MARGIN DO STORE-SECTION PARA NUNCA CORTAR O HEADER
html = html.replace(/<div id="root"[^>]*>/i, '<div id="root" style="max-width: 480px; margin: 0 auto; min-height: 100vh; background: #f8f8f8; padding-top: 56px;">');

// 2. CSS PARA GARANTIR QUE .divider-home-rec NUNCA APAREÇA NA ABA PRODUTOS
const dividerFixCss = `
    /* Garante que o topo da loja nunca fique coberto */
    .store-section {
      margin-top: 4px !important;
      padding-top: 10px !important;
    }

    /* Oculta o divisor "Recomendado para você" SEMPRE que a lista da aba produtos estiver ativa */
    #recommended-grid.produtos-layout-list ~ .divider-home-rec,
    .hide-home-divider {
      display: none !important;
    }

    /* Na aba produtos, o divisor fica oculto */
    body.is-tab-produtos .divider-home-rec {
      display: none !important;
    }
`;

html = html.replace('</head>', `<style>\n${dividerFixCss}\n</style>\n</head>`);

// 3. ATUALIZAR switchTab PARA OCULTAR O DIVISOR E CONTROLAR CLASSE NO BODY
const switchTabPolished = `
    function switchTab(btn, tab) {
      document.querySelectorAll('.nav-tab').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const mainSec = document.getElementById('principais-produtos-section');
      const novosSec = document.getElementById('novos-lancamentos-section');
      const recSec = document.getElementById('produtos-recomendados-section');
      const catSec = document.getElementById('categorias-section');
      const subBar = document.getElementById('subfilter-produtos-bar');
      const grid = document.getElementById('recommended-grid');
      const divider = document.querySelector('.divider-home-rec');

      // Reseta scroll para o topo absoluto
      window.scrollTo({ top: 0, behavior: 'instant' });

      if (tab === 'home') {
        document.body.classList.remove('is-tab-produtos');
        if (mainSec) mainSec.style.display = 'block';
        if (novosSec) novosSec.style.display = 'block';
        if (recSec) recSec.style.display = 'block';
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'none';
        if (divider) divider.style.setProperty('display', 'flex', 'important');
        if (grid) grid.classList.remove('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
      } else if (tab === 'produtos') {
        document.body.classList.add('is-tab-produtos');
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) recSec.style.display = 'block';
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'flex';
        if (divider) divider.style.setProperty('display', 'none', 'important');
        if (grid) grid.classList.add('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
      } else if (tab === 'categorias') {
        document.body.classList.remove('is-tab-produtos');
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) recSec.style.display = 'none';
        if (catSec) catSec.style.display = 'block';
        if (subBar) subBar.style.display = 'none';
      }
    }
`;

const sw1 = html.indexOf('function switchTab');
const sw2 = html.indexOf('function filterByCategory');
if (sw1 !== -1 && sw2 !== -1) {
  html = html.slice(0, sw1) + switchTabPolished + '\n\n    ' + html.slice(sw2);
  console.log('✅ switchTab ajustado para reset de scroll e ocultação instantânea do divisor!');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ index.html polido com sucesso!');
