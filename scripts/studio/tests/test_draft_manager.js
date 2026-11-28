const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const {
  computeSweetSpotPix,
  sanitizeVariationName,
  createDraft,
  applyDraftPatch,
  popFromReserve,
  buildProductJsonFromDraft,
} = require('../draft-manager');

test('computeSweetSpotPix calibrates realistic PIX and anchor prices when user pastes only URL', () => {
  const low = computeSweetSpotPix(69.9);
  assert.ok(low.pix >= 24.89 && low.pix <= 39.9 && low.orig > low.pix * 2);
  const mid = computeSweetSpotPix(149.9);
  assert.ok(mid.pix >= 44.89 && mid.pix <= 59.9 && mid.orig > mid.pix * 2);
});

test('sanitizeVariationName strips commas and separator chars that break validar-modelo-unico.js', () => {
  assert.equal(sanitizeVariationName('Kit 4 Cores (Preto, Vinho, Cinza)'), 'Kit 4 Cores (Preto/ Vinho/ Cinza)');
});

test('popFromReserve moves pre-fetched videos, unboxings, and comments in 0ms and keeps rating_count synced', () => {
  const draft = createDraft({
    targetId: 998,
    product_title: 'Porta-Joias Rosa Eterna',
    price_pix: 49.89,
    price_original_num: 249.9,
    reserve_videos: [
      { id: 'v1', video: 'https://files.catbox.moe/v1.mp4', poster: '/p1.jpg', username: 'ana_br', name: 'Ana' },
      { id: 'v2', video: 'https://files.catbox.moe/v2.mp4', poster: '/p2.jpg', username: 'bia_br', name: 'Bia' }
    ],
    reserve_unboxings: [
      { id: 'u1', name: 'C**a M**s', stars: 5, date: '26/11', variation: 'Vermelho', comment: 'Lindo demais!', photos: ['/u1.jpg'] }
    ],
    reserve_reviews: [
      { id: 'r1', name: 'J**a P**a', stars: 5, date: '25/11', variation: 'Vermelho', comment: 'Amei o colar!', photos: [] }
    ]
  });

  const vRes = popFromReserve(draft.draftId, 'videos', 1);
  assert.equal(vRes.added.length, 1);
  assert.equal(vRes.remaining, 1);
  assert.equal(vRes.draft.creators.length, 1);

  const uRes = popFromReserve(draft.draftId, 'unboxings', 1);
  assert.equal(uRes.added.length, 1);
  assert.equal(uRes.draft.reviews.filter(r => r.photos && r.photos.length).length, 1);

  const patched = applyDraftPatch(draft.draftId, { product_title: 'Porta-Joias Luxo 100 Idiomas', price_pix: 44.89 });
  assert.equal(patched.livePatch.price_int, '44');
  assert.equal(patched.livePatch.price_cents, ',89');

  const built = buildProductJsonFromDraft(patched.draft);
  assert.equal(built.reviews_header, `Avaliações dos clientes (${built.rating_count.replace(/[()]/g, '')})`);
  assert.equal(built.produto_atual.preco, 44.89);
  assert.ok(built.description_html.replace(/<[^>]+>/g, '').trim().length >= 300);
  assert.doesNotMatch(built.description_html, /R\$\s*\d|\b\d+%\s*OFF\b/i);

  fs.rmSync(path.join(process.cwd(), '.studio-drafts', draft.draftId), { recursive: true, force: true });
});

test('composite review variations (Cor · Tamanho) and video id on set_desc_video are preserved', () => {
  const draft = createDraft({
    targetId: 995,
    product_title: 'Kit 4 Vestidos Teste',
    price_pix: 54.89,
    price_original_num: 239.9,
    variations: {
      cor: { com_imagem: true, label: 'Cor', opcoes: [{ nome: 'Preto', imagem: '/s1.webp' }] },
      tamanho: { com_imagem: false, label: 'Tamanho', opcoes: ['P', 'M', 'G'] },
    },
    creators: [{ id: 'vid_abc', video: 'https://files.catbox.moe/abc.mp4', poster: '/p.jpg', username: 'bia.real', name: 'Bia' }],
    reviews: [{ name: 'M**a S**a', stars: 5, date: '26/11', variation: 'Preto · M', comment: 'Ficou lindo demais!', photos: [] }],
  });

  const built = buildProductJsonFromDraft(draft);
  assert.equal(built.reviews[0].variation, 'Preto · M');

  const swapped = applyDraftPatch(draft.draftId, { action: 'set_desc_video', index: 0 });
  assert.equal(swapped.draft.video.id, 'vid_abc');

  fs.rmSync(path.join(process.cwd(), '.studio-drafts', draft.draftId), { recursive: true, force: true });
});
