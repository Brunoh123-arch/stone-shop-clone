const fs = require('fs');
const path = require('path');

const adminPath = path.join(__dirname, 'admin.html');
let html = fs.readFileSync(adminPath, 'utf8');

// 1. Adicionar o botão da aba na navegação
const tabNavTarget = `<button class="tab-btn" onclick="trocarAba('pedidos', this)">`;
const newTabBtn = `    <button class="tab-btn" onclick="trocarAba('retencao', this); carregarDadosRetencao();">
      <span>🔥</span> Onde Param (Drop-Off) <span class="tab-counter" id="trackerCountBadge" style="background:#ff3b30; color:#fff;">LIVE</span>
    </button>
    <button class="tab-btn" onclick="trocarAba('pedidos', this)">`;

if (!html.includes("trocarAba('retencao'")) {
  html = html.replace(tabNavTarget, newTabBtn);
  console.log('Tab button added');
}

// 2. Adicionar o HTML da seção de retenção antes de </main>
const mainCloseTarget = `  </main>`;
const retencaoSectionHTML = `    <!-- ABA: ONDE PARAM (DROP-OFF & RETENÇÃO) -->
    <section id="tab-retencao" class="tab-content">
      <div class="card-box" style="border-color: rgba(255,59,48,0.3); box-shadow: 0 0 30px rgba(255,59,48,0.08);">
        <div class="card-box-header">
          <div>
            <div class="card-box-title" style="font-size: 18px; color: #ff5252;">
              <span>🔥</span> Raio-X de Abandono & Onde o Cliente Para (Drop-Off)
            </div>
            <div class="card-box-sub">
              Telemetria em tempo real das sessões do TikTok Ads: profundidade de scroll, gargalos e momento exato da desistência.
            </div>
          </div>
          <div class="filter-actions">
            <button class="btn-action" onclick="carregarDadosRetencao()">↻ Atualizar Telemetria</button>
            <button class="btn-action danger" onclick="resetarDadosRetencao()">🗑️ Resetar Histórico</button>
          </div>
        </div>

        <!-- KPIS DO TRACKER -->
        <div class="grid-kpis" style="margin-bottom: 24px;">
          <div class="kpi-card" style="border-left: 4px solid var(--blue);">
            <div class="kpi-title">Visitantes Rastreados</div>
            <div class="kpi-val" id="retencaoTotalVisitas">0</div>
            <div class="kpi-sub"><span id="retencaoTikTokVisitas" style="color:#00e5ff; font-weight:700;">0</span> vieram do TikTok Ads</div>
          </div>
          <div class="kpi-card" style="border-left: 4px solid #ff9100;">
            <div class="kpi-title">Rolagem Média (% Scroll)</div>
            <div class="kpi-val" id="retencaoScrollMedio" style="color: #ff9100;">0%</div>
            <div class="kpi-sub">Profundidade média na página</div>
          </div>
          <div class="kpi-card" style="border-left: 4px solid #00e676;">
            <div class="kpi-title">Tempo Médio na Loja</div>
            <div class="kpi-val" id="retencaoTempoMedio" style="color: #00e676;">0s</div>
            <div class="kpi-sub">Tempo antes de sair ou fechar</div>
          </div>
          <div class="kpi-card" style="border-left: 4px solid var(--red);">
            <div class="kpi-title">Abandono Pré-Checkout</div>
            <div class="kpi-val" id="retencaoAbandonoPct" style="color: var(--red);">0%</div>
            <div class="kpi-sub">Entraram mas nem clicaram em comprar</div>
          </div>
        </div>

        <!-- DIAGNÓSTICO INTELIGENTE (BRUNO CTO) -->
        <div id="diagnosticoBox" style="background: rgba(255,59,48,0.08); border: 1.5px solid rgba(255,59,48,0.3); border-radius: 14px; padding: 18px 20px; margin-bottom: 26px;">
          <div style="font-size: 13px; font-weight: 800; color: #ff5252; text-transform: uppercase; margin-bottom: 6px; display: flex; align-items: center; gap: 8px;">
            <span>⚡</span> Diagnóstico de Tráfego do Bruno CTO:
          </div>
          <div id="diagnosticoTexto" style="font-size: 13.5px; color: #f0f2ff; line-height: 1.6;">
            Aguardando primeiras visitas com o novo tracker ativo para gerar o diagnóstico...
          </div>
        </div>

        <!-- BARRAS DE FUNIL DE RETENÇÃO -->
        <div class="card-box" style="background: #0f111b; border-color: #232738; margin-bottom: 26px;">
          <div class="card-box-title" style="margin-bottom: 16px;">
            <span>📊</span> Funil de Conversão & Fricção por Etapa:
          </div>
          
          <div style="display: flex; flex-direction: column; gap: 14px;" id="funilBarrasContainer">
            <!-- Renderizado via JS -->
          </div>
        </div>

        <!-- TABELA DE SESSÕES EM TEMPO REAL -->
        <div>
          <div style="font-size: 14px; font-weight: 800; color: #fff; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
            <span>Últimas Sessões Gravadas (Onde cada cliente parou):</span>
            <span style="font-size: 11px; color: var(--text-muted);">Atualização Instantânea</span>
          </div>

          <div style="overflow-x: auto; border: 1px solid var(--border); border-radius: 14px;">
            <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: left;">
              <thead>
                <tr style="background: #121522; color: var(--text-muted); text-transform: uppercase; font-size: 10.5px; letter-spacing: 0.5px;">
                  <th style="padding: 12px 14px;">Horário</th>
                  <th style="padding: 12px 14px;">Origem</th>
                  <th style="padding: 12px 14px;">Dispositivo</th>
                  <th style="padding: 12px 14px;">Scroll Máximo</th>
                  <th style="padding: 12px 14px;">Tempo na Loja</th>
                  <th style="padding: 12px 14px;">Onde Parou (Ponto de Abandono)</th>
                </tr>
              </thead>
              <tbody id="tabelaRetencaoCorpo">
                <tr>
                  <td colspan="6" style="padding: 24px; text-align: center; color: var(--text-muted);">
                    Nenhuma sessão gravada ainda. Abra o site ou rode anúncios para ver os dados caírem aqui!
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </section>

  </main>`;

if (!html.includes('id="tab-retencao"')) {
  html = html.replace(mainCloseTarget, retencaoSectionHTML);
  console.log('Retencao section added');
}

// 3. Adicionar Funções JavaScript no Script
const scriptInitTarget = `    function initAdmin() {
      carregarStatusCloaker();
      carregarPedidos();
      carregarCatalogo();
      carregarConfigPixel();
    }`;

const newScriptInit = `    function initAdmin() {
      carregarStatusCloaker();
      carregarPedidos();
      carregarCatalogo();
      carregarConfigPixel();
      carregarDadosRetencao();
    }

    // ==========================================
    // TELEMETRIA DE RETENÇÃO & DROP-OFF (BRUNO CTO)
    // ==========================================
    function carregarDadosRetencao() {
      fetch('/api/tracking?t=' + Date.now())
        .then(r => r.json())
        .then(data => renderizarTelemetria(data))
        .catch(err => {
          console.warn('[Tracking] Erro ao carregar:', err);
        });
    }

    function renderizarTelemetria(data) {
      if (!data) return;
      const total = data.total || 0;
      document.getElementById('retencaoTotalVisitas').textContent = total;
      document.getElementById('retencaoTikTokVisitas').textContent = data.tiktok_total || 0;
      document.getElementById('retencaoScrollMedio').textContent = (data.scroll_medio || 0) + '%';
      document.getElementById('retencaoTempoMedio').textContent = (data.tempo_medio || 0) + 's';

      const funil = data.funil || {};
      const vLoja = funil.visualizou_loja || total;
      const vProd = funil.rolou_produto || 0;
      const vComp = funil.clicou_comprar || 0;
      const vCarr = funil.abriu_carrinho || 0;
      const vEnd = funil.digitou_endereco || 0;
      const vPix = funil.gerou_pix || 0;

      // Taxa de abandono pré-compra
      const abandonoPct = total > 0 ? Math.round(((total - vComp) / total) * 100) : 0;
      document.getElementById('retencaoAbandonoPct').textContent = abandonoPct + '%';

      // Diagnóstico inteligente
      const diagEl = document.getElementById('diagnosticoTexto');
      if (total === 0) {
        diagEl.textContent = 'Aguardando tráfego cair no site para auditar o comportamento dos clientes.';
      } else if (abandonoPct >= 80 && (data.scroll_medio || 0) < 35) {
        diagEl.innerHTML = '<strong style=\"color:#ff5252;\">🚨 ATENÇÃO BRUTAL:</strong> ' + abandonoPct + '% das pessoas estão abandonando logo no topo da página (scroll médio abaixo de 35%). Isso indica que a promessa do anúncio no TikTok não combina com a primeira dobra da loja, ou o carregamento causou rejeição.';
      } else if (abandonoPct >= 70 && vProd > 0 && vComp === 0) {
        diagEl.innerHTML = '<strong style=\"color:#ff9100;\">⚠️ GARGALO NO PREÇO/OFERTA:</strong> Os visitantes estão rolando e lendo sobre o produto, mas ' + abandonoPct + '% saem SEM clicar em comprar. Teste diminuir o preço ou reforçar o botão de compra na primeira dobra.';
      } else if (vComp > 0 && vEnd === 0) {
        diagEl.innerHTML = '<strong style=\"color:#ffd600;\">⚠️ TRAVA NO CARRINHO:</strong> Os clientes clicaram em comprar, mas travaram antes de preencher o endereço. Verifique se o modal de checkout abriu perfeitamente no celular.';
      } else if (vEnd > 0 && vPix === 0) {
        diagEl.innerHTML = '<strong style=\"color:#00e5ff;\">⚠️ TRAVA NO FORMULÁRIO DE ENVIO:</strong> Os clientes digitaram dados, mas não clicaram em Gerar Pix. O formulário pode estar pedindo dados demais ou frete assustou.';
      } else {
        diagEl.innerHTML = '<strong style=\"color:#00e676;\">✓ FUNIL FLUINDO:</strong> Visitantes navegando e avançando pelas etapas do site.';
      }

      // Renderizar Barras do Funil
      const pct = (n) => total > 0 ? Math.round((n / total) * 100) : 0;
      const containerBarras = document.getElementById('funilBarrasContainer');
      const etapas = [
        { label: '1. Entraram na Loja', count: vLoja, p: 100, color: '#00b0ff' },
        { label: '2. Rolaram até o Produto / Preço', count: vProd, p: pct(vProd), color: '#7c4dff' },
        { label: '3. Clicaram em Comprar / Fazer Pedido', count: vComp, p: pct(vComp), color: '#00e676' },
        { label: '4. Abriram o Carrinho / Modal', count: vCarr, p: pct(vCarr), color: '#ffd600' },
        { label: '5. Preencheram Endereço / CEP', count: vEnd, p: pct(vEnd), color: '#ff9100' },
        { label: '6. Chegaram na Tela do Pix', count: vPix, p: pct(vPix), color: '#ff3b30' }
      ];

      containerBarras.innerHTML = etapas.map(e => \`
        <div>
          <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700; margin-bottom:5px;">
            <span>\${e.label}</span>
            <span>\${e.count} (\${e.p}%)</span>
          </div>
          <div style="background:#1b1f30; border-radius:8px; height:12px; overflow:hidden;">
            <div style="background:\${e.color}; width:\${e.p}%; height:100%; border-radius:8px; transition:width 0.4s ease;"></div>
          </div>
        </div>
      \`).join('');

      // Renderizar Tabela de Sessões
      const tbody = document.getElementById('tabelaRetencaoCorpo');
      const sessoes = data.sessoes || [];
      if (sessoes.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="padding:24px; text-align:center; color:var(--text-muted);">Nenhuma sessão gravada ainda.</td></tr>';
      } else {
        tbody.innerHTML = sessoes.map(s => \`
          <tr style="border-top: 1px solid #1a1e2f;">
            <td style="padding:10px 14px; font-family:monospace; color:#a1a8c7;">\${s.horaFormatada || '--'}</td>
            <td style="padding:10px 14px;">
              \${s.isTikTok ? '<span style="background:rgba(0,229,255,0.15); color:#00e5ff; padding:2px 8px; border-radius:6px; font-weight:700; font-size:11px;">🎯 TikTok Ads</span>' : '<span style="color:#646a85;">🌐 Direto</span>'}
            </td>
            <td style="padding:10px 14px;">\${s.isMobile ? '📱 Mobile' : '💻 Desktop'}</td>
            <td style="padding:10px 14px; font-weight:700; color:\${s.maxScroll >= 60 ? '#00e676' : (s.maxScroll >= 30 ? '#ff9100' : '#ff5252')};">
              \${s.maxScroll}%
            </td>
            <td style="padding:10px 14px; color:#fff;">\${s.duracaoSegundos}s</td>
            <td style="padding:10px 14px; font-weight:600; color:#e0e3f5;">\${s.pontoAbandono || '--'}</td>
          </tr>
        \`).join('');
      }
    }

    function resetarDadosRetencao() {
      if (!confirm('Deseja realmente limpar todo o histórico de sessões gravadas?')) return;
      fetch('/api/tracking', { method: 'DELETE' })
        .then(() => {
          toast('Histórico de telemetria resetado!');
          carregarDadosRetencao();
        });
    }`;

if (!html.includes('carregarDadosRetencao')) {
  html = html.replace(scriptInitTarget, newScriptInit);
  console.log('Script functions added');
}

fs.writeFileSync(adminPath, html, 'utf8');
console.log('admin.html successfully updated with Drop-Off analytics!');
