const test = require('node:test');
const assert = require('node:assert/strict');
const { renderProdutoHtml, renderProdutoFromData } = require('../../../api/_lib/render-produto');

test('renderProdutoFromData renders in-memory draft with studio live bridge without touching disk', () => {
  const sample = {
    id: 999,
    title: 'Produto Teste Studio - Stone Shop',
    meta_description: 'Desc teste',
    product_title: 'Kit Teste Instantâneo Zero Delay',
    slider_imgs: [{ src: '/.studio-drafts/d1/slide-1.webp', alt: 'Slide 1' }],
    discount_badge: '-75%',
    price_int: '49',
    price_cents: ',89',
    price_original: 'R$ 199,90',
    installment_text: '3x R$ 16,63',
    installment_highlight: 'sem juros',
    coupon_main: 'Economize R$ 150,01',
    rating_score: '4.9',
    rating_count: '(22)',
    sold_count: '3420 vendidos on-line',
    frete_original: 'R$ 22,90',
    reviews_header: 'Avaliações dos clientes (22)',
    reviews_avg: '4.9',
    reviews: [{ name: 'M**a S**a', avatar: '../img/reviews-avatars/mulheres_validadas/av1.jpg', stars: 5, date: '25/11', variation: 'Preto', date_line: '25/11 · Preto', comment: 'Chegou super rápido!', photos: [] }],
    details: [{ label: 'Material', value: 'ABS', hidden: false }],
    video: { src: 'https://files.catbox.moe/test01.mp4', poster: '/.studio-drafts/d1/poster.jpg', duration: '0:18', catbox_id: 'test01.mp4' },
    size_guide_html: '',
    description_html: '<p>Descrição real do produto.</p>',
    related: [],
    produto_atual: { id: 999, nome: 'Kit Teste Instantâneo Zero Delay', preco: 49.89, preco_antigo: 199.9, imagens: ['/.studio-drafts/d1/slide-1.webp'] },
    extra_scripts: [],
    creator_context: 'casa',
    creators: []
  };

  const res = renderProdutoFromData(sample, { studioPreview: true });
  assert.equal(res.status, 200);
  assert.match(res.html, /Kit Teste Instantâneo Zero Delay/);
  assert.match(res.html, /id="studio-live-bridge"/);
  assert.match(res.html, /STUDIO_LIVE_PATCH/);

  const prod155 = renderProdutoHtml('155');
  assert.equal(prod155.status, 200);
  assert.doesNotMatch(prod155.html, /id="studio-live-bridge"/);
});
