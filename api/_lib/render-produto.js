const fs = require('fs');
const path = require('path');
const produtosRegistry = require('../../data/produtos/index');
const { getOfficialProduct } = require('./store-state');

const ASSET_VERSION = '20261124_bf_only_v5';
const TEMPLATE_PATH = path.join(__dirname, '..', '..', 'templates', 'produto-modelo.html');

let cachedTemplate = null;

function getTemplate() {
  if (process.env.NODE_ENV === 'production' && cachedTemplate) {
    return cachedTemplate;
  }
  const tpl = fs.readFileSync(TEMPLATE_PATH, 'utf8');
  cachedTemplate = tpl;
  return tpl;
}

function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderStarsSvg(count) {
  const n = Math.max(1, Math.min(5, Number(count) || 5));
  const starFull = '<svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>';
  const starEmpty = '<svg class="star-icon" fill="#e0e0e0" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>';
  return starFull.repeat(n) + starEmpty.repeat(5 - n);
}

function renderSliderImgs(imgs, fallbackAlt) {
  if (!Array.isArray(imgs) || imgs.length === 0) return '';
  return imgs.map((img, i) => {
    const src = escapeHtml(img.src || '');
    const alt = escapeHtml(img.alt || `${fallbackAlt} - ${i + 1}`);
    return `<img alt="${alt}" class="slider-img" onerror="this.style.display='none'" src="${src}"/>`;
  }).join('\n        ');
}

function renderInstallment(text, highlight) {
  if (!text) return '';
  return `<div class="installment-row" onclick="handleAddToCart()" style="display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #161823; cursor: pointer; margin-bottom: 8px;">
        <div style="display: inline-flex; align-items: center; gap: 5px;">
          <svg fill="none" height="16" style="flex-shrink: 0;" viewbox="0 0 24 24" width="16">
            <rect fill="none" height="13.5" rx="2" stroke="#161823" stroke-width="1.8" width="20" x="2" y="4"></rect>
            <line stroke="#161823" stroke-width="1.8" x1="2" x2="22" y1="8" y2="8"></line>
            <circle cx="16" cy="14" fill="#fff" r="4.2" stroke="#161823" stroke-width="1.8"></circle>
            <polyline points="16 11.8 16 14 18 14" stroke="#161823" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"></polyline>
          </svg>
          <span style="font-weight: 500;">${escapeHtml(text)}</span>
          <span style="color: #df3564; font-weight: 400; margin-left: 2px;">${escapeHtml(highlight || 'sem juros')}</span>
        </div>
        <svg fill="none" height="14" stroke="#8a8b91" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" style="flex-shrink: 0; margin-left: auto;" viewbox="0 0 24 24" width="14"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>`;
}

function renderCoupons(couponMain, couponBonus) {
  if (!couponMain && !couponBonus) return '';
  const mainBadge = couponMain ? `<span class="product-badge-discount" style="display: inline-flex; align-items: center; gap: 4px; background: #fff; border: 1px solid #ffd2d8; color: #d60643; font-size: 11.5px; font-weight: 600; padding: 2.5px 7px; border-radius: 4px; line-height: 1.4; white-space: nowrap;">
            <svg fill="none" height="11" style="flex-shrink: 0;" viewbox="0 0 667 534" width="14" xmlns="http://www.w3.org/2000/svg">
              <path d="M666.666 166.667C640.145 166.667 614.71 177.203 595.956 195.956C577.202 214.71 566.666 240.145 566.666 266.667C566.666 293.189 577.202 318.624 595.956 337.378C614.71 356.131 640.145 366.667 666.666 366.667L666.666 466.667C666.666 484.348 659.642 501.305 647.14 513.808C634.637 526.31 617.681 533.334 600 533.334L466.666 533.334L466.666 470.601C466.666 461.76 463.154 453.281 456.903 447.03C450.652 440.779 442.174 437.267 433.333 437.267C424.492 437.267 416.014 440.779 409.763 447.03C403.512 453.281 400 461.76 400 470.601L400 533.334L66.666 533.334C48.9852 533.334 32.0287 526.31 19.5264 513.808C7.02395 501.305 1.13666e-05 484.348 1.01189e-05 466.667L1.44901e-05 366.666C55.4279 366.576 100.333 266.167 100.333 266.167C100.333 210.718 55.4279 165.758 2.3276e-05 165.668L2.76035e-05 66.667C3.0397e-05 48.9859 7.02397 32.0288 19.5264 19.5264C32.0287 7.02422 48.9852 8.86041e-05 66.666 4.76048e-07L400 1.50465e-05L400 62.7334C400 71.5739 403.512 80.0525 409.763 86.3037C416.014 92.5549 424.492 96.0674 433.333 96.0674C442.174 96.0674 450.652 92.5549 456.903 86.3037C463.154 80.0525 466.666 71.5739 466.666 62.7334L466.666 1.79606e-05L600 2.37888e-05C617.681 0.000113468 634.637 7.02425 647.14 19.5264C659.642 32.0288 666.666 48.9859 666.666 66.667L666.666 166.667ZM466.666 156.867C466.666 148.027 463.154 139.548 456.903 133.297C450.652 127.046 442.174 123.533 433.333 123.533C424.492 123.533 416.014 127.046 409.763 133.297C403.512 139.548 400 148.027 400 156.867L400 219.601C400 228.441 403.512 236.92 409.763 243.171C416.014 249.422 424.493 252.934 433.333 252.934C442.174 252.934 450.652 249.422 456.903 243.171C463.154 236.92 466.666 228.441 466.666 219.601L466.666 156.867ZM466.666 313.733C466.666 304.893 463.154 296.414 456.903 290.163C450.652 283.912 442.174 280.4 433.333 280.4C424.493 280.4 416.014 283.912 409.763 290.163C403.512 296.414 400 304.893 400 313.733L400 376.467C400 385.307 403.512 393.786 409.763 400.037C416.014 406.288 424.492 409.801 433.333 409.801C442.174 409.801 450.652 406.288 456.903 400.037C463.154 393.786 466.666 385.307 466.666 376.467L466.666 313.733Z" fill="#D60643"></path>
            </svg>
            <span>${escapeHtml(couponMain)}</span>
          </span>` : '';
  const bonusBadge = couponBonus ? `<span class="bonus-discount-badge" style="display: inline-flex; align-items: center; background: #fff; border: 1px solid #ffd2d8; color: #d60643; font-size: 11.5px; font-weight: 600; padding: 2.5px 7px; border-radius: 4px; line-height: 1.4; white-space: nowrap;">${escapeHtml(couponBonus)}</span>` : '';
  return `<div class="discount-ticket" onclick="handleAddToCart()" style="flex-wrap: nowrap; display: flex; align-items: center; justify-content: space-between; cursor: pointer; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 6px; min-width: 0; overflow: hidden; flex: 1;">
          ${mainBadge}
          ${bonusBadge}
        </div>
        <svg fill="none" height="14" stroke="#8a8b91" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" style="flex-shrink: 0; margin-left: auto;" viewbox="0 0 24 24" width="14"><polyline points="9 18 15 12 9 6"></polyline></svg>
      </div>`;
}

function renderReviews(reviews) {
  if (!Array.isArray(reviews) || reviews.length === 0) return '';
  return reviews.map((rev) => {
    const name = escapeHtml(rev.name || '');
    const avatar = escapeHtml(rev.avatar || '../img/reviews-avatars/default-avatar.svg');
    const stars = Number(rev.stars) || 5;
    const dateAttr = escapeHtml(rev.date || '');
    const varAttr = escapeHtml(rev.variation || '');
    const dateLine = escapeHtml(rev.date_line || [rev.date, rev.variation].filter(Boolean).join(' · '));
    const comment = escapeHtml(rev.comment || '');
    let photosHtml = '';
    if (Array.isArray(rev.photos) && rev.photos.length > 0) {
      const imgs = rev.photos.map((src) =>
        `<img alt="Foto da avaliação" decoding="async" loading="lazy" src="${escapeHtml(src)}" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>`
      ).join('\n          ');
      photosHtml = `\n        <div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px; flex-wrap: wrap;">\n          ${imgs}\n        </div>`;
    }
    return `<div class="review-card" data-author-avatar="${avatar}" data-author-comment="${comment}" data-author-date="${dateAttr}" data-author-name="${name}" data-author-stars="${stars}" data-author-variation="${varAttr}">
        <div class="review-header">
          <div class="review-user">
            <div class="review-avatar">
              <img alt="${name}" decoding="async" loading="lazy" src="${avatar}"/>
            </div>
            <div class="review-user-info">
              <div class="review-user-name">${name}</div>
              <div class="review-user-stars">${renderStarsSvg(stars)}</div>
              <div class="review-date">${dateLine}</div>
            </div>
          </div>
        </div>
        <p class="review-comment">${comment}</p>${photosHtml}
      </div>`;
  }).join('\n      ');
}

function renderDetails(details) {
  if (!Array.isArray(details) || details.length === 0) return '';
  const hasHidden = details.some((d) => d.hidden);
  const rows = details.map((d) => {
    const cls = d.hidden ? 'detail-row toggleable-row is-hidden' : 'detail-row';
    const st = d.hidden ? ' style="display: none !important;"' : '';
    return `<div class="${cls}"${st}>
            <span class="detail-label">${escapeHtml(d.label)}</span>
            <span class="detail-value">${escapeHtml(d.value)}</span>
          </div>`;
  }).join('\n          ');
  const toggleBtn = hasHidden
    ? `<button class="btn-detalhes-link" id="btn-toggle-detalhes" onclick="toggleProductDetails(this)" type="button"><span>Ver mais</span></button>`
    : '';
  return `<div class="product-details-block">
          <h3 class="about-subtitle">Detalhes</h3>
          <div class="details-attributes-grid">
          ${rows}
          </div>
          ${toggleBtn}
        </div>`;
}

function renderVideo(video) {
  if (!video || !video.src) return '';
  const src = escapeHtml(video.src);
  const posterAttr = video.poster ? ` poster="${escapeHtml(video.poster)}"` : '';
  const dur = escapeHtml(video.duration || '0:15');
  return `<div class="product-video-block">
          <h3 class="about-subtitle">Vídeo</h3>
          <div class="tiktok-video-card" id="tt-product-video-wrapper" onclick="toggleTTVideo(event)">
            <video id="tt-product-video"${posterAttr} playsinline="" webkit-playsinline="" preload="metadata" src="${src}"></video>
            <div class="tt-video-center-play" id="tt-center-play">
              <svg fill="#ffffff" height="54" viewbox="0 0 24 24" width="54" aria-hidden="true">
                <path d="M7.5 4.8C7.5 3.9 8.48 3.35 9.25 3.82L19.95 10.32C20.68 10.76 20.68 11.84 19.95 12.28L9.25 18.78C8.48 19.25 7.5 18.7 7.5 17.8V4.8Z"></path>
              </svg>
            </div>
            <div class="tt-video-bar" onclick="event.stopPropagation()">
              <button aria-label="Play/Pause" class="tt-video-btn-play" id="tt-btn-play" onclick="event.stopPropagation(); toggleTTVideo();" type="button">
                <svg fill="#ffffff" height="18" id="tt-icon-play" viewbox="0 0 24 24" width="18"><path d="M7 4.6C7 3.8 7.87 3.32 8.55 3.74L19.2 10.34C19.84 10.74 19.84 11.66 19.2 12.06L8.55 18.66C7.87 19.08 7 18.6 7 17.8V4.6Z"></path></svg>
                <svg fill="#ffffff" height="18" id="tt-icon-pause" style="display:none;" viewbox="0 0 24 24" width="18"><rect height="15" rx="1.2" width="4" x="6" y="4.5"></rect><rect height="15" rx="1.2" width="4" x="14" y="4.5"></rect></svg>
              </button>
              <span class="tt-video-time" id="tt-cur-time">00:00</span>
              <div class="tt-video-progress-bg" id="tt-progress-bg" onclick="seekTTVideo(event)">
                <div class="tt-video-progress-track">
                  <div class="tt-video-progress-fill" id="tt-progress-fill"></div>
                  <div class="tt-video-progress-thumb" id="tt-progress-thumb"></div>
                </div>
              </div>
              <span class="tt-video-time" id="tt-dur-time">${dur}</span>
              <button aria-label="Tela cheia" class="tt-video-btn-fs" id="tt-btn-fs" onclick="event.stopPropagation(); toggleTTFullscreen(event);" type="button">
                <svg fill="none" height="18" stroke="#ffffff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" viewbox="0 0 24 24" width="18">
                  <path d="M4 9V5a1 1 0 0 1 1-1h4"></path>
                  <path d="M20 9V5a1 1 0 0 0-1-1h-4"></path>
                  <path d="M4 15v4a1 1 0 0 0 1 1h4"></path>
                  <path d="M20 15v4a1 1 0 0 1-1 1h-4"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>`;
}

function renderRelated(related) {
  if (!Array.isArray(related) || related.length === 0) return '';
  const cards = related.map((r) => `<a class="related-card" href="${escapeHtml(r.href)}">
          <img alt="${escapeHtml(r.alt || r.name)}" class="related-img" decoding="async" loading="lazy" onerror="this.style.display='none'" src="${escapeHtml(r.img)}"/>
          <div class="related-info">
            <div class="related-name">${escapeHtml(r.name)}</div>
            <div class="related-price-row">
              <span class="related-price">${escapeHtml(r.price)}</span>
              <span class="related-price-original">${escapeHtml(r.price_original)}</span>
            </div>
            <div class="related-badges">
              <span class="related-discount">${escapeHtml(r.discount)}</span>
              <span class="badge-frete">· Frete grátis</span>
            </div>
            <div class="related-sold">${escapeHtml(r.sold)}</div>
          </div>
        </a>`).join('\n        ');
  return `<div class="related-section">
        <h3 class="related-title">Você também pode gostar</h3>
        <div class="related-grid">
        ${cards}
        </div>
      </div>`;
}

function renderExtraScripts(extraScripts) {
  if (!Array.isArray(extraScripts) || extraScripts.length === 0) return '';
  return extraScripts
    .map((src) => `<script src="${escapeHtml(src)}?v=${ASSET_VERSION}"></script>`)
    .join('\n');
}

function getProductData(id) {
  return getOfficialProduct(id);
}

function renderProdutoHtml(id) {
  const data = getProductData(id);
  if (!data) return { status: 404, html: '<h1>Produto não encontrado</h1>' };

  if (data.redirect) {
    return { status: 302, redirect: data.redirect };
  }

  let html = getTemplate();
  const safeJson = JSON.stringify(data.produto_atual || {}).replace(/</g, '\\u003c');
  const safeCreatorsJson = JSON.stringify(data.creators || []).replace(/</g, '\\u003c');
  const safeCreatorsCtx = escapeHtml(data.creator_context || 'general');

  const replacements = {
    '{{ASSET_VERSION}}': ASSET_VERSION,
    '{{TITLE}}': escapeHtml(data.title || `${data.product_title} - Stone Shop`),
    '{{META_DESCRIPTION}}': escapeHtml(data.meta_description || data.product_title || ''),
    '{{SLIDER_IMGS_HTML}}': renderSliderImgs(data.slider_imgs, data.product_title || ''),
    '{{SLIDER_COUNT}}': String((data.slider_imgs && data.slider_imgs.length) || 1),
    '{{DISCOUNT_BADGE}}': escapeHtml(data.discount_badge || '-50%'),
    '{{PRICE_INT}}': escapeHtml(data.price_int || '0'),
    '{{PRICE_CENTS}}': escapeHtml(data.price_cents || ',00'),
    '{{PRICE_ORIGINAL}}': escapeHtml(data.price_original || ''),
    '{{INSTALLMENT_HTML}}': renderInstallment(data.installment_text, data.installment_highlight),
    '{{COUPONS_HTML}}': renderCoupons(data.coupon_main, data.coupon_bonus),
    '{{PRODUCT_TITLE}}': escapeHtml(data.product_title || ''),
    '{{RATING_SCORE}}': escapeHtml(data.rating_score || '4.8'),
    '{{RATING_COUNT}}': escapeHtml(data.rating_count || `(${(data.reviews || []).length})`),
    '{{SOLD_COUNT}}': escapeHtml(data.sold_count || '1.2K vendidos'),
    '{{FRETE_ORIGINAL}}': escapeHtml(data.frete_original || 'R$ 15,60'),
    '{{REVIEWS_HEADER}}': escapeHtml(data.reviews_header || `Avaliações dos clientes (${(data.reviews || []).length})`),
    '{{REVIEWS_AVG}}': escapeHtml(data.reviews_avg || data.rating_score || '4,8'),
    '{{REVIEWS_AVG_COMMA}}': escapeHtml(String(data.reviews_avg || data.rating_score || '4,8').replace('.', ',')),
    '{{REVIEWS_CARDS_HTML}}': renderReviews(data.reviews),
    '{{DETAILS_HTML}}': renderDetails(data.details),
    '{{VIDEO_HTML}}': renderVideo(data.video),
    '{{SIZE_GUIDE_HTML}}': data.size_guide_html || '',
    '{{DESCRIPTION_HTML}}': data.description_html || '',
    '{{RELATED_HTML}}': renderRelated(data.related),
    '{{PRODUTO_ATUAL_JSON}}': safeJson,
    '{{PRODUTO_CRIADORES_JSON}}': safeCreatorsJson,
    '{{PRODUTO_CRIADORES_CTX}}': safeCreatorsCtx,
    '{{EXTRA_SCRIPTS_HTML}}': renderExtraScripts(data.extra_scripts),
  };

  for (const [token, val] of Object.entries(replacements)) {
    html = html.split(token).join(val);
  }

  return { status: 200, html };
}

module.exports = {
  ASSET_VERSION,
  getProductData,
  renderProdutoHtml,
  listProductIds: () => Object.keys(produtosRegistry),
};
