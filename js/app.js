// === TIKTOK SHOP OFICIAL: TOGGLE CARROSSEL IMAGENS <-> GUIA DE TAMANHOS ===
window.switchSliderTab = function(tab, e) {
  if (e) {
    if (typeof e.preventDefault === 'function') e.preventDefault();
    if (typeof e.stopPropagation === 'function') e.stopPropagation();
  }
  let guide = document.getElementById('slider-size-guide');
  const track = document.querySelector('.slider-track');
  const counterImages = document.getElementById('slider-counter-images') || document.querySelector('.slider-counter[data-has-tamanho="true"]');
  const counterSize = document.getElementById('slider-counter-size');

  // Single Source of Truth: busca imagem na descrição para manter estritamente espelhado
  const descGuideImg = document.querySelector('.size-guide-img, .description-text img[src*="guia-tamanhos"], .about-product-section img[src*="guia-tamanhos"], .product-desc img[src*="guia-tamanhos"]');
  const guideSrc = descGuideImg ? (descGuideImg.getAttribute('src') || descGuideImg.src) : (typeof getProductSizeGuideImage === 'function' ? getProductSizeGuideImage() : null);

  const hasModernToggle = !!document.querySelector('.slider-counter-toggle');
  const btnFotos = document.getElementById('btn-tab-fotos');
  const btnTamanho = document.getElementById('btn-tab-tamanho');

  if (tab === 'tamanho') {
    if (!guide && guideSrc) {
      const slider = document.querySelector('.image-slider');
      if (slider) {
        guide = document.createElement('div');
        guide.id = 'slider-size-guide';
        guide.className = 'slider-size-guide';
        guide.style.cssText = 'position:absolute; top:0; left:0; width:100%; height:100%; background:#fff; z-index:5; display:none; align-items:center; justify-content:center; padding:16px 14px 44px 14px; box-sizing:border-box;';
        guide.innerHTML = `<img src="${guideSrc}" alt="Guia de Tamanhos Oficial" style="max-width:100%; max-height:100%; object-fit:contain; display:block; margin:auto;" />`;
        slider.appendChild(guide);
      }
    }
    if (guide) {
      const imgInGuide = guide.querySelector('img');
      if (imgInGuide && guideSrc && imgInGuide.getAttribute('src') !== guideSrc) {
        imgInGuide.src = guideSrc;
      }
      guide.style.setProperty('display', 'flex', 'important');
    }
    if (track) track.style.visibility = 'hidden';
    if (hasModernToggle) {
      if (counterImages) counterImages.style.setProperty('display', 'none', 'important');
      if (btnTamanho) {
        btnTamanho.style.background = 'rgba(255,255,255,0.24)';
        btnTamanho.style.color = '#ffffff';
      }
      if (btnFotos) {
        btnFotos.style.background = 'transparent';
        btnFotos.style.color = 'rgba(255,255,255,0.88)';
      }
    } else {
      if (counterImages) counterImages.style.setProperty('display', 'none', 'important');
      if (counterSize) counterSize.style.setProperty('display', 'flex', 'important');
    }
  } else {
    if (guide) {
      guide.style.setProperty('display', 'none', 'important');
    }
    if (track) track.style.visibility = 'visible';
    if (hasModernToggle) {
      if (counterImages) counterImages.style.setProperty('display', 'none', 'important');
      if (btnFotos) {
        btnFotos.style.background = 'rgba(255,255,255,0.24)';
        btnFotos.style.color = '#ffffff';
      }
      if (btnTamanho) {
        btnTamanho.style.background = 'transparent';
        btnTamanho.style.color = 'rgba(255,255,255,0.88)';
      }
    } else {
      if (counterImages) counterImages.style.setProperty('display', 'flex', 'important');
      if (counterSize) counterSize.style.setProperty('display', 'none', 'important');
    }
  }
};

// Desativada injeção sintética de atributos para fidelidade 1:1 ao TikTok Shop oficial
function getTikTokCategoryAttributes(productTitle = '', starCount = 5) {
  return [];
}
// ===== CARRINHO - gerenciamento via localStorage =====
const CART_KEY = 'famosinhos_cart';

function getCart() {
  try {
    return JSON.parse(localStorage.getItem(CART_KEY)) || [];
  } catch { return []; }
}

function saveCart(cart) {
  localStorage.setItem(CART_KEY, JSON.stringify(cart));
}

function addToCart(produto, qty = 1) {
  const cart = getCart();

  // Custom price override se configurado no Admin
  try {
    if (typeof localStorage !== 'undefined') {
      const customPrecos = JSON.parse(localStorage.getItem('stone_custom_precos') || '{}');
      if (customPrecos[produto.id] !== undefined && customPrecos[produto.id] !== null && customPrecos[produto.id] !== '') {
        produto.preco = parseFloat(customPrecos[produto.id]);
      }
    }
  } catch(e) {}
  
  // Normaliza o nome do produto 101 Pirelli universalmente para "Pneus Pirelli"
  let prodNome = produto.nome;
  if (Number(produto.id) === 101) {
    prodNome = 'Pneus Pirelli';
  }

  const idx = cart.findIndex(i => Number(i.id) === Number(produto.id) && i.variacao === (produto.variacao || null));
  if (idx >= 0) {
    cart[idx].qty += qty;
  } else {
    // Pega a imagem principal, ignorando vídeos .mp4
    let cleanImg = '';
    if (produto.imagens && produto.imagens.length) {
      // Prefere a primeira imagem real (não mp4)
      const primeiraImg = produto.imagens.find(i => !i.endsWith('.mp4') && !i.endsWith('.webm'));
      cleanImg = primeiraImg || produto.imagens[0];
    }
    if (!cleanImg) cleanImg = produto.img || '';
    if (cleanImg.startsWith('../')) {
      cleanImg = cleanImg.substring(3);
    }
    cart.push({
      id: produto.id,
      nome: prodNome,
      preco: produto.preco,
      precoOrig: produto.precoOrig || (typeof CATALOGO_PRODUTOS !== 'undefined' && CATALOGO_PRODUTOS.find(p => p.id == produto.id) ? CATALOGO_PRODUTOS.find(p => p.id == produto.id).precoOrig : null) || (produto.preco * 1.5),
      img: cleanImg,
      qty: qty,
      variacao: produto.variacao || null
    });
  }
  saveCart(cart);
  updateCartBadges();
  return cart;
}

function removeFromCart(id, variacao = null) {
  const targetId = Number(id);
  const cart = getCart().filter(i => {
    const matchId = Number(i.id) === targetId;
    if (matchId) {
      if (variacao !== null) {
        return i.variacao !== variacao;
      }
      return false; // Se não passou variação, remove todos com este ID
    }
    return true;
  });
  saveCart(cart);
  updateCartBadges();
  return cart;
}

function updateQty(id, delta, variacao = null) {
  let cart = getCart();
  const idx = cart.findIndex(i => {
    const matchId = Number(i.id) === Number(id);
    if (matchId && variacao !== null) {
      return i.variacao === variacao;
    }
    return matchId;
  });
  if (idx >= 0) {
    const newQty = cart[idx].qty + delta;
    if (newQty <= 0) {
      return null;
    } else {
      cart[idx].qty = newQty;
      saveCart(cart);
    }
  }
  return cart;
}

function getCartCount() {
  return getCart().reduce((sum, i) => sum + i.qty, 0);
}

function getCartTotal() {
  return getCart().reduce((sum, i) => sum + i.preco * i.qty, 0);
}

function updateCartBadges() {
  const count = getCartCount();
  document.querySelectorAll('.cart-badge').forEach(badge => {
    badge.textContent = count > 0 ? count : '';
    badge.style.display = count > 0 ? 'flex' : 'none';
    badge.classList.remove('pop');
    void badge.offsetWidth;
    if (count > 0) badge.classList.add('pop');
  });
}

// ===== TOAST OFICIAL TIKTOK SHOP (CENTRALIZADO, DARK PILL BLINDADO) =====
function showTikTokToast(msg, duration = 1800) {
  let toast = document.getElementById('tiktok-toast-global');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'tiktok-toast-global';
    toast.className = 'tiktok-toast-notification';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  // Estilos inline blindados para renderização sem falha em qualquer contexto
  toast.style.position = 'fixed';
  toast.style.top = '50%';
  toast.style.left = '50%';
  toast.style.transform = 'translate(-50%, -50%) scale(1)';
  toast.style.background = '#383838';
  toast.style.color = '#ffffff';
  toast.style.padding = '13px 24px';
  toast.style.borderRadius = '12px';
  toast.style.fontSize = '15px';
  toast.style.fontWeight = '600';
  toast.style.fontFamily = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';
  toast.style.lineHeight = '1.25';
  toast.style.letterSpacing = '-0.15px';
  toast.style.whiteSpace = 'nowrap';
  toast.style.textAlign = 'center';
  toast.style.zIndex = '999999999';
  toast.style.pointerEvents = 'none';
  toast.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.25)';
  toast.style.transition = 'opacity 0.15s ease, transform 0.15s ease';
  toast.style.opacity = '1';
  toast.style.display = 'block';

  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translate(-50%, -50%) scale(0.96)';
    setTimeout(() => {
      if (toast.style.opacity === '0') {
        toast.style.display = 'none';
      }
    }, 180);
  }, duration);
}
window.showTikTokToast = showTikTokToast;

// ===== TOAST =====
function showToast(msg, duration = 2500) {
  let toast = document.getElementById('toast-global');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast-global';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove('show'), duration);
}

// ===== COMPARTILHAR PRODUTO (Copiar link) =====
function shareProduct() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    showToast('Link do produto copiado com sucesso!');
  }).catch(() => {
    // Fallback caso clipboard API falhe
    const tempInput = document.createElement('input');
    tempInput.value = url;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    showToast('Link do produto copiado com sucesso!');
  });
}

// ===== MAIS OPÇÕES (Três Pontos) =====
function showMoreOptions() {
  let overlay = document.getElementById('more-options-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'more-options-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.4);
      z-index: 1100;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      opacity: 0;
      transition: opacity 0.25s ease;
    `;

    // Obter o caminho base correto dependendo se está na raiz ou na pasta pages
    const isIndex = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/');
    const basePath = isIndex ? '' : '../';
    const pagesPath = isIndex ? 'pages/' : '';

    const panel = document.createElement('div');
    panel.style.cssText = `
      width: 100%;
      max-width: 480px;
      background: #fff;
      border-radius: 20px 20px 0 0;
      padding: 20px 16px 30px 16px;
      box-sizing: border-box;
      transform: translateY(100%);
      transition: transform 0.25s ease;
    `;

    panel.innerHTML = `
      <div style="width: 40px; height: 5px; background: #e0e0e0; border-radius: 3px; margin: 0 auto 20px auto;"></div>
      <h3 style="margin: 0 0 20px 0; font-size: 16px; font-weight: 600; color: #222; text-align: center;">Mais ações</h3>
      <div style="display: flex; flex-direction: column; gap: 4px;">
        <a href="${isIndex ? 'index.html' : '../index.html'}" style="display: flex; align-items: center; gap: 12px; padding: 14px 12px; text-decoration: none; color: #222; font-size: 15px; border-bottom: 1px solid #f5f5f5;">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          Página inicial da loja
        </a>
        <a href="${pagesPath}carrinho.html" style="display: flex; align-items: center; gap: 12px; padding: 14px 12px; text-decoration: none; color: #222; font-size: 15px; border-bottom: 1px solid #f5f5f5;">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>
          Ir para o carrinho
        </a>
        <div onclick="hideMoreOptions(); shareProduct();" style="display: flex; align-items: center; gap: 12px; padding: 14px 12px; color: #222; font-size: 15px; cursor: pointer; border-bottom: 1px solid #f5f5f5;">
          <img src="${basePath}img/share-arrow.png" alt="Compartilhar" style="width: 20px; height: 20px; object-fit: contain;">
          Copiar link do produto
        </div>
        <div onclick="hideMoreOptions(); showMyOrders();" style="display: flex; align-items: center; gap: 12px; padding: 14px 12px; color: #222; font-size: 15px; cursor: pointer;">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path><line x1="3" y1="6" x2="21" y2="6"></line><path d="M16 10a4 4 0 0 1-8 0"></path></svg>
          Pedidos
        </div>
      </div>
      <button onclick="hideMoreOptions()" style="margin-top: 20px; width: 100%; height: 44px; border-radius: 22px; border: 1px solid #ddd; background: #fff; font-size: 15px; font-weight: 500; color: #555; cursor: pointer;">Fechar</button>
    `;
    overlay.appendChild(panel);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) hideMoreOptions();
    });
  }

  // Ativar com transição suave
  overlay.style.display = 'flex';
  setTimeout(() => {
    overlay.style.opacity = '1';
    overlay.firstElementChild.style.transform = 'translateY(0)';
  }, 10);
}

function hideMoreOptions() {
  const overlay = document.getElementById('more-options-overlay');
  if (overlay) {
    overlay.style.opacity = '0';
    overlay.firstElementChild.style.transform = 'translateY(100%)';
    setTimeout(() => {
      overlay.style.display = 'none';
    }, 250);
  }
}

// ===== SLIDER DE IMAGENS =====
function initSlider(sliderEl) {
  if (!sliderEl) return;
  const track = sliderEl.querySelector('.slider-track');
  const counter = sliderEl.querySelector('.slider-counter');
  const dotsContainer = sliderEl.querySelector('.slider-dots');
  const imgs = track ? (track.querySelectorAll('.slider-img').length > 0 ? track.querySelectorAll('.slider-img') : track.querySelectorAll('.slide img, img')) : [];
  let current = 0;
  let startX = 0;
  let isDragging = false;
  let dragDelta = 0;

  function goto(idx) {
    current = Math.max(0, Math.min(imgs.length - 1, idx));
    if (track) track.style.transform = `translateX(calc(-${current * 100}% + 0px))`;
    const countCur = sliderEl.querySelector('#slider-count-cur');
    if (countCur) countCur.textContent = String(current + 1);
    if (counter) {
      const hasTamanho = counter.getAttribute('data-has-tamanho') || counter.textContent.includes('Tamanho');
      if (hasTamanho) {
        counter.setAttribute('data-has-tamanho', 'true');
        counter.setAttribute('role', 'button');
        counter.setAttribute('tabindex', '0');
        counter.innerHTML = `<span id="slider-counter-num">${current + 1}/${imgs.length}</span> <span class="slider-tamanho-trigger" style="cursor:pointer; margin-left:2px; font-weight:500; pointer-events:auto !important;">Tamanho</span>`;
        const triggerTab = function(ev) {
          if (ev) {
            if (typeof ev.preventDefault === 'function') ev.preventDefault();
            if (typeof ev.stopPropagation === 'function') ev.stopPropagation();
          }
          switchSliderTab('tamanho', ev);
        };
        counter.onclick = triggerTab;
        counter.ontouchend = triggerTab;
      } else {
        counter.textContent = `${current + 1}/${imgs.length}`;
      }
    }
    if (dotsContainer) {
      dotsContainer.querySelectorAll('.slider-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === current);
      });
    }
  }

  // Criar dots
  if (dotsContainer) {
    if (imgs.length <= 1) {
      dotsContainer.style.display = 'none';
    } else {
      dotsContainer.style.display = 'flex';
      dotsContainer.innerHTML = '';
      imgs.forEach((_, i) => {
        const dot = document.createElement('div');
        dot.className = 'slider-dot' + (i === 0 ? ' active' : '');
        dot.addEventListener('click', () => goto(i));
        dotsContainer.appendChild(dot);
      });
    }
  }

  // Eventos touch/mouse
  let startY = 0;
  let isHorizontalSwipe = false;

  function onStart(x, y) {
    startX = x;
    startY = y;
    isDragging = true;
    isHorizontalSwipe = false;
    dragDelta = 0;
    if (track) track.style.transition = 'none';
  }

  function onMove(e, x, y) {
    if (!isDragging) return;

    const diffX = Math.abs(x - startX);
    const diffY = Math.abs(y - startY);

    if (!isHorizontalSwipe && diffX > 5 && diffX > diffY) {
      isHorizontalSwipe = true;
    }

    if (isHorizontalSwipe) {
      if (e && e.cancelable) {
        e.preventDefault();
      }
      dragDelta = x - startX;
      if (track) track.style.transform = `translateX(calc(-${current * 100}% + ${dragDelta}px))`;
    }
  }

  function onEnd() {
    if (!isDragging) return;
    isDragging = false;
    if (track) track.style.transition = 'transform 0.3s ease-out';
    if (dragDelta < -50) goto(current + 1);
    else if (dragDelta > 50) goto(current - 1);
    else goto(current);
    dragDelta = 0;
  }

    // Não disparar drag se tocar nos botões de alternância
  sliderEl.addEventListener('touchstart', e => {
    if (e.target && (e.target.closest('.slider-counter') || e.target.closest('.slider-counter-toggle'))) return;
    onStart(e.touches[0].clientX, e.touches[0].clientY);
  }, { passive: false });
  sliderEl.addEventListener('touchmove', e => onMove(e, e.touches[0].clientX, e.touches[0].clientY), { passive: false });
  sliderEl.addEventListener('touchend', onEnd);
  sliderEl.addEventListener('mousedown', e => onStart(e.clientX, e.clientY));
  sliderEl.addEventListener('mousemove', e => { if (isDragging) onMove(e, e.clientX, e.clientY); });
  sliderEl.addEventListener('mouseup', onEnd);
  sliderEl.addEventListener('mouseleave', onEnd);

  goto(0);
}

// ===== MODAL DE FOTO E GALERIA MULTI-MÍDIA OFICIAL TIKTOK (REVIEW MEDIA VIEWER) =====
window._photoGallery = {
  items: [],
  currentIndex: 0,
  reviewMeta: null,
  touchStartX: 0,
  touchStartY: 0,
  commentExpanded: false
};

window.ensurePhotoModalStyles = function () {
  if (document.getElementById('photo-modal-style-tag')) return;
  const style = document.createElement('style');
  style.id = 'photo-modal-style-tag';
  style.textContent = `
    .photo-modal {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      background: #000000;
      z-index: 99999999;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.22s ease;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      user-select: none;
      -webkit-user-select: none;
      box-sizing: border-box;
    }
    .photo-modal.open {
      opacity: 1;
      pointer-events: auto;
    }
    .photo-modal-header {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 56px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 10000003;
      pointer-events: none;
      box-sizing: border-box;
    }
    .photo-modal-close {
      pointer-events: auto;
      cursor: pointer;
      width: 44px;
      height: 44px;
      display: flex;
      align-items: center;
      justify-content: flex-start;
      color: #ffffff;
      -webkit-tap-highlight-color: transparent;
    }
    .photo-modal-counter {
      color: #ffffff;
      font-size: 15px;
      font-weight: 600;
      letter-spacing: 0.5px;
      text-shadow: 0 1px 4px rgba(0,0,0,0.7);
      pointer-events: auto;
    }
    #photo-modal-content {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      touch-action: pan-y;
      overflow: hidden;
    }
    .photo-modal-media-wrap {
      position: relative;
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .photo-modal-media-wrap img,
    .photo-modal-media-wrap video {
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
      background: #000000;
    }
    .photo-modal-play-btn {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 68px;
      height: 68px;
      display: flex;
      align-items: center;
      justify-content: center;
      pointer-events: none;
      transition: opacity 0.2s ease, transform 0.2s ease;
      z-index: 10000002;
    }
    .photo-modal-play-btn.hidden {
      opacity: 0;
      transform: translate(-50%, -50%) scale(0.85);
    }
    .photo-modal-desktop-arrow {
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.45);
      color: #ffffff;
      display: none;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10000002;
      border: 1px solid rgba(255, 255, 255, 0.25);
      transition: background 0.2s ease;
    }
    @media (hover: hover) and (min-width: 768px) {
      .photo-modal-desktop-arrow {
        display: flex;
      }
      .photo-modal-desktop-arrow:hover {
        background: rgba(0, 0, 0, 0.8);
      }
    }
    .photo-modal-arrow-prev {
      left: 20px;
    }
    .photo-modal-arrow-next {
      right: 20px;
    }
        .photo-modal {
      position: fixed !important;
      inset: 0 !important;
      width: 100vw !important;
      height: 100vh !important;
      height: 100dvh !important;
      background: #000000 !important;
      z-index: 99999999 !important;
      display: flex !important;
      flex-direction: column !important;
      overflow: hidden !important;
    }
    .photo-modal-header {
      position: absolute !important;
      top: 0 !important;
      left: 0 !important;
      right: 0 !important;
      height: 56px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: space-between !important;
      padding: 0 16px !important;
      z-index: 10000005 !important;
      pointer-events: none !important;
    }
    .photo-modal-close {
      pointer-events: auto !important;
      cursor: pointer !important;
      width: 44px !important;
      height: 44px !important;
      display: flex !important;
      align-items: center !important;
      justify-content: flex-start !important;
      color: #ffffff !important;
      background: transparent !important;
      border: none !important;
      border-radius: 0 !important;
      position: static !important;
      top: auto !important;
      right: auto !important;
    }
    .photo-modal-counter {
      color: #ffffff !important;
      font-size: 15px !important;
      font-weight: 600 !important;
      letter-spacing: 0.5px !important;
      text-shadow: 0 1px 4px rgba(0,0,0,0.7) !important;
      pointer-events: auto !important;
      position: static !important;
      top: auto !important;
      left: auto !important;
      background: transparent !important;
      padding: 0 !important;
      border-radius: 0 !important;
    }
    .photo-modal-footer {
      position: absolute !important;
      bottom: 0 !important;
      left: 0 !important;
      right: 0 !important;
      padding: 34px 16px max(78px, calc(env(safe-area-inset-bottom, 0px) + 65px)) 16px !important;
      background: linear-gradient(to top, rgba(0,0,0,0.96) 0%, rgba(0,0,0,0.7) 65%, transparent 100%) !important;
      z-index: 10000004 !important;
      pointer-events: auto !important;
      box-sizing: border-box !important;
      max-height: 50vh !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: flex-end !important;
    }
    .photo-modal-user-row {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }
    .photo-modal-user-avatar {
      width: 26px;
      height: 26px;
      border-radius: 50%;
      object-fit: cover;
      flex-shrink: 0;
      border: 1px solid rgba(255, 255, 255, 0.25);
    }
    .photo-modal-user-name {
      font-size: 13.5px;
      font-weight: 600;
      color: #ffffff;
      letter-spacing: 0.2px;
    }
    .photo-modal-stars {
      color: #ffb800;
      font-size: 13px;
      letter-spacing: 1px;
      display: inline-flex;
      align-items: center;
    }
    .photo-modal-comment-wrap {
      font-size: 13.5px;
      line-height: 1.45;
      color: #ffffff;
      word-break: break-word;
      max-height: 120px;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
    }
    .photo-modal-ver-mais {
      color: #ffffff;
      font-weight: 700;
      cursor: pointer;
      margin-left: 4px;
      text-decoration: underline;
      display: inline-block;
    }
    .photo-modal-video-progress {
      position: absolute;
      bottom: 0;
      left: 0;
      width: 0%;
      height: 2.5px;
      background: #ffffff;
      z-index: 10000004;
      transition: width 0.1s linear;
    }
  `;
  document.head.appendChild(style);
};

function formatReviewMaskedName(raw) {
  if (!raw) return 'C**a D**e';
  const clean = String(raw).trim();
  if (clean.includes('*')) return clean;
  const parts = clean.split(/\s+/);
  if (parts.length === 1) {
    const single = parts[0];
    return single.length <= 2 ? single + '**' : single[0] + '**' + single[single.length - 1];
  }
  const first = parts[0];
  const last = parts[parts.length - 1];
  const m1 = first.length <= 2 ? first + '**' : first[0] + '**' + first[first.length - 1];
  const m2 = last.length <= 2 ? last + '**' : last[0] + '**' + last[last.length - 1];
  return `${m1} ${m2}`;
}


window.formatReviewMaskedName = formatReviewMaskedName;

window.ttOpenReviewMedia = function(reviewId, mediaIndex) {
  if (typeof _ttFullReviewsData === 'undefined' || !_ttFullReviewsData || !_ttFullReviewsData.reviews) return;
  const rev = _ttFullReviewsData.reviews.find(r => r.id === reviewId);
  if (!rev || !rev.media || rev.media.length === 0) return;
  
  if (typeof openPhotoModal === 'function') {
    openPhotoModal(rev.media, mediaIndex || 0, {
      avatar: rev.avatar,
      name: rev.name,
      stars: rev.stars,
      comment: rev.comment
    });
  }
};

function openPhotoModal(input, startIndex = 0, explicitMeta = null) {
  let items = [];
  let foundMeta = explicitMeta || null;

  if (Array.isArray(input)) {
    items = input.map(item => {
      if (typeof item === 'string') {
        return {
          src: item,
          isVideo: /\.(mp4|webm|mov|m4v)($|\?)/i.test(item) || item.includes('/mms/')
        };
      }
      return {
        src: item.src || '',
        isVideo: !!item.isVideo || (item.src && (/\.(mp4|webm|mov|m4v)($|\?)/i.test(item.src) || item.src.includes('/mms/')))
      };
    });
  } else if (input) {
    let targetEl = (input instanceof HTMLElement) ? input : null;
    let srcStr = (typeof input === 'string') ? input : (targetEl ? targetEl.src : '');

    if (!targetEl && srcStr) {
      targetEl = Array.from(document.querySelectorAll('.review-card img, .review-card video, .review-photos img, .review-photos video, .review-compact-thumb-wrap img, .tt-full-review-card img, .tt-rev-media-item img'))
        .find(el => el.src === srcStr || (srcStr && el.src.endsWith(srcStr.replace(/^(\.\.\/|\.\/)/, ''))));
    }

    if (targetEl) {
      const card = targetEl.closest('.review-card, .tt-full-review-card');
      if (card) {
        // Extrai todas as mídias irmãs deste card
        const rawMediaEls = Array.from(card.querySelectorAll('.review-photos img, .review-photos video, .review-photo, .review-compact-thumb-wrap img, .review-compact-thumb-wrap video, .tt-rev-media-item img, .tt-rev-media-item video'));
        const seen = new Set();
        const cardItems = [];
        rawMediaEls.forEach(el => {
          const s = el.src || '';
          if (s && !seen.has(s)) {
            seen.add(s);
            cardItems.push({
              src: s,
              isVideo: el.tagName === 'VIDEO' || /\.(mp4|webm|mov|m4v)($|\?)/i.test(s) || s.includes('/mms/')
            });
          }
        });
        if (cardItems.length > 0) {
          items = cardItems;
          const foundIdx = cardItems.findIndex(it => it.src === srcStr || (srcStr && it.src.endsWith(srcStr.replace(/^(\.\.\/|\.\/)/, ''))));
          startIndex = foundIdx >= 0 ? foundIdx : 0;
        }

        // Extrai metadados do autor do comentário
        if (!foundMeta) {
          const avatarUrl = card.getAttribute('data-author-avatar') || card.querySelector('.review-avatar img, .tt-rev-user-avatar img')?.src || '../img/reviews-avatars/default-avatar.svg';
          const rawName = card.getAttribute('data-author-name') || card.querySelector('.review-user-name, .tt-rev-user-name')?.textContent.trim() || '';
          
          let maskedName = '';
          if (rawName && !rawName.toLowerCase().includes('cliente oficial')) {
            maskedName = formatReviewMaskedName(rawName);
          } else {
            const pool = (typeof BRAZILIAN_MASKED_NAMES !== 'undefined' && BRAZILIAN_MASKED_NAMES.length > 0)
              ? BRAZILIAN_MASKED_NAMES
              : ['M**a C**o', 'C**a D**e', 'L**a M**s', 'B**z L**a', 'J**e S**a', 'R**a G**s'];
            maskedName = pool[0];
          }

          let starCount = parseInt(card.getAttribute('data-author-stars')) || 0;
          if (!starCount) {
            const starsEl = card.querySelector('.review-user-stars, .tt-rev-stars');
            starCount = 5;
            if (starsEl) {
              const poly = starsEl.querySelectorAll('polygon, svg').length;
              if (poly > 0) starCount = poly;
              else if (starsEl.textContent.includes('4')) starCount = 4;
              else if (starsEl.textContent.includes('3')) starCount = 3;
              else if (starsEl.textContent.includes('2')) starCount = 2;
              else if (starsEl.textContent.includes('1')) starCount = 1;
            }
          }

          const commentText = card.getAttribute('data-author-comment') || card.querySelector('.review-comment, .tt-rev-comment')?.textContent.trim() || 'Potência me surpreendeu muito! Puxou toda a terra seca do carpete do carro e ainda limpei os teclados do escritório.';

          foundMeta = {
            avatar: avatarUrl,
            name: maskedName,
            stars: starCount,
            comment: commentText
          };
        }
      }
    }

    if (items.length === 0 && srcStr) {
      items = [{
        src: srcStr,
        isVideo: /\.(mp4|webm|mov|m4v)($|\?)/i.test(srcStr) || srcStr.includes('/mms/')
      }];
      startIndex = 0;
    }
  }

  if (!items || items.length === 0) return;

  // Fallback de autor se ainda não tiver
  if (!foundMeta) {
    const pool = (typeof BRAZILIAN_MASKED_NAMES !== 'undefined' && BRAZILIAN_MASKED_NAMES.length > 0)
      ? BRAZILIAN_MASKED_NAMES
      : ['M**a C**o', 'C**a D**e', 'L**a M**s', 'B**z L**a'];
    foundMeta = {
      avatar: '../img/reviews-avatars/default-avatar.svg',
      name: pool[0],
      stars: 5,
      comment: 'Produto excelente, superou minhas expectativas e chegou super rápido!'
    };
  }

  window.ensurePhotoModalStyles();

  window._photoGallery.items = items;
  window._photoGallery.currentIndex = Math.max(0, Math.min(startIndex, items.length - 1));
  window._photoGallery.reviewMeta = foundMeta;
  window._photoGallery.commentExpanded = false;

  let modal = document.getElementById('photo-modal');
  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'photo-modal';
    modal.className = 'photo-modal';
    modal.innerHTML = `
      <!-- Header do TikTok -->
      <div class="photo-modal-header">
        <div class="photo-modal-close" onclick="closePhotoModal()" aria-label="Fechar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </div>
        <div id="photo-modal-counter" class="photo-modal-counter">1/1</div>
      </div>

      <!-- Setas Desktop -->
      <div class="photo-modal-desktop-arrow photo-modal-arrow-prev" onclick="prevPhotoModalItem(event)" aria-label="Anterior">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </div>
      <div class="photo-modal-desktop-arrow photo-modal-arrow-next" onclick="nextPhotoModalItem(event)" aria-label="Próxima">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>

      <!-- Viewport Principal com Touch Gestures -->
      <div id="photo-modal-content"></div>

      <!-- Rodapé TikTok com Autor, Estrelas e Comentário -->
      <div class="photo-modal-footer" id="photo-modal-footer">
        <div class="photo-modal-user-row">
          <img id="photo-modal-user-avatar" class="photo-modal-user-avatar" src="../img/reviews-avatars/default-avatar.svg" alt="" onerror="this.src='../img/reviews-avatars/default-avatar.svg'">
          <span id="photo-modal-user-name" class="photo-modal-user-name">M**l B**o</span>
          <span id="photo-modal-stars" class="photo-modal-stars">★★★★★</span>
        </div>
        <div class="photo-modal-comment-wrap" id="photo-modal-comment-wrap">
          <span id="photo-modal-comment-text"></span>
          <span id="photo-modal-ver-mais" class="photo-modal-ver-mais" onclick="ttToggleViewerComment(event)">... Ver mais</span>
        </div>
      </div>
    `;

    // Touch Swipe Support ("só passa pro lado")
    modal.addEventListener('touchstart', e => {
      if (e.touches && e.touches.length > 0) {
        window._photoGallery.touchStartX = e.touches[0].clientX;
        window._photoGallery.touchStartY = e.touches[0].clientY;
      }
    }, { passive: true });

    modal.addEventListener('touchend', e => {
      if (!e.changedTouches || e.changedTouches.length === 0) return;
      const diffX = e.changedTouches[0].clientX - window._photoGallery.touchStartX;
      const diffY = e.changedTouches[0].clientY - window._photoGallery.touchStartY;
      if (Math.abs(diffX) > 35 && Math.abs(diffX) > Math.abs(diffY)) {
        if (diffX < 0) {
          nextPhotoModalItem();
        } else {
          prevPhotoModalItem();
        }
      }
    }, { passive: true });

    // Keyboard support
    document.addEventListener('keydown', e => {
      const m = document.getElementById('photo-modal');
      if (!m || !m.classList.contains('open')) return;
      if (e.key === 'ArrowRight') nextPhotoModalItem();
      if (e.key === 'ArrowLeft') prevPhotoModalItem();
      if (e.key === 'Escape') closePhotoModal();
      if (e.key === ' ') {
        e.preventDefault();
        ttToggleModalVideoPlay();
      }
    });

    document.body.appendChild(modal);
  }

  updatePhotoModalView();
  modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function updatePhotoModalView() {
  const g = window._photoGallery;
  if (!g.items || g.items.length === 0) return;

  const currentItem = g.items[g.currentIndex];
  const container = document.getElementById('photo-modal-content');
  const counter = document.getElementById('photo-modal-counter');
  const prevArrow = document.querySelector('.photo-modal-arrow-prev');
  const nextArrow = document.querySelector('.photo-modal-arrow-next');

  // Atualiza contador 1/4 no topo direito
  if (counter) {
    counter.textContent = `${g.currentIndex + 1}/${g.items.length}`;
  }

  // Setas desktop aparecem se houver mais de 1 mídia
  if (prevArrow && nextArrow) {
    const showArrows = g.items.length > 1;
    prevArrow.style.display = showArrows ? '' : 'none';
    nextArrow.style.display = showArrows ? '' : 'none';
  }

  // Atualiza rodapé com dados do autor
  const meta = g.reviewMeta || {
    avatar: '../img/reviews-avatars/default-avatar.svg',
    name: 'M**l B**o',
    stars: 5,
    comment: ''
  };

  const avatarImg = document.getElementById('photo-modal-user-avatar');
  if (avatarImg) avatarImg.src = meta.avatar || '../img/reviews-avatars/default-avatar.svg';

  const nameSpan = document.getElementById('photo-modal-user-name');
  if (nameSpan) nameSpan.textContent = meta.name || 'M**l B**o';

  const starsSpan = document.getElementById('photo-modal-stars');
  if (starsSpan) {
    const count = Math.max(1, Math.min(5, meta.stars || 5));
    starsSpan.textContent = '★'.repeat(count);
  }

  const commentTextSpan = document.getElementById('photo-modal-comment-text');
  const verMaisBtn = document.getElementById('photo-modal-ver-mais');
  const fullComment = meta.comment || '';

  if (commentTextSpan) {
    if (fullComment.length > 75 && !g.commentExpanded) {
      commentTextSpan.textContent = fullComment.slice(0, 75);
      if (verMaisBtn) verMaisBtn.style.display = 'inline-block';
    } else {
      commentTextSpan.textContent = fullComment;
      if (verMaisBtn) verMaisBtn.style.display = 'none';
    }
  }

  // Renderiza mídia central (Vídeo com botão Play ou Imagem para passar pro lado)
  if (container) {
    if (currentItem.isVideo) {
      container.innerHTML = `
        <div class="photo-modal-media-wrap is-video" onclick="ttToggleModalVideoPlay(event)">
          <video id="photo-modal-video" src="${currentItem.src}" playsinline webkit-playsinline loop preload="auto"></video>
          <!-- Botão Play oficial TikTok com drop-shadow -->
          <div class="photo-modal-play-btn" id="photo-modal-play-btn">
            <svg viewBox="0 0 24 24" width="60" height="60" fill="#ffffff" style="filter: drop-shadow(0 2px 10px rgba(0,0,0,0.55));">
              <polygon points="7 4 20 12 7 20"></polygon>
            </svg>
          </div>
          <div class="photo-modal-video-progress" id="photo-modal-video-progress"></div>
        </div>
      `;

      const vid = document.getElementById('photo-modal-video');
      const progress = document.getElementById('photo-modal-video-progress');
      if (vid) {
        vid.addEventListener('timeupdate', () => {
          if (progress && vid.duration) {
            progress.style.width = ((vid.currentTime / vid.duration) * 100) + '%';
          }
        });
        vid.addEventListener('play', () => {
          const playBtn = document.getElementById('photo-modal-play-btn');
          if (playBtn) playBtn.classList.add('hidden');
        });
        vid.addEventListener('pause', () => {
          const playBtn = document.getElementById('photo-modal-play-btn');
          if (playBtn) playBtn.classList.remove('hidden');
        });
      }
    } else {
      container.innerHTML = `
        <div class="photo-modal-media-wrap is-image">
          <img id="photo-modal-img" src="${currentItem.src}" alt="Mídia da avaliação" onerror="var w=this.closest('.review-compact-thumb-wrap');if(w){w.style.display='none';}">
        </div>
      `;
    }
  }
}

window.ttToggleModalVideoPlay = function(e) {
  if (e) {
    if (e.target && e.target.closest && e.target.closest('.photo-modal-header, .photo-modal-footer, .photo-modal-desktop-arrow')) return;
    e.stopPropagation();
  }
  const vid = document.getElementById('photo-modal-video');
  const playBtn = document.getElementById('photo-modal-play-btn');
  if (!vid) return;

  if (vid.paused) {
    vid.play().then(() => {
      if (playBtn) playBtn.classList.add('hidden');
    }).catch(() => {});
  } else {
    vid.pause();
    if (playBtn) playBtn.classList.remove('hidden');
  }
};

window.ttToggleViewerComment = function(e) {
  if (e) e.stopPropagation();
  window._photoGallery.commentExpanded = true;
  const meta = window._photoGallery.reviewMeta;
  const commentTextSpan = document.getElementById('photo-modal-comment-text');
  const verMaisBtn = document.getElementById('photo-modal-ver-mais');
  if (commentTextSpan && meta) {
    commentTextSpan.textContent = meta.comment || '';
  }
  if (verMaisBtn) verMaisBtn.style.display = 'none';
};

function nextPhotoModalItem(e) {
  if (e && typeof e.stopPropagation === 'function') e.stopPropagation();
  const g = window._photoGallery;
  if (!g.items || g.items.length <= 1) return;
  
  // Pausa vídeo atual se existir
  const curVid = document.getElementById('photo-modal-video');
  if (curVid) curVid.pause();

  g.currentIndex = (g.currentIndex + 1) % g.items.length;
  updatePhotoModalView();
}

function prevPhotoModalItem(e) {
  if (e && typeof e.stopPropagation === 'function') e.stopPropagation();
  const g = window._photoGallery;
  if (!g.items || g.items.length <= 1) return;

  // Pausa vídeo atual se existir
  const curVid = document.getElementById('photo-modal-video');
  if (curVid) curVid.pause();

  g.currentIndex = (g.currentIndex - 1 + g.items.length) % g.items.length;
  updatePhotoModalView();
}

function selectPhotoModalIndex(index, e) {
  if (e && typeof e.stopPropagation === 'function') e.stopPropagation();
  const g = window._photoGallery;
  if (!g.items || index < 0 || index >= g.items.length) return;

  const curVid = document.getElementById('photo-modal-video');
  if (curVid) curVid.pause();

  g.currentIndex = index;
  updatePhotoModalView();
}

function closePhotoModal() {
  const modal = document.getElementById('photo-modal');
  if (modal) {
    modal.classList.remove('open');
    const curVid = document.getElementById('photo-modal-video');
    if (curVid) curVid.pause();
    const container = document.getElementById('photo-modal-content');
    if (container) container.innerHTML = '';
  }
  document.body.style.overflow = '';
}


// ===== TIMER DE OFERTA RELÂMPAGO =====
function initOfertaTimer() {
  const timers = document.querySelectorAll('.oferta-timer');
  if (!timers.length) return;

  let endTime = parseInt(localStorage.getItem('oferta_end')) || 0;
  const now = Date.now();
  if (!endTime || endTime < now) {
    endTime = now + (3 * 3600 + 45 * 60 + 18) * 1000;
    localStorage.setItem('oferta_end', endTime);
  }

  function tick() {
    const remaining = Math.max(0, endTime - Date.now());
    const h = Math.floor(remaining / 3600000);
    const m = Math.floor((remaining % 3600000) / 60000);
    const s = Math.floor((remaining % 60000) / 1000);
    const str = `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
    timers.forEach(t => { t.textContent = str; });
    if (remaining <= 0) {
      endTime = Date.now() + 4 * 3600 * 1000;
      localStorage.setItem('oferta_end', endTime);
    }
  }
  tick();
  setInterval(tick, 1000);
}

// ===== CONTADOR DE PESSOAS OLHANDO E ESTOQUE DE URGÊNCIA (simulado) =====
function initPessoasOlhando() { return; }

// ===== ESTADO E PAGINAÇÃO DE AVALIAÇÕES (TIKTOK SHOP BLINDADO) =====
const reviewPaginationState = {};

function initReviewPagination() {
  formatCompactReviews();
  renderStoreReviewsFilter();
}

function verMaisReviews(containerId, btnId, totalOriginal) {
  if (typeof expandStoreReviews === 'function') {
    expandStoreReviews();
  }
}

// ===== CORES DOS AVATARES POR INICIAL =====
function initAvatarColors() {
  const CORES_PALETA = [
    '#5c6bc0', // Azul/Violeta
    '#26a69a', // Verde/Teal
    '#26c6da', // Ciano
    '#66bb6a', // Verde claro
    '#8d6e63', // Marrom suave
    '#78909c', // Azul acinzentado
    '#ffa726', // Laranja suave
    '#ab47bc', // Roxo
    '#ec407a', // Rosa escuro
    '#7e57c2', // Roxo médio
    '#29b6f6'  // Azul celeste
  ];

  const placeholders = document.querySelectorAll('.review-avatar-placeholder');
  placeholders.forEach(placeholder => {
    const letra = placeholder.textContent.trim().toUpperCase();
    if (letra) {
      const charCode = letra.charCodeAt(0);
      const cor = CORES_PALETA[charCode % CORES_PALETA.length];
      placeholder.style.setProperty('background', cor, 'important');
      placeholder.style.setProperty('background-color', cor, 'important');
    }
  });
}

// ===== PRODUTOS RELACIONADOS DINÂMICOS — MASONRY CASCATA REAL COM VÍDEO E DADOS 1:1 TIKTOK SHOP =====

// ===== SKELETON / LOADING 1:1 TIKTOK SHOP (Fundo #f5f5f5 + 1 barra título + 2 blocos suaves #f9f9f9) =====
function getRelatedSkeletonHtml() {
  return `
    <div class="tt-related-skeleton-wrap" style="width:100%; padding:2px 0 10px; box-sizing:border-box;">
      <div class="tt-rel-skel-shimmer" style="width:48%; height:18px; border-radius:4px; margin:0 0 12px 2px;"></div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; width:100%;">
        <div class="tt-rel-skel-shimmer" style="width:100%; height:246px; border-radius:8px;"></div>
        <div class="tt-rel-skel-shimmer" style="width:100%; height:246px; border-radius:8px;"></div>
      </div>
    </div>
  `;
}

function renderRelacionados() {
  const grid = document.querySelector('.related-grid');
  if (!grid) return;
  if (typeof CATALOGO_PRODUTOS === 'undefined') return;

  const idAtual = typeof PRODUTO_ATUAL !== 'undefined' ? Number(PRODUTO_ATUAL.id) : -1;
  const isPagesDir = typeof window !== 'undefined' && window.location.pathname.includes('/pages/');
  const pathPrefix = isPagesDir ? '../' : '';

  function fixPath(src) {
    if (!src) return pathPrefix + 'logo.png';
    if (src.startsWith('http://') || src.startsWith('https://')) return src;
    if (isPagesDir) {
      if (src.startsWith('../')) return src;
      return '../' + src.replace(/^\.?\//, '');
    } else {
      return src.replace(/^\.\.\//, '');
    }
  }

  // Mapa rigoroso de vídeos 1:1 por ID do produto
  const PRODUTO_VIDEOS_MAP = {
    104: {
      video: 'https://files.catbox.moe/tsjc1l.mp4',
      poster: fixPath('img/poster-chinelo-real-1.jpg'),
      name: 'Kethellen Jade',
      avatar: fixPath('img/reviews-avatars/review-user-104-c10.jpg'),
      duracao: '00:40'
    },
    106: {
      video: 'https://files.catbox.moe/jpmxf4.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-106.jpg'),
      name: 'Giulia Ferreira',
      avatar: fixPath('img/reviews-avatars/review-user-1.jpg'),
      duracao: '00:28'
    },
    107: {
      video: 'https://files.catbox.moe/nwhxcm.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-107.jpg'),
      name: 'Bia Resenhas',
      avatar: fixPath('img/reviews-avatars/review-user-10.jpg'),
      duracao: '00:24'
    },
    108: {
      video: 'https://files.catbox.moe/e7z9vc.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-108.jpg'),
      name: 'Camila Resenhas',
      avatar: fixPath('img/reviews-avatars/review-user-2.jpg'),
      duracao: '00:32'
    },
    109: {
      video: 'https://files.catbox.moe/bjcwqr.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-109.jpg'),
      name: 'Lorena Cachos',
      avatar: fixPath('img/reviews-avatars/review-user-3.jpg'),
      duracao: '00:35'
    },
    110: {
      video: 'https://files.catbox.moe/2t30kf.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-110.jpg'),
      name: 'Lucas Running',
      avatar: fixPath('img/reviews-avatars/review-user-103-c3.jpg'),
      duracao: '00:28'
    },
    111: {
      video: 'https://files.catbox.moe/facj5t.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-111.jpg'),
      name: 'Decorações & Dicas',
      avatar: fixPath('img/reviews-avatars/review-user-111-de.jpg'),
      duracao: '00:25'
    },
    112: {
      video: 'https://files.catbox.moe/geut5n.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-112.jpg'),
      name: 'Brinquedos Kids',
      avatar: fixPath('img/reviews-avatars/review-user-112-c1.jpg'),
      duracao: '00:20'
    },
    113: {
      video: 'https://files.catbox.moe/grwbds.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-113.jpg'),
      name: 'Pets & Dicas',
      avatar: fixPath('img/reviews-avatars/review-user-4.jpg'),
      duracao: '00:25'
    },
    114: {
      video: 'https://files.catbox.moe/cfm2lc.mp4',
      poster: fixPath('videosprodutos/posters/poster-produto-114.jpg'),
      name: 'Gamer Retro TV',
      avatar: fixPath('img/reviews-avatars/review-user-114-c2.jpg'),
      duracao: '00:30'
    }
  };

  const outros = CATALOGO_PRODUTOS.filter(p => Number(p.id) !== idAtual);
  const cardsData = [];

  // Exatamente 2 cards de vídeo no feed inteiro, bem espaçados
  let videoSlotsCount = 0;
  // Bruno CTO: ZERO vídeos de outros produtos tocando em feed de páginas individuais
  const maxVideoSlots = 0;

  outros.slice(0, 16).forEach((p, idx) => {
    const pPrecoNum = typeof p.preco === 'number' ? p.preco : parseFloat(String(p.preco).replace(',', '.')) || 39.90;
    const pPreco = pPrecoNum.toFixed(2).replace('.', ',');
    const pPrecoOrig = p.precoOrig ? String(p.precoOrig) : (pPrecoNum * 2.5).toFixed(2).replace('.', ',');
  const pVendidos = p.vendidos
      ? String(p.vendidos).replace(/\./g, '') + ' vendidos'
      : String(5120 + ((p.id * 731) % 8800)) + ' vendidos';

    const vInfo = PRODUTO_VIDEOS_MAP[p.id];
    // Ativa vídeo estritamente em apenas 2 posições espaçadas (1º no card 1 e 2º no card 5 ou 6)
    const isTargetSlot = (videoSlotsCount === 0 && (idx === 1 || idx === 0)) || (videoSlotsCount === 1 && (idx === 4 || idx === 5 || idx === 6));
    const shouldHaveVideo = vInfo && videoSlotsCount < maxVideoSlots && isTargetSlot;
    
    let itemVideo = null;
    let itemPoster = null;
    let itemCreatorName = null;
    let itemCreatorAvatar = null;
    let itemDuracao = null;

    if (shouldHaveVideo) {
      itemVideo = vInfo.video;
      itemPoster = vInfo.poster;
      itemCreatorName = vInfo.name;
      itemCreatorAvatar = vInfo.avatar;
      itemDuracao = vInfo.duracao;
      videoSlotsCount++;
    }

    cardsData.push({
      id: p.id,
      video: itemVideo,
      poster: itemPoster,
      name: itemCreatorName,
      avatar: itemCreatorAvatar,
      duracao: itemDuracao,
      img: fixPath(p.img),
      title: p.nome,
      preco: pPreco,
      precoOrig: pPrecoOrig,
      is1111: (idx % 3 === 0),
      badgeTipo: 'off_frete',
      descOff: (p.desc || 60) + '% OFF',
      rating: (4.7 + ((p.id * 3) % 3) * 0.1).toFixed(1).replace('.', ','),
      vendidos: pVendidos
    });
  });

  // Proporções verticais para o Masonry
  const ASPECT_RATIOS = ['3 / 4', '4 / 5', '1 / 1', '4 / 5', '3 / 4', '4 / 5', '1 / 1', '3 / 4'];

  function buildCardHtml(item, idx) {
    const ratio = item.video ? '3 / 4' : (idx % 3 === 0 ? '4 / 5' : '1 / 1');
    const linkHref = isPagesDir ? `produto-${item.id}.html` : `pages/produto-${item.id}.html`;
    
    const parts = (item.preco || '19,90').split(',');
    const precoInt = parts[0];
    const precoCent = parts[1] || '00';

    const badgeBfSrc = isPagesDir ? '../img/badge-blackfriday.png' : 'img/badge-blackfriday.png';
    const badge1111Html = item.is1111 ? `
      <img class="badge-1111" src="${badgeBfSrc}" alt="Black Friday" style="height:13.5px; width:auto; vertical-align:-2px; margin-right:4px; display:inline-block; flex-shrink:0;">
    ` : '';

    let badgesHtml = '';
    if (item.badgeTipo === 'relampago') {
      badgesHtml = `
        <span style="background:#fff2e8; color:#ff5722; font-size:9.5px; font-weight:700; padding:1px 4.5px; border-radius:2px; display:inline-flex; align-items:center; gap:2px; line-height:1.2;">
          <svg width="8" height="8" viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h8l-1 8 11-12h-8l1-8z"/></svg> Oferta Relâmpago
        </span>
      `;
    } else {
      badgesHtml = `
        <span style="background:#ffeeef; color:#fe2c55; font-size:9.5px; font-weight:700; padding:1px 4.5px; border-radius:2px; display:inline-flex; align-items:center; gap:3px; line-height:1.2;">
          <svg width="10" height="8" viewBox="0 0 667 534" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;"><path d="M666.666 166.667C640.145 166.667 614.71 177.203 595.956 195.956C577.202 214.71 566.666 240.145 566.666 266.667C566.666 293.189 577.202 318.624 595.956 337.378C614.71 356.131 640.145 366.667 666.666 366.667L666.666 466.667C666.666 484.348 659.642 501.305 647.14 513.808C634.637 526.31 617.681 533.334 600 533.334L466.666 533.334L466.666 470.601C466.666 461.76 463.154 453.281 456.903 447.03C450.652 440.779 442.174 437.267 433.333 437.267C424.492 437.267 416.014 440.779 409.763 447.03C403.512 453.281 400 461.76 400 470.601L400 533.334L66.666 533.334C48.9852 533.334 32.0287 526.31 19.5264 513.808C7.02395 501.305 1.13666e-05 484.348 1.01189e-05 466.667L1.44901e-05 366.666C55.4279 366.576 100.333 266.167 100.333 266.167C100.333 210.718 55.4279 165.758 2.3276e-05 165.668L2.76035e-05 66.667C3.0397e-05 48.9859 7.02397 32.0288 19.5264 19.5264C32.0287 7.02422 48.9852 8.86041e-05 66.666 4.76048e-07L400 1.50465e-05L400 62.7334C400 71.5739 403.512 80.0525 409.763 86.3037C416.014 92.5549 424.492 96.0674 433.333 96.0674C442.174 96.0674 450.652 92.5549 456.903 86.3037C463.154 80.0525 466.666 71.5739 466.666 62.7334L466.666 1.79606e-05L600 2.37888e-05C617.681 0.000113468 634.637 7.02425 647.14 19.5264C659.642 32.0288 666.666 48.9859 666.666 66.667L666.666 166.667ZM466.666 156.867C466.666 148.027 463.154 139.548 456.903 133.297C450.652 127.046 442.174 123.533 433.333 123.533C424.492 123.533 416.014 127.046 409.763 133.297C403.512 139.548 400 148.027 400 156.867L400 219.601C400 228.441 403.512 236.92 409.763 243.171C416.014 249.422 424.493 252.934 433.333 252.934C442.174 252.934 450.652 249.422 456.903 243.171C463.154 236.92 466.666 228.441 466.666 219.601L466.666 156.867ZM466.666 313.733C466.666 304.893 463.154 296.414 456.903 290.163C450.652 283.912 442.174 280.4 433.333 280.4C424.493 280.4 416.014 283.912 409.763 290.163C403.512 296.414 400 304.893 400 313.733L400 376.467C400 385.307 403.512 393.786 409.763 400.037C416.014 406.288 424.492 409.801 433.333 409.801C442.174 409.801 450.652 406.288 456.903 400.037C463.154 393.786 466.666 385.307 466.666 376.467L466.666 313.733Z" fill="currentColor"></path></svg> ${item.descOff || '60% OFF'}
        </span>
        <span style="background:#e6f9f6; color:#00a699; font-size:9.5px; font-weight:600; padding:1px 4.5px; border-radius:2px; line-height:1.2;">Frete grátis</span>
      `;
    }

    return `
      <a class="related-card" href="${linkHref}" style="background:#ffffff; border-radius:8px; overflow:hidden; border:none; box-shadow:0 1px 3px rgba(0,0,0,0.05); text-decoration:none; color:inherit; display:flex; flex-direction:column; width:100%; box-sizing:border-box; position:relative; margin-bottom:8px; font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text','TikTok Sans','Plus Jakarta Sans',sans-serif;">
        <div class="related-img-wrapper" style="position:relative; width:100%; aspect-ratio:${ratio}; overflow:hidden; background:#000;">
          ${item.video ? `
            <video class="related-card-video" src="${item.video}" poster="${item.poster || ''}" autoplay muted loop playsinline style="width:100%; height:100%; object-fit:cover; display:block;"></video>
            <!-- BADGE DE PLAY/PAUSE E TEMPO 1:1 TIKTOK SHOP OFICIAL (IMAGEM 2) -->
            <div class="tt-feed-video-badge" style="position:absolute; top:6px; left:6px; background:rgba(0,0,0,0.45); color:#ffffff; font-size:10.5px; font-weight:600; padding:2px 5.5px; height:18px; box-sizing:border-box; border-radius:4px; display:inline-flex; align-items:center; gap:3.5px; backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px); z-index:4; font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text','TikTok Sans','Plus Jakarta Sans',sans-serif; letter-spacing:0.2px; cursor:pointer; user-select:none;">
              <!-- Ícone dinâmico: Pause ❚❚ quando tocando / Play ▶ quando pausado -->
              <span class="tt-feed-video-icon" style="display:inline-flex; align-items:center; height:9px;">
                <span style="display:inline-flex; align-items:center; gap:1.8px; height:9px;">
                  <span style="width:2px; height:8.5px; background:#ffffff; border-radius:0.5px;"></span>
                  <span style="width:2px; height:8.5px; background:#ffffff; border-radius:0.5px;"></span>
                </span>
              </span>
              <span class="tt-feed-video-time" style="font-size:10.5px; font-weight:600; line-height:1; letter-spacing:0.2px;">${item.duracao || '00:04'}</span>
            </div>
            <!-- GRADIENT DE CONTRASTE -->
            <div style="position:absolute; bottom:0; left:0; width:100%; height:35%; background:linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.55) 100%); pointer-events:none; z-index:2;"></div>
            <!-- CRIADOR: AVATAR + NOME OFICIAL -->
            <div style="position:absolute; bottom:6px; left:6px; display:flex; align-items:center; gap:5px; z-index:3; max-width:calc(100% - 12px);">
              <img src="${item.avatar}" style="width:18px; height:18px; border-radius:50%; object-fit:cover; border:1.5px solid #ffffff; box-shadow:0 1px 2px rgba(0,0,0,0.4); flex-shrink:0;" alt="">
              <span style="color:#ffffff; font-size:11px; font-weight:600; text-shadow:0 1px 2px rgba(0,0,0,0.85); letter-spacing:-0.1px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${item.name}</span>
            </div>
          ` : `
            <img src="${item.img}" alt="${item.title}" loading="lazy" style="width:100%; height:100%; object-fit:cover; display:block;">
          `}
        </div>
        <div class="related-card-info" style="padding:6px 7px 8px; display:flex; flex-direction:column; gap:3.5px; flex:1;">
          <!-- LINHA DO TÍTULO COM MINI-THUMBNAIL DO PRODUTO (PARIDADE 1:1 TIKTOK SHOP) -->
          <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:5px;">
            <h4 class="related-card-title" style="font-size:12.5px; font-weight:400; line-height:1.3; color:#161823; margin:0; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; flex:1; min-width:0; letter-spacing:-0.1px;">
              ${badge1111Html}${item.title}
            </h4>
            ${item.video ? `
              <!-- QUADRADINHO DO PRODUTO (THUMBNAIL OFICIAL) -->
              <img src="${item.img}" alt="${item.title}" style="width:34px; height:34px; min-width:34px; border-radius:3px; object-fit:cover; border:1px solid #f0f0f0; margin-top:1px; flex-shrink:0;" loading="lazy">
            ` : ''}
          </div>

          <div style="display:flex; align-items:baseline; gap:3px; margin-top:2px;">
            <div style="color:#fe2c55; font-size:11px; font-weight:700; line-height:1; display:flex; align-items:baseline;">
              R$ <span style="font-size:16px; font-weight:800; margin-left:1px;">${precoInt}</span><span style="font-size:11px; font-weight:700;">,${precoCent}</span>
            </div>
            <span style="color:#8a8b91; font-size:10.5px; text-decoration:line-through; margin-left:2px;">R$ ${item.precoOrig}</span>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:3px; margin-top:1px;">
            ${badgesHtml}
          </div>
          <div style="display:flex; align-items:center; gap:2.5px; margin-top:2px; font-size:10.5px; color:#73747b;">
            <span style="display:inline-flex; align-items:center; gap:2.5px;">
              <svg viewBox="0 0 24 24" width="11" height="11" fill="#ffb800" style="display:inline-block; vertical-align:middle; flex-shrink:0;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
              <span style="font-size:10.5px; font-weight:500; color:#555; line-height:1;">${String(item.rating || '4.8').replace('.', ',')}</span>
            </span>
            <span style="color:#e0e0e0; font-size:9px; margin:0 1px;">|</span>
            <span style="color:#73747b; font-size:10.5px; font-weight:400; line-height:1;">${item.vendidos}</span>
          </div>
        </div>
      </a>
    `;
  }

  // Divisão balanceada em 2 colunas para efeito Masonry fluido
  const colLeft = [];
  const colRight = [];

  cardsData.forEach((item, i) => {
    if (i % 2 === 0) {
      colLeft.push(buildCardHtml(item, i));
    } else {
      colRight.push(buildCardHtml(item, i));
    }
  });

  const finalMasonryHtml = `
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colLeft.join('')}
    </div>
    <div class="masonry-column" style="display:flex; flex-direction:column; flex:1; min-width:0;">
      ${colRight.join('')}
    </div>
  `;

  const relSection = grid.closest('.related-section');
  const relTitle = relSection ? relSection.querySelector('.related-title') : null;

  // Inicializa com o Skeleton oficial 1:1 (igual à print) abaixo do "Ver mais ⌄" e carrega os produtos ao entrar na tela
  if (relTitle) relTitle.style.display = 'none';
  grid.innerHTML = getRelatedSkeletonHtml();

  let hasRevealedRel = false;
  function revealRelatedProducts() {
    if (hasRevealedRel) return;
    hasRevealedRel = true;
    setTimeout(() => {
      if (relTitle) relTitle.style.display = '';
      grid.style.opacity = '0';
      grid.style.transition = 'opacity 0.22s ease';
      grid.innerHTML = finalMasonryHtml;
      requestAnimationFrame(() => {
        grid.style.opacity = '1';
      });
      bindRelatedVideos();
    }, 680);
  }

  if (typeof IntersectionObserver !== 'undefined' && (relSection || grid)) {
    const skelObs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          skelObs.disconnect();
          revealRelatedProducts();
        }
      });
    }, { rootMargin: '20px 0px', threshold: 0.05 });
    skelObs.observe(relSection || grid);
  } else {
    revealRelatedProducts();
  }

  function bindRelatedVideos() {
  // === DINÂMICA OFICIAL TIKTOK SHOP: TEMPO PASSANDO EM TEMPO REAL & PLAY/PAUSE INTERATIVO ===
  const videoCards = grid.querySelectorAll('.related-card');
  
  // IntersectionObserver para Autoplay automático quando o vídeo entrar na tela (Padrão TikTok)
  const videoObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const vid = entry.target.querySelector('.related-card-video');
      if (!vid) return;
      if (entry.isIntersecting) {
        vid.muted = true;
        vid.play().catch(() => {});
      } else {
        vid.pause();
      }
    });
  }, { threshold: 0.25 });

  videoCards.forEach(card => {
    const video = card.querySelector('.related-card-video');
    const badge = card.querySelector('.tt-feed-video-badge');
    const timeSpan = card.querySelector('.tt-feed-video-time');
    const iconSpan = card.querySelector('.tt-feed-video-icon');

    if (!video || !badge || !timeSpan) return;

    // Observa o card para iniciar reprodução assim que entrar na tela
    videoObserver.observe(card);

    function formatTime(sec) {
      if (!isFinite(sec) || sec < 0) return '00:00';
      const m = String(Math.floor(sec / 60)).padStart(2, '0');
      const s = String(Math.floor(sec % 60)).padStart(2, '0');
      return `${m}:${s}`;
    }

    function updateBadgeState() {
      if (video.paused) {
        // Ícone de Play ▶ quando pausado
        if (iconSpan) {
          iconSpan.innerHTML = `<svg width="7.5" height="9" viewBox="0 0 24 24" fill="#ffffff" style="display:block;"><polygon points="5 3 19 12 5 21 5 3"/></svg>`;
        }
      } else {
        // Ícone de Pause ❚❚ quando tocando
        if (iconSpan) {
          iconSpan.innerHTML = `<span style="display:inline-flex; align-items:center; gap:1.8px; height:9px;"><span style="width:2px; height:8.5px; background:#ffffff; border-radius:0.5px;"></span><span style="width:2px; height:8.5px; background:#ffffff; border-radius:0.5px;"></span></span>`;
        }
      }
    }

    // O tempo passa rigorosamente conforme o vídeo avança em tempo real
    video.addEventListener('timeupdate', () => {
      timeSpan.textContent = formatTime(video.currentTime);
      updateBadgeState();
    });

    video.addEventListener('play', () => {
      updateBadgeState();
    });

    video.addEventListener('pause', () => {
      updateBadgeState();
    });

    // Permite pausar/despausar ao clicar no badge do vídeo sem redirecionar
    badge.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (video.paused) {
        video.play().catch(() => {});
      } else {
        video.pause();
      }
      updateBadgeState();
    });
  });
  }
}

// ===== ABAS DE NAVEGAÇÃO DO PRODUTO =====
function initProductTabs() {
  const tabsBar = document.querySelector('.product-tabs');
  const tabs = document.querySelectorAll('.product-tab');
  if (!tabsBar || !tabs.length) return;

  const HEADER = 48;   // altura real do header fixo
  const TABS = 42;     // altura das abas
  const SHOW_AT = 60;  // aparece somente após rolar além do topo (tela inicial limpa 1:1)

  // Configuração inicial forçada para garantir visibilidade absoluta
  tabsBar.style.position = 'fixed';
  tabsBar.style.left = '50%';
  tabsBar.style.transform = 'translateX(-50%)';
  tabsBar.style.width = '100%';
  tabsBar.style.maxWidth = '480px'; // alinhado com max-width do app
  tabsBar.style.zIndex = '998';

  // Ordem visual correta dos elementos no HTML:
  // Visão Geral -> Avaliações -> Descrição -> Recomendações
  const sections = {
    'visao-geral': document.querySelector('.image-slider, .price-section'),
    'avaliacoes': document.querySelector('.reviews-section'),
    'descricao': document.querySelector('.about-product-section, .description-section'),
    'recomendacoes': document.querySelector('.related-section'),
  };

  const scrollContainer = document.querySelector('.page-content');

  function getScrollTopReal() {
    const winSy = window.scrollY || window.pageYOffset || document.documentElement.scrollTop || 0;
    const innerSy = scrollContainer ? (scrollContainer.scrollTop || 0) : 0;
    return Math.max(winSy, innerSy);
  }

  function updateActiveTab() {
    const sy = getScrollTopReal();

    if (sy > SHOW_AT) {
      tabsBar.classList.add('tabs-visible');
    } else {
      tabsBar.classList.remove('tabs-visible');
    }

    const threshold = HEADER + TABS + 88;
    let active = 'visao-geral';
    const domOrder = ['avaliacoes', 'descricao', 'recomendacoes'];
    for (const key of domOrder) {
      const el = sections[key];
      if (el) {
        const rect = el.getBoundingClientRect();
        if (rect.top <= threshold) {
          active = key;
        }
      }
    }
    document.querySelectorAll('.product-tab').forEach(t => {
      const isAct = t.dataset.tab === active;
      const wasAct = t.classList.contains('active');
      t.classList.toggle('active', isAct);
      if (isAct && !wasAct && tabsBar.scrollWidth > tabsBar.clientWidth) {
        const targetLeft = t.offsetLeft - (tabsBar.clientWidth - t.offsetWidth) / 2;
        tabsBar.scrollTo({ left: Math.max(0, targetLeft), behavior: 'smooth' });
      }
    });
  }

  function handleTabClick(tab) {
    const key = tab.dataset.tab;
    const el = sections[key];
    const useInner = scrollContainer && (scrollContainer.scrollHeight > scrollContainer.clientHeight + 20) && (window.getComputedStyle(scrollContainer).overflowY !== 'visible');
    if (!el || key === 'visao-geral') {
      if (useInner) scrollContainer.scrollTo({ top: 24, behavior: 'smooth' });
      else window.scrollTo({ top: 24, behavior: 'smooth' });
      return;
    }
    if (useInner) {
      const rect = el.getBoundingClientRect();
      const cRect = scrollContainer.getBoundingClientRect();
      const target = scrollContainer.scrollTop + (rect.top - cRect.top) - (TABS + 4);
      scrollContainer.scrollTo({ top: Math.max(0, target), behavior: 'smooth' });
    } else {
      const rect = el.getBoundingClientRect();
      const target = (window.scrollY || window.pageYOffset || 0) + rect.top - (HEADER + TABS + 4);
      window.scrollTo({ top: Math.max(0, target), behavior: 'smooth' });
    }
  }

  // Configura os botões limpos
  tabs.forEach(tab => {
    tab.replaceWith(tab.cloneNode(true));
  });

  const cleanTabs = document.querySelectorAll('.product-tab');
  cleanTabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      handleTabClick(tab);
    });
  });

  if (scrollContainer) {
    scrollContainer.addEventListener('scroll', updateActiveTab, { passive: true });
  }
  window.addEventListener('scroll', updateActiveTab, { passive: true });
  document.addEventListener('scroll', updateActiveTab, { passive: true });

  // Executa uma vez
  setTimeout(updateActiveTab, 80);
}

// Normalização global: Garante que todo produto com objeto variacoes vazio ou ausente 
// receba dinamicamente a variação padrão de 1 opção com sua respectiva imagem.
function normalizarVariacoesProduto(p) {
  if (!p) return;

  // Blindagem bidirecional de chaves PT/EN para resiliência absoluta
  if (p.preco === undefined && p.price !== undefined) p.preco = p.price;
  if (p.price === undefined && p.preco !== undefined) p.price = p.preco;
  if (p.precoOrig === undefined && p.originalPrice !== undefined) p.precoOrig = p.originalPrice;
  if (p.originalPrice === undefined && p.precoOrig !== undefined) p.originalPrice = p.precoOrig;
  if (p.preco_antigo === undefined && (p.precoOrig || p.originalPrice)) p.preco_antigo = p.precoOrig || p.originalPrice;
  if (!p.img && p.image) p.img = p.image;
  if (!p.image && p.img) p.image = p.img;
  if (!p.nome && p.name) p.nome = p.name;
  if (!p.name && p.nome) p.name = p.nome;
  if (!p.imagens && p.image) p.imagens = [p.image];
  if (!p.imagens && p.img) p.imagens = [p.img];

  // Se não encontrou imagem no objeto, busca a primeira do DOM (.slider-img)
  if (!p.img && typeof document !== 'undefined') {
    const domImg = document.querySelector('.slider-track .slider-img, .slider-track img, .product-slider img');
    if (domImg && domImg.src) {
      p.img = domImg.src;
      p.image = domImg.src;
      if (!p.imagens) p.imagens = [domImg.src];
    }
  }

  // Se o preço ainda for indefinido ou zero, tenta resgatar do DOM (.price-current) ou catálogo
  if ((!p.preco || p.preco === 0 || isNaN(p.preco)) && typeof document !== 'undefined') {
    const priceEl = document.querySelector('.price-current');
    if (priceEl) {
      const parsed = parseFloat(priceEl.textContent.replace(/[^\d,.]/g, '').replace(',', '.'));
      if (!isNaN(parsed) && parsed > 0) {
        p.preco = parsed;
        p.price = parsed;
      }
    }
  }

  // Se o preço original for indefinido ou zero, resgata do DOM (.price-original)
  if ((!p.precoOrig && !p.preco_antigo && !p.originalPrice) && typeof document !== 'undefined') {
    const origEl = document.querySelector('.price-original');
    if (origEl) {
      const parsedOrig = parseFloat(origEl.textContent.replace(/[^\d,.]/g, '').replace(',', '.'));
      if (!isNaN(parsedOrig) && parsedOrig > 0) {
        p.precoOrig = parsedOrig;
        p.originalPrice = parsedOrig;
        p.preco_antigo = parsedOrig;
      }
    }
  }

  // Se variacoes for um array de objetos (ex: [{ nome, preco, img }, ...]), normaliza para o objeto oficial
  if (Array.isArray(p.variacoes) && p.variacoes.length > 0) {
    p.variacoes = {
      "modelo": {
        "com_imagem": true,
        "label": "Modelo / Versão",
        "opcoes": p.variacoes.map(v => {
          if (typeof v === 'object' && v !== null) {
            return {
              nome: v.nome || 'Opção',
              imagem: v.img || v.imagem || v.image || p.img || '',
              preco: v.preco || v.price || p.preco
            };
          }
          return {
            nome: String(v),
            imagem: p.img || '',
            preco: p.preco
          };
        })
      }
    };
    return;
  }

  // Se não tem variações, tenta resgatar do objeto global window.PRODUTO_ATUAL ou do CATALOGO_PRODUTOS antes do fallback
  if (!p.variacoes || Object.keys(p.variacoes).length === 0 || (Array.isArray(p.variacoes) && p.variacoes.length === 0)) {
    if (typeof window !== 'undefined' && window.PRODUTO_ATUAL && window.PRODUTO_ATUAL.variacoes && Object.keys(window.PRODUTO_ATUAL.variacoes).length > 0) {
      p.variacoes = JSON.parse(JSON.stringify(window.PRODUTO_ATUAL.variacoes));
      return;
    }
    if (typeof CATALOGO_PRODUTOS !== 'undefined' && p.id) {
      const doCat = CATALOGO_PRODUTOS.find(item => Number(item.id) === Number(p.id));
      if (doCat && doCat.variacoes && Object.keys(doCat.variacoes).length > 0) {
        p.variacoes = JSON.parse(JSON.stringify(doCat.variacoes));
        return;
      }
    }

    let principalImg = p.img || p.image || '';
    if (principalImg && /\.(mp4|webm|ogg|mov)$/i.test(principalImg)) {
      principalImg = '';
    }
    if (!principalImg && Array.isArray(p.imagem)) {
      principalImg = p.imagem.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || p.imagem[0];
    } else if (!principalImg && typeof p.imagem === 'string' && !/\.(mp4|webm|ogg|mov)$/i.test(p.imagem)) {
      principalImg = p.imagem;
    } else if (!principalImg && Array.isArray(p.imagens)) {
      principalImg = p.imagens.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || p.imagens[0];
    }

    // Se ainda for vídeo ou vazia, busca do array imagens ou do DOM
    if (!principalImg || /\.(mp4|webm|ogg|mov)$/i.test(principalImg)) {
      if (Array.isArray(p.imagens)) {
        principalImg = p.imagens.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || '';
      }
      if (!principalImg && typeof document !== 'undefined') {
        const domImg = document.querySelector('.slider-track .slider-img, .slider-track img, .product-slider img');
        if (domImg && domImg.src) principalImg = domImg.src;
      }
    }

    p.variacoes = {
      "modelo": {
        "label": "OPÇÃO",
        "opcoes": [
          {
            "nome": "Padrão único",
            "imagem": principalImg,
            "preco": p.preco
          }
        ]
      }
    };
  }
}

if (typeof PRODUTO_ATUAL !== 'undefined') {
  normalizarVariacoesProduto(PRODUTO_ATUAL);
}

// ===== MODAL DE VARIAÇÕES (TAMANHO / COR / MODELO) =====

// Banner 11.11 Liquidação oficial TikTok Shop embutido em Data URI WebP (0ms delay / zero rede)
const BANNER_1111_MODAL_DATA_URI = "data:image/webp;base64,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";
if (typeof Image !== 'undefined' && !window._banner1111Preloaded) {
  window._banner1111Preloaded = new Image();
  window._banner1111Preloaded.src = BANNER_1111_MODAL_DATA_URI;
}

function openVariacaoModal(produto, fluxo = 'cart', onConfirm) {
  // Garante a normalização do produto antes de abrir o modal
  normalizarVariacoesProduto(produto);

  // Remove qualquer modal anterior
  const existing = document.getElementById('variacoes-modal-overlay');
  if (existing) existing.remove();

  const variacoes = produto.variacoes || {};
  const keys = Object.keys(variacoes);

  // Imagem principal (sem mp4)
  function getImg() {
    const imgs = produto.imagens || (produto.img ? [produto.img] : []);
    const limpa = imgs.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i));
    return limpa || imgs[0] || '';
  }

  // Construir HTML das opções
  function buildGrupos() {
    return keys.map(chave => {
      const grupo = variacoes[chave];
      const label = grupo.label || chave;
      const opcoes = Array.isArray(grupo.opcoes) ? grupo.opcoes : [];
      const temImagem = opcoes.some(o => typeof o === 'object' && o.imagem);

      if (temImagem) {
        // Botões com imagem real (cor/modelo) - estilo oficial TikTok Shop (Print 3 - Item 5)
        const btns = opcoes.map((o, i) => {
          const nome = typeof o === 'object' ? o.nome : o;
          const img = typeof o === 'object' ? o.imagem : '';
          const precoOpt = (typeof o === 'object' && o.preco !== undefined) ? o.preco : '';
          const precoOrigOpt = (typeof o === 'object' && (o.preco_antigo || o.precoOrig)) ? (o.preco_antigo || o.precoOrig) : '';
          const fallback = getImg();
          return `
            <button class="var-color-btn" data-chave="${chave}" data-val="${nome}" data-img="${img}" data-preco="${precoOpt}" data-preco-orig="${precoOrigOpt}" onclick="varModalSelect(this)">
               <div class="var-color-img-wrap">
                 ${img ? `<img src="${img}" alt="${nome}" onerror="this.src='${fallback}'">` : '<div class="var-color-placeholder"></div>'}
                 <div class="var-zoom-badge">
                   <svg viewBox="0 0 24 24" width="10" height="10" fill="none" stroke="#fff" stroke-width="2.5"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
                 </div>
               </div>
               <span class="var-color-name">${nome}</span>
            </button>
          `;
        }).join('');
        return `
          <div class="var-group">
            <span class="var-label">${label} (${opcoes.length})</span>
            <div class="var-color-grid">${btns}</div>
          </div>
        `;
      } else {
        // Botões normais (tamanho/voltagem) com link do Guia de tamanhos (Print 3 - Item 6)
        const isSize = chave.toLowerCase().includes('tam') || label.toLowerCase().includes('tam');
        const btns = opcoes.map((o, i) => {
          const nome = typeof o === 'object' ? o.nome : o;
          const precoOpt = (typeof o === 'object' && o.preco !== undefined) ? o.preco : '';
          const precoOrigOpt = (typeof o === 'object' && (o.preco_antigo || o.precoOrig)) ? (o.preco_antigo || o.precoOrig) : '';
          return `
            <button class="var-size-btn" data-chave="${chave}" data-val="${nome}" data-preco="${precoOpt}" data-preco-orig="${precoOrigOpt}" onclick="varModalSelect(this)">
               ${nome}
            </button>
          `;
        }).join('');
        return `
          <div class="var-group">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
              <span class="var-label">${label}</span>
              ${isSize ? `<span class="var-size-guide-link" onclick="openSizeGuideModal()" style="font-size:12.5px; color:#4364db; font-weight:500; cursor:pointer;">Guia de tamanhos</span>` : ''}
            </div>
            <div class="var-size-options">${btns}</div>
          </div>
        `;
      }
    }).join('');
  }

  // Formata o preço da variação se houver alteração com blindagem absoluta anti-zero
  if ((!produto.preco || produto.preco <= 0 || isNaN(produto.preco)) && typeof document !== 'undefined') {
    const curEl = document.querySelector('.price-current');
    if (curEl) {
      const parsedDom = parseFloat(curEl.textContent.replace(/[^\d,.]/g, '').replace(',', '.'));
      if (!isNaN(parsedDom) && parsedDom > 0) {
        produto.preco = parsedDom;
        produto.price = parsedDom;
      }
    }
  }

  const formatPreco = (val) => {
    const num = parseFloat(val);
    return (!isNaN(num) && num > 0) ? num.toFixed(2).replace('.', ',') : '97,90';
  };

  const preco = formatPreco(produto.preco);
  const precoPartes = preco.split(',');
  const precoInteiro = precoPartes[0];
  const precoCentavos = precoPartes[1] || '00';

  // Extrai preço original e percentual de desconto oficiais
  const precoOrigRaw = produto.precoOrig || produto.preco_antigo || produto.precoAntigo || (document.querySelector('.price-original') ? document.querySelector('.price-original').textContent.replace('R$', '').trim() : '');
  let precoOrigFormatado = '';
  let parsedOrigNum = null;
  if (precoOrigRaw) {
    if (typeof precoOrigRaw === 'number') {
      parsedOrigNum = precoOrigRaw;
      precoOrigFormatado = precoOrigRaw.toFixed(2).replace('.', ',');
    } else {
      const cleanStr = String(precoOrigRaw).replace('R$', '').trim();
      const num = parseFloat(cleanStr.replace(/\./g, '').replace(',', '.'));
      if (!isNaN(num)) {
        parsedOrigNum = num;
        precoOrigFormatado = num.toFixed(2).replace('.', ',');
      } else {
        precoOrigFormatado = cleanStr;
      }
    }
  }

  // Extrai percentual de desconto se disponível (Padrão Oficial TikTok Shop Imagem 1)
  let descPercent = produto.desc || produto.desconto || '';
  if (!descPercent) {
    const badgeEl = document.querySelector('.discount-badge-white') || document.querySelector('.flash-discount-badge');
    if (badgeEl) descPercent = badgeEl.textContent.replace(/[^0-9]/g, '');
  }
  if (!descPercent && parsedOrigNum && produto.preco) {
    const precoNum = parseFloat(String(produto.preco).replace(/\./g, '').replace(',', '.'));
    if (parsedOrigNum > precoNum) {
      descPercent = Math.round(((parsedOrigNum - precoNum) / parsedOrigNum) * 100);
    }
  }
  if (descPercent) {
    descPercent = String(descPercent).replace(/[^0-9]/g, '');
  }

  const temOferta = document.querySelector('.flash-deal-banner') !== null || document.querySelector('.price-decalque') !== null || document.querySelector('.price-section') !== null;
  const subTextoBotao = temOferta ? `Oferta relâmpago R$ <span id="var-modal-btn-preco">${preco}</span>` : `R$ <span id="var-modal-btn-preco">${preco}</span> com cupom`;

  let footerButtonHtml = `
    <div class="var-modal-footer">
      <button class="var-btn-buy-full" onclick="varModalConfirm('${fluxo}')">
        <span style="font-size:15px; font-weight:700; line-height:1.2;">Compre</span>
        <span style="font-size:11.5px; font-weight:500; opacity:0.95; line-height:1.2;">${subTextoBotao}</span>
      </button>
    </div>
  `;

  const overlay = document.createElement('div');
  overlay.id = 'variacoes-modal-overlay';
  overlay.style.cssText = `
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.6); z-index: 10000;
    display: flex; align-items: flex-end; justify-content: center;
    animation: fadeInOverlay 0.2s ease;
  `;

  overlay.innerHTML = `
    <style>
      @keyframes fadeInOverlay { from { opacity:0 } to { opacity:1 } }
      @keyframes slideUpModal { from { transform:translateY(100%) } to { transform:translateY(0) } }
      #variacoes-modal {
        background: #fff;
        width: 100%;
        max-width: 480px;
        border-radius: 16px 16px 0 0;
        max-height: 80vh;
        overflow-y: auto;
        animation: slideUpModal 0.3s cubic-bezier(.4,0,.2,1);
        position: relative;
        padding-bottom: env(safe-area-inset-bottom, 0px);
      }
      #variacoes-modal::-webkit-scrollbar { display: none; }
      .var-modal-header {
        display: flex;
        gap: 12px;
        padding: 16px 16px 8px;
        border-bottom: none;
        align-items: center;
      }
      .var-modal-img {
        width: 72px;
        height: 72px;
        object-fit: cover;
        border-radius: 8px;
        background: #f5f5f5;
        flex-shrink: 0;
      }
      .var-modal-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
      }
      .var-modal-preco-row {
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 2px;
      }
      .var-modal-desc-badge {
        background: #ff2b56;
        color: #ffffff;
        font-size: 13px;
        font-weight: 700;
        padding: 1.5px 5.5px;
        border-radius: 4px;
        line-height: 1.2;
        display: inline-block;
      }
      .var-modal-preco {
        display: inline-flex;
        align-items: baseline;
        color: #ff2b56;
        font-weight: 700;
        line-height: 1;
      }
      .var-modal-currency {
        font-size: 14px;
        font-weight: 700;
        margin-right: 2px;
      }
      .var-modal-int {
        font-size: 22px;
        font-weight: 700;
      }
      .var-modal-cents {
        font-size: 15px;
        font-weight: 700;
      }
      .var-modal-preco-orig {
        font-size: 13px;
        color: #8a8b91;
        text-decoration: line-through;
        margin: 0;
        line-height: 1.2;
      }
      .var-modal-nome {
        display: none !important;
      }
      .var-close-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        background: #f5f5f5;
        border: none;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        font-size: 16px;
        color: #666;
        flex-shrink: 0;
        z-index: 10;
      }
      .var-modal-body {
        padding: 12px 16px 16px;
        display: flex;
        flex-direction: column;
        gap: 14px;
      }
      .var-group { display: flex; flex-direction: column; gap: 8px; }
      .var-label {
        font-size: 13px;
        color: #333;
        font-weight: 600;
      }
      .var-color-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
      }
      .var-color-btn {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 0;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        overflow: hidden;
        transition: all 0.2s ease;
      }
      .var-color-btn.selected {
        border: 1.5px solid #fe2c55 !important;
        box-shadow: 0 0 0 1px #fe2c55;
      }
      .var-color-img-wrap {
        width: 100%;
        aspect-ratio: 1/1;
        position: relative;
        overflow: hidden;
        background: #f7f7f7;
      }
      .var-color-img-wrap img, .var-color-placeholder {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }
      .var-zoom-badge {
        position: absolute;
        top: 3px;
        left: 3px;
        width: 16px;
        height: 16px;
        background: rgba(0, 0, 0, 0.4);
        border-radius: 3px;
        display: flex;
        align-items: center;
        justify-content: center;
        pointer-events: none;
      }
      .var-color-btn span.var-color-name {
        font-size: 11px;
        color: #161823;
        text-align: center;
        padding: 5px 2px;
        line-height: 1.2;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 100%;
        display: block;
      }
      .var-color-btn.selected span.var-color-name {
        color: #fe2c55;
        font-weight: 600;
      }
      .var-size-options { display: flex; flex-wrap: wrap; gap: 6px; }
      .var-size-btn {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 13px;
        font-weight: 500;
        color: #333;
        cursor: pointer;
        transition: all 0.2s;
        min-width: 44px;
        text-align: center;
        font-family: inherit;
      }
      .var-size-btn.selected {
        border-color: #FF2B56;
        color: #FF2B56;
        background: #fff5f7;
      }
      .var-qty-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 2px;
      }
      .var-qty-label { font-size: 13px; font-weight: 500; color: #333; }
      .var-qty-controls {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #f5f5f5;
        border-radius: 6px;
        padding: 2px 6px;
      }
      .var-qty-btn {
        background: none;
        border: none;
        font-size: 16px;
        cursor: pointer;
        color: #333;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .var-qty-value { font-size: 14px; font-weight: 600; min-width: 16px; text-align: center; }
      .var-modal-footer {
        padding: 10px 16px;
        display: flex;
        gap: 8px;
        border-top: 1px solid #f2f2f2;
        position: sticky;
        bottom: 0;
        background: #fff;
        z-index: 100;
      }
      .var-btn-cart-full, .var-btn-buy-full {
        flex: 1;
        background: #FF2B56;
        color: #fff;
        border: none;
        border-radius: 22px;
        padding: 10px;
        font-size: 14.5px;
        font-weight: 700;
        cursor: pointer;
        transition: opacity 0.2s;
        font-family: inherit;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 40px;
        box-sizing: border-box;
      }
      .var-btn-cart-full:hover, .var-btn-buy-full:hover { opacity: 0.9; }
      .var-error-msg {
        display: none !important;
      }
    </style>

    <div id="variacoes-modal">
      <div class="var-modal-header">
        <img class="var-modal-img" src="${getImg() || (produto.img || '')}" alt="${produto.nome}" onerror="this.onerror=null; const _domImg = (document.querySelector('.slider-track .slider-img') || document.querySelector('.slider-img') || document.querySelector('.product-slider img')); this.src = (_domImg && _domImg.src) ? _domImg.src : '../img/livro-interativo-slide-1.webp';">
        <div class="var-modal-info">
          <div class="var-modal-preco-row">
            ${descPercent ? `<span class="var-modal-desc-badge">-${descPercent}%</span>` : ''}
            <div class="var-modal-preco" id="var-modal-preco-val">
              <span class="var-modal-currency">R$</span>
              <span class="var-modal-int">${precoInteiro}</span><span class="var-modal-cents">,${precoCentavos}</span>
            </div>
          </div>
          ${precoOrigFormatado ? `<div class="var-modal-preco-orig" id="var-modal-preco-orig-val">R$ ${precoOrigFormatado}</div>` : `<div class="var-modal-preco-orig" id="var-modal-preco-orig-val" style="display:none;"></div>`}
          <div class="var-modal-frete-badge" style="display:inline-flex; align-items:center; gap:4.5px; margin-top:6px; padding:2.5px 6.5px; border:1px solid #d7ebe8; border-radius:4px; background:#ffffff; color:#007f73; font-family:'BFOnlyNumbers','Plus Jakarta Sans',sans-serif; font-size:12px; font-weight:600; line-height:1.2; width:fit-content; letter-spacing:0px;">
            <svg viewBox="0 0 22 16" width="14" height="11" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0; display:block;">
              <path d="M2.2 2.2C2.2 1.54 2.74 1 3.4 1H13.4C14.06 1 14.6 1.54 14.6 2.2V12.2H2.2V9.8H4.6C5.04 9.8 5.4 9.44 5.4 9C5.4 8.56 5.04 8.2 4.6 8.2H2.2V6.6H5.6C6.04 6.6 6.4 6.24 6.4 5.8C6.4 5.36 6.04 5 5.6 5H2.2V2.2Z" fill="#007f73"/>
              <path d="M14.6 4.4H17.85C18.55 4.4 19.18 4.82 19.45 5.47L20.75 8.55C20.91 8.93 21 9.34 21 9.75V12.2H14.6V4.4Z" fill="#007f73"/>
              <path d="M16.1 6H17.95L19.05 8.55H16.1V6Z" fill="#ffffff"/>
              <circle cx="6.8" cy="12.6" r="2.5" fill="#007f73" stroke="#ffffff" stroke-width="1.15"/>
              <circle cx="6.8" cy="12.6" r="0.85" fill="#ffffff"/>
              <circle cx="17.1" cy="12.6" r="2.5" fill="#007f73" stroke="#ffffff" stroke-width="1.15"/>
              <circle cx="17.1" cy="12.6" r="0.85" fill="#ffffff"/>
            </svg>
            <span>Frete grátis</span>
          </div>
          <div class="var-modal-preco-unit" style="display:none;" id="var-modal-preco-unit-val">${produto.preco}</div>
        </div>
        <button class="var-close-btn" onclick="closeVariacaoModal()">✕</button>
      </div>

      <!-- BANNER OFICIAL TIKTOK SHOP - BLACK FRIDAY -->
      <div class="var-modal-banner-bf" style="padding: 6px 16px 12px 16px; width: 100%; box-sizing: border-box;">
        <img src="/decalque/banner-modal-bf-v2.png?v=20261126" alt="Black Friday - 12 de nov – 3 de dez" style="width: 100%; aspect-ratio: 415 / 42; height: auto; display: block; border-radius: 10px; object-fit: cover;">
      </div>

      <div class="var-modal-body">
        ${buildGrupos()}
        <div class="var-qty-row">
          <span class="var-qty-label">Quantidade</span>
          <div class="var-qty-controls">
            <button class="var-qty-btn" onclick="varModalQty(-1)">−</button>
            <span class="var-qty-value" id="var-qty-val">1</span>
            <button class="var-qty-btn" onclick="varModalQty(+1)">+</button>
          </div>
        </div>
      </div>



      ${footerButtonHtml}
    </div>
  `;

  // Quantidade interna
  let modalQty = 1;
  const selecionadosRef = {};
  let currentImg = getImg();
  let currentPreco = typeof produto.preco === 'number' ? produto.preco : (parseFloat(String(produto.preco).replace(',', '.')) || 0);
  let currentPrecoOrig = parsedOrigNum;

  function updateModalPriceAndUI() {
    const totalPreco = currentPreco * modalQty;
    const totalOrig = currentPrecoOrig ? (currentPrecoOrig * modalQty) : null;
    const precoFinalStr = totalPreco.toFixed(2).replace('.', ',');
    const parts = precoFinalStr.split(',');

    const precoEl = overlay.querySelector('#var-modal-preco-val');
    if (precoEl) {
      precoEl.innerHTML = `<span class="var-modal-currency">R$</span><span class="var-modal-int">${parts[0]}</span><span class="var-modal-cents">,${parts[1]}</span>`;
    }

    const precoOrigEl = overlay.querySelector('#var-modal-preco-orig-val');
    if (precoOrigEl) {
      if (totalOrig && totalOrig > totalPreco) {
        precoOrigEl.textContent = `R$ ${totalOrig.toFixed(2).replace('.', ',')}`;
        precoOrigEl.style.display = 'block';
      } else {
        precoOrigEl.style.display = 'none';
      }
    }

    // Atualiza percentual de desconto no modal
    if (totalOrig && totalOrig > totalPreco) {
      const newDesc = Math.round(((totalOrig - totalPreco) / totalOrig) * 100);
      const badgeEl = overlay.querySelector('.var-modal-desc-badge');
      if (badgeEl) {
        badgeEl.textContent = `-${newDesc}%`;
        badgeEl.style.display = 'inline-block';
      }
    }

    // Atualiza o botão inferior do modal
    const btnPrecoEl = overlay.querySelector('#var-modal-btn-preco');
    if (btnPrecoEl) {
      btnPrecoEl.textContent = precoFinalStr;
    }
  }

  window._varModalQty = function (delta) {
    modalQty = Math.max(1, modalQty + delta);
    const el = overlay.querySelector('#var-qty-val');
    if (el) el.textContent = modalQty;
    updateModalPriceAndUI();
  };

  window._varModalSelect = function (btn) {
    const chave = btn.dataset.chave;
    const val = btn.dataset.val;
    overlay.querySelectorAll(`[data-chave="${chave}"]`).forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    selecionadosRef[chave] = val;

    // 1. Atualiza na hora o thumbnail no topo do modal se a opção tiver imagem
    if (btn.dataset.img) {
      currentImg = btn.dataset.img;
      const modalImgEl = overlay.querySelector('.var-modal-img');
      if (modalImgEl) {
        modalImgEl.src = currentImg;
      }
    }

    // 2. Atualiza o preço da opção se tiver preço específico
    if (btn.dataset.preco) {
      const pNum = parseFloat(btn.dataset.preco);
      if (!isNaN(pNum) && pNum > 0) {
        currentPreco = pNum;
      }
    }
    if (btn.dataset.precoOrig) {
      const oNum = parseFloat(String(btn.dataset.precoOrig).replace(',', '.'));
      if (!isNaN(oNum) && oNum > 0) {
        currentPrecoOrig = oNum;
      }
    }

    updateModalPriceAndUI();
  };

  window._varModalConfirm = function (tipoConfirm) {
    // Valida se selecionou todas as chaves
    const faltando = keys.filter(k => !selecionadosRef[k]);
    if (faltando.length > 0) {
      // Pega a primeira chave que falta (na ordem de exibição top-down do modal)
      const primeiraChave = faltando[0];
      const varObj = variacoes[primeiraChave];
      let label = (varObj && varObj.label) ? varObj.label : primeiraChave;
      label = String(label).replace(/\s*\(\d+\)/g, '').trim();
      const low = label.toLowerCase();
      let nomeFormatado = 'Opção';
      if (low.includes('tam')) {
        nomeFormatado = 'Tamanho';
      } else if (low.includes('cor') || low.includes('color')) {
        nomeFormatado = 'Cor';
      } else if (low.includes('mod') || low.includes('vers')) {
        nomeFormatado = 'Modelo';
      } else if (low.includes('volt')) {
        nomeFormatado = 'Voltagem';
      } else if (label.length > 0) {
        nomeFormatado = label.charAt(0).toUpperCase() + label.slice(1);
      }

      if (typeof window.showTikTokToast === 'function') {
        window.showTikTokToast(`Selecionar ${nomeFormatado}`);
      } else if (typeof showTikTokToast === 'function') {
        showTikTokToast(`Selecionar ${nomeFormatado}`);
      }
      return;
    }

    closeVariacaoModal();
    if (typeof onConfirm === 'function') {
      onConfirm({
        selecionados: selecionadosRef,
        qty: modalQty,
        tipo: tipoConfirm,
        imagem: currentImg,
        preco: currentPreco,
        precoOrig: currentPrecoOrig
      });
    } else if (tipoConfirm === 'buy') {
      const varLabel = Object.values(selecionadosRef).join(', ');
      const pObj = {
        ...produto,
        preco: currentPreco,
        precoOrig: currentPrecoOrig,
        img: currentImg
      };
      if (typeof irDiretoAoCheckoutComProduto === 'function') {
        irDiretoAoCheckoutComProduto(pObj, varLabel, modalQty);
      }
    }
  };

  window._varModalClose = function () {
    overlay.remove();
  };

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeVariacaoModal();
  });

  document.body.appendChild(overlay);

  // Auto-seleciona a primeira opção de cada grupo (padrão oficial TikTok Shop)
  try {
    keys.forEach(k => {
      const firstBtn = overlay.querySelector(`[data-chave="${k}"]`);
      if (firstBtn && typeof window._varModalSelect === 'function') {
        window._varModalSelect(firstBtn);
      }
    });
  } catch (e) {}
}

// Aliases globais chamados pelo HTML inline
window.varModalQty = function (delta) { if (window._varModalQty) window._varModalQty(delta); };
window.varModalSelect = function (btn) { if (window._varModalSelect) window._varModalSelect(btn); };
window.varModalConfirm = function (tipo) { if (window._varModalConfirm) window._varModalConfirm(tipo); };
window.closeVariacaoModal = function () { if (window._varModalClose) window._varModalClose(); };

// =====================================================================
// ITENS OFICIAIS TIKTOK SHOP (3, 5, 6, 8, 9, 11, 12, 14 - BRUNO CTO)
// =====================================================================

// Item 6: Modal do Guia de Tamanhos
function openSizeGuideModal() {
  const existing = document.getElementById('size-guide-modal-overlay');
  if (existing) existing.remove();

  // Single Source of Truth: busca primeiro na descrição, depois no slider ou na função mestre
  const descGuideImg = document.querySelector('.size-guide-img, .description-text img[src*="guia-tamanhos"], .about-product-section img[src*="guia-tamanhos"], .product-desc img[src*="guia-tamanhos"]');
  const sliderGuideImg = document.querySelector('#slider-size-guide img');
  const officialImgSrc = descGuideImg ? (descGuideImg.getAttribute('src') || descGuideImg.src) : (sliderGuideImg ? (sliderGuideImg.getAttribute('src') || sliderGuideImg.src) : (typeof getProductSizeGuideImage === 'function' ? getProductSizeGuideImage() : ''));

  if (!officialImgSrc) return;

  const tableContent = `<div style="text-align:center; padding:6px 0;"><img src="${officialImgSrc}" alt="Guia de tamanhos oficial" style="max-width:100%; height:auto; border-radius:8px; display:block; margin:0 auto;"></div>`;

  const modal = document.createElement('div');
  modal.id = 'size-guide-modal-overlay';
  modal.style.cssText = 'position:fixed; top:0; left:0; right:0; bottom:0; background:rgba(0,0,0,0.6); z-index:100000; display:flex; align-items:flex-end; justify-content:center; animation:fadeInOverlay 0.2s ease;';
  modal.innerHTML = `
    <div style="background:#fff; width:100%; max-width:480px; border-radius:16px 16px 0 0; padding:18px 16px 24px; max-height:80vh; overflow-y:auto; box-sizing:border-box;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <span style="font-size:16px; font-weight:700; color:#161823;">Guia de tamanhos</span>
        <button onclick="document.getElementById('size-guide-modal-overlay').remove()" style="background:none; border:none; font-size:20px; cursor:pointer; color:#757575; padding:4px;">✕</button>
      </div>
      <div style="margin-bottom:16px;">
        <p style="font-size:12.5px; color:#666; margin:0 0 12px 0;">Use as medidas abaixo como referência para escolher o melhor tamanho:</p>
        ${tableContent}
      </div>
      <button onclick="document.getElementById('size-guide-modal-overlay').remove()" style="width:100%; background:#fe2c55; color:#fff; border:none; height:42px; border-radius:21px; font-size:14px; font-weight:700; cursor:pointer;">Entendi</button>
    </div>
  `;
  modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
  document.body.appendChild(modal);
}
window.openSizeGuideModal = openSizeGuideModal;

// Item 3: Botão Flutuante de Scroll ao Topo (↑) Oficial TikTok Shop 1:1
function initScrollToTopBtn() {
  let btn = document.getElementById('scroll-to-top-btn');
  if (!btn) {
    btn = document.createElement('button');
    btn.id = 'scroll-to-top-btn';
    btn.setAttribute('aria-label', 'Voltar ao topo');
    document.body.appendChild(btn);
  }
  btn.className = 'scroll-to-top-btn';
  btn.innerHTML = `
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#161823" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
      <line x1="5" y1="5.5" x2="19" y2="5.5"></line>
      <line x1="12" y1="19" x2="12" y2="9"></line>
      <polyline points="7 14 12 9 17 14"></polyline>
    </svg>
  `;
  btn.onclick = (e) => {
    if (e) e.preventDefault();
    const sc = document.querySelector('.page-content');
    if (sc) sc.scrollTo({ top: 0, behavior: 'smooth' });
    window.scrollTo({ top: 0, behavior: 'smooth' });
    if (document.documentElement) document.documentElement.scrollTo({ top: 0, behavior: 'smooth' });
  };
  window.scrollToTop = btn.onclick;

  function checkScroll() {
    const sc = document.querySelector('.page-content');
    const sy = (sc && sc.scrollTop) ? sc.scrollTop : (window.scrollY || (document.documentElement ? document.documentElement.scrollTop : 0));
    if (sy > 150) {
      btn.classList.add('visible');
      btn.style.opacity = '1';
      btn.style.pointerEvents = 'auto';
      btn.style.transform = 'translateY(0)';
    } else {
      btn.classList.remove('visible');
      btn.style.opacity = '0';
      btn.style.pointerEvents = 'none';
      btn.style.transform = 'translateY(10px)';
    }
  }

  window.addEventListener('scroll', checkScroll, { passive: true });
  document.addEventListener('scroll', checkScroll, { passive: true });
  const attachSc = () => {
    const sc = document.querySelector('.page-content');
    if (sc) sc.addEventListener('scroll', checkScroll, { passive: true });
  };
  attachSc();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachSc);
  }
  setTimeout(attachSc, 300);
  setTimeout(checkScroll, 100);
}

// ===== POOL OFICIAL DE AVATARES AUTÊNTICOS DO TIKTOK CDN (220 UNIDADES 100% ÚNICAS) =====
const isPagesDirApp = typeof window !== 'undefined' && window.location.pathname.includes('/pages/');
const revAvatarBase = isPagesDirApp ? '../img/reviews-avatars/tiktok_real/' : 'img/reviews-avatars/tiktok_real/';
const REAL_AVATAR_POOL = Array.from({ length: 220 }, (_, i) => `${revAvatarBase}tt_avatar_${i + 1}.jpg`);

function getAppCurrentProductId() {
  if (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.id) return parseInt(PRODUTO_ATUAL.id, 10);
  const m = (typeof window !== 'undefined' && window.location.pathname) ? window.location.pathname.match(/produto-(\d+)\.html/) : null;
  if (m) return parseInt(m[1], 10);
  return 1;
}

function getAvatarForProductReview(productId = null, reviewIndex = 0) {
  const pid = (productId !== null && !isNaN(productId)) ? parseInt(productId, 10) : getAppCurrentProductId();
  const offset = (pid * 17) % REAL_AVATAR_POOL.length;
  const targetIdx = (offset + reviewIndex) % REAL_AVATAR_POOL.length;
  return REAL_AVATAR_POOL[targetIdx];
}

// Item 11: Miniaturas Compactas à Direita nas Avaliações (+4 / +5) e Limitação Estrita a 3 Visíveis Inicialmente
function formatCompactReviews() {
  const reviewsSection = document.querySelector('.reviews-section, .customer-reviews-section');
  if (!reviewsSection) return;

  // Unifica contêineres legados de paginação
  const maisContainers = reviewsSection.querySelectorAll('[id^="mais-reviews-"]');
  maisContainers.forEach(container => {
    container.style.display = 'contents';
  });
  reviewsSection.querySelectorAll('.ver-mais-btn, [id^="ver-mais-btn-"]').forEach(btn => {
    btn.style.display = 'none';
  });

  // Cabeçalho oficial compacto no topo (★ 4,8 Avaliações dos clientes (X) ⓘ Ver mais ›)
  const cards = Array.from(reviewsSection.querySelectorAll('.review-card'));
  const realCount = cards.length;

  const header = reviewsSection.querySelector('.reviews-header');
  const summary = reviewsSection.querySelector('.reviews-summary');
  let nota = '4.9';
  let total = realCount > 0 ? String(realCount) : '0';

  if (summary) {
    const avgEl = summary.querySelector('.review-avg');
    if (avgEl && avgEl.textContent.trim()) nota = avgEl.textContent.trim();
  }

  if (header) {
    const headerMatch = header.textContent.match(/\(([^)]+)\)/);
    if (headerMatch && headerMatch[1]) {
      total = headerMatch[1];
    } else if (realCount > 0) {
      total = String(realCount);
    }
  } else {
    const existingOfficial = reviewsSection.querySelector('.reviews-header-official');
    if (existingOfficial) {
      const m = existingOfficial.textContent.match(/\(([^)]+)\)/);
      if (m && m[1]) total = m[1];
    }
  }

  const notaVirgula = String(nota || '4,8').replace('.', ',');

  if (header && !reviewsSection.querySelector('.reviews-header-official')) {
    const officialHeader = document.createElement('div');
    officialHeader.className = 'reviews-header-official';
    officialHeader.onclick = () => { if (typeof expandStoreReviews === 'function') expandStoreReviews(); };
    officialHeader.innerHTML = `
      <div class="reviews-header-left">
        ${getTTOfficialStarSvg(16, true)}
        <span class="reviews-header-score">${notaVirgula}</span>
        <span class="reviews-header-divider" aria-hidden="true"></span>
        <span class="reviews-header-title-text">Avaliações dos clientes ...</span>
      </div>
      <div class="reviews-header-ver-mais">
        <svg class="reviews-header-info-icon" width="13.5" height="13.5" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <circle cx="12" cy="12" r="9.5"></circle>
          <line x1="12" y1="11" x2="12" y2="16.2"></line>
          <circle cx="12" cy="7.6" r="1" fill="#161823" stroke="none"></circle>
        </svg>
        <span>Ver mais</span>
        <svg class="reviews-header-chevron" width="12.5" height="12.5" viewBox="0 0 24 24" fill="none" stroke="#73747b" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
    `;

    header.style.display = 'none';
    if (summary) summary.style.display = 'none';
    reviewsSection.insertBefore(officialHeader, reviewsSection.firstChild);
  } else if (reviewsSection.querySelector('.reviews-header-official')) {
    const scoreEl = reviewsSection.querySelector('.reviews-header-official .reviews-header-score');
    if (scoreEl && !scoreEl.textContent.trim()) scoreEl.textContent = notaVirgula;
    const titleTextEl = reviewsSection.querySelector('.reviews-header-official .reviews-header-title-text');
    if (titleTextEl) {
      titleTextEl.textContent = 'Avaliações dos clientes ...';
    }
  }

  // Sincroniza a contagem no bloco do topo (ao lado das estrelas de avaliação)
  if (total) {
    const topRatingCountEl = document.querySelector('.ratings-row .star-row span:last-child');
    if (topRatingCountEl && topRatingCountEl.textContent.includes('(')) {
      topRatingCountEl.textContent = `(${total})`;
      topRatingCountEl.style.color = '#4364db';
      topRatingCountEl.style.cursor = 'pointer';
      topRatingCountEl.onclick = () => { if (typeof window.abrirTelaAvaliacoesCompletas === 'function') window.abrirTelaAvaliacoesCompletas(); };
    }
  }

  // Itera sobre todos os cards
  cards.forEach((card, idx) => {
    // Evita refazer se o card já foi reconstruído
    if (card.classList.contains('review-card-formatted')) {
      if (idx < 3) {
        card.style.display = 'flex';
        card.classList.remove('review-card-hidden');
      } else {
        card.style.display = 'none';
        card.classList.add('review-card-hidden');
      }
      return;
    }
    card.classList.add('review-card-formatted');

    // Detecta estrelas
    const starsEl = card.querySelector('.review-user-stars');
    const starsTxt = starsEl ? starsEl.textContent.trim() : '';
    const is5Stars = starsTxt.includes('⭐⭐⭐⭐⭐') || starsTxt.includes('★★★★★') || starsTxt.length >= 5 || !starsTxt;
    card.setAttribute('data-is-5stars', is5Stars ? 'true' : 'false');
    card.setAttribute('data-review-index', idx);

    const photosContainer = card.querySelector('.review-photos');
    const rawAuthorName = card.getAttribute('data-author-name') || card.querySelector('.review-user-name')?.childNodes[0]?.textContent.trim() || card.querySelector('.review-user-name')?.textContent.trim() || '';
    let rawAuthorAvatar = card.getAttribute('data-author-avatar') || card.querySelector('.review-avatar img')?.src || '';
    if (!rawAuthorAvatar || rawAuthorAvatar.includes('data:image/svg') || rawAuthorAvatar.includes('_tn') || rawAuthorAvatar.includes('default-avatar')) {
      rawAuthorAvatar = getAvatarForProductReview(null, idx);
    }
    const rawAuthorComment = card.querySelector('.review-comment')?.textContent.trim() || '';
    const rawAuthorStars = card.querySelectorAll('.review-user-stars polygon, .review-user-stars svg').length || (is5Stars ? 5 : 4);

        if (rawAuthorName) card.setAttribute('data-author-name', rawAuthorName);
    if (rawAuthorAvatar) card.setAttribute('data-author-avatar', rawAuthorAvatar);
    if (rawAuthorComment) card.setAttribute('data-author-comment', rawAuthorComment);
    card.setAttribute('data-author-stars', rawAuthorStars);


    const mediaEls = photosContainer ? Array.from(photosContainer.querySelectorAll('img, video')).filter(el => {
      const s = (el.src || '').toLowerCase();
      return s && !s.includes('data:image/svg') && !s.includes('avatar') && !s.includes('review-user-') && !s.includes('/avt-');
    }) : [];

    // Coluna vertical da esquerda Oficial TikTok Shop (Imagem 2)
    const contentWrap = document.createElement('div');
    contentWrap.className = 'review-content-wrap';
    contentWrap.style.cssText = 'flex: 1; min-width: 0; display: flex; flex-direction: column;';

    // Extrai avatar existente ou atribui avatar humano autêntico
    const avatarEl = card.querySelector('.review-avatar img');
    let avatarSrc = card.getAttribute('data-author-avatar') || (avatarEl ? (avatarEl.src || '') : '');
    if (!avatarSrc || avatarSrc.includes('data:image/svg') || avatarSrc.includes('_tn') || avatarSrc.includes('default-avatar')) {
      avatarSrc = getAvatarForProductReview(null, idx);
    }

    // Extrai e normaliza a variação
    const dateEl = card.querySelector('.review-date');
    let rawDateTxt = dateEl ? dateEl.textContent.trim() : '';
    let varTxt = '';
    if (rawDateTxt.includes('·')) {
      varTxt = rawDateTxt.split('·')[1].replace(/variac(a|ã)o\s*:\s*/i, '').trim();
    } else if (rawDateTxt.includes('|')) {
      varTxt = rawDateTxt.split('|')[1].replace(/variac(a|ã)o\s*:\s*/i, '').trim();
    } else if (rawDateTxt.toLowerCase().includes('varia')) {
      varTxt = rawDateTxt.replace(/.*varia[cç][aã]o\s*:\s*/gi, '').trim();
    } else {
      const pills = Array.from(document.querySelectorAll('.var-item-pill, .var-size-btn, .option-card, .cor-btn, .tamanho-btn'));
      if (pills.length > 0) {
        varTxt = (pills[idx % pills.length].getAttribute('data-val') || pills[idx % pills.length].textContent).trim();
      }
    }
    
    // Se não encontrou variação explícita, usa variações contextuais reais
    if (!varTxt || varTxt.toLowerCase() === 'padrão') {
      const prodTitle = (document.querySelector('.product-title')?.textContent || document.title || '').toLowerCase();
      if (prodTitle.includes('cacho') || prodTitle.includes('modelador') || prodTitle.includes('escova')) {
        const hairVars = ['Cinza Espacial com Roxo', 'Rosa Bebê', 'Branco Pérola'];
        varTxt = hairVars[idx % hairVars.length];
      } else {
        varTxt = 'Padrão';
      }
    }
    const varAttrDisplay = varTxt;
    card.setAttribute('data-author-variation', varAttrDisplay);
    card.setAttribute('data-author-date', rawDateTxt.split('·')[0].split('|')[0].trim() || (idx === 0 ? '23/10' : (idx < 3 ? '1 sem.' : '2 sem.')));

    // Cabeçalho compacto 1:1 com print oficial TikTok Shop:
    // [Avatar 24x24] + [★★★★★] + [· Variação] em linha única centralizada (sem nome e sem data visíveis)
    const maskedName = (typeof formatTikTokMaskedName === 'function') ? formatTikTokMaskedName(rawAuthorName, idx) : (rawAuthorName || 'Cliente');
    const starCountNum = Math.max(1, Math.min(5, parseInt(rawAuthorStars, 10) || 5));
    let starsInlineHtml = '';
    for (let s = 1; s <= 5; s++) {
      starsInlineHtml += getTTOfficialStarSvg(12, s <= starCountNum);
    }
    const compactHeader = document.createElement('div');
    compactHeader.className = 'review-header';
    compactHeader.style.cssText = 'display: flex; align-items: center; gap: 7px; margin-bottom: 7px; width: 100%; overflow: hidden;';
    compactHeader.innerHTML = `
      <div class="review-avatar" style="width: 24px; height: 24px; min-width: 24px; border-radius: 50%; overflow: hidden; flex-shrink: 0;">
        <img src="${avatarSrc}" alt="${maskedName}" style="width: 100%; height: 100%; object-fit: cover; display: block;">
      </div>
      <div style="display: flex; align-items: center; gap: 5px; flex: 1; min-width: 0; overflow: hidden; white-space: nowrap;">
        <span style="display: inline-flex; align-items: center; gap: 2px; flex-shrink: 0;">${starsInlineHtml}</span>
        <span style="color: #8a8b91; font-size: 12.5px; line-height: 1; flex-shrink: 0;">·</span>
        <span style="font-size: 12.5px; color: #73747b; font-weight: 400; line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${varAttrDisplay}</span>
      </div>
    `;
    contentWrap.appendChild(compactHeader);

    const comment = card.querySelector('.review-comment');
    if (comment) {
      comment.style.cssText = 'font-size: 13.5px; line-height: 1.4; color: #161823; margin: 0; word-break: break-word; width: 100%; font-weight: 400; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;';
      contentWrap.appendChild(comment);
    }

    card.innerHTML = '';
    card.style.cssText = 'display: flex; justify-content: space-between; align-items: flex-start; padding: 10px 0; border-bottom: none; width: 100%; box-sizing: border-box; cursor: pointer;';
    card.addEventListener('click', function(e) {
      if (e.target.closest('.review-compact-thumb-wrap, .review-photo, video')) return;
      if (typeof window.abrirTelaAvaliacoesCompletas === 'function') {
        window.abrirTelaAvaliacoesCompletas();
      }
    });
    card.appendChild(contentWrap);

    // Se tiver mídia real válida, monta o thumbWrap 70x70 à direita
    if (mediaEls.length > 0) {
      card.setAttribute('data-has-media', 'true');
      contentWrap.style.marginRight = '10px';

      // Coleta todas as mídias da avaliação sem repetições (bloqueia avatares)
      const mediaList = [];
      const seenSrcs = new Set();
      mediaEls.forEach(el => {
        const s = el.src || '';
        const sLower = s.toLowerCase();
        if (s && !seenSrcs.has(s) && !sLower.includes('avatar') && !sLower.includes('review-user-') && !sLower.includes('/avt-')) {
          seenSrcs.add(s);
          const isVid = el.tagName === 'VIDEO' || (/\.(mp4|webm|mov|m4v)($|\?)/i.test(s) || s.includes('/mms/') || s.includes('/vod/'));
          mediaList.push({ src: s, isVideo: isVid });
        }
      });

      if (mediaList.length === 0) return;

      const totalFotos = mediaList.length;
      const bestThumbItem = mediaList.find(m => !m.isVideo) || mediaList[0] || { src: '', isVideo: false };
      const isVideo = bestThumbItem.isVideo;

      const thumbWrap = document.createElement('div');
      thumbWrap.className = 'review-compact-thumb-wrap';
      thumbWrap.style.cssText = `
        width: 84px;
        height: 84px;
        min-width: 84px;
        border-radius: 8px;
        overflow: hidden;
        position: relative;
        flex-shrink: 0;
        cursor: pointer;
        background: #f5f5f5;
      `;

      // Play badge oficial idêntico ao TikTok Shop (Imagem 2)
      const playBadge = `
        <div class="review-thumb-play" style="position:absolute; top:5px; left:5px; width:20px; height:20px; background:rgba(0,0,0,0.45); border-radius:50%; display:flex; align-items:center; justify-content:center; pointer-events:none; z-index:2;">
          <svg viewBox="0 0 24 24" width="9" height="9" fill="#fff" style="margin-left:1px;"><polygon points="6 4 20 12 6 20"></polygon></svg>
        </div>`;

      const mediaHtml = isVideo ? `
        <video src="${bestThumbItem.src}" muted playsinline loop autoplay style="width:100%; height:100%; object-fit:cover; display:block; pointer-events:none;"></video>
      ` : `
        <img src="${bestThumbItem.src}" alt="Mídia do cliente" style="width:100%; height:100%; object-fit:cover; display:block;" onerror="var w=this.closest('.review-compact-thumb-wrap');if(w){w.style.display='none';}">
      `;

      // Badge de quantidade (+3, +2) com estilo e opacidade idênticos à print oficial
      thumbWrap.innerHTML = `
        ${mediaHtml}
        ${isVideo ? playBadge : ''}
        ${totalFotos > 1 ? `<div class="review-thumb-count" style="position:absolute; bottom:5px; right:5px; background:rgba(0,0,0,0.62); color:#fff; font-size:11px; font-weight:600; padding:1.5px 5.5px; border-radius:4px; line-height:1.2; pointer-events:none; z-index:2;">+${totalFotos}</div>` : ''}
      `;

      thumbWrap.onclick = (e) => {
        if (e && typeof e.stopPropagation === 'function') e.stopPropagation();
        if (typeof openPhotoModal === 'function') {
          const authorAvatar = card.getAttribute('data-author-avatar') || (card.querySelector('.review-avatar img')?.src) || '../img/reviews-avatars/default-avatar.svg';
          const rawName = card.getAttribute('data-author-name') || card.querySelector('.review-user-name')?.textContent.trim() || '';
          const authorName = (typeof formatReviewMaskedName === 'function' && rawName) ? formatReviewMaskedName(rawName) : (typeof BRAZILIAN_MASKED_NAMES !== 'undefined' ? BRAZILIAN_MASKED_NAMES[idx % BRAZILIAN_MASKED_NAMES.length] : 'C**a D**e');
          const authorStars = parseInt(card.getAttribute('data-author-stars')) || 5;
          const authorComment = card.getAttribute('data-author-comment') || card.querySelector('.review-comment')?.textContent.trim() || '';
          openPhotoModal(mediaList, 0, {
            avatar: authorAvatar,
            name: authorName,
            stars: authorStars,
            comment: authorComment
          });
        }
      };

      if (photosContainer) photosContainer.style.display = 'none';

      card.appendChild(thumbWrap);
      if (photosContainer) card.appendChild(photosContainer);
    } else {
      card.setAttribute('data-has-media', 'false');
      contentWrap.style.marginRight = '0';
    }

    // Regra Global Inegociável: Mostra estritamente as primeiras 3 avaliações inicialmente
    if (idx < 3) {
      card.classList.remove('review-card-hidden');
      card.classList.add('review-card-visible');
      card.style.setProperty('display', 'flex', 'important');
    } else {
      card.classList.remove('review-card-visible');
      card.classList.add('review-card-hidden');
      card.style.setProperty('display', 'none', 'important');
    }
  });

  // Remove qualquer botão antigo se existir
  const oldBtnWrap = reviewsSection.querySelector('.btn-ver-todas-reviews-wrap, .btn-ver-todas-reviews');
  if (oldBtnWrap) oldBtnWrap.remove();
}

// Item 12: Filtros de Avaliação da Loja (Estático, Retangular tipo quadrado border-radius: 4px, Oficial TikTok Shop)
function renderStoreReviewsFilter() {
  const reviewsSection = document.querySelector('.reviews-section, .customer-reviews-section');
  if (!reviewsSection) return;

  const existingBlock = document.querySelector('.store-reviews-summary-block');
  if (existingBlock) existingBlock.remove();

  // Dados oficiais TikTok Shop de reputação da loja (Stone Shop: 112240 vendidos)
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
}

// ==========================================================================
// TELA OFICIAL DE AVALIAÇÕES COMPLETAS TIKTOK SHOP (100% IDÊNTICA À IMAGEM 1)
// ==========================================================================

let _ttFullReviewsActiveFilter = 'all';

function getTTOfficialStarSvg(size, isFilled) {
  const sz = size || 13;
  const color = (isFilled !== false) ? '#ffb800' : '#e5e5e5';
  return `<svg width="${sz}" height="${sz}" viewBox="0 0 24 24" fill="${color}" stroke="${color}" stroke-width="0.8" stroke-linejoin="round" stroke-linecap="round" style="display:inline-block; vertical-align:middle; flex-shrink:0;"><path d="M12 1.5c.38 0 .72.23.86.58l2.76 6.64 7.08.62c.39.04.72.31.84.68.12.38.01.79-.28 1.05l-5.36 4.74 1.59 6.96c.09.39-.07.79-.39 1.02-.32.23-.75.25-1.09.06L12 20.18l-6.01 3.67c-.34.19-.77.17-1.09-.06-.32-.23-.48-.63-.39-1.02l1.59-6.96-5.36-4.74c-.29-.26-.4-.67-.28-1.05.12-.37.45-.64.84-.68l7.08-.62 2.76-6.64c.14-.35.48-.58.86-.58z"/></svg>`;
}

let _ttFullReviewsSort = 'recent';
let _ttFullReviewsData = null;

const BRAZILIAN_MASKED_NAMES = [
  'D**o M**s', 'M**a S**a', 'R**o S**a', 'V**a L**a', 'C**a P**o',
  'J**e F**s', 'A**a N**a', 'T**o A**o', 'L**a M**s', 'G**a R**s',
  'F**a B**a', 'P**a S**s', 'B**z L**a', 'E**a S**a', 'N**y M**a',
  'H**o C**a', 'I**a S**a', 'K**s M**o', 'W**r P**a', 'Y**a C**o',
  'S**a M**s', 'V**r H**o', 'L**s F**a', 'D**a G**s', 'M**o B**o',
  'J**o P**o', 'C**s E**o', 'R**a G**s', 'B**a N**s', 'T**s A**s',
  'A**r C**s', 'F**e M**a', 'L**u D**e', 'G**o B**o', 'R**n O**a',
  'M**s P**a', 'C**o L**a', 'B**a C**o', 'E**e S**s', 'L**z V**a',
  'R**l M**t', 'S**o F**o', 'T**g R**s', 'K**a L**a', 'J**n S**a',
  'P**o H**e', 'D**e A**s', 'V**a F**a', 'M**e T**o', 'N**a R**o',
  'G**l S**a', 'L**e C**o', 'F**o P**a', 'A**e M**s', 'C**e B**a',
  'I**r D**s', 'H**a N**o', 'T**a L**s', 'M**l G**o', 'Y**r S**a'
];

function formatTikTokMaskedName(name, index = 0) {
  if (!name) return BRAZILIAN_MASKED_NAMES[index % BRAZILIAN_MASKED_NAMES.length];
  const clean = name.trim();
  // Se contiver números, circunflexos ou se for handle/bot de shopee, NUNCA deixa passar! Substitui por nome brasileiro real
  if (/\d/.test(clean) || /\^/.test(clean) || /^[a-z0-9_.-]{1,6}$/i.test(clean) || clean.toLowerCase().includes('shopee') || clean.toLowerCase().includes('usuario') || clean.toLowerCase().includes('cliente')) {
    return BRAZILIAN_MASKED_NAMES[index % BRAZILIAN_MASKED_NAMES.length];
  }
  // Se já for mascarado estilo TikTok legítimo sem dígitos (ex: A**a N**a, L**a M**s, J**e, M** M**l)
  if (clean.includes('**') && !/\d/.test(clean) && !/\^/.test(clean)) {
    return clean;
  }
  const parts = clean.split(/[\s._-]+/).filter(Boolean);
  if (parts.length === 1) {
    const p = parts[0];
    if (p.length <= 2) return BRAZILIAN_MASKED_NAMES[index % BRAZILIAN_MASKED_NAMES.length];
    return p[0].toUpperCase() + '**' + p[p.length - 1].toLowerCase();
  }
  const first = parts[0];
  const last = parts[parts.length - 1];
  const m1 = first.length <= 2 ? first[0].toUpperCase() + '**' : first[0].toUpperCase() + '**' + first[first.length - 1].toLowerCase();
  const m2 = last.length <= 2 ? last[0].toUpperCase() + '**' : last[0].toUpperCase() + '**' + last[last.length - 1].toLowerCase();
  return `${m1} ${m2}`;
}

function extractAllReviewsForFullView() {
  const reviewsSection = document.querySelector('.reviews-section, .customer-reviews-section');
  const cards = reviewsSection ? Array.from(reviewsSection.querySelectorAll('.review-card')) : [];
  
  const prodTitle = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.nome) || document.querySelector('h1')?.textContent.trim() || 'Produto Oficial';
  
  // Preço com cupom
  let precoFormatado = '29,90';
  const btnBuyLine2 = document.querySelector('#btn-buy .btn-line2, .btn-buy-now .btn-line2');
  if (btnBuyLine2 && btnBuyLine2.textContent) {
    const m = btnBuyLine2.textContent.match(/R\$\s*([0-9.,]+)/i);
    if (m) precoFormatado = m[1];
  } else if (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.preco) {
    precoFormatado = parseFloat(PRODUTO_ATUAL.preco).toFixed(2).replace('.', ',');
  } else {
    const priceCurrent = document.querySelector('.price-current, .produto-preco-atual');
    if (priceCurrent) {
      const m = priceCurrent.textContent.match(/R\$\s*([0-9.,]+)/i);
      if (m) precoFormatado = m[1];
    }
  }

  // Nota média oficial
  let notaMedia = '4.1';
  const avgEl = document.querySelector('.review-avg');
  if (avgEl && avgEl.textContent.trim()) {
    notaMedia = avgEl.textContent.trim().replace(',', '.');
  } else {
    const topStarSpan = document.querySelector('.ratings-row .star-row span:nth-child(2)');
    if (topStarSpan && topStarSpan.textContent.trim()) {
      notaMedia = topStarSpan.textContent.trim().replace(',', '.');
    }
  }

  // Lista de variações disponíveis
  const variacoesDisponiveis = [];
  document.querySelectorAll('.var-item-pill, .var-size-btn, .option-card, .cor-btn, .tamanho-btn').forEach(b => {
    const val = b.getAttribute('data-val') || b.textContent.trim();
    if (val && !variacoesDisponiveis.includes(val)) variacoesDisponiveis.push(val);
  });
  if (variacoesDisponiveis.length === 0) {
    variacoesDisponiveis.push('Padrão');
  }

  // Coleta fotos reais de produtos para usar de forma elegante
  const photoPool = [];
  document.querySelectorAll('.swiper-slide img, .product-slider img, .slider-track img, .galeria-img, .review-photo, .review-compact-thumb-wrap img').forEach(img => {
    const s = img.src || '';
    if (s && !s.includes('data:image/svg') && !s.includes('avatar') && !photoPool.includes(s)) {
      photoPool.push(s);
    }
  });

  const list = [];
  cards.forEach((card, idx) => {
    // 1. Avatar (resiliente a mutação de DOM)
    const attrAvatar = card.getAttribute('data-author-avatar');
    const imgEl = card.querySelector('.review-avatar img');
    let avatarUrl = attrAvatar || ((imgEl && imgEl.src && !imgEl.src.includes('data:image/svg') && !imgEl.src.includes('_tn') && !imgEl.src.includes('susercontent.com') && !imgEl.src.includes('default-avatar')) ? imgEl.src : '');
    if (!avatarUrl) {
      avatarUrl = getAvatarForProductReview(null, idx);
    }

    // 2. Nome do autor
    const attrName = card.getAttribute('data-author-name');
    const rawName = attrName || card.querySelector('.review-user-name')?.textContent.trim() || `Cliente ${idx + 1}`;
    const maskedName = formatTikTokMaskedName(rawName, idx);

    // 3. Estrelas
    const attrStars = card.getAttribute('data-author-stars');
    const starsEl = card.querySelector('.review-user-stars');
    const starsTxt = starsEl ? starsEl.textContent.trim() : '';
    let starCount = attrStars ? parseInt(attrStars, 10) : 5;
    if (!attrStars && starsEl) {
      const polygonCount = starsEl.querySelectorAll('polygon, svg').length;
      if (polygonCount > 0) starCount = polygonCount;
      else if (starsTxt.includes('4') || starsTxt === '★★★★☆') starCount = 4;
      else if (starsTxt.includes('3') || starsTxt === '★★★☆☆') starCount = 3;
      else if (starsTxt.includes('2') || starsTxt === '★★☆☆☆') starCount = 2;
      else if (starsTxt.includes('1') || starsTxt === '★☆☆☆☆') starCount = 1;
    }

    // 4. Data e Variação
    const attrVar = card.getAttribute('data-author-variation');
    const attrDate = card.getAttribute('data-author-date');
    const dateEl = card.querySelector('.review-date');
    const dateTxt = dateEl ? dateEl.textContent.trim() : '';
    let parsedDate = attrDate || (idx === 0 ? '23/10' : (idx < 3 ? '1 sem.' : '2 sem.'));
    let parsedVar = attrVar || variacoesDisponiveis[idx % variacoesDisponiveis.length];

    if (!attrVar && !attrDate && dateTxt) {
      if (dateTxt.includes('·') || dateTxt.includes('|')) {
        const parts = dateTxt.split(/[·|]/);
        parsedDate = parts[0].trim();
        const vMatch = parts[1].replace(/.*varia[cç][aã]o\s*:\s*/gi, '').replace(/^[^:]*:\s*/, '').trim();
        if (vMatch) parsedVar = vMatch;
      } else {
        parsedDate = dateTxt.replace(/.*varia[cç][aã]o\s*:\s*/gi, '').trim();
      }
    }
    parsedVar = parsedVar.replace(/.*varia[cç][aã]o\s*:\s*/gi, '').replace(/^[^:]*:\s*/, '').replace(/^[•·\-\s]+/, '').trim();
    if (parsedVar.toLowerCase().indexOf('varia') !== -1) {
      parsedVar = parsedVar.replace(/.*varia[cç][aã]o\s*:\s*/gi, '').trim();
    }

    if (/^\d{4}-\d{2}-\d{2}/.test(parsedDate)) {
      const dp = parsedDate.split(' ')[0].split('-');
      parsedDate = `${dp[2]}/${dp[1]}`;
    } else if (/^\d{2}\/\d{2}\/\d{4}/.test(parsedDate)) {
      const dp = parsedDate.split('/');
      parsedDate = `${dp[0]}/${dp[1]}`;
    }

    // 5. Comentário
    const attrComment = card.getAttribute('data-author-comment');
    const commentEl = card.querySelector('.review-comment');
    const commentText = attrComment || (commentEl ? commentEl.textContent.trim() : '');

    // Mídias completas da avaliação (todas as fotos e vídeos reais sem limite de 3)
    const mediaList = [];
    const seenMedia = new Set();
    card.querySelectorAll('img.review-photo, video.review-video, video, .review-photos img, .review-photos video, .review-compact-thumb-wrap img, .review-compact-thumb-wrap video').forEach(m => {
      const s = m.src || '';
      if (s && !s.includes('data:image/svg') && !seenMedia.has(s)) {
        seenMedia.add(s);
        const isVid = m.tagName === 'VIDEO' || /\.(mp4|webm|mov|m4v)($|\?)/i.test(s) || s.includes('/vod/') || s.includes('/mms/');
        mediaList.push({ src: s, isVideo: isVid });
      }
    });

    const atributos = [];

    list.push({
      id: idx + 1,
      avatar: avatarUrl,
      name: maskedName,
      stars: starCount,
      variation: parsedVar,
      date: parsedDate,
      comment: commentText,
      attributes: atributos,
      media: mediaList,
      likes: (idx === 0 ? 0 : (idx === 3 ? 3 : 0))
    });
  });

  return {
    title: prodTitle,
    nota: notaMedia,
    preco: precoFormatado,
    reviews: list
  };
}

function renderChipsHtml(reviews, activeFilter) {
  const mediaCount = reviews.filter(r => r.media && r.media.length > 0).length;
  const s5 = reviews.filter(r => r.stars === 5).length;
  const s4 = reviews.filter(r => r.stars === 4).length;
  const s3 = reviews.filter(r => r.stars === 3).length;
  const s2 = reviews.filter(r => r.stars === 2).length;
  const s1 = reviews.filter(r => r.stars === 1).length;

  return `
    <button type="button" class="tt-rev-chip ${activeFilter === 'media' ? 'active' : ''}" onclick="ttSelectReviewFilter('media')">
      <svg width="14" height="14" viewBox="0 0 16 16" fill="#161823" style="display:inline-block; vertical-align:middle; flex-shrink:0;"><path fill-rule="evenodd" clip-rule="evenodd" d="M5.5 2.5C5.16 2.5 4.85 2.7 4.71 3.01L4.08 4.38C3.99 4.56 3.81 4.69 3.61 4.69H2.5C1.67 4.69 1 5.36 1 6.19V12C1 12.83 1.67 13.5 2.5 13.5H13.5C14.33 13.5 15 12.83 15 12V6.19C15 5.36 14.33 4.69 13.5 4.69H12.39C12.19 4.69 12.01 4.56 11.92 4.38L11.29 3.01C11.15 2.7 10.84 2.5 10.5 2.5H5.5ZM8 11.25C9.52 11.25 10.75 10.02 10.75 8.5C10.75 6.98 9.52 5.75 8 5.75C6.48 5.75 5.25 6.98 5.25 8.5C5.25 10.02 6.48 11.25 8 11.25ZM8 10C8.83 10 9.5 9.33 9.5 8.5C9.5 7.67 8.83 7 8 7C7.17 7 6.5 7.67 6.5 8.5C6.5 9.33 7.17 10 8 10Z"/></svg>
      <span>Inclui imagens ou vídeos</span>
      <span class="tt-rev-chip-count">(${mediaCount})</span>
    </button>
    <button type="button" class="tt-rev-chip ${activeFilter === '5' ? 'active' : ''}" onclick="ttSelectReviewFilter('5')">
      ${getTTOfficialStarSvg(11.5, true)}
      <span>5</span>
      <span class="tt-rev-chip-count">(${s5})</span>
    </button>
    <button type="button" class="tt-rev-chip ${activeFilter === '4' ? 'active' : ''}" onclick="ttSelectReviewFilter('4')">
      ${getTTOfficialStarSvg(11.5, true)}
      <span>4</span>
      <span class="tt-rev-chip-count">(${s4})</span>
    </button>
    <button type="button" class="tt-rev-chip ${activeFilter === '3' ? 'active' : ''}" onclick="ttSelectReviewFilter('3')">
      ${getTTOfficialStarSvg(11.5, true)}
      <span>3</span>
      <span class="tt-rev-chip-count">(${s3})</span>
    </button>
    <button type="button" class="tt-rev-chip ${activeFilter === '2' ? 'active' : ''}" onclick="ttSelectReviewFilter('2')">
      ${getTTOfficialStarSvg(11.5, true)}
      <span>2</span>
      <span class="tt-rev-chip-count">(${s2})</span>
    </button>
    <button type="button" class="tt-rev-chip ${activeFilter === '1' ? 'active' : ''}" onclick="ttSelectReviewFilter('1')">
      ${getTTOfficialStarSvg(11.5, true)}
      <span>1</span>
      <span class="tt-rev-chip-count">(${s1})</span>
    </button>
  `;
}

function renderReviewsListHtml(reviews, filter, sort) {
  let filtered = reviews.slice();

  if (filter === 'media') {
    filtered = filtered.filter(r => r.media && r.media.length > 0);
  } else if (filter === '5' || filter === '5stars') {
    filtered = filtered.filter(r => r.stars === 5);
  } else if (filter === '4') {
    filtered = filtered.filter(r => r.stars === 4);
  } else if (filter === '3') {
    filtered = filtered.filter(r => r.stars === 3);
  } else if (filter === '2') {
    filtered = filtered.filter(r => r.stars === 2);
  } else if (filter === '1') {
    filtered = filtered.filter(r => r.stars === 1);
  }

  if (sort === 'rating') {
    filtered.sort((a, b) => b.stars - a.stars);
  }

  if (filtered.length === 0) {
    return `<div style="text-align:center; padding:40px 20px; color:#888; font-size:13.5px;">Nenhuma avaliação encontrada para este filtro.</div>`;
  }

  return filtered.map(r => {
    let starsHtml = '';
    for (let i = 1; i <= 5; i++) {
      starsHtml += getTTOfficialStarSvg(13, i <= r.stars);
    }

    const cleanVar = (r.variation || '')
      .replace(/.*varia[cç][aã]o\s*:\s*/gi, '')
      .replace(/^[^:]*:\s*/, '')
      .replace(/^[•·\-\s]+/, '')
      .trim();

    const fallbackSvg = isPagesDirApp ? '../img/reviews-avatars/default-avatar.svg' : 'img/reviews-avatars/default-avatar.svg';
    const avatarHtml = `<img src="${r.avatar}" alt="" style="width:100%; height:100%; object-fit:cover; display:block;" onerror="this.onerror=null; this.src='${fallbackSvg}';">`;

    let attrHtml = '';
    if (r.attributes && r.attributes.length > 0) {
      attrHtml = `
        <div class="tt-rev-attributes">
          ${r.attributes.map(a => `<div>${a}</div>`).join('')}
        </div>
      `;
    }

    let mediaHtml = '';
    if (r.media && r.media.length > 0) {
      mediaHtml = `
        <div class="tt-rev-media-grid">
          ${r.media.map((m, mIdx) => {
            const src = typeof m === 'string' ? m : (m.src || '');
            const isVid = typeof m === 'string' ? (/\.(mp4|webm|mov|m4v)($|\?)/i.test(src) || src.includes('/vod/') || src.includes('/mms/')) : !!m.isVideo;
            return `
              <div class="tt-rev-media-item" onclick="ttOpenReviewMedia(${r.id}, ${mIdx})">
                ${isVid 
                  ? `<video src="${src}" muted playsinline loop style="width:100%; height:100%; object-fit:cover; display:block; pointer-events:none;"></video>
                     <div class="tt-rev-play-badge">
                       <svg viewBox="0 0 24 24" width="10" height="10" fill="#fff"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                     </div>`
                  : `<img src="${src}" alt="" loading="lazy" style="width:100%; height:100%; object-fit:cover; display:block;">`
                }
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    const commentHtml = r.comment ? `<p class="tt-rev-comment">${r.comment}</p>` : '';

    return `
      <div class="tt-full-review-card">
        <div class="tt-rev-user-row">
          <div class="tt-rev-user-avatar">
            ${avatarHtml}
          </div>
          <div class="tt-rev-user-meta">
            <div class="tt-rev-user-name">${r.name}</div>
            <div class="tt-rev-user-subline">
              <span class="tt-rev-stars">${starsHtml}</span>
              ${cleanVar ? `<span class="tt-rev-dot">·</span><span class="tt-rev-variation">${cleanVar}</span>` : ''}
            </div>
          </div>
        </div>

        ${attrHtml}
        ${commentHtml}
        ${mediaHtml}

        <div class="tt-rev-footer-row">
          <span class="tt-rev-date">${r.date}</span>
          <div class="tt-rev-actions">
            <div class="tt-rev-more-btn" onclick="ttShowMoreToast()">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="#8a8b91">
                <circle cx="5" cy="12" r="2"></circle>
                <circle cx="12" cy="12" r="2"></circle>
                <circle cx="19" cy="12" r="2"></circle>
              </svg>
            </div>
            <div class="tt-rev-like-btn" onclick="ttToggleLikeReview(this, event)">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 10v12"/>
                <path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h3"/>
              </svg>
              <span class="tt-like-count">${r.likes > 0 ? r.likes : ''}</span>
            </div>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

window.ttSelectReviewFilter = function(filter) {
  if (_ttFullReviewsActiveFilter === filter) {
    _ttFullReviewsActiveFilter = 'all';
  } else {
    _ttFullReviewsActiveFilter = filter;
  }
  const chipsContainer = document.getElementById('tt-rev-chips-container');
  if (chipsContainer && _ttFullReviewsData) {
    chipsContainer.innerHTML = renderChipsHtml(_ttFullReviewsData.reviews, _ttFullReviewsActiveFilter);
  }
  const listContainer = document.getElementById('tt-rev-cards-list');
  if (listContainer && _ttFullReviewsData) {
    listContainer.innerHTML = renderReviewsListHtml(_ttFullReviewsData.reviews, _ttFullReviewsActiveFilter, _ttFullReviewsSort);
  }
};

window.ttToggleSortOrder = function() {
  _ttFullReviewsSort = _ttFullReviewsSort === 'recent' ? 'rating' : 'recent';
  const label = document.getElementById('tt-sort-label');
  if (label) {
    label.textContent = _ttFullReviewsSort === 'recent' ? 'Mais recentes' : 'Maior nota';
  }
  const listContainer = document.getElementById('tt-rev-cards-list');
  if (listContainer && _ttFullReviewsData) {
    listContainer.innerHTML = renderReviewsListHtml(_ttFullReviewsData.reviews, _ttFullReviewsActiveFilter, _ttFullReviewsSort);
  }
};

window.ttToggleLikeReview = function(el, e) {
  if (e) { e.preventDefault(); e.stopPropagation(); }
  el.classList.toggle('liked');
  const countEl = el.querySelector('.tt-like-count');
  if (countEl) {
    let cur = parseInt(countEl.textContent.trim()) || 0;
    if (el.classList.contains('liked')) {
      countEl.textContent = String(cur + 1);
    } else {
      countEl.textContent = cur > 1 ? String(cur - 1) : '';
    }
  }
};

window.ttShowMoreToast = function() {
  if (typeof showToast === 'function') {
    showToast('Avaliação marcada como útil');
  } else {
    const t = document.createElement('div');
    t.className = 'tiktok-toast-notification';
    t.textContent = 'Avaliação marcada como útil';
    document.body.appendChild(t);
    setTimeout(() => { t.remove(); }, 2000);
  }
};

window.ttShareProduct = function() {
  if (navigator.share) {
    navigator.share({
      title: document.title,
      url: window.location.href
    }).catch(() => {});
  } else {
    if (typeof showToast === 'function') {
      showToast('Link do produto copiado!');
    }
    try { navigator.clipboard.writeText(window.location.href); } catch(e) {}
  }
};

window.ttHandleBuyFromReviews = function() {
  fecharTelaAvaliacoesCompletas();
  if (typeof handleBuyNow === 'function') {
    handleBuyNow();
  } else if (typeof openVariacaoModal === 'function' && typeof PRODUTO_ATUAL !== 'undefined') {
    openVariacaoModal(PRODUTO_ATUAL, 'buy');
  } else {
    const btnBuy = document.querySelector('#btn-buy, .btn-buy, .btn-buy-now');
    if (btnBuy) btnBuy.click();
  }
};

window.abrirTelaAvaliacoesCompletas = function(filtro = 'all') {
  _ttFullReviewsActiveFilter = filtro || 'all';
  const data = extractAllReviewsForFullView();
  _ttFullReviewsData = data;

  let overlay = document.getElementById('tiktok-full-reviews-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'tiktok-full-reviews-overlay';
    document.body.appendChild(overlay);
  }

  overlay.innerHTML = `
    <!-- Top Header Oficial TikTok Shop com Ícones Exatos da Imagem 1 -->
    <div class="tt-rev-header">
      <div class="tt-rev-header-left" onclick="fecharTelaAvaliacoesCompletas()">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </div>
      <div class="tt-rev-header-title">
        ${getTTOfficialStarSvg(16, true)}
        <span style="font-weight:700;">${data.nota}</span>
        <span>Avaliações (${data.reviews.length})</span>
      </div>
      <div class="tt-rev-header-right">
        <div class="tt-rev-share-btn" onclick="ttShareProduct()">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M13.5 4.5l6.5 6.5-6.5 6.5v-4.2c-5.2 0-8.8 1.8-11.5 5.7 1.1-5.5 4.3-10.8 11.5-11.8V4.5z"/>
          </svg>
        </div>
        <div class="tt-rev-cart-icon-wrap" onclick="window.location.href='carrinho.html'">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          <span class="tt-rev-cart-badge">13</span>
        </div>
      </div>
    </div>

    <!-- Filter Chips Bar Oficial em 2 Linhas Exatas como a Imagem 1 -->
    <div class="tt-rev-chips-bar" id="tt-rev-chips-container">
      ${renderChipsHtml(data.reviews, _ttFullReviewsActiveFilter)}
    </div>

    <!-- Subheader Oficial Imagem 1: Veja o que os outros clientes estão dizendo ⓘ + Mais recentes ◷ em Linha Única Perfeita -->
    <div class="tt-rev-subheader">
      <div class="tt-rev-sub-left">
        <span>Veja o que os outros clientes estão dizendo</span>
        <span class="tt-rev-info-icon">ⓘ</span>
      </div>
      <div class="tt-rev-sub-right" onclick="ttToggleSortOrder()">
        <span id="tt-sort-label">Mais recentes</span>
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </div>
    </div>

    <!-- Lista de Avaliações em Feed com Rolagem Suave -->
    <div class="tt-rev-list" id="tt-rev-cards-list">
      ${renderReviewsListHtml(data.reviews, _ttFullReviewsActiveFilter, _ttFullReviewsSort)}
    </div>

    <!-- Fixed Bottom Bar TikTok Shop Oficial (Botão Rosa com Carrinho + Compre) -->
    <div class="tt-rev-bottom-bar">
      <div class="tt-rev-bottom-left">
        <!-- Bloco Oficial Loja e Chat idêntico à Página Inicial e Produto -->
        <div class="store-chat-image-group tt-rev-store-chat">
          <div class="store-chat-clickable-loja" onclick="window.location.href='../index.html'"></div>
          <div class="store-chat-clickable-chat" onclick="if (typeof openSmartChat==='function') openSmartChat(); else window.location.href='../index.html'"></div>
        </div>
        <!-- Caixa Rosa com Carrinho e Ícone de Mais Oficial TikTok Shop -->
        <div class="tt-rev-cart-box-btn" onclick="window.location.href='carrinho.html'">
          <svg aria-hidden="true" width="25" height="22" viewBox="0 0 50 44" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3.8 4H8.6C9.8 4 10.5 4.6 10.8 5.8L15.6 26.2C16.1 28.3 17.5 29.5 19.7 29.5H37.3C39.5 29.5 40.9 28.3 41.5 26.2L45.3 12.8" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="4"></path>
            <path d="M28.5 6V19M22 12.5H35" stroke="currentColor" stroke-linecap="round" stroke-width="4"></path>
            <circle cx="17" cy="38" r="3.5" fill="currentColor"></circle>
            <circle cx="40" cy="38" r="3.5" fill="currentColor"></circle>
          </svg>
        </div>
      </div>
      <button type="button" class="tt-rev-btn-buy" onclick="ttHandleBuyFromReviews()">
        <span class="tt-buy-line1">Compre</span>
        <span class="tt-buy-line2">R$ ${data.preco} com cupom</span>
      </button>
    </div>
  `;

  requestAnimationFrame(() => {
    overlay.classList.add('tt-active');
    document.body.style.overflow = 'hidden';
  });

  try {
    if (!window.history.state || !window.history.state.ttReviewsModal) {
      window.history.pushState({ ttReviewsModal: true }, '');
    }
  } catch(e) {}
};

window.fecharTelaAvaliacoesCompletas = function(triggerHistoryBack = true) {
  const overlay = document.getElementById('tiktok-full-reviews-overlay');
  if (overlay) {
    overlay.classList.remove('tt-active');
  }
  document.body.style.overflow = '';
  if (triggerHistoryBack) {
    try {
      if (window.history.state && window.history.state.ttReviewsModal) {
        window.history.back();
      }
    } catch(e) {}
  }
};

window.addEventListener('popstate', function(e) {
  const overlay = document.getElementById('tiktok-full-reviews-overlay');
  if (overlay && overlay.classList.contains('tt-active')) {
    window.fecharTelaAvaliacoesCompletas(false);
  }
});

// Expansão Dinâmica de Avaliações ao Clicar na Seta ou em 'Ver mais ›'
window.expandStoreReviews = function() {
  window.abrirTelaAvaliacoesCompletas();
};

window.verMaisReviews = function(containerId, btnId, totalOriginal) {
  window.abrirTelaAvaliacoesCompletas();
};

const EXTRA_STORE_REVIEWS = [
  {
    nome: 'Mariana Souza',
    iniciais: 'M',
    foto: 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/3b26c7e2b6e19c085cbca3e8e2c0b020~tplv-tiktokx-cropcenter:100:100.jpg',
    estrelas: '⭐⭐⭐⭐⭐',
    data: '15/10/2026',
    comentario: 'Muito satisfeita com a compra! Postaram super rápido, produto veio muito bem embalado e idêntico às fotos. Recomendo!',
    midias: [
      'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/79bf69882ab7434bb96ad7521ba36aa3~tplv-aphluv4xwc-crop-webp:300:300.webp',
      'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/3d4600770ace47a6a81fa34b7f8d70c1~tplv-aphluv4xwc-crop-webp:300:300.webp',
      'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/7ea205573dd5458389d61912d996e766~tplv-aphluv4xwc-crop-webp:300:300.webp'
    ]
  },
  {
    nome: 'Gabriela Duarte',
    iniciais: 'G',
    foto: '',
    estrelas: '⭐⭐⭐⭐⭐',
    data: '12/10/2026',
    comentario: 'Atendimento nota 10 no chat e entrega antes do prazo previsto. O produto superou as expectativas, material de altíssima qualidade!',
    midias: []
  },
  {
    nome: 'Priscila Mendes',
    iniciais: 'P',
    foto: 'https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/a8bb9a9af974fb6c5d2ff46ea8688158~tplv-tiktokx-cropcenter:100:100.jpg',
    estrelas: '⭐⭐⭐⭐⭐',
    data: '08/10/2026',
    comentario: 'Segunda vez que compro na loja. Sempre chega tudo impecável, sem nenhum defeito. Podem comprar sem medo.',
    midias: [
      'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/30679ceee5ff422892d1b8161722a9ea~tplv-aphluv4xwc-crop-webp:300:300.webp',
      'https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/d2e7e165475c4959af274c3a31b3c9a4~tplv-aphluv4xwc-crop-webp:300:300.webp'
    ]
  },
  {
    nome: 'Larissa Albuquerque',
    iniciais: 'L',
    foto: '',
    estrelas: '⭐⭐⭐⭐⭐',
    data: '04/10/2026',
    comentario: 'Chegou em 3 dias aqui em São Paulo! Linda demais, acabamento perfeito e muito confortável.',
    midias: []
  }
];

function appendNextStoreReviews(reviewsSection) {
  const storeSummaryBlock = reviewsSection.querySelector('.store-reviews-summary-block');
  window._extraStoreReviewIdx = (window._extraStoreReviewIdx || 0);

  if (window._extraStoreReviewIdx >= EXTRA_STORE_REVIEWS.length) {
    return;
  }

  const batch = EXTRA_STORE_REVIEWS.slice(window._extraStoreReviewIdx, window._extraStoreReviewIdx + 2);
  window._extraStoreReviewIdx += batch.length;

  batch.forEach(rev => {
    const midias = Array.isArray(rev.midias) ? rev.midias : (rev.midia ? [rev.midia] : []);
    const hasMedia = midias.length > 0;
    const card = document.createElement('div');
    card.className = 'review-card';
    card.setAttribute('data-has-media', hasMedia ? 'true' : 'false');
    card.setAttribute('data-is-5stars', 'true');
    card.style.cssText = 'display:flex; justify-content:space-between; align-items:flex-start; padding:12px 0; border-bottom:1px solid #f0f0f0; opacity:0; transform:translateY(6px); transition:opacity 0.25s ease, transform 0.25s ease;';

    const avatarHtml = rev.foto
      ? `<img src="${rev.foto}" alt="${rev.nome}" style="width:100%; height:100%; object-fit:cover; border-radius:50%;" onerror="this.outerHTML='<div class=\\'review-avatar-placeholder\\'>${rev.iniciais}</div>'">`
      : `<div class="review-avatar-placeholder" style="width:100%; height:100%; border-radius:50%; background:#f0f0f0; display:flex; align-items:center; justify-content:center; font-weight:700; color:#555; font-size:13px;">${rev.iniciais}</div>`;

    const mediaThumbHtml = hasMedia ? `
      <div class="review-compact-thumb-wrap" style="width:70px; height:70px; min-width:70px; border-radius:6px; overflow:hidden; position:relative; flex-shrink:0; cursor:pointer; background:#f5f5f5; margin-left:10px;">
        <img src="${midias[0]}" alt="Mídia do cliente" style="width:100%; height:100%; object-fit:cover; display:block;">
        ${midias.length > 1 ? `<div style="position:absolute; bottom:3px; right:3px; background:rgba(0,0,0,0.65); color:#fff; font-size:10px; font-weight:700; padding:1px 5px; border-radius:3px; pointer-events:none;">+${midias.length}</div>` : ''}
      </div>
    ` : '';

    card.innerHTML = `
      <div style="flex:1; min-width:0;">
        <div class="review-header" style="margin-bottom:6px;">
          <div class="review-user" style="display:flex; align-items:center; gap:8px;">
            <div class="review-avatar" style="width:32px; height:32px; border-radius:50%; overflow:hidden; flex-shrink:0;">
              ${avatarHtml}
            </div>
            <div class="review-user-info" style="font-size:12px;">
              <div class="review-user-name" style="font-weight:700; color:#111;">${rev.nome}</div>
              <div style="display:flex; align-items:center; gap:4px; margin-top:1px;">
                <span class="review-user-stars" style="color:#f5a623; font-size:11px;">${rev.estrelas}</span>
                <span class="review-date" style="color:#888; font-size:11px;">· ${rev.data}</span>
              </div>
            </div>
          </div>
        </div>
        <p class="review-comment" style="font-size:13px; line-height:1.4; color:#222; margin:0;">${rev.comentario}</p>
      </div>
      ${mediaThumbHtml}
    `;

    if (hasMedia) {
      const thumb = card.querySelector('.review-compact-thumb-wrap');
      if (thumb) {
        thumb.onclick = (e) => {
          if (e && typeof e.stopPropagation === 'function') e.stopPropagation();
          if (typeof openPhotoModal === 'function') openPhotoModal(midias, 0);
        };
      }
    }

    if (storeSummaryBlock) {
      reviewsSection.insertBefore(card, storeSummaryBlock);
    } else {
      reviewsSection.appendChild(card);
    }

    requestAnimationFrame(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    });
  });
}

window._currentReviewFilter = null;
window.toggleReviewFilter = function(filterType) {
  if (typeof window.abrirTelaAvaliacoesCompletas === 'function') {
    window.abrirTelaAvaliacoesCompletas(filterType === '5stars' ? '5' : filterType);
    return;
  }
  const reviewsSection = document.querySelector('.reviews-section, .customer-reviews-section');
  if (!reviewsSection) return;

  const btnMedia = reviewsSection.querySelector('.review-chip-media');
  const btnRating = reviewsSection.querySelector('.review-chip-rating');
  const allCards = Array.from(reviewsSection.querySelectorAll('.review-card'));

  if (window._currentReviewFilter === filterType) {
    window._currentReviewFilter = null;
    if (btnMedia) {
      btnMedia.style.background = '#fdf5ea';
      btnMedia.style.borderColor = '#f8e4c8';
      btnMedia.style.fontWeight = '600';
    }
    if (btnRating) {
      btnRating.style.background = '#fdf5ea';
      btnRating.style.borderColor = '#f8e4c8';
      btnRating.style.fontWeight = '600';
    }
    allCards.forEach((c, idx) => {
      c.classList.remove('filtered-out');
      if (idx < 3) {
        c.classList.remove('review-card-hidden');
        c.classList.add('review-card-visible');
        c.style.setProperty('display', 'flex', 'important');
      } else {
        c.classList.remove('review-card-visible');
        c.classList.add('review-card-hidden');
        c.style.setProperty('display', 'none', 'important');
      }
    });
    return;
  }

  window._currentReviewFilter = filterType;

  if (filterType === 'media') {
    if (btnMedia) {
      btnMedia.style.background = '#fae4c8';
      btnMedia.style.borderColor = '#d49a46';
      btnMedia.style.fontWeight = '700';
    }
    if (btnRating) {
      btnRating.style.background = '#fdf5ea';
      btnRating.style.borderColor = '#f8e4c8';
      btnRating.style.fontWeight = '600';
    }
    allCards.forEach(card => {
      const hasMedia = card.getAttribute('data-has-media') === 'true' ||
                       card.querySelector('.review-compact-thumb-wrap') !== null ||
                       (card.querySelector('.review-photos') && card.querySelector('.review-photos img, .review-photos video'));
      if (hasMedia) {
        card.classList.remove('filtered-out');
        card.classList.remove('review-card-hidden');
        card.classList.add('review-card-visible');
        card.style.setProperty('display', 'flex', 'important');
      } else {
        card.classList.add('filtered-out');
        card.classList.remove('review-card-visible');
        card.classList.add('review-card-hidden');
        card.style.setProperty('display', 'none', 'important');
      }
    });
  } else if (filterType === '5stars') {
    if (btnRating) {
      btnRating.style.background = '#fae4c8';
      btnRating.style.borderColor = '#d49a46';
      btnRating.style.fontWeight = '700';
    }
    if (btnMedia) {
      btnMedia.style.background = '#fdf5ea';
      btnMedia.style.borderColor = '#f8e4c8';
      btnMedia.style.fontWeight = '600';
    }
    allCards.forEach(card => {
      const is5 = card.getAttribute('data-is-5stars') === 'true';
      if (is5) {
        card.classList.remove('filtered-out');
        card.classList.remove('review-card-hidden');
        card.classList.add('review-card-visible');
        card.style.setProperty('display', 'flex', 'important');
      } else {
        card.classList.add('filtered-out');
        card.classList.remove('review-card-visible');
        card.classList.add('review-card-hidden');
        card.style.setProperty('display', 'none', 'important');
      }
    });
  }
};

// Item 14: Player de Vídeo Oficial "Sobre este produto" com Guia de Tamanhos
function renderSobreEsteProdutoVideo() {
  // Desativado: o bloco oficial Sobre este produto é estruturado diretamente no HTML sem duplicações
  return;
}

// Função para enviar o produto escolhido DIRETO para o resumo (Checkout 1-click)
function irDiretoAoCheckoutComProduto(produto, varLabel, qty) {
  const itemQty = parseInt(qty) || 1;
  const precoNum = typeof produto.preco === 'number'
    ? produto.preco
    : parseFloat(String(produto.preco).replace(',', '.')) || 0;

  let imgProd = produto.img || '';
  if (!imgProd && Array.isArray(produto.imagem)) {
    imgProd = produto.imagem.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || produto.imagem[0];
  } else if (!imgProd && typeof produto.imagem === 'string') {
    imgProd = produto.imagem;
  } else if (!imgProd && Array.isArray(produto.imagens)) {
    imgProd = produto.imagens.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || produto.imagens[0];
  }

  const checkoutItem = {
    id: produto.id,
    nome: produto.nome,
    preco: precoNum,
    precoOrig: produto.precoOrig || null,
    img: imgProd,
    variacao: varLabel || '',
    qty: itemQty
  };

  // Garante que o item também é sincronizado no carrinho geral para persistência
  addToCart(produto, itemQty);

  // Sobrescreve checkout_cart para conter EXCLUSIVAMENTE o produto escolhido
  // Feedback visual imediato: Loader oficial de 2 bolinhas com fundo escuro 0.50
  if (typeof window.showTikTokLoader === 'function') {
    window.showTikTokLoader({ type: 'normal', duration: 900 });
  }
  try { localStorage.setItem('famosinhos_checkout_cart', JSON.stringify([checkoutItem])); } catch (e) { }
  try { sessionStorage.setItem('famosinhos_checkout_cart', JSON.stringify([checkoutItem])); } catch (e) { }

  // Redireciona com breve delay suave para o cliente ver o HUD na tela correta com parâmetros de fallback blindados
  const isPagesDir = window.location.pathname.includes('/pages/');
  const targetBase = isPagesDir ? 'resumo.html' : 'pages/resumo.html';
  const queryParts = [
    'produto=' + encodeURIComponent(checkoutItem.id),
    'preco=' + encodeURIComponent(checkoutItem.preco),
    'qty=' + encodeURIComponent(checkoutItem.qty || 1)
  ];
  if (checkoutItem.variacao) queryParts.push('var=' + encodeURIComponent(checkoutItem.variacao));
  if (checkoutItem.img) queryParts.push('img=' + encodeURIComponent(checkoutItem.img));
  queryParts.push('v=' + Date.now());

  const targetUrl = targetBase + '?' + queryParts.join('&');
  window.location.href = targetUrl;
}
window.irDiretoAoCheckoutComProduto = irDiretoAoCheckoutComProduto;

// Função que intercepta o clique de "Adicionar ao carrinho" e "Comprar agora"
// para produtos com variações
function handleAddToCartWithVariacoes(produto, buyNow = false) {
  // Se o produto não possui variações declaradas no catálogo, cria dinamicamente uma variação de 1 opção única
  if (!produto.variacoes || Object.keys(produto.variacoes).length === 0) {
    produto.variacoes = {
      "modelo": {
        "label": "OPÇÃO",
        "opcoes": [
          {
            "nome": "Padrão único",
            "imagem": produto.img || ""
          }
        ]
      }
    };
  }

  const variacoes = produto.variacoes || {};
  const keys = Object.keys(variacoes);

  if (!keys.length) {
    // Sem variações: comportamento padrão
    if (buyNow) {
      irDiretoAoCheckoutComProduto(produto, '', 1);
    } else {
      // Loader bolinhas ao adicionar
      if (typeof window.showTikTokLoader === 'function') {
        window.showTikTokLoader({ type: 'normal', duration: 450 });
      }
      addToCart(produto);
      animateFlyToCart();
    }
    return;
  }

  // Tem variações: abre modal informando se o fluxo é comprar ou carrinho
  openVariacaoModal(produto, buyNow ? 'buy' : 'cart', function ({ selecionados, qty, tipo, imagem, preco, precoOrig }) {
    // Monta a variação como string para exibir no carrinho
    const varLabel = selecionados
      ? Object.values(selecionados).join(', ')
      : '';

    // Cria objeto do produto com a imagem e preço da variação escolhida
    const produtoComVariacao = {
      ...produto,
      preco: (typeof preco === 'number' && !isNaN(preco) && preco > 0) ? preco : produto.preco,
      precoOrig: (precoOrig !== undefined && precoOrig !== null) ? precoOrig : (produto.precoOrig || produto.preco_antigo),
      img: imagem || produto.img
    };

    // Modifica a inclusão de forma redundante para usar window.parent.addToCart se estiver no iframe
    let localAddToCart = addToCart;
    let localGetCart = getCart;
    let localSaveCart = saveCart;
    let localUpdateCartBadges = updateCartBadges;
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const isFromStoreList = urlParams.get('fromStoreList') === '1';
      if (isFromStoreList && window.parent) {
        if (typeof window.parent.addToCart === 'function') localAddToCart = window.parent.addToCart;
        if (typeof window.parent.getCart === 'function') localGetCart = window.parent.getCart;
        if (typeof window.parent.saveCart === 'function') localSaveCart = window.parent.saveCart;
        if (typeof window.parent.updateCartBadges === 'function') localUpdateCartBadges = window.parent.updateCartBadges;
      }
    } catch (e) { }

    localAddToCart(produtoComVariacao, qty);

    // Registra variação no carrinho (sobrescreve com a variação e foto correta)
    try {
      const cart = localGetCart();
      const idx = cart.findIndex(i => Number(i.id) === Number(produtoComVariacao.id) && (!i.variacao || i.variacao === varLabel));
      if (idx >= 0 && varLabel) {
        cart[idx].variacao = varLabel;
        if (imagem) cart[idx].img = imagem;
        if (preco) cart[idx].preco = preco;
        localSaveCart(cart);
        localUpdateCartBadges();
      }
    } catch (e) { }

    // Notificação manual e redundante para a página pai
    try {
      if (window.parent && window.parent.updateCartBadges) {
        window.parent.updateCartBadges();
        window.parent.updateFloatingCartBar();
      }
    } catch (e) { }

    if (tipo === 'buy') {
      irDiretoAoCheckoutComProduto(produtoComVariacao, varLabel, qty);
    } else {
      animateFlyToCart();
    }
  });
}

// ===== CHAT INTELIGENTE E BOTÃO SEGUIR =====

function initSeguirBtn() {
  const followBtns = document.querySelectorAll('.store-follow-btn');
  if (!followBtns.length) return;

  const isSeguindo = (localStorage.getItem('loja_seguindo') === 'true' || localStorage.getItem('seguindo_loja') === 'true');

  followBtns.forEach(btn => {
    updateFollowBtnState(btn, isSeguindo);
    btn.onclick = function(e) {
      if (e) e.stopPropagation();
      toggleSeguirLoja(this);
    };
  });
}

function updateFollowBtnState(btn, isSeguindo) {
  if (!btn) return;
  if (isSeguindo) {
    btn.innerHTML = '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right:2px; vertical-align:-1px;"><polyline points="20 6 9 17 4 12"></polyline></svg> Seguindo';
    btn.classList.add('following');
    btn.style.setProperty('background', '#f1f1f2', 'important');
    btn.style.setProperty('color', '#161823', 'important');
    btn.style.border = 'none';
    btn.style.fontWeight = '600';
  } else {
    btn.innerHTML = 'Seguir';
    btn.classList.remove('following');
    btn.style.setProperty('background', '#fe2c55', 'important');
    btn.style.setProperty('color', '#ffffff', 'important');
    btn.style.border = 'none';
    btn.style.fontWeight = '600';
  }
}

function toggleSeguirLoja(btn) {
  const current = (localStorage.getItem('loja_seguindo') === 'true' || localStorage.getItem('seguindo_loja') === 'true');
  const novoEstado = !current;
  try {
    localStorage.setItem('loja_seguindo', novoEstado ? 'true' : 'false');
    localStorage.setItem('seguindo_loja', novoEstado ? 'true' : 'false');
  } catch (e) {}

  document.querySelectorAll('.store-follow-btn').forEach(b => {
    updateFollowBtnState(b, novoEstado);
  });

  if (typeof showToast === 'function') {
    if (novoEstado) {
      showToast('❤️ Você começou a seguir Stone Shop!');
    } else {
      showToast('Você deixou de seguir Stone Shop');
    }
  }
}
window.toggleSeguirLoja = toggleSeguirLoja;
window.updateFollowBtnState = updateFollowBtnState;

// Chat Oficial 1:1 TikTok Shop (Stone Shop)
function openSmartChat() {
  const existing = document.getElementById('smart-chat-overlay');
  if (existing) {
    existing.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    return;
  }

  const now = new Date();
  const timeStr = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');

  // Coleta dados reais do produto atual (se estiver numa página de produto)
  const hasProd = typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL && PRODUTO_ATUAL.nome;
  const domSliderImg = document.querySelector('.slider-track .slider-img, .slider-img');
  const prodImg = hasProd ? (PRODUTO_ATUAL.img || (Array.isArray(PRODUTO_ATUAL.imagens) && PRODUTO_ATUAL.imagens[0]) || (domSliderImg ? domSliderImg.src : '')) : '';
  const prodName = hasProd ? String(PRODUTO_ATUAL.nome) : '';
  const prodPriceNum = hasProd ? Number(PRODUTO_ATUAL.preco || 0) : 0;
  const prodOrigNum = hasProd ? Number(PRODUTO_ATUAL.preco_antigo || 0) : 0;
  const prodPriceStr = hasProd ? ('R$ ' + prodPriceNum.toFixed(2).replace('.', ',')) : '';
  const prodOrigStr = (hasProd && prodOrigNum > prodPriceNum) ? ('R$ ' + prodOrigNum.toFixed(2).replace('.', ',')) : (document.querySelector('.price-original')?.textContent?.trim() || '');
  const soldText = document.querySelector('.sold-count')?.textContent?.trim() || '2540 vendidos on-line';

  const botAvatarSvg = `<div class="tt-chat-bot-avatar" aria-hidden="true">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="5.1" r="1.75" stroke="#161823" stroke-width="1.75"></circle>
      <line x1="12" y1="6.85" x2="12" y2="8.5" stroke="#161823" stroke-width="1.85"></line>
      <rect x="5.8" y="8.5" width="12.4" height="9.6" rx="2.1" stroke="#161823" stroke-width="1.8"></rect>
      <circle cx="9.65" cy="13.3" r="1.2" fill="#161823"></circle>
      <circle cx="14.35" cy="13.3" r="1.2" fill="#161823"></circle>
      <line x1="3.2" y1="11.1" x2="3.2" y2="15.5" stroke="#161823" stroke-width="1.85" stroke-linecap="butt"></line>
      <line x1="20.8" y1="11.1" x2="20.8" y2="15.5" stroke="#161823" stroke-width="1.85" stroke-linecap="butt"></line>
    </svg>
  </div>`;

  const chevronSvg = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polyline points="9 18 15 12 9 6"></polyline></svg>`;

  const overlay = document.createElement('div');
  overlay.id = 'smart-chat-overlay';
  overlay.style.cssText = `
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.45); z-index: 100000;
    display: flex; align-items: flex-end; justify-content: center;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  `;

  const chatContainer = document.createElement('div');
  chatContainer.id = 'smart-chat-container';
  chatContainer.style.cssText = `
    width: 100%; max-width: 480px; height: 100dvh;
    background: #f5f5f5;
    display: flex; flex-direction: column; overflow: hidden;
    animation: slideUpTTChat 0.22s ease-out;
  `;

  const floatingProductCardHtml = hasProd ? `
    <div class="tt-chat-product-float" id="tt-chat-product-float">
      <button type="button" class="tt-chat-float-close" aria-label="Fechar produto" onclick="document.getElementById('tt-chat-product-float')?.remove()">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
      </button>
      <img class="tt-chat-float-img" src="${prodImg}" alt="${prodName.replace(/"/g, '&quot;')}">
      <div class="tt-chat-float-info">
        <div class="tt-chat-float-title">${prodName}</div>
        <div class="tt-chat-float-sold">${soldText}</div>
        <div class="tt-chat-float-price-row">
          <span class="tt-chat-float-price">${prodPriceStr}</span>
          ${prodOrigStr ? `<span class="tt-chat-float-orig">${prodOrigStr}</span>` : ''}
        </div>
      </div>
      <button type="button" class="tt-chat-float-send" onclick="sendChatProductCard()">Enviar</button>
    </div>
  ` : '';

  chatContainer.innerHTML = `
    <style>
      @keyframes slideUpTTChat { from { transform: translateY(32px); opacity: 0.7; } to { transform: translateY(0); opacity: 1; } }
      .tt-chat-header {
        background: #ffffff;
        height: 54px;
        padding: 0 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #eeeeee;
        flex-shrink: 0;
      }
      .tt-chat-header-left {
        display: flex;
        align-items: center;
        gap: 14px;
        min-width: 0;
      }
      .tt-chat-icon-btn {
        background: none;
        border: none;
        padding: 4px;
        color: #161823;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
      }
      .tt-chat-store-title {
        font-size: 17px;
        font-weight: 700;
        color: #161823;
        letter-spacing: -0.2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .tt-chat-body {
        flex: 1;
        overflow-y: auto;
        padding: 14px 14px 12px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .tt-chat-time {
        text-align: center;
        font-size: 12px;
        color: #8a8b91;
        margin: 2px 0 6px;
      }
      .tt-chat-bot-row {
        display: flex;
        align-items: flex-start;
        gap: 8px;
      }
      .tt-chat-bot-avatar {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: none;
      }
      .tt-chat-bot-col {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
        flex: 1;
        min-width: 0;
      }
      .tt-chat-bubble-bot {
        background: #ffffff;
        color: #161823;
        border-radius: 12px;
        padding: 12px 14px;
        font-size: 15px;
        line-height: 1.38;
        max-width: 268px;
        word-wrap: break-word;
      }
      .tt-chat-bubble-user {
        background: #fe2c55;
        color: #ffffff;
        border-radius: 12px;
        padding: 11px 14px;
        font-size: 14.5px;
        line-height: 1.38;
        max-width: 80%;
        align-self: flex-end;
        word-wrap: break-word;
      }
      .tt-chat-faq-card {
        background: #ffffff;
        border-radius: 12px;
        width: 100%;
        max-width: 295px;
        overflow: hidden;
      }
      .tt-chat-faq-header {
        padding: 13px 14px;
        font-size: 15px;
        font-weight: 700;
        color: #161823;
        border-bottom: 1px solid #f0f0f0;
      }
      .tt-chat-faq-item {
        width: 100%;
        background: transparent;
        border: none;
        padding: 13px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        text-align: left;
        font-family: inherit;
        font-size: 14.5px;
        line-height: 1.3;
        color: #161823;
        cursor: pointer;
      }
      .tt-chat-faq-item:active {
        background: #f8f8f8;
      }
      .tt-chat-bot-caption {
        font-size: 12px;
        color: #9c9da3;
        padding-left: 2px;
      }
      .tt-chat-product-float {
        position: relative;
        margin: 6px 12px 10px;
        background: #ffffff;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }
      .tt-chat-float-close {
        position: absolute;
        top: 8px;
        right: 8px;
        background: none;
        border: none;
        padding: 2px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .tt-chat-float-img {
        width: 68px;
        height: 68px;
        border-radius: 8px;
        object-fit: cover;
        flex-shrink: 0;
        background: #f5f5f5;
      }
      .tt-chat-float-info {
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 3px;
        padding-right: 14px;
      }
      .tt-chat-float-title {
        font-size: 14px;
        font-weight: 600;
        color: #161823;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .tt-chat-float-sold {
        font-size: 12px;
        color: #8a8b91;
      }
      .tt-chat-float-price-row {
        display: flex;
        align-items: baseline;
        gap: 6px;
        margin-top: 2px;
      }
      .tt-chat-float-price {
        font-size: 15px;
        font-weight: 700;
        color: #161823;
      }
      .tt-chat-float-orig {
        font-size: 12px;
        color: #9c9da3;
        text-decoration: line-through;
      }
      .tt-chat-float-send {
        background: #fe2c55;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 600;
        font-family: inherit;
        cursor: pointer;
        align-self: flex-end;
        flex-shrink: 0;
      }
      .tt-chat-input-bar {
        background: #ffffff;
        padding: 8px 12px max(10px, env(safe-area-inset-bottom));
        border-top: 1px solid #efefef;
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
      }
      .tt-chat-input {
        flex: 1;
        height: 40px;
        background: #f3f3f4;
        border: none;
        border-radius: 20px;
        padding: 0 15px;
        font-size: 14.5px;
        color: #161823;
        outline: none;
        font-family: inherit;
      }
      .tt-chat-input::placeholder {
        color: #8a8b91;
      }
      .tt-chat-bar-icon {
        background: none;
        border: none;
        padding: 4px;
        color: #161823;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }
      .tt-chat-sent-product {
        background: #ffffff;
        border-radius: 12px;
        padding: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
        max-width: 82%;
        align-self: flex-end;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
      }
      .tt-chat-sent-product img {
        width: 52px;
        height: 52px;
        border-radius: 6px;
        object-fit: cover;
        flex-shrink: 0;
      }
    </style>

    <div class="tt-chat-header">
      <div class="tt-chat-header-left">
        <button type="button" class="tt-chat-icon-btn" aria-label="Voltar" onclick="closeSmartChat()">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
        </button>
        <div class="tt-chat-store-title">Stone Shop</div>
      </div>
      <button type="button" class="tt-chat-icon-btn" aria-label="Mais opções" onclick="sendChatSuggestion('Quero falar com um atendente', 'atendente')">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="#161823"><circle cx="5" cy="12" r="1.8"/><circle cx="12" cy="12" r="1.8"/><circle cx="19" cy="12" r="1.8"/></svg>
      </button>
    </div>

    <div class="tt-chat-body" id="chat-messages-box">
      <div class="tt-chat-time">${timeStr}</div>
      <div class="tt-chat-bot-row">
        ${botAvatarSvg}
        <div class="tt-chat-bot-col">
          <div class="tt-chat-bubble-bot">Agradecemos por entrar em contato. Como posso ajudar hoje?</div>
          <div class="tt-chat-faq-card">
            <div class="tt-chat-faq-header">Como posso ajudar você hoje?</div>
            <button type="button" class="tt-chat-faq-item" onclick="sendChatSuggestion('Como posso rastrear meu pacote?', 'rastrear')">
              <span>Como posso rastrear meu pacote?</span>${chevronSvg}
            </button>
            <button type="button" class="tt-chat-faq-item" onclick="sendChatSuggestion('Ainda não recebi o produto.', 'nao_recebi')">
              <span>Ainda não recebi o produto.</span>${chevronSvg}
            </button>
            <button type="button" class="tt-chat-faq-item" onclick="sendChatSuggestion('Quando vou receber as mercadorias?', 'quando_receber')">
              <span>Quando vou receber as mercadorias?</span>${chevronSvg}
            </button>
            <button type="button" class="tt-chat-faq-item" onclick="sendChatSuggestion('Quando meu pedido chegará?', 'quando_chegara')">
              <span>Quando meu pedido chegará?</span>${chevronSvg}
            </button>
          </div>
          <div class="tt-chat-bot-caption">Enviado por chatbot</div>
        </div>
      </div>
    </div>

    ${floatingProductCardHtml}

    <div class="tt-chat-input-bar">
      <input type="text" class="tt-chat-input" id="chat-input-text" placeholder="Enviar mensagem..." onkeypress="handleChatEnter(event)">
      <button type="button" class="tt-chat-bar-icon" aria-label="Emoji" onclick="document.getElementById('chat-input-text')?.focus()">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="9.7" stroke="#161823" stroke-width="1.85"></circle>
          <ellipse cx="8.9" cy="10.1" rx="1.35" ry="1.85" fill="#161823"></ellipse>
          <ellipse cx="15.1" cy="10.1" rx="1.35" ry="1.85" fill="#161823"></ellipse>
          <path d="M8 13.7H16C15.8 16.4 14.1 17.9 12 17.9C9.9 17.9 8.2 16.4 8 13.7Z" fill="#161823"></path>
        </svg>
      </button>
      <button type="button" class="tt-chat-bar-icon" aria-label="Enviar ou mais" onclick="sendChatManual()">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="1.85" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.7"/><line x1="12" y1="7.8" x2="12" y2="16.2"/><line x1="7.8" y1="12" x2="16.2" y2="12"/></svg>
      </button>
    </div>
  `;

  overlay.appendChild(chatContainer);
  document.body.appendChild(overlay);
  document.body.style.overflow = 'hidden';

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeSmartChat();
  });

  window.closeSmartChat = function () {
    overlay.style.display = 'none';
    document.body.style.overflow = '';
  };

  function appendUserMsg(texto) {
    const box = document.getElementById('chat-messages-box');
    if (!box) return;
    const div = document.createElement('div');
    div.className = 'tt-chat-bubble-user';
    div.textContent = texto;
    box.appendChild(div);
    box.scrollTo({ top: box.scrollHeight, behavior: 'smooth' });
  }

  function appendBotMsg(htmlTexto) {
    const box = document.getElementById('chat-messages-box');
    if (!box) return;
    const row = document.createElement('div');
    row.className = 'tt-chat-bot-row';
    row.innerHTML = `${botAvatarSvg}<div class="tt-chat-bot-col"><div class="tt-chat-bubble-bot">${htmlTexto}</div><div class="tt-chat-bot-caption">Enviado por chatbot</div></div>`;
    box.appendChild(row);
    box.scrollTo({ top: box.scrollHeight, behavior: 'smooth' });
  }

  window.sendChatProductCard = function () {
    const box = document.getElementById('chat-messages-box');
    if (!box || !hasProd) return;
    const card = document.createElement('div');
    card.className = 'tt-chat-sent-product';
    card.innerHTML = `<img src="${prodImg}" alt=""><div><div style="font-size:13px;font-weight:600;color:#161823;line-height:1.25;">${prodName.slice(0, 48)}</div><div style="font-size:14px;font-weight:700;color:#fe2c55;margin-top:3px;">${prodPriceStr}</div></div>`;
    box.appendChild(card);
    document.getElementById('tt-chat-product-float')?.remove();
    box.scrollTo({ top: box.scrollHeight, behavior: 'smooth' });
    setTimeout(() => {
      appendBotMsg(`Sim! O produto <strong>${prodName}</strong> está disponível em nosso estoque com <strong>Frete grátis</strong> e envio imediato após a confirmação do pagamento.`);
    }, 550);
  };

  window.sendChatSuggestion = function (texto, tipo) {
    appendUserMsg(texto);
    let resposta = 'Obrigado pelo contato! Nossa equipe da <strong>Stone Shop</strong> está à disposição. Como posso te ajudar com seu pedido?';
    if (tipo === 'rastrear') {
      resposta = 'Assim que o pedido for despachado, você recebe o <strong>código de rastreamento oficial</strong> automaticamente no seu e-mail e WhatsApp cadastrados no checkout.';
    } else if (tipo === 'nao_recebi') {
      resposta = 'Fique tranquilo! Todos os pedidos possuem <strong>Proteção do cliente</strong> com garantia de entrega ou reembolso integral. Nos informe o número do seu pedido ou CPF para verificarmos agora mesmo.';
    } else if (tipo === 'quando_receber' || tipo === 'quando_chegara' || tipo === 'prazo') {
      const prazoTxt = document.getElementById('frete-prazo-dinamico')?.textContent?.trim() || '3 a 7 dias úteis';
      resposta = `O envio é realizado em até 24h úteis após a aprovação do pagamento. Previsão estimada: <strong>${prazoTxt}</strong>, com frete grátis para todo o Brasil.`;
    } else if (tipo === 'atendente') {
      resposta = 'Nosso atendimento humano está disponível de segunda a sábado, das 08h às 20h. Pode enviar sua dúvida aqui mesmo que já te respondemos!';
    }
    setTimeout(() => appendBotMsg(resposta), 550);
  };

  window.sendChatManual = function () {
    const input = document.getElementById('chat-input-text');
    if (!input) return;
    const txt = input.value.trim();
    if (!txt) { input.focus(); return; }
    appendUserMsg(txt);
    input.value = '';
    setTimeout(() => {
      const lower = txt.toLowerCase();
      let resposta = 'Recebemos sua mensagem! Um atendente da <strong>Stone Shop</strong> já foi acionado e vai te responder por aqui em instantes.';
      if (lower.includes('prazo') || lower.includes('chega') || lower.includes('demora') || lower.includes('entrega')) {
        const prazoTxt = document.getElementById('frete-prazo-dinamico')?.textContent?.trim() || '3 a 7 dias úteis';
        resposta = `A previsão de entrega para a sua região é <strong>${prazoTxt}</strong>, com código de rastreamento completo.`;
      } else if (lower.includes('frete') || lower.includes('envio')) {
        resposta = 'O envio hoje está com <strong>Frete grátis</strong> para todo o Brasil na promoção Black Friday!';
      } else if (lower.includes('pix') || lower.includes('pagar') || lower.includes('cartao')) {
        resposta = 'Aceitamos <strong>PIX</strong> com aprovação instantânea e envio prioritário no mesmo dia.';
      } else if (lower.includes('rastre')) {
        resposta = 'Seu código de rastreamento é enviado por e-mail e WhatsApp logo após a postagem do pedido.';
      }
      appendBotMsg(resposta);
    }, 600);
  };

  window.handleChatEnter = function (e) {
    if (e.key === 'Enter') sendChatManual();
  };
}

// Configura botões de chat na página para abrir o modal de chat inteligente
function initChatButtons() {
  // Intercepta clique no botão de mensagem da store-section (index.html)
  const storeMsgBtn = document.querySelector('.store-message-btn');
  if (storeMsgBtn) {
    storeMsgBtn.removeAttribute('onclick');
    storeMsgBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openSmartChat();
    });
  }

  // Intercepta botões de chat inferiores das páginas de produtos
  const productChatBtn = document.querySelector('button[aria-label="Chat"]');
  if (productChatBtn) {
    productChatBtn.removeAttribute('onclick');
    productChatBtn.addEventListener('click', (e) => {
      e.preventDefault();
      openSmartChat();
    });
  }
}

// ===== INICIALIZAÇÃO GERAL =====

// ===== SISTEMA GLOBAL DE LOADING OFICIAL TIKTOK =====
// - Normal: Bolinhas orbitando limpas SEM TEXTO e SEM QUADRADO (usado em compras e navegação)
// - HUD Quadrado Preto: Modal escuro 95x95px com bolinhas e texto (usado exclusivamente no PIX)
window.ensureTikTokLoaderStyles = function () {
  if (document.getElementById('tiktok-loader-style-tag')) return;
  const style = document.createElement('style');
  style.id = 'tiktok-loader-style-tag';
  style.textContent = `
    :root {
      --tiktok-pink: #FE2C55;
      --tiktok-cyan: #25F4EE;
    }
    .tiktok-loader-overlay, #tiktok-global-loader {
      position: fixed !important;
      top: 0 !important;
      left: 0 !important;
      width: 100vw !important;
      height: 100vh !important;
      z-index: 9999999 !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      pointer-events: auto !important;
      margin: 0 !important;
      padding: 0 !important;
      box-sizing: border-box !important;
    }
    .tiktok-balls {
      position: relative;
      width: 34px;
      height: 16px;
      display: inline-block;
      vertical-align: middle;
      box-sizing: border-box;
    }
    .tiktok-balls .ball {
      position: absolute;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      top: 0;
      box-sizing: border-box;
    }
    .tiktok-balls .ball-cyan {
      background-color: #25F4EE;
      left: 0;
      animation: ballCyan 0.91s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
    }
    .tiktok-balls .ball-pink {
      background-color: #FE2C55;
      right: 0;
      animation: ballPink 0.91s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
    }
    @keyframes ballCyan {
      0% { transform: translateX(0) scale(1); z-index: 2; }
      50% { transform: translateX(18px) scale(1.1); z-index: 2; }
      50.01% { z-index: 1; }
      100% { transform: translateX(0) scale(0.9); z-index: 1; }
    }
    @keyframes ballPink {
      0% { transform: translateX(0) scale(0.9); z-index: 1; }
      50% { transform: translateX(-18px) scale(0.9); z-index: 1; }
      50.01% { z-index: 2; }
      100% { transform: translateX(0) scale(1.1); z-index: 2; }
    }
    .tiktok-balls.tiktok-balls-lg {
      width: 24px;
      height: 11px;
    }
    .tiktok-balls.tiktok-balls-lg .ball {
      width: 11px;
      height: 11px;
    }
    .tiktok-balls.tiktok-balls-lg .ball-cyan {
      background-color: #25F4EE;
      animation-name: ballCyanLg;
    }
    .tiktok-balls.tiktok-balls-lg .ball-pink {
      background-color: #FE2C55;
      animation-name: ballPinkLg;
    }
    @keyframes ballCyanLg {
      0% { transform: translateX(0) scale(0.96); z-index: 1; }
      50% { transform: translateX(13px) scale(1.06); z-index: 2; }
      50.01% { z-index: 2; }
      100% { transform: translateX(0) scale(0.96); z-index: 1; }
    }
    @keyframes ballPinkLg {
      0% { transform: translateX(0) scale(1.06); z-index: 2; }
      50% { transform: translateX(-13px) scale(0.92); z-index: 1; }
      50.01% { z-index: 1; }
      100% { transform: translateX(0) scale(1.06); z-index: 2; }
    }

    /* O QUADRADO PRETO HUD OFICIAL (USADO SOMENTE NA GERAÇÃO DO PIX) */
    
    @keyframes ttHudScaleIn {
      from { opacity: 0; transform: scale(0.9); }
      to { opacity: 1; transform: scale(1); }
    }
    .hud-box, .tiktok-hud-box {
      width: 122px !important;
      height: 105px !important;
      min-width: 122px !important;
      min-height: 105px !important;
      max-width: 122px !important;
      max-height: 105px !important;
      background: rgba(46, 46, 46, 0.93) !important;
      border: none !important;
      border-radius: 16px !important;
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      gap: 8px !important;
      padding: 16px 8px 14px 8px !important;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.22) !important;
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
      animation: ttHudScaleIn 0.16s cubic-bezier(0.16, 1, 0.3, 1) !important;
      box-sizing: border-box !important;
    }
    .hud-box .tiktok-balls, .tiktok-hud-box .tiktok-balls {
      position: relative !important;
      width: 28px !important;
      height: 13px !important;
      display: inline-block !important;
      box-sizing: border-box !important;
    }
    .hud-box .tiktok-balls .ball, .tiktok-hud-box .tiktok-balls .ball {
      position: absolute !important;
      width: 13px !important;
      height: 13px !important;
      border-radius: 50% !important;
      top: 0 !important;
      box-sizing: border-box !important;
    }
    .hud-box .tiktok-balls .ball-cyan, .tiktok-hud-box .tiktok-balls .ball-cyan {
      background-color: #25F4EE !important;
      left: 0 !important;
      animation: ballCyanHud 0.91s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite !important;
    }
    .hud-box .tiktok-balls .ball-pink, .tiktok-hud-box .tiktok-balls .ball-pink {
      background-color: #FE2C55 !important;
      right: 0 !important;
      animation: ballPinkHud 0.91s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite !important;
    }
    @keyframes ballCyanHud {
      0% { transform: translateX(0) scale(1); z-index: 2; }
      50% { transform: translateX(15px) scale(1.1); z-index: 2; }
      50.01% { z-index: 1; }
      100% { transform: translateX(0) scale(0.9); z-index: 1; }
    }
    @keyframes ballPinkHud {
      0% { transform: translateX(0) scale(0.9); z-index: 1; }
      50% { transform: translateX(-15px) scale(0.9); z-index: 1; }
      50.01% { z-index: 2; }
      100% { transform: translateX(0) scale(1.1); z-index: 2; }
    }
    .hud-box span, .tiktok-hud-box span {
      font-size: 12px !important;
      color: #ffffff !important;
      font-weight: 500 !important;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
      letter-spacing: -0.15px !important;
      white-space: nowrap !important;
      margin: 0 !important;
      margin-top: 2px !important;
    }
    
    .tiktok-loader-overlay.type-hud {
      background: transparent !important;
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
    }
    .tiktok-loader-overlay.type-normal {
      background: rgba(0, 0, 0, 0.50) !important;
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
    }
  `;
  document.head.appendChild(style);
};

// 1. CARREGAMENTO NORMAL (BOLINHAS PURAS SEM TEXTO E SEM QUADRADO)
window.showTikTokLoader = function (options = {}) {
  window.ensureTikTokLoaderStyles();
  const isHud = (options && options.type === 'hud');

  let overlay = document.getElementById('tiktok-global-loader');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'tiktok-global-loader';
    document.body.appendChild(overlay);
  }

  overlay.className = 'tiktok-loader-overlay ' + (isHud ? 'type-hud' : 'type-normal');
  overlay.style.position = 'fixed';
  overlay.style.top = '0';
  overlay.style.left = '0';
  overlay.style.width = '100vw';
  overlay.style.height = '100vh';
  overlay.style.zIndex = '9999999';
  overlay.style.display = 'flex';
  overlay.style.alignItems = 'center';
  overlay.style.justifyContent = 'center';
  overlay.style.pointerEvents = 'auto';
  overlay.style.opacity = '1';
  if (isHud) {
    overlay.style.background = 'transparent';
    overlay.style.backdropFilter = 'none';
    overlay.style.webkitBackdropFilter = 'none';
  } else {
    overlay.style.background = 'rgba(0, 0, 0, 0.50)';
    overlay.style.backdropFilter = 'none';
    overlay.style.webkitBackdropFilter = 'none';
  }

  if (isHud) {
    const text = (options && options.text) ? options.text : 'Gerando PIX...';
    overlay.innerHTML = `
      <div class="tiktok-hud-box">
        <div class="tiktok-balls">
          <div class="ball ball-cyan"></div>
          <div class="ball ball-pink"></div>
        </div>
        <span>${text}</span>
      </div>
    `;
  } else {
    // Normal: estritamente apenas as bolinhas sem texto
    overlay.innerHTML = `
      <div class="tiktok-balls tiktok-balls-lg">
        <div class="ball ball-cyan"></div>
        <div class="ball ball-pink"></div>
      </div>
    `;
  }

  // Limpa qualquer timeout pendente para evitar vazamentos e conflitos
  if (window.__ttLoaderTimer) {
    clearTimeout(window.__ttLoaderTimer);
    window.__ttLoaderTimer = null;
  }

  // BLINDAGEM CONTRA CONGELAMENTO / TRAVA:
  // SEMPRE aplica um timeout máximo de segurança (se a navegação falhar ou demorar, o loader se autodestrói)
  const safetyDuration = (options && typeof options.duration === 'number' && options.duration > 0)
    ? options.duration
    : 2200;

  window.__ttLoaderTimer = setTimeout(() => {
    window.hideTikTokLoader();
  }, safetyDuration);

  // CLIQUE NO OVERLAY DESBLOQUEIA A TELA:
  // Se o usuário tocar na tela enquanto o loader estiver visível, dispensa na hora!
    // CLIQUE NO OVERLAY DESBLOQUEIA A TELA (APENAS PARA O LOADER NORMAL, NUNCA PARA O HUD):
  if (!isHud) {
    overlay.onclick = function (e) {
      e.stopPropagation();
      window.hideTikTokLoader();
    };
  } else {
    overlay.onclick = null;
  }
};

window.hideTikTokLoader = function () {
  if (window.__ttLoaderTimer) {
    clearTimeout(window.__ttLoaderTimer);
    window.__ttLoaderTimer = null;
  }
  const overlay = document.getElementById('tiktok-global-loader');
  if (overlay) {
    overlay.style.opacity = '0';
    setTimeout(() => {
      if (overlay && overlay.parentNode) {
        overlay.parentNode.removeChild(overlay);
      }
    }, 150);
  }
};

// 2. QUADRADO PRETO HUD (USADO EXCLUSIVAMENTE NA GERAÇÃO DO PIX)
window.showTikTokHUD = function (text = 'Gerando PIX...', duration = 0) {
  window.showTikTokLoader({ type: 'hud', text, duration });
};

window.showTikTokNormal = function (duration = 0) {
  window.showTikTokLoader({ type: 'normal', duration });
};


function initStoneShopApp() {
  // O carregamento inicial instantâneo é feito via inline spinner crítico no topo do <body>

  // Função para renderizar e injetar o Widget da Loja (Stone Shop) acima de avaliações nas páginas de produtos
  function renderStoreWidget() {
    // Tolerância zero a repetição: remove qualquer card de loja estático anterior ou duplicata
    document.querySelectorAll('.store-card-stone').forEach(el => el.remove());
    const existingWidgets = document.querySelectorAll('.store-widget-section');
    if (existingWidgets.length > 0) {
      existingWidgets.forEach((w, idx) => { if (idx > 0) w.remove(); });
      return;
    }
    if (document.querySelector('.seller-profile-card')) return;

    const reviewsSection = document.querySelector('.reviews-section');
    if (!reviewsSection) return;
    if (typeof CATALOGO_PRODUTOS === 'undefined') return;

    // Pega o ID do produto atual
    const idAtual = typeof PRODUTO_ATUAL !== 'undefined' ? PRODUTO_ATUAL.id : -1;

    // Filtra e pega 6 produtos aleatórios para o carrossel "Mais desta loja"
    const outros = CATALOGO_PRODUTOS.filter(p => p.id !== idAtual);
    for (let i = outros.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [outros[i], outros[j]] = [outros[j], outros[i]];
    }
    const selecionados = outros.slice(0, 6);

    const couponHtml = `
      <div class="store-widget-coupon-card" style="width:104px; min-width:104px; height:154px; background:#fff5f0; border-radius:8px; display:flex; flex-direction:column; justify-content:space-between; padding:12px 8px 10px 8px; box-sizing:border-box; flex-shrink:0; text-align:center;">
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; flex:1;">
          <svg viewBox="0 0 24 24" width="16" height="18" fill="#ff6422" style="margin-bottom:6px; flex-shrink:0;">
            <path d="M13 2L3 14h8l-1 8 11-12h-8l1-8z"></path>
          </svg>
          <div style="font-size:13px; font-weight:800; color:#eb571e; line-height:1.25; letter-spacing:-0.2px;">
            Até 74% de<br>desconto
          </div>
        </div>
        <div style="border-top:1px dashed #ffd5c4; margin:6px 2px 5px 2px;"></div>
        <div style="font-size:10.5px; color:#8c827a; font-weight:500; white-space:nowrap;">
          Termina em 1 dia
        </div>
      </div>
    `;

    let itemsHtml = '';
    selecionados.forEach(p => {
      const precoFmt = 'R$ ' + parseFloat(p.preco).toFixed(2).replace('.', ',');
      const descVal = p.desc || (p.precoOrig ? Math.round((1 - p.preco / parseFloat(p.precoOrig.replace(',', '.'))) * 100) : 55);
      let prodImg = p.img || '../logo.png';
      if (prodImg.startsWith('img/')) prodImg = '../' + prodImg;
      itemsHtml += `
        <a class="store-widget-product-card" href="produto-${p.id}.html" style="text-decoration:none; display:flex; flex-direction:column; width:96px; flex-shrink:0; background:#fff; border-radius:8px; overflow:hidden;">
          <img class="store-widget-product-img" src="${prodImg}" alt="${p.nome}" onerror="this.onerror=null;this.src='../logo.png';" style="width:96px; height:104px; object-fit:cover; border-radius:8px;">
          <span class="store-widget-product-price" style="font-size:13px; font-weight:700; color:#111; text-align:left; margin-top:6px; display:block; line-height:1.2;">${precoFmt}</span>
          ${descVal > 0 ? `
          <div style="margin-top:3px; text-align:left;">
            <span class="store-widget-product-discount" style="background:#fff0f3; color:#fe2c55; font-size:10px; font-weight:700; padding:1.5px 5px; border-radius:2px; display:inline-block; line-height:1.2;">-${descVal}%</span>
          </div>` : ''}
        </a>
      `;
    });

    let widgetHtml = '';

    if (idAtual === 99) {
      widgetHtml = `
        <div class="store-widget-section" style="background:#fff; padding:16px; margin:0; border-top:8px solid #f5f5f5; border-bottom:8px solid #f5f5f5; box-sizing:border-box; font-family:-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;">
          <!-- Cabeçalho Flex da Loja -->
          <div class="store-widget-header" style="display:flex; align-items:center; gap:12px; margin-bottom:0px; width:100%; box-sizing:border-box;">
            <div class="store-widget-logo-wrapper" style="position:relative; width:50px; height:50px; border-radius:50%; border:1px solid #eee; overflow:hidden; flex-shrink:0; display:flex; align-items:center; justify-content:center; background:#222;">
              <img class="store-widget-logo" src="../pumalogo/image.png" onerror="this.src='https://via.placeholder.com/50'" alt="PUMA OFICIAL" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div class="store-widget-info" style="flex:1; min-width:0; display:flex; flex-direction:column; justify-content:center;">
              <div class="store-widget-name" style="font-size:15px; font-weight:700; color:#111; margin-bottom:2px; display:flex; align-items:center; gap:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                PUMA OFICIAL
                <svg viewBox="0 0 24 24" width="16" height="16" style="color:#0095f6; flex-shrink:0;" fill="currentColor">
                  <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <div class="store-widget-sales" style="font-size:12px; color:#888;">147200 vendidos</div>
            </div>
            <button class="store-widget-btn-visitar" onclick="openPumaStoreModal()" style="background:#f5f5f5; color:#111; font-size:13px; font-weight:700; padding:6px 16px; border-radius:20px; border:none; cursor:pointer; flex-shrink:0; outline:none; transition:background 0.2s;">Visitar</button>
          </div>
          
          <!-- Estatísticas da Loja -->
          <div class="store-widget-stats" style="display:flex; gap:16px; margin-top:10px; font-size:11.5px; color:#555;">
            <span><strong style="color:#111;">100%</strong> responde em 24 horas</span>
            <span><strong style="color:#111;">97%</strong> envios pontuais</span>
          </div>
        </div>
      `;
    } else {
      widgetHtml = `
        <div class="store-widget-section" style="background:#fff; padding:16px; margin:0; border-top:8px solid #f5f5f5; border-bottom:8px solid #f5f5f5; box-sizing:border-box; font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,Helvetica,Arial,sans-serif;">
          <!-- Cabeçalho Flex da Loja (100% Paridade com a Referência Oficial do TikTok Shop) -->
          <div class="store-widget-header" style="display:flex; align-items:center; gap:12px; margin-bottom:12px; width:100%; box-sizing:border-box;">
            <div class="store-widget-logo-wrapper" style="position:relative; width:48px; height:48px; border-radius:50%; border:1px solid #f0f0f0; overflow:hidden; flex-shrink:0; display:flex; align-items:center; justify-content:center; background:#f8f8f8;">
              <img class="store-widget-logo" src="../logo.png" onerror="this.src='https://via.placeholder.com/48'" alt="Stone Shop" style="width:100%; height:100%; object-fit:cover;">
            </div>
            <div class="store-widget-info" style="flex:1; min-width:0; display:flex; flex-direction:column; justify-content:center;">
              <div class="store-widget-name" style="font-size:16px; font-weight:600; color:#161823; letter-spacing:-0.2px; line-height:1.25; margin-bottom:2px; display:flex; align-items:center; gap:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                Stone Shop
                <svg viewBox="0 0 24 24" width="14" height="14" style="color:#0095f6; flex-shrink:0; vertical-align:middle;" fill="currentColor">
                  <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              ${window.location.pathname.includes('produto-101') ? `
              <div class="store-widget-pirelli" style="display:flex; align-items:center; gap:6px; margin-top:-1px; margin-bottom:-1px; padding:0;">
                <img src="../logopirelli/pirelli.png" alt="Pirelli" style="height:24px; object-fit:contain; vertical-align:middle; border-radius:2px;">
                <span style="color:#bbb; font-size:13px; line-height:1; font-weight:300;">|</span>
                <span style="font-size:11px; color:#555; font-weight:500; letter-spacing:0.1px;">Loja Credenciada</span>
              </div>` : ''}
              <div class="store-widget-sales" style="font-size:12.5px; color:#8a8b91; font-weight:400; margin-top:1px; line-height:1.2;">112240 vendidos</div>
            </div>
            <!-- Botão Visitar Idêntico à Imagem 2 (Flat, border-radius: 18px, font-weight: 600, sem sombra) -->
            <button class="store-widget-btn-visitar" onclick="window.location.href='../index.html'" style="background:#fe2c55; color:#fff; font-size:13.5px; font-weight:600; padding:6px 18px; height:34px; border-radius:18px; border:none; cursor:pointer; flex-shrink:0; outline:none; box-shadow:none; letter-spacing:-0.2px; display:inline-flex; align-items:center; justify-content:center; -webkit-tap-highlight-color:transparent;">Visitar</button>
          </div>
          
          <!-- Estatísticas da Loja (Números 95% e 99% em #161823 font-weight:700 e textos em #8a8b91 font-weight:400) -->
          <div class="store-widget-stats" style="display:flex; align-items:center; gap:20px; margin-bottom:14px; margin-top:2px;">
            <span style="display:inline-flex; align-items:baseline; font-size:12px; color:#8a8b91; font-weight:400; letter-spacing:-0.1px;">
              <strong style="color:#161823; font-weight:700; font-size:12.5px; margin-right:3px;">95%</strong>responde em 24 horas
            </span>
            <span style="display:inline-flex; align-items:baseline; font-size:12px; color:#8a8b91; font-weight:400; letter-spacing:-0.1px;">
              <strong style="color:#161823; font-weight:700; font-size:12.5px; margin-right:3px;">99%</strong>envios pontuais
            </span>
          </div>
          
          <!-- Título Mais Desta Loja -->
          <div class="store-widget-title-row" onclick="window.location.href='../index.html'" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; cursor:pointer;">
            <span class="store-widget-section-title" style="font-size:13.5px; font-weight:700; color:#222;">Mais desta loja</span>
            <span class="store-widget-arrow" style="font-size:16px; color:#888; line-height:1; font-weight:300;">›</span>
          </div>
          
          <!-- Carrossel horizontal de produtos -->
          <div class="store-widget-products-scroll" style="display:flex; gap:10px; overflow-x:auto; padding-bottom:4px; width:100%; -webkit-overflow-scrolling:touch; box-sizing:border-box; scrollbar-width:none;">
            ${couponHtml}
            ${itemsHtml}
          </div>
        </div>
      `;
    }

    reviewsSection.insertAdjacentHTML('afterend', widgetHtml);
  }
  function formatCentavosDecalque() {
    if (typeof PRODUTO_ATUAL === 'undefined') return;

    // Remove qualquer resquício de rótulo 'apartir'
    document.querySelectorAll('.price-label-apartir').forEach(el => el.remove());

    const priceEl = document.querySelector('.price-current');
    if (!priceEl) return;

    // Garante que o R$ esteja presente na price-row
    const priceRow = priceEl.closest('.price-row');
    if (priceRow && !priceRow.querySelector('.price-currency-sign')) {
      const sign = document.createElement('span');
      sign.className = 'price-currency-sign';
      sign.textContent = 'R$';
      priceRow.insertBefore(sign, priceEl);
    }

    // Se a caixinha branca estiver dentro da price-row, joga ela pra fora (filha direta de price-section)
    const priceSection = document.querySelector('.price-section');
    if (priceSection) {
      const nestedBadge = priceSection.querySelector('.price-row .discount-badge-white');
      if (nestedBadge) {
        priceSection.insertBefore(nestedBadge, priceSection.firstChild);
      }
    }

    let priceText = priceEl.textContent.trim().replace(/R\$\s*/gi, '').trim();
    if (priceText.includes(',')) {
      const parts = priceText.split(',');
      priceEl.innerHTML = `${parts[0]}<span class="price-cents">,${parts[1]}</span>`;
    } else {
      priceEl.innerHTML = priceText;
    }
  }

  function renderProductInfoRows() {
    // Se o produto não possui variações declaradas no catálogo, cria dinamicamente uma variação de 1 opção única
    if (typeof PRODUTO_ATUAL !== 'undefined') {
      if (!PRODUTO_ATUAL.variacoes || Object.keys(PRODUTO_ATUAL.variacoes).length === 0) {
        let principalImg = PRODUTO_ATUAL.img || '';
        if (!principalImg && Array.isArray(PRODUTO_ATUAL.imagem)) {
          principalImg = PRODUTO_ATUAL.imagem.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || PRODUTO_ATUAL.imagem[0];
        } else if (!principalImg && typeof PRODUTO_ATUAL.imagem === 'string') {
          principalImg = PRODUTO_ATUAL.imagem;
        } else if (!principalImg && Array.isArray(PRODUTO_ATUAL.imagens)) {
          principalImg = PRODUTO_ATUAL.imagens.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || PRODUTO_ATUAL.imagens[0];
        }

        PRODUTO_ATUAL.variacoes = {
          "modelo": {
            "label": "OPÇÃO",
            "opcoes": [
              {
                "nome": "Padrão único",
                "imagem": principalImg
              }
            ]
          }
        };
      }
    }

    // Remove qualquer frete antigo residual ou proteção antiga para evitar duplicidade
    const oldFreteSections = document.querySelectorAll('.frete-row, .shipping-section, .delivery-info');
    oldFreteSections.forEach(el => el.remove());

    const oldProtectionSections = document.querySelectorAll('.protection-section');
    oldProtectionSections.forEach(el => el.remove());

    let container = document.querySelector('.product-info-rows');
    if (!container) {
      // Se não tem .product-info-rows, verifica se já existem linhas soltas no DOM para encapsular
      const existingItems = Array.from(document.querySelectorAll('.info-row-item, .info-row-item-protection, .info-row-envio, .info-row-opcoes'));
      if (existingItems.length > 0) {
        container = document.createElement('div');
        container.className = 'product-info-rows';
        container.style.cssText = 'border-top:1px solid #f5f5f5; border-bottom:1px solid #f5f5f5; margin-bottom:14px; background:#fff;';
        const parent = existingItems[0].parentNode;
        parent.insertBefore(container, existingItems[0]);
        existingItems.forEach(el => container.appendChild(el));
      }
    }

    // 1. Calcular data do prazo dinamicamente
    const obterDataPrazo = () => {
      const hoje = new Date();
      const minData = new Date(hoje);
      minData.setDate(hoje.getDate() + 5);
      const maxData = new Date(hoje);
      maxData.setDate(hoje.getDate() + 9);

      const diasSemana = ['dom.', 'seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.'];
      const meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
      const minSem = diasSemana[minData.getDay()];
      const minDia = minData.getDate();
      const minMes = meses[minData.getMonth()];
      const maxSem = diasSemana[maxData.getDay()];
      const maxDia = maxData.getDate();
      const maxMes = meses[maxData.getMonth()];

      return `Receba até ${minSem}, ${minDia} de ${minMes}–${maxSem}, ${maxDia} de ${maxMes}`;
    };

    // Se o contêiner já existir no DOM, atualiza a data do frete dinamicamente sem causar flicker
    if (container) {
      const freteRow = container.querySelector('.info-row-item');
      if (freteRow) {
        let titleEl = freteRow.querySelector('.frete-prazo-dinamico') || freteRow.querySelector('.info-row-subtitle') || freteRow.querySelector('.info-row-title');
        if (titleEl) {
          const novoPrazo = obterDataPrazo();
          if (titleEl.textContent.trim() !== novoPrazo) {
            titleEl.textContent = novoPrazo;
          }
        }
      }
    }

    // 2. Montar as miniaturas de opções disponíveis para TODOS os produtos
    let thumbnailsHtml = '';
    let opcoesCount = 1;
    const temVariacoes = typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.variacoes && Object.keys(PRODUTO_ATUAL.variacoes).length > 0;
    const imgsReais = [];

    if (temVariacoes) {
      // Coleta todas as opções de imagem das variações
      Object.values(PRODUTO_ATUAL.variacoes).forEach(v => {
        if (Array.isArray(v.opcoes)) {
          v.opcoes.forEach(o => {
            if (typeof o === 'object' && o.imagem && !imgsReais.includes(o.imagem)) {
              imgsReais.push(o.imagem);
            }
          });
        }
      });

      // Define a contagem baseando-se na quantidade de opções do primeiro grupo de variações
      const primeiraVar = Object.values(PRODUTO_ATUAL.variacoes)[0];
      if (primeiraVar && Array.isArray(primeiraVar.opcoes)) {
        opcoesCount = primeiraVar.opcoes.length;
      } else {
        opcoesCount = imgsReais.length || 1;
      }
    }

    // Se o produto não tem variações cadastradas ou as variações não têm fotos, extrai da galeria do produto
    if (imgsReais.length === 0 && typeof PRODUTO_ATUAL !== 'undefined') {
      if (Array.isArray(PRODUTO_ATUAL.imagens) && PRODUTO_ATUAL.imagens.length > 0) {
        PRODUTO_ATUAL.imagens.forEach(img => {
          if (img && !/\.(mp4|webm|ogg|mov)$/i.test(img) && !imgsReais.includes(img)) {
            imgsReais.push(img);
          }
        });
      }
      if (imgsReais.length === 0) {
        let principalImg = PRODUTO_ATUAL.img || '';
        if (principalImg && !/\.(mp4|webm|ogg|mov)$/i.test(principalImg)) {
          imgsReais.push(principalImg);
        }
      }
      if (!temVariacoes) {
        opcoesCount = imgsReais.length > 0 ? (imgsReais.length > 1 ? Math.min(imgsReais.length, 3) : 1) : 1;
      }
    }

    const fallback = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.img && !/\.(mp4|webm|ogg|mov)$/i.test(PRODUTO_ATUAL.img))
      ? PRODUTO_ATUAL.img
      : (typeof PRODUTO_ATUAL !== 'undefined' && Array.isArray(PRODUTO_ATUAL.imagens) ? PRODUTO_ATUAL.imagens.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) : '');

    imgsReais.slice(0, 4).forEach(img => {
      thumbnailsHtml += `<div style="width:34px; height:34px; border-radius:4px; border:1px solid #e8e8e8; background:#f0f0f0; overflow:hidden; flex-shrink:0;"><img src="${img}" style="width:100%; height:100%; object-fit:cover; display:block;" onerror="this.src='${fallback}'"></div>`;
    });

    const opcoesCountText = opcoesCount === 1 ? '1 opção disponível' : `${opcoesCount} opções disponíveis`;

    // Se o contêiner já existe (renderizado estaticamente no HTML), hidrata a linha de opções para 100% dos produtos
    if (container) {
      const opcoesRow = container.querySelector('.info-row-opcoes');
      if (opcoesRow) {
        let infoRowLeft = opcoesRow.querySelector('.info-row-left');
        let gridIcon = opcoesRow.querySelector('.info-row-icon');
        if (!gridIcon && infoRowLeft) {
          gridIcon = document.createElement('div');
          gridIcon.className = 'info-row-icon';
          gridIcon.style.cssText = 'display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-right:8px;';
          gridIcon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7" rx="1.5"></rect>
              <rect x="14" y="3" width="7" height="7" rx="1.5"></rect>
              <rect x="14" y="14" width="7" height="7" rx="1.5"></rect>
              <rect x="3" y="14" width="7" height="7" rx="1.5"></rect>
            </svg>`;
          infoRowLeft.insertBefore(gridIcon, infoRowLeft.firstChild);
        } else if (gridIcon) {
          gridIcon.style.display = 'flex';
          gridIcon.style.marginRight = '8px';
          gridIcon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7" rx="1.5"></rect>
              <rect x="14" y="3" width="7" height="7" rx="1.5"></rect>
              <rect x="14" y="14" width="7" height="7" rx="1.5"></rect>
              <rect x="3" y="14" width="7" height="7" rx="1.5"></rect>
            </svg>`;
        }
        opcoesRow.style.display = 'flex';
        const opcoesContent = opcoesRow.querySelector('.info-row-opcoes-content');
        if (opcoesContent) {
          const imgsExistentes = Array.from(opcoesContent.querySelectorAll('img'));
          const temAvatarFake = imgsExistentes.some(img => /avatar|review-user/i.test(img.src));
          const jaTemThumbs = imgsExistentes.length > 0 && !temAvatarFake;
          if ((!jaTemThumbs || temAvatarFake) && thumbnailsHtml) {
            opcoesContent.innerHTML = `
              <div style="display:flex; gap:4px; align-items:center;">${thumbnailsHtml}</div>
              <span class="info-row-title">${opcoesCountText}</span>
            `;
          } else if (jaTemThumbs) {
            const titleEl = opcoesContent.querySelector('.info-row-title');
            if (titleEl && opcoesCountText) titleEl.textContent = opcoesCountText;
          }
        }
      }
      return;
    }

    const newHtml = `
      <div class="product-info-rows" style="border-top:1px solid #f5f5f5; border-bottom:1px solid #f5f5f5; margin-bottom:14px; background:#fff;">
        <!-- Linha 1: Frete Grátis -->
        <div class="info-row-item">
          <div class="info-row-left">
            <div class="info-row-icon">
              <!-- Ícone clássico de caminhão original com listras de movimento -->
              <svg width="20" height="20" viewBox="0 -2 20 20" xmlns="http://www.w3.org/2000/svg">
                <g transform="translate(-2 -4)">
                  <path d="M9.17,17H13V6a1,1,0,0,0-1-1H5" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  <path d="M3,13v3a1,1,0,0,0,1,1h.87" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  <path d="M14.87,17H13V7h4.25a1,1,0,0,1,1,.73L19,10.5l1.24.31a1,1,0,0,1,.76,1V16a1,1,0,0,1-1,1h-.89" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                  <path d="M9,17a2,2,0,1,1-2-2A2,2,0,0,1,9,17Zm8-2a2,2,0,1,0,2,2A2,2,0,0,0,17,15ZM3,9H9" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                </g>
              </svg>
            </div>
            <div class="info-row-text-group">
              <div style="display:flex; align-items:center; gap:6px;">
                <span style="background:#e6f8f6; color:#00bfa5; font-size:10.5px; font-weight:700; padding:1px 4px; border-radius:2px;">Frete grátis</span>
                <span style="font-size:12px; color:#888; text-decoration:line-through;">R$ 15,60</span>
              </div>
              <span class="info-row-subtitle" style="font-size:13px; color:#333; font-weight:500;">${obterDataPrazo()}</span>
            </div>
          </div>
          <span class="info-row-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
        </div>

        <!-- Linha 2: Opções Disponíveis (Sempre visível com miniaturas e ícone 4 quadradinhos) -->
        <div class="info-row-item info-row-opcoes" onclick="handleAddToCart()">
          <div class="info-row-left">
            <div class="info-row-icon" style="display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-right:8px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7" rx="1.5"></rect>
                <rect x="14" y="3" width="7" height="7" rx="1.5"></rect>
                <rect x="14" y="14" width="7" height="7" rx="1.5"></rect>
                <rect x="3" y="14" width="7" height="7" rx="1.5"></rect>
              </svg>
            </div>
            <div class="info-row-opcoes-content" style="display:flex; align-items:center; gap:8px;">
              ${thumbnailsHtml ? `<div style="display:flex; gap:4px; align-items:center;">${thumbnailsHtml}</div>` : ''}
              <span class="info-row-title">${opcoesCountText}</span>
            </div>
          </div>
          <span class="info-row-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
        </div>

        <!-- Linha 4: Proteção do Cliente -->
        <div class="info-row-item-protection" onclick="window.openProtecaoModal()" style="background:#fff; padding:12px 16px; border-bottom:1px solid #f2f2f2; cursor:pointer;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <div class="info-row-left" style="display:flex; align-items:center; gap:7px;">
              <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#8B5E2B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <polyline points="9 12 11 14 15 10"></polyline>
              </svg>
              <span class="info-row-title" style="color:#8B5E2B; font-weight:500; font-size:13.5px;">Proteção do cliente</span>
            </div>
            <span class="info-row-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#aaa" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg></span>
          </div>
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px 12px; margin-top:8px; padding-left:24px; box-sizing:border-box;">
            <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Devolução gratuita</div>
            <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Garantia de pontualidade</div>
            <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Pagamento seguro</div>
            <div style="font-size:12px; color:#161823; display:flex; align-items:center; gap:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;"><svg width="11" height="11" viewBox="0 0 12 12" fill="none" style="flex-shrink:0;"><path d="M2 6.5L4.5 9L10 3" stroke="#8B5E2B" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/></svg> Reembolso se algo der errado</div>
          </div>
        </div>
      </div>
    `;

    // Blindagem soberana: Se o contêiner já existe ou se já foi inserido, NUNCA duplica
    if (document.querySelector('.product-info-rows') || document.querySelector('.info-row-item-protection')) {
      return;
    }

    const targetParent = document.querySelector('.product-info');
    const insertBeforeEl = document.querySelector('#creators-section, .reviews-section');
    if (targetParent && insertBeforeEl) {
      const div = document.createElement('div');
      div.innerHTML = newHtml;
      targetParent.insertBefore(div.firstElementChild, insertBeforeEl);
    }
  }

  function renderProductCupomHeader() {
    // Mantém o HTML oficial original estático da página sem sobrescrever dinamicamente
    return;
  }

  updateCartBadges();
  initSlider(document.querySelector('.image-slider'));
  initOfertaTimer();
  initPessoasOlhando();
  renderRelacionados();
  renderStoreWidget();
  initProductTabs();
  initSeguirBtn();
  initChatButtons();
  initReviewPagination();
  initAvatarColors();
  formatCentavosDecalque();
  renderProductInfoRows();
  renderProductCupomHeader();
  initScrollToTopBtn();        // Item 3: Botão flutuante de scroll ao topo (↑)
  formatCompactReviews();      // Item 11: Miniaturas compactas à direita com badge (+4 / +5)
  renderStoreReviewsFilter();  // Item 12: Filtros de avaliação da loja
  renderSobreEsteProdutoVideo(); // Item 14: Player de vídeo oficial "Sobre este produto"

  // Sobrescreve com atraso (delay) as ações de rodapé para anular qualquer script inline posterior do HTML do produto
  setTimeout(() => {
    if (typeof PRODUTO_ATUAL !== 'undefined') {
      normalizarVariacoesProduto(PRODUTO_ATUAL);
    }
    window.handleAddToCart = function () {
      if (typeof PRODUTO_ATUAL !== 'undefined') {
        normalizarVariacoesProduto(PRODUTO_ATUAL);
        handleAddToCartWithVariacoes(PRODUTO_ATUAL, false);
      }
    };
    window.handleBuyNow = function () {
      if (typeof PRODUTO_ATUAL !== 'undefined') {
        normalizarVariacoesProduto(PRODUTO_ATUAL);
        handleAddToCartWithVariacoes(PRODUTO_ATUAL, true);
      }
    };
  }, 250);

  // Efeito interativo do produto voando até o ícone do carrinho
  window.animateFlyToCart = function (startElement) {
    try {
      const cartIcon = document.querySelector('.header-icon-btn svg, .header-icon-btn');
      if (!cartIcon || typeof PRODUTO_ATUAL === 'undefined') return;

      // Obtém a imagem principal do produto de forma segura
      let imgUrl = PRODUTO_ATUAL.img || '';
      if (!imgUrl && Array.isArray(PRODUTO_ATUAL.imagem)) {
        imgUrl = PRODUTO_ATUAL.imagem.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || PRODUTO_ATUAL.imagem[0];
      } else if (!imgUrl && typeof PRODUTO_ATUAL.imagem === 'string') {
        imgUrl = PRODUTO_ATUAL.imagem;
      } else if (!imgUrl && Array.isArray(PRODUTO_ATUAL.imagens)) {
        imgUrl = PRODUTO_ATUAL.imagens.find(i => !/\.(mp4|webm|ogg|mov)$/i.test(i)) || PRODUTO_ATUAL.imagens[0];
      }

      if (!imgUrl) return;

      // Cria a imagem voadora
      const flyer = document.createElement('img');
      flyer.src = imgUrl;
      flyer.style.cssText = `
        position: fixed;
        z-index: 100000;
        width: 50px;
        height: 50px;
        object-fit: cover;
        border-radius: 50%;
        border: 2px solid #FF2B56;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        pointer-events: none;
        opacity: 1;
        transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
      `;

      // Posiciona o elemento no início
      let startX = window.innerWidth / 2 - 25;
      let startY = window.innerHeight - 80;
      if (startElement) {
        const rect = startElement.getBoundingClientRect();
        startX = rect.left + rect.width / 2 - 25;
        startY = rect.top + rect.height / 2 - 25;
      }

      flyer.style.left = startX + 'px';
      flyer.style.top = startY + 'px';
      document.body.appendChild(flyer);

      // Obtém as coordenadas do ícone do carrinho
      const cartRect = cartIcon.getBoundingClientRect();
      const endX = cartRect.left + cartRect.width / 2 - 10;
      const endY = cartRect.top + cartRect.height / 2 - 10;

      // Inicia a transição
      setTimeout(() => {
        flyer.style.left = endX + 'px';
        flyer.style.top = endY + 'px';
        flyer.style.transform = 'scale(0.1)';
        flyer.style.opacity = '0.3';
      }, 50);

      // Remove após o término e faz o pop no badge
      setTimeout(() => {
        flyer.remove();
        const badge = document.querySelector('.cart-badge');
        if (badge) {
          badge.classList.remove('pop');
          void badge.offsetWidth; // Força reflow
          badge.classList.add('pop');
        }
      }, 850);

      // Exibe o modal flutuante exatamente 1 segundo após a conclusão do vôo (850ms + 1000ms = 1850ms)
      setTimeout(() => {
        showPremiumSuccessModal();
      }, 1850);
    } catch (e) {
      console.error('Erro na animacao fly to cart:', e);
    }
  };

  // Modal flutuante quadrado premium (Shopee Style) para indicação de produto adicionado ao carrinho
  function showPremiumSuccessModal() {
    const existing = document.getElementById('premium-success-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'premium-success-modal';
    modal.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 140px;
      height: 120px;
      background: rgba(50, 50, 50, 0.95);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 100000;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      animation: zoomInSuccess 0.2s ease-out;
    `;

    // Adiciona a animação de zoom-in
    const styleId = 'success-modal-style';
    let style = document.getElementById(styleId);
    if (!style) {
      style = document.createElement('style');
      style.id = styleId;
      style.innerHTML = `
        @keyframes zoomInSuccess {
          from { transform: translate(-50%, -50%) scale(0.85); opacity: 0; }
          to { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }
      `;
      document.head.appendChild(style);
    }

    modal.innerHTML = `
      <div style="font-size: 34px; color: #ffffff; font-weight: 300; line-height: 1; margin-top: 4px;">✓</div>
      <div style="font-size: 13px; color: #ffffff; font-weight: 500; margin-top: 14px; text-align: center; font-family: -apple-system, BlinkMacSystemFont, sans-serif; padding: 0 8px; line-height: 1.25;">Adicionado ao carrinho</div>
    `;

    document.body.appendChild(modal);

    // Esconde e remove o modal após 1.5 segundos
    setTimeout(() => {
      modal.style.transition = 'opacity 0.2s ease';
      modal.style.opacity = '0';
      setTimeout(() => modal.remove(), 200);
    }, 1500);
  }
  window.showPremiumSuccessModal = showPremiumSuccessModal;

  // Modal flutuante da Proteção do Cliente para páginas de produtos
  window.openProtecaoModal = function () {
    const existingOverlay = document.getElementById('app-protecao-modal-overlay');
    const existingBox = document.getElementById('app-protecao-modal-box');
    if (existingOverlay) existingOverlay.remove();
    if (existingBox) existingBox.remove();

    const overlay = document.createElement('div');
    overlay.id = 'app-protecao-modal-overlay';
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.5); z-index: 100000;
      animation: fadeInOverlay 0.2s ease;
    `;
    overlay.onclick = window.closeProtecaoModal;

    const box = document.createElement('div');
    box.id = 'app-protecao-modal-box';
    box.style.cssText = `
      position: fixed; bottom: 0; left: 50%; transform: translateX(-50%);
      width: 100%; max-width: 480px; background: #fff;
      border-radius: 16px 16px 0 0; z-index: 100001;
      overflow: hidden; box-shadow: 0 -4px 16px rgba(0,0,0,0.15);
      animation: slideUpProtecao 0.3s ease-out;
      max-height: 85vh;
    `;

    const styleId = 'protecao-modal-animation-style';
    let style = document.getElementById(styleId);
    if (!style) {
      style = document.createElement('style');
      style.id = styleId;
      style.innerHTML = `
        @keyframes slideUpProtecao {
          from { transform: translate(-50%, 100%); }
          to { transform: translate(-50%, 0); }
        }
        @keyframes fadeInOverlay {
          from { opacity: 0; }
          to { opacity: 1; }
        }
      `;
      document.head.appendChild(style);
    }

    box.innerHTML = `
      <div style="position:relative; width:100%;">
        <!-- Área de clique invisível exatamente em cima do X desenhado na imagem -->
        <div onclick="window.closeProtecaoModal()" style="position:absolute; top:12px; right:12px; width:42px; height:42px; cursor:pointer; z-index:100002; background:transparent;"></div>
        
        <!-- Imagem de Proteção do Cliente Oficial -->
        <div style="width:100%; overflow-y:auto; max-height:85vh; -webkit-overflow-scrolling:touch; box-sizing:border-box;">
          <img src="../modalprotecaodocliente/IMG_5391.PNG" alt="Proteção do cliente" style="width:100%; display:block; height:auto; object-fit:contain; pointer-events:none;-webkit-touch-callout:none;user-select:none;">
        </div>
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(box);
  };

  window.closeProtecaoModal = function () {
    const overlay = document.getElementById('app-protecao-modal-overlay');
    const box = document.getElementById('app-protecao-modal-box');
    if (box) {
      box.style.transition = 'transform 0.2s ease-out';
      box.style.transform = 'translate(-50%, 100%)';
    }
    if (overlay) {
      overlay.style.transition = 'opacity 0.2s ease';
      overlay.style.opacity = '0';
    }
    setTimeout(() => {
      if (overlay) overlay.remove();
      if (box) box.remove();
    }, 200);
  };

  // Funções para abrir o modal profissional da PUMA OFICIAL
  window.openPumaStoreModal = function () {
    // Evita duplicados
    if (document.getElementById('puma-modal-overlay')) return;

    const overlay = document.createElement('div');
    overlay.id = 'puma-modal-overlay';
    overlay.style.cssText = `
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0,0,0,0.6); z-index: 100000;
      display: flex; align-items: flex-end; justify-content: center;
      opacity: 0; transition: opacity 0.3s ease;
    `;

    const box = document.createElement('div');
    box.id = 'puma-modal-box';
    box.style.cssText = `
      position: fixed; bottom: 0; left: 50%; transform: translate(-50%, 100%);
      width: 100%; max-width: 480px; background: #fff;
      border-radius: 20px 20px 0 0; z-index: 100001;
      overflow: hidden; box-shadow: 0 -4px 20px rgba(0,0,0,0.2);
      transition: transform 0.3s cubic-bezier(0.1, 0.76, 0.55, 0.94);
      font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
      box-sizing: border-box; padding: 24px 20px;
    `;

    box.innerHTML = `
      <div style="display:flex; flex-direction:column; align-items:center; text-align:center;">
        <!-- Ícone / Logo da Puma Oficial em destaque circular -->
        <div style="width: 80px; height: 80px; border-radius: 50%; overflow: hidden; border: 2px solid #222; display: flex; align-items: center; justify-content: center; background: #222; margin-bottom: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); box-sizing: border-box; padding: 0;">
          <img src="../pumalogo/image.png" alt="Puma Logo" style="width: 100%; height: 100%; object-fit: cover; transform: scale(1.1); display: block;">
        </div>

        <div style="font-size: 18px; font-weight: 800; color: #111; display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
          PUMA OFICIAL
          <svg viewBox="0 0 24 24" width="18" height="18" style="color:#0095f6; flex-shrink:0;" fill="currentColor">
            <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        </div>
        
        <div style="font-size: 12px; color: #888; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 16px;">
          Parceiro Oficial Autorizado
        </div>

        <div style="font-size: 14px; color: #444; line-height: 1.6; margin-bottom: 22px; padding: 0 10px;">
          Esta é a página exclusiva do produto oficial <strong>Kit Compre 1 Leve 2 Portugal 2026</strong>. Como parceiro oficial da marca, oferecemos garantia de autenticidade, suporte premium e frete prioritário grátis para todo o Brasil diretamente dos centros de distribuição autorizados.
        </div>

        <!-- Estatísticas no Modal -->
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; width: 100%; border-top: 1px solid #eee; border-bottom: 1px solid #eee; padding: 16px 0; margin-bottom: 24px;">
          <div>
            <div style="font-size: 16px; font-weight: 800; color: #111;">147.2K</div>
            <div style="font-size: 10.5px; color: #888; margin-top: 2px;">Vendas Totais</div>
          </div>
          <div>
            <div style="font-size: 16px; font-weight: 800; color: #4caf50;">100%</div>
            <div style="font-size: 10.5px; color: #888; margin-top: 2px;">Suporte 24h</div>
          </div>
          <div>
            <div style="font-size: 16px; font-weight: 800; color: #111;">97%</div>
            <div style="font-size: 10.5px; color: #888; margin-top: 2px;">Envio Imediato</div>
          </div>
        </div>

        <button onclick="window.closePumaStoreModal()" style="width: 100%; background: #111; color: #fff; font-size: 15px; font-weight: 700; padding: 14px; border: none; border-radius: 25px; cursor: pointer; outline: none; transition: background 0.2s;">
          Entendido
        </button>
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(box);

    // Ativa as transições após o append
    setTimeout(() => {
      overlay.style.opacity = '1';
      box.style.transform = 'translate(-50%, 0)';
    }, 50);

    // Fecha ao clicar no overlay
    overlay.addEventListener('click', () => window.closePumaStoreModal());
  };

  window.closePumaStoreModal = function () {
    const overlay = document.getElementById('puma-modal-overlay');
    const box = document.getElementById('puma-modal-box');
    if (box) {
      box.style.transform = 'translate(-50%, 100%)';
    }
    if (overlay) {
      overlay.style.opacity = '0';
    }
    setTimeout(() => {
      if (overlay) overlay.remove();
      if (box) box.remove();
    }, 300);
  };
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initStoneShopApp);
} else {
  initStoneShopApp();
}

// Disparador global para abrir o modal de variacao de qualquer produto se vier ?openModal=1 na URL
document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const isFromStoreList = urlParams.get('fromStoreList') === '1';

  // Se veio da listagem da loja (via iframe), intercepta redirecionamentos e acoes locais
  if (isFromStoreList) {
    // Intercepta adicionais de carrinho
    const originalAddToCart = window.addToCart;
    window.addToCart = function (produto, qty = 1) {
      if (window.parent && typeof window.parent.addToCart === 'function') {
        return window.parent.addToCart(produto, qty);
      }

      const cart = getCart();
      const idx = cart.findIndex(i => Number(i.id) === Number(produto.id) && i.variacao === produto.variacao);
      if (idx >= 0) {
        cart[idx].qty += qty;
      } else {
        let cleanImg = produto.img || '';
        if (produto.imagens && produto.imagens.length) {
          const primeiraImg = produto.imagens.find(i => !i.endsWith('.mp4'));
          cleanImg = primeiraImg || produto.imagens[0];
        }
        if (cleanImg.startsWith('../')) {
          cleanImg = cleanImg.substring(3);
        }
        cart.push({
          id: produto.id,
          nome: produto.nome,
          preco: produto.preco,
          precoOrig: produto.precoOrig || (typeof CATALOGO_PRODUTOS !== 'undefined' && CATALOGO_PRODUTOS.find(p => p.id == produto.id) ? CATALOGO_PRODUTOS.find(p => p.id == produto.id).precoOrig : null) || (produto.preco * 1.5),
          img: cleanImg,
          qty: qty,
          variacao: produto.variacao || null
        });
      }
      saveCart(cart);
      updateCartBadges();
      return cart;
    };

    // Sobrescreve handleBuyNow e handleAddToCart especificos para apenas adicionar e fechar sem navegar
    window.handleAddToCart = function () {
      if (typeof PRODUTO_ATUAL !== 'undefined') {
        addToCart(PRODUTO_ATUAL);
        showToast('✅ Adicionado ao carrinho!');
        setTimeout(() => {
          try {
            const tempModal = document.querySelector('.modal-overlay') || document.querySelector('.custom-modal-overlay') || document.getElementById('custom-var-modal');
            if (tempModal) tempModal.style.display = 'none';
          } catch (e) { }
        }, 800);
      }
    };

    window.handleBuyNow = function () {
      if (typeof PRODUTO_ATUAL !== 'undefined') {
        addToCart(PRODUTO_ATUAL);
        setTimeout(() => {
          try {
            const tempModal = document.querySelector('.modal-overlay') || document.querySelector('.custom-modal-overlay') || document.getElementById('custom-var-modal');
            if (tempModal) tempModal.style.display = 'none';
          } catch (e) { }
        }, 500);
      }
    };
  }

  if (urlParams.get('openModal') === '1') {
    setTimeout(() => {
      // Procura o botao principal de adicionar ao carrinho na pagina do produto
      const btnAddCart = document.getElementById('btn-add-cart') || document.querySelector('.btn-add-cart') || document.querySelector('[onclick*="handleAddToCart"]');
      if (btnAddCart) {
        btnAddCart.click();
      } else if (typeof handleAddToCart === 'function') {
        handleAddToCart();
      } else if (typeof showCustomModal === 'function') {
        showCustomModal('cart');
      }
    }, 600); // Pequeno delay para garantir que os scripts especificos do produto estejam prontos
  }

  // ===== SALVA ÚLTIMO PRODUTO VISITADO =====
  if (window.location.pathname.includes('/produto-')) {
    localStorage.setItem('famosinhos_ultimo_produto_url', window.location.href);
  }
});

// ===== HISTÓRICO DE PEDIDOS DO CLIENTE (Três pontinhos -> Pedidos) =====
window.showMyOrders = function() {
  let overlay = document.getElementById('my-orders-overlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'my-orders-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      z-index: 99999999;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      opacity: 0;
      transition: opacity 0.25s ease;
    `;

    const panel = document.createElement('div');
    panel.style.cssText = `
      width: 100%;
      max-width: 480px;
      height: 80vh;
      background: #f7f9fa;
      border-radius: 20px 20px 0 0;
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
      transform: translateY(100%);
      transition: transform 0.25s ease;
      position: relative;
    `;

    overlay.appendChild(panel);
    document.body.appendChild(overlay);

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) hideMyOrders();
    });
  }

  const isIndex = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/');
  const pagesPath = isIndex ? 'pages/' : '';
  const basePath = isIndex ? '' : '../';

  // Obter pedidos salvos
  let pedidos = [];
  try {
    pedidos = JSON.parse(localStorage.getItem('famosinhos_pedidos') || '[]');
  } catch (e) {
    pedidos = [];
  }

  const panel = overlay.firstElementChild;
  let contentHtml = '';

  if (!pedidos || pedidos.length === 0) {
    // Tela de "Sem pedidos" estilo Shopee limpa
    contentHtml = `
      <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 20px; text-align: center; color: #888; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
        <svg viewBox="0 0 24 24" width="60" height="60" fill="none" stroke="#ccc" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 16px;">
          <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <path d="M16 10a4 4 0 0 1-8 0"></path>
        </svg>
        <div style="font-size: 16px; font-weight: 700; color: #333; margin-bottom: 8px;">Você ainda não tem pedidos</div>
        <div style="font-size: 13px; color: #666; max-width: 250px; line-height: 1.4; margin-bottom: 24px;">Que tal adicionar alguns produtos incríveis ao seu carrinho agora mesmo?</div>
        <button onclick="hideMyOrders()" style="padding: 12px 28px; background: #ff2c55; color: #fff; border: none; border-radius: 20px; font-size: 14px; font-weight: 700; cursor: pointer; outline: none; border: none;">Voltar a comprar</button>
      </div>
    `;
  } else {
    // Renderiza a lista de pedidos
    let cardsHtml = '';
    pedidos.forEach((p, index) => {
      let itemsHtml = '';
      if (p.itens && Array.isArray(p.itens)) {
        p.itens.forEach(item => {
          let imgSrc = item.img || '';
          if (!imgSrc.startsWith('http') && !imgSrc.startsWith('//')) {
            // Ajustar o path relativo da imagem dependendo de onde o modal está sendo aberto
            if (imgSrc.startsWith('../')) {
              imgSrc = isIndex ? imgSrc.substring(3) : imgSrc;
            } else {
              imgSrc = isIndex ? imgSrc : '../' + imgSrc;
            }
          }
          itemsHtml += `
            <div style="display: flex; gap: 12px; margin-bottom: 12px; border-bottom: 1px solid #f9f9f9; padding-bottom: 12px;">
              <img src="${imgSrc}" onerror="this.src='https://via.placeholder.com/64'" style="width: 50px; height: 50px; border-radius: 6px; object-fit: cover; border: 1px solid #eee; flex-shrink: 0;" />
              <div style="flex: 1; min-width: 0;">
                <div style="font-size: 13px; color: #222; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${item.nome}</div>
                ${item.variacao ? `<div style="font-size: 11px; color: #888; margin-top: 2px;">Variação: ${item.variacao}</div>` : ''}
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                  <span style="font-size: 13px; font-weight: 700; color: #222;">R$ ${parseFloat(item.preco).toFixed(2).replace('.', ',')}</span>
                  <span style="font-size: 11px; color: #666;">x${item.qty}</span>
                </div>
              </div>
            </div>
          `;
        });
      }

      cardsHtml += `
        <div style="background: #fff; border-radius: 12px; padding: 16px; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); font-family: -apple-system, BlinkMacSystemFont, sans-serif;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #f5f5f5; padding-bottom: 8px;">
            <div style="font-size: 11px; color: #666;">Gerado em ${p.data}</div>
            <div style="font-size: 12px; color: #ff2c55; font-weight: 700;">Aguardando pagamento</div>
          </div>
          <div>
            ${itemsHtml}
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; border-top: 1px solid #f5f5f5; padding-top: 12px;">
            <div style="font-size: 14px; font-weight: 700; color: #222;">Total: R$ ${parseFloat(p.total).toFixed(2).replace('.', ',')}</div>
            <button onclick="window.redirecionarParaPix('${p.pix_code || ''}', '${p.txid || ''}', '${p.total || ''}')" style="padding: 8px 16px; background: #ff2c55; color: #fff; border: none; border-radius: 6px; font-size: 12px; font-weight: 700; cursor: pointer; outline: none;">Visualizar código</button>
          </div>
        </div>
      `;
    });

    contentHtml = `
      <div style="flex: 1; overflow-y: auto; padding: 16px; -webkit-overflow-scrolling: touch;">
        ${cardsHtml}
      </div>
    `;
  }

  panel.innerHTML = `
    <!-- Header -->
    <div style="background: #fff; min-height: 54px; display: flex; align-items: center; padding: 0 16px; border-bottom: 1px solid #eee; border-radius: 20px 20px 0 0; position: sticky; top: 0; z-index: 10;">
      <h2 style="font-size: 16px; font-weight: 700; color: #000; margin: 0; flex: 1; text-align: center;">Meus Pedidos</h2>
      <button onclick="hideMyOrders()" style="position: absolute; right: 16px; background: none; border: none; cursor: pointer; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; border-radius: 50%; background: #f3f3f3; font-size: 14px; font-weight: bold; color: #666;">✕</button>
    </div>
    
    <!-- Corpo -->
    ${contentHtml}
  `;

  // Função interna para redirecionar para a página do pix a partir do card
  window.redirecionarParaPix = function(pix_code, txid, total) {
    sessionStorage.setItem('sealpay_pix_code', pix_code);
    sessionStorage.setItem('sealpay_txid', txid);
    sessionStorage.setItem('sealpay_total', total);
    window.location.href = pagesPath + 'pix.html';
  };

  overlay.style.display = 'flex';
  setTimeout(() => {
    overlay.style.opacity = '1';
    panel.style.transform = 'translateY(0)';
  }, 10);
};

window.hideMyOrders = function() {
  const overlay = document.getElementById('my-orders-overlay');
  if (overlay) {
    overlay.style.opacity = '0';
    overlay.firstElementChild.style.transform = 'translateY(100%)';
    setTimeout(() => {
      overlay.style.display = 'none';
    }, 250);
  }
};

// Substituição de estrelas emojis por SVGs com a mesma cor amarela queimada (#F5A623)
(function() {
  function substituirEstrelas() {
    const elements = document.querySelectorAll('.review-user-stars, .review-stars');
    const svgEstrela = `<svg class="review-star-svg" fill="#F5A623" viewBox="0 0 48 48" width="13" height="13" style="margin-right: 2px; vertical-align: middle;"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg>`;

    elements.forEach(el => {
      if (el.querySelector('.review-star-svg')) return;
      const texto = el.textContent || "";
      const count = (texto.match(/⭐|⭐️/g) || []).length;
      if (count > 0) {
        el.innerHTML = svgEstrela.repeat(count);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', substituirEstrelas);
  } else {
    substituirEstrelas();
  }

  // MutationObserver para observar elementos inseridos dinamicamente
  if (typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver((mutations) => {
      let shouldRun = false;
      for (const mutation of mutations) {
        if (mutation.addedNodes.length > 0) {
          shouldRun = true;
          break;
        }
      }
      if (shouldRun) {
        substituirEstrelas();
        if (typeof initAvatarColors === 'function') {
          initAvatarColors();
        }
      }
    });
    const attachObserver = () => {
      const target = document.body || document.documentElement;
      if (target) {
        observer.observe(target, { childList: true, subtree: true });
      }
    };
    if (document.body) {
      attachObserver();
    } else {
      document.addEventListener('DOMContentLoaded', attachObserver);
    }
  }
})();



  // Lógica global e inteligente para o botão de voltar das páginas de produtos
  document.addEventListener('DOMContentLoaded', () => {
    // Rastreia a página anterior de produto visitada
    const currentUrl = window.location.href;
    if (!currentUrl.includes('index.html')) {
      const prevProd = localStorage.getItem('last_visited_product');
      if (prevProd && prevProd !== currentUrl) {
        localStorage.setItem('prev_visited_product', prevProd);
      }
      localStorage.setItem('last_visited_product', currentUrl);
    }

    const setupBackBtn = () => {
      const backBtn = document.querySelector('.header-back-btn');
      if (backBtn) {
        // Remove event listener antigo se houver clonando o botão
        const newBackBtn = backBtn.cloneNode(true);
        backBtn.parentNode.replaceChild(newBackBtn, backBtn);

        newBackBtn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();

          // Tenta voltar pelo histórico do navegador primeiro se a página anterior for do mesmo site
          if (document.referrer && document.referrer.includes(window.location.host)) {
            window.history.back();
            return;
          }

          // Se não houver histórico válido, usa o produto anteriormente visitado
          const prevProd = localStorage.getItem('prev_visited_product');
          if (prevProd) {
            window.location.href = prevProd;
          } else {
            // Fallback padrão para a loja inicial
            window.location.href = '../index.html';
          }
        });
      }
    };
    setupBackBtn();
    // Fallback para SPA ou atrasos na injeção do cabeçalho
    setTimeout(setupBackBtn, 500);
  });

  // Execução imediata defensiva para blindar e travar o limite de 3 avaliações em todos os produtos
  if (typeof document !== 'undefined') {
    if (document.querySelector('.reviews-section, .customer-reviews-section')) {
      formatCompactReviews();
      renderStoreReviewsFilter();
    }
  }


// Interceptação global de cliques para disparar o carregamento bolinhas com timeout de segurança
if (typeof document !== 'undefined' && !window.__ttLoaderClickBound) {
  window.__ttLoaderClickBound = true;
  document.addEventListener('click', function (e) {
    // Se o clique for no overlay do próprio loader, não faz nada (o onclick do overlay já dispensa)
    if (e.target.closest('#tiktok-global-loader')) return;

    // Links para outras páginas
    const link = e.target.closest('a[href]');
    if (link) {
      const href = link.getAttribute('href');
      // Ignora âncoras locais, javascript:, tel:, mailto: ou links com target (ex: _blank)
      if (href && !href.startsWith('#') && !href.startsWith('javascript:') && !href.startsWith('tel:') && !href.startsWith('mailto:') && !link.getAttribute('target') && !e.ctrlKey && !e.metaKey) {
        if (typeof window.showTikTokLoader === 'function') {
          window.showTikTokLoader({ type: 'normal', duration: 500 });
        }
      }
      return;
    }
    // Cards de produtos clicáveis
    const card = e.target.closest('.recommended-card, .product-card, .product-card-rec, .store-more-item, .related-card, .store-widget-product-card');
    if (card && !e.target.closest('button')) {
      if (typeof window.showTikTokLoader === 'function') {
        window.showTikTokLoader({ type: 'normal', duration: 650 });
      }
      return;
    }
    // Botões de ação da loja (Comprar, Carrinho, Opções, Frete, Proteção, Parcelas, Cupons, Avaliações, Chat, Loja)
    const actionBtn = e.target.closest(
      '#btn-buy, #btn-add-cart, .btn-buy, .btn-add-cart, .unified-buy-btn, ' +
      '.var-btn-buy-full, .var-btn-cart-full, ' +
      '.info-row-item, .info-row-item-protection, .installment-row, .discount-ticket, ' +
      '.reviews-header-official, .store-chat-clickable-chat, .store-chat-clickable-loja, ' +
      '.checkout-btn, #btn-checkout, #btn-finalizar-compra'
    );
    if (actionBtn) {
      if (typeof window.showTikTokLoader === 'function') {
        window.showTikTokLoader({ type: 'normal', duration: 360 });
      }
    }
  }, true);

  // BLINDAGEM MÁXIMA PARA CELULAR (BFCACHE / BOTÃO VOLTAR DO CHROME & SAFARI):
  // Quando o usuário volta à página usando o botão "Voltar" do navegador ou do Android,
  // a página é restaurada da memória. O evento 'pageshow' mata o loader imediatamente!
  window.addEventListener('pageshow', function (event) {
    if (typeof window.hideTikTokLoader === 'function') {
      window.hideTikTokLoader();
    }
  });

  // Se a aba for minimizada ou restaurada, também garante a limpeza
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible' && typeof window.hideTikTokLoader === 'function') {
      window.hideTikTokLoader();
    }
  });
}

// tiktok-page-transition-listener: Transição suave instantânea TikTok Shop entre páginas
document.addEventListener('click', function (e) {
  const link = e.target.closest('a');
  if (link && link.href && !link.target && !link.href.startsWith('javascript:') && !link.href.includes('#') && !link.href.startsWith('tel:') && !link.href.startsWith('mailto:')) {
    const hrefAttr = link.getAttribute('href') || '';
    const isInternal = (link.href.indexOf(window.location.host) !== -1) || hrefAttr.startsWith('.') || hrefAttr.startsWith('/');
    if (isInternal && !link.classList.contains('no-loader')) {
      if (typeof window.showTikTokNormal === 'function') {
        window.showTikTokNormal(800);
      }
    }
  }
}, true);


/* ========================================================================== */
/* 🚚 MODAL DE ENVIO OFICIAL TIKTOK SHOP (BOTTOM SHEET INFERIOR)               */
/* ========================================================================== */

function formatarPrazoEnvioCompleto() {
  const hoje = new Date();
  const dMin = new Date(hoje);
  dMin.setDate(hoje.getDate() + 5);
  const dMax = new Date(hoje);
  dMax.setDate(hoje.getDate() + 9);

  const diasSemana = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'];
  const meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];

  const semMin = diasSemana[dMin.getDay()];
  const diaMin = dMin.getDate();
  const mesMin = meses[dMin.getMonth()];

  const semMax = diasSemana[dMax.getDay()];
  const diaMax = dMax.getDate();
  const mesMax = meses[dMax.getMonth()];

  return `Receba até ${semMin}., ${diaMin} de ${mesMin}–${semMax}., ${diaMax} de ${mesMax}`;
}

const BR_ESTADOS_ENVIO = [
  { uf: 'AC', nome: 'Acre', cap: ['Rio Branco', 'Cruzeiro do Sul', 'Sena Madureira', 'Tarauacá'] },
  { uf: 'AL', nome: 'Alagoas', cap: ['Maceió', 'Arapiraca', 'Rio Largo', 'Palmeira dos Índios'] },
  { uf: 'AP', nome: 'Amapá', cap: ['Macapá', 'Santana', 'Laranjal do Jari', 'Oiapoque'] },
  { uf: 'AM', nome: 'Amazonas', cap: ['Manaus', 'Parintins', 'Itacoatiara', 'Manacapuru'] },
  { uf: 'BA', nome: 'Bahia', cap: ['Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Camaçari', 'Ilhéus', 'Juazeiro', 'Lauro de Freitas'] },
  { uf: 'CE', nome: 'Ceará', cap: ['Fortaleza', 'Caucaia', 'Juazeiro do Norte', 'Maracanaú', 'Sobral'] },
  { uf: 'DF', nome: 'Distrito Federal', cap: ['Brasília', 'Taguatinga', 'Ceilândia', 'Águas Claras', 'Gama'] },
  { uf: 'ES', nome: 'Espírito Santo', cap: ['Vitória', 'Vila Velha', 'Serra', 'Cariacica', 'Cachoeiro de Itapemirim'] },
  { uf: 'GO', nome: 'Goiás', cap: ['Goiânia', 'Aparecida de Goiânia', 'Anápolis', 'Rio Verde', 'Luziânia'] },
  { uf: 'MA', nome: 'Maranhão', cap: ['São Luís', 'Imperatriz', 'São José de Ribamar', 'Timon', 'Caxias'] },
  { uf: 'MT', nome: 'Mato Grosso', cap: ['Cuiabá', 'Várzea Grande', 'Rondonópolis', 'Sinop', 'Tangará da Serra'] },
  { uf: 'MS', nome: 'Mato Grosso do Sul', cap: ['Campo Grande', 'Dourados', 'Três Lagoas', 'Corumbá'] },
  { uf: 'MG', nome: 'Minas Gerais', cap: ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora', 'Betim', 'Montes Claros', 'Uberaba'] },
  { uf: 'PA', nome: 'Pará', cap: ['Belém', 'Ananindeua', 'Santarém', 'Marabá', 'Parauapebas', 'Castanhal', 'Abaetetuba'] },
  { uf: 'PB', nome: 'Paraíba', cap: ['João Pessoa', 'Campina Grande', 'Santa Rita', 'Patos'] },
  { uf: 'PR', nome: 'Paraná', cap: ['Curitiba', 'Londrina', 'Maringá', 'Ponta Grossa', 'Cascavel', 'São José dos Pinhais', 'Foz do Iguaçu'] },
  { uf: 'PE', nome: 'Pernambuco', cap: ['Recife', 'Jaboatão dos Guararapes', 'Olinda', 'Caruaru', 'Petrolina', 'Paulista'] },
  { uf: 'PI', nome: 'Piauí', cap: ['Teresina', 'Parnaíba', 'Picos', 'Piripiri'] },
  { uf: 'RJ', nome: 'Rio de Janeiro', cap: ['Rio de Janeiro', 'São Gonçalo', 'Duque de Caxias', 'Nova Iguaçu', 'Niterói', 'Belford Roxo', 'Campos dos Goytacazes'] },
  { uf: 'RN', nome: 'Rio Grande do Norte', cap: ['Natal', 'Mossoró', 'Parnamirim', 'São Gonçalo do Amarante'] },
  { uf: 'RS', nome: 'Rio Grande do Sul', cap: ['Porto Alegre', 'Caxias do Sul', 'Canoas', 'Pelotas', 'Santa Maria', 'Gravataí', 'Novo Hamburgo'] },
  { uf: 'RO', nome: 'Rondônia', cap: ['Porto Velho', 'Ji-Paraná', 'Ariquemes', 'Vilhena'] },
  { uf: 'RR', nome: 'Roraima', cap: ['Boa Vista', 'Rorainópolis', 'Caracaraí'] },
  { uf: 'SC', nome: 'Santa Catarina', cap: ['Florianópolis', 'Joinville', 'Blumenau', 'São José', 'Chapecó', 'Itajaí', 'Criciúma'] },
  { uf: 'SP', nome: 'São Paulo', cap: ['São Paulo', 'Guarulhos', 'Campinas', 'São Bernardo do Campo', 'Santo André', 'Osasco', 'Ribeirão Preto', 'Sorocaba', 'Santos', 'São José dos Campos'] },
  { uf: 'SE', nome: 'Sergipe', cap: ['Aracaju', 'Nossa Senhora do Socorro', 'Lagarto', 'Itabaiana'] },
  { uf: 'TO', nome: 'Tocantins', cap: ['Palmas', 'Araguaína', 'Gurupi', 'Porto Nacional'] }
];

const _ibgeCidadesCache = {};
let _envioSelectedEstado = null;

function getSavedEnvioDestino() {
  try {
    const saved = localStorage.getItem('stone_envio_local');
    if (saved) {
      const p = JSON.parse(saved);
      if (p && p.cidade && p.estadoNome) return `${p.cidade}, ${p.estadoNome}, Brasil`;
    }
    const cepData = localStorage.getItem('user_cep_info');
    if (cepData) {
      const parsed = JSON.parse(cepData);
      if (parsed && parsed.cidade && parsed.uf) {
        const est = BR_ESTADOS_ENVIO.find(e => e.uf === String(parsed.uf).toUpperCase());
        return `${parsed.cidade}, ${est ? est.nome : parsed.uf}, Brasil`;
      }
    }
  } catch (e) {}
  return '';
}

window.showEnvioMainStep = function() {
  const stepMain = document.getElementById('modal-envio-step-main');
  const stepPicker = document.getElementById('modal-envio-step-picker');
  const backBtn = document.getElementById('modal-envio-back-btn');
  const titleEl = document.getElementById('modal-envio-header-title');
  if (stepMain) stepMain.style.display = 'block';
  if (stepPicker) stepPicker.style.display = 'none';
  if (backBtn) backBtn.style.display = 'none';
  if (titleEl) titleEl.textContent = 'Envio';

  const destinoEl = document.getElementById('modal-envio-destino-txt');
  if (destinoEl) {
    const savedTxt = getSavedEnvioDestino();
    if (savedTxt) {
      destinoEl.textContent = savedTxt;
      destinoEl.style.color = '#161823';
    } else {
      destinoEl.textContent = 'Selecionar estado';
      destinoEl.style.color = '#161823';
    }
  }
};

window.openEnvioEstadoPicker = function() {
  _envioSelectedEstado = null;
  const stepMain = document.getElementById('modal-envio-step-main');
  const stepPicker = document.getElementById('modal-envio-step-picker');
  const backBtn = document.getElementById('modal-envio-back-btn');
  const titleEl = document.getElementById('modal-envio-header-title');
  const searchInput = document.getElementById('modal-envio-search-input');
  const listWrap = document.getElementById('modal-envio-picker-list');
  if (!stepPicker || !listWrap) return;

  if (stepMain) stepMain.style.display = 'none';
  stepPicker.style.display = 'flex';
  if (backBtn) {
    backBtn.style.display = 'flex';
    backBtn.onclick = function() { window.showEnvioMainStep(); };
  }
  if (titleEl) titleEl.textContent = 'Selecionar estado';
  if (searchInput) {
    searchInput.value = '';
    searchInput.placeholder = 'Pesquisar estado...';
    searchInput.oninput = function() { renderEstadosList(searchInput.value); };
  }
  renderEstadosList('');
};

function renderEstadosList(filtro) {
  const listWrap = document.getElementById('modal-envio-picker-list');
  if (!listWrap) return;
  const q = String(filtro || '').trim().toLowerCase();
  const filtrados = BR_ESTADOS_ENVIO.filter(e => !q || e.nome.toLowerCase().includes(q) || e.uf.toLowerCase().includes(q));
  listWrap.innerHTML = filtrados.map(e => `
    <div onclick="window.openEnvioCidadePicker('${e.uf}')" style="display:flex; align-items:center; justify-content:space-between; padding:13px 16px; border-bottom:1px solid #f3f3f5; cursor:pointer; font-size:14.5px; color:#161823; -webkit-tap-highlight-color:transparent;">
      <span>${e.nome}</span>
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#999aa0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
    </div>
  `).join('');
  listWrap.scrollTop = 0;
}

window.openEnvioCidadePicker = async function(uf) {
  const est = BR_ESTADOS_ENVIO.find(e => e.uf === uf);
  if (!est) return;
  _envioSelectedEstado = est;

  const backBtn = document.getElementById('modal-envio-back-btn');
  const titleEl = document.getElementById('modal-envio-header-title');
  const searchInput = document.getElementById('modal-envio-search-input');
  const listWrap = document.getElementById('modal-envio-picker-list');
  if (!listWrap) return;

  if (titleEl) titleEl.textContent = `Selecionar cidade (${est.uf})`;
  if (backBtn) {
    backBtn.style.display = 'flex';
    backBtn.onclick = function() { window.openEnvioEstadoPicker(); };
  }
  if (searchInput) {
    searchInput.value = '';
    searchInput.placeholder = `Pesquisar cidade em ${est.nome}...`;
  }

  listWrap.innerHTML = '<div style="padding:28px 16px; text-align:center; color:#8a8b91; font-size:13.5px;">Carregando cidades...</div>';

  let cidades = _ibgeCidadesCache[uf];
  if (!cidades) {
    try {
      const ctrl = new AbortController();
      const tId = setTimeout(() => ctrl.abort(), 3500);
      const resp = await fetch(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${uf}/municipios?orderBy=nome`, { signal: ctrl.signal });
      clearTimeout(tId);
      if (resp.ok) {
        const arr = await resp.json();
        if (Array.isArray(arr) && arr.length > 0) {
          cidades = arr.map(c => c.nome);
          _ibgeCidadesCache[uf] = cidades;
        }
      }
    } catch (e) {}
  }
  if (!cidades || !cidades.length) {
    cidades = est.cap.slice().sort((a, b) => a.localeCompare(b, 'pt-BR'));
  }

  function renderCidades(qStr) {
    const q = String(qStr || '').trim().toLowerCase();
    const matches = cidades.filter(c => !q || c.toLowerCase().includes(q));
    if (!matches.length) {
      listWrap.innerHTML = '<div style="padding:24px 16px; text-align:center; color:#8a8b91; font-size:13.5px;">Nenhuma cidade encontrada</div>';
      return;
    }
    listWrap.innerHTML = matches.map(c => {
      const safeC = c.replace(/'/g, "\\'");
      return `
        <div onclick="window.selectEnvioCidade('${safeC}')" style="display:flex; align-items:center; justify-content:space-between; padding:13px 16px; border-bottom:1px solid #f3f3f5; cursor:pointer; font-size:14.5px; color:#161823; -webkit-tap-highlight-color:transparent;">
          <span>${c}</span>
        </div>
      `;
    }).join('');
    listWrap.scrollTop = 0;
  }

  if (searchInput) {
    searchInput.oninput = function() { renderCidades(searchInput.value); };
  }
  renderCidades('');
};

window.selectEnvioCidade = function(cidade) {
  if (!_envioSelectedEstado || !cidade) return;
  try {
    localStorage.setItem('stone_envio_local', JSON.stringify({
      uf: _envioSelectedEstado.uf,
      estadoNome: _envioSelectedEstado.nome,
      cidade: cidade
    }));
  } catch (e) {}
  window.showEnvioMainStep();
};

window.openEnvioModal = function() {
  let overlay = document.getElementById('modal-envio-overlay');
  if (!overlay) {
    window.initEnvioModal();
    overlay = document.getElementById('modal-envio-overlay');
  }
  if (!overlay) return;

  window.showEnvioMainStep();

  // Atualiza a data dinâmica
  const prazoEl = document.getElementById('modal-envio-prazo-txt');
  if (prazoEl) {
    prazoEl.textContent = formatarPrazoEnvioCompleto();
  }

  // Puxa o preço original do frete da tela principal ou exibe R$ 19,20
  const precoEl = document.getElementById('modal-envio-preco-txt');
  if (precoEl) {
    const riscadoEl = document.querySelector('.info-row-frete-orig, .info-row-text-group span[style*="line-through"]');
    if (riscadoEl && riscadoEl.textContent.trim()) {
      precoEl.textContent = riscadoEl.textContent.trim();
    } else {
      precoEl.textContent = 'R$ 19,20';
    }
  }

  overlay.style.display = 'flex';
  void overlay.offsetWidth;
  overlay.style.opacity = '1';
  overlay.style.pointerEvents = 'auto';

  const box = document.getElementById('modal-envio-box');
  if (box) {
    box.style.transform = 'translateY(0)';
  }

  document.body.style.overflow = 'hidden';
};

window.closeEnvioModal = function() {
  const overlay = document.getElementById('modal-envio-overlay');
  const box = document.getElementById('modal-envio-box');
  if (box) {
    box.style.transform = 'translateY(100%)';
  }
  if (overlay) {
    overlay.style.opacity = '0';
    overlay.style.pointerEvents = 'none';
    setTimeout(() => {
      overlay.style.display = 'none';
      document.body.style.overflow = '';
    }, 280);
  }
};

window.atualizarPrazoFreteNaPagina = function() {
  try {
    const prazo = formatarPrazoEnvioCompleto();
    // 1. Atualizar por seletores de classe e ID conhecidos
    const els = document.querySelectorAll('#frete-prazo-dinamico, .frete-prazo-dinamico, .info-row-envio .info-row-subtitle, .shipping-date');
    els.forEach(el => {
      el.textContent = prazo;
    });

    // 2. Varrer qualquer nó de texto dentro da linha de frete que tenha data antiga estática
    document.querySelectorAll('.info-row-item, .info-row-envio').forEach(row => {
      row.querySelectorAll('span, p, div').forEach(node => {
        if (node.children.length === 0 && (node.textContent.includes('Receba até') || node.textContent.includes('Receba em'))) {
          node.textContent = prazo;
        }
      });
    });
  } catch(e) {}
};

// Auto-execução imediata e no carregamento da página
if (typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      if (typeof window.atualizarPrazoFreteNaPagina === 'function') {
        window.atualizarPrazoFreteNaPagina();
      }
    });
  } else {
    window.atualizarPrazoFreteNaPagina();
  }
}

window.initEnvioModal = function() {
  if (typeof window.atualizarPrazoFreteNaPagina === 'function') {
    window.atualizarPrazoFreteNaPagina();
  }
  if (document.getElementById('modal-envio-overlay')) return;

  const overlay = document.createElement('div');
  overlay.id = 'modal-envio-overlay';
  overlay.style.cssText = 'position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 100000; display: none; align-items: flex-end; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.25s ease;';

  overlay.innerHTML = `
    <div id="modal-envio-box" style="position: relative; width: 100%; max-width: 480px; background: #ffffff; border-radius: 14px 14px 0 0; z-index: 100001; overflow: hidden; box-shadow: 0 -4px 20px rgba(0,0,0,0.18); transform: translateY(100%); transition: transform 0.28s cubic-bezier(0.25, 1, 0.5, 1); min-height: 58vh; max-height: 78vh; display: flex; flex-direction: column; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
      
      <!-- Cabeçalho Oficial -->
      <div style="position: relative; height: 52px; min-height: 52px; display: flex; align-items: center; justify-content: center; border-bottom: 1px solid #f1f1f2; padding: 0 16px;">
        <button id="modal-envio-back-btn" type="button" style="display: none; position: absolute; left: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; padding: 8px; align-items: center; justify-content: center;" aria-label="Voltar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
        <span id="modal-envio-header-title" style="font-size: 16px; font-weight: 700; color: #161823; letter-spacing: -0.2px;">Envio</span>
        <button type="button" onclick="window.closeEnvioModal()" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; padding: 8px; display: flex; align-items: center; justify-content: center;" aria-label="Fechar">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <!-- STEP 1: TELA PRINCIPAL ENVIO 1:1 -->
      <div id="modal-envio-step-main" style="flex: 1;">
        <!-- Bloco 1: Origem e Destino -->
        <div style="padding: 18px 16px 14px 16px;">
          <!-- Linha 1: Origem (Ícone Caixa com Aba + Seta Direita 1:1 da Print) -->
          <div style="display: flex; align-items: center; gap: 12px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;">
              <path d="M4 8.5H20V19C20 19.8284 19.3284 20.5 18.5 20.5H5.5C4.67157 20.5 4 19.8284 4 19V8.5Z" stroke="#161823" stroke-width="1.75" stroke-linejoin="round"/>
              <path d="M4 8.5L6.8 4H17.2L20 8.5" stroke="#161823" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8.5 14.3H15.2" stroke="#161823" stroke-width="1.75" stroke-linecap="round"/>
              <path d="M12.6 11.8L15.3 14.3L12.6 16.8" stroke="#161823" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span style="font-size: 14.5px; font-weight: 400; color: #161823;">De São Paulo</span>
          </div>

          <!-- Setinhas duplas conectoras 1:1 -->
          <div style="width: 18px; margin: 7px 0; display: flex; align-items: center; justify-content: center;">
            <svg width="11" height="13" viewBox="0 0 12 14" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: block;">
              <path d="M2.2 2.5L6 6.3L9.8 2.5" stroke="#999aa0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M2.2 7.5L6 11.3L9.8 7.5" stroke="#999aa0" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>

          <!-- Linha 2: Destino Clicável (Selecionar Estado → Cidade) -->
          <div onclick="window.openEnvioEstadoPicker()" style="display: flex; align-items: center; justify-content: space-between; gap: 12px; cursor: pointer; -webkit-tap-highlight-color: transparent;">
            <div style="display: flex; align-items: center; gap: 12px; min-width: 0; flex: 1;">
              <!-- Ícone Pin Destino 1:1 -->
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink: 0;">
                <path d="M12 21C15.8 17.6 19 13.9 19 9.8C19 5.93401 15.866 2.8 12 2.8C8.13401 2.8 5 5.93401 5 9.8C5 13.9 8.2 17.6 12 21Z" stroke="#161823" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="9.8" r="2.6" stroke="#161823" stroke-width="1.75"/>
              </svg>
              <span id="modal-envio-destino-txt" style="font-size: 14.5px; font-weight: 400; color: #161823; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Selecionar estado</span>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><polyline points="9 18 15 12 9 6"></polyline></svg>
          </div>
        </div>

        <!-- Linha divisória -->
        <div style="height: 1px; background: #f1f1f2; margin: 4px 16px 16px 16px;"></div>

        <!-- Bloco 2: Opção de Envio (Envio padrão) -->
        <div style="padding: 0 16px 24px 16px; display: flex; justify-content: space-between; align-items: flex-start;">
          <div>
            <div style="font-size: 14.5px; font-weight: 600; color: #161823; margin-bottom: 4px;">Envio padrão</div>
            <div id="modal-envio-prazo-txt" style="font-size: 13px; color: #757575; line-height: 1.35;">${formatarPrazoEnvioCompleto()}</div>
          </div>
          <div id="modal-envio-preco-txt" style="font-size: 14px; font-weight: 400; color: #161823; white-space: nowrap; margin-left: 12px;">R$ 19,20</div>
        </div>
      </div>

      <!-- STEP 2 & 3: SELETOR ESTADO → CIDADE -->
      <div id="modal-envio-step-picker" style="display: none; flex-direction: column; flex: 1; min-height: 0; max-height: calc(78vh - 52px);">
        <div style="padding: 10px 16px; background: #ffffff; border-bottom: 1px solid #f1f1f2;">
          <input id="modal-envio-search-input" type="text" placeholder="Pesquisar estado..." style="width: 100%; height: 36px; border-radius: 8px; border: none; background: #f3f3f5; padding: 0 12px; font-size: 13.5px; color: #161823; outline: none; box-sizing: border-box;" />
        </div>
        <div id="modal-envio-picker-list" style="flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch;"></div>
      </div>

    </div>
  `;

  overlay.onclick = function(e) {
    if (e.target === overlay) {
      window.closeEnvioModal();
    }
  };

  document.body.appendChild(overlay);

  // Anexa listeners nas linhas de frete
  bindFreteClickListeners();
};

function bindFreteClickListeners() {
  document.querySelectorAll('.info-row-item').forEach(el => {
    if (el.textContent.includes('Frete') || el.textContent.includes('Receba')) {
      el.style.cursor = 'pointer';
      el.onclick = function(e) {
        e.preventDefault();
        e.stopPropagation();
        window.openEnvioModal();
      };
    }
  });
}

// Inicializa no carregamento do DOM
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', function() {
    window.initEnvioModal();
  });
} else {
  window.initEnvioModal();
}

// Tecla ESC fecha o modal
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    window.closeEnvioModal();
  }
});

// Toggle oficial TikTok Shop: Detalhes do Produto (Ver mais / Ver menos)
window.toggleProductDetails = function(btn) {
  if (!btn) return;
  var container = btn.closest('.product-details-block') || btn.parentElement;
  if (!container) return;
  var hiddenRows = container.querySelectorAll('.detail-row.toggleable-row');
  var isExpanded = btn.classList.contains('expanded');

  if (isExpanded) {
    hiddenRows.forEach(function(r) {
      r.classList.add('is-hidden');
      r.style.setProperty('display', 'none', 'important');
    });
    btn.classList.remove('expanded');
    var span = btn.querySelector('span');
    if (span) span.textContent = 'Ver mais';
  } else {
    hiddenRows.forEach(function(r) {
      r.classList.remove('is-hidden');
      r.style.setProperty('display', 'flex', 'important');
    });
    btn.classList.add('expanded');
    var span = btn.querySelector('span');
    if (span) span.textContent = 'Ver menos';
  }
};


window.toggleProductVideo = function(wrapper) {
  if (!wrapper) return;
  var video = wrapper.querySelector('video');
  var playBtn = wrapper.querySelector('.play-overlay-btn');
  if (!video) return;
  if (video.paused) {
    video.play();
    if (playBtn) playBtn.style.opacity = '0';
  } else {
    video.pause();
    if (playBtn) playBtn.style.opacity = '1';
  }
};

window.scrollToTop = function() {
  var sc = document.querySelector('.page-content');
  if (sc) sc.scrollTo({ top: 0, behavior: 'smooth' });
  window.scrollTo({ top: 0, behavior: 'smooth' });
};


// ==========================================================================
// TIKTOK SHOP: TOGGLES GLOBAIS SOBRE ESTE PRODUTO (MULTI-PRODUTO)
// ==========================================================================
window.toggleProductDetails = function(btn) {
  if (!btn) return;
  var container = btn.closest('.product-details-block') || btn.parentElement;
  if (!container) return;
  var hiddenRows = container.querySelectorAll('.detail-row.toggleable-row');
  var isExpanded = btn.classList.contains('is-expanded');

  if (isExpanded) {
    hiddenRows.forEach(function(r) {
      r.classList.add('is-hidden');
      r.style.setProperty('display', 'none', 'important');
    });
    btn.classList.remove('is-expanded');
    container.classList.remove('is-expanded');
    btn.textContent = 'Ver mais';
  } else {
    hiddenRows.forEach(function(r) {
      r.classList.remove('is-hidden');
      r.style.setProperty('display', 'flex', 'important');
    });
    btn.classList.add('is-expanded');
    container.classList.add('is-expanded');
    btn.textContent = 'Ver menos';
  }
};

window.toggleSobreProdutoDescricao = function(expand) {
  var desc = document.getElementById('sobre-produto-desc-section');
  var btnMais = document.getElementById('btn-toggle-ver-mais');
  if (!desc) return;

  if (expand) {
    desc.style.setProperty('display', 'block', 'important');
    if (btnMais) btnMais.style.display = 'none';
    desc.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } else {
    desc.style.setProperty('display', 'none', 'important');
    if (btnMais) btnMais.style.display = 'flex';
    var guide = document.querySelector('.size-guide-block') || document.getElementById('sobre-este-produto');
    if (guide) guide.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
};


// ==========================================================================
// TIKTOK SHOP: TOGGLE DESCRIÇÃO EXPANSÍVEL COM FADE-OUT
// ==========================================================================
window.calibrateDescricaoCollapsedHeight = function() {
  var container = document.getElementById('desc-expandable-container');
  var fade = document.getElementById('desc-fade-overlay');
  if (!container || container.classList.contains('is-expanded')) return;
  container.style.removeProperty('max-height');
  var fullH = container.scrollHeight || 0;
  if (fullH > 0 && fullH <= 445) {
    var targetH = Math.max(170, Math.round(fullH * 0.72));
    container.style.setProperty('max-height', targetH + 'px', 'important');
    if (fade) fade.style.setProperty('height', Math.min(124, Math.round(targetH * 0.62)) + 'px', 'important');
  } else {
    container.style.setProperty('max-height', '430px', 'important');
    if (fade) fade.style.setProperty('height', '124px', 'important');
  }
};

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      window.calibrateDescricaoCollapsedHeight();
      setTimeout(window.calibrateDescricaoCollapsedHeight, 350);
    });
  } else {
    window.calibrateDescricaoCollapsedHeight();
    setTimeout(window.calibrateDescricaoCollapsedHeight, 350);
  }
}

window.toggleDescricaoCompleta = function() {
  var container = document.getElementById('desc-expandable-container');
  var btn = document.getElementById('btn-toggle-desc');
  var text = document.getElementById('btn-toggle-desc-text');
  if (!container || !btn) return;

  var isExpanded = container.classList.contains('is-expanded');
  if (isExpanded) {
    container.classList.remove('is-expanded');
    btn.classList.remove('is-expanded');
    if (text) text.textContent = 'Ver mais';
    window.calibrateDescricaoCollapsedHeight();
    var section = document.getElementById('sobre-produto-desc-section');
    if (section) section.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  } else {
    container.classList.add('is-expanded');
    container.style.setProperty('max-height', (container.scrollHeight + 200) + 'px', 'important');
    btn.classList.add('is-expanded');
    if (text) text.textContent = 'Ver menos';
  }
};

// ==========================================================================
// TIKTOK SHOP: CONTROLES DO PLAYER DE VÍDEO 16:9 OFICIAL (MODELO PERMANENTE)
// ==========================================================================
(function initTTDescriptionPlayer() {
  function fmtCurrent(s) {
    if (!isFinite(s) || s < 0) return '00:00';
    var m = Math.floor(s / 60);
    var sec = Math.floor(s % 60);
    return (m < 10 ? '0' : '') + m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  function fmtDuration(s) {
    if (!isFinite(s) || s <= 0) return '0:00';
    var m = Math.floor(s / 60);
    var sec = Math.floor(s % 60);
    return m + ':' + (sec < 10 ? '0' : '') + sec;
  }

  function syncPlayState(card, isPlaying) {
    if (!card) return;
    var centerPlay = card.querySelector('#tt-center-play, .tt-video-center-play');
    var iconPlay = card.querySelector('#tt-icon-play');
    var iconPause = card.querySelector('#tt-icon-pause');
    if (isPlaying) {
      card.classList.add('is-playing');
      if (centerPlay) centerPlay.style.removeProperty('display');
      if (iconPlay) iconPlay.style.display = 'none';
      if (iconPause) iconPause.style.display = 'block';
    } else {
      card.classList.remove('is-playing');
      if (centerPlay) centerPlay.style.removeProperty('display');
      if (iconPlay) iconPlay.style.display = 'block';
      if (iconPause) iconPause.style.display = 'none';
    }
  }

  function updateProgressVisual(card, pct) {
    var clamped = Math.max(0, Math.min(100, pct));
    var fill = card.querySelector('#tt-progress-fill');
    var thumb = card.querySelector('#tt-progress-thumb');
    if (fill) fill.style.width = clamped + '%';
    if (thumb) thumb.style.left = clamped + '%';
  }

  window.toggleTTVideo = function(e) {
    if (e && e.target && e.target.closest && e.target.closest('.tt-video-bar') && !e.target.closest('#tt-btn-play')) return;
    if (e && e.target && e.target.closest && e.target.closest('.tt-fs-close-btn')) return;
    var card = document.getElementById('tt-product-video-wrapper') || (e && e.currentTarget ? e.currentTarget : null);
    var video = card ? card.querySelector('video') : document.getElementById('tt-product-video');
    if (!video) return;

    var now = Date.now();
    if (video._lastToggle && (now - video._lastToggle) < 220) return;
    video._lastToggle = now;

    if (!video.getAttribute('src') && video.dataset && video.dataset.src) {
      video.preload = 'auto';
      video.src = video.dataset.src;
    }

    if (video.paused || video.ended) {
      video.muted = false;
      var p = video.play();
      if (p && typeof p.then === 'function') {
        p.then(function() {
          syncPlayState(card, true);
        }).catch(function() {
          video.muted = true;
          video.play().then(function() {
            syncPlayState(card, true);
          }).catch(function() {});
        });
      } else {
        syncPlayState(card, true);
      }
    } else {
      video.pause();
      syncPlayState(card, false);
    }
  };

  function applySeekFromClientX(card, clientX) {
    var video = card ? card.querySelector('video') : document.getElementById('tt-product-video');
    var track = card ? (card.querySelector('.tt-video-progress-track') || card.querySelector('#tt-progress-bg')) : null;
    var curTime = card ? card.querySelector('#tt-cur-time') : null;
    if (!video || !track) return;
    var rect = track.getBoundingClientRect();
    if (!rect.width) return;
    var ratio = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    updateProgressVisual(card, ratio * 100);
    if (isFinite(video.duration) && video.duration > 0) {
      video.currentTime = ratio * video.duration;
      if (curTime) curTime.textContent = fmtCurrent(video.currentTime);
    }
  }

  window.seekTTVideo = function(e) {
    if (e) e.stopPropagation();
    var card = (e && e.target) ? e.target.closest('.tiktok-video-card') : document.getElementById('tt-product-video-wrapper');
    if (!card || !e) return;
    var cx = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
    applySeekFromClientX(card, cx);
  };

  window.toggleTTFullscreen = function(e) {
    if (e) e.stopPropagation();
    var card = (e && e.target) ? e.target.closest('.tiktok-video-card') : document.getElementById('tt-product-video-wrapper');
    if (!card) return;
    var isExpanded = card.classList.toggle('tt-fs-expanded');
    document.documentElement.style.overflow = isExpanded ? 'hidden' : '';
    document.body.style.overflow = isExpanded ? 'hidden' : '';
    if (!isExpanded && (document.fullscreenElement || document.webkitFullscreenElement)) {
      if (document.exitFullscreen) document.exitFullscreen().catch(function() {});
      else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
    }
  };

  function setupPlayer() {
    var video = document.getElementById('tt-product-video');
    var card = document.getElementById('tt-product-video-wrapper');
    if (!video || !card || video.dataset.ttBound) return;
    video.dataset.ttBound = 'true';

    // Hidrata metadados do vídeo de descrição apenas quando o usuário chega perto da seção
    if (!video.getAttribute('src') && video.dataset && video.dataset.src && 'IntersectionObserver' in window) {
      var descVidObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            if (!video.getAttribute('src') && video.dataset.src) {
              video.preload = 'metadata';
              video.src = video.dataset.src;
            }
            descVidObs.disconnect();
          }
        });
      }, { rootMargin: '450px 0px' });
      descVidObs.observe(card);
    }

    // Remove qualquer tag amarela antiga caso exista
    card.querySelectorAll('.tt-desc-product-anchor').forEach(function(el) { el.remove(); });

    // Garante botão de fechar no modo fullscreen
    if (!card.querySelector('.tt-fs-close-btn')) {
      var closeBtn = document.createElement('button');
      closeBtn.type = 'button';
      closeBtn.className = 'tt-fs-close-btn';
      closeBtn.setAttribute('aria-label', 'Sair da tela cheia');
      closeBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
      closeBtn.addEventListener('click', function(ev) {
        ev.stopPropagation();
        window.toggleTTFullscreen(ev);
      });
      card.appendChild(closeBtn);
    }

    var curTime = card.querySelector('#tt-cur-time');
    var durTime = card.querySelector('#tt-dur-time');
    var barBg = card.querySelector('#tt-progress-bg');

    // Drag / Scrubbing suave (mouse + touch)
    if (barBg) {
      var dragging = false;
      var onMove = function(ev) {
        if (!dragging) return;
        var cx = ev.clientX !== undefined ? ev.clientX : (ev.touches && ev.touches[0] ? ev.touches[0].clientX : 0);
        applySeekFromClientX(card, cx);
      };
      var onUp = function() {
        if (!dragging) return;
        dragging = false;
        barBg.classList.remove('is-scrubbing');
        window.removeEventListener('pointermove', onMove);
        window.removeEventListener('pointerup', onUp);
      };
      barBg.addEventListener('pointerdown', function(ev) {
        ev.stopPropagation();
        dragging = true;
        barBg.classList.add('is-scrubbing');
        applySeekFromClientX(card, ev.clientX);
        window.addEventListener('pointermove', onMove);
        window.addEventListener('pointerup', onUp);
      });
    }

    // Fechar fullscreen com ESC
    document.addEventListener('keydown', function(ev) {
      if (ev.key === 'Escape' && card.classList.contains('tt-fs-expanded')) {
        window.toggleTTFullscreen();
      }
    });

    // Pausa quando o usuário rolar para fora da tela
    if ('IntersectionObserver' in window) {
      var obs = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
          if (!entry.isIntersecting && !video.paused && !card.classList.contains('tt-fs-expanded')) {
            video.pause();
            syncPlayState(card, false);
          }
        });
      }, { threshold: 0.1 });
      obs.observe(card);
    }

    video.addEventListener('loadedmetadata', function() {
      if (durTime && isFinite(video.duration) && video.duration > 0) {
        durTime.textContent = fmtDuration(video.duration);
      }
    });

    if (video.readyState >= 1 && durTime && isFinite(video.duration) && video.duration > 0) {
      durTime.textContent = fmtDuration(video.duration);
    }

    video.addEventListener('timeupdate', function() {
      if (curTime) curTime.textContent = fmtCurrent(video.currentTime);
      if (isFinite(video.duration) && video.duration > 0) {
        updateProgressVisual(card, (video.currentTime / video.duration) * 100);
      }
    });

    video.addEventListener('play', function() { syncPlayState(card, true); });
    video.addEventListener('pause', function() { syncPlayState(card, false); });

    video.addEventListener('ended', function() {
      syncPlayState(card, false);
      updateProgressVisual(card, 0);
      if (curTime) curTime.textContent = '00:00';
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupPlayer);
  } else {
    setupPlayer();
  }
})();


// =========================================================================
// SISTEMA BLINDADO OFICIAL TIKTOK SHOP: TOGGLE SLIDER <-> GUIA DE TAMANHOS
// =========================================================================

(function() {
  function getProductSizeGuideImage() {
    // 1. REGRA SOBERANA DE OURO: Single Source of Truth direto da descrição do DOM!
    // A imagem que está na descrição da página É a autoridade máxima e deve ser exatamente a mesma no slider e no modal.
    const descImg = document.querySelector('.size-guide-img, .description-text img[src*="guia-tamanhos"], .about-product-section img[src*="guia-tamanhos"], .product-desc img[src*="guia-tamanhos"]');
    if (descImg && descImg.getAttribute('src')) {
      return descImg.getAttribute('src');
    }

    if (typeof PRODUTO_ATUAL === 'undefined') return null;
    const id = Number(PRODUTO_ATUAL.id);
    const nome = (PRODUTO_ATUAL.nome || '').toLowerCase();

    // Timestamp dinâmico para blindagem contra cache do navegador
    const vTime = '1795058371562';
    const mapById = {
      74: `../img/guia-tamanhos-74.png?v=${vTime}`,
      75: `../img/guia-tamanhos-75.png?v=${vTime}`,
      87: `../img/guia-tamanhos-87.png?v=${vTime}`,
      88: `../img/guia-tamanhos-88.png?v=${vTime}`,
      99: `../img/guia-tamanhos-99.png?v=${vTime}`,
      103: `../img/guia-tamanhos-103.png?v=${vTime}`,
      104: `../img/guia-tamanhos-104.png?v=${vTime}`,
      106: `../img/guia-tamanhos-106.png?v=${vTime}`,
      110: `../img/guia-tamanhos-110.png?v=${vTime}`
    };

    if (mapById[id]) return mapById[id];

    // Mapeamento por nicho/palavra-chave
    if (nome.includes('chinelo') || nome.includes('sandália') || nome.includes('sandalia')) {
      return `../img/guia-tamanhos-104.png?v=${vTime}`;
    }
    if (nome.includes('body') || nome.includes('cinta') || nome.includes('modelador')) {
      return `../img/guia-tamanhos-106.png?v=${vTime}`;
    }
    if (nome.includes('tênis') || nome.includes('tenis') || nome.includes('kappa')) {
      return `../img/guia-tamanhos-110.png?v=${vTime}`;
    }
    if (nome.includes('calça') || nome.includes('calca') || nome.includes('jeans')) {
      return `../img/guia-tamanhos-87.png?v=${vTime}`;
    }
    if (nome.includes('alfaiataria') || (nome.includes('conjunto') && nome.includes('feminino'))) {
      return `../img/guia-tamanhos-88.png?v=${vTime}`;
    }
    if (nome.includes('brasil')) {
      return `../img/guia-tamanhos-74.png?v=${vTime}`;
    }
    if (nome.includes('portugal')) {
      return `../img/guia-tamanhos-99.png?v=${vTime}`;
    }
    if (nome.includes('dry fit') || nome.includes('dryfit') || nome.includes('camiseta')) {
      return `../img/guia-tamanhos-75.png?v=${vTime}`;
    }
    if (nome.includes('vestido')) {
      return `../img/guia-tamanhos-103.png?v=${vTime}`;
    }

    return null;
  }
  window.getProductSizeGuideImage = getProductSizeGuideImage;

  function initSliderSizeGuideBadge() {
    const slider = document.querySelector('.image-slider');
    if (!slider) return;

    const sizeGuideImgSrc = getProductSizeGuideImage();
    if (!sizeGuideImgSrc) {
      const existingGuide = document.getElementById('slider-size-guide');
      if (existingGuide) existingGuide.remove();
      const existingToggle = slider.querySelector('.slider-counter-toggle');
      if (existingToggle) existingToggle.remove();
      const counter = slider.querySelector('.slider-counter');
      if (counter) {
        counter.classList.remove('is-hidden-by-toggle');
        counter.removeAttribute('data-has-tamanho');
        counter.style.removeProperty('display');
        const track = slider.querySelector('.slider-track');
        const totalImgs = track ? track.querySelectorAll('.slider-img, img').length : 1;
        counter.textContent = `1/${totalImgs}`;
      }
      return;
    }

    // 1. Injetar ou Atualizar container do Guia de Tamanhos no Slider
    let guideContainer = document.getElementById('slider-size-guide');
    if (!guideContainer) {
      guideContainer = document.createElement('div');
      guideContainer.id = 'slider-size-guide';
      guideContainer.className = 'slider-size-guide';
      guideContainer.style.cssText = 'position:absolute; top:0; left:0; width:100%; height:100%; background:#fff; z-index:5; display:none; align-items:center; justify-content:center; padding:16px 14px 44px 14px; box-sizing:border-box;';
      guideContainer.innerHTML = `<img src="${sizeGuideImgSrc}" alt="Guia de Tamanhos Oficial" style="max-width:100%; max-height:100%; object-fit:contain; display:block; margin:auto;" />`;
      slider.appendChild(guideContainer);
    } else {
      const guideImg = guideContainer.querySelector('img');
      if (guideImg && guideImg.getAttribute('src') !== sizeGuideImgSrc) {
        guideImg.src = sizeGuideImgSrc;
      }
    }

    // 2. Ocultar definitivamente o .slider-counter simples para zero fantasma atrás
    const counter = slider.querySelector('.slider-counter');
    if (counter) {
      counter.classList.add('is-hidden-by-toggle');
      counter.removeAttribute('data-has-tamanho');
      counter.style.setProperty('display', 'none', 'important');
    }

    // 3. Injetar o Toggle 1:1 [ 1/9 | Tamanho ] na escala exata (20px altura, 11px SemiBold, rgba(0,0,0,0.47))
    let toggle = slider.querySelector('.slider-counter-toggle');
    if (!toggle) {
      toggle = document.createElement('div');
      toggle.className = 'slider-counter-toggle';
      toggle.style.cssText = 'position:absolute; bottom:12px; right:16px; z-index:12; display:inline-flex; align-items:center; height:20px; background:rgba(0,0,0,0.47); border-radius:999px; padding:2px; box-sizing:border-box;';

      const track = slider.querySelector('.slider-track');
      const totalImgs = track ? track.querySelectorAll('.slider-img, img').length : 5;

      toggle.innerHTML = `
        <div id="btn-tab-fotos" style="height:16px; padding:0 7px; border-radius:999px; color:#ffffff; font-size:11px; font-weight:600; background:rgba(255,255,255,0.24); cursor:pointer; display:inline-flex; align-items:center; justify-content:center; transition:all 0.18s;">
          <span id="slider-count-cur">1</span>/${totalImgs}
        </div>
        <div id="btn-tab-tamanho" style="height:16px; padding:0 7px; border-radius:999px; color:rgba(255,255,255,0.88); font-size:11px; font-weight:600; background:transparent; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; transition:all 0.18s;">
          Tamanho
        </div>
      `;

      slider.appendChild(toggle);

      const btnFotos = toggle.querySelector('#btn-tab-fotos');
      const btnTamanho = toggle.querySelector('#btn-tab-tamanho');

      btnFotos.onclick = function(e) {
        if (e) { e.preventDefault(); e.stopPropagation(); }
        window.switchSliderTab('fotos', e);
      };

      btnTamanho.onclick = function(e) {
        if (e) { e.preventDefault(); e.stopPropagation(); }
        window.switchSliderTab('tamanho', e);
      };
    }
  }

  // Chamar no carregamento
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSliderSizeGuideBadge);
  } else {
    initSliderSizeGuideBadge();
  }
  window.initSliderSizeGuideBadge = initSliderSizeGuideBadge;
})();
