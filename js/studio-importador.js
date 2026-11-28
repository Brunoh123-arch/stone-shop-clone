(function () {
  let currentDraft = null;
  let sseSource = null;
  let saveTimer = null;

  const urlKey = new URLSearchParams(window.location.search).get('key') || '';
  if (urlKey) {
    try { localStorage.setItem('STONE_STUDIO_KEY', urlKey); } catch (_) {}
  }

  function getStudioKey() {
    return urlKey || localStorage.getItem('STONE_STUDIO_KEY') || '';
  }

  async function api(pathUrl, method = 'GET', body = null) {
    const headers = { 'x-studio-key': getStudioKey() };
    if (body) headers['Content-Type'] = 'application/json';
    const resp = await fetch(pathUrl, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    });
    const data = await resp.json().catch(() => ({}));
    return { status: resp.status, ok: resp.ok, data };
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function toast(msg) {
    const el = document.getElementById('stToast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(window._stToastTimer);
    window._stToastTimer = setTimeout(() => el.classList.remove('show'), 2400);
  }

  function setBanner(msg, isWarn = false) {
    const b = document.getElementById('statusBanner');
    if (!b) return;
    if (!msg) {
      b.style.display = 'none';
      return;
    }
    b.style.display = 'block';
    b.style.borderColor = isWarn ? 'rgba(245,158,11,0.5)' : 'rgba(59,130,246,0.4)';
    b.style.color = isWarn ? '#fde68a' : '#bfdbfe';
    b.textContent = msg;
  }

  function postLiveToPhone(payload) {
    const ifr = document.getElementById('studioPhoneIframe');
    if (ifr && ifr.contentWindow) {
      ifr.contentWindow.postMessage({ type: 'STUDIO_LIVE_PATCH', payload }, '*');
    }
  }

  function formatBRL(num) {
    const [i, d] = Number(num || 0).toFixed(2).split('.');
    return i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + ',' + d;
  }

  window.onLiveFieldInput = function () {
    if (!currentDraft) return;
    const title = document.getElementById('editTitle').value;
    const pix = Math.max(1, Number(document.getElementById('editPix').value || 49.89));
    const orig = Math.max(pix + 5, Number(document.getElementById('editOrig').value || pix * 3.5));
    const sold = Math.max(10, Number(document.getElementById('editSold').value || 4820));

    const [pInt, pDec] = pix.toFixed(2).split('.');
    const pct = Math.min(90, Math.max(20, Math.round((1 - pix / orig) * 100)));
    const v3x = (Math.floor((pix / 3) * 100) / 100).toFixed(2).replace('.', ',');

    // 0ms instant DOM update inside mobile iframe!
    postLiveToPhone({
      product_title: title,
      price_int: pInt.replace(/\B(?=(\d{3})+(?!\d))/g, '.'),
      price_cents: ',' + pDec,
      price_original: 'R$ ' + formatBRL(orig),
      discount_badge: `-${pct}%`,
      installment_text: `3x R$ ${v3x}`,
      coupon_main: `Economize R$ ${formatBRL(orig - pix)}`,
      sold_num: sold,
    });

    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      window.saveDraftPatch({
        product_title: title,
        price_pix: pix,
        price_original_num: orig,
        sold_num: sold,
      }, true);
    }, 280);
  };

  window.saveDraftPatch = async function (patch, silent = false) {
    if (!currentDraft) return;
    const res = await api(`/api/studio/draft/${currentDraft.draftId}`, 'POST', patch);
    if (res.ok && res.data.draft) {
      currentDraft = res.data.draft;
      renderDraftPanels(silent);
      if (res.data.livePatch) postLiveToPhone(res.data.livePatch);
      if (!silent) toast('Atualizado!');
    }
  };

  window.popMore = async function (kind, count) {
    if (!currentDraft) return toast('Cole um link primeiro!');
    const res = await api(`/api/studio/draft/${currentDraft.draftId}/more`, 'POST', { kind, count });
    if (!res.ok) return;
    currentDraft = res.data.draft;
    renderDraftPanels(false);
    if (res.data.livePatch) {
      const scrollMap = {
        videos: '#creators-section',
        unboxings: '.reviews-section',
        reviews: '.reviews-section',
      };
      postLiveToPhone({ ...res.data.livePatch, scrollToSection: scrollMap[kind] });
    }
    if (res.data.added && res.data.added.length) {
      toast(`⚡ +${res.data.added.length} adicionado(s) na hora!`);
    } else {
      toast('Reserva esgotada — buscando mais em background...');
    }
  };

  function connectStream(draftId) {
    if (sseSource) sseSource.close();
    const k = encodeURIComponent(getStudioKey());
    sseSource = new EventSource(`/api/studio/stream/${draftId}?key=${k}`);

    const onStage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.draft) {
          currentDraft = data.draft;
          renderDraftPanels(false);
        }
        if (data.livePatch) postLiveToPhone(data.livePatch);
        if (data.event === 'fast_preview') {
          setBanner('⚡ Prévia rápida aberta! Carregando banco reserva de unboxings e vídeos nos bastidores...');
          window.reloadPreviewIframe();
        } else if (data.event === 'reviews_pool_ready') {
          setBanner('📸 Fotos 1:1, variações e avaliações reais carregadas! Preparando vídeos...');
        } else if (data.event === 'videos_preview_ready') {
          setBanner('✅ Tudo pronto na tela! Os MP4s já estão subindo pro Catbox em 4x paralelo nos bastidores.');
        } else if (data.event === 'warning' && data.extra && data.extra.message) {
          setBanner('⚠️ ' + data.extra.message, true);
        }
      } catch (_) {}
    };

    ['fast_preview', 'reviews_pool_ready', 'videos_preview_ready', 'video_catbox_done', 'warning'].forEach((evt) => {
      sseSource.addEventListener(evt, onStage);
    });
  }

  window.startInstantExtract = async function (ev) {
    ev.preventDefault();
    const url1 = document.getElementById('url1Input').value.trim();
    const url2 = document.getElementById('url2Input').value.trim();
    const pricePix = Number(document.getElementById('initPixInput').value || 0);
    const gender = document.getElementById('initGenderSelect').value;
    const targetId = Number(document.getElementById('initTargetId').value || 0);

    if (!url1) return;
    const btn = document.getElementById('extractBtn');
    btn.disabled = true;
    btn.textContent = '⏳ Extraindo...';
    setBanner('🚀 Conectando no anúncio (modo zero-áudio) e montando página...');

    const res = await api('/api/studio/extract', 'POST', {
      url1,
      url2,
      price_pix: pricePix,
      gender,
      targetId,
      autoVideos: true,
    });

    btn.disabled = false;
    btn.textContent = '⚡ Puxar Tudo Agora';

    if (!res.ok) {
      setBanner('❌ ' + (res.data.error || 'Erro ao iniciar extração'), true);
      return;
    }

    currentDraft = res.data.draft;
    renderDraftPanels(false);
    const k = encodeURIComponent(getStudioKey());
    document.getElementById('studioPhoneIframe').src = `${res.data.previewUrl}&key=${k}`;
    connectStream(currentDraft.draftId);
    refreshStateHeader();
  };

  window.reloadPreviewIframe = function () {
    if (!currentDraft) return;
    const k = encodeURIComponent(getStudioKey());
    document.getElementById('studioPhoneIframe').src = `/api/studio/preview/${currentDraft.draftId}?owner=1&key=${k}&t=${Date.now()}`;
  };

  window.loadSelectedDraft = async function (draftId) {
    if (!draftId) return;
    const res = await api(`/api/studio/draft/${draftId}`);
    if (!res.ok) return;
    currentDraft = res.data.draft;
    renderDraftPanels(false);
    window.reloadPreviewIframe();
    connectStream(draftId);
  };

  function renderDraftPanels(skipTextInputs) {
    if (!currentDraft) return;
    const d = currentDraft;

    if (!skipTextInputs) {
      document.getElementById('editTitle').value = d.product_title || '';
      document.getElementById('editPix').value = d.price_pix || '';
      document.getElementById('editOrig').value = d.price_original_num || '';
      document.getElementById('editSold').value = d.sold_num || 4820;
      document.getElementById('editTargetId').value = d.targetId || '';
      document.getElementById('editCategory').value = d.category || 'casa';
      document.getElementById('editGender').value = d.gender || 'feminino';
      const qInp = document.getElementById('videoSearchQuery');
      if (qInp && !qInp.value && d.product_title && !d.product_title.startsWith('Extraindo')) {
        qInp.value = d.product_title.split(/\s+/).slice(0, 5).join(' ');
      }
    }

    // Reserve badges
    document.getElementById('resVideosCount').textContent = `${(d.reserve_videos || []).length} na reserva`;
    document.getElementById('resUnboxCount').textContent = `${(d.reserve_unboxings || []).length} na reserva`;
    document.getElementById('resReviewsCount').textContent = `${(d.reserve_reviews || []).length} na reserva`;

    document.getElementById('phonePreviewLabel').textContent = `Produto #${d.targetId} · R$ ${formatBRL(d.price_pix)}`;

    // Variations
    const vHost = document.getElementById('variationsHost');
    const vars = d.variations || {};
    vHost.innerHTML = Object.entries(vars).map(([gKey, grp]) => `
      <div class="st-var-group">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong style="font-size:12.5px;">${esc(grp.label || gKey)} (${(grp.opcoes || []).length})</strong>
          ${gKey !== 'cor' ? `<button type="button" class="st-mini-btn" onclick="window.removeVarGroup('${esc(gKey)}')">✕ Grupo</button>` : ''}
        </div>
        <div class="st-var-chips">
          ${(grp.opcoes || []).map((o, oIdx) => {
            const name = typeof o === 'string' ? o : o.nome;
            return `<span class="st-var-chip">${esc(name)} <button type="button" style="background:none;border:none;color:#f87171;cursor:pointer;" onclick="window.removeVarOption('${esc(gKey)}', ${oIdx})">✕</button></span>`;
          }).join('')}
          <button type="button" class="st-mini-btn" onclick="window.promptAddVarOption('${esc(gKey)}')">+ Opção</button>
        </div>
      </div>
    `).join('');

    // Slides
    const slides = d.slides || [];
    const sPill = document.getElementById('slidesCounterPill');
    sPill.textContent = `${slides.length} fotos`;
    sPill.className = `st-pill ${slides.length >= 4 ? 'ok' : 'warn'}`;
    document.getElementById('slidesGrid').innerHTML = slides.map((s, idx) => `
      <div class="st-media-card">
        <img src="${esc(s.src)}" alt="" loading="lazy" />
        <div class="st-media-actions">
          <button type="button" class="st-mini-btn" onclick="window.saveDraftPatch({ action: 'promote_slide', index: ${idx} })">${idx === 0 ? '★ Capa' : '↑ Capa'}</button>
          <button type="button" class="st-mini-btn" style="color:#f87171;" onclick="window.saveDraftPatch({ action: 'remove_slide', index: ${idx} })">✕</button>
        </div>
      </div>
    `).join('');

    // Unboxings
    const reviews = d.reviews || [];
    const unboxings = reviews.map((r, i) => ({ ...r, _idx: i })).filter((r) => Array.isArray(r.photos) && r.photos.length > 0);
    const uPill = document.getElementById('unboxCounterPill');
    uPill.textContent = `${unboxings.length}/6 cards c/ foto`;
    uPill.className = `st-pill ${unboxings.length >= 6 ? 'ok' : 'warn'}`;
    document.getElementById('tabFotosBadge').textContent = `(${slides.length}+${unboxings.length})`;

    document.getElementById('unboxGrid').innerHTML = unboxings.map((u) => `
      <div class="st-media-card">
        <img src="${esc(u.photos[0])}" alt="" loading="lazy" />
        <div class="st-media-actions">
          <span title="${esc(u.comment)}">${esc(u.name)} (${u.photos.length}ft)</span>
          <button type="button" class="st-mini-btn" style="color:#f87171;" onclick="window.saveDraftPatch({ action: 'remove_review', index: ${u._idx} })">✕</button>
        </div>
      </div>
    `).join('');

    // Videos
    const creators = d.creators || [];
    const descVid = d.video && d.video.src ? d.video : null;
    const allCatboxReady = [...(descVid ? [descVid] : []), ...creators].filter((v) => /catbox\.moe\//i.test(v.src || v.video || '')).length;
    const totalVids = (descVid ? 1 : 0) + creators.length;
    const vPill = document.getElementById('catboxStatusPill');
    vPill.textContent = `${allCatboxReady}/${totalVids} no Catbox`;
    vPill.className = `st-pill ${allCatboxReady === totalVids && totalVids >= 2 ? 'ok' : 'warn'}`;
    document.getElementById('tabVideosBadge').textContent = `(${totalVids})`;

    const descCard = descVid ? `
      <div class="st-vid-card is-desc">
        <img class="st-vid-thumb" src="${esc(descVid.poster || '/logo.png')}" alt="" />
        <div class="st-vid-meta">
          <strong style="color:#34d399;">★ Vídeo da Descrição</strong>
          <span>${/catbox\.moe\//i.test(descVid.src) ? '☁️ Catbox Pronto ✓' : '⏳ Subindo Catbox...'}</span>
        </div>
      </div>
    ` : '';

    document.getElementById('videosGrid').innerHTML = descCard + creators.map((c, idx) => {
      const ready = /catbox\.moe\//i.test(c.video || '');
      return `
        <div class="st-vid-card">
          <img class="st-vid-thumb" src="${esc(c.poster || c.avatar || '/logo.png')}" alt="" />
          <div class="st-vid-meta">
            <strong>@${esc(c.username)}</strong>
            <span style="color:${ready ? '#34d399' : '#fbbf24'};">${ready ? '☁️ Catbox ✓' : '⏳ Subindo...'}</span>
            <div style="display:flex; gap:4px; margin-top:4px;">
              <button type="button" class="st-mini-btn" style="flex:1;" onclick="window.saveDraftPatch({ action: 'set_desc_video', index: ${idx} })">★ Desc</button>
              <button type="button" class="st-mini-btn" style="color:#f87171;" onclick="window.saveDraftPatch({ action: 'remove_creator', index: ${idx} })">✕</button>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Reviews list
    document.getElementById('reviewsTotalPill').textContent = `${reviews.length} avaliações`;
    document.getElementById('tabReviewsBadge').textContent = `(${reviews.length})`;
    document.getElementById('reviewsListHost').innerHTML = reviews.map((r, idx) => `
      <div class="st-rev-item">
        <div>
          <strong>${esc(r.name)} · ${r.stars}★ ${r.photos && r.photos.length ? `📸(${r.photos.length})` : ''}</strong>
          <div style="color:#cbd5e1; margin-top:2px;">${esc(r.comment)}</div>
        </div>
        <button type="button" class="st-mini-btn" style="color:#f87171;" onclick="window.saveDraftPatch({ action: 'remove_review', index: ${idx} })">✕</button>
      </div>
    `).join('');
  }

  window.addPresetSecondGroup = function (preset) {
    if (!currentDraft) return;
    const vars = JSON.parse(JSON.stringify(currentDraft.variations || {}));
    if (preset === 'tamanho_roupa') {
      vars.tamanho = { com_imagem: false, label: 'Tamanho', opcoes: ['P', 'M', 'G', 'GG'] };
    } else if (preset === 'numeracao_calcado') {
      vars.numeracao = { com_imagem: false, label: 'Numeração', opcoes: ['34', '35', '36', '37', '38', '39'] };
    } else if (preset === 'voltagem') {
      vars.voltagem = { com_imagem: false, label: 'Voltagem', opcoes: ['110V (127V)', '220V'] };
    }
    window.saveDraftPatch({ variations: vars });
  };

  window.removeVarGroup = function (gKey) {
    if (!currentDraft) return;
    const vars = JSON.parse(JSON.stringify(currentDraft.variations || {}));
    delete vars[gKey];
    window.saveDraftPatch({ variations: vars });
  };

  window.removeVarOption = function (gKey, oIdx) {
    if (!currentDraft) return;
    const vars = JSON.parse(JSON.stringify(currentDraft.variations || {}));
    if (vars[gKey] && Array.isArray(vars[gKey].opcoes)) {
      vars[gKey].opcoes.splice(oIdx, 1);
      window.saveDraftPatch({ variations: vars });
    }
  };

  window.promptAddVarOption = function (gKey) {
    if (!currentDraft) return;
    const name = prompt('Nome da nova opção (sem vírgulas):');
    if (!name) return;
    const vars = JSON.parse(JSON.stringify(currentDraft.variations || {}));
    if (!vars[gKey]) return;
    const withImg = vars[gKey].com_imagem;
    vars[gKey].opcoes.push(withImg ? { nome: name.trim(), imagem: (currentDraft.slides[0] && currentDraft.slides[0].src) || '/logo.png' } : name.trim());
    window.saveDraftPatch({ variations: vars });
  };

  window.submitPastedVideos = async function () {
    if (!currentDraft) return toast('Crie ou abra um rascunho primeiro!');
    const raw = document.getElementById('pasteVideoUrls').value || '';
    const urls = raw.split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
    if (!urls.length) return toast('Cole pelo menos 1 link do TikTok!');
    document.getElementById('pasteVideoUrls').value = '';
    setBanner(`🎬 Baixando ${urls.length} vídeo(s) silenciosamente via tikwm + Catbox...`);
    await api(`/api/studio/draft/${currentDraft.draftId}/videos`, 'POST', { mode: 'urls', urls });
  };

  window.submitSearchVideos = async function () {
    if (!currentDraft) return toast('Crie ou abra um rascunho primeiro!');
    const q = document.getElementById('videoSearchQuery').value.trim();
    if (!q) return toast('Digite o termo de busca!');
    setBanner(`🔍 Buscando vídeos reais no TikTok para "${q}"...`);
    await api(`/api/studio/draft/${currentDraft.draftId}/videos`, 'POST', { mode: 'search', query: q });
  };

  window.addQuickComment = function () {
    if (!currentDraft) return;
    const inp = document.getElementById('newRevComment');
    const txt = inp.value.trim();
    if (txt.length < 6) return;
    inp.value = '';
    window.saveDraftPatch({ action: 'add_custom_review', review: { comment: txt, stars: 5 } });
  };

  window.publishCurrentDraft = async function (deploy) {
    if (!currentDraft) return toast('Cole um link primeiro!');
    const btn = document.getElementById(deploy ? 'publishVercelBtn' : 'publishLocalBtn');
    const resBox = document.getElementById('publishResultBox');
    const origTxt = btn.textContent;
    btn.disabled = true;
    btn.textContent = deploy ? '⏳ Validando & Subindo na Vercel...' : '⏳ Validando...';
    resBox.style.display = 'block';
    resBox.innerHTML = '🔍 Finalizando uploads Catbox pendentes (se houver) e rodando <code>validar-modelo-unico.js</code>...';

    const res = await api(`/api/studio/publish/${currentDraft.draftId}`, 'POST', { deploy });
    btn.disabled = false;
    btn.textContent = origTxt;

    if (!res.ok || !res.data.ok) {
      const errs = (res.data.errors || ['Erro desconhecido']).map((e) => `<li>${esc(e)}</li>`).join('');
      resBox.innerHTML = `<strong style="color:#f87171;">❌ Bloqueado pelo Validador (Rollback limpo aplicado):</strong><ul style="margin:6px 0 0 16px;color:#fca5a5;">${errs}</ul>`;
      return;
    }

    resBox.innerHTML = `
      <strong style="color:#34d399;">🏆 Produto #${res.data.productId} Publicado com ZERO ERROS!</strong><br/>
      👉 <a href="${esc(res.data.liveUrl)}" target="_blank" style="color:#93c5fd;">Abrir Página na Loja (#${res.data.productId}) ↗</a><br/>
      🎬 <a href="${esc(res.data.adsUrl)}" target="_blank" style="color:#6ee7a8;">Ir para Central /videos-ads ↗</a>
    `;
    toast(`🏆 Produto #${res.data.productId} publicado!`);
    refreshStateHeader();
  };

  window.toggleExtraInputs = function () {
    const el = document.getElementById('extraInputsRow');
    el.style.display = el.style.display === 'none' ? 'flex' : 'none';
  };

  window.switchSubtab = function (name, btn) {
    document.querySelectorAll('.st-subtab').forEach((b) => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    document.querySelectorAll('.st-tab-panel').forEach((p) => p.classList.remove('active'));
    const target = document.getElementById(`panel-${name}`);
    if (target) target.classList.add('active');
  };

  window.setMobilePane = function (pane, btn) {
    document.querySelectorAll('.st-mob-btn').forEach((b) => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    const left = document.getElementById('paneCuradoria');
    const right = document.getElementById('panePreview');
    if (pane === 'preview') {
      left.classList.add('mob-hidden');
      right.classList.add('mob-active');
    } else {
      left.classList.remove('mob-hidden');
      right.classList.remove('mob-active');
    }
  };

  async function refreshStateHeader() {
    const res = await api('/api/studio/state');
    if (!res.ok) return;
    const badge = document.getElementById('daemonBadge');
    if (res.data.daemonOnline) {
      badge.textContent = res.data.browserWarm ? 'Motor Aquecido ✓' : 'Daemon Online';
    } else {
      badge.textContent = 'Daemon Offline';
      badge.style.color = '#fbbf24';
    }
    const idInp = document.getElementById('initTargetId');
    if (idInp && !idInp.value) idInp.placeholder = `#${res.data.nextId}`;

    const sel = document.getElementById('recentDraftsSelect');
    sel.innerHTML = `<option value="">Rascunhos recentes (${(res.data.drafts || []).length})...</option>` +
      (res.data.drafts || []).map((d) => `<option value="${esc(d.draftId)}">#${d.targetId} — ${esc(String(d.product_title).slice(0, 32))}</option>`).join('');
  }

  refreshStateHeader();
})();
