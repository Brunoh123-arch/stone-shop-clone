const http = require('http');
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const COMPRESSIBLE_EXTS = new Set(['.html', '.css', '.js', '.json', '.svg']);

const PORT = process.env.PORT || 3333;
const ROOT = __dirname;

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf'
};

const server = http.createServer((req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');

  // Stone Studio (/importador + /api/studio/*) — ativo exclusivamente em STUDIO_MODE=1
  if (process.env.STUDIO_MODE === '1' && require('./scripts/studio/studio-api').handleStudioRequest(req, res)) {
    return;
  }

  // Intercepta rota de API /api/chave (se existir)
  if (req.url.startsWith('/api/chave') && fs.existsSync(path.join(ROOT, 'api', 'chave.js'))) {
    const chaveHandler = require(path.join(ROOT, 'api', 'chave.js'));
    const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    req.query = Object.fromEntries(parsedUrl.searchParams);
    res.status = (code) => { res.statusCode = code; return res; };
    res.json = (data) => {
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
      res.end(JSON.stringify(data));
      return res;
    };
    return chaveHandler(req, res);
  }

  // Intercepta rota de API /api/pedidos
  if (req.url.startsWith('/api/pedidos')) {
    const pedidosHandler = require('./api/pedidos');
    let bodyData = '';
    req.on('data', chunk => { bodyData += chunk; });
    req.on('end', () => {
      try { req.body = bodyData ? JSON.parse(bodyData) : {}; } catch(e) { req.body = {}; }
      const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
      req.query = Object.fromEntries(parsedUrl.searchParams);
      res.status = (code) => { res.statusCode = code; return res; };
      res.json = (data) => {
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify(data));
        return res;
      };
      return pedidosHandler(req, res);
    });
    return;
  }

  // Intercepta rota de API /api/create-pix
  if (req.url.startsWith('/api/create-pix')) {
    const createPixHandler = require('./api/create-pix');
    let bodyData = '';
    req.on('data', chunk => { bodyData += chunk; });
    req.on('end', () => {
      try { req.body = bodyData ? JSON.parse(bodyData) : {}; } catch(e) { req.body = {}; }
      const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
      req.query = Object.fromEntries(parsedUrl.searchParams);
      res.status = (code) => { res.statusCode = code; return res; };
      res.json = (data) => {
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify(data));
        return res;
      };
      return createPixHandler(req, res);
    });
    return;
  }

  // Intercepta rota de API /api/payment-status
  if (req.url.startsWith('/api/payment-status')) {
    const paymentStatusHandler = require('./api/payment-status');
    let bodyData = '';
    req.on('data', chunk => { bodyData += chunk; });
    req.on('end', () => {
      try { req.body = bodyData ? JSON.parse(bodyData) : {}; } catch(e) { req.body = {}; }
      const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
      req.query = Object.fromEntries(parsedUrl.searchParams);
      res.status = (code) => { res.statusCode = code; return res; };
      res.json = (data) => {
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify(data));
        return res;
      };
      return paymentStatusHandler(req, res);
    });
    return;
  }

  // Intercepta rota de API /api/produtos (se existir)
  if (req.url.startsWith('/api/produtos') && fs.existsSync(path.join(ROOT, 'api', 'produtos.js'))) {
    const produtosHandler = require(path.join(ROOT, 'api', 'produtos.js'));
    let bodyData = '';
    req.on('data', chunk => { bodyData += chunk; });
    req.on('end', () => {
      try { req.body = bodyData ? JSON.parse(bodyData) : {}; } catch(e) { req.body = {}; }
      const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
      req.query = Object.fromEntries(parsedUrl.searchParams);
      res.status = (code) => { res.statusCode = code; return res; };
      res.json = (data) => {
        res.setHeader('Content-Type', 'application/json; charset=utf-8');
        res.end(JSON.stringify(data));
        return res;
      };
      return produtosHandler(req, res);
    });
    return;
  }

  // Intercepta rota raiz / ou /index.html para Server-Side Cloaking
  const cleanUrl = req.url.split('?')[0];

  // Modelo Único Permanente: renderiza /pages/produto-X, /produto-X e /produto/X via api/serve.js
  const prodMatch = cleanUrl.match(/^(?:\/pages)?\/produto[-/](\d+)(?:\.html)?$/i);
  if (prodMatch) {
    const serveHandler = require('./api/serve');
    req.query = { slug: `produto-${prodMatch[1]}` };
    res.status = (code) => { res.statusCode = code; return res; };
    res.send = (html) => {
      if (!res.getHeader('Content-Type')) res.setHeader('Content-Type', 'text/html; charset=utf-8');
      const acceptEnc = req.headers['accept-encoding'] || '';
      if (acceptEnc.includes('gzip') && typeof html === 'string' && html.length > 1024) {
        res.setHeader('Content-Encoding', 'gzip');
        res.setHeader('Vary', 'Accept-Encoding');
        return zlib.gzip(Buffer.from(html, 'utf8'), (err, buf) => {
          if (err) { res.removeHeader('Content-Encoding'); return res.end(html); }
          res.setHeader('Content-Length', buf.length);
          res.end(buf);
        });
      }
      res.end(html);
      return res;
    };
    return serveHandler(req, res);
  }

  if (cleanUrl === '/' || cleanUrl === '' || cleanUrl === '/index' || cleanUrl === '/index.html') {
    const serveHandler = require('./api/serve');
    const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
    req.query = Object.fromEntries(parsedUrl.searchParams);
    res.status = (code) => { res.statusCode = code; return res; };
    res.send = (html) => {
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      const acceptEnc = req.headers['accept-encoding'] || '';
      if (acceptEnc.includes('gzip') && typeof html === 'string' && html.length > 1024) {
        res.setHeader('Content-Encoding', 'gzip');
        res.setHeader('Vary', 'Accept-Encoding');
        return zlib.gzip(Buffer.from(html, 'utf8'), (err, buf) => {
          if (err) { res.removeHeader('Content-Encoding'); return res.end(html); }
          res.setHeader('Content-Length', buf.length);
          res.end(buf);
        });
      }
      res.end(html);
      return res;
    };
    return serveHandler(req, res);
  }

  let reqPath = decodeURIComponent(cleanUrl);
  if (reqPath === '/carrinho') reqPath = '/pages/carrinho.html';
  else if (reqPath === '/resumo' || reqPath === '/checkout') reqPath = '/pages/resumo.html';
  else if (reqPath === '/catalogo-ads' || reqPath === '/todos-produtos') reqPath = '/catalogo-ads.html';
  else if (reqPath === '/videos-ads' || reqPath === '/ads' || reqPath === '/painel' || reqPath === '/admin') reqPath = '/admin.html';

  let filePath = path.join(ROOT, reqPath);

  // If path is a directory, look for index.html
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, 'index.html');
  }

  // If file doesn't exist, try appending .html
  if (!fs.existsSync(filePath) && fs.existsSync(filePath + '.html')) {
    filePath = filePath + '.html';
  }

  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    res.end('404 Not Found');
    return;
  }

  const stat = fs.statSync(filePath);
  const ext = path.extname(filePath).toLowerCase();
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  // Handle Video Streaming / HTTP Range Requests
  if (ext === '.mp4' || ext === '.webm') {
    const range = req.headers.range;
    if (range) {
      const parts = range.replace(/bytes=/, '').split('-');
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : stat.size - 1;
      const chunksize = (end - start) + 1;
      const file = fs.createReadStream(filePath, { start, end });

      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${stat.size}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': chunksize,
        'Content-Type': contentType
      });
      file.pipe(res);
      return;
    }
  }

  // Normal File Serving (com Gzip automático para HTML/CSS/JS/JSON/SVG e cache rápido de mídia/fontes)
  const isImmutableMedia = (ext === '.png' || ext === '.jpg' || ext === '.jpeg' || ext === '.webp' || ext === '.gif' || ext === '.woff' || ext === '.woff2' || ext === '.ttf' || ext === '.ico');
  const cacheHeader = isImmutableMedia
    ? 'public, max-age=31536000, immutable'
    : ((ext === '.css' || ext === '.js') ? 'public, max-age=300' : 'no-cache');

  const acceptEncoding = req.headers['accept-encoding'] || '';
  if (COMPRESSIBLE_EXTS.has(ext) && stat.size > 1024 && acceptEncoding.includes('gzip')) {
    res.writeHead(200, {
      'Content-Type': contentType,
      'Content-Encoding': 'gzip',
      'Vary': 'Accept-Encoding',
      'Cache-Control': cacheHeader
    });
    fs.createReadStream(filePath).pipe(zlib.createGzip({ level: 6 })).pipe(res);
    return;
  }

  res.writeHead(200, {
    'Content-Length': stat.size,
    'Content-Type': contentType,
    'Cache-Control': cacheHeader
  });
  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, () => {
  console.log(`====================================================`);
  console.log(`🚀 Stone Shop Cloned Store Online!`);
  console.log(`🔗 URL: http://localhost:${PORT}`);
  console.log(`🛍️ Vitrine: http://localhost:${PORT}/index.html`);
  console.log(`🛒 Carrinho: http://localhost:${PORT}/pages/carrinho.html`);
  console.log(`====================================================`);
});
