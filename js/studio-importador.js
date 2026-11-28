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
    try {
      const resp = await fetch(pathUrl, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
      });
      const data = await resp.json().catch(() => ({ error: `HTTP ${resp.status}` }));
      return { status: resp.status, ok: resp.ok, data };
    } catch (err) {
      return { status: 0, ok: false, data: { error: err.message || 'Falha de conexão com o Studio' } };
    }
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function toast(msg) {
    const el = document.getElementById('stToast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(window._stToastTimer);
    window._stToastTimer = setTimeout(() => el.classList.remove('show'), 2300);
  }

  const jobClock = {
    timerId: null,
    startMs: 0,
    stageStartMs: 0,
    estRemainingFromStageSec: 26,
    basePct: 0,
    ceilPct: 22,
    running: false,
  };

  function fmtSec(sec) {
    return Math.max(0, Number(sec || 0)).toFixed(1).replace('.', ',');
  }

  function stopJobClock() {
    jobClock.running = false;
    if (jobClock.timerId) {
      clearInterval(jobClock.timerId);
      jobClock.timerId = null;
    }
  }

  function tickJobClock() {
    if (!jobClock.running) return;
    const now = performance.now();
    const totalElapsed = (now - jobClock.startMs) / 1000;
    const stageElapsed = (now - jobClock.stageStartMs) / 1000;
    const timerEl = document.getElementById('statusBannerTimer');
    const fillEl = document.getElementById('statusBannerFill');

    const estRem = Math.max(1, Math.ceil(jobClock.estRemainingFromStageSec - stageElapsed));
    if (timerEl) {
      if (stageElapsed <= jobClock.estRemainingFromStageSec) {
        timerEl.textContent = `${fmtSec(totalElapsed)}s · falta ~${estRem}s`;
      } else {
        timerEl.textContent = `${fmtSec(totalElapsed)}s · finalizando`;
      }
    }

    if (fillEl) {
      const span = Math.max(0, jobClock.ceilPct - jobClock.basePct);
      const frac = Math.min(0.92, stageElapsed / Math.max(2, jobClock.estRemainingFromStageSec));
      const pct = Math.min(99, jobClock.basePct + span * frac);
      fillEl.style.width = `${pct.toFixed(1)}%`;
    }

    // Safety watchdog so banner never hangs forever if network drops
    if (totalElapsed > 75) {
      finishBannerJob('Extração concluída com os itens disponíveis.', false);
    }
  }

  function startBannerJob(msg, estTotalSec = 26, ceilPct = 24) {
    stopJobClock();
    const b = document.getElementById('statusBanner');
    const m = document.getElementById('statusBannerMsg');
    const t = document.getElementById('statusBannerTimer');
    const tr = document.getElementById('statusBannerTrack');
    const f = document.getElementById('statusBannerFill');
    if (!b) return;

    b.style.display = 'flex';
    b.className = 'st-live-banner is-running';
    if (m) m.textContent = msg;
    if (tr) tr.style.display = 'block';
    if (f) f.style.width = '4%';
    if (t) {
      t.style.display = 'inline-block';
      t.textContent = `0,0s · falta ~${Math.ceil(estTotalSec)}s`;
    }

    jobClock.startMs = performance.now();
    jobClock.stageStartMs = jobClock.startMs;
    jobClock.estRemainingFromStageSec = estTotalSec;
    jobClock.basePct = 4;
    jobClock.ceilPct = ceilPct;
    jobClock.running = true;
    jobClock.timerId = setInterval(tickJobClock, 100);
  }

  function updateBannerStage(msg, basePct, ceilPct, estRemSec) {
    const b = document.getElementById('statusBanner');
    const m = document.getElementById('statusBannerMsg');
    const tr = document.getElementById('statusBannerTrack');
    const f = document.getElementById('statusBannerFill');
    if (!b) return;

    if (!jobClock.running) {
      startBannerJob(msg, estRemSec || 18, ceilPct || 70);
      return;
    }

    b.style.display = 'flex';
    b.className = 'st-live-banner is-running';
    if (m && msg) m.textContent = msg;
    if (tr) tr.style.display = 'block';
    jobClock.stageStartMs = performance.now();
    jobClock.basePct = basePct;
    jobClock.ceilPct = Math.max(basePct + 2, ceilPct);
    jobClock.estRemainingFromStageSec = Math.max(2, estRemSec);
    if (f) f.style.width = `${basePct}%`;
    tickJobClock();
  }

  function finishBannerJob(msg, isWarn = false) {
    const elapsed = jobClock.startMs ? (performance.now() - jobClock.startMs) / 1000 : 0;
    stopJobClock();
    const b = document.getElementById('statusBanner');
    const m = document.getElementById('statusBannerMsg');
    const t = document.getElementById('statusBannerTimer');
    const tr = document.getElementById('statusBannerTrack');
    const f = document.getElementById('statusBannerFill');
    if (!b) return;

    b.style.display = 'flex';
    b.className = `st-live-banner ${isWarn ? 'is-warn' : 'is-done'}`;
    if (m) m.textContent = msg;
    if (t) {
      t.style.display = elapsed > 0.2 ? 'inline-block' : 'none';
      if (elapsed > 0.2) {
        t.textContent = isWarn ? `${fmtSec(elapsed)}s` : `Pronto em ${fmtSec(elapsed)}s ✓`;
      }
    }
    if (tr) tr.style.display = isWarn ? 'none' : 'block';
    if (f) f.style.width = '100%';
  }

  function setBanner(msg, isWarn = false) {
    const b = document.getElementById('statusBanner');
    if (!b) return;
    if (!msg) {
      stopJobClock();
      b.style.display = 'none';
      return;
    }
    if (isWarn) {
      finishBannerJob(msg, true);
      return;
    }
    const m = document.getElementById('statusBannerMsg');
    const t = document.getElementById('statusBannerTimer');
    const tr = document.getElementById('statusBannerTrack');
    b.style.display = 'flex';
    b.className = 'st-live-banner';
    if (m) m.textContent = msg;
    if (t && !jobClock.running) t.style.display = 'none';
    if (tr && !jobClock.running) tr.style.display = 'none';
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

  function updateLiveCalcBadge(pix, orig) {
    const el = document.getElementById('liveCalcBadge');
    if (!el) return;
    const p = Math.max(1, Number(pix || 49.89));
    const o = Math.max(p + 5, Number(orig || p * 3.5));
    const pct = Math.min(90, Math.max(20, Math.round((1 - p / o) * 100)));
    const v3x = (Math.floor((p / 3) * 100) / 100).toFixed(2).replace('.', ',');
    el.textContent = `-${pct}% OFF · 3x R$ ${v3x}`;
  }

  window.pasteClipboardUrl = async function () {
    try {
      const txt = await navigator.clipboard.readText();
      if (txt && txt.trim()) {
        const inp = document.getElementById('url1Input');
        inp.value = txt.trim();
        toast('Link colado');
      }
    } catch (_) {
      document.getElementById('url1Input').focus();
    }
  };

  window.onLiveFieldInput = function () {
    if (!currentDraft) return;
    const title = document.getElementById('editTitle').value;
    const pix = Math.max(1, Number(document.getElementById('editPix').value || 49.89));
    const orig = Math.max(pix + 5, Number(document.getElementById('editOrig').value || pix * 3.5));
    const sold = Math.max(10, Number(document.getElementById('editSold').value || 4820));

    updateLiveCalcBadge(pix, orig);

    const [pInt, pDec] = pix.toFixed(2).split('.');
    const pct = Math.min(90, Math.max(20, Math.round((1 - pix / orig) * 100)));
    const v3x = (Math.floor((pix / 3) * 100) / 100).toFixed(2).replace('.', ',');

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
    }, 260);
  };

  window.saveDraftPatch = async function (patch, silent = false) {
    if (!currentDraft) return;
    const res = await api(`/api/studio/draft/${currentDraft.draftId}`, 'POST', patch);
    if (res.ok && res.data.draft) {
      currentDraft = res.data.draft;
      renderDraftPanels(silent);
      if (res.data.livePatch) postLiveToPhone(res.data.livePatch);
      if (!silent) toast('Atualizado');
    }
  };

  window.popMore = async function (kind, count) {
    if (!currentDraft) return toast('Cole um link primeiro');
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
      toast(`+${res.data.added.length} adicionado(s) na hora`);
    } else {
      toast('Reserva vazia — buscando mais em segundo plano');
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
          updateBannerStage('Título e capa 1:1 prontos · Puxando galeria HD e avaliações...', 22, 58, 19);
          window.reloadPreviewIframe();
          if (window.innerWidth < 1080) window.setMobilePane('preview');
        } else if (data.event === 'status_info' && data.extra && data.extra.message) {
          updateBannerStage(data.extra.message, 38, 62, 15);
        } else if (data.event === 'reviews_pool_ready') {
          updateBannerStage('Galeria 1:1 e avaliações prontas · Buscando vídeos TikTok...', 62, 78, 12);
          window.reloadPreviewIframe();
        } else if (data.event === 'videos_preview_ready') {
          const d = currentDraft || {};
          const allVids = [...(d.video && d.video.src ? [d.video] : []), ...(d.creators || [])];
          const total = allVids.length;
          if (total > 0) {
            const estCatboxSec = Math.max(8, Math.ceil(total / 4) * 12);
            updateBannerStage(`Subindo ${total} vídeo(s) pro Catbox (0/${total} prontos)...`, 78, 98, estCatboxSec);
          } else {
            finishBannerJob('Galeria e avaliações prontas! (Cole links na aba Vídeos se desejar mais)', false);
          }
          window.reloadPreviewIframe();
        } else if (data.event === 'video_catbox_done') {
          const d = currentDraft || {};
          const allVids = [...(d.video && d.video.src ? [d.video] : []), ...(d.creators || [])];
          const ready = allVids.filter((v) => /catbox\.moe\//i.test(v.src || v.video || '')).length;
          const pending = Math.max(0, allVids.length - ready);
          if (allVids.length > 0 && ready >= allVids.length) {
            finishBannerJob(`Página 100% pronta! (${ready}/${allVids.length} vídeos no Catbox ✓)`, false);
          } else if (allVids.length > 0) {
            const pctNow = Math.round(78 + (ready / allVids.length) * 20);
            const remSec = Math.max(4, Math.ceil(pending / 4) * 11);
            updateBannerStage(`Subindo vídeos pro Catbox (${ready}/${allVids.length} prontos)...`, pctNow, 99, remSec);
          }
        } else if (data.event === 'warning' && data.extra && data.extra.message) {
          finishBannerJob(data.extra.message, true);
        }
      } catch (_) {}
    };

    ['sync_state', 'fast_preview', 'status_info', 'reviews_pool_ready', 'videos_preview_ready', 'video_catbox_done', 'warning'].forEach((evt) => {
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
    const origHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span>Lendo link...</span>';
    startBannerJob('Lendo anúncio e decodificando capa 1:1...', 26, 22);

    const res = await api('/api/studio/extract', 'POST', {
      url1,
      url2,
      price_pix: pricePix,
      gender,
      targetId,
      autoVideos: true,
    });

    btn.disabled = false;
    btn.innerHTML = origHtml;

    if (!res.ok) {
      setBanner(res.data.error || 'Erro ao iniciar extração', true);
      return;
    }

    currentDraft = res.data.draft;
    renderDraftPanels(false);
    const k = encodeURIComponent(getStudioKey());
    document.getElementById('studioPhoneIframe').src = `${res.data.previewUrl}&key=${k}`;
    if (window.innerWidth < 1080) {
      window.setMobilePane('preview');
    }
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

  function setChipState(id, text, ok) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
    el.className = `st-ready-chip ${ok ? 'ok' : 'warn'}`;
  }

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
      updateLiveCalcBadge(d.price_pix, d.price_original_num);

      const qInp = document.getElementById('videoSearchQuery');
      if (qInp && !qInp.value && d.product_title && !d.product_title.startsWith('Extraindo')) {
        qInp.value = d.product_title.split(/\s+/).slice(0, 5).join(' ');
      }
    }

    const slides = d.slides || [];
    const reviews = d.reviews || [];
    const unboxings = reviews.map((r, i) => ({ ...r, _idx: i })).filter((r) => Array.isArray(r.photos) && r.photos.length > 0);
    const creators = d.creators || [];
    const descVid = d.video && d.video.src ? d.video : null;
    const totalVids = (descVid ? 1 : 0) + creators.length;
    const catboxReadyCount = [...(descVid ? [descVid] : []), ...creators].filter((v) => /catbox\.moe\//i.test(v.src || v.video || '')).length;

    document.getElementById('kpiSlidesNum').textContent = String(slides.length);
    document.getElementById('kpiSlidesPill').textContent = slides.length >= 4 ? 'OK' : 'Mín. 4';

    document.getElementById('kpiUnboxNum').innerHTML = `${unboxings.length}<small>/6</small>`;
    document.getElementById('resUnboxCount').textContent = `${(d.reserve_unboxings || []).length} res`;

    document.getElementById('kpiVideosNum').textContent = String(totalVids);
    document.getElementById('resVideosCount').textContent = `${(d.reserve_videos || []).length} res`;
    document.getElementById('catboxStatusPill').textContent = `${catboxReadyCount}/${totalVids} Catbox`;

    document.getElementById('kpiReviewsNum').textContent = String(reviews.length);
    document.getElementById('resReviewsCount').textContent = `${(d.reserve_reviews || []).length} res`;

    setChipState('gateSlides', `Fotos ${slides.length}/4`, slides.length >= 4);
    setChipState('gateUnbox', `Unbox ${unboxings.length}/6`, unboxings.length >= 6);
    setChipState('gateReviews', `Reviews ${reviews.length}/20`, reviews.length >= 20);
    setChipState('gateCatbox', `Catbox ${catboxReadyCount}/${totalVids}`, totalVids >= 2 && catboxReadyCount === totalVids);

    document.getElementById('phonePreviewLabel').textContent = `#${d.targetId} · PIX R$ ${formatBRL(d.price_pix)}`;

    document.getElementById('tabFotosBadge').textContent = `${slides.length + unboxings.length}`;
    document.getElementById('tabVideosBadge').textContent = `${totalVids}`;
    document.getElementById('tabReviewsBadge').textContent = `${reviews.length}`;

    // Variations
    const vHost = document.getElementById('variationsHost');
    const vars = d.variations || {};
    vHost.innerHTML = Object.entries(vars).map(([gKey, grp]) => `
      <div class="st-var-group">
        <div style="display:flex; justify-content:space-between; align-items:center;">
          <strong style="font-size:13px;">${esc(grp.label || gKey)} <span style="color:#71717a;font-weight:500;">(${(grp.opcoes || []).length})</span></strong>
          ${gKey !== 'cor' ? `<button type="button" class="st-chip-action" onclick="window.removeVarGroup('${esc(gKey)}')">Remover</button>` : ''}
        </div>
        <div class="st-var-chips">
          ${(grp.opcoes || []).map((o, oIdx) => {
            const name = typeof o === 'string' ? o : o.nome;
            return `<span class="st-var-chip">${esc(name)} <button type="button" class="st-var-del" onclick="window.removeVarOption('${esc(gKey)}', ${oIdx})">✕</button></span>`;
          }).join('')}
          <button type="button" class="st-chip-action" onclick="window.promptAddVarOption('${esc(gKey)}')">+ Opção</button>
        </div>
      </div>
    `).join('');

    // Slides Grid
    const sPill = document.getElementById('slidesCounterPill');
    sPill.textContent = `${slides.length} / 4 mín`;
    sPill.className = `st-gate-pill ${slides.length >= 4 ? 'ok' : 'warn'}`;
    document.getElementById('slidesGrid').innerHTML = slides.length ? slides.map((s, idx) => `
      <div class="st-media-card">
        <img src="${esc(s.src)}" alt="" loading="lazy" />
        <div class="st-media-actions">
          <button type="button" class="st-chip-action" style="height:24px;padding:0 8px;font-size:10.5px;" onclick="window.saveDraftPatch({ action: 'promote_slide', index: ${idx} })">${idx === 0 ? 'Capa' : 'Virar Capa'}</button>
          <button type="button" class="st-var-del" onclick="window.saveDraftPatch({ action: 'remove_slide', index: ${idx} })">✕</button>
        </div>
      </div>
    `).join('') : '<div class="st-empty-state">Cole um link acima para carregar as fotos 1:1.</div>';

    // Unboxings Grid
    const uPill = document.getElementById('unboxCounterPill');
    uPill.textContent = `${unboxings.length} / 6 mín`;
    uPill.className = `st-gate-pill ${unboxings.length >= 6 ? 'ok' : 'warn'}`;
    document.getElementById('unboxGrid').innerHTML = unboxings.length ? unboxings.map((u) => `
      <div class="st-media-card">
        <img src="${esc(u.photos[0])}" alt="" loading="lazy" />
        <div class="st-media-actions">
          <span title="${esc(u.comment)}">${esc(u.name)} · ${u.photos.length}ft</span>
          <button type="button" class="st-var-del" onclick="window.saveDraftPatch({ action: 'remove_review', index: ${u._idx} })">✕</button>
        </div>
      </div>
    `).join('') : '<div class="st-empty-state">Nenhuma foto de comprador ativa ainda.</div>';

    // Videos Grid
    const descCard = descVid ? `
      <div class="st-vid-card is-desc">
        <img class="st-vid-thumb" referrerpolicy="no-referrer" src="${esc(descVid.poster || '/logo.png')}" alt="" />
        <div class="st-vid-meta">
          <strong style="color:#6ee7a8;">Vídeo Descrição</strong>
          <span style="color:#a1a1aa;">${/catbox\.moe\//i.test(descVid.src) ? 'Catbox ✓' : 'Subindo...'}</span>
        </div>
      </div>
    ` : '';

    const vidHtml = descCard + creators.map((c, idx) => {
      const ready = /catbox\.moe\//i.test(c.video || '');
      return `
        <div class="st-vid-card">
          <img class="st-vid-thumb" referrerpolicy="no-referrer" src="${esc(c.poster || c.avatar || '/logo.png')}" alt="" />
          <div class="st-vid-meta">
            <strong style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">@${esc(c.username)}</strong>
            <span style="color:${ready ? '#6ee7a8' : '#fcd34d'};">${ready ? 'Catbox ✓' : 'Subindo...'}</span>
            <div style="display:flex; gap:4px; margin-top:4px;">
              <button type="button" class="st-chip-action" style="flex:1;height:24px;padding:0 6px;font-size:10px;" onclick="window.saveDraftPatch({ action: 'set_desc_video', index: ${idx} })">Desc</button>
              <button type="button" class="st-var-del" onclick="window.saveDraftPatch({ action: 'remove_creator', index: ${idx} })">✕</button>
            </div>
          </div>
        </div>
      `;
    }).join('');
    document.getElementById('videosGrid').innerHTML = vidHtml || '<div class="st-empty-state">Cole links do TikTok ou busque acima.</div>';

    // Reviews List
    const rPill = document.getElementById('reviewsTotalPill');
    rPill.textContent = `${reviews.length} ativas`;
    rPill.className = `st-gate-pill ${reviews.length >= 20 ? 'ok' : 'warn'}`;
    document.getElementById('reviewsListHost').innerHTML = reviews.length ? reviews.map((r, idx) => `
      <div class="st-rev-item">
        <div>
          <div style="display:flex;align-items:center;gap:6px;">
            <strong style="color:#fff;">${esc(r.name)}</strong>
            <span style="color:#fcd34d;font-size:11px;">${'★'.repeat(Number(r.stars) || 5)}</span>
            ${r.photos && r.photos.length ? `<span style="font-size:10.5px;color:#6ee7a8;font-weight:700;">${r.photos.length}ft</span>` : ''}
          </div>
          <div style="color:#a1a1aa; margin-top:2px;">${esc(r.comment)}</div>
        </div>
        <button type="button" class="st-var-del" onclick="window.saveDraftPatch({ action: 'remove_review', index: ${idx} })">✕</button>
      </div>
    `).join('') : '<div class="st-empty-state">As avaliações aparecerão aqui.</div>';
  }

  window.openTabAndEdit = function (tabName) {
    if (window.innerWidth < 1080) window.setMobilePane('curadoria');
    window.switchSubtab(tabName);
  };

  window.addPresetSecondGroup = function (preset) {
    if (!currentDraft) return toast('Cole um link primeiro');
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
    const name = prompt('Nome da nova opção:');
    if (!name) return;
    const vars = JSON.parse(JSON.stringify(currentDraft.variations || {}));
    if (!vars[gKey]) return;
    const withImg = vars[gKey].com_imagem;
    vars[gKey].opcoes.push(withImg ? { nome: name.trim(), imagem: (currentDraft.slides[0] && currentDraft.slides[0].src) || '/logo.png' } : name.trim());
    window.saveDraftPatch({ variations: vars });
  };

  window.submitPastedVideos = async function () {
    if (!currentDraft) return toast('Cole o link do produto primeiro');
    const raw = document.getElementById('pasteVideoUrls').value || '';
    const urls = raw.split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
    if (!urls.length) return toast('Informe pelo menos 1 link do TikTok');
    document.getElementById('pasteVideoUrls').value = '';
    startBannerJob(`Baixando ${urls.length} vídeo(s) e subindo pro Catbox...`, Math.max(12, Math.ceil(urls.length / 4) * 14), 78);
    await api(`/api/studio/draft/${currentDraft.draftId}/videos`, 'POST', { mode: 'urls', urls });
  };

  window.submitSearchVideos = async function () {
    if (!currentDraft) return toast('Cole o link do produto primeiro');
    const q = document.getElementById('videoSearchQuery').value.trim();
    if (!q) return toast('Digite o termo de busca');
    startBannerJob(`Buscando vídeos no TikTok para "${q}"...`, 22, 65);
    await api(`/api/studio/draft/${currentDraft.draftId}/videos`, 'POST', { mode: 'search', query: q });
  };

  window.addQuickComment = function () {
    if (!currentDraft) return toast('Cole o link do produto primeiro');
    const inp = document.getElementById('newRevComment');
    const txt = inp.value.trim();
    if (txt.length < 6) return;
    inp.value = '';
    window.saveDraftPatch({ action: 'add_custom_review', review: { comment: txt, stars: 5 } });
  };

  window.publishCurrentDraft = async function (deploy) {
    if (!currentDraft) return toast('Cole um link primeiro');
    const btn = document.getElementById(deploy ? 'publishVercelBtn' : 'publishLocalBtn');
    const resBox = document.getElementById('publishResultBox');
    const origHtml = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = deploy ? '<span>Publicando...</span>' : '<span>Salvando...</span>';
    resBox.style.display = 'block';
    resBox.innerHTML = 'Validando mídias e executando <code>validar-modelo-unico.js</code>...';

    const res = await api(`/api/studio/publish/${currentDraft.draftId}`, 'POST', { deploy });
    btn.disabled = false;
    btn.innerHTML = origHtml;

    if (!res.ok || !res.data.ok) {
      const errs = (res.data.errors || ['Erro desconhecido']).map((e) => `<li>${esc(e)}</li>`).join('');
      resBox.innerHTML = `<strong style="color:#fb7185;">Falta ajustar antes de subir:</strong><ul style="margin:6px 0 0 16px;color:#fda4af;">${errs}</ul>`;
      return;
    }

    resBox.innerHTML = `
      <strong style="color:#6ee7a8;">Produto #${res.data.productId} no ar com ZERO ERROS!</strong><br/>
      <a href="${esc(res.data.liveUrl)}" target="_blank" style="color:#93c5fd;text-decoration:none;font-weight:700;">Abrir Produto #${res.data.productId} ↗</a> ·
      <a href="${esc(res.data.adsUrl)}" target="_blank" style="color:#6ee7a8;text-decoration:none;font-weight:700;">Abrir /videos-ads ↗</a>
    `;
    toast(`Produto #${res.data.productId} publicado!`);
    refreshStateHeader();
  };

  window.toggleExtraInputs = function () {
    const el = document.getElementById('extraInputsRow');
    el.style.display = el.style.display === 'none' ? 'grid' : 'none';
  };

  window.switchSubtab = function (name, segBtn, railBtn) {
    document.querySelectorAll('.st-seg-btn').forEach((b) => {
      b.classList.toggle('active', b.dataset.tab === name);
    });
    if (segBtn) segBtn.classList.add('active');

    document.querySelectorAll('.st-rail-btn[data-rail]').forEach((b) => {
      b.classList.toggle('active', b.dataset.rail === name);
    });
    if (railBtn) railBtn.classList.add('active');

    document.querySelectorAll('.st-tab-panel').forEach((p) => p.classList.remove('active'));
    const target = document.getElementById(`panel-${name}`);
    if (target) target.classList.add('active');
  };

  window.setMobilePane = function (pane) {
    const btnEdit = document.getElementById('mobBtnEdit');
    const btnPrev = document.getElementById('mobBtnPreview');
    if (btnEdit) btnEdit.classList.toggle('active', pane !== 'preview');
    if (btnPrev) btnPrev.classList.toggle('active', pane === 'preview');

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

  window.connectProfile42 = async function () {
    setBanner('Aguardando você clicar em "Permitir / Allow" no Chrome do PC (Profile 42)...');
    await api('/api/studio/connect-profile42', 'POST', {});
    let checks = 0;
    const iv = setInterval(async () => {
      checks += 1;
      const st = await api('/api/studio/state');
      if (st.ok && st.data.profile42Connected) {
        clearInterval(iv);
        refreshStateHeader();
        setBanner('Chrome Profile 42 conectado! Pode colar qualquer link agora.');
        toast('Profile 42 conectado!');
      } else if (checks >= 25) {
        clearInterval(iv);
        refreshStateHeader();
      }
    }, 2500);
  };

  async function refreshStateHeader() {
    const res = await api('/api/studio/state');
    if (!res.ok) return;
    const badgeTxt = document.getElementById('daemonBadgeText');
    const badgeWrap = document.getElementById('daemonBadge');
    if (res.data.profile42Connected) {
      badgeTxt.textContent = 'Profile 42 · OK';
      badgeWrap.style.color = '#6ee7a8';
    } else if (res.data.connectingProfile42) {
      badgeTxt.textContent = 'Clique Permitir...';
      badgeWrap.style.color = '#fcd34d';
    } else if (res.data.daemonOnline) {
      badgeTxt.textContent = 'Engatar P42';
      badgeWrap.style.color = '#fcd34d';
    } else {
      badgeTxt.textContent = 'Offline';
      badgeWrap.style.color = '#fb7185';
    }
    const idInp = document.getElementById('initTargetId');
    if (idInp && !idInp.value) idInp.placeholder = `#${res.data.nextId}`;

    const sel = document.getElementById('recentDraftsSelect');
    sel.innerHTML = `<option value="">Rascunhos (${(res.data.drafts || []).length})</option>` +
      (res.data.drafts || []).map((d) => `<option value="${esc(d.draftId)}">#${d.targetId} · ${esc(String(d.product_title).slice(0, 22))}</option>`).join('');
  }

  refreshStateHeader();
})();
