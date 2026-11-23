with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function renderStoreReviewsFilter() {')
if idx != -1:
    start = content.rfind('// Item 12', 0, idx)
    
    # Find full function block until closing brace of renderStoreReviewsFilter
    brace_count = 0
    fn_end = idx
    for i in range(idx, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                fn_end = i + 1
                break
    
    new_code = """// Item 12: Filtros de Avaliação da Loja (Estático, Retangular tipo quadrado border-radius: 4px, Oficial TikTok Shop)
function renderStoreReviewsFilter() {
  const reviewsSection = document.querySelector('.reviews-section, .customer-reviews-section');
  if (!reviewsSection) return;

  const existingBlock = document.querySelector('.store-reviews-summary-block');
  if (existingBlock) existingBlock.remove();

  // Dados oficiais TikTok Shop de reputação da loja (Stone Shop: 112.2K vendidos)
  const storeTotalReviews = '2,9 mil';
  const storeMediaReviews = '742';
  const store5StarReviews = '2,2 mil';

  const block = document.createElement('div');
  block.className = 'store-reviews-summary-block';
  block.style.cssText = 'padding: 16px 16px 12px 16px; border-top: 1px solid #f2f2f2; margin-top: 12px; background: #fff; width: 100%; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;';
  
  block.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 11px; cursor: pointer;" onclick="window.abrirTelaAvaliacoesCompletas ? window.abrirTelaAvaliacoesCompletas('all') : null">
      <span style="font-size: 14.5px; font-weight: 700; color: #161823; letter-spacing: -0.2px;">Avaliações da loja (${storeTotalReviews})</span>
      <span style="font-size: 16px; color: #8a8b91; line-height: 1; font-weight: 300;">›</span>
    </div>
    <div class="review-filter-chips" style="display: flex; gap: 8px; align-items: center; flex-wrap: nowrap; overflow: hidden; width: 100%;">
      <!-- Card 1: Retângulo tipo quadrado estático (Inclui imagens ou vídeos) -->
      <button type="button" class="store-filter-chip" style="background: #fff6e0; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11.5px; color: #977633; font-weight: 500; display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; cursor: pointer; outline: none; flex-shrink: 0; -webkit-tap-highlight-color: transparent;" onclick="window.abrirTelaAvaliacoesCompletas ? window.abrirTelaAvaliacoesCompletas('media') : null">
        <svg width="13" height="13" viewBox="0 0 16 16" fill="#977633" style="display: inline-block; vertical-align: middle; flex-shrink: 0;">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M5.5 2.5C5.16 2.5 4.85 2.7 4.71 3.01L4.08 4.38C3.99 4.56 3.81 4.69 3.61 4.69H2.5C1.67 4.69 1 5.36 1 6.19V12C1 12.83 1.67 13.5 2.5 13.5H13.5C14.33 13.5 15 12.83 15 12V6.19C15 5.36 14.33 4.69 13.5 4.69H12.39C12.19 4.69 12.01 4.56 11.92 4.38L11.29 3.01C11.15 2.7 10.84 2.5 10.5 2.5H5.5ZM8 11.25C9.52 11.25 10.75 10.02 10.75 8.5C10.75 6.98 9.52 5.75 8 5.75C6.48 5.75 5.25 6.98 5.25 8.5C5.25 10.02 6.48 11.25 8 11.25ZM8 10C8.83 10 9.5 9.33 9.5 8.5C9.5 7.67 8.83 7 8 7C7.17 7 6.5 7.67 6.5 8.5C6.5 9.33 7.17 10 8 10Z"/>
        </svg>
        <span>Inclui imagens ou vídeos (${storeMediaReviews})</span>
      </button>

      <!-- Card 2: Retângulo tipo quadrado estático (5 Estrelas Oficial) -->
      <button type="button" class="store-filter-chip" style="background: #fff6e0; border: none; border-radius: 4px; padding: 6px 10px; font-size: 11.5px; color: #977633; font-weight: 500; display: inline-flex; align-items: center; gap: 4px; white-space: nowrap; cursor: pointer; outline: none; flex-shrink: 0; -webkit-tap-highlight-color: transparent;" onclick="window.abrirTelaAvaliacoesCompletas ? window.abrirTelaAvaliacoesCompletas('5') : null">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="#f4bc15" stroke="#f4bc15" stroke-width="0.8" style="display: inline-block; vertical-align: middle; flex-shrink: 0;">
          <path d="M12 1.5c.38 0 .72.23.86.58l2.76 6.64 7.08.62c.39.04.72.31.84.68.12.38.01.79-.28 1.05l-5.36 4.74 1.59 6.96c.09.39-.07.79-.39 1.02-.32.23-.75.25-1.09.06L12 20.18l-6.01 3.67c-.34.19-.77.17-1.09-.06-.32-.23-.48-.63-.39-1.02l1.59-6.96-5.36-4.74c-.29-.26-.4-.67-.28-1.05.12-.37.45-.64.84-.68l7.08-.62 2.76-6.64c.14-.35.48-.58.86-.58z"/>
        </svg>
        <span>5 (${store5StarReviews})</span>
      </button>
    </div>
  `;

  reviewsSection.appendChild(block);
}"""
    
    content = content[:start] + new_code + content[fn_end:]
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Updated js/app.js to static square format!")
else:
    print("ERROR: function not found")
