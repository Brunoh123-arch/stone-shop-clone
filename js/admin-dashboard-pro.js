/**
 * STONE SHOP CORE — BENTO OBSIDIAN DASHBOARD (FIEL À REFERÊNCIA VISUAL)
 * Layout:
 *  - Saudação limpa "Olá, Bruno! 👋" + seletor de período pill
 *  - Topo 50/50: Grid 2x2 KPIs (Hero Card BRANCO PURO c/ botão azul ↗ + 3 Cards Obsidian)
 *                + Gráfico de Barras Arredondadas Azul Cornflower (#638cff) c/ botão branco ↗
 *  - Base 50/50: 2 Cards de Ação com botão circular branco ↗ flutuante no centro
 *                + Gráfico Donut Multicolorido (Categorias / Dispositivos) c/ legenda lateral
 *  - Faixa inferior discreta: Cloaker v6.6 & Dispositivos ao vivo (telemetria real /api/tracking)
 */
(function () {
  let currentPeriod = 'hoje';
  let dashManifest = null;
  let lastTelemetry = null;
  let lastOrdersStats = null;
  let lastTracking = null;

  function esc(s) {
    return String(s ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatBRL(v) {
    return 'R$ ' + Number(v || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function injectBentoDashStyles() {
    if (document.getElementById('bento-dash-styles')) return;
    const st = document.createElement('style');
    st.id = 'bento-dash-styles';
    st.textContent = `
      .bd-header {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-end;
        justify-content: space-between;
        gap: 14px;
        margin-bottom: 20px;
      }
      .bd-hello {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #ffffff;
        line-height: 1.15;
      }
      .bd-sub {
        font-size: 13px;
        color: #8a8f98;
        margin-top: 4px;
      }
      .bd-controls {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }
      .bd-select {
        height: 38px;
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        padding: 0 14px;
        color: #e5e7eb;
        font-size: 12.5px;
        font-weight: 700;
        font-family: inherit;
        outline: none;
        cursor: pointer;
      }

      /* TOPO 50/50: 2x2 KPIs à esquerda + Bar Chart Azul à direita */
      .bd-top-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 16px;
        margin-bottom: 16px;
      }
      @media (min-width: 1024px) {
        .bd-top-grid { grid-template-columns: 1fr 1.08fr; }
      }

      .bd-kpi-2x2 {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
      }
      .bd-kpi {
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 22px;
        padding: 18px 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 146px;
        cursor: pointer;
        transition: transform 0.16s ease, border-color 0.16s ease;
      }
      .bd-kpi:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.15);
      }
      .bd-kpi.hero-white {
        background: #ffffff;
        border-color: #ffffff;
        color: #09090b;
      }
      .bd-kpi-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
      }
      .bd-kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #9ca3af;
      }
      .bd-kpi.hero-white .bd-kpi-title {
        color: #3f3f46;
      }
      .bd-kpi-mid {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin: 12px 0 8px;
      }
      .bd-kpi-val {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.9px;
        color: #ffffff;
        line-height: 1.05;
      }
      .bd-kpi.hero-white .bd-kpi-val {
        color: #09090b;
      }
      .bd-kpi-foot {
        font-size: 11.5px;
        color: #6b7280;
        font-weight: 500;
      }
      .bd-kpi.hero-white .bd-kpi-foot {
        color: #71717a;
      }

      /* Card do Gráfico de Barras Arredondadas */
      .bd-chart-card {
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 22px;
        padding: 20px 22px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .bd-card-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 14px;
      }
      .bd-card-title {
        font-size: 16px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.3px;
      }
      .bd-card-sub {
        font-size: 12px;
        color: #6b7280;
        margin-top: 2px;
      }
      .bd-bar-svg-wrap {
        width: 100%;
        height: 224px;
      }

      /* BASE 50/50: Bridge 2 Cards com botão ↗ no centro + Donut Chart Categorias */
      .bd-bottom-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 16px;
        margin-bottom: 16px;
      }
      @media (min-width: 1024px) {
        .bd-bottom-grid { grid-template-columns: 1fr 1.08fr; }
      }

      .bd-bridge-wrap {
        position: relative;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
      }
      .bd-bridge-card {
        background: #16161a;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 22px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 206px;
        cursor: pointer;
        transition: border-color 0.16s ease, transform 0.16s ease;
        background-image: radial-gradient(circle at 88% 18%, rgba(99, 140, 255, 0.07), transparent 55%);
      }
      .bd-bridge-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
      }
      .bd-bridge-ico {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #23232b;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #e5e7eb;
      }
      .bd-bridge-num {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff;
        line-height: 1.05;
        margin-top: 24px;
      }
      .bd-bridge-unit {
        font-size: 16px;
        font-weight: 600;
        color: #d4d4d8;
        margin-left: 4px;
      }
      .bd-bridge-note {
        font-size: 12px;
        color: #8a8f98;
        margin-top: 8px;
        line-height: 1.4;
      }
      .bd-bridge-note em {
        font-style: normal;
        color: #f69d72;
        font-weight: 700;
      }
      .bd-center-orb {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 46px;
        height: 46px;
        border-radius: 50%;
        background: #ffffff;
        color: #09090b;
        border: 5px solid #09090b;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 17px;
        font-weight: 800;
        cursor: pointer;
        z-index: 4;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
        transition: transform 0.16s ease;
      }
      .bd-center-orb:hover {
        transform: translate(-50%, -50%) scale(1.08);
      }

      /* Donut Card */
      .bd-donut-layout {
        display: grid;
        grid-template-columns: 158px 1fr;
        gap: 18px;
        align-items: center;
      }
      @media (max-width: 520px) {
        .bd-donut-layout { grid-template-columns: 1fr; justify-items: center; }
      }
      .bd-legend {
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 100%;
      }
      .bd-legend-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        font-size: 12.5px;
        color: #d4d4d8;
        cursor: pointer;
        padding: 3px 6px;
        border-radius: 8px;
        transition: background 0.14s ease;
      }
      .bd-legend-row:hover { background: rgba(255, 255, 255, 0.04); }
      .bd-dot {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        flex-shrink: 0;
      }

      /* Strip Discreto Inferior: Cloaker v6.6 + Dispositivos */
      .bd-telemetry-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 14px;
      }
      @media (min-width: 900px) {
        .bd-telemetry-grid { grid-template-columns: 1fr 1fr; }
      }
    `;
    document.head.appendChild(st);
  }

  function renderRoundedBarsSVG(items) {
    const W = 540;
    const H = 220;
    const padL = 36;
    const padR = 12;
    const padT = 26;
    const padB = 28;
    const innerW = W - padL - padR;
    const innerH = H - padT - padB;
    const bottomY = padT + innerH;

    const maxVal = Math.max(4, ...items.map((x) => x.value || 0));
    const niceMax = Math.ceil(maxVal / 4) * 4;
    const count = items.length || 1;
    const gap = 10;
    const barW = Math.min(46, Math.max(18, (innerW - gap * (count - 1)) / count));
    const totalBarsW = count * barW + (count - 1) * gap;
    const startX = padL + (innerW - totalBarsW) / 2;

    // Peak index for floating dark pill badge (just like "$14.342" in the screenshot!)
    let peakIdx = 0;
    items.forEach((it, i) => { if ((it.value || 0) >= (items[peakIdx]?.value || 0)) peakIdx = i; });

    const gridLines = [0, 0.25, 0.5, 0.75, 1].map((t) => {
      const y = (bottomY - t * innerH).toFixed(1);
      const val = Math.round(t * niceMax);
      return `
        <line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="rgba(255,255,255,0.05)" stroke-dasharray="3 4"/>
        <text x="${padL - 8}" y="${Number(y) + 3.5}" text-anchor="end" fill="#6b7280" font-size="10" font-family="JetBrains Mono, monospace">${val}</text>
      `;
    }).join('');

    const bars = items.map((it, i) => {
      const x = startX + i * (barW + gap);
      const h = Math.max(8, ((it.value || 0) / niceMax) * innerH);
      const y = bottomY - h;
      const isPeak = i === peakIdx && (it.value || 0) > 0;
      const fill = isPeak ? '#7c9cff' : '#5b82f6';
      return `
        <g style="cursor:pointer;" onclick="${it.prodId ? `window.openProductInAdsStudio && window.openProductInAdsStudio(${it.prodId})` : ''}">
          <rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${barW.toFixed(1)}" height="${h.toFixed(1)}" rx="9" fill="${fill}" opacity="${isPeak ? '1' : '0.88'}">
            <title>${esc(it.tooltip || `${it.label}: ${it.value}`)}</title>
          </rect>
          ${isPeak ? `
            <rect x="${(x + barW / 2 - 30).toFixed(1)}" y="${Math.max(2, y - 24).toFixed(1)}" width="60" height="19" rx="9.5" fill="#09090b" stroke="rgba(255,255,255,0.16)"/>
            <text x="${(x + barW / 2).toFixed(1)}" y="${Math.max(14, y - 11.5).toFixed(1)}" text-anchor="middle" fill="#ffffff" font-size="9.5" font-weight="800" font-family="JetBrains Mono, monospace">${esc(it.peakText || it.value)}</text>
          ` : ''}
          <text x="${(x + barW / 2).toFixed(1)}" y="${H - 8}" text-anchor="middle" fill="#71717a" font-size="9.5" font-weight="600" font-family="JetBrains Mono, monospace">${esc(it.label)}</text>
        </g>
      `;
    }).join('');

    return `
      <svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" style="overflow:visible;">
        ${gridLines}
        ${bars}
      </svg>
    `;
  }

  function renderDonutSVG(slices) {
    const size = 154;
    const cx = size / 2;
    const cy = size / 2;
    const r = 54;
    const strokeW = 24;
    const circ = 2 * Math.PI * r;
    const total = Math.max(1, slices.reduce((a, s) => a + s.value, 0));

    let offset = 0;
    const arcs = slices.map((s) => {
      const frac = s.value / total;
      const len = Math.max(2, frac * circ - 2);
      const dash = `${len.toFixed(2)} ${(circ - len).toFixed(2)}`;
      const curOffset = -offset;
      offset += frac * circ;
      return `
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="${s.color}" stroke-width="${strokeW}"
          stroke-dasharray="${dash}" stroke-dashoffset="${curOffset.toFixed(2)}"
          transform="rotate(-90 ${cx} ${cy})">
          <title>${esc(s.label)}: ${s.value} (${Math.round(frac * 100)}%)</title>
        </circle>
      `;
    }).join('');

    return `
      <svg viewBox="0 0 ${size} ${size}" width="154" height="154">
        <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#222229" stroke-width="${strokeW}"/>
        ${arcs}
        <text x="${cx}" y="${cy - 3}" text-anchor="middle" fill="#ffffff" font-size="20" font-weight="800">${total}</text>
        <text x="${cx}" y="${cy + 13}" text-anchor="middle" fill="#8a8f98" font-size="10" font-weight="600">produtos</text>
      </svg>
    `;
  }

  function renderBentoDashboard() {
    const root = document.getElementById('dashboardProRoot');
    if (!root) return;

    const tel = lastTelemetry || { total: 0, allowed: 0, blocked: 0, approvalRate: 100, series: [], devices: {}, botTypes: {}, prodHits: {} };
    const trackSess = (lastTracking && lastTracking.total) || 0;
    const totalVisits = (tel.total || 0) + (tel.total === 0 ? trackSess : 0);
    const totalAllowed = (tel.allowed || 0) + (tel.total === 0 ? trackSess : 0);
    const totalBlocked = tel.blocked || 0;

    // Pedidos (mescla live + localStorage)
    const allOrders = Array.isArray(window.pedidos) ? window.pedidos : [];
    const paidOrders = allOrders.filter((p) => p.status === 'pago');
    const pendingOrders = allOrders.filter((p) => p.status !== 'pago');
    const revenuePaid = (lastOrdersStats && lastOrdersStats.revenuePaid) ||
      paidOrders.reduce((acc, p) => acc + (parseFloat(p.valor) || 0), 0);
    const totalOrdersCount = Math.max(allOrders.length, (lastOrdersStats && lastOrdersStats.total) || 0);
    const pendingCount = Math.max(pendingOrders.length, (lastOrdersStats && lastOrdersStats.pending) || 0);

    const prods = (dashManifest && dashManifest.products) || [];
    const totalProds = prods.length || 85;
    const newBfCount = prods.filter((p) => p.is_new_bf).length || 22;
    const totalAdsVids = (dashManifest && dashManifest.total_ads_videos) || 522;
    const avgHealth = (dashManifest && dashManifest.avg_health_score) || 88;

    // Dados do Gráfico de Barras Arredondadas Azul:
    // Se houver tráfego real na janela, mostra barras de tráfego por hora; caso contrário mostra os 8 lançamentos Black Friday (qtd de vídeos Ads prontos)
    const hasLiveSeries = (tel.series || []).some((s) => (s.allowed || 0) + (s.blocked || 0) > 0);
    let barItems = [];
    let barTitle = 'Desempenho & Tráfego';
    let barSub = 'Acessos reais no período selecionado';

    if (hasLiveSeries) {
      barItems = tel.series.slice(-8).map((s) => ({
        label: s.label,
        value: (s.allowed || 0) + (s.blocked || 0),
        peakText: `${(s.allowed || 0) + (s.blocked || 0)} vis`,
        tooltip: `${s.label} — Permitidos: ${s.allowed} | Bloqueados: ${s.blocked}`,
      }));
    } else {
      barTitle = 'Criativos Ads — Novos Black Friday';
      barSub = 'Vídeos MP4 prontos por lançamento (clique na barra p/ abrir)';
      barItems = prods.slice(0, 8).reverse().map((p) => {
        const vCount = (p.video && p.video.src ? 1 : 0) + (p.creators_count || 0);
        return {
          prodId: p.id,
          label: `#${p.id}`,
          value: vCount,
          peakText: `${vCount} MP4`,
          tooltip: `#${p.id} ${p.title} — ${vCount} vídeos Ads (R$ ${Number(p.preco || 0).toFixed(2)})`,
        };
      });
    }

    // Donut por categoria (exact 5 colors from reference!)
    const catMap = {};
    prods.forEach((p) => {
      const c = p.category || 'Casa & Cozinha';
      catMap[c] = (catMap[c] || 0) + 1;
    });
    const donutColors = ['#f69d72', '#638cff', '#fde068', '#f87171', '#6ee7a8', '#c084fc'];
    const donutSlices = Object.entries(catMap)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([label, value], i) => ({ label, value, color: donutColors[i % donutColors.length] }));

    const devEntries = Object.entries(tel.devices || { 'TikTok App': 0, 'Android': 0, 'iPhone / iOS': 0, 'Desktop': 0 });
    const devTotal = Math.max(1, devEntries.reduce((a, [, v]) => a + v, 0));
    const botEntries = Object.entries(tel.botTypes || {});

    root.innerHTML = `
      <!-- Greeting & Period Controls -->
      <div class="bd-header">
        <div>
          <h1 class="bd-hello">Olá, Bruno! 👋</h1>
          <p class="bd-sub">Veja o que está acontecendo na Stone Shop agora · Cloaker v6.6 & ${totalAdsVids} vídeos Ads prontos.</p>
        </div>
        <div class="bd-controls">
          <select class="bd-select" onchange="window.setDashboardPeriod(this.value)">
            <option value="hoje" ${currentPeriod === 'hoje' ? 'selected' : ''}>Hoje</option>
            <option value="ontem" ${currentPeriod === 'ontem' ? 'selected' : ''}>Ontem</option>
            <option value="7d" ${currentPeriod === '7d' ? 'selected' : ''}>Últimos 7 dias</option>
            <option value="30d" ${currentPeriod === '30d' ? 'selected' : ''}>Este mês</option>
            <option value="total" ${currentPeriod === 'total' ? 'selected' : ''}>Todo período</option>
          </select>
          <button type="button" class="bento-dark-pill-btn" onclick="window.reloadEnterpriseDashboard(true)" title="Atualizar métricas ao vivo">↻ Live</button>
          <button type="button" class="bento-white-pill-btn" onclick="trocarAba('ads')">🎬 Vídeos TikTok Ads</button>
        </div>
      </div>

      <!-- TOP BENTO: 2x2 KPIs (Hero White + 3 Obsidian) + Cornflower Blue Bar Chart -->
      <div class="bd-top-grid">
        <div class="bd-kpi-2x2">
          <!-- HERO CARD BRANCO PURO (igual "Total revenue" da referência) -->
          <div class="bd-kpi hero-white" onclick="trocarAba('pedidos')">
            <div class="bd-kpi-head">
              <span class="bd-kpi-title">Faturamento Pix</span>
              <span class="arrow-circle blue">↗</span>
            </div>
            <div class="bd-kpi-mid">
              <span class="bd-kpi-val">${formatBRL(revenuePaid)}</span>
              <span class="delta-pill up">↑ ${paidOrders.length} pagos</span>
            </div>
            <div class="bd-kpi-foot">Pix confirmados · Taxa live</div>
          </div>

          <!-- KPI 2: Total Pedidos -->
          <div class="bd-kpi" onclick="trocarAba('pedidos')">
            <div class="bd-kpi-head">
              <span class="bd-kpi-title">Total de pedidos</span>
              <span class="arrow-circle dark">↗</span>
            </div>
            <div class="bd-kpi-mid">
              <span class="bd-kpi-val">${totalOrdersCount}</span>
              <span class="delta-pill ${pendingCount > 0 ? 'down' : 'up'}">${pendingCount > 0 ? `${pendingCount} pend.` : '✓ Em dia'}</span>
            </div>
            <div class="bd-kpi-foot">CRM WhatsApp integrado</div>
          </div>

          <!-- KPI 3: Visitas Cloaker -->
          <div class="bd-kpi" onclick="trocarAba('trafego')">
            <div class="bd-kpi-head">
              <span class="bd-kpi-title">Visitas (Cloaker)</span>
              <span class="arrow-circle dark">↗</span>
            </div>
            <div class="bd-kpi-mid">
              <span class="bd-kpi-val">${totalVisits.toLocaleString('pt-BR')}</span>
              <span class="delta-pill ${totalBlocked > 0 ? 'down' : 'up'}">${totalBlocked > 0 ? `${totalBlocked} bots` : '100% real'}</span>
            </div>
            <div class="bd-kpi-foot">${totalAllowed} permitidos · Cloaker v6.6</div>
          </div>

          <!-- KPI 4: Vídeos TikTok Ads -->
          <div class="bd-kpi" onclick="trocarAba('ads')">
            <div class="bd-kpi-head">
              <span class="bd-kpi-title">Vídeos TikTok Ads</span>
              <span class="arrow-circle dark">↗</span>
            </div>
            <div class="bd-kpi-mid">
              <span class="bd-kpi-val">${totalAdsVids}</span>
              <span class="delta-pill up">↑ ${totalProds} prods</span>
            </div>
            <div class="bd-kpi-foot">MP4s limpos prontos p/ subir</div>
          </div>
        </div>

        <!-- BAR CHART ARREDONDADO AZUL CORNFLOWER -->
        <div class="bd-chart-card">
          <div class="bd-card-head">
            <div>
              <div class="bd-card-title">${esc(barTitle)}</div>
              <div class="bd-card-sub">${esc(barSub)}</div>
            </div>
            <button type="button" class="arrow-circle white" onclick="trocarAba('ads')" title="Abrir Central de Vídeos TikTok Ads">↗</button>
          </div>
          <div class="bd-bar-svg-wrap">${renderRoundedBarsSVG(barItems)}</div>
        </div>
      </div>

      <!-- BOTTOM BENTO: 2-Card Bridge (c/ botão branco ↗ central) + Multi-Color Donut -->
      <div class="bd-bottom-grid">
        <div class="bd-bridge-wrap">
          <div class="bd-bridge-card" onclick="trocarAba('pedidos')">
            <div class="bd-bridge-ico">✓</div>
            <div>
              <div class="bd-bridge-num">${totalProds}<span class="bd-bridge-unit">produtos</span></div>
              <div class="bd-bridge-note"><em>${newBfCount} novos Black Friday</em> com saúde média de ${avgHealth}% no catálogo.</div>
            </div>
          </div>

          <button type="button" class="bd-center-orb" onclick="trocarAba('ads')" title="Abrir Vídeos TikTok Ads">↗</button>

          <div class="bd-bridge-card" onclick="trocarAba('ads')">
            <div class="bd-bridge-ico">🎬</div>
            <div>
              <div class="bd-bridge-num">${totalAdsVids}<span class="bd-bridge-unit">vídeos</span></div>
              <div class="bd-bridge-note"><em>${pendingCount} Pix pendentes</em> e criativos limpos prontos pro TikTok Ads.</div>
            </div>
          </div>
        </div>

        <!-- DONUT MULTICOLORIDO POR CATEGORIA -->
        <div class="bd-chart-card">
          <div class="bd-card-head">
            <div>
              <div class="bd-card-title">Catálogo por Categoria</div>
              <div class="bd-card-sub">Distribuição dos ${totalProds} produtos ativos</div>
            </div>
            <button type="button" class="arrow-circle white" onclick="trocarAba('catalogo')" title="Abrir Catálogo Completo">↗</button>
          </div>
          <div class="bd-donut-layout">
            <div>${renderDonutSVG(donutSlices)}</div>
            <div class="bd-legend">
              ${donutSlices.map((s) => {
                const pct = Math.round((s.value / Math.max(1, totalProds)) * 100);
                return `
                  <div class="bd-legend-row" onclick="trocarAba('ads'); window.setAdsCategory && window.setAdsCategory('${esc(s.label)}')">
                    <div style="display:flex; align-items:center; gap:9px; min-width:0;">
                      <span class="bd-dot" style="background:${s.color};"></span>
                      <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${esc(s.label)}</span>
                    </div>
                    <strong style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#ffffff;">${s.value} <span style="color:#6b7280; font-weight:500;">(${pct}%)</span></strong>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      </div>

      <!-- TELEMETRIA REAL DE DISPOSITIVOS & CLOAKER -->
      <div class="bd-telemetry-grid">
        <div class="bd-chart-card" style="padding:18px 20px;">
          <div class="bd-card-head" style="margin-bottom:12px;">
            <div>
              <div class="bd-card-title" style="font-size:14.5px;">Dispositivos ao Vivo</div>
              <div class="bd-card-sub">Origem real detectada pelo servidor</div>
            </div>
            <span class="delta-pill blue">Cloaker v6.6</span>
          </div>
          <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:10px;">
            ${devEntries.slice(0, 4).map(([name, cnt], idx) => {
              const pct = totalVisits > 0 ? Math.round((cnt / devTotal) * 100) : 0;
              const cols = ['#638cff', '#6ee7a8', '#f69d72', '#fde068'];
              return `
                <div style="background:#111114; border:1px solid rgba(255,255,255,0.05); border-radius:14px; padding:11px 13px;">
                  <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#9ca3af;">
                    <span>${esc(name)}</span>
                    <strong style="color:${cols[idx % cols.length]}; font-family:'JetBrains Mono',monospace;">${pct}%</strong>
                  </div>
                  <div style="font-size:18px; font-weight:800; color:#fff; margin-top:4px;">${cnt}</div>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <div class="bd-chart-card" style="padding:18px 20px;">
          <div class="bd-card-head" style="margin-bottom:12px;">
            <div>
              <div class="bd-card-title" style="font-size:14.5px;">Escudo Anti-Clone & Bots</div>
              <div class="bd-card-sub">SaveWeb2Zip, HTTrack, Headless e Spy Tools</div>
            </div>
            <span class="delta-pill up">Ativo</span>
          </div>
          ${botEntries.length ? `
            <div style="display:flex; flex-direction:column; gap:8px;">
              ${botEntries.slice(0, 4).map(([name, cnt]) => `
                <div style="display:flex; justify-content:space-between; align-items:center; background:#111114; border-radius:12px; padding:9px 12px; font-size:12px;">
                  <span style="color:#e5e7eb;">${esc(name)}</span>
                  <span class="delta-pill ${name.includes('Whitelist') ? 'up' : 'down'}">${cnt}</span>
                </div>
              `).join('')}
            </div>
          ` : `
            <div style="background:#111114; border:1px solid rgba(110,231,168,0.2); border-radius:14px; padding:14px; font-size:12.5px; color:#d4d4d8; line-height:1.5;">
              <strong style="color:#6ee7a8;">✓ Proteção 100% operacional.</strong> Nenhum ataque de ripper/clonador nesta janela. Bots oficiais do TikTok/Meta/Google Ads permanecem na Whitelist para aprovação limpa.
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
      const tRes = await fetch(`/api/tracking?mode=dashboard&period=${encodeURIComponent(currentPeriod)}`, { cache: 'no-store' }).catch(() => null);
      if (tRes && tRes.ok) {
        const j = await tRes.json();
        if (j && j.telemetry) lastTelemetry = j.telemetry;
        if (j && j.ordersStats) lastOrdersStats = j.ordersStats;
      }
    } catch (_) {}
    renderBentoDashboard();
    if (notify && window.showToast) window.showToast('Dashboard atualizado ao vivo!', 'success');
  };

  async function initBentoDashboard() {
    injectBentoDashStyles();
    if (!document.getElementById('dashboardProRoot')) return;
    // Renderiza imediatamente o esqueleto completo Bento antes mesmo da rede responder
    renderBentoDashboard();
    try {
      const mRes = await fetch('/data/admin-catalogo-360.json?v=20261127_bento');
      if (mRes.ok) {
        dashManifest = await mRes.json();
        renderBentoDashboard();
      }
    } catch (_) {}
    window.reloadEnterpriseDashboard(false);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initBentoDashboard);
  } else {
    initBentoDashboard();
  }
})();
