const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { createDraft } = require('../draft-manager');
const { handleStudioRequest } = require('../studio-api');

test('studio-api enforces STUDIO_TOKEN (401 without key) and serves preview + 0ms reserve expansion with key', async () => {
  process.env.STUDIO_MODE = '1';
  process.env.STUDIO_TOKEN = 'test_secret_token_123';

  const draft = createDraft({
    targetId: 996,
    product_title: 'Maleta Maquiagem Completa',
    price_pix: 47.89,
    price_original_num: 239.9,
    reserve_reviews: [{ id: 'r1', name: 'L**a C**a', stars: 5, date: '26/11', variation: 'Rosa', comment: 'Maleta linda demais!', photos: [] }],
  });

  const srv = http.createServer((req, res) => {
    if (!handleStudioRequest(req, res)) {
      res.writeHead(404);
      res.end('not studio');
    }
  });

  await new Promise((resolve) => srv.listen(0, '127.0.0.1', resolve));
  const port = srv.address().port;

  const unauth = await fetch(`http://127.0.0.1:${port}/importador`);
  assert.equal(unauth.status, 401);

  const authPage = await fetch(`http://127.0.0.1:${port}/importador?key=test_secret_token_123`);
  assert.equal(authPage.status, 200);
  const cookie = authPage.headers.get('set-cookie') || '';
  assert.match(cookie, /studio_key=test_secret_token_123/);

  const preview = await fetch(`http://127.0.0.1:${port}/api/studio/preview/${draft.draftId}?owner=1`, {
    headers: { Cookie: 'studio_key=test_secret_token_123' },
  });
  assert.equal(preview.status, 200);
  const html = await preview.text();
  assert.match(html, /Maleta Maquiagem Completa/);
  assert.match(html, /STUDIO_LIVE_PATCH/);

  const more = await fetch(`http://127.0.0.1:${port}/api/studio/draft/${draft.draftId}/more`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-studio-key': 'test_secret_token_123' },
    body: JSON.stringify({ kind: 'reviews', count: 1 }),
  });
  assert.equal(more.status, 200);
  const moreJson = await more.json();
  assert.equal(moreJson.added.length, 1);

  srv.close();
  fs.rmSync(path.join(process.cwd(), '.studio-drafts', draft.draftId), { recursive: true, force: true });
});
