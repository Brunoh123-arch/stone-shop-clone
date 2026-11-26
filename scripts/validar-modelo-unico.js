const { renderProdutoHtml, listProductIds } = require('../api/_lib/render-produto');

const ids = listProductIds();
console.log(`🔍 Validando ${ids.length} produtos no Modelo Único Permanente...\n`);

let ok200 = 0;
let ok302 = 0;
let totalReviews = 0;
let totalVideos = 0;
const errors = [];

for (const id of ids) {
  const res = renderProdutoHtml(id);
  if (res.status === 302) {
    if (!res.redirect) errors.push(`produto-${id}: redirect sem destino`);
    else ok302++;
    continue;
  }
  if (res.status !== 200) {
    errors.push(`produto-${id}: status inesperado ${res.status}`);
    continue;
  }
  ok200++;
  const html = res.html;

  // 1. Zero placeholders sobrando
  const leftovers = html.match(/\{\{[A-Z0-9_]+\}\}/g);
  if (leftovers) errors.push(`produto-${id}: placeholders sobrando: ${leftovers.join(', ')}`);

  // 2. Banner Black Friday + CSS oficial presentes
  if (!html.includes('price-section-bf')) errors.push(`produto-${id}: falta price-section-bf`);
  if (!html.includes('ui-oficial.css')) errors.push(`produto-${id}: falta ui-oficial.css`);
  if (!html.includes('decalque-blackfriday.png')) errors.push(`produto-${id}: falta decalque-blackfriday.png`);

  // 3. Reviews count
  const revMatches = html.match(/class="review-card"/g) || [];
  totalReviews += revMatches.length;
  if (revMatches.length === 0) errors.push(`produto-${id}: 0 avaliações renderizadas`);

  // 4. Player 16:9 com bolinha e 4 cantos
  if (html.includes('id="tt-product-video"')) {
    totalVideos++;
    if (!html.includes('tt-progress-thumb')) errors.push(`produto-${id}: falta bolinha #tt-progress-thumb no player`);
    if (!html.includes('M4 9V5a1 1 0 0 1 1-1h4')) errors.push(`produto-${id}: falta SVG 4 cantos no fullscreen`);
  }

  // 5. Zero vazamento de Tipo de Fogão em 118, 119, 120, 122, 123
  if (['118', '119', '120', '122', '123'].includes(id) && /tipo de fog[aã]o/i.test(html)) {
    errors.push(`produto-${id}: ainda contém 'Tipo de Fogão'!`);
  }

  // 6. PRODUTO_ATUAL sintaticamente válido
  const m = html.match(/const PRODUTO_ATUAL = (\{[\s\S]*?\});/);
  if (!m) {
    errors.push(`produto-${id}: PRODUTO_ATUAL não encontrado`);
  } else {
    try {
      JSON.parse(m[1].replace(/\\u003c/g, '<'));
    } catch (e) {
      errors.push(`produto-${id}: PRODUTO_ATUAL JSON inválido: ${e.message}`);
    }
  }
}

console.log(`✅ Produtos 200 OK:     ${ok200}`);
console.log(`↪️  Redirects 302:       ${ok302}`);
console.log(`⭐ Total de avaliações: ${totalReviews} (esperado: 3316)`);
console.log(`🎬 Produtos com vídeo:  ${totalVideos}`);

if (totalReviews !== 3316) {
  errors.push(`Total de avaliações divergente: ${totalReviews} != 3316`);
}

if (errors.length > 0) {
  console.error(`\n❌ ${errors.length} ERRO(S) ENCONTRADO(S):`);
  errors.forEach((e) => console.error('  -', e));
  process.exit(1);
}

console.log(`\n🏆 VALIDAÇÃO 100% APROVADA — ZERO ERROS EM TODOS OS ${ok200} PRODUTOS!`);
