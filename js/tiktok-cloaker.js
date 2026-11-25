/**
 * TikTok Ad Cloaker v6.5 Ultra-Shield
 * Proteção Anti-Clonagem & Anti-Espionagem de Nível Avançado
 * 
 * 1. Anti-FOUC: Oculta a página imediatamente até validação (0 visualização para invasores).
 * 2. Bloqueio de Robôs, IAs, Scrapers e Headless Browsers (Puppeteer, Selenium, Playwright).
 * 3. Bloqueio de Computador/PC/Notebook nativo.
 * 4. Bloqueio de Emulador de Celular no PC:
 *    - Platform spoofing (Win32, MacIntel, Linux x86_64)
 *    - Desktop GPU disfarçada (NVIDIA, AMD, Intel, Direct3D)
 *    - Fake iPhone Battery API trap (iPhone real NÃO tem Battery API, Chrome Desktop tem)
 *    - Desktop PDF plugins em celular
 * 5. Validação de Sensores Físicos Mobile (Orientation / Touch).
 * 6. Bloqueio de Inspetores Mobile (Eruda, vConsole).
 * 7. Validação de Anúncio TikTok real (ttclid com hash longo ou TikTok In-App WebView).
 * 8. Suporte a sessão contínua para compras reais no celular.
 * 9. Bypass para o Dono testar no PC via ?preview=1 ou ?owner=1 ou localhost.
 */
(function () {
  'use strict';

  try {
    var search = window.location.search || '';
    var params = new URLSearchParams(search);
    var ua = navigator.userAgent || '';
    var pathname = window.location.pathname || '';

    // Se já estiver na página da Loja Whitehat, garante exibição e encerra
    if (pathname.indexOf('loja') !== -1 || pathname.indexOf('safe') !== -1) {
      if (document.documentElement) document.documentElement.style.visibility = '';
      return;
    }

    // 0. Anti-FOUC: Oculta o documento antes de qualquer renderização
    if (document.documentElement) {
      document.documentElement.style.visibility = 'hidden';
    }

    // BYPASS EXCLUSIVO DO DONO DA LOJA (para visualizar no PC e fazer manutenções)
    var isOwner = params.get('preview') === '1' || 
                  params.get('c') === '1' || 
                  params.get('owner') === '1' ||
                  window.location.hostname === 'localhost' || 
                  window.location.hostname === '127.0.0.1';

    if (isOwner) {
      sessionStorage.setItem('is_ad_traffic', 'true');
      if (document.documentElement) document.documentElement.style.visibility = '';
      return; // Acesso liberado para o dono
    }

    function redirectToWhitehat() {
      window.location.replace('/loja' + search);
    }

    // 1. BLOQUEIO DE ROBÔS, SCRAPERS, HEADLESS BROWSERS E IAs
    var isHeadless = navigator.webdriver === true || 
                     window.document.documentElement.getAttribute('webdriver') !== null ||
                     Boolean(window.callPhantom || window._phantom || window.__nightmare);

    var isBotOrSpy = isHeadless || /bot|crawl|spider|slurp|facebookexternalhit|Facebot|Twitterbot|LinkedInBot|Bytespider|TikTokBot|Semrush|Ahrefs|AdHeart|SpyHorus|Puppeteer|Playwright|Selenium|PhantomJS|Wget|Python|Scrapy/i.test(ua);

    if (isBotOrSpy) {
      redirectToWhitehat();
      return;
    }

    // 2. BLOQUEIO DE INSPETORES MOBILE (Eruda, vConsole)
    if (window.eruda || window.__vConsole || window.vConsole || window._chii) {
      redirectToWhitehat();
      return;
    }

    // 3. BLOQUEIO NATIVO DE COMPUTADORES / DESKTOPS
    var isMobileUA = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile/i.test(ua);
    var isDesktopOS = /Windows NT|Macintosh|Mac OS X|Linux x86_64|CrOS/i.test(ua) && !/Android|iPhone|iPad/i.test(ua);
    var isLargeScreen = window.innerWidth > 992 && window.screen.width > 992;
    var hasTouch = navigator.maxTouchPoints > 0 || 'ontouchstart' in window;

    if (!isMobileUA || isDesktopOS || isLargeScreen || !hasTouch) {
      redirectToWhitehat();
      return;
    }

    // 4. DETECÇÃO DE EMULADOR DE CELULAR NO PC (Chrome DevTools Device Toolbar)
    var platform = (navigator.platform || '').toLowerCase();
    var uaDataPlatform = (navigator.userAgentData && navigator.userAgentData.platform ? navigator.userAgentData.platform : '').toLowerCase();

    // 4.1 Plataforma Desktop fingindo ser Mobile
    var isSpoofedPlatform = platform.indexOf('win') !== -1 || 
                           platform.indexOf('macintel') !== -1 || 
                           platform.indexOf('linux x86_64') !== -1 ||
                           uaDataPlatform.indexOf('windows') !== -1 ||
                           uaDataPlatform.indexOf('macos') !== -1;

    if (isSpoofedPlatform) {
      redirectToWhitehat();
      return;
    }

    // 4.2 Armadilha de Bateria para iPhone Fake no Chrome do PC
    // iOS Safari NUNCA implementou navigator.getBattery. Chrome Desktop sempre implementa!
    if (/iPhone|iPad|iPod/i.test(ua) && typeof navigator.getBattery === 'function') {
      redirectToWhitehat();
      return;
    }

    // 4.3 Plugins de Desktop presentes em UA mobile
    if (navigator.plugins && navigator.plugins.length > 0) {
      for (var p = 0; p < navigator.plugins.length; p++) {
        var pName = (navigator.plugins[p].name || '').toLowerCase();
        if (pName.indexOf('pdf') !== -1 || pName.indexOf('chrome') !== -1 || pName.indexOf('native client') !== -1) {
          redirectToWhitehat();
          return;
        }
      }
    }

    // 4.4 Detecção de GPU de Desktop
    try {
      var canvas = document.createElement('canvas');
      var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (gl) {
        var debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
        if (debugInfo) {
          var renderer = (gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) || '').toLowerCase();
          if ((renderer.indexOf('nvidia') !== -1 || 
               renderer.indexOf('geforce') !== -1 || 
               renderer.indexOf('radeon') !== -1 || 
               renderer.indexOf('direct3d') !== -1 ||
               renderer.indexOf('llvmpipe') !== -1) && 
              renderer.indexOf('adreno') === -1 && 
              renderer.indexOf('mali') === -1 && 
              renderer.indexOf('apple') === -1) {
            redirectToWhitehat();
            return;
          }
        }
      }
    } catch (e) {}

    // 5. VALIDAÇÃO DE ANÚNCIO REAL DO TIKTOK
    // 5.1 Navegador In-App Oficial do TikTok
    var isTikTokInApp = /musical_ly|ByteLocale|BytedanceWebview|TikTok|trill|ByteFull/i.test(ua);

    // 5.2 Parâmetro Oficial de Clique com Hash Válido (ttclid >= 10 caracteres)
    var ttclid = params.get('ttclid') || params.get('tt_click_id') || '';
    var hasValidTtclid = ttclid.length >= 10;

    // 5.3 Outros parâmetros de campanha
    var hasAdParams = hasValidTtclid ||
                      isTikTokInApp ||
                      params.has('campaign_id') ||
                      (params.get('utm_source') === 'tiktok' && params.has('tt_medium'));

    // 5.4 Sessão já aprovada de comprador navegando no celular
    var hasAdSession = sessionStorage.getItem('is_ad_traffic') === 'true' || 
                       Boolean(sessionStorage.getItem('ttclid')) || 
                       Boolean(localStorage.getItem('ttclid'));

    if (hasAdParams) {
      var savedId = ttclid || (isTikTokInApp ? 'tiktok_app_verified' : 'ad_verified');
      sessionStorage.setItem('ttclid', savedId);
      localStorage.setItem('ttclid', savedId);
      sessionStorage.setItem('is_ad_traffic', 'true');
      if (document.documentElement) document.documentElement.style.visibility = '';
      return; // APROVADO: Tráfego legítimo do anúncio no celular
    }

    if (hasAdSession) {
      if (document.documentElement) document.documentElement.style.visibility = '';
      return; // APROVADO: Comprador navegando entre telas da loja
    }

    // 6. Acesso no celular comum sem anúncio -> Envia para a Loja Whitehat
    redirectToWhitehat();

  } catch (err) { window.location.replace('/loja'); }
})();
