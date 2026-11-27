const fs = require('fs');
const path = require('path');
const { recordTrafficHit } = require('./_lib/store-state');

let _cachedIndexHtml = null;
let _versionsBundle = null;

function getStoneFallback() {
  try { return require('./_lib/stone_content'); } catch (e) { return '<h1>Stone Shop</h1>'; }
}

function getFakeFallback() {
  try { return require('./_lib/fake_content'); } catch (e) { return ''; }
}

function getVersionsBundle() {
  if (!_versionsBundle) {
    try { _versionsBundle = require('./_lib/versions_content'); } catch (e) { _versionsBundle = {}; }
  }
  return _versionsBundle;
}

// 1. Whitelist Oficial: Bots de aprovação de anúncios (TikTok, Facebook, Google)
// Eles DEVEM ver a loja 100% perfeita para aprovar suas campanhas sem reprovação!
const AD_REVIEW_BOTS = [
  'bytespider',
  'tiktokbot',
  'bytedance',
  'tiktok',
  'facebookexternalhit',
  'facebot',
  'googlebot',
  'adsbot-google',
  'google-adwords',
  'mediapartners-google',
  'twitterbot',
  'pinterest'
];

// 2. Blacklist: Ladrões, clonadores e rippers tipo SaveWeb2Zip
const SCRAPER_BOTS = [
  'saveweb2zip',
  'saveweb',
  'httrack',
  'wget',
  'curl',
  'python',
  'scrapy',
  'headlesschrome',
  'headless',
  'phantomjs',
  'puppeteer',
  'playwright',
  'selenium',
  'axios',
  'node-fetch',
  'go-http-client',
  'postman',
  'cyotek',
  'webcopy',
  'teleport',
  'offline explorer',
  'website extractor',
  'page2zip',
  'adheart',
  'bigspy',
  'dropispy'
];

function isAdReviewer(req) {
  const ua = (req.headers['user-agent'] || '').toLowerCase();
  for (const bot of AD_REVIEW_BOTS) {
    if (ua.includes(bot)) return true;
  }
  return false;
}

function isScraper(req) {
  if (isAdReviewer(req)) return false;

  const ua = (req.headers['user-agent'] || '').toLowerCase();
  for (const bot of SCRAPER_BOTS) {
    if (ua.includes(bot)) return true;
  }
  if (req.headers['x-saveweb2zip'] || req.headers['x-scraper']) return true;
  return false;
}

function detectScraperReason(req) {
  if (isAdReviewer(req)) return null;
  const ua = (req.headers['user-agent'] || '').toLowerCase();
  if (req.headers['x-saveweb2zip'] || ua.includes('saveweb')) return 'SaveWeb2Zip / Ripper';
  if (ua.includes('httrack') || ua.includes('webcopy') || ua.includes('teleport') || ua.includes('offline explorer')) return 'Clonador (HTTrack/Copy)';
  if (ua.includes('headless') || ua.includes('puppeteer') || ua.includes('playwright') || ua.includes('selenium') || ua.includes('phantom')) return 'Browser Headless / Automação';
  if (ua.includes('adheart') || ua.includes('bigspy') || ua.includes('dropispy')) return 'Espião de Anúncios (Spy Tool)';
  for (const bot of SCRAPER_BOTS) {
    if (ua.includes(bot)) return `Bot / CLI (${bot})`;
  }
  if (req.headers['x-scraper']) return 'Header Scraper Detectado';
  return null;
}

module.exports = async function handler(req, res) {
  try {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0, s-maxage=0');
    res.setHeader('CDN-Cache-Control', 'no-store');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');

    const uaStr = req.headers['user-agent'] || '';
    const slugRaw = (req.query && req.query.slug) ? String(req.query.slug) : '';
    const pidMatch = slugRaw.match(/produto-(\d+)/i);
    const hitPid = pidMatch ? Number(pidMatch[1]) : null;
    const scraperReason = detectScraperReason(req);

    // Se for SaveWeb2Zip, HTTrack ou espião concorrente -> Recebe a página fake embaralhada!
    if (scraperReason) {
      recordTrafficHit({ allowed: false, blockedReason: scraperReason, isAdBot: false, ua: uaStr, productId: hitPid, pathUrl: req.url || '/' });
      let fakeHtml = '';
      try {
        const fakePath = path.join(__dirname, '..', 'fake.html');
        if (fs.existsSync(fakePath)) fakeHtml = fs.readFileSync(fakePath, 'utf8');
      } catch (e) {}
      if (!fakeHtml) fakeHtml = getFakeFallback();
      return res.status(200).send(fakeHtml);
    }

    recordTrafficHit({ allowed: true, isAdBot: isAdReviewer(req), ua: uaStr, productId: hitPid, pathUrl: req.url || '/' });

    // Se for requisição de página de produto (/pages/:slug) ou atalho admin (/videos-ads, /ads, /painel)
    if (req.query && req.query.slug) {
      let slug = String(req.query.slug).replace(/[^a-zA-Z0-9_-]/g, '');
      if (slug.endsWith('.html')) slug = slug.replace('.html', '');

      if (slug === 'admin') {
        const adminPath = path.join(__dirname, '..', 'admin.html');
        if (fs.existsSync(adminPath)) {
          return res.status(200).send(fs.readFileSync(adminPath, 'utf8'));
        }
      }

      // Modelo Único Permanente para produto-<id>
      const prodMatch = slug.match(/^produto-(\d+)$/i);
      if (prodMatch) {
        const { renderProdutoHtml } = require('./_lib/render-produto');
        const rendered = renderProdutoHtml(prodMatch[1]);
        if (rendered.status === 302 && rendered.redirect) {
          const target = rendered.redirect.startsWith('/') ? rendered.redirect : `/pages/${rendered.redirect}`;
          res.setHeader('Location', target);
          return res.status(302).end();
        }
        return res.status(rendered.status || 200).send(rendered.html);
      }

      const pathsToTry = [
        path.join(__dirname, '..', 'pages', `${slug}.html`),
        path.join(__dirname, '..', '_pages', `${slug}.html`)
      ];

      for (const p of pathsToTry) {
        if (fs.existsSync(p)) {
          const pageHtml = fs.readFileSync(p, 'utf8');
          return res.status(200).send(pageHtml);
        }
      }
    }

    // 3. Suporte a Time Machine / Preview de Versões Históricas (?v=v1, ?preview=v2, etc.)
    const previewVer = (req.query && (req.query.preview_version || req.query.v || req.query.preview)) || null;
    if (previewVer) {
      const cleanVer = String(previewVer).trim().toLowerCase().replace(/[^a-z0-9_-]/g, '');
      
      // Tenta puxar do bundle em memória apenas sob demanda (evita parsear 2MB no cold start)
      const vb = getVersionsBundle();
      if (vb && vb[cleanVer]) {
        return res.status(200).send(vb[cleanVer]);
      }

      // Tenta puxar do filesystem
      const verPath = path.join(__dirname, '..', 'versions', `${cleanVer}.html`);
      try {
        if (fs.existsSync(verPath)) {
          return res.status(200).send(fs.readFileSync(verPath, 'utf8'));
        }
      } catch (e) {}
    }

    // Página principal da Loja Real (index.html com cache em memória em produção)
    if (process.env.NODE_ENV === 'production' && _cachedIndexHtml) {
      return res.status(200).send(_cachedIndexHtml);
    }
    let html = '';
    try {
      const realPath = path.join(__dirname, '..', 'index.html');
      if (fs.existsSync(realPath)) {
        html = fs.readFileSync(realPath, 'utf8');
        if (process.env.NODE_ENV === 'production') _cachedIndexHtml = html;
      }
    } catch (e) {}
    if (!html) html = getStoneFallback();

    return res.status(200).send(html);
  } catch (err) {
    return res.status(200).send(getStoneFallback());
  }
};
