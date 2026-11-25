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

  // 5. Anti-Debugger Dinâmico (Congela a execução se o DevTools for aberto)
  var killPage = function () {
    try {
      if (document.body) document.body.innerHTML = '';
    } catch (e) {}
    window.location.replace('about:blank');
  };

  var checkDebugger = function () {
    var startTime = performance.now();
    debugger;
    var endTime = performance.now();
    if (endTime - startTime > 100) {
      killPage();
    }
  };
  setInterval(checkDebugger, 800);

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
