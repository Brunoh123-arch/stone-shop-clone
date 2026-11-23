const fs = require('fs');
const path = require('path');
const stoneHtmlFallback = require('./_lib/stone_content');
const fakeHtmlFallback = require('./_lib/fake_content');
let versionsBundle = {};
try {
  versionsBundle = require('./_lib/versions_content');
} catch (e) {}

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

module.exports = async function handler(req, res) {
  try {
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0, s-maxage=0');
    res.setHeader('CDN-Cache-Control', 'no-store');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');

    // Se for SaveWeb2Zip, HTTrack ou espião concorrente -> Recebe a página fake embaralhada!
    if (isScraper(req)) {
      let fakeHtml = fakeHtmlFallback;
      try {
        const fakePath = path.join(__dirname, '..', 'fake.html');
        if (fs.existsSync(fakePath)) fakeHtml = fs.readFileSync(fakePath, 'utf8');
      } catch (e) {}
      return res.status(200).send(fakeHtml);
    }

    // Se for requisição de página de produto (/pages/:slug)
    if (req.query && req.query.slug) {
      let slug = String(req.query.slug).replace(/[^a-zA-Z0-9_-]/g, '');
      if (slug.endsWith('.html')) slug = slug.replace('.html', '');

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
      
      // Tenta puxar do bundle em memória (super rápido no serverless da Vercel)
      if (versionsBundle && versionsBundle[cleanVer]) {
        return res.status(200).send(versionsBundle[cleanVer]);
      }

      // Tenta puxar do filesystem
      const verPath = path.join(__dirname, '..', 'versions', `${cleanVer}.html`);
      try {
        if (fs.existsSync(verPath)) {
          return res.status(200).send(fs.readFileSync(verPath, 'utf8'));
        }
      } catch (e) {}
    }

    // Página principal da Loja Real (real.html ou index.html)
    let html = stoneHtmlFallback;
    try {
      const realPath = path.join(__dirname, '..', 'index.html');
      if (fs.existsSync(realPath)) {
        html = fs.readFileSync(realPath, 'utf8');
      }
    } catch (e) {}

    return res.status(200).send(html);
  } catch (err) {
    return res.status(200).send(stoneHtmlFallback || '<h1>Stone Shop</h1>');
  }
};
