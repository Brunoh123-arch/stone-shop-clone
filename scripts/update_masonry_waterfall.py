# Script para calibrar renderRelacionados e o CSS de produtos relacionados
with open('js/app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

idx_start = js_content.find('// ===== PRODUTOS RELACIONADOS DINÂMICOS — MASONRY 2 COLUNAS =====')
if idx_start == -1:
    idx_start = js_content.find('function renderRelacionados() {')

idx_end = js_content.find('// ===== ABAS DE NAVEGAÇÃO DO PRODUTO =====', idx_start)
if idx_end == -1:
    idx_end = js_content.find('function initProductTabs() {', idx_start)

new_render_relacionados = """// ===== PRODUTOS RELACIONADOS DINÂMICOS — MASONRY CASCATA REAL (PARIDADE 1:1 TIKTOK SHOP) =====
function renderRelacionados() {
  const grid = document.querySelector('.related-grid');
  if (!grid) return;
  if (typeof CATALOGO_PRODUTOS === 'undefined') return;

  const idAtual = typeof PRODUTO_ATUAL !== 'undefined' ? PRODUTO_ATUAL.id : -1;

  // Filtra outros produtos
  const outros = CATALOGO_PRODUTOS.filter(p => p.id !== idAtual);

  // Embaralha para variedade orgânica
  for (let i = outros.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [outros[i], outros[j]] = [outros[j], outros[i]];
  }

  // Pega até 16 produtos para preencher uma cascata rica
  const selecionados = outros.slice(0, 16);

  // Proporções verticais variadas para criar o descompasso orgânico de cascata (Masonry Real)
  const ASPECT_RATIOS = ['3 / 4', '4 / 5', '1 / 1', '4 / 5', '3 / 4', '1 / 1', '4 / 5', '3 / 4'];

  const CREATOR_NAMES = [
    'Kethellen Jade | Creator',
    'Luana Mirella | Review',
    'Brenda Ramos | TikTok',
    'Camila Silva | Provador',
    'Jessica Souza | Moda'
  ];

  function cardHtml(p, idx) {
    const precoNum = parseFloat(p.preco).toFixed(2).replace('.', ',');
    const precoOrigFmt = p.precoOrig ? 'R$ ' + p.precoOrig : 'R$ ' + (parseFloat(p.preco) * 2.8).toFixed(2).replace('.', ',');
    const rating = (4.6 + ((p.id * 7) % 4) * 0.1).toFixed(1);
    const vendasK = (8 + ((p.id * 13) % 25) * 0.7).toFixed(1);
    
    // Proporção assimétrica por card para NUNCA alinhar horizontalmente
    const ratio = ASPECT_RATIOS[idx % ASPECT_RATIOS.length];
    
    // Simula badge de vídeo oficial TikTok Shop em alguns cards selecionados
    const isVideoCard = (idx === 0 || idx === 5 || idx === 11);
    const creatorName = CREATOR_NAMES[idx % CREATOR_NAMES.length];

    // Desconto percentual
    const descVal = p.desc || Math.round((1 - p.preco / (parseFloat(p.preco) * 2.8)) * 100) || 55;
    
    // Variação de badges conforme o print oficial
    let badgeHtml = '';
    if (idx % 3 === 1) {
      badgeHtml = `<span class="tt-rel-badge-relampago" style="background:#fff2e8; color:#ff5722; font-size:10px; font-weight:700; padding:1.5px 5px; border-radius:2px; display:inline-flex; align-items:center; gap:2px;">⚡ Oferta Relâmpago</span>`;
    } else {
      badgeHtml = `
        <span class="tt-rel-badge-off" style="background:#fff0f3; color:#fe2c55; font-size:10px; font-weight:700; padding:1.5px 5px; border-radius:2px;">${descVal}% OFF</span>
        <span class="tt-rel-badge-frete" style="background:#e8f7f5; color:#00a699; font-size:10px; font-weight:600; padding:1.5px 5px; border-radius:2px;">Frete grátis</span>
      `;
    }

    return `
      <a class="related-card" href="produto-${p.id}.html" style="background:#fff; border-radius:8px; overflow:hidden; border:none; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-decoration:none; color:inherit; display:flex; flex-direction:column; width:100%; box-sizing:border-box; position:relative; margin-bottom:8px;">
        <!-- Imagem com Aspect Ratio Dinâmico Vertical para Cascata Orgânica -->
        <div class="related-img-wrapper" style="position:relative; width:100%; aspect-ratio:${ratio}; overflow:hidden; background:#f0f0f0;">
          <img class="related-img" src="${p.img}" alt="${p.nome}" loading="lazy" onerror="this.src='../logo.png'" style="width:100%; height:100%; object-fit:cover; display:block;">
          
          ${isVideoCard ? `
          <!-- Badge de Tempo de Vídeo TikTok -->
          <div style="position:absolute; top:7px; left:7px; background:rgba(0,0,0,0.5); color:#fff; font-size:9.5px; font-weight:700; padding:2px 5px; border-radius:3px; display:flex; align-items:center; gap:3px; z-index:2; backdrop-filter:blur(2px);">
            <span style="font-size:7.5px; letter-spacing:-1px;">❚❚</span> 00:${35 + (idx * 5) % 25}
          </div>
          <!-- Tag do Criador no Rodapé da Imagem -->
          <div style="position:absolute; bottom:6px; left:7px; right:7px; display:flex; align-items:center; gap:4px; color:#fff; font-size:10.5px; font-weight:500; text-shadow:0 1px 2px rgba(0,0,0,0.9); z-index:2; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
            <div style="width:15px; height:15px; border-radius:50%; background:#fe2c55; display:flex; align-items:center; justify-content:center; font-size:8px; font-weight:700; flex-shrink:0;">✓</div>
            <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${creatorName}</span>
          </div>
          <div style="position:absolute; bottom:0; left:0; right:0; height:32px; background:linear-gradient(to top, rgba(0,0,0,0.5), transparent); pointer-events:none;"></div>
          ` : ''}
        </div>

        <!-- Informações do Produto (Ordem 1:1 com a Imagem Oficial do TikTok Shop) -->
        <div class="related-info" style="padding:8px 8px 10px 8px; display:flex; flex-direction:column; flex:1; box-sizing:border-box;">
          <!-- Linha 1: Título do produto com 2 linhas compactas -->
          <div class="related-name" style="font-size:12.5px; font-weight:400; color:#161823; line-height:1.35; max-height:2.7em; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; text-overflow:ellipsis; margin-bottom:4px;">
            ${p.nome}
          </div>

          <!-- Linha 2: Preço Promocional em Vermelho + Preço Original Riscado Cinza -->
          <div class="related-price-row" style="display:flex; align-items:baseline; gap:4px; margin-top:2px; margin-bottom:3px;">
            <div class="related-price" style="font-size:15px; font-weight:700; color:#fe2c55; display:flex; align-items:baseline;">
              <span class="currency" style="font-size:11px; font-weight:700; margin-right:1px;">R$</span> ${precoNum}
            </div>
            ${precoOrigFmt ? `<div class="related-price-original" style="font-size:11px; color:#8a8b91; text-decoration:line-through; font-weight:400; margin-left:2px;">${precoOrigFmt}</div>` : ''}
          </div>

          <!-- Linha 3: Badges de Oferta / Frete Grátis -->
          <div class="card-badges-row" style="display:flex; align-items:center; gap:4px; flex-wrap:wrap; margin-bottom:4px;">
            ${badgeHtml}
          </div>

          <!-- Linha 4: Avaliação e Quantidade de Vendidos -->
          <div class="card-rating-row" style="display:flex; align-items:center; gap:3px; font-size:11px; color:#8a8b91; margin-top:auto;">
            <span style="color:#ffb800; font-size:11px; line-height:1;">★</span>
            <span style="color:#161823; font-weight:600; font-size:11px;">${rating}</span>
            <span style="color:#d0d0d0; margin:0 2px;">|</span>
            <span style="color:#8a8b91; font-size:11px;">${vendasK}K vendidos</span>
          </div>
        </div>
      </a>`;
  }

  // Cria 2 colunas independentes para formar a Cascata Real (Masonry)
  const colLeft = document.createElement('div');
  const colRight = document.createElement('div');
  colLeft.className = 'related-col';
  colRight.className = 'related-col';
  colLeft.style.cssText = 'flex:1; min-width:0; display:flex; flex-direction:column; gap:8px;';
  colRight.style.cssText = 'flex:1; min-width:0; display:flex; flex-direction:column; gap:8px;';

  // Distribuição alternada: as diferentes alturas geram a cascata fluida
  selecionados.forEach((p, i) => {
    const html = cardHtml(p, i);
    const col = i % 2 === 0 ? colLeft : colRight;
    col.insertAdjacentHTML('beforeend', html);
  });

  // Estilização do grid para fundo #f5f5f5 e padding limpo
  grid.style.cssText = 'display:flex; align-items:flex-start; gap:8px; padding:0 8px 24px 8px; width:100%; box-sizing:border-box; background:#f5f5f5;';
  grid.innerHTML = '';
  grid.appendChild(colLeft);
  grid.appendChild(colRight);

  // Garante que o container pai tenha o fundo #f5f5f5 oficial
  const sec = grid.closest('.related-section');
  if (sec) {
    sec.style.cssText = 'background:#f5f5f5; padding-top:4px; border-top:8px solid #f5f5f5; margin-top:10px; width:100%; box-sizing:border-box;';
    const title = sec.querySelector('.related-title');
    if (title) {
      title.style.cssText = 'font-size:15.5px; font-weight:700; color:#161823; padding:12px 10px 8px 10px; margin:0; letter-spacing:-0.2px; background:#f5f5f5;';
    }
  }
}
"""

js_content = js_content[:idx_start] + new_render_relacionados + js_content[idx_end:]

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("SUCCESS: Updated renderRelacionados with 1:1 TikTok Shop Masonry Waterfall!")
