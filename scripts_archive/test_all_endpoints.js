const http = require('http');
const fs = require('fs');
const path = require('path');

// Import server logic
const PORT = 3055;
process.env.PORT = PORT;
require('./server.js');

setTimeout(async () => {
  const routes = [
    '/',
    '/index.html',
    '/inicio.html',
    '/confirmar-saque',
    '/confirmar-saque.html',
    '/vsl.html',
    '/css/style.css',
    '/js/main.js',
    '/js/tracking.js',
    '/videos/vsl.mp4',
    '/images/bacen.png',
    '/images/fi-bs-check.svg',
    '/images/fi-rs-credit-card.png',
    '/images/flor.png',
    '/images/gol.png',
    '/images/gov-br.webp',
    '/images/logotiktok.png',
    '/images/p-assista.svg',
    '/images/p-dia.svg',
    '/images/p-saldo-maior.png',
    '/images/p-saldo.svg',
    '/images/parabens-img.png',
    '/images/pix-logo.svg',
    '/images/pix-solo.svg',
    '/images/receitafederal.png'
  ];

  let failed = 0;
  let passed = 0;

  for (const r of routes) {
    await new Promise((resolve) => {
      http.get(`http://localhost:${PORT}${r}`, (res) => {
        if (res.statusCode === 200) {
          console.log(`✅ [200 OK] ${r} (${res.headers['content-type']})`);
          passed++;
        } else {
          console.error(`❌ [FAIL ${res.statusCode}] ${r}`);
          failed++;
        }
        res.resume();
        resolve();
      }).on('error', (err) => {
        console.error(`❌ [ERROR] ${r}:`, err.message);
        failed++;
        resolve();
      });
    });
  }

  // Test Range request for video
  await new Promise((resolve) => {
    const req = http.request(`http://localhost:${PORT}/videos/vsl.mp4`, {
      headers: { Range: 'bytes=0-1023' }
    }, (res) => {
      if (res.statusCode === 206) {
        console.log(`✅ [206 Partial Content] /videos/vsl.mp4 range test passed`);
        passed++;
      } else {
        console.error(`❌ [FAIL ${res.statusCode}] /videos/vsl.mp4 range test failed`);
        failed++;
      }
      res.resume();
      resolve();
    });
    req.end();
  });

  console.log(`\n=== RESULT: ${passed} passed, ${failed} failed ===`);
  process.exit(failed > 0 ? 1 : 0);
}, 500);
