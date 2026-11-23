function renderStoreReviewsFilter() {
  const reviewsSection = document.querySelector('.reviews-section, .customer-reviews-section');
  if (!reviewsSection || document.querySelector('.store-reviews-summary-block')) return;

  const block = document.createElement('div');
  block.className = 'store-reviews-summary-block';
  block.style.cssText = 'padding:14px 0 6px 0; border-top:1px solid #f0f0f0; margin-top:10px; background:#fff;';
  block.innerHTML = `
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; cursor:pointer;" onclick="document.querySelector('.reviews-section')?.scrollIntoView({behavior:'smooth'})">
      <span style="font-size:14px; font-weight:700; color:#161823;">Avaliações da loja (15,3 mil)</span>
      <span style="font-size:16px; color:#888;">›</span>
    </div>
    <div class="review-filter-chips" style="display:flex; gap:8px; overflow-x:auto; -webkit-overflow-scrolling:touch; padding-bottom:4px; scrollbar-width:none;">
      <button type="button" style="background:#fdf5ea; border:1px solid #f8e4c8; border-radius:16px; padding:6px 12px; font-size:11.5px; color:#91580f; font-weight:600; display:inline-flex; align-items:center; gap:4px; white-space:nowrap; cursor:pointer;">
        📷 Inclui imagens ou vídeos (3 mil)
      </button>
      <button type="button" style="background:#fdf5ea; border:1px solid #f8e4c8; border-radius:16px; padding:6px 12px; font-size:11.5px; color:#91580f; font-weight:600; display:inline-flex; align-items:center; gap:4px; white-space:nowrap; cursor:pointer;">
        ★ 5 (12,3 mil)
      </button>
    </div>
  `;

  reviewsSection.appendChild(block);
}

// Item 14: Player de Vídeo Oficial "Sobre este produto" com Guia de Tamanhos
function renderSobreEsteProdutoVideo() {
  if (document.querySelector('.sobre-este-produto-video-section')) return;
  const descSection = document.querySelector('.description-section, .product-description-section');
  if (!descSection) return;

  let videoSrc = '../img/video-chinelo-completo.mp4';
  if (typeof PRODUTO_ATUAL !== 'undefined') {
    if (PRODUTO_ATUAL.video) videoSrc = PRODUTO_ATUAL.video;
    else if (PRODUTO_ATUAL.video_url) videoSrc = PRODUTO_ATUAL.video_url;
  }

  const videoBlock = document.createElement('div');
  videoBlock.className = 'sobre-este-produto-video-section';
  videoBlock.style.cssText = 'background:#fff; padding:14px 0 16px 0; border-bottom:8px solid #f5f5f5;';
  videoBlock.innerHTML = `
    <h3 style="font-size:15px; font-weight:700; color:#161823; margin:0 0 10px 0;">Sobre este produto</h3>
    <div style="font-size:13.5px; font-weight:600; color:#161823; margin-bottom:8px;">Vídeo</div>
    <div class="product-video-player-box" style="position:relative; width:100%; aspect-ratio:16/9; background:#000; border-radius:10px; overflow:hidden; display:flex; align-items:center; justify-content:center;">
      <video id="sobre-produto-video" src="${videoSrc}" playsinline loop style="width:100%; height:100%; object-fit:contain;"></video>
      <button id="sobre-produto-play-btn" style="position:absolute; width:52px; height:52px; border-radius:50%; background:rgba(0,0,0,0.5); border:2px solid #fff; display:flex; align-items:center; justify-content:center; cursor:pointer; z-index:2; outline:none;">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="#fff" style="margin-left:3px;"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
      </button>
      <div class="product-video-controls" 