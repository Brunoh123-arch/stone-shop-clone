/**
 * Preserva UTMs e ids de clique no localStorage (para chat, pagamentos e relatórios).
 *
 * Antes existiam 2 cópias idênticas em front/js/tracking.js e cpf/js/tracking.js.
 * Agora há UMA cópia aqui, carregada por TODAS as páginas via
 * <script src="../../assets/js/tracking.js"></script>.
 *
 * API pública (window):
 *   gvdesenrolaMergeTracking(): object  — merge do localStorage + URL atual
 *   gvdesenrolaAppendQuery(url): string — reescreve href preservando UTMs/click-ids
 *
 * IMPORTANTE: manter a chave localStorage "utm_params_all" por compat com versões antigas
 * (links já em circulação na internet).
 */
(function () {
  var STORE_KEY = "utm_params_all";
  var CLICK_IDS = ["fbclid", "gclid", "wbraid", "gbraid", "ttclid", "msclkid"];
  var EXTRA_KEYS = ["src", "sck", "xcod"];

  function isTrackKey(key) {
    return key.indexOf("utm_") === 0 || CLICK_IDS.indexOf(key) >= 0 || EXTRA_KEYS.indexOf(key) >= 0;
  }

  var params = new URLSearchParams(window.location.search);
  var fromStorage = {};
  try {
    fromStorage = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
  } catch (e) {}

  var fromUrl = {};
  params.forEach(function (value, key) {
    if (isTrackKey(key) && value) fromUrl[key] = value;
  });

  var merged = Object.assign({}, fromStorage, fromUrl);
  if (Object.keys(merged).length > 0) {
    localStorage.setItem(STORE_KEY, JSON.stringify(merged));
  }

  window.gvdesenrolaMergeTracking = function () {
    var out = {};
    try {
      var s = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
      Object.keys(s).forEach(function (k) {
        if (s[k]) out[k] = s[k];
      });
    } catch (e) {}
    params.forEach(function (v, k) {
      if (v) out[k] = v;
    });
    return out;
  };

  window.gvdesenrolaAppendQuery = function (baseUrl) {
    var u = new URL(baseUrl, window.location.origin);
    var m = window.gvdesenrolaMergeTracking();
    Object.keys(m).forEach(function (k) {
      if (!u.searchParams.has(k)) u.searchParams.set(k, m[k]);
    });
    return u.pathname + u.search + u.hash;
  };

  /**
   * UserTracker - Sistema de telemetria e captura de eventos da página
   */
  function UserTracker(config) {
    this.config = Object.assign({
      endpoint: 'tracker.php',
      sessionId: 'sess_' + Math.random().toString(36).substring(2, 12) + '_' + Date.now(),
      trackClicks: true,
      trackScrolls: true,
      trackFormInputs: true,
      trackPageViews: true,
      trackRedirects: true,
      flushInterval: 2000
    }, config || {});

    this.queue = [];
    var self = this;

    if (this.config.flushInterval > 0) {
      setInterval(function () {
        self.flush();
      }, this.config.flushInterval);
    }
  }

  UserTracker.prototype.trackCustom = function (eventName, data) {
    var payload = {
      event: eventName,
      data: data || {},
      sessionId: this.config.sessionId,
      timestamp: Date.now(),
      url: window.location.href
    };
    this.queue.push(payload);
    // Log silencioso ou debug
    if (window.__TRACKER_DEBUG__) {
      console.log('📡 [Tracker Event]:', eventName, payload);
    }
  };

  UserTracker.prototype.flush = function () {
    if (this.queue.length === 0) return;
    var toSend = this.queue.slice();
    this.queue = [];

    if (this.config.endpoint && navigator.sendBeacon) {
      try {
        var blob = new Blob([JSON.stringify(toSend)], { type: 'application/json' });
        navigator.sendBeacon(this.config.endpoint, blob);
      } catch (err) {
        // Fallback silencioso
      }
    }
  };

  window.UserTracker = UserTracker;
})();