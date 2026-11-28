const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');

test('package.json defines npm run studio and start-studio.ps1 enforces Cloudflare HTTPS + STUDIO_TOKEN', () => {
  const pkg = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'package.json'), 'utf8'));
  assert.ok(pkg.scripts && pkg.scripts.studio, 'package.json must define scripts.studio');

  const ps1Path = path.join(process.cwd(), 'scripts', 'studio', 'start-studio.ps1');
  assert.equal(fs.existsSync(ps1Path), true, 'start-studio.ps1 must exist');

  const ps1 = fs.readFileSync(ps1Path, 'utf8');
  assert.match(ps1, /STUDIO_MODE/);
  assert.match(ps1, /STUDIO_TOKEN/);
  assert.match(ps1, /trycloudflare\\?\.com/);
  assert.match(ps1, /\[switch\]\$Detach/);
  assert.match(ps1, /\/health/);

  const homeHtml = fs.readFileSync(path.join(process.cwd(), 'index.html'), 'utf8');
  const pubJs = fs.readFileSync(path.join(process.cwd(), 'scripts', 'studio', 'publisher.js'), 'utf8');
  assert.doesNotMatch(pubJs, /Automotivo & Ferramentas/);
  assert.match(homeHtml, /Churrasco, Piscina & Lazer/);
});

test('importador uses 100% local TikTok Sans + iOS SF Pro fonts with zero Google Fonts', () => {
  const html = fs.readFileSync(path.join(process.cwd(), 'importador.html'), 'utf8');
  const css = fs.readFileSync(path.join(process.cwd(), 'css', 'studio-importador.css'), 'utf8');
  assert.doesNotMatch(html, /fonts\.googleapis\.com/);
  assert.match(css, /font-family:\s*'TikTokSans'/);
  assert.match(css, /tt-pro-400\.ttf/);
  assert.match(css, /tt-pro-500\.ttf/);
  assert.match(css, /tt-pro-600\.ttf/);
  assert.match(css, /SF-Pro-Display-Bold\.otf/);
});
