const fs = require('fs');
const path = require('path');
const http = require('http');
const { renderProdutoFromData, renderReviews } = require('../../api/_lib/render-produto');
const {
  DRAFTS_ROOT,
  getNextProductId,
  createDraft,
  loadDraft,
  saveDraft,
  listDrafts,
  popFromReserve,
  applyDraftPatch,
  applyDaemonPatch,
  buildProductJsonFromDraft,
} = require('./draft-manager');
const { publishDraft } = require('./publisher');

const ROOT = path.join(__dirname, '..', '..');
const DAEMON_PORT = Number(process.env.STUDIO_DAEMON_PORT || 3334);

const sseClients = new Map(); // draftId -> Set<res>

const MIME_MAP = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webp': 'image/webp',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.mp4': 'video/mp4',
};

function parseCookies(cookieHeader) {
  const out = {};
  String(cookieHeader || '')
    .split(';')
    .forEach((pair) => {
      const idx = pair.indexOf('=');
      if (idx > 0) {
        const k = pair.slice(0, idx).trim();
        const v = pair.slice(idx + 1).trim();
        try {
          out[k] = decodeURIComponent(v);
        } catch (_) {
          out[k] = v;
        }
      }
    });
  return out;
}

function sendJson(res, status, obj, extraHeaders = {}) {
  const body = JSON.stringify(obj);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    ...extraHeaders,
  });
  res.end(body);
}

function readJsonBody(req) {
  return new Promise((resolve) => {
    let raw = '';
    req.on('data', (c) => {
      raw += c;
      if (raw.length > 8 * 1024 * 1024) req.destroy();
    });
    req.on('end', () => {
      try {
        resolve(raw ? JSON.parse(raw) : {});
      } catch (_) {
        resolve({});
      }
    });
    req.on('error', () => resolve({}));
  });
}

function callDaemon(method, endpoint, bodyObj = null, timeoutMs = 4000) {
  return new Promise((resolve) => {
    const payload = bodyObj ? Buffer.from(JSON.stringify(bodyObj), 'utf8') : null;
    const req = http.request(
      {
        hostname: '127.0.0.1',
        port: DAEMON_PORT,
        path: endpoint,
        method,
        timeout: timeoutMs,
        headers: payload
          ? { 'Content-Type': 'application/json', 'Content-Length': String(payload.length) }
          : {},
      },
      (res) => {
        let data = '';
        res.on('data', (c) => { data += c; });
        res.on('end', () => {
          try {
            resolve({ ok: res.statusCode >= 200 && res.statusCode < 300, data: JSON.parse(data || '{}') });
          } catch (_) {
            resolve({ ok: false, data: {} });
          }
        });
      }
    );
    req.on('timeout', () => { req.destroy(); resolve({ ok: false, data: {} }); });
    req.on('error', () => resolve({ ok: false, data: {} }));
    if (payload) req.write(payload);
    req.end();
  });
}

function buildSseFrame(draft, eventName, extra = {}) {
  const built = buildProductJsonFromDraft(draft);
  const livePatch = {
    product_title: built.product_title,
    price_int: built.price_int,
    price_cents: built.price_cents,
    price_original: built.price_original,
    discount_badge: built.discount_badge,
    installment_text: built.installment_text,
    coupon_main: built.coupon_main,
    sold_num: parseInt(String(built.sold_count).replace(/\D/g, ''), 10) || 1240,
    rating_score: built.rating_score,
    rating_count: built.rating_count,
    reviews_header: built.reviews_header,
    description_html: built.description_html,
    slider_imgs: built.slider_imgs,
    reviews_cards_html: renderReviews(built.reviews),
    video: built.video,
    creators: built.creators,
    produto_atual: built.produto_atual,
  };
  return `event: ${eventName}\ndata: ${JSON.stringify({ event: eventName, draft, livePatch, extra })}\n\n`;
}

function broadcastDraftEvent(draftId, eventName, extra = {}) {
  const listeners = sseClients.get(draftId);
  if (!listeners || listeners.size === 0) return;
  const draft = loadDraft(draftId);
  if (!draft) return;
  const frame = buildSseFrame(draft, eventName, extra);
  for (const clientRes of listeners) {
    try { clientRes.write(frame); } catch (_) {}
  }
}

async function waitForActiveCatboxUploads(draftId, maxWaitMs = 25000) {
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    const d = loadDraft(draftId);
    if (!d) return;
    const descPending = d.video && d.video.src && !/catbox\.moe\//i.test(d.video.src);
    const creatorPending = (d.creators || []).some((c) => c.video && !/catbox\.moe\//i.test(c.video));
    if (!descPending && !creatorPending) return;
    await new Promise((r) => setTimeout(r, 1200));
  }
}

function handleStudioRequest(req, res) {
  if (process.env.STUDIO_MODE !== '1') return false;

  const parsedUrl = new URL(req.url || '/', `http://${req.headers.host || '127.0.0.1'}`);
  let decodedPath;
  try {
    decodedPath = decodeURIComponent(parsedUrl.pathname || '/');
  } catch (_) {
    res.writeHead(400, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('400 Bad Request');
    return true;
  }

  const pathname = path.posix.normalize(decodedPath).replace(/\\/g, '/').replace(/\/{2,}/g, '/');
  const lowerPath = pathname.toLowerCase();

  // Hard block internal/dot directories from ever leaking over public Cloudflare Tunnel
  if (
    (lowerPath.startsWith('/.') && !lowerPath.startsWith('/.studio-drafts/')) ||
    lowerPath.startsWith('/scripts/') ||
    lowerPath === '/scripts' ||
    lowerPath.startsWith('/docs/') ||
    lowerPath === '/docs'
  ) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end('403 Forbidden');
    return true;
  }

  const isStudioRoute =
    lowerPath === '/importador' ||
    lowerPath === '/importador.html' ||
    lowerPath.startsWith('/api/studio/') ||
    lowerPath.startsWith('/.studio-drafts/');

  if (!isStudioRoute) return false;

  // Fail-closed token authentication
  const expectedToken = String(process.env.STUDIO_TOKEN || '').trim();
  if (!expectedToken) {
    res.writeHead(401, { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end('401 STUDIO_TOKEN ausente');
    return true;
  }

  const queryKey = parsedUrl.searchParams.get('key') || '';
  const headerKey = req.headers['x-studio-key'] || '';
  const cookies = parseCookies(req.headers.cookie);
  const cookieKey = cookies.studio_key || '';

  const provided = queryKey || headerKey || cookieKey;
  if (provided !== expectedToken) {
    res.writeHead(401, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end('<h1>401 — Acesso restrito ao Stone Studio</h1><p>Abra pelo link completo com ?key=... gerado no terminal.</p>');
    return true;
  }

  if (queryKey === expectedToken && cookieKey !== expectedToken) {
    res.setHeader('Set-Cookie', `studio_key=${encodeURIComponent(expectedToken)}; Path=/; HttpOnly; SameSite=Lax`);
  }

  // 1. Serve Studio HTML
  if (req.method === 'GET' && (lowerPath === '/importador' || lowerPath === '/importador.html')) {
    const htmlPath = path.join(ROOT, 'importador.html');
    if (!fs.existsSync(htmlPath)) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('importador.html not found');
      return true;
    }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' });
    fs.createReadStream(htmlPath).pipe(res);
    return true;
  }

  // 2. Serve local draft media safely
  if (req.method === 'GET' && lowerPath.startsWith('/.studio-drafts/')) {
    const rel = pathname.replace(/^\/\.studio-drafts\//i, '');
    const abs = path.resolve(DRAFTS_ROOT, rel);
    if (!abs.startsWith(path.resolve(DRAFTS_ROOT) + path.sep) || !fs.existsSync(abs) || !fs.statSync(abs).isFile()) {
      res.writeHead(404);
      res.end('Not found');
      return true;
    }
    const ext = path.extname(abs).toLowerCase();
    res.writeHead(200, {
      'Content-Type': MIME_MAP[ext] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
    });
    fs.createReadStream(abs).pipe(res);
    return true;
  }

  // 3A. Single-writer atomic daemon delta merge endpoint
  if (req.method === 'POST' && pathname === '/api/studio/internal/patch') {
    readJsonBody(req).then((body) => {
      if (!body || !body.draftId) return sendJson(res, 400, { ok: false });
      const resPatch = applyDaemonPatch(body.draftId, body);
      if (!resPatch) return sendJson(res, 404, { ok: false });
      if (body.event) {
        broadcastDraftEvent(body.draftId, body.event, body.extra || {});
      }
      return sendJson(res, 200, { ok: true, draft: resPatch.draft });
    });
    return true;
  }

  // 3B. Internal daemon notification webhook (warnings/status)
  if (req.method === 'POST' && pathname === '/api/studio/internal/notify') {
    readJsonBody(req).then((body) => {
      if (body && body.draftId && body.event) {
        broadcastDraftEvent(body.draftId, body.event, body.payload || {});
      }
      sendJson(res, 200, { ok: true });
    });
    return true;
  }

  // 4. Studio state
  if (req.method === 'GET' && pathname === '/api/studio/state') {
    callDaemon('GET', '/health', null, 1500).then((health) => {
      sendJson(res, 200, {
        ok: true,
        nextId: getNextProductId(),
        daemonOnline: Boolean(health.ok),
        browserWarm: Boolean(health.data && health.data.browser_warm),
        drafts: listDrafts().map((d) => ({
          draftId: d.draftId,
          targetId: d.targetId,
          product_title: d.product_title,
          price_pix: d.price_pix,
          updatedAt: d.updatedAt,
        })),
      });
    });
    return true;
  }

  // 5. Start instant extraction
  if (req.method === 'POST' && pathname === '/api/studio/extract') {
    readJsonBody(req).then(async (body) => {
      const url1 = String(body.url1 || '').trim();
      const url2 = String(body.url2 || '').trim();
      if (!url1) return sendJson(res, 400, { ok: false, error: 'Informe o link do TikTok Shop ou Mercado Livre.' });

      const manualPix = Number(body.price_pix || 0);
      const draft = createDraft({
        targetId: Number(body.targetId) || getNextProductId(),
        product_title: 'Extraindo dados do anúncio...',
        price_pix: manualPix > 0 ? manualPix : 49.89,
        gender: body.gender || 'feminino',
        source_urls: [url1, url2].filter(Boolean),
        status: 'extracting',
      });

      if (manualPix > 0) {
        draft.user_locked_price = true;
        saveDraft(draft);
      }

      const draftDir = path.join(DRAFTS_ROOT, draft.draftId);
      await callDaemon('POST', '/extract', {
        draftId: draft.draftId,
        draftDir,
        url1,
        url2,
        autoVideos: body.autoVideos !== false,
      }, 4000);

      const built = buildProductJsonFromDraft(draft);
      return sendJson(res, 200, {
        ok: true,
        draft,
        built,
        previewUrl: `/api/studio/preview/${draft.draftId}?owner=1`,
      });
    });
    return true;
  }

  // 6. SSE real-time stream (pushes immediate snapshot on connect to prevent fast_preview race)
  const streamMatch = pathname.match(/^\/api\/studio\/stream\/([a-zA-Z0-9_-]+)$/);
  if (req.method === 'GET' && streamMatch) {
    const draftId = streamMatch[1];
    res.writeHead(200, {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-cache, no-transform',
      Connection: 'keep-alive',
    });
    res.write(': connected\n\n');
    const curDraft = loadDraft(draftId);
    if (curDraft) {
      res.write(buildSseFrame(curDraft, 'sync_state', {}));
    }

    if (!sseClients.has(draftId)) sseClients.set(draftId, new Set());
    sseClients.get(draftId).add(res);

    const hb = setInterval(() => {
      try { res.write(': ping\n\n'); } catch (_) {}
    }, 15000);

    req.on('close', () => {
      clearInterval(hb);
      const set = sseClients.get(draftId);
      if (set) {
        set.delete(res);
        if (set.size === 0) sseClients.delete(draftId);
      }
    });
    return true;
  }

  // 7. Live mobile preview HTML
  const previewMatch = pathname.match(/^\/api\/studio\/preview\/([a-zA-Z0-9_-]+)$/);
  if (req.method === 'GET' && previewMatch) {
    const draft = loadDraft(previewMatch[1]);
    if (!draft) {
      res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end('<h1>Rascunho não encontrado</h1>');
      return true;
    }
    const built = buildProductJsonFromDraft(draft);
    const rendered = renderProdutoFromData(built, { studioPreview: true });
    res.writeHead(rendered.status || 200, {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
    });
    res.end(rendered.html);
    return true;
  }

  // 8. 0ms Reserve Expansion (+ Mais Vídeos / + Mais Fotos / + Mais Comentários)
  const moreMatch = pathname.match(/^\/api\/studio\/draft\/([a-zA-Z0-9_-]+)\/more$/);
  if (req.method === 'POST' && moreMatch) {
    const draftId = moreMatch[1];
    readJsonBody(req).then((body) => {
      try {
        const result = popFromReserve(draftId, body.kind || 'reviews', Number(body.count) || 2);
        if (body.kind === 'videos' && result.remaining < 3) {
          const draftDir = path.join(DRAFTS_ROOT, draftId);
          const q = String(result.draft.product_title || '').split(/\s+/).slice(0, 4).join(' ');
          callDaemon('POST', '/videos', { draftId, draftDir, mode: 'search', query: `${q} review` }, 3000);
        }
        return sendJson(res, 200, { ok: true, ...result });
      } catch (err) {
        return sendJson(res, 404, { ok: false, error: err.message });
      }
    });
    return true;
  }

  // 9. Add pasted TikTok video URLs or run custom TikTok search
  const vidMatch = pathname.match(/^\/api\/studio\/draft\/([a-zA-Z0-9_-]+)\/videos$/);
  if (req.method === 'POST' && vidMatch) {
    const draftId = vidMatch[1];
    readJsonBody(req).then(async (body) => {
      const draft = loadDraft(draftId);
      if (!draft) return sendJson(res, 404, { ok: false, error: 'Rascunho não encontrado.' });
      const draftDir = path.join(DRAFTS_ROOT, draftId);
      await callDaemon('POST', '/videos', {
        draftId,
        draftDir,
        mode: body.mode || 'urls',
        query: body.query || '',
        urls: Array.isArray(body.urls) ? body.urls : [],
      }, 4000);
      return sendJson(res, 202, { ok: true });
    });
    return true;
  }

  // 10. Get or Patch Draft
  const draftMatch = pathname.match(/^\/api\/studio\/draft\/([a-zA-Z0-9_-]+)$/);
  if (draftMatch) {
    const draftId = draftMatch[1];
    if (req.method === 'GET') {
      const draft = loadDraft(draftId);
      if (!draft) return sendJson(res, 404, { ok: false, error: 'Rascunho não encontrado.' }) || true;
      return sendJson(res, 200, { ok: true, draft, built: buildProductJsonFromDraft(draft) }) || true;
    }
    if (req.method === 'POST') {
      readJsonBody(req).then((body) => {
        try {
          const out = applyDraftPatch(draftId, body);
          return sendJson(res, 200, { ok: true, ...out });
        } catch (err) {
          return sendJson(res, 404, { ok: false, error: err.message });
        }
      });
      return true;
    }
  }

  // 11. Publish Draft (Atomic Validator + Optional Git/Vercel Deploy)
  const pubMatch = pathname.match(/^\/api\/studio\/publish\/([a-zA-Z0-9_-]+)$/);
  if (req.method === 'POST' && pubMatch) {
    const draftId = pubMatch[1];
    readJsonBody(req).then(async (body) => {
      await waitForActiveCatboxUploads(draftId, 25000);
      const out = await publishDraft(draftId, { deploy: body.deploy !== false });
      return sendJson(res, out.ok ? 200 : 422, out);
    });
    return true;
  }

  sendJson(res, 404, { ok: false, error: 'Rota Studio desconhecida' });
  return true;
}

module.exports = {
  handleStudioRequest,
};
