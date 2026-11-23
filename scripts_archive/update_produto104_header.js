const fs = require('fs');
const path = require('path');

const p104Path = path.join(__dirname, 'pages', 'produto-104.html');
let html = fs.readFileSync(p104Path, 'utf8');

// Target the block containing product-title and ratings-row
const targetRegex = /<!-- 2\. Título do produto \+ estrelas \+ contagem de vendidos -->[\s\S]*?<div class="ratings-row">[\s\S]*?<\/div>\s*<\/div>/;

const newSnippet = `<!-- 2. Título do produto + estrelas + contagem de vendidos -->
      <!-- Parcelamento oficial (topo do título) -->
      <div class="installment-row" style="display: flex; align-items: center; gap: 4px; font-size: 12.5px; color: #161823; margin: 6px 0 8px 0; cursor: pointer;">
        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #666;">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
        <span>2x R$ 11,48 <span style="color: #fe2c55; font-weight: 600;">sem juros</span></span>
        <span style="color: #999; font-size: 13px; margin-left: 2px;">›</span>
      </div>

      <!-- Título com Bookmark à direita -->
      <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 8px;">
        <h1 class="product-title" style="font-size: 16px; font-weight: 700; color: #161823; line-height: 1.35; margin: 0; flex: 1;">
          Chinelo Feminino Luxo Strass Brilhante Macio Leve
        </h1>
        <button class="bookmark-btn" onclick="toggleBookmark(this)" style="background: none; border: none; padding: 2px 0 0 0; cursor: pointer; color: #161823; display: flex; align-items: center; justify-content: center; flex-shrink: 0;" aria-label="Salvar">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      </div>

      <!-- Avaliações e Vendas (Cores e Formatação Oficial TikTok Shop) -->
      <div class="ratings-row" style="display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
        <div class="star-row" style="display: flex; align-items: center; gap: 4px;">
          <svg class="star-icon" viewBox="0 0 24 24" width="13" height="13" fill="#ffb800">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
          <span style="font-size: 13px; font-weight: 700; color: #161823;">4.8</span>
          <span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector('.reviews-section')?.scrollIntoView({behavior:'smooth'})">(5,1 mil)</span>
        </div>
        <span style="color: #e5e5e5; font-size: 12px; margin: 0 1px;">|</span>
        <div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">21.3K vendidos</div>
      </div>`;

if (targetRegex.test(html)) {
  html = html.replace(targetRegex, newSnippet);
  
  // Add toggleBookmark script if not present
  if (!html.includes('function toggleBookmark')) {
    html = html.replace('</body>', `<script>
function toggleBookmark(btn) {
  const svg = btn.querySelector('svg');
  if (svg.getAttribute('fill') === 'currentColor') {
    svg.setAttribute('fill', 'none');
  } else {
    svg.setAttribute('fill', 'currentColor');
  }
}
</script>\n</body>`);
  }

  fs.writeFileSync(p104Path, html, 'utf8');
  console.log('✅ produto-104.html atualizado com sucesso!');

  // Sync to ds/produto-chinelo-tiktok.html
  const dsPath = path.join('C:', 'Users', 'Dell', 'Downloads', 'ds', 'produto-chinelo-tiktok.html');
  if (fs.existsSync(dsPath)) {
    fs.writeFileSync(dsPath, html, 'utf8');
    console.log('✅ ds/produto-chinelo-tiktok.html sincronizado!');
  }
} else {
  console.error('❌ Não encontrou o bloco de título e ratings em produto-104.html');
  process.exit(1);
}
