with open('js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('function renderStoreReviewsFilter() {')
if idx != -1:
    start = content.rfind('// Item 12', 0, idx)
    end = content.find('}', idx) + 1
    
    new_code = """// Item 12: Filtros de Avaliação da Loja (📷 Inclui imagens ou vídeos / ★ 5) Oficial TikTok Shop
function renderStoreReviewsFilter() {
  const reviewsSection = document.querySelector('.reviews-section, .customer-reviews-section');
  if (!reviewsSection) return;

  const existingBlock = document.querySelector('.store-reviews-summary-block');
  if (existingBlock) existingBlock.remove();

  const cards = reviewsSection.querySelectorAll('.review-card');
  const totalCount = cards.length > 0 ? cards.length : 5;
  const mediaCount = Array.from(cards).filter(c => c.querySelectorAll('img, video, .review-photo, .review-video').length > 0).length || totalCount;
  const fiveStarsCount = totalCount;

  const block = document.createElement('div');
  block.className = 'store-reviews-summary-block';
  block.style.cssText = 'padding: 14px 16px 12px 16px; border-top: 1px solid #f2f2f2; margin-top: 12px; background: #fff; width: 100%; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;';
  
  block.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; cursor: pointer;" onclick="window.abrirTelaAvaliacoesCompletas ? window.abrirTelaAvaliacoesCompletas('all') : null">
      <span style="font-size: 14.5px; font-weight: 700; color: #161823; letter-spacing: -0.2px;">Avaliações da loja (${totalCount})</span>
      <span style="font-size: 17px; color: #8a8b91; line-height: 1; font-weight: 300;">›</span>
    </div>
    <div class="review-filter-chips" style="display: flex; gap: 8px; overflow-x: auto; -webkit-overflow-scrolling: touch; padding-bottom: 2px; scrollbar-width: none;">
      <button type="button" class="store-filter-chip" style="background: #fdf5ea; border: 1px solid #f8e4c8; border-radius: 16px; padding: 6px 13px; font-size: 11.5px; color: #91580f; font-weight: 600; display: inline-flex; align-items: center; gap: 5px; white-space: nowrap; cursor: pointer; outline: none;" onclick="window.abrirTelaAvaliacoesCompletas ? window.abrirTelaAvaliacoesCompletas('media') : null">
        <svg width="13" height="13" viewBox="0 0 16 16" fill="#91580f" style="display: inline-block; vertical-align: middle; flex-shrink: 0;"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.5 2.5C5.16 2.5 4.85 2.7 4.71 3.01L4.08 4.38C3.99 4.56 3.81 4.69 3.61 4.69H2.5C1.67 4.69 1 5.36 1 6.19V12C1 12.83 1.67 13.5 2.5 13.5H13.5C14.33 13.5 15 12.83 15 12V6.19C15 5.36 14.33 4.69 13.5 4.69H12.39C12.19 4.69 12.01 4.56 11.92 4.38L11.29 3.01C11.15 2.7 10.84 2.5 10.5 2.5H5.5ZM8 11.25C9.52 11.25 10.75 10.02 10.75 8.5C10.75 6.98 9.52 5.75 8 5.75C6.48 5.75 5.25 6.98 5.25 8.5C5.25 10.02 6.48 11.25 8 11.25ZM8 10C8.83 10 9.5 9.33 9.5 8.5C9.5 7.67 8.83 7 8 7C7.17 7 6.5 7.67 6.5 8.5C6.5 9.33 7.17 10 8 10Z"/></svg>
        <span>Inclui imagens ou vídeos (${mediaCount})</span>
      </button>
      <button type="button" class="store-filter-chip" style="background: #fdf5ea; border: 1px solid #f8e4c8; border-radius: 16px; padding: 6px 13px; font-size: 11.5px; color: #91580f; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; white-space: nowrap; cursor: pointer; outline: none;" onclick="window.abrirTelaAvaliacoesCompletas ? window.abrirTelaAvaliacoesCompletas('5') : null">
        <span style="color: #91580f; font-size: 12px; line-height: 1;">★</span>
        <span>5 (${fiveStarsCount})</span>
      </button>
    </div>
  `;

  reviewsSection.appendChild(block);
}"""
    content = content[:start] + new_code + content[end:]
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: Updated js/app.js!")
else:
    print("ERROR: function not found")
