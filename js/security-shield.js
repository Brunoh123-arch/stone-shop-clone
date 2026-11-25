/**
 * SecurityShield v4.0 - Ultra Anti-Inspection, Anti-Debugger & Mobile Inspector Defense
 * Protege contra:
 * - Abertura de DevTools no PC (F12, atalhos, debugger trap)
 * - Inspetores de Desenvolvedor no Celular (Eruda, vConsole, Chii)
 * - Download de assets, arrastar imagens e seleção
 * - Iframes e clickjacking
 */
(function () {
  'use strict';

  // Bypass do Dono (para manutenção, inspeção e testes com ?preview=1, ?owner=1 ou localhost)
  try {
    var params = new URLSearchParams(window.location.search || '');
    var isOwner = params.get('preview') === '1' || 
                  params.get('c') === '1' || 
                  params.get('owner') === '1' ||
                  window.location.hostname === 'localhost' || 
                  window.location.hostname === '127.0.0.1';
    if (isOwner) return;
  } catch (eBypass) {}

  // 1. Anti-Frame / Anti-Clickjacking
  try {
    if (window.top !== window.self) {
      window.top.location = window.self.location;
    }
  } catch (e) {}

  // 2. Bloqueio de Clique com Botão Direito (Context Menu)
  document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
    return false;
  }, { capture: true });

  // 3. Bloqueio de Atalhos de Teclado (F12, Ctrl+U, Ctrl+Shift+I/J/C, Ctrl+S, Ctrl+P)
  document.addEventListener('keydown', function (e) {
    if (e.keyCode === 123 || e.key === 'F12') {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
    if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.key === 'J' || e.key === 'j' || e.key === 'C' || e.key === 'c')) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
    if (e.ctrlKey && (e.key === 'u' || e.key === 'U' || e.key === 's' || e.key === 'S' || e.key === 'p' || e.key === 'P')) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
  }, { capture: true });

  // 4. Bloqueio de Arrastar Imagens
  document.addEventListener('dragstart', function (e) {
    if (e.target && e.target.nodeName === 'IMG') {
      e.preventDefault();
      return false;
    }
  }, { capture: true });

  // 5. Anti-Debugger Dinâmico (Ativo apenas em Desktop ou quando DevTools está aberto)
  var killPage = function () {
    try {
      if (document.body) document.body.innerHTML = '';
    } catch (e) {}
    window.location.replace('about:blank');
  };

  var checkDebugger = function () {
    // Se a aba estiver em segundo plano (ex: cliente no app do banco pagando Pix), não dispara
    if (document.hidden || (typeof document.hasFocus === 'function' && !document.hasFocus())) {
      return;
    }

    // Se for celular legítimo em tela cheia com touch, não quebra por micro-lag de CPU
    var isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent || '') && (navigator.maxTouchPoints > 0 || 'ontouchstart' in window);
    var devtoolsOpen = false;
    if (window.outerWidth && window.innerWidth) {
      devtoolsOpen = (window.outerWidth - window.innerWidth > 160) || (window.outerHeight - window.innerHeight > 160);
    }

    var startTime = performance.now();
    debugger;
    var endTime = performance.now();

    // No desktop com DevTools dockado ou lag anormal de breakpoint aberto
    if (endTime - startTime > 120 && (!isMobile || devtoolsOpen)) {
      killPage();
    }
  };
  setInterval(checkDebugger, 1000);

  // 6. Bloqueio de Inspetores Mobile (Eruda, vConsole, Chii)
  var checkMobileInspectors = function () {
    if (window.eruda || 
        window.__vConsole || 
        window.vConsole || 
        window._chii ||
        document.getElementById('eruda') || 
        document.querySelector('.vc-panel') ||
        document.querySelector('.eruda-container')) {
      killPage();
    }
  };
  setInterval(checkMobileInspectors, 600);

  // Armadilhas de interceptação de Eruda e vConsole no objeto window
  try {
    ['eruda', '__vConsole', 'vConsole', '_chii'].forEach(function(prop) {
      Object.defineProperty(window, prop, {
        configurable: false,
        enumerable: false,
        get: function() { return undefined; },
        set: function() { killPage(); }
      });
    });
  } catch (err) {}

  // 7. Limpeza e Proteção de Console
  try {
    var noop = function () {};
    ['log', 'debug', 'info', 'warn', 'error', 'table', 'trace', 'dir'].forEach(function (method) {
      if (window.console && window.console[method]) {
        window.console[method] = noop;
      }
    });
  } catch (e) {}

})();
