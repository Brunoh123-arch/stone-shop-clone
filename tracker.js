(function() {
  // TRACKER DE RETENÇÃO E ABANDONO - BRUNO CTO (STONE SHOP CLOAKER)
  try {
    const STORAGE_KEY = 'stone_tracker_session_id';
    let sessionId = sessionStorage.getItem(STORAGE_KEY);
    if (!sessionId) {
      sessionId = 'sess_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
      sessionStorage.setItem(STORAGE_KEY, sessionId);
    }

    const urlParams = new URLSearchParams(window.location.search);
    const hasTikTokClick = !!(urlParams.get('ttclid') || urlParams.get('tt_click_id') || sessionStorage.getItem('ttclid') || localStorage.getItem('ttclid'));
    const isMobile = /Android|iPhone|iPad|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    let maxScroll = 0;
    let currentStep = '1_visualizou_loja';
    let pontoAbandono = 'Abandonou no Topo (não rolou a página)';
    const startTime = Date.now();
    let lastPing = 0;

    function calcularScroll() {
      const h = document.documentElement;
      const b = document.body;
      const st = 'scrollTop';
      const sh = 'scrollHeight';
      const ch = 'clientHeight';
      const pct = Math.round(((h[st] || b[st]) / ((h[sh] || b[sh]) - h[ch])) * 100) || 0;
      const capped = Math.min(100, Math.max(0, pct));
      if (capped > maxScroll) {
        maxScroll = capped;
        atualizarPontoAbandono();
      }
    }

    function atualizarPontoAbandono() {
      if (currentStep === '6_gerou_pix') {
        pontoAbandono = 'Gerou o Pix mas não pagou';
      } else if (currentStep === '5_digitou_endereco') {
        pontoAbandono = 'Travou no Formulário de Endereço / CEP';
      } else if (currentStep === '4_abriu_carrinho') {
        pontoAbandono = 'Abriu o Carrinho e desistiu antes de preencher endereço';
      } else if (currentStep === '3_clicou_comprar') {
        pontoAbandono = 'Clicou em Comprar mas fechou antes do checkout';
      } else if (maxScroll >= 70) {
        pontoAbandono = 'Rolou até o fim da página (leu tudo) mas NÃO clicou em comprar';
      } else if (maxScroll >= 40) {
        pontoAbandono = 'Viu o Produto e Preço, mas NÃO clicou em comprar';
      } else {
        pontoAbandono = 'Abandonou no Topo (nem chegou a ver o preço direito)';
      }
    }

    function registrarEtapa(etapa, descricao) {
      currentStep = etapa;
      if (descricao) pontoAbandono = descricao;
      atualizarPontoAbandono();
      enviarDados(true);
    }

    function enviarDados(imediato) {
      const now = Date.now();
      if (!imediato && (now - lastPing < 4000)) return; // Throttling
      lastPing = now;

      const duracaoSegundos = Math.round((now - startTime) / 1000);
      atualizarPontoAbandono();

      const payload = {
        sessionId: sessionId,
        timestamp: now,
        isMobile: isMobile,
        isTikTok: hasTikTokClick,
        maxScroll: maxScroll,
        duracaoSegundos: duracaoSegundos,
        etapa: currentStep,
        pontoAbandono: pontoAbandono,
        path: window.location.pathname
      };

      const jsonStr = JSON.stringify(payload);

      if (navigator.sendBeacon) {
        const blob = new Blob([jsonStr], { type: 'application/json' });
        navigator.sendBeacon('/api/tracking', blob);
      } else {
        fetch('/api/tracking', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: jsonStr,
          keepalive: true
        }).catch(function() {});
      }
    }

    // Ouvintes de Scroll
    window.addEventListener('scroll', function() {
      calcularScroll();
      if (maxScroll >= 30 && currentStep === '1_visualizou_loja') {
        currentStep = '2_rolou_produto';
      }
    }, { passive: true });

    // Ouvinte global de cliques no funil
    document.addEventListener('click', function(e) {
      const target = e.target;
      const btn = target.closest('button, a, [role="button"], input[type="submit"]');
      if (!btn) return;

      const text = (btn.textContent || btn.value || '').toLowerCase();
      const id = (btn.id || '').toLowerCase();
      const cls = (btn.className || '').toLowerCase();

      // Clique em comprar / adicionar carrinho
      if (text.includes('comprar') || text.includes('pedido') || text.includes('carrinho') || 
          id.includes('buy') || id.includes('comprar') || cls.includes('buy') || cls.includes('comprar')) {
        registrarEtapa('3_clicou_comprar', 'Clicou em Comprar');
      }

      // Clique em Gerar Pix / Pagar
      if (text.includes('pix') || text.includes('pagar') || text.includes('finalizar') || 
          id.includes('pix') || id.includes('pagar')) {
        registrarEtapa('6_gerou_pix', 'Chegou na tela de Pagamento Pix');
      }
    }, true);

    // Ouvinte para detecção de abertura de modal/carrinho
    const observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(m) {
        if (m.type === 'attributes' && m.attributeName === 'style') {
          const el = m.target;
          const cls = typeof el.className === 'string' ? el.className : (el.getAttribute && el.getAttribute('class') || '');
          const id = typeof el.id === 'string' ? el.id : (el.getAttribute && el.getAttribute('id') || '');
          if (id.toLowerCase().includes('modal') || cls.toLowerCase().includes('modal')) {
            if (el.style.display !== 'none' && currentStep.startsWith('1_') || currentStep.startsWith('2_') || currentStep.startsWith('3_')) {
              registrarEtapa('4_abriu_carrinho', 'Abriu a Gaveta/Modal de Checkout');
            }
          }
        }
      });
    });
    const attachObserver = () => {
      const target = document.body || document.documentElement;
      if (target) {
        observer.observe(target, { attributes: true, subtree: true });
      }
    };
    if (document.body) {
      attachObserver();
    } else {
      document.addEventListener('DOMContentLoaded', attachObserver);
    }

    // Ouvinte para campos de formulário (endereço / CEP / dados)
    document.addEventListener('focusin', function(e) {
      const el = e.target;
      if (el.tagName === 'INPUT' || el.tagName === 'SELECT') {
        const name = (el.name || el.id || el.placeholder || '').toLowerCase();
        if (name.includes('cep') || name.includes('end') || name.includes('rua') || name.includes('nome') || name.includes('cpf')) {
          if (!currentStep.includes('6_')) {
            registrarEtapa('5_digitou_endereco', 'Começou a Preencher Endereço / CEP');
          }
        }
      }
    }, true);

    // Pings regulares: 4s, 10s, 25s, 60s
    setTimeout(function() { enviarDados(); }, 4000);
    setTimeout(function() { enviarDados(); }, 12000);
    setTimeout(function() { enviarDados(); }, 25000);
    setTimeout(function() { enviarDados(); }, 60000);

    // Envio garantido na saída do usuário (fechar aba ou mudar app no mobile)
    window.addEventListener('visibilitychange', function() {
      if (document.visibilityState === 'hidden') {
        enviarDados(true);
      }
    });
    window.addEventListener('pagehide', function() {
      enviarDados(true);
    });

    // Envio inicial
    calcularScroll();
    enviarDados(true);

  } catch(e) {
    console.warn('[Tracker] Erro silencioso:', e);
  }
})();
