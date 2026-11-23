const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('>>> [BRUNO CTO] INICIANDO BLINDAGEM TOTAL DO INDEX.HTML <<<');

// =========================================================================
// 1. REFINAR O CABEÇALHO DA LOJA COM O BADGE "Loja Estrela" E O CUPOM OFICIAL
// =========================================================================
const storeSectionOfficial = `<!-- STORE SECTION OFICIAL -->
          <div class="store-section">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <div style="display: flex; align-items: center; gap: 10px;">
                <img src="./logo.png" alt="Stone Shop"
                  style="width: 58px; height: 58px; object-fit: cover; border-radius: 50%; border: 1px solid #f0f0f0;">
                <div>
                  <h2 style="display: flex; align-items: center; gap: 4px; font-size: 16px; font-weight: 700; color: #161823; margin: 0 0 2px 0; line-height: 1.2;">
                    Stone Shop
                    <svg viewBox="0 0 24 24" width="15" height="15" style="color:#0095f6; flex-shrink:0;" fill="currentColor">
                      <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                    </svg>
                  </h2>
                  <div style="margin-bottom: 2px;">
                    <span class="badge-loja-estrela">Loja Estrela</span>
                  </div>
                  <div style="font-size: 12px; color: #161823; font-weight: 400;">
                    112.2K vendido(s)
                  </div>
                </div>
              </div>
              <div style="display: flex; flex-direction: column; gap: 6px; align-items: flex-end;">
                <button style="background: #fe2c55; color: #fff; border: none; height: 32px; padding: 0 20px; border-radius: 16px; font-size: 13px; font-weight: 700; cursor: pointer;">Seguir</button>
                <button style="background: #f1f1f2; color: #161823; border: none; height: 32px; padding: 0 16px; border-radius: 16px; font-size: 13px; font-weight: 600; cursor: pointer;" onclick="openSmartChat()">Mensagem</button>
              </div>
            </div>
          </div>

          <!-- CUPOM DENTRO DA ÁREA DA LOJA (SEM CORTES, RESGATADO EM VERDE-ÁGUA) -->
          <div class="coupons-container">
            <div class="coupon-card-official">
              <div class="coupon-text-left">
                <div class="coupon-title">Cupom de envio</div>
                <div class="coupon-sub">em pedidos acima de R$ 109</div>
              </div>
              <div class="coupon-resgatado-txt">Resgatado</div>
            </div>
          </div>`;

const storeStart = html.indexOf('<div class="store-section">');
const navTabsStart = html.indexOf('<!-- NAV TABS -->');
if (storeStart !== -1 && navTabsStart !== -1) {
  html = html.slice(0, storeStart) + storeSectionOfficial + '\n\n          ' + html.slice(navTabsStart);
  console.log('1. Store section e cupons atualizados.');
}

// =========================================================================
// 2. REFINAR SEÇÃO "PRINCIPAIS PRODUTOS" COM "Ver mais >"
// =========================================================================
const principaisHeaderOfficial = `<div style="background: white; padding: 16px; margin-bottom: 8px;" id="principais-produtos-section">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; cursor: pointer;" onclick="switchTab(document.querySelectorAll('.nav-tab')[1], 'produtos')">
              <h2 style="font-size: 16px; font-weight: 700; color: #161823; margin: 0px;">Principais produtos</h2>
              <div style="display: flex; align-items: center; gap: 2px; font-size: 13px; color: #8a8b91;">
                Ver mais
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>`;

const pSecIdx = html.indexOf('<div style="background: white; padding: 16px; margin-bottom: 8px;" id="principais-produtos-section">');
const pSecEnd = html.indexOf('<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">', pSecIdx);
if (pSecIdx !== -1 && pSecEnd !== -1) {
  html = html.slice(0, pSecIdx) + principaisHeaderOfficial + '\n            ' + html.slice(pSecEnd);
  console.log('2. Principais produtos com link "Ver mais >" restaurado.');
}

// =========================================================================
// 3. RESTAURAR SEÇÃO "Novos lançamentos" E O DIVISOR DEGRADÊ ROSA
// =========================================================================
const novosLancamentosHtml = `<!-- SEÇÃO NOVOS LANÇAMENTOS (Print 4 Oficial) -->
          <div style="background: white; padding: 14px 16px 16px 16px; margin-bottom: 8px;" id="novos-lancamentos-section">
            <div style="font-size: 16px; font-weight: 700; color: #161823; margin-bottom: 12px;">Novos lançamentos</div>
            <a href="pages/produto-104.html" style="text-decoration: none; color: inherit; display: flex; align-items: center; justify-content: space-between; gap: 12px;">
              <img src="https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192"
                alt="Sandália feminino LIA Delicada"
                style="width: 88px; height: 88px; object-fit: cover; border-radius: 8px; flex-shrink: 0; background: #f7f7f7;">
              <div style="flex: 1; min-width: 0;">
                <h3 style="font-size: 13.5px; font-weight: 500; color: #161823; line-height: 1.3; margin: 0 0 5px 0; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                  Sandália feminino LIA Delicada, Confortável e Elegante
                </h3>
                <div style="margin-bottom: 5px;">
                  <span class="badge-frete-gratis">Frete grátis</span>
                </div>
                <div style="display: flex; align-items: baseline; gap: 2px;">
                  <span style="font-size: 12px; font-weight: 700; color: #fe2c55;">R$</span>
                  <span style="font-size: 17px; font-weight: 700; color: #fe2c55;">25,95</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px; margin-top: 2px;">
                  <span style="font-size: 11px; color: #8a8b91; text-decoration: line-through;">R$ 49,90</span>
                  <span style="background: #ffe8ee; color: #ff2b56; font-size: 10.5px; font-weight: 700; padding: 1px 4px; border-radius: 2px;">-48%</span>
                </div>
              </div>
              <div class="unified-buy-btn" onclick="event.preventDefault(); window.location.href='pages/produto-104.html';">
                <div class="btn-cart-part">
                  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#fe2c55" stroke-width="2">
                    <circle cx="9" cy="21" r="1"></circle>
                    <circle cx="20" cy="21" r="1"></circle>
                    <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                  </svg>
                </div>
                <div class="btn-txt-part">
                  Comprar
                </div>
              </div>
            </a>
          </div>

          <!-- PRODUTOS RECOMENDADOS -->
          <div style="background: white; padding: 14px 16px;" id="produtos-recomendados-section">
            <div class="divider-home-rec">Recomendado para você</div>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">`;

// Remover o header anterior de produtos recomendados e inserir a seção Novos Lançamentos
const recSectionStart = html.indexOf('<!-- PRODUTOS RECOMENDADOS -->');
const recGridStart = html.indexOf('<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">');

if (recSectionStart !== -1 && recGridStart !== -1) {
  html = html.slice(0, recSectionStart) + novosLancamentosHtml + html.slice(recGridStart + '<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px;" id="recommended-grid">'.length);
  console.log('3. Seção "Novos lançamentos" e divisor degradê rosa restaurados com sucesso.');
}

// =========================================================================
// 4. RESTAURAR SEÇÃO OFICIAL DE CATEGORIAS (Print 2)
// =========================================================================
const categoriasSectionOfficial = `<!-- CATEGORIAS SECTION OFICIAL TIKTOK SHOP (Print 2) -->
          <div id="categorias-section" style="display: none; background: white; min-height: 85vh; padding: 4px 16px 20px 16px;">
            <!-- Categoria 1: Calçados -->
            <div class="category-item-row" onclick="filterByCategory('Calçados')" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid #f5f5f5; cursor: pointer;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <img src="https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp?dr=15582&t=555f072d&ps=933b5bde&shp=c940a200&shcp=9b759fb9&idc=my3&from=3376456192"
                  alt="Calçados"
                  style="width: 48px; height: 48px; border-radius: 6px; object-fit: cover; background: #f7f7f7;">
                <span style="font-size: 15px; font-weight: 700; color: #161823;">Calçados</span>
              </div>
              <div style="display: flex; align-items: center; gap: 4px; color: #8a8b91; font-size: 14px;">
                <span>19</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>

            <!-- Categoria 2: Moda infantil / Vestuário -->
            <div class="category-item-row" onclick="filterByCategory('Moda Feminina')" style="display: flex; align-items: center; justify-content: space-between; padding: 14px 0; border-bottom: 1px solid #f5f5f5; cursor: pointer;">
              <div style="display: flex; align-items: center; gap: 14px;">
                <img src="https://down-br.img.susercontent.com/file/sg-11134201-7rd5p-m7uwvu85tnp9ae"
                  alt="Moda infantil"
                  style="width: 48px; height: 48px; border-radius: 6px; object-fit: cover; background: #f7f7f7;">
                <span style="font-size: 15px; font-weight: 700; color: #161823;">Moda infantil</span>
              </div>
              <div style="display: flex; align-items: center; gap: 4px; color: #8a8b91; font-size: 14px;">
                <span>3</span>
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </div>
            </div>
          </div>`;

// Inserir categorias-section logo após o fechamento de produtos-recomendados-section
// ou substituir se já existir
if (html.includes('id="categorias-section"')) {
  // Substituir existente
  const catS = html.indexOf('id="categorias-section"');
  const catOpen = html.lastIndexOf('<div', catS);
  const catClose = html.indexOf('</div>\n          </div>', catS); // ou achar próximo bloco
  // Vamos usar regex ou replace limpo
  html = html.replace(/<div id="categorias-section"[\s\S]*?<\/div>\s*<\/div>/i, categoriasSectionOfficial);
  console.log('4. Categorias section existente atualizada.');
} else {
  // Inserir logo após o fechamento de produtos-recomendados-section
  const recEnd = html.indexOf('<!-- FOOTER');
  if (recEnd !== -1) {
    html = html.slice(0, recEnd) + categoriasSectionOfficial + '\n\n          ' + html.slice(recEnd);
    console.log('4. Categorias section oficial inserida.');
  }
}

// =========================================================================
// 5. INJETAR O BOTÃO UNIFICADO E ESTRUTURA Y2K EM CADA CARD DE RECOMMENDED-GRID
// =========================================================================
// Adicionar o botão [ 🛒 | Comprar ] dentro dos cards para quando estiverem em modo lista
html = html.replace(/<div class="product-sales">([\s\S]*?)<\/div>/g, (match, salesText) => {
  // Se já tiver o botão unificado, não duplica
  if (match.includes('unified-buy-btn')) return match;
  return `<div class="product-sales">${salesText}</div>
                    <div class="unified-buy-btn" onclick="event.preventDefault(); event.stopPropagation(); window.location.href=this.closest('a').href;">
                      <div class="btn-cart-part">
                        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="#fe2c55" stroke-width="2">
                          <circle cx="9" cy="21" r="1"></circle>
                          <circle cx="20" cy="21" r="1"></circle>
                          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                        </svg>
                      </div>
                      <div class="btn-txt-part">
                        Comprar
                      </div>
                    </div>`;
});

// =========================================================================
// 6. FUNÇÕES JS BLINDADAS: switchTab, setSubFilter, applySubFilter, filterByCategory
// =========================================================================
const officialScripts = `
    // Switch de Abas Oficial TikTok Shop
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

      if (tab === 'home') {
        if (mainSec) mainSec.style.display = 'block';
        if (novosSec) novosSec.style.display = 'block';
        if (recSec) recSec.style.display = 'block';
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'none';
        if (divider) divider.style.display = 'flex';
        if (grid) grid.classList.remove('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else if (tab === 'produtos') {
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) recSec.style.display = 'block';
        if (catSec) catSec.style.display = 'none';
        if (subBar) subBar.style.display = 'flex';
        if (divider) divider.style.display = 'none';
        if (grid) grid.classList.add('produtos-layout-list');
        document.querySelectorAll('.product-card-rec').forEach(c => c.style.display = '');
      } else if (tab === 'categorias') {
        if (mainSec) mainSec.style.display = 'none';
        if (novosSec) novosSec.style.display = 'none';
        if (recSec) recSec.style.display = 'none';
        if (catSec) catSec.style.display = 'block';
        if (subBar) subBar.style.display = 'none';
      }
    }

    // Filtro por categoria (Print 2)
    function filterByCategory(catName) {
      // Chaveia para a aba produtos
      const produtosTabBtn = document.querySelectorAll('.nav-tab')[1];
      switchTab(produtosTabBtn, 'produtos');

      const cards = document.querySelectorAll('.product-card-rec');
      cards.forEach(card => {
        const cat = card.getAttribute('data-cat') || '';
        const nome = card.getAttribute('data-nome') || '';
        if (cat.toLowerCase().includes(catName.toLowerCase()) || nome.toLowerCase().includes(catName.toLowerCase())) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    }

    // Sub-filtro da aba Produtos: Recomendado | Mais vendidos | Lançamentos
    function setSubFilter(el, type) {
      document.querySelectorAll('.subfilter-item').forEach(item => item.classList.remove('active'));
      if (el) el.classList.add('active');

      const grid = document.getElementById('recommended-grid');
      if (!grid) return;
      const cards = Array.from(grid.querySelectorAll('.product-card-rec'));

      if (type === 'mais-vendidos') {
        cards.sort((a, b) => {
          const getSalesNum = (card) => {
            const text = card.textContent || '';
            const match = text.match(/([\\d\\.,]+)\\s*k?\\s*vendido/i);
            if (!match) return 0;
            let val = parseFloat(match[1].replace(',', '.'));
            if (text.toLowerCase().includes('k vendido') || text.toLowerCase().includes('k. vendido')) val *= 1000;
            return val;
          };
          return getSalesNum(b) - getSalesNum(a);
        });
      } else if (type === 'lancamentos') {
        cards.sort((a, b) => {
          const getProdId = (card) => {
            const href = card.getAttribute('href') || '';
            const m = href.match(/produto-(\\d+)\\.html/);
            return m ? parseInt(m[1], 10) : 0;
          };
          return getProdId(b) - getProdId(a);
        });
      } else {
        // Recomendado: traz o produto 104 primeiro, seguido dos outros
        cards.sort((a, b) => {
          const hrefA = a.getAttribute('href') || '';
          const hrefB = b.getAttribute('href') || '';
          if (hrefA.includes('produto-104.html')) return -1;
          if (hrefB.includes('produto-104.html')) return 1;
          return 0;
        });
      }

      cards.forEach(card => grid.appendChild(card));
    }

    // Alias para compatibilidade total
    window.applySubFilter = setSubFilter;
    window.setSubFilter = setSubFilter;
    window.switchTab = switchTab;
    window.filterByCategory = filterByCategory;

    function toggleLayoutView() {
      const grid = document.getElementById('recommended-grid');
      if (!grid) return;
      grid.classList.toggle('produtos-layout-list');
    }
`;

// Substituir as funções antigas no final do script
const sOldStart = html.indexOf('function switchTab');
const sOldEnd = html.indexOf('initShareTooltip();');
if (sOldStart !== -1 && sOldEnd !== -1) {
  html = html.slice(0, sOldStart) + officialScripts + '\n\n    ' + html.slice(sOldEnd);
  console.log('6. Funções JS de abas e ordenação subfilter atualizadas com sucesso.');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('>>> [BRUNO CTO] INDEX.HTML 100% BLINDADO E ATUALIZADO! <<<');
