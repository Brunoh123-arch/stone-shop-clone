const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const PRODS_DIR = path.join(ROOT, 'data', 'produtos');
const REGISTRY_PATH = path.join(ROOT, 'data', 'catbox-registry.json');
const ADMIN_360_PATH = path.join(ROOT, 'data', 'admin-catalogo-360.json');
const CATALOGO_JS_PATH = path.join(ROOT, 'js', 'catalogo.js');

const registry = fs.existsSync(REGISTRY_PATH)
  ? JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'))
  : { videos: {}, conflicts_detected: [] };

const conflictPids = new Set();
for (const c of (registry.conflicts_detected || [])) {
  conflictPids.add(Number(c.first_owner));
  conflictPids.add(Number(c.also_used_in));
}

const files = fs.readdirSync(PRODS_DIR)
  .filter((f) => /^produto-\d+\.json$/.test(f))
  .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));

const adminItems = [];
const byIdMap = new Map();

for (const f of files) {
  const d = JSON.parse(fs.readFileSync(path.join(PRODS_DIR, f), 'utf8'));
  if (d.redirect) continue;

  const pid = Number(d.id);
  const pa = d.produto_atual || {};
  const slides = d.slider_imgs || [];
  const creators = d.creators || [];
  const reviews = d.reviews || [];
  const reviewsWithPhotos = reviews.filter((r) => Array.isArray(r.photos) && r.photos.length > 0);
  const hasConflict = conflictPids.has(pid);

  // Cálculo objetivo do Score de Saúde (0 a 100%)
  let score = 0;
  const alerts = [];
  if (slides.length >= 4) score += 25;
  else if (slides.length >= 3) { score += 18; alerts.push(`Apenas ${slides.length} slides (ideal: 4+)`); }
  else alerts.push(`Poucos slides (${slides.length})`);

  if (d.video && d.video.src) score += 25;
  else alerts.push('Sem vídeo na descrição');

  if (creators.length >= 10) score += 25;
  else if (creators.length >= 1) { score += 15; alerts.push(`${creators.length} vídeos de criadores (meta: 10–30+)`); }
  else alerts.push('Sem vídeos de criadores');

  if (reviewsWithPhotos.length >= 3 && !hasConflict) score += 25;
  else {
    if (reviewsWithPhotos.length > 0) score += 15;
    else alerts.push('Sem fotos de unboxing');
    if (hasConflict) alerts.push('Vídeo Catbox compartilhado com outro produto');
  }

  byIdMap.set(pid, d);

  adminItems.push({
    id: pid,
    title: d.product_title || pa.nome || d.title,
    preco: Number(pa.preco || 0),
    preco_antigo: Number(pa.preco_antigo || 0) || d.price_original || '',
    price_original_str: d.price_original || '',
    discount_badge: d.discount_badge || '',
    installment_text: d.installment_text || '',
    sold_count: d.sold_count || '',
    rating_score: d.rating_score || '4.8',
    img: (pa.img || (slides[0] && slides[0].src) || '').replace(/^\.\.\//, ''),
    slides: slides.map((s) => ({ src: (s.src || '').replace(/^\.\.\//, ''), alt: s.alt || '' })),
    variacoes: pa.variacoes || {},
    video: d.video ? {
      src: (d.video.src || '').replace(/^\.\.\//, ''),
      poster: (d.video.poster || '').replace(/^\.\.\//, ''),
      duration: d.video.duration || '',
      catbox_id: d.video.catbox_id || '',
    } : null,
    creators_count: creators.length,
    creators: creators.map((c) => ({
      name: c.name,
      username: c.username,
      avatar: (c.avatar || '').replace(/^\.\.\//, ''),
      poster: (c.poster || '').replace(/^\.\.\//, ''),
      video: (c.video || '').replace(/^\.\.\//, ''),
      catbox_id: c.catbox_id || '',
      likes: c.likes,
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

// Sincroniza preços e imagens principais em js/catalogo.js sem quebrar categorias/estrutura existente
if (fs.existsSync(CATALOGO_JS_PATH)) {
  let catTxt = fs.readFileSync(CATALOGO_JS_PATH, 'utf8');
  let syncedCount = 0;
  catTxt = catTxt.replace(/(\{\s*["']?id["']?\s*:\s*(\d+)[\s\S]*?\n\s*\})/g, (block, _full, idStr) => {
    const pid = Number(idStr);
    const srcProd = byIdMap.get(pid);
    if (!srcProd || !srcProd.produto_atual) return block;
    const officialPrice = Number(srcProd.produto_atual.preco);
    if (officialPrice > 0) {
      const updated = block.replace(/(["']?preco["']?\s*:\s*)[0-9]+(?:\.[0-9]+)?/, `$1${officialPrice}`);
      if (updated !== block) syncedCount++;
      return updated;
    }
    return block;
  });
  fs.writeFileSync(CATALOGO_JS_PATH, catTxt, 'utf8');
  console.log(`✅ js/catalogo.js sincronizado (${syncedCount} preços alinhados com data/produtos/).`);
}

const summary = {
  generated_at: new Date().toISOString(),
  total_products: adminItems.length,
  total_slides: adminItems.reduce((a, x) => a + x.slides.length, 0),
  total_creators_videos: adminItems.reduce((a, x) => a + x.creators_count, 0),
  total_reviews: adminItems.reduce((a, x) => a + x.reviews_count, 0),
  total_unboxing_photos: adminItems.reduce((a, x) => a + x.reviews_photos_count, 0),
  avg_health_score: Math.round(adminItems.reduce((a, x) => a + x.health_score, 0) / (adminItems.length || 1)),
  catbox_stats: registry.stats || {},
  catbox_conflicts: registry.conflicts_detected || [],
  products: adminItems,
};

fs.writeFileSync(ADMIN_360_PATH, JSON.stringify(summary), 'utf8');
console.log(`✅ data/admin-catalogo-360.json gerado (${(fs.statSync(ADMIN_360_PATH).size / 1024).toFixed(0)} KB, ${adminItems.length} produtos, Score médio: ${summary.avg_health_score}%).`);
