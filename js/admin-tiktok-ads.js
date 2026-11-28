/**
 * STONE SHOP CORE — CENTRAL DE VÍDEOS TIKTOK ADS (DESIGN BENTO OBSIDIAN PRO)
 * Fiel à tela "Order list" da referência:
 *  - 4 Pastel-Cap Bento Cards no topo (Azul Periwinkle / Pêssego / Amarelo / Menta)
 *  - Busca pill + Exportar + Ordenar + Botão Branco Puro "+ Copiar Pacote Ads"
 *  - Modo Visual Bento Cards (c/ player sob demanda + troca de criativos) E Modo Tabela Limpa ("Order list")
 *  - Download MP4 renomeado, Link UTM limpo, Copy + Kit Ads em 1 clique
 */
(function () {
  const STORAGE_STATUS_KEY = 'STONE_ADS_CAMPAIGN_STATUS_V1';
  const STORAGE_FAV_KEY = 'STONE_ADS_FAV_VIDEO_V1';

  let adsManifest = null;
  let adsEditedMap = {};
  let adsStatusMap = {};
  let adsFavMap = {};
  let adsActiveVideoIdx = {};
  let adsFilterChip = 'all';
  let adsSortBy = 'newest';
  let adsCategoryFilter = 'todas';
  let adsViewMode = 'cards'; // 'cards' | 'table'

  function esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function normAsset(u) {
    const s = String(u || '').trim();
    if (!s) return '/logo.png';
    if (/^https?:\/\//i.test(s) || s.startsWith('data:')) return s;
    return '/' + s.replace(/^\.\.\//, '').replace(/^\/+/, '');
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

    // 0. Vídeos EDITADOS exclusivos para TikTok Ads (NÃO mexem nos vídeos limpos do site!)
    const editedItems = adsEditedMap[String(prod.id)] || [];
    editedItems.forEach((ed, eIdx) => {
      const url = cleanUrl(ed && ed.url);
      if (!url || seen.has(url)) return;
      seen.add(url);
      list.push({
        slot: `edited_${eIdx + 1}`,
        isEdited: true,
        label: eIdx === 0 ? '🔥 Editado Ads' : `🔥 Editado #${eIdx + 1}`,
        badge: '🔥 PRONTO P/ ADS (PREÇO + SETAS)',
        url,
        poster: normAsset(ed.poster || (prod.video && prod.video.poster) || prod.img || '/logo.png'),
        duration: ed.duration || '',
        catboxId: ed.catbox_id || url.split('/').pop(),
        author: 'Criativo Editado TikTok Ads',
        desc: ed.headline || prod.title,
        posNote: ed.pos_note || '',
      });
    });

    if (prod.video && prod.video.src) {
      const url = cleanUrl(prod.video.src);
      if (url && !seen.has(url)) {
        seen.add(url);
        list.push({
          slot: 'principal',
          isEdited: false,
          label: 'Limpo #1',
          badge: 'Principal Limpo',
          url,
          poster: normAsset(prod.video.poster || prod.img || '/logo.png'),
          duration: prod.video.duration || '',
          catboxId: prod.video.catbox_id || url.split('/').pop(),
          author: 'Stone Shop Oficial (Sem Texto)',
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
        isEdited: false,
        label: `UGC #${idx + 1}`,
        badge: `UGC Limpo #${idx + 1}`,
        url,
        poster: normAsset(c.poster || c.avatar || prod.img || '/logo.png'),
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
    if (st === 'running') return { key: 'running', label: 'Rodando', cls: 'st-running', pillBg: 'rgba(110,231,168,0.16)', pillCol: '#6ee7a8' };
    if (st === 'testing') return { key: 'testing', label: 'Em teste', cls: 'st-testing', pillBg: 'rgba(246,157,114,0.18)', pillCol: '#f69d72' };
    return { key: 'idle', label: 'Na fila', cls: 'st-idle', pillBg: 'rgba(255,255,255,0.08)', pillCol: '#a1a1aa' };
  }

  function injectAdsStyles() {
    if (document.getElementById('ads-studio-styles')) return;
    const st = document.createElement('style');
    st.id = 'ads-studio-styles';
    st.textContent = `
      .ads-bento-head {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        justify-content: space-between;
        gap: 14px;
        margin-bottom: 18px;
      }
      .ads-bento-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.6px;
        color: #ffffff;
        line-height: 1.15;
      }
      .ads-bento-sub {
        font-size: 13px;
        color: #8a8f98;
        margin-top: 4px;
      }

      /* Barra de controle idêntica à tela "Order list" */
      .ads-bar-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 12px;
      }
      .ads-bar-left {
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1;
        min-width: 240px;
      }
      .ads-search-pill {
        position: relative;
        flex: 1;
        max-width: 360px;
      }
      .ads-search-pill svg {
        position: absolute;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        color: #6b7280;
        pointer-events: none;
      }
      .ads-search-pill input {
        width: 100%;
        height: 40px;
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        padding: 0 16px 0 40px;
        color: #ffffff;
        font-size: 13px;
        font-family: inherit;
        outline: none;
      }
      .ads-search-pill input:focus { border-color: #638cff; }

      .ads-bar-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .ads-select-pill {
        height: 38px;
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        padding: 0 14px;
        color: #e5e7eb;
        font-size: 12px;
        font-weight: 700;
        font-family: inherit;
        outline: none;
        cursor: pointer;
      }

      /* Chips de filtro minimalistas Obsidian */
      .ads-chips-bar {
        display: flex;
        align-items: center;
        gap: 8px;
        overflow-x: auto;
        padding-bottom: 4px;
        margin-bottom: 16px;
        scrollbar-width: none;
      }
      .ads-chips-bar::-webkit-scrollbar { display: none; }
      .ads-chip {
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #9ca3af;
        font-size: 12px;
        font-weight: 700;
        padding: 7px 14px;
        border-radius: 999px;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.15s ease;
      }
      .ads-chip:hover { color: #ffffff; border-color: rgba(255, 255, 255, 0.2); }
      .ads-chip.active {
        background: #ffffff;
        border-color: #ffffff;
        color: #09090b;
      }

      /* Grid Bento de Cards de Vídeo Ads */
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
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.065);
        border-radius: 22px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        padding: 15px;
        gap: 12px;
        transition: transform 0.16s ease, border-color 0.16s ease;
      }
      .ads-card:hover {
        border-color: rgba(255, 255, 255, 0.16);
        transform: translateY(-2px);
      }
      .ads-card.st-running {
        border-color: rgba(110, 231, 168, 0.45);
      }
      .ads-card.st-testing {
        border-color: rgba(246, 157, 114, 0.45);
      }

      .ads-card-head {
        display: flex;
        gap: 11px;
        align-items: flex-start;
      }
      .ads-prod-thumb {
        width: 52px;
        height: 52px;
        border-radius: 14px;
        object-fit: cover;
        background: #1f1f26;
        border: 1px solid rgba(255, 255, 255, 0.08);
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
      }
      .ads-id-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 800;
        color: #d4d4d8;
        background: #222229;
        padding: 2px 8px;
        border-radius: 999px;
      }
      .ads-status-btn {
        font-size: 11px;
        font-weight: 800;
        padding: 3px 10px;
        border-radius: 999px;
        border: none;
        cursor: pointer;
        transition: opacity 0.15s ease;
      }
      .ads-status-btn:hover { opacity: 0.85; }
      .ads-prod-name {
        font-size: 13.5px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.32;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      .ads-price-strip {
        display: flex;
        align-items: center;
        gap: 7px;
        flex-wrap: wrap;
        margin-top: 2px;
      }
      .ads-price-now {
        font-family: 'JetBrains Mono', monospace;
        font-size: 16px;
        font-weight: 800;
        color: #ffffff;
      }
      .ads-price-old {
        font-size: 11px;
        color: #6b7280;
        text-decoration: line-through;
      }

      /* Palco de Vídeo Bento Arredondado */
      .ads-video-stage {
        position: relative;
        width: 100%;
        aspect-ratio: 16 / 10;
        border-radius: 16px;
        background: #09090b;
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
        background: linear-gradient(180deg, rgba(0,0,0,0.22) 0%, rgba(0,0,0,0.08) 45%, rgba(0,0,0,0.72) 100%);
      }
      .ads-play-circle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #ffffff;
        color: #09090b;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
        transition: transform 0.16s ease;
      }
      .ads-video-stage:hover .ads-play-circle { transform: scale(1.08); }
      .ads-stage-top {
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
      .ads-stage-pill {
        font-size: 10.5px;
        font-weight: 800;
        padding: 3px 9px;
        border-radius: 999px;
        background: rgba(9, 9, 11, 0.8);
        backdrop-filter: blur(8px);
        color: #ffffff;
      }
      .ads-stage-pill.blue {
        background: #638cff;
        color: #09090b;
      }

      /* Seletor horizontal de criativos */
      .ads-variants-bar {
        display: flex;
        gap: 6px;
        overflow-x: auto;
        scrollbar-width: none;
      }
      .ads-variants-bar::-webkit-scrollbar { display: none; }
      .ads-vid-pill {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 4px 10px;
        border-radius: 999px;
        background: #111114;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #9ca3af;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
        flex-shrink: 0;
        transition: all 0.14s ease;
      }
      .ads-vid-pill:hover { color: #ffffff; }
      .ads-vid-pill.active {
        background: #638cff;
        border-color: #638cff;
        color: #09090b;
      }
      .ads-vid-pill img {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        object-fit: cover;
      }

      .ads-url-box {
        display: flex;
        align-items: center;
        gap: 6px;
        background: #111114;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 999px;
        padding: 5px 11px;
      }
      .ads-url-input {
        flex: 1;
        background: transparent;
        border: none;
        color: #9ca3af;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        outline: none;
        min-width: 0;
      }

      .ads-actions-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
      }
      .ads-btn {
        height: 38px;
        border-radius: 999px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        background: #1f1f26;
        color: #ffffff;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        text-decoration: none;
        transition: all 0.15s ease;
        padding: 0 12px;
      }
      .ads-btn:hover { background: #2a2a33; }
      .ads-btn-white {
        background: #ffffff;
        border-color: #ffffff;
        color: #09090b;
        font-weight: 800;
      }
      .ads-btn-white:hover { background: #e5e7eb; }
      .ads-btn-blue {
        background: rgba(99, 140, 255, 0.16);
        border-color: rgba(99, 140, 255, 0.35);
        color: #93c5fd;
      }
      .ads-btn-blue:hover { background: rgba(99, 140, 255, 0.26); color: #ffffff; }

      /* Modal Kit Subida TikTok Ads — Bento Obsidian */
      .ads-kit-modal {
        position: fixed;
        inset: 0;
        z-index: 100000;
        background: rgba(0, 0, 0, 0.82);
        backdrop-filter: blur(12px);
        display: none;
        align-items: center;
        justify-content: center;
        padding: 14px;
      }
      .ads-kit-modal.open { display: flex; }
      .ads-kit-box {
        width: 100%;
        max-width: 800px;
        max-height: 92dvh;
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        box-shadow: 0 28px 70px rgba(0, 0, 0, 0.78);
      }
      .ads-kit-head {
        padding: 18px 22px;
        background: #111114;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
      }
      .ads-kit-body {
        padding: 20px 22px;
        overflow-y: auto;
        display: grid;
        grid-template-columns: 1fr;
        gap: 18px;
      }
      @media (min-width: 700px) {
        .ads-kit-body { grid-template-columns: 240px 1fr; }
      }
      .ads-kit-textarea {
        width: 100%;
        min-height: 112px;
        background: #09090b;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        color: #f8fafc;
        padding: 12px 14px;
        font-family: inherit;
        font-size: 12.5px;
        line-height: 1.5;
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
            <div style="font-size:16px; font-weight:800; color:#fff;" id="adsKitTitle">Kit Subida TikTok Ads</div>
            <div style="font-size:12px; color:#8a8f98; margin-top:2px;" id="adsKitSub">Pronto para colar no TikTok Ads Manager</div>
          </div>
          <button type="button" onclick="window.closeAdsKitModal()" class="arrow-circle dark" style="width:34px; height:34px; font-size:14px;">✕</button>
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

      if (adsFilterChip === 'edited' && !(adsEditedMap[String(p.id)] && adsEditedMap[String(p.id)].length)) return false;
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
    const newBf = prods.filter((p) => p.is_new_bf).length;
    const runningCount = Object.values(adsStatusMap).filter((s) => s === 'running').length;
    const testingCount = Object.values(adsStatusMap).filter((s) => s === 'testing').length;

    const setTxt = (id, val) => { const el = document.getElementById(id); if (el) el.textContent = val; };
    setTxt('adsKpiProds', totalProds);
    setTxt('adsKpiVidsSub', `${totalVids} MP4s sem marca`);
    setTxt('adsKpiTesting', testingCount);
    setTxt('adsKpiNewBf', newBf);
    setTxt('adsKpiRunning', runningCount);
    setTxt('badgeAdsTop', totalVids);
    setTxt('bNavAdsBadge', totalProds);
    setTxt('kpiAdsTotal', `${totalVids} vídeos`);
  }

  function renderAdsListOrGrid() {
    const host = document.getElementById('adsVideosGridHost');
    if (!host) return;

    const list = getFilteredAdsProducts();
    const countLbl = document.getElementById('adsShowingCount');
    if (countLbl) countLbl.textContent = `${list.length} produto(s)`;

    if (!list.length) {
      host.innerHTML = `
        <div style="text-align:center; padding:48px 16px; background:#16161a; border:1px solid rgba(255,255,255,0.06); border-radius:22px; color:#9ca3af;">
          <div style="font-size:32px; margin-bottom:8px;">🎬</div>
          <div style="font-size:15px; font-weight:800; color:#ffffff;">Nenhum produto encontrado neste filtro</div>
          <div style="font-size:12.5px; margin-top:4px;">Clique abaixo para ver todos os produtos com vídeo pronto pro TikTok Ads.</div>
          <button type="button" class="bento-white-pill-btn" style="margin-top:14px;" onclick="window.setAdsFilterChip('all')">Mostrar Todos os Produtos</button>
        </div>
      `;
      return;
    }

    // MODO TABELA LIMPA ("ORDER LIST" DA REFERÊNCIA)
    if (adsViewMode === 'table') {
      host.innerHTML = `
        <div class="bento-table-wrap">
          <table class="bento-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Produto</th>
                <th>Categoria</th>
                <th>Preço PIX</th>
                <th>Vídeo Ads</th>
                <th>Status</th>
                <th style="text-align:right;">Subir no TikTok Ads</th>
              </tr>
            </thead>
            <tbody>
              ${list.map((p) => {
                const { vids, current } = getSelectedVideo(p);
                const price = getEffectivePrice(p);
                const stMeta = getStatusMeta(adsStatusMap[String(p.id)] || 'idle');
                return `
                  <tr>
                    <td><span class="ads-id-tag">#${p.id}</span></td>
                    <td>
                      <div style="display:flex; align-items:center; gap:10px; max-width:310px;">
                        <img src="${esc(normAsset(p.img))}" style="width:38px; height:38px; border-radius:10px; object-fit:cover; background:#1f1f26; flex-shrink:0;" decoding="async" onerror="this.src='/logo.png'">
                        <div style="min-width:0;">
                          <div style="font-weight:700; color:#fff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${esc(p.title)}">${esc(p.title)}</div>
                          <div style="font-size:11px; color:${current.isEdited ? '#6ee7a8' : '#6b7280'};">${current.isEdited ? '🔥 Editado pronto · ' : ''}${vids.length} vídeos · ${esc(current.catboxId)}</div>
                        </div>
                      </div>
                    </td>
                    <td style="color:#9ca3af; font-size:12px;">${esc(p.category)}</td>
                    <td style="font-family:'JetBrains Mono',monospace; font-weight:800; color:#fff; white-space:nowrap;">${formatBRL(price)}</td>
                    <td>
                      <button type="button" class="ads-vid-pill active" onclick="window.openAdsKitModal(${p.id})">▶ Assistir (${vids.length})</button>
                    </td>
                    <td>
                      <button type="button" class="ads-status-btn" style="background:${stMeta.pillBg}; color:${stMeta.pillCol};" onclick="window.cycleAdsStatus(${p.id})">${stMeta.label} ▾</button>
                    </td>
                    <td style="text-align:right; white-space:nowrap;">
                      <div style="display:inline-flex; gap:6px;">
                        <button type="button" class="bento-white-pill-btn" style="height:32px; padding:0 12px; font-size:11.5px;" id="adsDlBtn-${p.id}" onclick="window.downloadAdsVideo(${p.id})">⬇️ MP4</button>
                        <button type="button" class="bento-dark-pill-btn" style="height:32px; padding:0 11px; font-size:11.5px;" onclick="window.copyAdsUtm(${p.id})">🔗 UTM</button>
                        <button type="button" class="bento-dark-pill-btn" style="height:32px; padding:0 11px; font-size:11.5px;" onclick="window.openAdsKitModal(${p.id})">✍️ Kit</button>
                      </div>
                    </td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      `;
      return;
    }

    // MODO CARDS BENTO OBSIDIAN
    host.innerHTML = `<div class="ads-grid" id="adsVideosGrid">${list.map((p) => {
      const { vids, idx, current } = getSelectedVideo(p);
      const price = getEffectivePrice(p);
      const origStr = p.price_original_str || (p.preco_antigo ? formatBRL(p.preco_antigo) : '');
      const stMeta = getStatusMeta(adsStatusMap[String(p.id)] || 'idle');
      const isFav = adsFavMap[String(p.id)] === (current && current.url);

      return `
        <article class="ads-card ${stMeta.cls}" id="adsCard-${p.id}">
          <div class="ads-card-head">
            <img src="${esc(normAsset(p.img))}" alt="${esc(p.title)}" class="ads-prod-thumb" decoding="async" onerror="this.src='/logo.png'">
            <div class="ads-prod-meta">
              <div class="ads-prod-top-row">
                <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                  <span class="ads-id-tag">#${p.id}</span>
                  ${current.isEdited ? `<span class="delta-pill up" style="font-size:10px; padding:2px 7px;">🔥 Editado</span>` : ''}
                  <button type="button" class="ads-status-btn" style="background:${stMeta.pillBg}; color:${stMeta.pillCol};" onclick="window.cycleAdsStatus(${p.id})" title="Alternar status: Fila → Em teste → Rodando">${stMeta.label}</button>
                </div>
                <a href="/produto-${p.id}?owner=1" target="_blank" class="arrow-circle dark" style="width:30px; height:30px; font-size:13px;" title="Abrir página limpa do produto na loja">↗</a>
              </div>
              <div class="ads-prod-name" title="${esc(p.title)}">${esc(p.title)}</div>
              <div class="ads-price-strip">
                <span class="ads-price-now">${formatBRL(price)}</span>
                ${origStr ? `<span class="ads-price-old">${esc(origStr)}</span>` : ''}
                ${p.discount_badge ? `<span class="delta-pill up">${esc(p.discount_badge)}</span>` : ''}
              </div>
            </div>
          </div>

          <div class="ads-video-stage" id="adsStage-${p.id}" style="${current.isEdited ? 'aspect-ratio: 9 / 14; max-height: 360px;' : ''}" onclick="window.playInlineAdsVideo(${p.id})">
            <div class="ads-stage-top">
              <span class="ads-stage-pill" style="${current.isEdited ? 'background:#6ee7a8; color:#052e16;' : ''}">${esc(current.badge)}${isFav ? ' ★' : ''}</span>
              <span class="ads-stage-pill blue">${vids.length} ${vids.length === 1 ? 'vídeo' : 'vídeos'}</span>
            </div>
            <img src="${esc(current.poster)}" alt="Vídeo Ads ${esc(p.title)}" class="ads-poster" style="${current.isEdited ? 'object-fit:contain; background:#050507; filter:brightness(0.96);' : ''}" decoding="async" onerror="this.src='${esc(normAsset(p.img))}'">
            <div class="ads-play-overlay">
              <div class="ads-play-circle">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><polygon points="6 4 20 12 6 20 6 4"></polygon></svg>
              </div>
              <span class="ads-stage-pill" style="font-size:10.5px;">Assistir · ${esc(current.catboxId)}</span>
            </div>
          </div>

          <div class="ads-variants-bar">
            ${vids.map((v, vIdx) => `
              <button type="button" class="ads-vid-pill ${vIdx === idx ? 'active' : ''}" style="${v.isEdited && vIdx !== idx ? 'border-color:rgba(110,231,168,0.45); color:#6ee7a8;' : ''}" onclick="window.selectAdsVideo(${p.id}, ${vIdx})" title="${esc(v.author)}">
                <img src="${esc(v.poster)}" alt="" decoding="async" onerror="this.src='/logo.png'">
                <span>${esc(v.label)}</span>
              </button>
            `).join('')}
          </div>

          <div class="ads-url-box">
            <span style="font-size:10px; font-weight:800; color:${current.isEdited ? '#6ee7a8' : '#638cff'}; flex-shrink:0;">${current.isEdited ? 'ADS' : 'MP4'}</span>
            <input type="text" readonly class="ads-url-input" value="${esc(current.url)}" onclick="this.select()">
            <button type="button" onclick="window.copyAdsText('${esc(current.url)}', 'Link MP4 copiado!')" title="Copiar link MP4" style="background:none; border:none; color:#cbd5e1; cursor:pointer; font-size:13px;">📋</button>
            <button type="button" onclick="window.toggleFavAdsVideo(${p.id})" title="Fixar criativo favorito" style="background:none; border:none; color:${isFav ? '#fde068' : '#6b7280'}; cursor:pointer; font-size:14px;">★</button>
          </div>

          <div class="ads-actions-row">
            <button type="button" class="ads-btn ads-btn-white" id="adsDlBtn-${p.id}" onclick="window.downloadAdsVideo(${p.id})">
              ⬇️ ${current.isEdited ? 'Baixar Editado' : 'Baixar MP4'}
            </button>
            <button type="button" class="ads-btn ads-btn-blue" onclick="window.copyAdsUtm(${p.id})">
              🔗 Copiar UTM
            </button>
            <button type="button" class="ads-btn" style="grid-column:1 / -1;" onclick="window.openAdsKitModal(${p.id})">
              ✍️ Abrir Copy + Kit TikTok Ads
            </button>
          </div>
        </article>
      `;
    }).join('')}</div>`;
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
    stage.innerHTML = `<video controls autoplay playsinline src="${esc(current.url)}" poster="${esc(current.poster)}" style="width:100%; height:100%; object-fit:contain; background:#000;"></video>`;
  };

  window.selectAdsVideo = function (pid, vIdx) {
    adsActiveVideoIdx[pid] = Number(vIdx);
    renderAdsListOrGrid();
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
      window.showToast && window.showToast(`★ Criativo fixado como favorito do #${pid}!`, 'success');
    }
    saveLocalState();
    syncProductAdsOverride(pid);
    renderAdsListOrGrid();
  };

  window.cycleAdsStatus = function (pid) {
    const cur = adsStatusMap[String(pid)] || 'idle';
    const next = cur === 'idle' ? 'testing' : (cur === 'testing' ? 'running' : 'idle');
    adsStatusMap[String(pid)] = next;
    saveLocalState();
    syncProductAdsOverride(pid);
    updateAdsKpis();
    renderAdsListOrGrid();
    window.showToast && window.showToast(`Produto #${pid}: ${getStatusMeta(next).label}`, 'success');
  };

  function syncProductAdsOverride(pid) {
    fetch('/api/admin-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'save_product_override',
        productId: pid,
        patch: { ads_status: adsStatusMap[String(pid)] || 'idle', ads_fav_video: adsFavMap[String(pid)] || '' },
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
    window.copyAdsText(buildUtmUrl(prod, idx), `🔗 Link UTM do Produto #${pid} copiado!`);
  };

  window.downloadAdsVideo = async function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    const { idx, current } = getSelectedVideo(prod);
    if (!current || !current.url) return;

    const btn = document.getElementById(`adsDlBtn-${pid}`);
    const origLabel = btn ? btn.innerHTML : '';
    const tag = current.isEdited ? 'EDITADO_ADS' : `Ad${idx + 1}`;
    const fileName = `StoneShop_Prod${prod.id}_${(prod.slug || 'produto').slice(0, 20)}_${tag}.mp4`;

    if (btn) { btn.disabled = true; btn.innerHTML = '⏳ Baixando...'; }
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
      if (btn) { btn.disabled = false; btn.innerHTML = origLabel; }
    }
  };

  window.openAdsKitModal = function (pid) {
    if (!adsManifest) return;
    const prod = adsManifest.products.find((x) => x.id === Number(pid));
    if (!prod) return;
    const { idx, current } = getSelectedVideo(prod);
    const copy = buildAdCopy(prod, idx);
    const price = getEffectivePrice(prod);

    document.getElementById('adsKitTitle').textContent = `#${prod.id} — ${prod.title.slice(0, 52)}`;
    document.getElementById('adsKitSub').textContent = `PIX ${formatBRL(price)} · ${prod.discount_badge || ''} · Criativo #${idx + 1} (${current.catboxId})`;

    document.getElementById('adsKitBody').innerHTML = `
      <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="background:#000; border-radius:16px; overflow:hidden; aspect-ratio:9/15; border:1px solid rgba(255,255,255,0.08);">
          <video controls playsinline preload="metadata" poster="${esc(current.poster)}" src="${esc(current.url)}" style="width:100%; height:100%; object-fit:contain;"></video>
        </div>
        <button type="button" class="bento-white-pill-btn" style="width:100%; height:42px;" onclick="window.downloadAdsVideo(${prod.id})">⬇️ Baixar MP4 pro TikTok Ads</button>
        <a href="/produto-${prod.id}?owner=1" target="_blank" class="bento-dark-pill-btn" style="width:100%;">Abrir Página do Produto ↗</a>
      </div>

      <div style="display:flex; flex-direction:column; gap:13px;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <label style="font-size:11.5px; font-weight:700; color:#9ca3af; text-transform:uppercase;">1. Link de Destino (UTM TikTok)</label>
            <button type="button" class="ads-vid-pill active" onclick="window.copyAdsText(document.getElementById('kitUtmInput').value, 'Link UTM copiado!')">Copiar URL</button>
          </div>
          <input type="text" id="kitUtmInput" readonly class="form-control" style="height:40px; font-family:'JetBrains Mono',monospace; font-size:11.5px;" value="${esc(copy.utm)}" onclick="this.select()">
        </div>

        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <label style="font-size:11.5px; font-weight:700; color:#9ca3af; text-transform:uppercase;">2. Headline / Chamada Curta</label>
            <button type="button" class="ads-vid-pill active" onclick="window.copyAdsText(document.getElementById('kitHeadlineInput').value, 'Headline copiada!')">Copiar</button>
          </div>
          <input type="text" id="kitHeadlineInput" class="form-control" style="height:40px; font-size:13px;" value="${esc(copy.headline)}">
        </div>

        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <label style="font-size:11.5px; font-weight:700; color:#9ca3af; text-transform:uppercase;">3. Texto Principal do Anúncio</label>
            <button type="button" class="ads-vid-pill active" onclick="window.copyAdsText(document.getElementById('kitCopyArea').value, 'Copy copiada!')">Copiar Texto</button>
          </div>
          <textarea id="kitCopyArea" class="ads-kit-textarea">${esc(copy.primaryText)}</textarea>
        </div>

        <div style="background:#111114; border:1px solid rgba(110,231,168,0.22); border-radius:14px; padding:12px 14px; font-size:12px; color:#d4d4d8; line-height:1.55;">
          <strong style="color:#6ee7a8;">✓ Checklist TikTok Ads Manager:</strong><br>
          • Objetivo: <strong>Conversões no Site</strong> · Evento: <strong>CompletePayment (Pix)</strong><br>
          • Pixel: <code>DBD7ASBC77UF91061F1G</code> (CAPI ativo) · MP4: <code style="color:#93c5fd;">${esc(current.url)}</code>
        </div>

        <button type="button" class="bento-white-pill-btn" style="height:44px; font-size:13px;" onclick="window.copyFullAdsKit(${prod.id})">
          📋 Copiar Kit Completo (Nome + Copy + Link UTM + MP4)
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
    window.copyAdsText(buildAdCopy(prod, idx).fullText, `Kit completo do Produto #${pid} copiado!`);
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
    renderAdsListOrGrid();
  };

  window.setAdsCategory = function (cat) {
    adsCategoryFilter = cat;
    const sel = document.getElementById('adsCategorySelect');
    if (sel) sel.value = cat;
    renderAdsListOrGrid();
  };

  window.setAdsSort = function (sort) {
    adsSortBy = sort;
    renderAdsListOrGrid();
  };

  window.setAdsViewMode = function (mode) {
    adsViewMode = mode;
    document.querySelectorAll('.ads-view-toggle').forEach((b) => {
      b.classList.toggle('active', b.dataset.mode === mode);
    });
    renderAdsListOrGrid();
  };

  window.filtrarAdsVideos = function () {
    renderAdsListOrGrid();
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
      lines.push(`#${p.id} | ${p.title}`);
      lines.push(`💰 PIX: ${formatBRL(getEffectivePrice(p))} ${p.discount_badge || ''} | Status: ${getStatusMeta(adsStatusMap[String(p.id)] || 'idle').label}`);
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
      const [mRes, edRes, cfgRes] = await Promise.all([
        fetch('/data/admin-catalogo-360.json?v=' + Date.now()),
        fetch('/data/ads-editados.json?v=' + Date.now()).catch(() => null),
        fetch('/api/admin-config').catch(() => null),
      ]);
      if (mRes.ok) adsManifest = await mRes.json();
      if (edRes && edRes.ok) {
        const edJson = await edRes.json();
        adsEditedMap = (edJson && edJson.items) || {};
      }
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
    const editedCount = Object.keys(adsEditedMap).filter((k) => Array.isArray(adsEditedMap[k]) && adsEditedMap[k].length > 0).length;

    mountTarget.innerHTML = `
      <div class="ads-bento-head">
        <div>
          <h1 class="ads-bento-title">Vídeos TikTok Ads</h1>
          <p class="ads-bento-sub">Nome do produto, preço PIX, criativos MP4 sem marca d'água e links UTM prontos para subir.</p>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <button type="button" class="bento-dark-pill-btn" onclick="window.copyAdsText('https://stoneshopclone.vercel.app/videos-ads', 'Link direto /videos-ads copiado!')">🔗 /videos-ads</button>
          <a href="/catalogo-ads" target="_blank" class="bento-dark-pill-btn">Lab Ads ↗</a>
          <button type="button" class="bento-white-pill-btn" onclick="window.exportarPacoteAds()">+ Exportar Pacote Ads</button>
        </div>
      </div>

      <!-- 4 PASTEL-CAP BENTO CARDS (EXATAMENTE IGUAL À TELA "ORDER LIST" DA REFERÊNCIA) -->
      <div class="pastel-kpi-grid">
        <div class="pastel-card" onclick="window.setAdsFilterChip('all')">
          <div class="pastel-cap cap-blue"><span>Produtos c/ Vídeo</span><span>↗</span></div>
          <div class="pastel-body">
            <div class="pastel-num-row">
              <span class="pastel-num" id="adsKpiProds">0</span>
              <span class="delta-pill up">↑ 100%</span>
            </div>
            <div class="pastel-sub" id="adsKpiVidsSub">522 MP4s sem marca</div>
          </div>
        </div>

        <div class="pastel-card" onclick="window.setAdsFilterChip('testing')">
          <div class="pastel-cap cap-peach"><span>Em Teste Ads</span><span>↗</span></div>
          <div class="pastel-body">
            <div class="pastel-num-row">
              <span class="pastel-num" id="adsKpiTesting">0</span>
              <span class="delta-pill down">Testando</span>
            </div>
            <div class="pastel-sub">Criativos em validação</div>
          </div>
        </div>

        <div class="pastel-card" onclick="window.setAdsFilterChip('new_bf')">
          <div class="pastel-cap cap-yellow"><span>Lançamentos BF</span><span>↗</span></div>
          <div class="pastel-body">
            <div class="pastel-num-row">
              <span class="pastel-num" id="adsKpiNewBf">0</span>
              <span class="delta-pill up">↑ Novos</span>
            </div>
            <div class="pastel-sub">Mix Campeão #126–#154</div>
          </div>
        </div>

        <div class="pastel-card" onclick="window.setAdsFilterChip('running')">
          <div class="pastel-cap cap-mint"><span>Rodando no TikTok</span><span>↗</span></div>
          <div class="pastel-body">
            <div class="pastel-num-row">
              <span class="pastel-num" id="adsKpiRunning">0</span>
              <span class="delta-pill up">↑ Ativos</span>
            </div>
            <div class="pastel-sub">Campanhas em escala</div>
          </div>
        </div>
      </div>

      <!-- BARRA DE CONTROLE (SEARCH PILL + CONTADOR + SORT + VIEW MODE) -->
      <div class="ads-bar-row">
        <div class="ads-bar-left">
          <div class="ads-search-pill">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" id="adsSearchInput" placeholder="Buscar produto, ID (154, 146, 136), @criador..." oninput="window.filtrarAdsVideos()">
          </div>
          <span id="adsShowingCount" style="font-size:12.5px; color:#6b7280; font-weight:600; white-space:nowrap;">...</span>
        </div>

        <div class="ads-bar-right">
          <select id="adsCategorySelect" class="ads-select-pill" onchange="window.setAdsCategory(this.value)">
            <option value="todas">Todas Categorias</option>
            ${categories.map((c) => `<option value="${esc(c)}">${esc(c)}</option>`).join('')}
          </select>

          <select class="ads-select-pill" onchange="window.setAdsSort(this.value)">
            <option value="newest">Sort: Mais Recentes</option>
            <option value="most_videos">Mais Vídeos</option>
            <option value="biggest_disc">Maior Desconto</option>
            <option value="price_asc">Menor Preço</option>
            <option value="price_desc">Maior Preço</option>
          </select>

          <button type="button" class="ads-chip ads-view-toggle active" data-mode="cards" onclick="window.setAdsViewMode('cards')">⊞ Cards</button>
          <button type="button" class="ads-chip ads-view-toggle" data-mode="table" onclick="window.setAdsViewMode('table')">☰ Lista</button>
        </div>
      </div>

      <!-- CHIPS DE FILTRO -->
      <div class="ads-chips-bar" id="adsFilterChips">
        ${editedCount > 0 ? `<button type="button" class="ads-chip ${adsFilterChip === 'edited' ? 'active' : ''}" data-chip="edited" onclick="window.setAdsFilterChip('edited', this)">🔥 Prontos Editados c/ Preço (${editedCount})</button>` : ''}
        <button type="button" class="ads-chip ${adsFilterChip === 'new_bf' ? 'active' : ''}" data-chip="new_bf" onclick="window.setAdsFilterChip('new_bf', this)">Lançamentos Black Friday (${newBfCount})</button>
        <button type="button" class="ads-chip ${adsFilterChip === 'all' ? 'active' : ''}" data-chip="all" onclick="window.setAdsFilterChip('all', this)">Todos os Produtos (${totalWithVids})</button>
        <button type="button" class="ads-chip" data-chip="running" onclick="window.setAdsFilterChip('running', this)">Rodando Ads</button>
        <button type="button" class="ads-chip" data-chip="testing" onclick="window.setAdsFilterChip('testing', this)">Em Teste</button>
        <button type="button" class="ads-chip" data-chip="high_anchor" onclick="window.setAdsFilterChip('high_anchor', this)">Susto no Preço (R$ 50+)</button>
        <button type="button" class="ads-chip" data-chip="impulse" onclick="window.setAdsFilterChip('impulse', this)">Impulso Barato (≤ R$ 50)</button>
      </div>

      <!-- HOST GRID / TABELA -->
      <div id="adsVideosGridHost"></div>
    `;

    updateAdsKpis();
    renderAdsListOrGrid();
  }

  window.__refreshAdsStudio = function () {
    updateAdsKpis();
    renderAdsListOrGrid();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdsStudio);
  } else {
    initAdsStudio();
  }
})();
