const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { createDraft } = require('../draft-manager');
const { allocateVerifiedAvatars, publishDraft } = require('../publisher');

test('allocateVerifiedAvatars assigns unique Brazilian avatars with zero BAD_AVATARS', () => {
  const dummy = {
    reviews: Array.from({ length: 10 }, (_, i) => ({
      name: `M**a ${i}`,
      avatar: '',
      stars: 5,
      date: '25/11',
      variation: 'Preto',
      comment: 'Ótimo produto!',
      photos: [],
    })),
    creators: [],
  };
  const out = allocateVerifiedAvatars(dummy, 'feminino');
  const seen = new Set(out.reviews.map((r) => r.avatar));
  assert.equal(seen.size, 10);
  for (const av of seen) {
    assert.doesNotMatch(av, /tt_avatar_(5|9|11|12|13|17|19|29|31|37|39|43|57)\b/);
    assert.doesNotMatch(av, /tt_cdn_(2|3|4|5|10|13|14|15|19|21|22|23|27|28|30|34|35|41|44|45|51|58|66|68|69|70)\b/);
  }
});

test('publishDraft rolls back 100% cleanly when validar-modelo-unico.js rejects an incomplete draft', async () => {
  const beforeIndex = fs.readFileSync(path.join(process.cwd(), 'data/produtos/index.js'), 'utf8');
  const beforeHome = fs.readFileSync(path.join(process.cwd(), 'index.html'), 'utf8');

  const badDraft = createDraft({
    targetId: 997,
    product_title: 'Rascunho Incompleto Sem Unboxings Suficientes',
    price_pix: 39.89,
    price_original_num: 159.9,
    slides: [{ src: '../img/bolsa-155-slide-1.webp', alt: 'S1' }],
    reviews: [{ name: 'A**a B**a', stars: 5, date: '25/11', variation: 'Padrão Oficial', comment: 'Muito bom mesmo!', photos: [] }],
  });

  const res = await publishDraft(badDraft.draftId, { deploy: false });
  assert.equal(res.ok, false);
  assert.ok(Array.isArray(res.errors) && res.errors.length > 0);
  assert.equal(fs.existsSync(path.join(process.cwd(), 'data/produtos/produto-997.json')), false);
  assert.equal(fs.readFileSync(path.join(process.cwd(), 'data/produtos/index.js'), 'utf8'), beforeIndex);
  assert.equal(fs.readFileSync(path.join(process.cwd(), 'index.html'), 'utf8'), beforeHome);

  fs.rmSync(path.join(process.cwd(), '.studio-drafts', badDraft.draftId), { recursive: true, force: true });
});
