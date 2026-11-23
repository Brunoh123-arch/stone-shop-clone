const fs = require('fs');
const path = require('path');

const pagesDir = path.join(__dirname, 'pages');
const files = fs.readdirSync(pagesDir).filter(f => f.startsWith('produto-') && f.endsWith('.html'));

console.log(`Encontrados ${files.length} arquivos de produto para atualizar.`);

let updatedCount = 0;

files.forEach(file => {
  const filePath = path.join(pagesDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let originalHtml = html;

  // 1. Extrair Preço Atual do Produto para calcular parcela
  let price = 19.90;
  const priceMatch = html.match(/class="[^"]*price-current[^"]*"[^>]*>[\s\S]*?(\d+[\.,]\d{2})/);
  if (priceMatch) {
    price = parseFloat(priceMatch[1].replace('.', '').replace(',', '.'));
  }
  const installmentVal = (price / 2).toFixed(2).replace('.', ',');

  // 2. Extrair título atual do produto
  const titleRegex = /<h1[^>]*class="[^"]*product-title[^"]*"[^>]*>([\s\S]*?)<\/h1>/i;
  const titleMatch = html.match(titleRegex);

  // Se já tiver o bookmark-btn, não precisa reencapsular o título
  const hasBookmark = html.includes('class="bookmark-btn"') || html.includes('bookmark-btn');

  // 3. Extrair dados da ratings-row
  // rating note: 4,8 ou 5,0
  let rating = '4.8';
  let reviews = '5,1 mil';
  let sales = '21.3K';

  const ratingNoteMatch = html.match(/class="[^"]*rating-number[^"]*"[^>]*>([\d,\.]+)<\/span>/i);
  if (ratingNoteMatch) {
    rating = ratingNoteMatch[1].replace(',', '.');
  }

  const reviewCountMatch = html.match(/class="[^"]*rating-number[^"]*"[^>]*>\s*\((\d+[\.,]?\d*)\)\s*<\/span>/i);
  if (reviewCountMatch) {
    let rawRev = reviewCountMatch[1].replace('.', '');
    let num = parseInt(rawRev);
    if (!isNaN(num)) {
      if (num >= 1000) {
        reviews = (num / 1000).toFixed(1).replace('.', ',') + ' mil';
      } else {
        reviews = num.toString();
      }
    }
  }

  const soldMatch = html.match(/class="[^"]*sold-count[^"]*"[^>]*>([\s\S]*?)<\/div>/i);
  if (soldMatch) {
    let rawSold = soldMatch[1].replace(/vendido\(s\)|vendidos/gi, '').trim();
    rawSold = rawSold.replace('.', '').replace(',', '.');
    let num = parseFloat(rawSold);
    if (!isNaN(num)) {
      if (num >= 1000) {
        sales = (num / 1000).toFixed(1) + 'K';
      } else {
        sales = num.toString();
      }
    } else {
      sales = '21.3K';
    }
  }

  // Montar novo bloco de parcelamento + título com bookmark + ratings-row oficial
  if (titleMatch && !hasBookmark) {
    const rawTitle = titleMatch[1].trim();
    
    // Novo bloco do título com bookmark
    const titleBlock = `<!-- Parcelamento oficial (2x sem juros >) -->
      <div class="installment-row" style="display: flex; align-items: center; gap: 4px; font-size: 12.5px; color: #161823; margin: 6px 0 8px 0; cursor: pointer;">
        <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #666;">
          <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
          <line x1="1" y1="10" x2="23" y2="10"></line>
        </svg>
        <span>2x R$ ${installmentVal} <span style="color: #fe2c55; font-weight: 600;">sem juros</span></span>
        <span style="color: #999; font-size: 13px; margin-left: 2px;">›</span>
      </div>

      <!-- Título com Bookmark à direita -->
      <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 8px;">
        <h1 class="product-title" style="font-size: 16px; font-weight: 700; color: #161823; line-height: 1.35; margin: 0; flex: 1;">
          ${rawTitle}
        </h1>
        <button class="bookmark-btn" onclick="toggleBookmark(this)" style="background: none; border: none; padding: 2px 0 0 0; cursor: pointer; color: #161823; display: flex; align-items: center; justify-content: center; flex-shrink: 0;" aria-label="Salvar">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      </div>`;

    html = html.replace(titleRegex, titleBlock);
  }

  // Atualizar ratings-row para a nova formatação idêntica ao print
  const ratingsRowRegex = /<div[^>]*class="[^"]*ratings-row[^"]*"[^>]*>[\s\S]*?<\/div>\s*<\/div>/i;
  const newRatingsRow = `<div class="ratings-row" style="display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
        <div class="star-row" style="display: flex; align-items: center; gap: 4px;">
          <svg class="star-icon" viewBox="0 0 24 24" width="13" height="13" fill="#ffb800">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
          <span style="font-size: 13px; font-weight: 700; color: #161823;">${rating}</span>
          <span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector('.reviews-section')?.scrollIntoView({behavior:'smooth'})">(${reviews})</span>
        </div>
        <span style="color: #e5e5e5; font-size: 12px; margin: 0 1px;">|</span>
        <div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">${sales} vendidos</div>
      </div>`;

  if (ratingsRowRegex.test(html) && !file.includes('produto-104.html')) {
    html = html.replace(ratingsRowRegex, newRatingsRow);
  }

  // 4. Adicionar script toggleBookmark se não existir
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

  if (html !== originalHtml) {
    fs.writeFileSync(filePath, html, 'utf8');
    updatedCount++;
  }
});

console.log(`✅ Sucesso: ${updatedCount} páginas de produto atualizadas com o padrão oficial!`);
