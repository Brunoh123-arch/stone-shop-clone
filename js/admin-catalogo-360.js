/**
 * STONE SHOP CORE — MÓDULO EXECUTIVO RAIO-X 360° POR PRODUTO + CATBOX LOCK + PIX RECOVERY
 * Conecta o /admin à Fonte Única da Verdade (data/admin-catalogo-360.json + data/catbox-registry.json + /api/admin-config)
 */
(function () {
  let manifest360 = null;
  let catboxRegistry = null;
  let serverOverrides = {};
  let activeHealthFilter = 'all';
  let currentModalProd = null;
  let currentModalTab = 'slides';
  let reviewsOnlyPhotos = false;

  function esc(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function injectAdmin360Styles() {
    if (document.getElementById('admin-360-styles')) return;
    const st = document.createElement('style');
    st.id = 'admin-360-styles';
    st.textContent = `
      .rx-kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 10px;
        margin-bottom: 14px;
      }
      .rx-kpi-card {
        background: var(--bg-subtle, #192338);
        border: 1px solid var(--border, rgba(255,255,255,0.08));
        border-radius: 12px;
        padding: 12px 14px;
      }
      .rx-kpi-val { font-size: 20px; font-weight: 800; color: #f8fafc; line-height: 1.15; }
      .rx-kpi-lbl { font-size: 11.5px; color: #94a3b8; margin-top: 3px; font-weight: 600; }
      .rx-catbox-checker {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 12px 14px;
        margin-bottom: 14px;
      }
      .rx-checker-row {
        display: flex;
        gap: 8px;
        margin-top: 8px;
        flex-wrap: wrap;
      }
      .rx-checker-input {
        flex: 1;
        min-width: 200px;
        background: #07090e;
        border: 1px solid rgba(255,255,255,0.14);
        border-radius: 8px;
        padding: 8px 12px;
        color: #f8fafc;
        font-size: 13px;
        font-family: 'JetBrains Mono', monospace;
      }
      .rx-pill-row {
        display: flex;
        gap: 8px;
        overflow-x: auto;
        padding-bottom: 6px;
        margin-bottom: 12px;
      }
      .rx-filter-btn {
        background: #141c2e;
        border: 1px solid rgba(255,255,255,0.1);
        color: #cbd5e1;
        border-radius: 999px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
      }
      .rx-filter-btn.active {
        background: #10b981;
        border-color: #10b981;
        color: #04130d;
      }
      .rx-badges-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin: 8px 0 10px;
      }
      .rx-mini-badge {
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(255,255,255,0.06);
        color: #cbd5e1;
        border: 1px solid rgba(255,255,255,0.08);
      }
      .rx-mini-badge.ok { background: rgba(16,185,129,0.14); color: #34d399; border-color: rgba(16,185,129,0.3); }
      .rx-mini-badge.warn { background: rgba(245,158,11,0.14); color: #fbbf24; border-color: rgba(245,158,11,0.3); }
      .rx-btn-360 {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 7px 12px;
        font-size: 12px;
        font-weight: 800;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 5px;
      }
      /* Modal 360 */
      .rx-modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(3, 6, 12, 0.86);
        backdrop-filter: blur(8px);
        z-index: 99999;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 12px;
      }
      .rx-modal-overlay.open { display: flex; }
      .rx-modal-box {
        width: 100%;
        max-width: 1080px;
        height: min(92dvh, 860px);
        background: #0b101b;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 16px;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        box-shadow: 0 24px 64px rgba(0,0,0,0.65);
      }
      .rx-modal-head {
        padding: 14px 18px;
        background: #0f172a;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }
      .rx-tabs-bar {
        display: flex;
        gap: 6px;
        padding: 10px 16px;
        background: #0d1322;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        overflow-x: auto;
        flex-shrink: 0;
      }
      .rx-tab {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: #94a3b8;
        padding: 7px 13px;
        border-radius: 8px;
        font-size: 12.5px;
        font-weight: 700;
        cursor: pointer;
        white-space: nowrap;
      }
      .rx-tab.active {
        background: #fe2c55;
        border-color: #fe2c55;
        color: #fff;
      }
      .rx-modal-body {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
      }
      .rx-slides-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(155px, 1fr));
        gap: 12px;
      }
      .rx-slide-card {
        background: #131b2e;
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 10px;
        overflow: hidden;
      }
      .rx-slide-card img {
        width: 100%;
        aspect-ratio: 1 / 1;
        object-fit: cover;
        display: block;
        background: #000;
        cursor: zoom-in;
      }
      .rx-creators-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
        gap: 12px;
      }
      .rx-creator-card {
        background: #131b2e;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
      }
      .rx-creator-media {
        position: relative;
        width: 100%;
        aspect-ratio: 9 / 14;
        background: #000;
      }
      .rx-creator-media video, .rx-creator-media img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
      }
      .rx-desc-preview {
        background: #ffffff;
        color: #161823;
        border-radius: 12px;
        padding: 16px;
        font-size: 14px;
        line-height: 1.55;
      }
      .rx-desc-preview img { max-width: 100%; height: auto; border-radius: 8px; }
    `;
    document.head.appendChild(st);
  }

  async function initAdmin360() {
    injectAdmin360Styles();
    createModalShell();

    try {
      const [mRes, cRes, cfgRes] = await Promise.all([
        fetch('data/admin-catalogo-360.json?v=' + Date.now()),
        fetch('data/catbox-registry.json?v=' + Date.now()),
        fetch('/api/admin-config').catch(() => null),
      ]);
      if (mRes.ok) manifest360 = await mRes.json();
      if (cRes && cRes.ok) catboxRegistry = await cRes.json();
      if (cfgRes && cfgRes.ok) {
        const cfgJson = await cfgRes.json();
        serverOverrides = cfgJson.overrides || {};
      }
    } catch (e) {
      console.warn('Erro ao carregar manifesto 360:', e);
    }

    if (manifest360 && Array.isArray(manifest360.products)) {
      mountTopDashboardInCatalogo();
      overrideCatalogFunctions();
      window.carregarCatalogo();
    }

    enhancePedidosWithRecovery();

    if (window.location.hash === '#catalogo' && typeof window.trocarAba === 'function') {
      window.trocarAba('catalogo');
    }
  }

  function mountTopDashboardInCatalogo() {
    const sec = document.getElementById('view-catalogo');
    const searchBox = sec && sec.querySelector('.search-filter-box');
    if (!sec || !searchBox || document.getElementById('rx-top-panel')) return;

    const totalEl = document.getElementById('totalProductsCount');
    const badgeTop = document.getElementById('badgeCatalogoTop');
    if (totalEl) totalEl.textContent = manifest360.total_products;
    if (badgeTop) badgeTop.textContent = manifest360.total_products;

    const wrap = document.createElement('div');
    wrap.id = 'rx-top-panel';
    wrap.innerHTML = `
      <div class="rx-kpi-grid">
        <div class="rx-kpi-card">
          <div class="rx-kpi-val">${manifest360.total_products}</div>
          <div class="rx-kpi-lbl">📦 Produtos Reais (JSON Único)</div>
        </div>
        <div class="rx-kpi-card">
          <div class="rx-kpi-val">${manifest360.total_slides}</div>
          <div class="rx-kpi-lbl">🖼️ Fotos de Slider</div>
        </div>
        <div class="rx-kpi-card">
          <div class="rx-kpi-val">${(catboxRegistry && catboxRegistry.stats && catboxRegistry.stats.total_unique_catbox_videos) || 478}</div>
          <div class="rx-kpi-lbl">🔒 Vídeos Catbox Travados</div>
        </div>
        <div class="rx-kpi-card">
          <div class="rx-kpi-val">${manifest360.total_reviews.toLocaleString('pt-BR')}</div>
          <div class="rx-kpi-lbl">⭐ Avaliações (${manifest360.total_unboxing_photos} fotos)</div>
        </div>
        <div class="rx-kpi-card">
          <div class="rx-kpi-val" style="color:#10b981;">${manifest360.avg_health_score}%</div>
          <div class="rx-kpi-lbl">🛡️ Saúde Média do Catálogo</div>
        </div>
      </div>

      <div class="rx-catbox-checker">
        <div style="font-size:13px; font-weight:800; color:#e2e8f0;">
          🔎 Rastreador Anti-Conflito Catbox — Descubra de qual produto é qualquer vídeo
        </div>
        <div style="font-size:12px; color:#94a3b8; margin-top:2px;">
          Cole o link <code style="color:#a5b4fc;">files.catbox.moe/xxxx.mp4</code> ou código (ex: <code style="color:#a5b4fc;">p85550</code>) para saber na hora o produto dono:
        </div>
        <div class="rx-checker-row">
          <input type="text" id="rx-catbox-lookup-input" class="rx-checker-input" placeholder="Ex: https://files.catbox.moe/p85550.mp4 ou p85550" oninput="window.lookupCatboxVideo(this.value)">
          <button type="button" class="rx-btn-360" onclick="window.lookupCatboxVideo(document.getElementById('rx-catbox-lookup-input').value)">Verificar Vínculo</button>
        </div>
        <div id="rx-catbox-lookup-result" style="margin-top:8px; font-size:12.5px;"></div>
      </div>

      <div class="rx-pill-row" id="rx-health-filters">
        <button type="button" class="rx-filter-btn active" onclick="window.setRxHealthFilter('all', this)">Todos (${manifest360.total_products})</button>
        <button type="button" class="rx-filter-btn" onclick="window.setRxHealthFilter('perfect', this)">🏆 Score 100% (${manifest360.products.filter(p => p.health_score === 100).length})</button>
        <button type="button" class="rx-filter-btn" onclick="window.setRxHealthFilter('30plus', this)">📱 30+ Criadores (${manifest360.products.filter(p => p.creators_count >= 30).length})</button>
        <button type="button" class="rx-filter-btn" onclick="window.setRxHealthFilter('low_creators', this)">⚡ &lt; 10 Criadores (${manifest360.products.filter(p => p.creators_count < 10).length})</button>
        <button type="button" class="rx-filter-btn" onclick="window.setRxHealthFilter('conflict', this)">⚠️ Vídeos Compartilhados (${manifest360.products.filter(p => p.has_catbox_conflict).length})</button>
      </div>
    `;
    searchBox.parentNode.insertBefore(wrap, searchBox);
  }

  window.lookupCatboxVideo = function (raw) {
    const out = document.getElementById('rx-catbox-lookup-result');
    if (!out) return;
    const q = String(raw || '').trim().toLowerCase();
    if (!q) { out.innerHTML = ''; return; }

    const cleanKey = q.split('#')[0].split('?')[0].replace(/^.*catbox\.moe\//, '').replace(/\.mp4$/, '');
    const videosMap = (catboxRegistry && catboxRegistry.videos) || {};
    let match = null;
    for (const [k, v] of Object.entries(videosMap)) {
      if (k.toLowerCase().includes(cleanKey) || (v.catbox_id || '').toLowerCase().includes(cleanKey)) {
        match = v;
        break;
      }
    }

    if (!match) {
      out.innerHTML = `<span style="color:#fbbf24; font-weight:700;">ℹ️ Nenhum produto usa o código "${esc(cleanKey)}" ainda — vídeo livre para vincular!</span>`;
      return;
    }

    const conflicts = ((catboxRegistry && catboxRegistry.conflicts_detected) || []).filter(c => c.url.toLowerCase().includes(cleanKey));
    const conflictNote = conflicts.length > 0
      ? `<div style="color:#f87171; margin-top:4px;">⚠️ Atenção: também aparece referenciado no(s) produto(s): ${conflicts.map(c => '#' + c.also_used_in).join(', ')}</div>`
      : `<div style="color:#34d399; margin-top:3px;">✅ Exclusivo 1:1 — zero conflito com outros produtos.</div>`;

    out.innerHTML = `
      <div style="background:#090d16; border:1px solid rgba(16,185,129,0.35); border-radius:8px; padding:10px 12px;">
        <div>🔒 <strong>Dono Oficial:</strong> <span style="color:#38bdf8; font-weight:800;">Produto #${match.owner_product_id}</span> — ${esc(match.owner_product_title)}</div>
        <div style="color:#94a3b8; font-size:11.5px; margin-top:2px;">Slot: <code>${esc(match.slot)}</code> · Tag Oficial: <code>${esc(match.tagged_url)}</code></div>
        ${conflictNote}
        <button type="button" class="rx-btn-360" style="margin-top:8px; padding:5px 10px;" onclick="window.openProduct360(${match.owner_product_id}, 'videos')">Abrir Produto #${match.owner_product_id} nos Vídeos</button>
      </div>
    `;
  };

  window.setRxHealthFilter = function (mode, btn) {
    activeHealthFilter = mode;
    document.querySelectorAll('#rx-health-filters .rx-filter-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    window.filtrarCatalogo();
  };

  function getFiltered360List() {
    if (!manifest360) return [];
    const term = (document.getElementById('catalogoSearch')?.value || '').toLowerCase().trim();
    return manifest360.products.filter((p) => {
      if (activeHealthFilter === 'perfect' && p.health_score < 100) return false;
      if (activeHealthFilter === '30plus' && p.creators_count < 30) return false;
      if (activeHealthFilter === 'low_creators' && p.creators_count >= 10) return false;
      if (activeHealthFilter === 'conflict' && !p.has_catbox_conflict) return false;

      if (!term) return true;
      if (String(p.id) === term || `#${p.id}` === term) return true;
      if ((p.title || '').toLowerCase().includes(term)) return true;
      if (p.video && (p.video.catbox_id || '').toLowerCase().includes(term)) return true;
      if ((p.creators || []).some(c => (c.catbox_id || '').toLowerCase().includes(term) || (c.username || '').toLowerCase().includes(term))) return true;
      return false;
    });
  }

  function overrideCatalogFunctions() {
    window.carregarCatalogo = function () {
      renderCards360(getFiltered360List());
    };
    window.filtrarCatalogo = function () {
      renderCards360(getFiltered360List());
    };
    window.salvarPreco = async function (id) {
      const saleVal = parseFloat(document.getElementById(`salePrice-${id}`)?.value);
      const origVal = (document.getElementById(`origPrice-${id}`)?.value || '').trim();
      if (isNaN(saleVal) || saleVal <= 0) {
        if (typeof window.showToast === 'function') window.showToast('Preço inválido!', 'danger');
        return;
      }
      try {
        const r = await fetch('/api/admin-config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            action: 'save_product_override',
            productId: id,
            patch: { preco: saleVal, precoOrig: origVal },
          }),
        });
        const j = await r.json();
        if (j && j.overrides) serverOverrides = j.overrides;
        const prod = manifest360.products.find(x => x.id === Number(id));
        if (prod) { prod.preco = saleVal; prod.price_original_str = origVal; }
        if (typeof window.showToast === 'function') {
          window.showToast(`✅ Produto #${id} atualizado no SERVIDOR para R$ ${saleVal.toFixed(2)}!`, 'success');
        }
      } catch (e) {
        if (typeof window.showToast === 'function') window.showToast('Erro ao salvar no servidor', 'danger');
      }
    };
  }

  function renderCards360(list) {
    const container = document.getElementById('productsContainer');
    if (!container) return;
    if (!list.length) {
      container.innerHTML = `<div style="text-align:center; padding:36px; color:#94a3b8;">Nenhum produto encontrado para este filtro.</div>`;
      return;
    }

    container.innerHTML = list.map((p) => {
      const ov = serverOverrides[String(p.id)] || {};
      const curPreco = ov.preco || p.preco || 0;
      const origStr = ov.precoOrig || p.price_original_str || (p.preco_antigo ? `R$ ${Number(p.preco_antigo).toFixed(2).replace('.', ',')}` : '');
      const varCount = Object.keys(p.variacoes || {}).reduce((acc, k) => acc + (((p.variacoes[k] || {}).opcoes || []).length), 0);
      const scoreClass = p.health_score >= 90 ? 'ok' : 'warn';

      return `
        <div class="product-card" id="productCard-${p.id}">
          <div class="product-card-top" style="cursor:pointer;" onclick="window.openProduct360(${p.id}, 'slides')">
            <img src="${esc(p.img || 'logo.png')}" class="product-thumb" alt="${esc(p.title)}" loading="lazy" onerror="this.src='logo.png'">
            <div class="product-info">
              <div class="product-meta-row">
                <span class="product-id-badge">#${p.id}</span>
                <span class="product-badge-sales">★ ${esc(p.rating_score)} · ${esc(p.sold_count)}</span>
                <span class="rx-mini-badge ${scoreClass}">🛡️ ${p.health_score}%</span>
              </div>
              <div class="product-title" title="${esc(p.title)}">${esc(p.title)}</div>
              <div class="rx-badges-strip">
                <span class="rx-mini-badge ${p.slides.length >= 4 ? 'ok' : 'warn'}">🖼️ ${p.slides.length} slides</span>
                <span class="rx-mini-badge ${p.video ? 'ok' : 'warn'}">🎬 ${p.video ? ('Desc: ' + (p.video.catbox_id || 'OK')) : 'Sem vídeo'}</span>
                <span class="rx-mini-badge ${p.creators_count >= 10 ? 'ok' : 'warn'}">📱 ${p.creators_count} criadores</span>
                <span class="rx-mini-badge ok">⭐ ${p.reviews_count} (${p.reviews_photos_count} fotos)</span>
                ${varCount ? `<span class="rx-mini-badge">🎨 ${varCount} SKUs</span>` : ''}
              </div>
            </div>
          </div>

          <div class="product-price-editor">
            <div class="price-input-group">
              <span class="price-input-label">De (Riscado)</span>
              <input type="text" id="origPrice-${p.id}" class="price-input orig" value="${esc(origStr)}">
            </div>
            <div class="price-input-group">
              <span class="price-input-label">Por (Venda Global)</span>
              <input type="number" step="0.01" id="salePrice-${p.id}" class="price-input" value="${Number(curPreco).toFixed(2)}">
            </div>
            <button class="btn-save-price" onclick="salvarPreco(${p.id})">Salvar Global</button>
          </div>

          <div class="product-card-actions" style="flex-wrap:wrap; gap:8px;">
            <button type="button" class="rx-btn-360" onclick="window.openProduct360(${p.id}, 'slides')">
              🔍 Raio-X 360° & Mídias
            </button>
            <div style="display:flex; gap:6px; flex-wrap:wrap;">
              <a href="pages/produto-${p.id}" target="_blank" class="btn-action-pill">
                <span>Abrir Loja</span>
              </a>
              <button type="button" class="btn-action-pill tiktok" onclick="copiarLinkTikTokAds(${p.id})">
                <span>UTM TikTok Ads</span>
              </button>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }

  function createModalShell() {
    if (document.getElementById('rx-modal-overlay')) return;
    const div = document.createElement('div');
    div.id = 'rx-modal-overlay';
    div.className = 'rx-modal-overlay';
    div.innerHTML = `
      <div class="rx-modal-box" onclick="event.stopPropagation()">
        <div class="rx-modal-head">
          <div style="min-width:0;">
            <div id="rx-m-title" style="font-size:16px; font-weight:800; color:#f8fafc; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Produto</div>
            <div id="rx-m-sub" style="font-size:12px; color:#94a3b8; margin-top:2px;"></div>
          </div>
          <div style="display:flex; gap:8px; align-items:center; flex-shrink:0;">
            <a id="rx-m-open-link" href="#" target="_blank" class="btn-action-pill" style="text-decoration:none;">Ver na Loja ↗</a>
            <button type="button" onclick="window.closeProduct360()" style="background:#1e293b; border:1px solid rgba(255,255,255,0.15); color:#fff; width:34px; height:34px; border-radius:8px; cursor:pointer; font-size:16px;">✕</button>
          </div>
        </div>
        <div class="rx-tabs-bar" id="rx-tabs-bar"></div>
        <div class="rx-modal-body" id="rx-modal-body"></div>
      </div>
    `;
    div.addEventListener('click', () => window.closeProduct360());
    document.body.appendChild(div);
  }

  window.openProduct360 = function (id, tab = 'slides') {
    if (!manifest360) return;
    const prod = manifest360.products.find(x => x.id === Number(id));
    if (!prod) return;
    currentModalProd = prod;
    currentModalTab = tab;
    reviewsOnlyPhotos = false;

    document.getElementById('rx-m-title').textContent = `#${prod.id} — ${prod.title}`;
    document.getElementById('rx-m-sub').textContent = `R$ ${Number(prod.preco).toFixed(2).replace('.', ',')} · ${prod.slides.length} slides · ${prod.creators_count} vídeos criadores · ${prod.reviews_count} avaliações · Score ${prod.health_score}%`;
    document.getElementById('rx-m-open-link').href = `/pages/produto-${prod.id}`;

    renderModal360Tabs();
    renderModal360Content();
    document.getElementById('rx-modal-overlay').classList.add('open');
    document.body.style.overflow = 'hidden';
  };

  window.closeProduct360 = function () {
    const ov = document.getElementById('rx-modal-overlay');
    if (ov) ov.classList.remove('open');
    const body = document.getElementById('rx-modal-body');
    if (body) body.innerHTML = '';
    document.body.style.overflow = '';
  };

  window.switchModal360Tab = function (tab) {
    currentModalTab = tab;
    renderModal360Tabs();
    renderModal360Content();
  };

  function renderModal360Tabs() {
    const p = currentModalProd;
    if (!p) return;
    const tabs = [
      { id: 'slides', label: `🖼️ Slider (${p.slides.length})` },
      { id: 'videos', label: `🎬 Vídeos & Catbox (${(p.video ? 1 : 0) + p.creators_count})` },
      { id: 'variacoes', label: `🎨 Variações & SKUs` },
      { id: 'descricao', label: `📋 Detalhes & Descrição` },
      { id: 'reviews', label: `⭐ Avaliações (${p.reviews_count})` },
      { id: 'config', label: `💰 Order Bump & JSON` },
    ];
    document.getElementById('rx-tabs-bar').innerHTML = tabs.map(t =>
      `<button type="button" class="rx-tab ${currentModalTab === t.id ? 'active' : ''}" onclick="window.switchModal360Tab('${t.id}')">${t.label}</button>`
    ).join('');
  }

  function renderModal360Content() {
    const p = currentModalProd;
    const box = document.getElementById('rx-modal-body');
    if (!p || !box) return;

    if (currentModalTab === 'slides') {
      box.innerHTML = `
        <div style="margin-bottom:12px; font-size:13px; color:#94a3b8;">
          Todas as fotos oficiais do carrossel principal do <strong>Produto #${p.id}</strong> (clique na foto para abrir em tamanho real):
        </div>
        <div class="rx-slides-grid">
          ${p.slides.map((s, idx) => `
            <div class="rx-slide-card">
              <img src="${esc(s.src)}" alt="${esc(s.alt)}" onclick="window.open('${esc(s.src)}','_blank')"
                   onload="this.nextElementSibling.querySelector('.rx-dim').textContent = this.naturalWidth + '×' + this.naturalHeight"
                   onerror="this.style.border='2px solid #ef4444'; this.nextElementSibling.querySelector('.rx-dim').innerHTML='<span style=color:#ef4444>⚠️ ERRO 404</span>'">
              <div style="padding:8px 10px; font-size:11.5px; display:flex; justify-content:space-between; align-items:center;">
                <strong style="color:#f8fafc;">Slide #${idx + 1}</strong>
                <span class="rx-dim" style="color:#10b981; font-family:monospace;">...</span>
              </div>
              <div style="padding:0 10px 8px; font-size:10.5px; color:#64748b; word-break:break-all;">${esc(s.src)}</div>
            </div>
          `).join('')}
        </div>
      `;
      return;
    }

    if (currentModalTab === 'videos') {
      const descVideoHtml = p.video ? `
        <div style="background:#131b2e; border:1px solid rgba(16,185,129,0.3); border-radius:12px; padding:14px; margin-bottom:18px; display:grid; grid-template-columns: minmax(220px, 320px) 1fr; gap:16px; align-items:center;">
          <video controls playsinline preload="metadata" poster="${esc(p.video.poster)}" src="${esc(p.video.src)}" style="width:100%; aspect-ratio:16/9; background:#000; border-radius:10px; object-fit:contain;"></video>
          <div>
            <div style="font-size:14px; font-weight:800; color:#34d399; margin-bottom:6px;">🎬 Vídeo Oficial da Descrição (Player 16:9)</div>
            <div style="font-size:12px; color:#cbd5e1; margin-bottom:4px;"><strong>Catbox ID Travado:</strong> <code style="color:#38bdf8;">${esc(p.video.catbox_id || 'Local')}</code></div>
            <div style="font-size:12px; color:#94a3b8; word-break:break-all; margin-bottom:6px;"><strong>URL Carimbada:</strong> <code>${esc(p.video.src)}</code></div>
            <div style="font-size:12px; color:#94a3b8;"><strong>Duração cadastrada:</strong> ${esc(p.video.duration || 'Auto')}</div>
          </div>
        </div>
      ` : `<div style="padding:14px; background:rgba(239,68,68,0.12); border-radius:10px; color:#fca5a5; margin-bottom:16px;">⚠️ Este produto não possui vídeo na descrição.</div>`;

      box.innerHTML = `
        <!-- UPLOADER CATBOX TRAVADO AO PRODUTO -->
        <div style="background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.35); border-radius:12px; padding:14px; margin-bottom:18px;">
          <div style="font-size:14px; font-weight:800; color:#34d399;">🔒 Uploader & Trava Catbox Exclusiva — Produto #${p.id}</div>
          <div style="font-size:12px; color:#94a3b8; margin-top:3px;">
            Suba um MP4 ou cole um link Catbox para carimbar e travar exclusivamente no <strong>Produto #${p.id}</strong> (bloqueia automaticamente se já pertencer a outro produto!):
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; align-items:center;">
            <select id="rx-up-slot" style="background:#07090e; color:#fff; border:1px solid rgba(255,255,255,0.18); border-radius:8px; padding:8px 10px; font-size:12.5px;">
              <option value="descricao">Slot: Vídeo da Descrição</option>
              <option value="criador_${p.creators_count + 1}">Slot: Novo Vídeo de Criador (#${p.creators_count + 1})</option>
            </select>
            <input type="file" id="rx-up-file" accept="video/mp4,video/webm" style="font-size:12px; color:#cbd5e1;">
            <button type="button" class="rx-btn-360" style="background:#10b981; color:#04130d;" onclick="window.uploadVideoLockedFromAdmin(${p.id})">⬆️ Subir na Catbox & Travar no #${p.id}</button>
          </div>
          <div style="display:flex; gap:8px; margin-top:8px; flex-wrap:wrap;">
            <input type="text" id="rx-lock-url-input" class="rx-checker-input" placeholder="Ou cole uma URL https://files.catbox.moe/xxxx.mp4 já existente para travar no Produto #${p.id}">
            <button type="button" class="rx-btn-360" onclick="window.lockExistingCatboxUrl(${p.id})">🔒 Validar & Travar URL</button>
          </div>
          <div id="rx-up-status" style="margin-top:8px; font-size:12.5px;"></div>
        </div>

        ${descVideoHtml}

        <div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:10px;">
          📱 Vídeos de Criadores deste Produto (${p.creators_count}) — Clique em qualquer vídeo para dar Play e conferir:
        </div>
        <div class="rx-creators-grid">
          ${p.creators.map((c, idx) => `
            <div class="rx-creator-card">
              <div class="rx-creator-media">
                <video controls playsinline preload="none" poster="${esc(c.poster || c.avatar)}" src="${esc(c.video)}"></video>
              </div>
              <div style="padding:8px 10px; font-size:11.5px;">
                <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px;">
                  <img src="${esc(c.avatar)}" alt="" style="width:22px; height:22px; border-radius:50%; object-fit:cover;" onerror="this.src='logo.png'">
                  <strong style="color:#f8fafc; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">@${esc(c.username)}</strong>
                </div>
                <div style="color:#38bdf8; font-family:monospace; font-size:10.5px;">#${idx + 1} · ${esc(c.catbox_id || 'local')}</div>
                <div style="color:#94a3b8; font-size:11px; margin-top:3px; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;">${esc(c.description)}</div>
              </div>
            </div>
          `).join('')}
        </div>
      `;
      return;
    }

    if (currentModalTab === 'variacoes') {
      const entries = Object.entries(p.variacoes || {});
      if (!entries.length) {
        box.innerHTML = `<div style="color:#94a3b8; padding:20px;">Produto de opção única padrão (sem grade de variações).</div>`;
        return;
      }
      box.innerHTML = entries.map(([key, grp]) => {
        const opts = (grp && grp.opcoes) || [];
        return `
          <div style="background:#131b2e; border:1px solid rgba(255,255,255,0.09); border-radius:12px; padding:14px; margin-bottom:14px;">
            <div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:10px;">${esc(grp.label || key)} (${opts.length} opções)</div>
            <div style="display:flex; flex-wrap:wrap; gap:10px;">
              ${opts.map((op) => {
                if (typeof op === 'object' && op !== null) {
                  const img = (op.imagem || '').replace(/^\.\.\//, '');
                  return `
                    <div style="background:#0b101b; border:1px solid rgba(255,255,255,0.12); border-radius:10px; padding:8px; width:125px; text-align:center;">
                      ${img ? `<img src="${esc(img)}" style="width:100%; aspect-ratio:1/1; object-fit:cover; border-radius:6px; margin-bottom:6px;">` : ''}
                      <div style="font-size:12px; font-weight:700; color:#f8fafc;">${esc(op.nome)}</div>
                      ${op.preco ? `<div style="font-size:11px; color:#34d399;">R$ ${Number(op.preco).toFixed(2)}</div>` : ''}
                    </div>
                  `;
                }
                return `<span style="background:#0b101b; border:1px solid rgba(255,255,255,0.15); border-radius:8px; padding:8px 14px; font-size:12.5px; font-weight:700; color:#f8fafc;">${esc(op)}</span>`;
              }).join('')}
            </div>
          </div>
        `;
      }).join('');
      return;
    }

    if (currentModalTab === 'descricao') {
      box.innerHTML = `
        <div style="background:#131b2e; border:1px solid rgba(255,255,255,0.09); border-radius:12px; padding:14px; margin-bottom:16px;">
          <div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:10px;">📌 Ficha Técnica (Detalhes — ${p.details.length} atributos)</div>
          <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap:8px;">
            ${p.details.map(d => `
              <div style="background:#0b101b; padding:8px 12px; border-radius:8px; font-size:12.5px;">
                <div style="color:#94a3b8; font-size:11px;">${esc(d.label)}</div>
                <div style="color:#f8fafc; font-weight:700; margin-top:2px;">${esc(d.value)}</div>
              </div>
            `).join('')}
          </div>
        </div>

        ${p.size_guide_html ? `<div style="margin-bottom:16px;"><div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:8px;">📏 Guia de Tamanhos</div><div class="rx-desc-preview">${p.size_guide_html}</div></div>` : ''}

        <div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:8px;">📝 Descrição Completa Renderizada</div>
        <div class="rx-desc-preview">${p.description_html || '<em>Sem descrição</em>'}</div>
      `;
      return;
    }

    if (currentModalTab === 'reviews') {
      const list = reviewsOnlyPhotos ? p.reviews.filter(r => r.photos && r.photos.length > 0) : p.reviews;
      box.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
          <div style="font-size:13.5px; font-weight:700; color:#f8fafc;">
            Exibindo ${list.length} de ${p.reviews_count} avaliações (${p.reviews_photos_count} fotos de unboxing)
          </div>
          <button type="button" class="rx-filter-btn ${reviewsOnlyPhotos ? 'active' : ''}" onclick="window.toggleRxReviewsPhotoFilter()">
            📸 Mostrar só com foto de unboxing
          </button>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px;">
          ${list.map(r => `
            <div style="background:#131b2e; border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:12px;">
              <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                <img src="${esc(r.avatar)}" style="width:32px; height:32px; border-radius:50%; object-fit:cover;" onerror="this.src='logo.png'">
                <div>
                  <div style="font-size:13px; font-weight:700; color:#f8fafc;">${esc(r.name)} <span style="color:#fbbf24;">${'★'.repeat(r.stars || 5)}</span></div>
                  <div style="font-size:11px; color:#94a3b8;">${esc(r.date_line || r.variation)}</div>
                </div>
              </div>
              <div style="font-size:13px; color:#e2e8f0; line-height:1.45;">${esc(r.comment)}</div>
              ${(r.photos && r.photos.length) ? `
                <div style="display:flex; gap:8px; margin-top:8px; flex-wrap:wrap;">
                  ${r.photos.map(ph => `<img src="${esc(ph)}" onclick="window.open('${esc(ph)}','_blank')" style="width:76px; height:76px; object-fit:cover; border-radius:6px; cursor:zoom-in; border:1px solid rgba(255,255,255,0.15);">`).join('')}
                </div>
              ` : ''}
            </div>
          `).join('')}
        </div>
      `;
      return;
    }

    if (currentModalTab === 'config') {
      const ov = serverOverrides[String(p.id)] || {};
      const bump = ov.order_bump || { title: 'Garantia Estendida + Envio Prioritário', price: 9.90, enabled: true };
      const utmUrl = `https://stoneshopclone.vercel.app/pages/produto-${p.id}?utm_source=tiktok&utm_medium=cpc&utm_campaign=bf_stoneshop&utm_content=prod_${p.id}`;
      box.innerHTML = `
        <div style="background:#131b2e; border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:16px; margin-bottom:16px;">
          <div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:8px;">🎯 Link Oficial de Campanha TikTok Ads (Produto #${p.id})</div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <input type="text" readonly class="rx-checker-input" value="${esc(utmUrl)}">
            <button type="button" class="rx-btn-360" onclick="navigator.clipboard.writeText('${esc(utmUrl)}'); showToast && showToast('Link copiado!','success')">Copiar Link UTM</button>
          </div>
        </div>

        <div style="background:#131b2e; border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:16px; margin-bottom:16px;">
          <div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:10px;">💰 Order Bump Individual no Checkout para quem compra o Produto #${p.id}</div>
          <div style="display:grid; grid-template-columns: 1fr 140px auto; gap:10px; align-items:end;">
            <div>
              <label style="font-size:11.5px; color:#94a3b8;">Título da Oferta Complementar</label>
              <input type="text" id="rx-bump-title" class="rx-checker-input" style="width:100%; margin-top:4px;" value="${esc(bump.title || '')}">
            </div>
            <div>
              <label style="font-size:11.5px; color:#94a3b8;">Valor (R$)</label>
              <input type="number" step="0.01" id="rx-bump-price" class="rx-checker-input" style="width:100%; margin-top:4px;" value="${Number(bump.price || 9.90).toFixed(2)}">
            </div>
            <button type="button" class="rx-btn-360" style="background:#10b981; color:#04130d; height:36px;" onclick="window.saveProductBump(${p.id})">Salvar Bump</button>
          </div>
        </div>

        <div style="background:#131b2e; border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:16px;">
          <div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:6px;">📦 Fonte Única JSON (data/produtos/produto-${p.id}.json)</div>
          <div style="font-size:12px; color:#94a3b8; margin-bottom:10px;">Baixe o JSON individual completo deste produto para backup ou inspeção técnica:</div>
          <a href="data/produtos/produto-${p.id}.json" download="produto-${p.id}.json" class="rx-btn-360" style="text-decoration:none;">⬇️ Baixar produto-${p.id}.json</a>
        </div>
      `;
    }
  }

  window.toggleRxReviewsPhotoFilter = function () {
    reviewsOnlyPhotos = !reviewsOnlyPhotos;
    renderModal360Content();
  };

  window.saveProductBump = async function (pid) {
    const title = document.getElementById('rx-bump-title')?.value?.trim() || '';
    const price = parseFloat(document.getElementById('rx-bump-price')?.value) || 9.90;
    const r = await fetch('/api/admin-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'save_product_override',
        productId: pid,
        patch: { order_bump: { title, price, enabled: true } },
      }),
    });
    const j = await r.json();
    if (j && j.overrides) serverOverrides = j.overrides;
    if (typeof window.showToast === 'function') window.showToast(`Order Bump do Produto #${pid} salvo!`, 'success');
  };

  window.lockExistingCatboxUrl = async function (pid) {
    const statusEl = document.getElementById('rx-up-status');
    const rawUrl = (document.getElementById('rx-lock-url-input')?.value || '').trim();
    const slot = document.getElementById('rx-up-slot')?.value || 'criador';
    if (!rawUrl.includes('catbox.moe/')) {
      statusEl.innerHTML = `<span style="color:#f87171;">Informe uma URL válida https://files.catbox.moe/xxxx.mp4</span>`;
      return;
    }
    const base = rawUrl.split('#')[0].split('?')[0].trim();

    // Checa primeiro no catboxRegistry estático
    const existingStatic = catboxRegistry && catboxRegistry.videos && catboxRegistry.videos[base];
    if (existingStatic && Number(existingStatic.owner_product_id) !== Number(pid)) {
      statusEl.innerHTML = `<span style="color:#f87171; font-weight:700;">🚨 CONFLITO BLOQUEADO! Este vídeo já pertence ao Produto #${existingStatic.owner_product_id} (${esc(existingStatic.owner_product_title)})!</span>`;
      return;
    }

    const r = await fetch('/api/admin-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'register_catbox_lock', productId: pid, baseUrl: base, slot }),
    });
    const j = await r.json();
    if (!r.ok || j.conflict) {
      statusEl.innerHTML = `<span style="color:#f87171; font-weight:700;">🚨 ${esc(j.error || 'Conflito detectado!')}</span>`;
      return;
    }
    if (catboxRegistry && catboxRegistry.videos) {
      catboxRegistry.videos[base] = {
        catbox_id: base.split('/').pop(),
        base_url: base,
        tagged_url: j.lock.tagged_url,
        owner_product_id: pid,
        owner_product_title: currentModalProd ? currentModalProd.title : `Produto #${pid}`,
        slot,
      };
    }
    statusEl.innerHTML = `<div style="color:#34d399; font-weight:700;">✅ Vídeo travado com exclusividade no Produto #${pid}!<br>URL Oficial Carimbada: <code>${esc(j.lock.tagged_url)}</code> <button type="button" class="rx-btn-360" style="padding:3px 8px; margin-left:6px;" onclick="navigator.clipboard.writeText('${esc(j.lock.tagged_url)}')">Copiar</button></div>`;
  };

  window.uploadVideoLockedFromAdmin = async function (pid) {
    const statusEl = document.getElementById('rx-up-status');
    const fileInput = document.getElementById('rx-up-file');
    const slot = document.getElementById('rx-up-slot')?.value || 'criador';
    const file = fileInput && fileInput.files && fileInput.files[0];
    if (!file) {
      statusEl.innerHTML = `<span style="color:#fbbf24;">Selecione um arquivo de vídeo .mp4 primeiro!</span>`;
      return;
    }

    statusEl.innerHTML = `<span style="color:#38bdf8;">⏳ Enviando "${esc(file.name)}" para a Catbox com trava SHA-256 no Produto #${pid}...</span>`;
    try {
      // Até 3.2 MB envia via relay /api/admin-config (sem bloqueio CORS e com trava SHA-256 server-side!)
      if (file.size <= 3.2 * 1024 * 1024) {
        const b64 = await new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(String(reader.result).split(',')[1]);
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
        const r = await fetch('/api/admin-config', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ action: 'upload_catbox_base64', productId: pid, slot, base64: b64 }),
        });
        const j = await r.json();
        if (!r.ok || !j.success) {
          throw new Error(j.error || 'Falha no upload Catbox');
        }
        statusEl.innerHTML = `<div style="color:#34d399; font-weight:700;">✅ Upload Catbox Concluído e Travado no Produto #${pid}!<br>URL Oficial: <code>${esc(j.lock.tagged_url)}</code> <button type="button" class="rx-btn-360" style="padding:3px 8px; margin-left:6px;" onclick="navigator.clipboard.writeText('${esc(j.lock.tagged_url)}')">Copiar</button></div>`;
        return;
      }

      const form = new FormData();
      form.append('reqtype', 'fileupload');
      form.append('fileToUpload', file, `stoneshop_prod_${pid}_${slot}_${Date.now()}.mp4`);
      const upResp = await fetch('https://catbox.moe/user/api.php', { method: 'POST', body: form });
      const txt = (await upResp.text()).trim();
      if (!upResp.ok || !txt.startsWith('https://files.catbox.moe/')) {
        throw new Error('Arquivo acima de 3.2MB — suba pelo terminal sem limite: node scripts/upload-catbox.js --produto ' + pid + ' --tipo ' + slot + ' --arquivo "' + file.name + '"');
      }
      document.getElementById('rx-lock-url-input').value = txt;
      await window.lockExistingCatboxUrl(pid);
    } catch (err) {
      statusEl.innerHTML = `<div style="color:#fbbf24;">⚠️ ${esc(err.message)}</div>`;
    }
  };

  async function enhancePedidosWithRecovery() {
    try {
      const r = await fetch('/api/pedidos');
      if (!r.ok) return;
      const j = await r.json();
      const pending = (j.pedidos || []).filter(p => p.status === 'pending');
      const secPedidos = document.getElementById('view-pedidos');
      if (!secPedidos || !pending.length || document.getElementById('rx-pix-recovery-banner')) return;

      const banner = document.createElement('div');
      banner.id = 'rx-pix-recovery-banner';
      banner.style.cssText = 'background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.35); border-radius:12px; padding:12px 14px; margin-bottom:14px;';
      banner.innerHTML = `
        <div style="font-size:13.5px; font-weight:800; color:#fbbf24; margin-bottom:8px;">
          🔥 Fila de Recuperação de Pix (${pending.length} aguardando pagamento)
        </div>
        <div style="display:flex; flex-direction:column; gap:8px;">
          ${pending.slice(0, 8).map(o => `
            <div style="display:flex; justify-content:space-between; align-items:center; gap:8px; background:#0b101b; padding:8px 12px; border-radius:8px; flex-wrap:wrap;">
              <div style="font-size:12.5px; color:#e2e8f0;">
                <strong>${esc((o.customer && o.customer.name) || 'Cliente')}</strong> · R$ ${Number(o.amount || 0).toFixed(2).replace('.', ',')}
                <span style="color:#94a3b8; font-size:11px; margin-left:6px;">há ${o.ageMinutes || 0} min</span>
              </div>
              ${o.whatsappRecoveryUrl ? `<a href="${esc(o.whatsappRecoveryUrl)}" target="_blank" style="background:#25D366; color:#04130d; text-decoration:none; padding:5px 10px; border-radius:6px; font-size:12px; font-weight:800;">💬 Recuperar no WhatsApp</a>` : ''}
            </div>
          `).join('')}
        </div>
      `;
      secPedidos.insertBefore(banner, secPedidos.firstChild);
    } catch (_) {}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAdmin360);
  } else {
    initAdmin360();
  }
})();
