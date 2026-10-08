// =======================================================================
// TIKTOK PIXEL â€” Navegador
// -----------------------------------------------------------------------
// Funil (nomes PADRAO do TikTok â€” evento fora desta lista entra como
// "custom" e nao alimenta otimizacao de conversao):
//   ViewContent -> AddToCart -> InitiateCheckout -> PlaceAnOrder -> CompletePayment
//
// Todo evento de fundo de funil leva event_id no TERCEIRO argumento de
// ttq.track(). E assim que o TikTok casa o evento do navegador com o mesmo
// evento vindo da CAPI e conta UMA conversao em vez de duas.
// (event_id dentro de properties, como estava antes, e ignorado.)
// =======================================================================
(function () {
  const PIXEL_ID = 'DB39LOJC77U3NUAQ99L0';

  // ---------------------------------------------------------------
  // Inicializacao com trava anti-duplicata.
  // Varias paginas ja trazem o snippet inline no <head>; sem esta trava
  // o app.js carregava o pixel de novo e disparava um segundo PageView.
  // ---------------------------------------------------------------
  function pixelJaCarregado() {
    return !!(window.ttq && window.ttq._i && window.ttq._i[PIXEL_ID]);
  }

  try {
    if (!pixelJaCarregado()) {
      !function (w, d, t) {
        w.TiktokAnalyticsObject = t;
        var ttq = w[t] = w[t] || [];
        ttq.methods = ['page','track','identify','instances','debug','on','off','once','ready','alias','group','enableCookie','disableCookie','holdConsent','revokeConsent','grantConsent'];
        ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; };
        for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
        ttq.instance = function (t) {
          for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]);
          return e;
        };
        ttq.load = function (e, n) {
          var r = 'https://analytics.tiktok.com/i18n/pixel/events.js';
          ttq._i = ttq._i || {};
          ttq._i[e] = [];
          ttq._i[e]._u = r;
          ttq._t = ttq._t || {};
          ttq._t[e] = +new Date();
          ttq._o = ttq._o || {};
          ttq._o[e] = n || {};
          var s = d.createElement('script');
          s.type = 'text/javascript';
          s.async = true;
          s.src = r + '?sdkid=' + e + '&lib=' + t;
          var a = d.getElementsByTagName('script')[0];
          a.parentNode.insertBefore(s, a);
        };
        ttq.load(PIXEL_ID);
        ttq.page();
      }(window, document, 'ttq');
      console.log('[TikTok Pixel] Inicializado:', PIXEL_ID);
    } else {
      console.log('[TikTok Pixel] Ja carregado pelo snippet da pagina â€” nao recarregando (evita PageView duplicado).');
    }
  } catch (err) {
    console.error('[TikTok Pixel] Erro na inicializacao:', err);
  }

  // ---------------------------------------------------------------
  // Identificadores de atribuicao
  // ---------------------------------------------------------------

  // ttclid e UTMs: vêm na URL do anúncio. Guardados para sobreviver à navegação.
  try {
    const urlP = new URLSearchParams(window.location.search);
    const ttclid = urlP.get('ttclid') || urlP.get('tt_click_id');
    if (ttclid) {
      sessionStorage.setItem('ttclid', ttclid);
      localStorage.setItem('ttclid', ttclid);
      console.log('[TikTok Pixel] ttclid capturado:', ttclid);
    }
    
    // Captura UTMs para sobreviver a navegação (carrinho.html -> resumo.html não tem params na URL)
    const paramsToSave = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'src', 'fbp', 'fbc'];
    paramsToSave.forEach(function(p) {
      const v = urlP.get(p);
      if (v) sessionStorage.setItem(p, v);
    });
  } catch (e) { /* silencioso */ }

  // _ttp: cookie que o proprio pixel grava. E o segundo identificador de
  // match do TikTok e antes nao era lido em lugar nenhum do projeto.
  function getTtp() {
    try {
      const m = document.cookie.match(/(?:^|;\s*)_ttp=([^;]+)/);
      return m ? decodeURIComponent(m[1]) : '';
    } catch (e) { return ''; }
  }

  window.ttqGetTtclid = function () {
    try {
      return sessionStorage.getItem('ttclid') || localStorage.getItem('ttclid') || '';
    } catch (e) { return ''; }
  };
  window.ttqGetTtp = getTtp;

  // Dados de atribuicao para mandar junto no /api/create-pix.
  window.ttqTrackingPayload = function () {
    return { ttclid: window.ttqGetTtclid(), ttp: getTtp() };
  };

  // ---------------------------------------------------------------
  // Disparo base
  // ---------------------------------------------------------------
  function identifyUser() {
    try {
      if (!window.ttq || typeof window.ttq.identify !== 'function') return;
      const email = localStorage.getItem('user_email') || '';
      const phone = localStorage.getItem('user_tel') || '';
      if (email || phone) {
        let params = {};
        if (email) params.email = email.trim().toLowerCase();
        if (phone) {
          let p = phone.replace(/\D/g, '');
          if (p && p.length <= 11) p = '+55' + p;
          else if (p) p = '+' + p;
          params.phone_number = p;
        }
        window.ttq.identify(params);
      }
    } catch (e) { /* silencioso */ }
  }

  function track(evento, props, eventId) {
    try {
      if (!window.ttq || typeof window.ttq.track !== 'function') return;
      // Injeta email e telefone para Advanced Matching aumentar o match rate
      identifyUser();

      // 3o argumento = { event_id }. Esta e a assinatura que o TikTok usa
      // para deduplicar contra a CAPI.
      if (eventId) {
        window.ttq.track(evento, props, { event_id: String(eventId) });
      } else {
        window.ttq.track(evento, props);
      }
      console.log('[TikTok Pixel] ' + evento + ' disparado.', props, eventId ? '| event_id: ' + eventId : '');
    } catch (e) {
      console.error('[TikTok Pixel] Erro ao disparar ' + evento + ':', e);
    }
  }

  function contents(lista) {
    return (lista || []).map(function (i) {
      return {
        content_id: String(i.id != null ? i.id : (i.content_id || '')),
        content_type: 'product',
        content_name: i.nome || i.content_name || '',
        price: parseFloat(i.preco != null ? i.preco : i.price) || 0,
        quantity: parseInt(i.qty || i.quantity, 10) || 1
      };
    });
  }

  // ---------------------------------------------------------------
  // Eventos do funil
  // ---------------------------------------------------------------

  window.ttqViewContent = function (produto) {
    if (!produto) return;
    track('ViewContent', {
      value: parseFloat(produto.preco) || 0,
      currency: 'BRL',
      content_type: 'product',
      contents: contents([produto])
    });
  };

  window.ttqAddToCart = function (produto, qty) {
    if (!produto) return;
    const q = parseInt(qty, 10) || 1;
    track('AddToCart', {
      value: (parseFloat(produto.preco) || 0) * q,
      currency: 'BRL',
      content_type: 'product',
      contents: contents([Object.assign({}, produto, { qty: q })])
    });
  };

  window.ttqInitiateCheckout = function (valor, itens) {
    track('InitiateCheckout', {
      value: parseFloat(valor) || 0,
      currency: 'BRL',
      content_type: 'product',
      contents: contents(itens || [])
    });
  };

  // PIX gerado / pedido feito, pagamento ainda pendente.
  // Espelha o sendPlaceAnOrder do servidor com o mesmo event_id.
  window.ttqPlaceAnOrder = function (valor, transaction_id, itens) {
    track('PlaceAnOrder', {
      value: parseFloat(valor) || 0,
      currency: 'BRL',
      content_type: 'product',
      contents: contents(itens || [])
    }, 'order_' + (transaction_id || Date.now()));
  };

  // PIX pago. Espelha o sendCompletePayment do servidor (webhook/polling).
  window.ttqCompletePayment = function (valor, transaction_id, itens) {
    track('CompletePayment', {
      value: parseFloat(valor) || 0,
      currency: 'BRL',
      content_type: 'product',
      contents: contents(itens || [])
    }, 'purchase_' + (transaction_id || Date.now()));
  };

  // ---------------------------------------------------------------
  // Ganchos automaticos
  // ---------------------------------------------------------------

  // AddToCart: envolve a funcao global addToCart, entao vale para todos os
  // botoes de compra do site sem tocar em nenhuma pagina.
  // Roda no DOMContentLoaded porque este arquivo carrega no <head>, antes do app.js.
  function hookAddToCart() {
    try {
      if (typeof window.addToCart === 'function' && !window.addToCart.__ttqHooked) {
        const originalAdd = window.addToCart;
        const wrapped = function (produto, qty) {
          const r = originalAdd.apply(this, arguments);
          try { window.ttqAddToCart(produto, qty); } catch (e) {}
          return r;
        };
        wrapped.__ttqHooked = true;
        window.addToCart = wrapped;
      }
    } catch (e) { /* silencioso */ }
  }

  // ViewContent: PRODUTO_ATUAL so existe depois que o script inline da pagina
  // de produto roda, entao le no DOMContentLoaded.
  document.addEventListener('DOMContentLoaded', function () {
    hookAddToCart();
    try {
      if (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL && PRODUTO_ATUAL.id) {
        window.ttqViewContent(PRODUTO_ATUAL);
      }
    } catch (e) { /* silencioso */ }
  });

})();
