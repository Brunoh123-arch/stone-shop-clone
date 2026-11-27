/**
 * STONE SHOP CORE — CENTRAL DE VÍDEOS TIKTOK ADS (ADS STUDIO)
 * Tela dedicada para subir campanhas no TikTok Ads Manager em 1 clique:
 *  - Nome completo + foto + preço PIX + desconto de cada produto
 *  - Todos os vídeos MP4 limpos (Principal + Criadores UGC) com player sob demanda
 *  - Download direto do MP4 renomeado para o TikTok Ads Manager
 *  - Link UTM limpo (/produto-ID), URL MP4 limpa e Copy/Headline pronta para anúncio
 *  - Controle de status de campanha por produto (Fila / Testando / Rodando)
 */
(function () {
  const STORAGE_STATUS_KEY = 'STONE_ADS_CAMPAIGN_STATUS_V1';
  const STORAGE_FAV_KEY = 'STONE_ADS_FAV_VIDEO_V1';

  let adsManifest = null;
  let adsStatusMap = {};
  let adsFavMap = {};
  let adsActiveVideoIdx = {}; // productId -> index inside buildVideoList(prod)
  let adsFilterChip = 'new_bf'; // padrão: lançamentos Black Friday primeiro, mas 1 clique mostra todos
  let adsSortBy = 'newest';
  let adsCategoryFilter = 'todas';
  let currentKitProdId = null;

  function esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function cleanUrl(u) {
    return String(u || '').split('#')[0].split('?')[0].trim();
  }

  function formatBRL(v) {
    return 'R$ ' + Number(v || 0).toFixed(2).replace('.', ',');
  }

  function loadLocalState() {
    try { adsStatusMap = JSON.parse(localStorage.getItem(STORAGE_STATUS_KEY) || '{}') || {}; } catch (_) { adsStatusMap = {}; }
    try { adsFavMap = JSON.parse(localStorage.getItem(STORAGE_FAV_KEY) || '{}') || {}; } catch (_) { adsFavMap = {}; }
  }

  function saveLocalState() {
    try { localStorage.setItem(STORAGE_STATUS_KEY, JSON.stringify(adsStatusMap)); } catch (_) {}
    try { localStorage.setItem(STORAGE_FAV_KEY, JSON.stringify(adsFavMap)); } catch (_) {}
  }

  function buildVideoList(prod) {
    const list = [];
    const seen = new Set();

    if (prod.video && prod.video.src) {
      const url = cleanUrl(prod.video.src);
      if (url && !seen.has(url)) {
        seen.add(url);
        list.push({
          slot: 'principal',
          label: 'Principal Ads',
          badge: '🏆 PRINCIPAL ADS',
          url,
          poster: prod.video.poster || prod.img || 'logo.png',
          duration: prod.video.duration || '',
          catboxId: prod.video.catbox_id || url.split('/').pop(),
          author: 'Stone Shop Oficial',
          desc: prod.title,
        });
      }
    }

    (prod.creators || []).forEach((c, idx) => {
      const url = cleanUrl(c && c.video);
      if (!url || seen.has(url)) return;
      seen.add(url);
      list.push({
        slot: `ugc_${idx + 1}`,
        label: `UGC #${idx + 1}`,
        badge: `📱 UGC #${idx + 1}`,
        url,
        poster: c.poster || c.avatar || prod.img || 'logo.png',
        duration: '',
        catboxId: c.catbox_id || url.split('/').pop(),
        author: c.username ? `@${c.username}` : (c.name || `Criador ${idx + 1}`),
        desc: c.description || '',
      });
    });

    return list;
  }

  function getSelectedVideo(prod) {
    const vids = buildVideoList(prod);
    if (!vids.length) return { vids, idx: 0, current: null };
    if (adsActiveVideoIdx[prod.id] === undefined) {
      const favUrl = adsFavMap[String(prod.id)];
      const favIdx = favUrl ? vids.findIndex((v) => v.url === favUrl) : -1;
      adsActiveVideoIdx[prod.id] = favIdx >= 0 ? favIdx : 0;
    }
    const idx = Math.min(adsActiveVideoIdx[prod.id] || 0, vids.length - 1);
    return { vids, idx, current: vids[idx] };
  }

  function getEffectivePrice(prod) {
    const ov = (window.__STONE_SERVER_OVERRIDES__ && window.__STONE_SERVER_OVERRIDES__[String(prod.id)]) || {};
    const localOv = (window.customPrecos && window.customPrecos[prod.id]) || {};
    return Number(ov.preco || localOv.preco || prod.preco || 0);
  }

  function buildUtmUrl(prod, videoIdx = 0) {
    const slug = (prod.slug || `prod${prod.id}`).replace(/[^a-z0-9-]/gi, '').slice(0, 22);
    return `https://stoneshopclone.vercel.app/produto-${prod.id}?utm_source=tiktok&utm_medium=cpc&utm_campaign=bf_${prod.id}_${slug}&utm_content=vid_${videoIdx + 1}`;
  }

  function buildAdCopy(prod, videoIdx = 0) {
    const price = getEffectivePrice(prod);
    const priceStr = formatBRL(price);
    const origStr = prod.price_original_str || (prod.preco_antigo ? formatBRL(prod.preco_antigo) : '');
    const disc = prod.discount_pct ? `${prod.discount_pct}% OFF` : (prod.discount_badge || 'OFERTA BLACK FRIDAY');
    const utm = buildUtmUrl(prod, videoIdx);
    const { current } = getSelectedVideo(prod);

    const headline = `🔥 ${disc} HOJE: ${prod.title.slice(0, 48)}${prod.title.length > 48 ? '...' : ''}`;
    const primaryText = [
      `😱 Susto no preço Black Friday! ${prod.title}`,
      origStr ? `De ${origStr} por apenas ${priceStr} no PIX (Frete Grátis Brasil 🇧🇷)` : `Por apenas ${priceStr} no PIX com Frete Grátis Brasil 🇧🇷`,
      `✅ Envio rápido com rastreio · Últimas unidades do lote promocional!`,
      `👇 Garanta o seu agora antes que acabe:`,
    ].join('\n');

    return {
      headline,
      primaryText,
      cta: 'Comprar Agora',
      utm,
      videoUrl: current ? current.url : '',
      fullText: `📦 PRODUTO #${prod.id}: ${prod.title}\n💰 PIX: ${priceStr}${origStr ? ` (Antes: ${origStr} · ${disc})` : ''}\n\n🎯 HEADLINE TIKTOK ADS:\n${headline}\n\n✍️ TEXTO DO ANÚNCIO:\n${primaryText}\n\n🔗 LINK DE DESTINO (UTM):\n${utm}\n\n🎬 VÍDEO MP4 LIMPO:\n${current ? current.url : 'N/A'}`,
    };
  }

  function getStatusMeta(st) {
    if (st === 'running') return { key: 'running', label: '🟢 Rodando Ads', cls: 'st-running' };
    if (st === 'testing') return { key: 'testing', label: '🟡 Em Teste', cls: 'st-testing' };
    return { key: 'idle', label: '⚪ Na Fila', cls: 'st-idle' };
  }

  function injectAdsStyles() {
    if (document.getElementById('ads-studio-styles')) return;
    const st = document.createElement('style');
    st.id = 'ads-studio-styles';
    st.textContent = `
      .ads-hero {
        background: linear-gradient(135deg, rgba(254, 44, 85, 0.14) 0%, rgba(14, 19, 31, 0.96) 55%, rgba(37, 244, 238, 0.08) 100%);
        border: 1px solid rgba(254, 44, 85, 0.28);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 16px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 14px;
      }
      .ads-hero-title {
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -0.4px;
        display: flex;
        align-items: center;
        gap: 9px;
        flex-wrap: wrap;
      }
      .ads-live-pill {
        font-size: 10px;
        font-weight: 800;
        padding: 3px 9px;
        border-radius: 999px;
        background: #fe2c55;
        color: #fff;
        letter-spacing: 0.6px;
        text-transform: uppercase;
      }
      .ads-hero-sub {
        font-size: 12.5px;
        color: #cbd5e1;
        margin-top: 4px;
        max-width: 680px;
      }
      .ads-hero-actions {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
      }
      .ads-mini-kpis {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-bottom: 16px;
      }
      @media (min-width: 768px) {
        .ads-mini-kpis { grid-template-columns: repeat(4, 1fr); }
      }
      .ads-kpi {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 12px 14px;
      }
      .ads-kpi-num { font-size: 20px; font-weight: 800; color: #f8fafc; line-height: 1.15; }
      .ads-kpi-lbl { font-size: 11px; color: #94a3b8; margin-top: 3px; font-weight: 600; }

      .ads-toolbar {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 16px;
        display: flex;
        flex-direction: column;
        gap: 12px;
      }
      .ads-toolbar-top {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
      }
      @media (min-width: 768px) {
        .ads-toolbar-top { grid-template-columns: 1fr 200px 190px; }
      }
      .ads-chips {
        display: flex;
        gap: 7px;
        overflow-x: auto;
        padding-bottom: 2px;
        scrollbar-width: none;
      }
      .ads-chips::-webkit-scrollbar { display: none; }
      .ads-chip {
        background: #0b101b;
        border: 1px solid rgba(255,255,255,0.1);
        color: #cbd5e1;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 12px;
        border-radius: 999px;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.16s ease;
      }
      .ads-chip:hover { border-color: rgba(254, 44, 85, 0.5); color: #fff; }
      .ads-chip.active {
        background: #fe2c55;
        border-color: #fe2c55;
        color: #fff;
        box-shadow: 0 2px 12px rgba(254, 44, 85, 0.32);
      }

      .ads-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 16px;
      }
      @media (min-width: 720px) {
        .ads-grid { grid-template-columns: repeat(2, 1fr); }
      }
      @media (min-width: 1120px) {
        .ads-grid { grid-template-columns: repeat(3, 1fr); }
      }

      .ads-card {
        background: var(--bg-card);
        border: 1.5px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
      }
      .ads-card:hover {
        border-color: rgba(254, 44, 85, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.42);
      }
      .ads-card.st-running {
        border-color: rgba(16, 185, 129, 0.55);
        box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.2);
      }
      .ads-card.st-testing {
        border-color: rgba(245, 158, 11, 0.5);
      }

      .ads-card-head {
        padding: 13px 14px 11px;
        display: flex;
        gap: 11px;
        align-items: flex-start;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      }
      .ads-prod-thumb {
        width: 56px;
        height: 56px;
        border-radius: 10px;
        object-fit: cover;
        background: #fff;
        border: 1px solid rgba(255, 255, 255, 0.12);
        flex-shrink: 0;
      }
      .ads-prod-meta {
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 4px;
      }
      .ads-prod-top-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 6px;
        flex-wrap: wrap;
      }
      .ads-id-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 800;
        color: #fff;
        background: #1f293d;
        padding: 2px 7px;
        border-radius: 6px;
      }
      .ads-status-btn {
        font-size: 10.5px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.12);
        background: #0b101b;
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .ads-status-btn.st-running {
        background: rgba(16, 185, 129, 0.16);
        border-color: rgba(16, 185, 129, 0.45);
        color: #34d399;
      }
      .ads-status-btn.st-testing {
        background: rgba(245, 158, 11, 0.16);
        border-color: rgba(245, 158, 11, 0.45);
        color: #fbbf24;
      }
      .ads-prod-name {
        font-size: 13.5px;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.32;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      .ads-price-strip {
        display: flex;
        align-items: baseline;
        gap: 7px;
        flex-wrap: wrap;
      }
      .ads-price-now {
        font-family: 'JetBrains Mono', monospace;
        font-size: 16px;
        font-weight: 800;
        color: #34d399;
      }
      .ads-price-old {
        font-size: 11px;
        color: #64748b;
        text-decoration: line-through;
      }
      .ads-disc-pill {
        font-size: 10px;
        font-weight: 800;
        padding: 1px 6px;
        border-radius: 4px;
        background: rgba(254, 44, 85, 0.16);
        color: #ff6482;
      }

      /* Stage de Vídeo Ads */
      .ads-video-stage {
        position: relative;
        width: 100%;
        aspect-ratio: 16 / 11;
        background: #05070c;
        overflow: hidden;
        cursor: pointer;
      }
      .ads-video-stage img.ads-poster {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
        filter: brightness(0.84);
        transition: transform 0.25s ease, filter 0.25s ease;
      }
      .ads-video-stage:hover img.ads-poster {
        transform: scale(1.03);
        filter: brightness(0.95);
      }
      .ads-video-stage video {
        width: 100%;
        height: 100%;
        object-fit: contain;
        background: #000;
        display: block;
      }
      .ads-play-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: linear-gradient(180deg, rgba(0,0,0,0.28) 0%, rgba(0,0,0,0.12) 45%, rgba(0,0,0,0.72) 100%);
      }
      .ads-play-circle {
        width: 54px;
        height: 54px;
        border-radius: 50%;
        background: rgba(254, 44, 85, 0.92);
        color: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 0 6px rgba(254, 44, 85, 0.24), 0 8px 20px rgba(0,0,0,0.5);
        transition: transform 0.16s ease;
      }
      .ads-video-stage:hover .ads-play-circle { transform: scale(1.08); }
      .ads-stage-top-badges {
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        pointer-events: none;
        z-index: 2;
      }
      .ads-vid-badge {
        font-size: 10.5px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(7, 9, 14, 0.82);
        backdrop-filter: blur(8px);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.16);
      }
      .ads-vid-count-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.9);
        color: #03150e;
      }
      .ads-stage-bottom-bar {
        position: absolute;
        bottom: 8px;
        left: 10px;
        right: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        pointer-events: none;
        z-index: 2;
      }
      .ads-author-pill {
        font-size: 11px;
        font-weight: 700;
        color: #f8fafc;
        text-shadow: 0 1px 4px rgba(0,0,0,0.9);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      /* Seletor de Criativos do Produto */
      .ads-variants-bar {
        padding: 10px 12px 6px;
        display: flex;
        gap: 6px;
        overflow-x: auto;
        background: rgba(7, 9, 14, 0.6);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        scrollbar-width: thin;
      }
      .ads-vid-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 9px;
        border-radius: 7px;
        background: #131b2e;
        border: 1px solid rgba(255, 255, 255, 0.09);
        color: #94a3b8;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
        flex-shrink: 0;
        transition: all 0.14s ease;
      }
      .ads-vid-pill:hover { color: #fff; border-color: rgba(255,255,255,0.22); }
      .ads-vid-pill.active {
        background: rgba(254, 44, 85, 0.18);
        border-color: #fe2c55;
        color: #fff;
      }
      .ads-vid-pill img {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        object-fit: cover;
      }

      /* Ações do Card Ads */
      .ads-card-body {
        padding: 12px 14px 14px;
        display: flex;
        flex-direction: column;
        gap: 9px;
        flex: 1;
        justify-content: flex-end;
      }
      .ads-url-box {
        display: flex;
        align-items: center;
        gap: 6px;
        background: #07090e;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 5px 8px;
      }
      .ads-url-input {
        flex: 1;
        background: transparent;
        border: none;
        color: #94a3b8;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        outline: none;
        min-width: 0;
      }
      .ads-btn-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 7px;
      }
      .ads-btn {
        height: 36px;
        border-radius: 9px;
        border: 1px solid var(--border);
        background: #141c2e;
        color: #f8fafc;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        text-decoration: none;
        transition: all 0.15s ease;
        padding: 0 10px;
      }
      .ads-btn:hover { background: #1d2840; border-color: rgba(255,255,255,0.2); }
      .ads-btn-download {
        background: linear-gradient(135deg, #fe2c55, #e11d48);
        border-color: #fe2c55;
        color: #fff;
        font-weight: 800;
      }
      .ads-btn-download:hover { filter: brightness(1.1); }
      .ads-btn-green {
        background: rgba(16, 185, 129, 0.16);
        border-color: rgba(16, 185, 129, 0.4);
        color: #34d399;
      }
      .ads-btn-green:hover { background: rgba(16, 185, 129, 0.26); color: #6ee7b7; }
      .ads-btn-full {
        grid-column: 1 / -1;
      }

      /* Modal Kit Subida TikTok Ads */
      .ads-kit-modal {
        position: fixed;
        inset: 0;
        z-index: 100000;
        background: rgba(3, 6, 12, 0.86);
        backdrop-filter: blur(10px);
        display: none;
        align-items: center;
        justify-content: center;
        padding: 14px;
      }
      .ads-kit-modal.open { display: flex; }
      .ads-kit-box {
        width: 100%;
        max-width: 780px;
        max-height: 92dvh;
        background: #0e131f;
        border: 1px solid rgba(254, 44, 85, 0.35);
        border-radius: 18px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        box-shadow: 0 28px 70px rgba(0, 0, 0, 0.72);
      }
      .ads-kit-head {
        padding: 15px 18px;
        background: #121929;
        border-bottom: 1px solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
      }
      .ads-kit-body {
        padding: 16px 18px;
        overflow-y: auto;
        display: grid;
        grid-template-columns: 1fr;
        gap: 16px;
      }
      @media (min-width: 700px) {
        .ads-kit-body { grid-template-columns: 240px 1fr; }
      }
      .ads-kit-textarea {
        width: 100%;
        min-height: 112px;
        background: #07090e;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px;
        color: #f8fafc;
        padding: 10px 12px;
        font-family: inherit;
        font-size: 12.5px;
        line-height: 1.48;
        resize: vertical;
      }
    `;
    document.head.appendChild(st);
  }

  function createKitModal() {
    if (document.getElementById('adsKitModal')) return;
    const el = document.createElement('div');
    el.id = 'adsKitModal';
    el.className = 'ads-kit-modal';
    el.innerHTML = `
      <div class="ads-kit-box" onclick="event.stopPropagation()">
        <div class="ads-kit-head">
          <div style="min-width:0;">
            <div style="font-size:15px; font-weight:800; color:#fff;" id="adsKitTitle">🚀 Kit Subida TikTok Ads</div>
            <div style="font-size:11.5px; color:#94a3b8; margin-top:2px;" id="adsKitSub">Pronto para colar no TikTok Ads Manager</div>
          </div>
          <button type="button" onclick="window.closeAdsKitModal()" style="background:#1e293b; border:1px solid rgba(255,255,255,0.15); color:#fff; width:34px; height:34px; border-radius:8px; cursor:pointer; font-size:16px;">✕</button>
        </div>
        <div class="ads-kit-body" id="adsKitBody"></div>
      </div>
    `;
    el.addEventListener('click', () => window.closeAdsKitModal());
    document.body.appendChild(el);
  }

  function getFilteredAdsProducts() {
    if (!adsManifest || !Array.isArray(adsManifest.products)) return [];
    const term = (document.getElementById('adsSearchInput')?.value || '').toLowerCase().trim();

    let list = adsManifest.products.filter((p) => {
      const vids = buildVideoList(p);
      if (!vids.length) return false;

      const st = adsStatusMap[String(p.id)] || 'idle';
      const price = getEffectivePrice(p);

      if (adsFilterChip === 'new_bf' && !p.is_new_bf) return false;
      if (adsFilterChip === 'running' && st !== 'running') return false;
      if (adsFilterChip === 'testing' && st !== 'testing') return false;
      if (adsFilterChip === 'high_anchor' && price < 50) return false;
      if (adsFilterChip === 'impulse' && price > 50) return false;

      if (adsCategoryFilter !== 'todas' && p.category !== adsCategoryFilter) return false;

      if (term) {
        const hitId = String(p.id) === term || `#${p.id}` === term || String(p.id).includes(term);
        const hitTitle = (p.title || '').toLowerCase().includes(term);
        const hitCat = (p.category || '').toLowerCase().includes(term);
        const hitVid = vids.some((v) =>
          (v.catboxId || '').toLowerCase().includes(term) ||
          (v.author || '').toLowerCase().includes(term)
        );
        if (!hitId && !hitTitle && !hitCat && !hitVid) return false;
      }
      return true;
    });

    if (adsSortBy === 'newest') list.sort((a, b) => b.id - a.id);
    else if (adsSortBy === 'most_videos') list.sort((a, b) => buildVideoList(b).length - buildVideoList(a).length);
    else if (adsSortBy === 'biggest_disc') list.sort((a, b) => (b.discount_pct || 0) - (a.discount_pct || 0));
    else if (adsSortBy === 'price_asc') list.sort((a, b) => getEffectivePrice(a) - getEffectivePrice(b));
    else if (adsSortBy === 'price_desc') list.sort((a, b) => getEffectivePrice(b) - getEffectivePrice(a));

    return list;
  }

  function updateAdsKpis() {
    if (!adsManifest) return;
    const prods = adsManifest.products || [];
    const totalProds = prods.filter((p) => buildVideoList(p).length > 0).length;
    const totalVids = prods.reduce((acc, p) => acc + buildVideoList(p).length, 0);
    const runningCount = Object.values(adsStatusMap).filter((s) => s === 'running').length;
    const testingCount = Object.values(adsStatusMap).filter((s) => s === 'testing').length;

    const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setTxt('adsKpiProds', totalProds);
    setTxt('adsKpiVids', totalVids);
    setTxt('adsKpiRunning', runningCount);
    setTxt('adsKpiTesting', testingCount);
    setTxt('badgeAdsTop', totalVids);
    setTxt('bNavAdsBadge', totalProds);
    setTxt('kpiAdsTotal', `${totalVids} vídeos`);
  }

  function renderAdsGrid() {
    const grid = document.getElementById('adsVideosGrid');
    if (!grid) return;

    const list = getFilteredAdsProducts();
    const countLbl = document.getElementById('adsShowingCount');
    if (countLbl) countLbl.textContent = `Exibindo ${list.length} produto(s) prontos para subir no TikTok Ads`;

    if (!list.length) {
      grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align:center; padding:48px 16px; background:var(--bg-card); border:1px dashed var(--border); border-radius:14px; color:#94a3b8;">
          <div style="font-size:34px; margin-bottom:8px;">🎬</div>
          <div style="font-size:15px; font-weight:800; color:#f8fafc;">Nenhum produto encontrado neste filtro</div>
          <div style="font-size:12.5px; margin-top:4px;">Troque o filtro acima ou clique em "Todos os Produtos" para ver os 85 produtos com vídeo.</div>
          <button type="button" class="ads-btn ads-btn-download" style="margin-top:14px;" onclick="window.setAdsFilterChip('all')">Mostrar Todos os Produtos</button>
        </div>
      `;
      return;
    }

    grid.innerHTML = list.map((p) => {
      const { vids, idx, current } = getSelectedVideo(p);
      const price = getEffectivePrice(p);
      const origStr = p.price_original_str || (p.preco_antigo ? formatBRL(p.preco_antigo) : '');
      const stMeta = getStatusMeta(adsStatusMap[String(p.id)] || 'idle');
      const isFav = adsFavMap[String(p.id)] === (current && current.url);

      return `
        <article class="ads-card ${stMeta.cls}" id="adsCard-${p.id}">
          <div class="ads-card-head">
            <img src="${esc(p.img || 'logo.png')}" alt="${esc(p.title)}" class="ads-prod-thumb" loading="lazy" onerror="this.src='logo.png'">
            <div class="ads-prod-meta">
              <div class="ads-prod-top-row">
                <div style="display:flex; align-items:center; gap:5px; flex-wrap:wrap;">
                  <span class="ads-id-tag">#${p.id}</span>
                  ${p.is_new_bf ? `<span style="font-size:9.5px; font-weight:800; padding:2px 6px; border-radius:5px; background:rgba(254,44,85,0.18); color:#ff6482;">BF NOVO</span>` : ''}
                  <span style="font-size:10px; color:#94a3b8; font-weight:600;">${esc(p.category)}</span>
                </div>
                <button type="button" class="ads-status-btn ${stMeta.cls}" onclick="window.cycleAdsStatus(${p.id})" title="Clique para alternar: Fila → Em Teste → Rodando Ads">${stMeta.label}</button>
              </div>
              <div class="ads-prod-name" title="${esc(p.title)}">${esc(p.title)}</div>
              <div class="ads-price-strip">
                <span class="ads-price-now">${formatBRL(price)}</span>
                ${origStr ? `<span class="ads-price-old">${esc(origStr)}</span>` : ''}
                ${p.discount_badge ? `<span class="ads-disc-pill">${esc(p.discount_badge)}</span>` : ''}
              </div>
            </div>
          </div>

          <!-- Palco do Vídeo (carrega MP4 sob demanda ao clicar em Play) -->
          <div class="ads-video-stage" id="adsStage-${p.id}" onclick="window.playInlineAdsVideo(${p.id})">
            <div class="ads-stage-top-badges">
              <span class="ads-vid-badge">${esc(current.badge)}${isFav ? ' ⭐' : ''}</span>
              <span class="ads-vid-count-badge">${vids.length} ${vids.length === 1 ? 'vídeo' : 'vídeos'}</span>
            </div>
            <img src="${esc(current.poster)}" alt="Vídeo Ads ${esc(p.title)}" class="ads-poster" loading="lazy" onerror="this.src='${esc(p.img || 'logo.png')}'">
            <div class="ads-play-overlay">
              <div class="ads-play-circle">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 4 20 12 6 20 6 4"></polygon></svg>
              </div>
              <span style="font-size:11px; font-weight:700; color:#fff; background:rgba(0,0,0,0.65); padding:3px 9px; border-radius:999px;">Assistir Criativo (${esc(current.catboxId)})</span>
            </div>
            <div class="ads-stage-bottom-bar">
              <span class="ads-author-pill">${esc(current.author)}</span>
            </div>
          </div>

          <!-- Barra de troca de Criativos do Produto -->
          <div class="ads-variants-bar">
            ${vids.map((v, vIdx) => `
              <button type="button" class="ads-vid-pill ${vIdx === idx ? 'active' : ''}" onclick="window.selectAdsVideo(${p.id}, ${vIdx})" title="${esc(v.author)} — ${esc(v.catboxId)}">
                <img src="${esc(v.poster)}" alt="" loading="lazy" onerror="this.src='logo.png'">
                <span>${vIdx === 0 ? '🏆 Principal' : `UGC #${vIdx}`}</span>
              </button>
            `).join('')}
          </div>

          <div class="ads-card-body">
            <!-- Link MP4 Limpo -->
            <div class="ads-url-box">
              <span style="font-size:10px; font-weight:800; color:#fe2c55; flex-shrink:0;">MP4</span>
              <input type="text" readonly class="ads-url-input" value="${esc(current.url)}" onclick="this.select()">
              <button type="button" onclick="window.copyAdsText('${esc(current.url)}', 'Link MP4 limpo copiado!')" title="Copiar link MP4" style="background:none; border:none; color:#cbd5e1; cursor:pointer; font-size:13px; padding:2px 4px;">📋</button>
              <button type="button" onclick="window.toggleFavAdsVideo(${p.id})" title="Fixar este vídeo como Criativo Favorito do produto" style="background:none; border:none; color:${isFav ? '#fbbf24' : '#64748b'}; cursor:pointer; font-size:14px; padding:2px 4px;">★</button>
            </div>

            <!-- Botões de Ação Rápida TikTok Ads -->
            <div class="ads-btn-grid">
              <button type="button" class="ads-btn ads-btn-download" id="adsDlBtn-${p.id}" onclick="window.downloadAdsVideo(${p.id})">
                ⬇️ Baixar MP4 Ads
              </button>
              <button type="button" class="ads-btn ads-btn-green" onclick="window.copyAdsUtm(${p.id})">
                🔗 Copiar Link UTM
              </button>
              <button type="button" class="ads-btn" onclick="window.openAdsKitModal(${p.id})">
                ✍️ Copy + Kit Ads
              </button>
              <a href="/produto-${p.id}?owner=1" target="_blank" class="ads-btn">
                🛍️ Ver Página ↗
              </a>
            </div>
          </div>
        </article>
      `;
    }).join('');
  }

  window.playInlineAdsVideo = function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    const { current } = getSelectedVideo(prod);
    if (!current) return;
    const stage = document.getElementById(`adsStage-${pid}`);
    if (!stage || stage.querySelector('video')) return;

    stage.onclick = null;
    stage.innerHTML = `
      <video controls autoplay playsinline src="${esc(current.url)}" poster="${esc(current.poster)}" style="width:100%; height:100%; object-fit:contain; background:#000;"></video>
    `;
  };

  window.selectAdsVideo = function (pid, vIdx) {
    adsActiveVideoIdx[pid] = Number(vIdx);
    renderAdsGrid();
  };

  window.toggleFavAdsVideo = function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    const { current } = getSelectedVideo(prod);
    if (!current) return;

    if (adsFavMap[String(pid)] === current.url) {
      delete adsFavMap[String(pid)];
      window.showToast && window.showToast(`Favorito removido do Produto #${pid}`, 'info');
    } else {
      adsFavMap[String(pid)] = current.url;
      window.showToast && window.showToast(`⭐ Vídeo fixado como Criativo Favorito do #${pid}!`, 'success');
    }
    saveLocalState();
    syncProductAdsOverride(pid);
    renderAdsGrid();
  };

  window.cycleAdsStatus = function (pid) {
    const cur = adsStatusMap[String(pid)] || 'idle';
    const next = cur === 'idle' ? 'testing' : (cur === 'testing' ? 'running' : 'idle');
    adsStatusMap[String(pid)] = next;
    saveLocalState();
    syncProductAdsOverride(pid);
    updateAdsKpis();
    renderAdsGrid();
    const meta = getStatusMeta(next);
    window.showToast && window.showToast(`Produto #${pid}: ${meta.label}`, 'success');
  };

  function syncProductAdsOverride(pid) {
    fetch('/api/admin-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'save_product_override',
        productId: pid,
        patch: {
          ads_status: adsStatusMap[String(pid)] || 'idle',
          ads_fav_video: adsFavMap[String(pid)] || '',
        },
      }),
    }).catch(() => {});
  }

  window.copyAdsText = function (txt, toastMsg = 'Copiado!') {
    navigator.clipboard.writeText(txt).then(() => {
      window.showToast && window.showToast(toastMsg, 'success');
    }).catch(() => {
      prompt('Copie abaixo:', txt);
    });
  };

  window.copyAdsUtm = function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    const { idx } = getSelectedVideo(prod);
    const utm = buildUtmUrl(prod, idx);
    window.copyAdsText(utm, `🔗 Link TikTok Ads UTM do Produto #${pid} copiado!`);
  };

  window.downloadAdsVideo = async function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    const { idx, current } = getSelectedVideo(prod);
    if (!current || !current.url) return;

    const btn = document.getElementById(`adsDlBtn-${pid}`);
    const origLabel = btn ? btn.innerHTML : '';
    const fileName = `StoneShop_Prod${prod.id}_${(prod.slug || 'produto').slice(0, 22)}_Ad${idx + 1}.mp4`;

    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '⏳ Baixando MP4...';
    }
    try {
      const resp = await fetch(current.url, { mode: 'cors' });
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      const blob = await resp.blob();
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(blobUrl), 8000);
      window.showToast && window.showToast(`⬇️ Baixado: ${fileName}`, 'success');
    } catch (e) {
      window.open(current.url, '_blank');
      window.showToast && window.showToast('Vídeo aberto em nova aba — clique em ⋮ → Fazer download.', 'info');
    } finally {
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = origLabel;
      }
    }
  };

  window.openAdsKitModal = function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    currentKitProdId = prod.id;

    const { idx, current } = getSelectedVideo(prod);
    const copy = buildAdCopy(prod, idx);
    const price = getEffectivePrice(prod);

    document.getElementById('adsKitTitle').textContent = `🚀 Kit TikTok Ads — #${prod.id} ${prod.title.slice(0, 48)}`;
    document.getElementById('adsKitSub').textContent = `PIX ${formatBRL(price)} · ${prod.discount_badge || ''} · Criativo #${idx + 1} (${current.catboxId})`;

    document.getElementById('adsKitBody').innerHTML = `
      <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="background:#000; border-radius:12px; overflow:hidden; aspect-ratio:9/15; border:1px solid rgba(255,255,255,0.12);">
          <video controls playsinline preload="metadata" poster="${esc(current.poster)}" src="${esc(current.url)}" style="width:100%; height:100%; object-fit:contain;"></video>
        </div>
        <button type="button" class="ads-btn ads-btn-download" style="width:100%; height:40px;" onclick="window.downloadAdsVideo(${prod.id})">⬇️ Baixar MP4 pro TikTok Ads</button>
        <a href="/produto-${prod.id}?owner=1" target="_blank" class="ads-btn" style="width:100%;">🛍️ Abrir Página do Produto ↗</a>
      </div>

      <div style="display:flex; flex-direction:column; gap:12px;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <label style="font-size:11.5px; font-weight:700; color:#94a3b8; text-transform:uppercase;">1. Link de Destino (URL com UTM TikTok)</label>
            <button type="button" class="ads-vid-pill active" onclick="window.copyAdsText(document.getElementById('kitUtmInput').value, 'Link UTM copiado!')">Copiar URL</button>
          </div>
          <input type="text" id="kitUtmInput" readonly class="form-control" style="height:38px; font-family:'JetBrains Mono',monospace; font-size:11.5px;" value="${esc(copy.utm)}" onclick="this.select()">
        </div>

        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <label style="font-size:11.5px; font-weight:700; color:#94a3b8; text-transform:uppercase;">2. Headline / Chamada Curta</label>
            <button type="button" class="ads-vid-pill active" onclick="window.copyAdsText(document.getElementById('kitHeadlineInput').value, 'Headline copiada!')">Copiar</button>
          </div>
          <input type="text" id="kitHeadlineInput" class="form-control" style="height:38px; font-size:13px;" value="${esc(copy.headline)}">
        </div>

        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
            <label style="font-size:11.5px; font-weight:700; color:#94a3b8; text-transform:uppercase;">3. Texto Principal do Anúncio (TikTok Ads)</label>
            <button type="button" class="ads-vid-pill active" onclick="window.copyAdsText(document.getElementById('kitCopyArea').value, 'Copy copiada!')">Copiar Texto</button>
          </div>
          <textarea id="kitCopyArea" class="ads-kit-textarea">${esc(copy.primaryText)}</textarea>
        </div>

        <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.28); border-radius:10px; padding:10px 12px; font-size:12px; color:#cbd5e1; line-height:1.5;">
          <strong style="color:#34d399;">✅ Checklist TikTok Ads Manager:</strong><br>
          • Objetivo: <strong>Conversões no Site</strong> · Evento: <strong>CompletePayment (Pix)</strong><br>
          • CTA sugerido: <strong>Comprar Agora</strong> · Pixel: <code>DBD7ASBC77UF91061F1G</code> (CAPI ativo)<br>
          • Vídeo MP4 limpo: <code style="color:#38bdf8;">${esc(current.url)}</code>
        </div>

        <button type="button" class="ads-btn ads-btn-green" style="height:42px; font-size:13px;" onclick="window.copyFullAdsKit(${prod.id})">
          📋 Copiar Kit Completo (Nome + Copy + Link UTM + Vídeo MP4)
        </button>
      </div>
    `;
    document.getElementById('adsKitModal').classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  window.copyFullAdsKit = function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    const { idx } = getSelectedVideo(prod);
    const copy = buildAdCopy(prod, idx);
    window.copyAdsText(copy.fullText, `🚀 Kit completo do Produto #${pid} copiado!`);
  };

  window.closeAdsKitModal = function () {
    const m = document.getElementById('adsKitModal');
    if (m) m.classList.remove('open');
    const b = document.getElementById('adsKitBody');
    if (b) b.innerHTML = '';
    document.body.style.overflow = '';
  };

  window.setAdsFilterChip = function (chip, btn) {
    adsFilterChip = chip;
    document.querySelectorAll('#adsFilterChips .ads-chip').forEach((c) => {
      c.classList.toggle('active', c.dataset.chip === chip);
    });
    if (btn) btn.classList.add('active');
    renderAdsGrid();
  };

  window.setAdsCategory = function (cat) {
    adsCategoryFilter = cat;
    renderAdsGrid();
  };

  window.setAdsSort = function (sort) {
    adsSortBy = sort;
    renderAdsGrid();
  };

  window.filtrarAdsVideos = function () {
    renderAdsGrid();
  };

  window.exportarPacoteAds = function () {
    const list = getFilteredAdsProducts();
    if (!list.length) {
      window.showToast && window.showToast('Nenhum produto filtrado para exportar.', 'info');
      return;
    }
    const lines = [
      `🚀 STONE SHOP — PACOTE DE CRIATIVOS TIKTOK ADS (${list.length} produtos)`,
      `Gerado em: ${new Date().toLocaleString('pt-BR')}`,
      `============================================================`,
      '',
    ];
    list.forEach((p) => {
      const { idx, current } = getSelectedVideo(p);
      const price = formatBRL(getEffectivePrice(p));
      const st = getStatusMeta(adsStatusMap[String(p.id)] || 'idle').label;
      lines.push(`#${p.id} | ${p.title}`);
      lines.push(`💰 PIX: ${price} ${p.discount_badge || ''} | Status: ${st}`);
      lines.push(`🔗 Página Ads (UTM): ${buildUtmUrl(p, idx)}`);
      lines.push(`🎬 Vídeo Ads (MP4): ${current ? current.url : 'N/A'}`);
      lines.push('');
    });
    const out = lines.join('\n');
    navigator.clipboard.writeText(out).then(() => {
      window.showToast && window.showToast(`📤 Pacote com ${list.length} produtos + vídeos copiado!`, 'success');
    }).catch(() => {
      const blob = new Blob([out], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `stoneshop_tiktok_ads_${Date.now()}.txt`;
      a.click();
    });
  };

  async function initAdsStudio() {
    loadLocalState();
    injectAdsStyles();
    createKitModal();

    const mountTarget = document.getElementById('adsStudioRoot');
    if (!mountTarget) return;

    try {
      const [mRes, cfgRes] = await Promise.all([
        fetch('data/admin-catalogo-360.json?v=' + Date.now()),
        fetch('/api/admin-config').catch(() => null),
      ]);
      if (mRes.ok) adsManifest = await mRes.json();
      if (cfgRes && cfgRes.ok) {
        const cfg = await cfgRes.json();
        const ovs = cfg.overrides || {};
        window.__STONE_SERVER_OVERRIDES__ = ovs;
        Object.entries(ovs).forEach(([pid, ov]) => {
          if (ov && ov.ads_status && !adsStatusMap[pid]) adsStatusMap[pid] = ov.ads_status;
          if (ov && ov.ads_fav_video && !adsFavMap[pid]) adsFavMap[pid] = ov.ads_fav_video;
        });
      }
    } catch (e) {
      console.warn('[AdsStudio] Erro ao carregar manifesto:', e);
    }

    if (!adsManifest || !Array.isArray(adsManifest.products)) {
      mountTarget.innerHTML = `<div style="padding:30px; text-align:center; color:#f87171;">Erro ao carregar data/admin-catalogo-360.json</div>`;
      return;
    }

    const categories = Array.from(new Set(adsManifest.products.map((p) => p.category))).sort();
    const newBfCount = adsManifest.products.filter((p) => p.is_new_bf).length;
    const totalWithVids = adsManifest.products.filter((p) => buildVideoList(p).length > 0).length;

    mountTarget.innerHTML = `
      <div class="ads-hero">
        <div>
          <h2 class="ads-hero-title">
            <span>🎬 Central de Vídeos TikTok Ads</span>
            <span class="ads-live-pill">Pronto pra Subir</span>
          </h2>
          <p class="ads-hero-sub">
            Nome do produto, preço PIX, preview do vídeo MP4 sem marca d'água, download renomeado, link UTM limpo e copy pronta — tudo em 1 tela pra subir campanha no TikTok Ads Manager em segundos.
          </p>
        </div>
        <div class="ads-hero-actions">
          <button type="button" class="ads-btn ads-btn-download" onclick="window.exportarPacoteAds()">📤 Copiar Pacote Ads (TXT)</button>
          <button type="button" class="ads-btn" onclick="window.copyAdsText('https://stoneshopclone.vercel.app/videos-ads', 'Link direto /videos-ads copiado!')">🔗 Link Direto /videos-ads</button>
          <a href="/catalogo-ads" target="_blank" class="ads-btn">📊 Lab de Testes ↗</a>
        </div>
      </div>

      <div class="ads-mini-kpis">
        <div class="ads-kpi">
          <div class="ads-kpi-num" id="adsKpiProds">0</div>
          <div class="ads-kpi-lbl">📦 Produtos c/ Vídeo Ads</div>
        </div>
        <div class="ads-kpi">
          <div class="ads-kpi-num" style="color:#fe2c55;" id="adsKpiVids">0</div>
          <div class="ads-kpi-lbl">🎬 Criativos MP4 Limpos</div>
        </div>
        <div class="ads-kpi">
          <div class="ads-kpi-num" style="color:#34d399;" id="adsKpiRunning">0</div>
          <div class="ads-kpi-lbl">🟢 Rodando no TikTok Ads</div>
        </div>
        <div class="ads-kpi">
          <div class="ads-kpi-num" style="color:#fbbf24;" id="adsKpiTesting">0</div>
          <div class="ads-kpi-lbl">🟡 Em Teste de Criativo</div>
        </div>
      </div>

      <div class="ads-toolbar">
        <div class="ads-toolbar-top">
          <div class="search-input-wrap">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" id="adsSearchInput" class="search-input" placeholder="Buscar produto, ID (ex: 146, 151, 136), @criador ou código Catbox..." oninput="window.filtrarAdsVideos()">
          </div>

          <select class="form-control" style="height:44px;" onchange="window.setAdsCategory(this.value)">
            <option value="todas">Todas as Categorias</option>
            ${categories.map((c) => `<option value="${esc(c)}">${esc(c)}</option>`).join('')}
          </select>

          <select class="form-control" style="height:44px;" onchange="window.setAdsSort(this.value)">
            <option value="newest">Ordenar: Mais Recentes</option>
            <option value="most_videos">Mais Vídeos Ads</option>
            <option value="biggest_disc">Maior Desconto %</option>
            <option value="price_asc">Menor Preço PIX</option>
            <option value="price_desc">Maior Preço PIX</option>
          </select>
        </div>

        <div class="ads-chips" id="adsFilterChips">
          <button type="button" class="ads-chip active" data-chip="new_bf" onclick="window.setAdsFilterChip('new_bf', this)">🔥 Lançamentos Black Friday (${newBfCount})</button>
          <button type="button" class="ads-chip" data-chip="all" onclick="window.setAdsFilterChip('all', this)">🎬 Todos os Produtos (${totalWithVids})</button>
          <button type="button" class="ads-chip" data-chip="running" onclick="window.setAdsFilterChip('running', this)">🟢 Rodando Ads</button>
          <button type="button" class="ads-chip" data-chip="testing" onclick="window.setAdsFilterChip('testing', this)">🟡 Em Teste</button>
          <button type="button" class="ads-chip" data-chip="high_anchor" onclick="window.setAdsFilterChip('high_anchor', this)">💎 Susto no Preço (R$ 50+)</button>
          <button type="button" class="ads-chip" data-chip="impulse" onclick="window.setAdsFilterChip('impulse', this)">⚡ Impulso Barato (≤ R$ 50)</button>
        </div>

        <div style="font-size:12px; color:#94a3b8; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <span id="adsShowingCount">Carregando...</span>
          <span style="color:#64748b;">💡 Dica: clique em <strong>⚪ Na Fila</strong> no card para marcar como <strong>🟡 Em Teste</strong> ou <strong>🟢 Rodando</strong>.</span>
        </div>
      </div>

      <div class="ads-grid" id="adsVideosGrid"></div>
    `;

    updateAdsKpis();
    renderAdsGrid();
  }

  window.__refreshAdsStudio = function () {
    updateAdsKpis();
    renderAdsGrid();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdsStudio);
  } else {
    initAdsStudio();
  }
})();
