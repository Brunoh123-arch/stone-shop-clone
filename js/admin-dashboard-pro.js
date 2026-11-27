/**
 * STONE SHOP ENTERPRISE — DASHBOARD EXECUTIVO DE TRÁFEGO, CLOAKER & CONVERSÃO
 * Visual Dark Enterprise (inspirado no painel de cloaker/tráfego ao vivo):
 *  - Saudação + Data + Faixa Enterprise Shield v6.6
 *  - Filtro de Período (Hoje / Ontem / 7 dias / 30 dias / Total)
 *  - 4 KPIs coloridos (Visitas Azul / Permitidos Verde / Bloqueados Coral / Taxa Neon)
 *  - Gráfico Dual Area SVG Suave (Permitidos vs Bloqueados) com tooltip interativo
 *  - Top Produtos Quentes (Ranking com barra dourada e atalho direto pro Vídeo Ads)
 *  - Quebra por Dispositivos & Tipos de Bot Detectados pelo Cloaker v6.6
 */
(function () {
  let currentPeriod = 'hoje';
  let dashManifest = null;
  let lastTelemetry = null;
  let lastTracking = null;

  function esc(s) {
    return String(s ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function greetingPT() {
    const h = new Date().getHours();
    if (h < 6) return 'Boa madrugada';
    if (h < 12) return 'Bom dia';
    if (h < 18) return 'Boa tarde';
    return 'Boa noite';
  }

  function formattedDatePT() {
    const raw = new Date().toLocaleDateString('pt-BR', {
      weekday: 'long',
      day: '2-digit',
      month: 'long',
      year: 'numeric',
    });
    return raw.charAt(0).toUpperCase() + raw.slice(1);
  }

  function injectDashboardStyles() {
    if (document.getElementById('dash-enterprise-styles')) return;
    const st = document.createElement('style');
    st.id = 'dash-enterprise-styles';
    st.textContent = `
      .ent-greet-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 14px;
      }
      .ent-greet-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #f8fafc;
      }
      .ent-greet-date {
        font-size: 12.5px;
        color: #64748b;
        margin-top: 2px;
      }
      .ent-shield-bar {
        background: linear-gradient(90deg, #0d121d 0%, #111827 55%, #0d1320 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 13px 16px;
        margin-bottom: 14px;
        display: grid;
        grid-template-columns: 1fr;
        gap: 12px;
        align-items: center;
      }
      @media (min-width: 900px) {
        .ent-shield-bar { grid-template-columns: auto 1fr auto; gap: 20px; }
      }
      .ent-plan-box {
        display: flex;
        align-items: center;
        gap: 11px;
      }
      .ent-crown {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: rgba(245, 158, 11, 0.14);
        border: 1px solid rgba(245, 158, 11, 0.35);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
      }
      .ent-meter-row {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
      }
      .ent-meter-head {
        display: flex;
        justify-content: space-between;
        font-size: 11px;
        color: #94a3b8;
        margin-bottom: 5px;
      }
      .ent-meter-track {
        height: 5px;
        background: rgba(255, 255, 255, 0.07);
        border-radius: 999px;
        overflow: hidden;
      }
      .ent-meter-fill-gold {
        height: 100%;
        background: linear-gradient(90deg, #f59e0b, #fbbf24);
        border-radius: 999px;
      }
      .ent-meter-fill-blue {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #06b6d4);
        border-radius: 999px;
      }

      .ent-period-bar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 14px;
      }
      .ent-period-pills {
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
      }
      .ent-p-btn {
        background: #0d121c;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 13px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.16s ease;
      }
      .ent-p-btn:hover { color: #fff; border-color: rgba(255,255,255,0.2); }
      .ent-p-btn.active {
        background: #2563eb;
        border-color: #3b82f6;
        color: #fff;
        box-shadow: 0 0 18px rgba(37, 99, 235, 0.45);
      }

      /* 4 KPI Cards Enterprise idênticos à referência */
      .ent-kpi-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-bottom: 16px;
      }
      @media (min-width: 900px) {
        .ent-kpi-grid { grid-template-columns: repeat(4, 1fr); gap: 14px; }
      }
      .ent-kpi-card {
        background: #0c111b;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 16px 18px;
        display: flex;
        flex-direction: column;
        gap: 8px;
        transition: border-color 0.2s ease, transform 0.2s ease;
      }
      .ent-kpi-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
      }
      .ent-kpi-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }
      .ent-kpi-label-wrap {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12.5px;
        font-weight: 600;
        color: #94a3b8;
      }
      .ent-kpi-ico {
        width: 28px;
        height: 28px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
      }
      .ent-kpi-ico.blue { background: rgba(59, 130, 246, 0.14); color: #60a5fa; }
      .ent-kpi-ico.green { background: rgba(16, 185, 129, 0.14); color: #34d399; }
      .ent-kpi-ico.red { background: rgba(239, 68, 68, 0.14); color: #f87171; }
      .ent-kpi-ico.cyan { background: rgba(34, 197, 94, 0.14); color: #4ade80; }
      .ent-kpi-val {
        font-family: 'JetBrains Mono', 'Plus Jakarta Sans', monospace;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -1px;
        line-height: 1.1;
      }
      .ent-kpi-val.blue { color: #3b82f6; }
      .ent-kpi-val.green { color: #10b981; }
      .ent-kpi-val.red { color: #ef4444; }
      .ent-kpi-val.cyan { color: #22c55e; }
      .ent-kpi-sub {
        font-size: 11.5px;
        color: #64748b;
      }

      /* Deck Principal (70% Gráfico / 30% Top Produtos) */
      .ent-main-deck {
        display: grid;
        grid-template-columns: 1fr;
        gap: 14px;
        margin-bottom: 14px;
      }
      @media (min-width: 1024px) {
        .ent-main-deck { grid-template-columns: 1.75fr 1fr; }
      }
      .ent-box {
        background: #0c111b;
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 16px 18px;
      }
      .ent-box-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 14px;
      }
      .ent-box-title {
        font-size: 14.5px;
        font-weight: 800;
        color: #f8fafc;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .ent-chart-wrap {
        position: relative;
        width: 100%;
        height: 250px;
      }
      .ent-chart-legend {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        margin-top: 8px;
        font-size: 11.5px;
        color: #94a3b8;
        font-weight: 600;
      }
      .ent-legend-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 5px;
      }

      /* Ranking Top Produtos (estilo Top Players) */
      .ent-rank-list {
        display: flex;
        flex-direction: column;
        gap: 11px;
      }
      .ent-rank-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 10px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.04);
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .ent-rank-item:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(254, 44, 85, 0.35);
      }
      .ent-medal {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        flex-shrink: 0;
      }
      .ent-medal.m1 { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.5); }
      .ent-medal.m2 { background: rgba(148, 163, 184, 0.2); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.4); }
      .ent-medal.m3 { background: rgba(180, 83, 9, 0.22); color: #fb923c; border: 1px solid rgba(180, 83, 9, 0.45); }
      .ent-medal.mN { background: rgba(255, 255, 255, 0.06); color: #94a3b8; }
      .ent-rank-thumb {
        width: 34px;
        height: 34px;
        border-radius: 8px;
        object-fit: cover;
        background: #fff;
        flex-shrink: 0;
      }
      .ent-rank-info {
        flex: 1;
        min-width: 0;
      }
      .ent-rank-top {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        font-size: 12px;
        font-weight: 700;
        color: #f8fafc;
      }
      .ent-rank-name {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .ent-rank-bar {
        height: 4px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 999px;
        margin-top: 6px;
        overflow: hidden;
      }
      .ent-rank-fill {
        height: 100%;
        background: linear-gradient(90deg, #f59e0b, #fe2c55);
        border-radius: 999px;
      }

      /* Bottom Deck (Dispositivos + Tipos de Bot) */
      .ent-bottom-deck {
        display: grid;
        grid-template-columns: 1fr;
        gap: 14px;
      }
      @media (min-width: 900px) {
        .ent-bottom-deck { grid-template-columns: 1fr 1fr; }
      }
      .ent-stat-row {
        margin-bottom: 10px;
      }
      .ent-stat-row:last-child { margin-bottom: 0; }
      .ent-stat-head {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: 600;
        color: #cbd5e1;
        margin-bottom: 5px;
      }
      .ent-stat-track {
        height: 6px;
        background: rgba(255, 255, 255, 0.06);
        border-radius: 999px;
        overflow: hidden;
      }
    `;
    document.head.appendChild(st);
  }

  function buildSmoothPath(points, closeBottomY = null) {
    if (!points.length) return '';
    let d = `M ${points[0][0].toFixed(1)} ${points[0][1].toFixed(1)}`;
    for (let i = 0; i < points.length - 1; i++) {
      const [x0, y0] = points[i];
      const [x1, y1] = points[i + 1];
      const cx = ((x0 + x1) / 2).toFixed(1);
      d += ` C ${cx} ${y0.toFixed(1)}, ${cx} ${y1.toFixed(1)}, ${x1.toFixed(1)} ${y1.toFixed(1)}`;
    }
    if (closeBottomY !== null) {
      d += ` L ${points[points.length - 1][0].toFixed(1)} ${closeBottomY} L ${points[0][0].toFixed(1)} ${closeBottomY} Z`;
    }
    return d;
  }

  function renderAreaChartSVG(series) {
    const W = 720;
    const H = 228;
    const padL = 40;
    const padR = 16;
    const padT = 16;
    const padB = 30;
    const innerW = W - padL - padR;
    const innerH = H - padT - padB;
    const bottomY = padT + innerH;

    const maxVal = Math.max(4, ...series.map((s) => Math.max(s.allowed || 0, s.blocked || 0)));
    const niceMax = Math.ceil(maxVal / 4) * 4;
    const n = Math.max(2, series.length);

    const ptsAllowed = series.map((s, i) => [
      padL + (i / (n - 1)) * innerW,
      bottomY - ((s.allowed || 0) / niceMax) * innerH,
    ]);
    const ptsBlocked = series.map((s, i) => [
      padL + (i / (n - 1)) * innerW,
      bottomY - ((s.blocked || 0) / niceMax) * innerH,
    ]);

    const gridLines = [0, 0.25, 0.5, 0.75, 1].map((t) => {
      const y = (bottomY - t * innerH).toFixed(1);
      const val = Math.round(t * niceMax);
      return `
        <line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="rgba(255,255,255,0.06)" stroke-dasharray="3 4"/>
        <text x="${padL - 8}" y="${Number(y) + 4}" text-anchor="end" fill="#64748b" font-size="10" font-family="JetBrains Mono, monospace">${val}</text>
      `;
    }).join('');

    const xLabels = series.map((s, i) => {
      if (i % 2 !== 0 && i !== series.length - 1) return '';
      const x = (padL + (i / (n - 1)) * innerW).toFixed(1);
      return `<text x="${x}" y="${H - 8}" text-anchor="middle" fill="#64748b" font-size="10" font-family="JetBrains Mono, monospace">${esc(s.label)}</text>`;
    }).join('');

    const hoverDots = series.map((s, i) => {
      const [xa, ya] = ptsAllowed[i];
      const [xb, yb] = ptsBlocked[i];
      return `
        <circle cx="${xa.toFixed(1)}" cy="${ya.toFixed(1)}" r="3.2" fill="#10b981" stroke="#0c111b" stroke-width="1.5">
          <title>${esc(s.label)} — Permitidos: ${s.allowed} | Bloqueados: ${s.blocked}</title>
        </circle>
        ${s.blocked > 0 ? `<circle cx="${xb.toFixed(1)}" cy="${yb.toFixed(1)}" r="2.8" fill="#ef4444" stroke="#0c111b" stroke-width="1.5"><title>${esc(s.label)} — Bloqueados: ${s.blocked}</title></circle>` : ''}
      `;
    }).join('');

    return `
      <svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" preserveAspectRatio="none" style="overflow:visible;">
        <defs>
          <linearGradient id="gradAllowed" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#10b981" stop-opacity="0.42"/>
            <stop offset="100%" stop-color="#10b981" stop-opacity="0.01"/>
          </linearGradient>
          <linearGradient id="gradBlocked" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#ef4444" stop-opacity="0.34"/>
            <stop offset="100%" stop-color="#ef4444" stop-opacity="0.01"/>
          </linearGradient>
        </defs>
        ${gridLines}
        <path d="${buildSmoothPath(ptsAllowed, bottomY)}" fill="url(#gradAllowed)"/>
        <path d="${buildSmoothPath(ptsBlocked, bottomY)}" fill="url(#gradBlocked)"/>
        <path d="${buildSmoothPath(ptsAllowed)}" fill="none" stroke="#10b981" stroke-width="2.4" stroke-linecap="round"/>
        <path d="${buildSmoothPath(ptsBlocked)}" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round"/>
        ${hoverDots}
        ${xLabels}
      </svg>
    `;
  }

  function renderDashboard() {
    const root = document.getElementById('dashboardProRoot');
    if (!root) return;

    const tel = lastTelemetry || {
      total: 0, allowed: 0, blocked: 0, approvalRate: 100,
      series: Array.from({ length: 12 }, (_, i) => ({ label: `${String(i * 2).padStart(2, '0')}:00`, allowed: 0, blocked: 0 })),
      devices: { 'TikTok App': 0, 'Android': 0, 'iPhone / iOS': 0, 'Desktop': 0 },
      botTypes: {},
      prodHits: {},
    };
    const trackSess = (lastTracking && lastTracking.total) || 0;
    const totalVisits = tel.total + (tel.total === 0 ? trackSess : 0);
    const totalAllowed = tel.allowed + (tel.total === 0 ? trackSess : 0);
    const totalBlocked = tel.blocked || 0;
    const approvalRate = totalVisits > 0 ? Math.round((totalAllowed / totalVisits) * 100) : 100;

    const totalProds = (dashManifest && dashManifest.total_products) || 85;
    const totalAdsVids = (dashManifest && dashManifest.total_ads_videos) || 523;
    const avgHealth = (dashManifest && dashManifest.avg_health_score) || 88;

    // Top 5 produtos (prioriza hits reais do servidor + lançamentos quentes Black Friday)
    const allProds = (dashManifest && dashManifest.products) || [];
    const ranked = [...allProds]
      .sort((a, b) => {
        const ha = (tel.prodHits && tel.prodHits[a.id]) || 0;
        const hb = (tel.prodHits && tel.prodHits[b.id]) || 0;
        if (hb !== ha) return hb - ha;
        return b.id - a.id;
      })
      .slice(0, 5);
    const maxScore = Math.max(1, ...ranked.map((p) => ((tel.prodHits && tel.prodHits[p.id]) || 0) || (p.creators_count + 1)));

    // Dispositivos
    const devEntries = Object.entries(tel.devices || {}).filter(([k]) => k !== 'Outros / Bot' || tel.devices[k] > 0);
    const devTotal = Math.max(1, devEntries.reduce((a, [, v]) => a + v, 0));
    const devColors = {
      'TikTok App': '#fe2c55',
      'Android': '#10b981',
      'iPhone / iOS': '#3b82f6',
      'Desktop': '#a855f7',
      'Outros / Bot': '#f59e0b',
    };

    // Tipos de bot
    const botEntries = Object.entries(tel.botTypes || {});
    const botTotal = Math.max(1, botEntries.reduce((a, [, v]) => a + v, 0));

    const periodLabels = { hoje: 'Hoje', ontem: 'Ontem', '7d': '7 dias', '30d': '30 dias', total: 'Total' };

    root.innerHTML = `
      <div class="ent-greet-row">
        <div>
          <h1 class="ent-greet-title">${greetingPT()}, Bruno</h1>
          <div class="ent-greet-date">${formattedDatePT()} · Telemetria ao vivo Stone Shop + Cloaker v6.6</div>
        </div>
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
          <button type="button" class="ent-p-btn" onclick="window.reloadEnterpriseDashboard(true)" style="border-color:rgba(16,185,129,0.35); color:#34d399;">↻ Atualizar Live</button>
          <button type="button" class="ent-p-btn" onclick="trocarAba('ads')" style="background:linear-gradient(135deg,#fe2c55,#e11d48); border-color:#fe2c55; color:#fff;">🎬 Subir Vídeos TikTok Ads</button>
        </div>
      </div>

      <!-- Faixa Enterprise Shield (inspirada na barra Enterprise do painel de referência) -->
      <div class="ent-shield-bar">
        <div class="ent-plan-box">
          <div class="ent-crown">👑</div>
          <div>
            <div style="display:flex; align-items:center; gap:7px;">
              <span style="font-size:13.5px; font-weight:800; color:#f8fafc;">Stone Shield Enterprise</span>
              <span style="font-size:9.5px; font-weight:800; padding:2px 7px; border-radius:999px; background:rgba(16,185,129,0.16); color:#34d399; border:1px solid rgba(16,185,129,0.35);">ATIVO</span>
            </div>
            <div style="font-size:11px; color:#64748b; margin-top:2px;">Cloaker v6.6 · Pixel + CAPI · Catbox 1:1 Lock</div>
          </div>
        </div>

        <div class="ent-meter-row">
          <div>
            <div class="ent-meter-head">
              <span>Criativos TikTok Ads</span>
              <strong style="color:#fbbf24; font-family:'JetBrains Mono',monospace;">${totalAdsVids} MP4s (${totalProds} prods)</strong>
            </div>
            <div class="ent-meter-track"><div class="ent-meter-fill-gold" style="width:100%;"></div></div>
          </div>
          <div>
            <div class="ent-meter-head">
              <span>Saúde do Catálogo</span>
              <strong style="color:#38bdf8; font-family:'JetBrains Mono',monospace;">${avgHealth}% / 100%</strong>
            </div>
            <div class="ent-meter-track"><div class="ent-meter-fill-blue" style="width:${avgHealth}%;"></div></div>
          </div>
        </div>

        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button type="button" class="ent-p-btn" onclick="trocarAba('catalogo')">🏷️ Catálogo (${totalProds})</button>
          <button type="button" class="ent-p-btn" onclick="trocarAba('pedidos')">📦 Pedidos</button>
        </div>
      </div>

      <!-- Barra de Período -->
      <div class="ent-period-bar">
        <div class="ent-period-pills">
          <span style="font-size:12px; color:#64748b; font-weight:700; margin-right:4px;">📅 Período:</span>
          ${Object.entries(periodLabels).map(([k, lbl]) => `
            <button type="button" class="ent-p-btn ${currentPeriod === k ? 'active' : ''}" onclick="window.setDashboardPeriod('${k}')">${lbl}</button>
          `).join('')}
        </div>
        <div style="font-size:11.5px; color:#64748b;">
          ${totalVisits > 0
            ? `🟢 Capturando acessos reais do servidor (${periodLabels[currentPeriod]})`
            : `ℹ️ Servidor aguardando tráfego neste período — abra qualquer produto para testar ao vivo`}
        </div>
      </div>

      <!-- 4 KPIs Enterprise Coloridos -->
      <div class="ent-kpi-grid">
        <div class="ent-kpi-card">
          <div class="ent-kpi-top">
            <div class="ent-kpi-label-wrap"><span class="ent-kpi-ico blue">👁️</span><span>Visitas</span></div>
            <span style="font-size:10.5px; font-weight:700; color:#60a5fa; background:rgba(59,130,246,0.12); padding:2px 7px; border-radius:999px;">${periodLabels[currentPeriod]}</span>
          </div>
          <div class="ent-kpi-val blue">${totalVisits.toLocaleString('pt-BR')}</div>
          <div class="ent-kpi-sub">Total de requisições no Cloaker v6.6</div>
        </div>

        <div class="ent-kpi-card">
          <div class="ent-kpi-top">
            <div class="ent-kpi-label-wrap"><span class="ent-kpi-ico green">✅</span><span>Permitidos</span></div>
          </div>
          <div class="ent-kpi-val green">${totalAllowed.toLocaleString('pt-BR')}</div>
          <div class="ent-kpi-sub">de ${totalVisits.toLocaleString('pt-BR')} visitas · clientes reais na loja</div>
        </div>

        <div class="ent-kpi-card">
          <div class="ent-kpi-top">
            <div class="ent-kpi-label-wrap"><span class="ent-kpi-ico red">🛡️</span><span>Bloqueados</span></div>
          </div>
          <div class="ent-kpi-val red">${totalBlocked.toLocaleString('pt-BR')}</div>
          <div class="ent-kpi-sub">Bots, rippers e clonadores barrados</div>
        </div>

        <div class="ent-kpi-card">
          <div class="ent-kpi-top">
            <div class="ent-kpi-label-wrap"><span class="ent-kpi-ico cyan">⚡</span><span>Taxa de Liberação</span></div>
          </div>
          <div class="ent-kpi-val cyan">${approvalRate}%</div>
          <div class="ent-kpi-sub">Visitas válidas / total filtrado</div>
        </div>
      </div>

      <!-- Deck Principal: Gráfico Dual Area + Top Produtos -->
      <div class="ent-main-deck">
        <div class="ent-box">
          <div class="ent-box-head">
            <div class="ent-box-title">
              <span style="color:#3b82f6;">📈</span>
              <span>Desempenho — ${periodLabels[currentPeriod]}</span>
            </div>
            <button type="button" class="ent-p-btn" style="padding:4px 10px; font-size:11px;" onclick="trocarAba('trafego')">Config Cloaker →</button>
          </div>
          <div class="ent-chart-wrap">${renderAreaChartSVG(tel.series || [])}</div>
          <div class="ent-chart-legend">
            <span><span class="ent-legend-dot" style="background:#10b981;"></span>Permitidos (Clientes Reais)</span>
            <span><span class="ent-legend-dot" style="background:#ef4444;"></span>Bloqueados (Bots / Clonadores)</span>
          </div>
        </div>

        <div class="ent-box">
          <div class="ent-box-head">
            <div class="ent-box-title">
              <span>🏆</span>
              <span>Top Produtos Ads</span>
            </div>
            <button type="button" class="ent-p-btn" style="padding:4px 10px; font-size:11px; color:#ff6482;" onclick="trocarAba('ads')">Ver Vídeos →</button>
          </div>
          <div class="ent-rank-list">
            ${ranked.map((p, idx) => {
              const hits = (tel.prodHits && tel.prodHits[p.id]) || 0;
              const val = hits || (p.creators_count + 1);
              const pct = Math.max(18, Math.round((val / maxScore) * 100));
              const mCls = idx === 0 ? 'm1' : (idx === 1 ? 'm2' : (idx === 2 ? 'm3' : 'mN'));
              return `
                <div class="ent-rank-item" onclick="window.openProductInAdsStudio && window.openProductInAdsStudio(${p.id})" title="Clique para abrir os Vídeos TikTok Ads deste produto">
                  <span class="ent-medal ${mCls}">${idx + 1}</span>
                  <img src="${esc(p.img || 'logo.png')}" class="ent-rank-thumb" alt="" loading="lazy" onerror="this.src='logo.png'">
                  <div class="ent-rank-info">
                    <div class="ent-rank-top">
                      <span class="ent-rank-name">#${p.id} ${esc(p.title)}</span>
                      <span style="color:#fbbf24; font-family:'JetBrains Mono',monospace; flex-shrink:0;">R$ ${Number(p.preco || 0).toFixed(2).replace('.', ',')}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:10.5px; color:#64748b; margin-top:2px;">
                      <span>${hits > 0 ? `${hits} acessos live` : `${p.creators_count + 1} vídeos Ads`}</span>
                      <span style="color:#ff6482; font-weight:700;">🎬 Subir Ads</span>
                    </div>
                    <div class="ent-rank-bar"><div class="ent-rank-fill" style="width:${pct}%;"></div></div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      </div>

      <!-- Deck Inferior: Dispositivos & Tipos de Bot Detectados -->
      <div class="ent-bottom-deck">
        <div class="ent-box">
          <div class="ent-box-head">
            <div class="ent-box-title"><span>📱</span><span>Dispositivos</span></div>
            <span style="font-size:11px; color:#64748b;">Tráfego Real</span>
          </div>
          ${devEntries.map(([name, count]) => {
            const pct = totalVisits > 0 ? Math.round((count / devTotal) * 100) : 0;
            const col = devColors[name] || '#3b82f6';
            return `
              <div class="ent-stat-row">
                <div class="ent-stat-head">
                  <span>${esc(name)}</span>
                  <span style="font-family:'JetBrains Mono',monospace; color:${col};">${count} (${pct}%)</span>
                </div>
                <div class="ent-stat-track"><div style="width:${pct}%; height:100%; background:${col}; border-radius:999px;"></div></div>
              </div>
            `;
          }).join('')}
        </div>

        <div class="ent-box">
          <div class="ent-box-head">
            <div class="ent-box-title"><span>🤖</span><span>Tipos de Bot Detectados (Cloaker v6.6)</span></div>
            <span style="font-size:11px; color:#34d399; font-weight:700;">Blindado</span>
          </div>
          ${botEntries.length ? botEntries.sort((a, b) => b[1] - a[1]).map(([name, count]) => {
            const pct = Math.round((count / botTotal) * 100);
            const isWhite = name.includes('Whitelist');
            const col = isWhite ? '#10b981' : '#ef4444';
            return `
              <div class="ent-stat-row">
                <div class="ent-stat-head">
                  <span>${esc(name)}</span>
                  <span style="font-family:'JetBrains Mono',monospace; color:${col};">${count} (${pct}%)</span>
                </div>
                <div class="ent-stat-track"><div style="width:${pct}%; height:100%; background:${col}; border-radius:999px;"></div></div>
              </div>
            `;
          }).join('') : `
            <div style="display:flex; flex-direction:column; gap:8px; font-size:12px; color:#94a3b8;">
              <div style="padding:10px 12px; background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); border-radius:10px; color:#34d399; font-weight:700;">
                ✅ Nenhum ataque de clonador/bot registrado neste período.
              </div>
              <div style="font-size:11.5px; color:#64748b; line-height:1.5;">
                Regras ativas no servidor: <strong>SaveWeb2Zip</strong>, <strong>HTTrack</strong>, <strong>Headless/Playwright</strong>, <strong>Curl/Python</strong> e <strong>Spy Tools (AdHeart/BigSpy)</strong> redirecionados para página fake · <strong>TikTok/Meta/Google Ads Review Bots</strong> na Whitelist.
              </div>
            </div>
          `}
        </div>
      </div>
    `;
  }

  window.setDashboardPeriod = function (period) {
    currentPeriod = period;
    window.reloadEnterpriseDashboard(false);
  };

  window.reloadEnterpriseDashboard = async function (notify = false) {
    try {
      const [tRes, trRes] = await Promise.all([
        fetch(`/api/tracking?mode=dashboard&period=${encodeURIComponent(currentPeriod)}`, { cache: 'no-store' }).catch(() => null),
        fetch('/api/tracking', { cache: 'no-store' }).catch(() => null),
      ]);
      if (tRes && tRes.ok) {
        const j = await tRes.json();
        if (j && j.telemetry) lastTelemetry = j.telemetry;
      }
      if (trRes && trRes.ok) {
        lastTracking = await trRes.json();
      }
    } catch (_) {}
    renderDashboard();
    if (notify && window.showToast) window.showToast('Dashboard Enterprise atualizado!', 'success');
  };

  async function initEnterpriseDashboard() {
    injectDashboardStyles();
    if (!document.getElementById('dashboardProRoot')) return;
    try {
      const mRes = await fetch('data/admin-catalogo-360.json?v=' + Date.now());
      if (mRes.ok) dashManifest = await mRes.json();
    } catch (_) {}
    await window.reloadEnterpriseDashboard(false);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEnterpriseDashboard);
  } else {
    initEnterpriseDashboard();
  }
})();
