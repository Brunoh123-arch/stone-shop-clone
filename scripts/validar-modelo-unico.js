const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { renderProdutoHtml, listProductIds } = require('../api/_lib/render-produto');

const ROOT = path.join(__dirname, '..');
const NEW_MIN_ID = 125; // produtos >= 125 passam pelas travas ESTRITAS de mídia
const BAD_AVATAR_DIRS = ['reviews-avatars/unique', 'reviews-avatars/curated'];
// Avatares inspecionados no olho: logos de loja / desenho / cartoon (PROIBIDO em produto novo)
const BAD_AVATARS = new Set([
  'tt_avatar_5', 'tt_avatar_9', 'tt_avatar_11', 'tt_avatar_12', 'tt_avatar_13', 'tt_avatar_17', 'tt_avatar_19',
  'tt_avatar_29', 'tt_avatar_31', 'tt_avatar_37', 'tt_avatar_39', 'tt_avatar_43', 'tt_avatar_57',
  'tt_cdn_2', 'tt_cdn_3', 'tt_cdn_4', 'tt_cdn_5', 'tt_cdn_10', 'tt_cdn_13', 'tt_cdn_14', 'tt_cdn_15',
  'tt_cdn_19', 'tt_cdn_21', 'tt_cdn_22', 'tt_cdn_23', 'tt_cdn_27', 'tt_cdn_30',
  'tt_cdn_28', 'tt_cdn_34', 'tt_cdn_35', 'tt_cdn_41', 'tt_cdn_44', 'tt_cdn_45',
  'tt_cdn_51', 'tt_cdn_58', 'tt_cdn_66', 'tt_cdn_68', 'tt_cdn_69', 'tt_cdn_70',
]);
const COMMERCIAL_CREATOR = /(shop|store|loja|oficial|official|ofertas|achadinhos|outlet|magazine|brasil|brazil|tech)/i;

const ids = listProductIds();
console.log(`🔍 Validando ${ids.length} produtos no Modelo Único Permanente...\n`);

let ok200 = 0;
let ok302 = 0;
let totalReviews = 0;
let totalVideos = 0;
const errors = [];
const warnings = [];

// ---------- 1. Renderização (todos os produtos) ----------
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

  const leftovers = html.match(/\{\{[A-Z0-9_]+\}\}/g);
  if (leftovers) errors.push(`produto-${id}: placeholders sobrando: ${leftovers.join(', ')}`);

  if (!html.includes('price-section-bf')) errors.push(`produto-${id}: falta price-section-bf`);
  if (!html.includes('ui-oficial.css')) errors.push(`produto-${id}: falta ui-oficial.css`);
  if (!html.includes('decalque-blackfriday.png')) errors.push(`produto-${id}: falta decalque-blackfriday.png`);
  if (/\d+(?:[.,]\d+)?\s*K\s*vendido/i.test(html)) errors.push(`produto-${id}: ainda contém contador abreviado com 'K' em vendidos`);
  const instBlock = (html.match(/<div class="installment-row"[\s\S]*?<\/div>/i) || [''])[0];
  if (/sem\s+juros[\s\S]*sem\s+juros/i.test(instBlock)) errors.push(`produto-${id}: 'sem juros' duplicado na linha de parcelamento`);
  if (/\dx\s+de\s+R\$/i.test(instBlock)) errors.push(`produto-${id}: parcelamento ainda contém 'de' (deve ser '3x R$ XX,XX sem juros')`);

  const revMatches = html.match(/class="review-card"/g) || [];
  totalReviews += revMatches.length;
  if (revMatches.length === 0) errors.push(`produto-${id}: 0 avaliações renderizadas`);

  if (html.includes('id="tt-product-video"')) {
    totalVideos++;
    if (!html.includes('tt-progress-thumb')) errors.push(`produto-${id}: falta bolinha #tt-progress-thumb no player`);
    if (!html.includes('M4 9V5a1 1 0 0 1 1-1h4')) errors.push(`produto-${id}: falta SVG 4 cantos no fullscreen`);
  }

  if (['118', '119', '120', '122', '123'].includes(id) && /tipo de fog[aã]o/i.test(html)) {
    errors.push(`produto-${id}: ainda contém 'Tipo de Fogão'!`);
  }

  // Travas globais de Descrição e Guia de Tamanhos (todos os 70 produtos ativos)
  const rawJsonPath = path.join(ROOT, 'data', 'produtos', `produto-${id}.json`);
  if (fs.existsSync(rawJsonPath)) {
    try {
      const pj = JSON.parse(fs.readFileSync(rawJsonPath, 'utf8'));
      const descHtml = String(pj.description_html || '');
      const descPlain = descHtml.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      if (descPlain.length < 300) {
        errors.push(`produto-${id}: description_html muito curta (${descPlain.length} chars < 300)`);
      }
      if (/R\$\s*\d|\b\d+%\s*OFF\b/i.test(descPlain)) {
        errors.push(`produto-${id}: PROIBIDO mencionar valor 'R$' ou '% OFF' dentro de description_html`);
      }
      const APPAREL_IDS = new Set([74, 75, 87, 88, 99, 103, 104, 106, 110, 132, 136, 137, 138, 140, 141, 143]);
      const hasSg = String(pj.size_guide_html || '').trim().length > 0;
      if (hasSg && !APPAREL_IDS.has(Number(id))) {
        errors.push(`produto-${id}: size_guide_html proibido em produto que não é vestuário/calçado/cinta`);
      }
    } catch (e) {}
  }

  const m = html.match(/const PRODUTO_ATUAL = (\{[\s\S]*?\});/);
  if (!m) {
    errors.push(`produto-${id}: PRODUTO_ATUAL não encontrado`);
  } else {
    try {
      const pa = JSON.parse(m[1].replace(/\\u003c/g, '<'));
      if (!(Number(pa.preco) > 0)) errors.push(`produto-${id}: PRODUTO_ATUAL sem 'preco' numérico (carrinho/checkout quebram)`);
    } catch (e) {
      errors.push(`produto-${id}: PRODUTO_ATUAL JSON inválido: ${e.message}`);
    }
  }
}

// ---------- 2. Travas de mídia (cross-produto) ----------
const catboxId = (u) => { const m = String(u || '').match(/catbox\.moe\/([a-z0-9]+\.\w+)/i); return m ? m[1].toLowerCase() : null; };
const clean = (p) => String(p || '').split('?')[0].split('#')[0];
const toAbs = (p) => path.join(ROOT, clean(p).replace(/^(\.\.\/|\.\/|\/)+/, ''));
const onDisk = (p) => fs.existsSync(toAbs(p));
const md5Cache = new Map();
const avatarFingerprint = (p) => {
  const c = clean(p);
  if (!c) return '';
  if (/^https?:\/\//i.test(c)) return c;
  const abs = toAbs(c);
  if (!fs.existsSync(abs)) return c;
  if (!md5Cache.has(abs)) {
    md5Cache.set(abs, crypto.createHash('md5').update(fs.readFileSync(abs)).digest('hex'));
  }
  return md5Cache.get(abs);
};

const owners = new Map(); // catbox_id -> [ids de produtos que usam]
const products = {};
for (const id of ids) {
  const f = path.join(ROOT, 'data', 'produtos', `produto-${id}.json`);
  if (!fs.existsSync(f)) continue;
  let d;
  try { d = JSON.parse(fs.readFileSync(f, 'utf8')); } catch (e) { errors.push(`produto-${id}: JSON ilegível`); continue; }
  if (d.redirect) continue;
  products[id] = d;
  const vids = [];
  if (d.video && d.video.src) vids.push(catboxId(d.video.src));
  (d.creators || []).forEach((c) => vids.push(catboxId(c.video)));
  new Set(vids.filter(Boolean)).forEach((v) => {
    if (!owners.has(v)) owners.set(v, []);
    owners.get(v).push(id);
  });
}

for (const id of ids) {
  const d = products[id];
  if (!d || Number(id) < NEW_MIN_ID) continue;
  const E = (msg) => errors.push(`produto-${id}: ${msg}`);
  const W = (msg) => warnings.push(`produto-${id}: ${msg}`);

  // 2.1 vídeos exclusivos do produto (nunca reaproveitar MP4 de outro produto)
  const mine = [];
  if (d.video && d.video.src) mine.push(['descrição', catboxId(d.video.src)]);
  (d.creators || []).forEach((c, i) => mine.push([`criador ${i + 1}`, catboxId(c.video)]));
  const seen = new Set();
  for (const [where, v] of mine) {
    if (!v) { E(`${where} sem URL Catbox válida`); continue; }
    if (seen.has(v)) E(`vídeo ${v} repetido dentro do próprio produto (${where})`);
    seen.add(v);
    const other = (owners.get(v) || []).filter((x) => String(x) !== String(id));
    if (other.length) E(`vídeo ${v} (${where}) já pertence ao(s) produto(s) ${other.join(', ')} — PROIBIDO reaproveitar mídia de outro produto`);
  }

  // 2.2 vídeo da descrição obrigatório + poster
  if (!d.video || !d.video.src) E('sem vídeo na descrição (#tt-product-video obrigatório)');
  else if (!onDisk(d.video.poster)) E(`poster da descrição não existe no disco: ${d.video.poster}`);

  // 2.3 criadores
  const creators = d.creators || [];
  if (creators.length === 0) E('sem criadores');
  if (creators.length < 8) W(`apenas ${creators.length} criadores (meta: 8 a 15)`);
  const users = new Set();
  const creatorAvFingerprints = new Set();
  creators.forEach((c, i) => {
    const tag = `criador ${i + 1} (@${c.username})`;
    if (users.has(c.username)) E(`${tag}: @username repetido`);
    users.add(c.username);
    if (COMMERCIAL_CREATOR.test(`${c.name} ${c.username}`)) E(`${tag}: perfil comercial/loja proibido`);
    if (!onDisk(c.avatar)) E(`${tag}: avatar não existe no disco ${c.avatar}`);
    const fp = avatarFingerprint(c.avatar);
    if (fp && creatorAvFingerprints.has(fp)) E(`${tag}: avatar repetido entre criadores do mesmo produto (${c.avatar})`);
    if (fp) creatorAvFingerprints.add(fp);
    if (!onDisk(c.poster)) E(`${tag}: poster não existe no disco ${c.poster}`);
    if (clean(c.poster).includes('catalogo') || /slide/i.test(clean(c.poster))) E(`${tag}: poster parece foto de catálogo (deve ser frame do MP4)`);
  });

  // 2.4 slider + variações
  (d.slider_imgs || []).forEach((s) => { if (!onDisk(s.src)) E(`slide não existe no disco: ${s.src}`); });
  if ((d.slider_imgs || []).length < 4) E('slider com menos de 4 fotos');
  const varNames = [];
  const varImgs = new Set();
  const vars = (d.produto_atual && d.produto_atual.variacoes) || {};
  Object.values(vars).forEach((g) => {
    (g.opcoes || []).forEach((o) => {
      if (typeof o === 'string') { varNames.push(o.toLowerCase()); return; }
      varNames.push(String(o.nome).toLowerCase());
      if (o.imagem) {
        if (!onDisk(o.imagem)) E(`imagem de variação não existe: ${o.imagem}`);
        if (varImgs.has(clean(o.imagem))) E(`imagem de variação repetida para cores diferentes: ${o.imagem}`);
        varImgs.add(clean(o.imagem));
      }
    });
  });

  // 2.5 avaliações
  const revCount = (d.reviews || []).length;
  if (revCount < 20) W(`apenas ${revCount} avaliações cadastradas (meta: 20+ para prova social forte)`);
  const rcMatch = String(d.rating_count || '').match(/\d+/);
  const rhMatch = String(d.reviews_header || '').match(/\d+/);
  if (rcMatch && rhMatch && rcMatch[0] !== rhMatch[0]) {
    E(`reviews_header '${d.reviews_header}' diverge de rating_count '${d.rating_count}' (js/app.js sobrescreve o topo!)`);
  }
  const photoSeen = new Set();
  const avSeen = new Set();
  (d.reviews || []).forEach((r, i) => {
    const tag = `avaliação ${i + 1} (${r.name})`;
    const av = clean(r.avatar);
    const avFp = avatarFingerprint(r.avatar);
    if (!onDisk(av)) E(`${tag}: avatar não existe ${r.avatar}`);
    if (BAD_AVATAR_DIRS.some((b) => av.includes(b))) E(`${tag}: avatar em pasta banida (gringos): ${av}`);
    const base = path.basename(av, path.extname(av));
    if (BAD_AVATARS.has(base)) E(`${tag}: avatar ${base} é logo/cartoon (proibido)`);
    if (creatorAvFingerprints.has(avFp)) E(`${tag}: avatar colide (mesmo rosto/MD5) com criador do carrossel de vídeos (${av})`);
    if (avSeen.has(avFp)) E(`${tag}: avatar repetido (mesmo rosto/MD5) dentro das avaliações (${av})`);
    avSeen.add(avFp);
    if (varNames.length && r.variation && !varNames.includes(String(r.variation).toLowerCase())) {
      E(`${tag}: variação '${r.variation}' não existe na grade do produto`);
    }
    (r.photos || []).forEach((p) => {
      if (!onDisk(p)) E(`${tag}: foto não existe ${p}`);
      if (photoSeen.has(clean(p))) E(`${tag}: foto de unboxing repetida ${p}`);
      photoSeen.add(clean(p));
    });
  });
  const withPhoto = (d.reviews || []).filter((r) => (r.photos || []).length > 0).length;
  if (withPhoto < 6) W(`apenas ${withPhoto} avaliações com foto de unboxing (meta: 6+)`);

  // 2.6 catálogo
  const cat = fs.readFileSync(path.join(ROOT, 'js', 'catalogo.js'), 'utf8');
  if (!new RegExp(`\\{id:${id},`).test(cat)) E('não registrado em js/catalogo.js');
}

// 2.7 Garantir que nenhum produto redirecionado (302) sobrou listado na vitrine (catalogo.js / index.html)
const catSrc = fs.readFileSync(path.join(ROOT, 'js', 'catalogo.js'), 'utf8');
const idxSrc = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');
for (const id of ids) {
  const f = path.join(ROOT, 'data', 'produtos', `produto-${id}.json`);
  if (!fs.existsSync(f)) continue;
  const d = JSON.parse(fs.readFileSync(f, 'utf8'));
  if (!d.redirect) continue;
  if (new RegExp(`\\{id:${id},`).test(catSrc)) errors.push(`produto-${id}: é redirect (${d.redirect}) mas ainda aparece em js/catalogo.js`);
  if (new RegExp(`data-id="${id}"`).test(idxSrc)) errors.push(`produto-${id}: é redirect (${d.redirect}) mas ainda aparece em index.html`);
}

// ---------- 3. Relatório ----------
const legacyBad = Object.entries(products).filter(([id, d]) => Number(id) < NEW_MIN_ID &&
  (d.reviews || []).some((r) => BAD_AVATARS.has(path.basename(clean(r.avatar), path.extname(clean(r.avatar)))) ||
    BAD_AVATAR_DIRS.some((b) => clean(r.avatar).includes(b)))).length;

console.log(`✅ Produtos 200 OK:     ${ok200}`);
console.log(`↪️  Redirects 302:       ${ok302}`);
console.log(`⭐ Total de avaliações: ${totalReviews}`);
console.log(`🎬 Produtos com vídeo:  ${totalVideos}`);
if (legacyBad) console.log(`ℹ️  ${legacyBad} produtos antigos (< ${NEW_MIN_ID}) ainda usam avatar de logo/cartoon — fila de correção.`);

if (warnings.length) {
  console.warn(`\n⚠️  ${warnings.length} AVISO(S) (não bloqueiam):`);
  warnings.forEach((w) => console.warn('  -', w));
}

const minExpectedReviews = ok200 * 25;
if (totalReviews < minExpectedReviews) errors.push(`Total de avaliações caiu para ${totalReviews} (< ${minExpectedReviews} para ${ok200} produtos ativos) — algo foi apagado`);

if (errors.length > 0) {
  console.error(`\n❌ ${errors.length} ERRO(S) ENCONTRADO(S):`);
  errors.forEach((e) => console.error('  -', e));
  process.exit(1);
}

console.log(`\n🏆 VALIDAÇÃO APROVADA — ZERO ERROS EM ${ok200} PRODUTOS (travas estritas de mídia ativas para ids >= ${NEW_MIN_ID})!`);
