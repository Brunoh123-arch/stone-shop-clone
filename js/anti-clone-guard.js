/**
 * Uppi Anti-Clone & Anti-Scraper Guard (Modo ZIKA Blindado - Trap Stone Whitehat)
 * Se o cara clonar ou tentar rodar fora do domínio oficial:
 * Ele cai na Loja Whitehat STONE® (Built for everyday) da foto!
 */
(function() {
  'use strict';

  var ALLOWED_HOSTS = ['stoneshopclone.vercel.app', 'localhost', '127.0.0.1'];

  // 1. Checagem de Domínio (Domain Lock: Garante que só roda no domínio oficial)
  function isAllowedHost() {
    if (window.location.protocol === 'file:') return false;
    var h = (window.location.hostname || '').toLowerCase();
    if (!h) return false;
    for (var i = 0; i < ALLOWED_HOSTS.length; i++) {
      if (h === ALLOWED_HOSTS[i] || h.endsWith('.' + ALLOWED_HOSTS[i]) || h.endsWith('.vercel.app')) {
        return true;
      }
    }
    return false; // Domínio clonado (ex: lojadoladrao.com)
  }

  // 2. Whitelist: Robôs oficiais de aprovação de anúncios (TikTok, Facebook, Google)
  function isAdPlatformBot() {
    var ua = (navigator.userAgent || '').toLowerCase();
    var adBots = ['bytespider', 'tiktok', 'bytedance', 'facebookexternalhit', 'facebot', 'googlebot', 'adsbot'];
    for (var i = 0; i < adBots.length; i++) {
      if (ua.indexOf(adBots[i]) !== -1) return true;
    }
    return false;
  }

  // 3. Detecção de Robô de Scraping / Headless NÃO AUTORIZADO
  function isBotAutomation() {
    if (isAdPlatformBot()) return false;
    try {
      if (window.location.search.indexOf('test=1') !== -1 || window.__bypass_guard) return false;
      if (navigator.webdriver) return true;
      if (window._phantom || window.__nightmare || window.callPhantom) return true;
    } catch(e) {}
    return false;
  }

  // 4. Renderizador da Armadilha: Loja Whitehat STONE (Built for everyday)
  function triggerScrambleTrap() {
    try {
      window.stop && window.stop();
    } catch(e) {}

    var stonePage = `
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
      <title>STONE® | Built for everyday — Coleção Oficial 2026</title>
      <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Playfair+Display:ital,wght@1,600&display=swap" rel="stylesheet">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: #0d0d0d; color: #121316; display: flex; justify-content: center; min-height: 100vh; }
        .app-shell { width: 100%; max-width: 480px; background: #F5F3EF; min-height: 100vh; display: flex; flex-direction: column; }
        .top-bar { background: #111215; color: #F5F3EF; font-size: 10.5px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; padding: 9px 16px; text-align: center; }
        .header { background: #F5F3EF; padding: 16px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(0,0,0,0.05); }
        .logo { font-size: 21px; font-weight: 900; letter-spacing: 2.5px; }
        .hero { position: relative; width: 100%; height: 600px; background: #222 url('https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=1000&auto=format&fit=crop') center top/cover; display: flex; flex-direction: column; justify-content: flex-end; padding: 32px 24px; color: #fff; }
        .hero::before { content: ''; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(18,19,22,0.95) 100%); }
        .hero-cnt { position: relative; z-index: 2; display: flex; flex-direction: column; gap: 10px; }
        .tag { font-size: 11px; font-weight: 700; letter-spacing: 2px; color: rgba(255,255,255,0.8); }
        .title { font-size: 50px; line-height: 0.95; font-weight: 800; letter-spacing: -1.5px; }
        .title em { font-family: 'Playfair Display', serif; font-style: italic; }
        .desc { font-size: 13.5px; color: rgba(255,255,255,0.85); line-height: 1.5; max-width: 300px; }
        .action { display: flex; justify-content: space-between; align-items: center; margin-top: 14px; }
        .cta { font-size: 12.5px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #fff; text-decoration: none; border-bottom: 1.5px solid #fff; padding-bottom: 4px; }
        .counter { font-size: 12px; font-weight: 700; letter-spacing: 2px; color: rgba(255,255,255,0.7); }
        .catalog { padding: 30px 20px; background: #F5F3EF; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px; }
        .card { display: flex; flex-direction: column; gap: 8px; }
        .thumb { width: 100%; aspect-ratio: 3/4; background: #EFECE6; border-radius: 4px; overflow: hidden; }
        .thumb img { width: 100%; height: 100%; object-fit: cover; }
        .p-name { font-size: 13px; font-weight: 700; }
        .p-price { font-size: 13.5px; font-weight: 800; }
      </style>
    </head>
    <body>
      <div class="app-shell">
        <div class="top-bar">FRETE GRÁTIS PARA COMPRAS ACIMA DE R$ 499 &rarr;</div>
        <div class="header">
          <div style="font-size: 18px;">☰</div>
          <div class="logo">STONE<sup>&reg;</sup></div>
          <div style="font-size: 18px;">👜</div>
        </div>
        <div class="hero">
          <div class="hero-cnt">
            <span class="tag">COLEÇÃO 04 &mdash; 2026</span>
            <div class="title">Built for<br><em>everyday.</em></div>
            <div class="desc">Peças essenciais, feitas para durar. Descubra a nova coleção.</div>
            <div class="action">
              <span class="cta">EXPLORAR COLEÇÃO &rarr;</span>
              <span class="counter">01 / 03</span>
            </div>
          </div>
        </div>
        <div class="catalog">
          <div style="font-size: 18px; font-weight: 800;">Destaques da Temporada</div>
          <div class="grid">
            <div class="card">
              <div class="thumb"><img src="https://images.unsplash.com/photo-1556905055-8f358a7a47b2?q=80&w=400&auto=format&fit=crop"></div>
              <div class="p-name">Moletom Essential Crewneck</div>
              <div class="p-price">R$ 489,00</div>
            </div>
            <div class="card">
              <div class="thumb"><img src="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=400&auto=format&fit=crop"></div>
              <div class="p-name">Camiseta Minimalist Oversized</div>
              <div class="p-price">R$ 229,00</div>
            </div>
          </div>
        </div>
      </div>
    </body>
    </html>
    `;

    document.open();
    document.write(stonePage);
    document.close();
  }

  // Se for robô de automação do SaveWeb2Zip/ripper
  if (isBotAutomation()) {
    triggerScrambleTrap();
    return;
  }

  // Se o cara abriu o ZIP no computador (file://) ou subiu no domínio dele
  if (!isAllowedHost()) {
    triggerScrambleTrap();
    return;
  }

  // Bloqueio de Botão Direito
  window.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    return false;
  }, true);

  // Bloqueio de Atalhos (F12, Ctrl+Shift+I, Ctrl+U, Ctrl+S)
  window.addEventListener('keydown', function(e) {
    if (e.key === 'F12') {
      e.preventDefault();
      e.stopPropagation();
      triggerScrambleTrap();
      return false;
    }
    if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.key === 'J' || e.key === 'j' || e.key === 'C' || e.key === 'c')) {
      e.preventDefault();
      e.stopPropagation();
      triggerScrambleTrap();
      return false;
    }
    if (e.ctrlKey && (e.key === 'u' || e.key === 'U')) {
      e.preventDefault();
      e.stopPropagation();
      triggerScrambleTrap();
      return false;
    }
    if (e.ctrlKey && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      e.stopPropagation();
      triggerScrambleTrap();
      return false;
    }
  }, true);

  window.addEventListener('dragstart', function(e) {
    if (e.target && e.target.nodeName === 'IMG') {
      e.preventDefault();
    }
  }, true);

})();
