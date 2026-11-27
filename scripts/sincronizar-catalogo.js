const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const PRODS_DIR = path.join(ROOT, 'data', 'produtos');
const REGISTRY_PATH = path.join(ROOT, 'data', 'catbox-registry.json');
const ADMIN_360_PATH = path.join(ROOT, 'data', 'admin-catalogo-360.json');

function cleanCatboxBase(url) {
  if (!url || typeof url !== 'string') return '';
  return url.split('#')[0].split('?')[0].trim();
}

function slugifyShort(str) {
  return String(str || 'produto')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 32) || 'produto';
}

function inferCategory(title) {
  const t = String(title || '').toLowerCase();
  if (/iphone|samsung|galaxy|xiaomi|poco|tablet|smartwatch|watch|tv |smart tv|jbl|aiwa|caixa de som|karaok|projetor|starlink|alexa|alaxe|echo|switch|arcade|c[aâ]mera/.test(t)) return 'Eletrônicos';
  if (/vestido|chinelo|sand[aá]lia|t[eê]nis|camiseta|cinta|body|bolsa|cal[cç]a|short/.test(t)) return 'Moda & Calçados';
  if (/escova|secador|prancha|modelador|sobrancelha|depilador|lattafa|perfume|maquiagem/.test(t)) return 'Beleza & Perfumes';
  if (/infantil|patinete|triciclo|carrinho|livro|fralda|patinho|beb[eê]|crian[cç]a/.test(t)) return 'Infantil & Brinquedos';
  if (/piscina|praia|bike|bicicleta|bola|colch[aã]o|churrasqueira|cadeira|mala|scooter|pneu/.test(t)) return 'Lazer & Viagem';
  return 'Casa & Cozinha';
}

const files = fs.readdirSync(PRODS_DIR)
  .filter((f) => /^produto-\d+\.json$/.test(f))
  .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));

// 1. Reconstrói data/catbox-registry.json diretamente da Fonte Única (data/produtos/*.json)
const registry = {
  version: '2.0.0',
  updated_at: new Date().toISOString(),
  description: 'Livro-Razão Oficial Anti-Conflito Catbox — Gerado diretamente de data/produtos/*.json.',
  videos: {},
  conflicts_detected: [],
  stats: {},
};

const rawProducts = [];
let totalDescVideos = 0;
let totalCreatorSlots = 0;
let productsWithCreators = 0;

for (const f of files) {
  const d = JSON.parse(fs.readFileSync(path.join(PRODS_DIR, f), 'utf8'));
  if (d.redirect) continue;
  rawProducts.push(d);

  const pid = Number(d.id);
  const title = d.product_title || (d.produto_atual && d.produto_atual.nome) || d.title || `Produto #${pid}`;
  const slug = slugifyShort(title);

  if (d.video && d.video.src) {
    const base = cleanCatboxBase(d.video.src);
    if (base.includes('catbox.moe')) {
      totalDescVideos++;
      const cid = path.basename(base);
      const tagged = `${base}#prod=${pid}&slot=descricao&slug=${slug}`;
      if (registry.videos[base] && registry.videos[base].owner_product_id !== pid) {
        registry.conflicts_detected.push({
          url: base,
          first_owner: registry.videos[base].owner_product_id,
          also_used_in: pid,
          slot: 'descricao',
        });
      } else if (!registry.videos[base]) {
        registry.videos[base] = {
          catbox_id: cid,
          base_url: base,
          tagged_url: tagged,
          owner_product_id: pid,
          owner_product_title: title,
          slot: 'descricao',
          poster: (d.video.poster || '').replace(/^\.\.\//, ''),
        };
      }
    }
  }

  const creators = Array.isArray(d.creators) ? d.creators : [];
  if (creators.length > 0) productsWithCreators++;
  creators.forEach((c, idx) => {
    const base = cleanCatboxBase(c && c.video);
    if (!base || !base.includes('catbox.moe')) return;
    totalCreatorSlots++;
    const cid = path.basename(base);
    const slot = `criador_${idx + 1}`;
    const tagged = `${base}#prod=${pid}&slot=${slot}&slug=${slug}`;
    if (registry.videos[base] && registry.videos[base].owner_product_id !== pid) {
      registry.conflicts_detected.push({
        url: base,
        first_owner: registry.videos[base].owner_product_id,
        also_used_in: pid,
        slot,
      });
    } else if (!registry.videos[base]) {
      registry.videos[base] = {
        catbox_id: cid,
        base_url: base,
        tagged_url: tagged,
        owner_product_id: pid,
        owner_product_title: title,
        slot,
        creator_username: c.username || '',
        poster: (c.poster || '').replace(/^\.\.\//, ''),
      };
    }
  });
}

registry.stats = {
  total_unique_catbox_videos: Object.keys(registry.videos).length,
  total_desc_videos: totalDescVideos,
  total_creator_videos_slots: totalCreatorSlots,
  products_with_creators: productsWithCreators,
  conflicts_count: registry.conflicts_detected.length,
};

fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2), 'utf8');

// 2. Reconstrói data/admin-catalogo-360.json (ordenado dos mais recentes para os mais antigos)
const conflictPids = new Set();
for (const c of registry.conflicts_detected) {
  conflictPids.add(Number(c.first_owner));
  conflictPids.add(Number(c.also_used_in));
}

const adminItems = [];
for (const d of rawProducts) {
  const pid = Number(d.id);
  const pa = d.produto_atual || {};
  const slides = d.slider_imgs || [];
  const creators = d.creators || [];
  const reviews = d.reviews || [];
  const reviewsWithPhotos = reviews.filter((r) => Array.isArray(r.photos) && r.photos.length > 0);
  const hasConflict = conflictPids.has(pid);

  let score = 0;
  const alerts = [];
  if (slides.length >= 4) score += 25;
  else if (slides.length >= 3) { score += 18; alerts.push(`Apenas ${slides.length} slides (ideal: 4+)`); }
  else alerts.push(`Poucos slides (${slides.length})`);

  if (d.video && d.video.src) score += 25;
  else alerts.push('Sem vídeo na descrição');

  if (creators.length >= 8) score += 25;
  else if (creators.length >= 4) { score += 20; alerts.push(`${creators.length} criadores (meta: 8+)`); }
  else if (creators.length >= 1) { score += 15; alerts.push(`${creators.length} criadores (meta: 8+)`); }
  else alerts.push('Sem vídeos de criadores');

  if (reviewsWithPhotos.length >= 6 && !hasConflict) score += 25;
  else if (reviewsWithPhotos.length >= 3 && !hasConflict) { score += 22; }
  else {
    if (reviewsWithPhotos.length > 0) score += 15;
    else alerts.push('Sem fotos de unboxing');
    if (hasConflict) alerts.push('Vídeo Catbox compartilhado com outro produto');
  }

  const title = d.product_title || pa.nome || d.title || `Produto #${pid}`;
  const precoNum = Number(pa.preco || 0);
  const precoOrigNum = Number(pa.preco_antigo || pa.precoOrig || 0) ||
    parseFloat(String(d.price_original || '').replace(/[^\d.,]/g, '').replace(/\./g, '').replace(',', '.')) || 0;
  const calcDesc = precoOrigNum > precoNum && precoNum > 0
    ? Math.round(((precoOrigNum - precoNum) / precoOrigNum) * 100)
    : parseInt(String(d.discount_badge || '').replace(/\D/g, ''), 10) || 0;

  adminItems.push({
    id: pid,
    title,
    slug: slugifyShort(title),
    category: inferCategory(title),
    is_new_bf: pid >= 126,
    preco: precoNum,
    preco_antigo: precoOrigNum,
    price_original_str: d.price_original || (precoOrigNum ? `R$ ${precoOrigNum.toFixed(2).replace('.', ',')}` : ''),
    discount_badge: d.discount_badge || (calcDesc ? `-${calcDesc}%` : ''),
    discount_pct: calcDesc,
    installment_text: d.installment_text || '',
    sold_count: d.sold_count || '',
    rating_score: d.rating_score || '4.9',
    img: (pa.img || (slides[0] && slides[0].src) || '').replace(/^\.\.\//, ''),
    slides: slides.map((s) => ({ src: (s.src || '').replace(/^\.\.\//, ''), alt: s.alt || '' })),
    variacoes: pa.variacoes || {},
    video: d.video ? {
      src: cleanCatboxBase(d.video.src).replace(/^\.\.\//, ''),
      tagged_src: (d.video.src || '').replace(/^\.\.\//, ''),
      poster: (d.video.poster || '').replace(/^\.\.\//, ''),
      duration: d.video.duration || '',
      catbox_id: d.video.catbox_id || path.basename(cleanCatboxBase(d.video.src || '')),
    } : null,
    creators_count: creators.length,
    creators: creators.map((c) => ({
      name: c.name || 'Criador',
      username: c.username || '',
      avatar: (c.avatar || '').replace(/^\.\.\//, ''),
      poster: (c.poster || '').replace(/^\.\.\//, ''),
      video: cleanCatboxBase(c.video || '').replace(/^\.\.\//, ''),
      tagged_video: (c.video || '').replace(/^\.\.\//, ''),
      catbox_id: c.catbox_id || path.basename(cleanCatboxBase(c.video || '')),
      likes: c.likes || 0,
      description: c.description || '',
    })),
    details: d.details || [],
    description_html: (d.description_html || '').replace(/\.\.\/img\//g, 'img/'),
    size_guide_html: (d.size_guide_html || '').replace(/\.\.\/img\//g, 'img/'),
    reviews_count: reviews.length,
    reviews_photos_count: reviewsWithPhotos.reduce((acc, r) => acc + r.photos.length, 0),
    reviews: reviews.map((r) => ({
      name: r.name,
      avatar: (r.avatar || '').replace(/^\.\.\//, ''),
      stars: r.stars,
      date_line: r.date_line,
      variation: r.variation,
      comment: r.comment,
      photos: (r.photos || []).map((ph) => ph.replace(/^\.\.\//, '')),
    })),
    health_score: score,
    has_catbox_conflict: hasConflict,
    alerts,
  });
}

// Ordena mais recentes primeiro (#154 -> #4) para destacar lançamentos no painel
adminItems.sort((a, b) => b.id - a.id);

const summary = {
  generated_at: new Date().toISOString(),
  total_products: adminItems.length,
  total_slides: adminItems.reduce((a, x) => a + x.slides.length, 0),
  total_desc_videos: adminItems.filter((x) => x.video && x.video.src).length,
  total_creators_videos: adminItems.reduce((a, x) => a + x.creators_count, 0),
  total_ads_videos: adminItems.reduce((a, x) => a + (x.video && x.video.src ? 1 : 0) + x.creators_count, 0),
  total_reviews: adminItems.reduce((a, x) => a + x.reviews_count, 0),
  total_unboxing_photos: adminItems.reduce((a, x) => a + x.reviews_photos_count, 0),
  avg_health_score: Math.round(adminItems.reduce((a, x) => a + x.health_score, 0) / (adminItems.length || 1)),
  catbox_stats: registry.stats,
  catbox_conflicts: registry.conflicts_detected,
  products: adminItems,
};

fs.writeFileSync(ADMIN_360_PATH, JSON.stringify(summary), 'utf8');
console.log(`✅ data/catbox-registry.json atualizado (${registry.stats.total_unique_catbox_videos} vídeos únicos, ${registry.stats.conflicts_count} conflitos).`);
console.log(`✅ data/admin-catalogo-360.json gerado (${(fs.statSync(ADMIN_360_PATH).size / 1024).toFixed(0)} KB, ${adminItems.length} produtos, ${summary.total_ads_videos} vídeos Ads, Score médio: ${summary.avg_health_score}%).`);
