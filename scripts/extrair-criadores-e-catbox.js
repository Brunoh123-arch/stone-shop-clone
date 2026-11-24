const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
const V3_PATH = path.join(ROOT, 'js', 'videos-criadores-v3.js');
const PRODS_DIR = path.join(ROOT, 'data', 'produtos');
const REGISTRY_PATH = path.join(ROOT, 'data', 'catbox-registry.json');

const v3Source = fs.readFileSync(V3_PATH, 'utf8');

// Injeta um hook cirúrgico logo após o fim do switch(prodId) (antes do filtro DOM)
// para capturar activeDataset e contextType exatos de cada produto!
const marker = '// Desacoplamento estrito entre o vídeo oficial da descrição e os vídeos de criadores (BLINDADO)';
if (!v3Source.includes(marker)) {
  throw new Error('Marcador de fim do switch(prodId) não encontrado em videos-criadores-v3.js');
}

const instrumentedSource = v3Source.replace(
  marker,
  `if (typeof window.__CAPTURE_CREATORS__ === 'function') { window.__CAPTURE_CREATORS__(prodId, activeDataset, contextType); return; }\n    ${marker}`
);

function extractCreatorsForProd(prodId) {
  let captured = { dataset: [], contextType: 'sem_video' };
  const dummyEl = {
    innerHTML: '',
    style: { setProperty: () => {} },
    getAttribute: () => '',
    setAttribute: () => {},
    appendChild: () => {},
    addEventListener: () => {},
    querySelector: () => null,
    querySelectorAll: () => [],
  };
  const win = {
    location: { pathname: `/pages/produto-${prodId}.html`, href: `https://stoneshopclone.vercel.app/pages/produto-${prodId}` },
    addEventListener: () => {},
    __CAPTURE_CREATORS__: (_id, ds, ctx) => {
      captured = {
        dataset: Array.isArray(ds) ? JSON.parse(JSON.stringify(ds)) : [],
        contextType: ctx || 'general',
      };
    },
  };
  const sandbox = {
    window: win,
    document: {
      readyState: 'complete',
      title: '',
      head: dummyEl,
      body: dummyEl,
      getElementById: (id) => (id === 'creators-section' ? dummyEl : null),
      querySelector: () => null,
      querySelectorAll: () => [],
      createElement: () => dummyEl,
      addEventListener: () => {},
    },
    navigator: { userAgent: '' },
    IntersectionObserver: function() { return { observe: () => {}, disconnect: () => {} }; },
    requestAnimationFrame: (fn) => fn(),
    setTimeout: () => {},
    clearTimeout: () => {},
    console,
  };
  vm.runInNewContext(instrumentedSource, sandbox);
  return captured;
}

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
    .slice(0, 28) || 'produto';
}

const prodFiles = fs.readdirSync(PRODS_DIR)
  .filter((f) => /^produto-\d+\.json$/.test(f))
  .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));

const registry = {
  version: '1.0.0',
  updated_at: new Date().toISOString(),
  description: 'Livro-Razão Oficial Anti-Conflito Catbox — Cada vídeo Catbox pertence exclusivamente ao seu produto.',
  videos: {},
  conflicts_detected: [],
};

let totalProductsWithCreators = 0;
let totalCreatorVideos = 0;
let totalDescVideos = 0;

for (const file of prodFiles) {
  const filePath = path.join(PRODS_DIR, file);
  const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  if (data.redirect) continue;

  const pid = data.id;
  const slug = slugifyShort(data.product_title || data.title);

  // 1. Vídeo principal da descrição
  let descBaseUrl = '';
  if (data.video && data.video.src) {
    descBaseUrl = cleanCatboxBase(data.video.src);
    if (descBaseUrl.includes('catbox.moe')) {
      const catboxId = path.basename(descBaseUrl);
      const taggedDescUrl = `${descBaseUrl}#prod=${pid}&slot=descricao&slug=${slug}`;
      data.video.src = taggedDescUrl;
      data.video.catbox_id = catboxId;
      totalDescVideos++;

      if (registry.videos[descBaseUrl] && registry.videos[descBaseUrl].owner_product_id !== pid) {
        registry.conflicts_detected.push({
          url: descBaseUrl,
          first_owner: registry.videos[descBaseUrl].owner_product_id,
          also_used_in: pid,
          slot: 'descricao',
        });
      } else if (!registry.videos[descBaseUrl]) {
        registry.videos[descBaseUrl] = {
          catbox_id: catboxId,
          base_url: descBaseUrl,
          tagged_url: taggedDescUrl,
          owner_product_id: pid,
          owner_product_title: data.product_title,
          slot: 'descricao',
          poster: data.video.poster || '',
        };
      }
    }
  }

  // 2. Vídeos de criadores extraídos do switch(prodId)
  const { dataset, contextType } = extractCreatorsForProd(pid);

  // Desacopla do vídeo da descrição e remove duplicados dentro do mesmo produto
  const seenBase = new Set();
  const cleanCreators = [];
  let creatorIdx = 0;

  for (const rawItem of dataset) {
    const rawVid = (rawItem.video || rawItem.localVideo || '').trim();
    if (!rawVid) continue;
    const baseVid = cleanCatboxBase(rawVid);
    if (!baseVid || seenBase.has(baseVid)) continue;
    if (descBaseUrl && baseVid === descBaseUrl && dataset.length > 1) continue;

    seenBase.add(baseVid);
    creatorIdx++;

    let finalVid = rawVid;
    let catboxId = null;

    if (baseVid.includes('catbox.moe')) {
      catboxId = path.basename(baseVid);
      finalVid = `${baseVid}#prod=${pid}&slot=criador_${creatorIdx}&slug=${slug}`;

      if (registry.videos[baseVid] && registry.videos[baseVid].owner_product_id !== pid) {
        registry.conflicts_detected.push({
          url: baseVid,
          first_owner: registry.videos[baseVid].owner_product_id,
          also_used_in: pid,
          slot: `criador_${creatorIdx}`,
        });
      } else if (!registry.videos[baseVid]) {
        registry.videos[baseVid] = {
          catbox_id: catboxId,
          base_url: baseVid,
          tagged_url: finalVid,
          owner_product_id: pid,
          owner_product_title: data.product_title,
          slot: `criador_${creatorIdx}`,
          creator_username: rawItem.username || '',
          poster: rawItem.poster || '',
        };
      }
    }

    cleanCreators.push({
      name: rawItem.name || 'Criador Oficial',
      username: rawItem.username || `criador_${creatorIdx}`,
      avatar: rawItem.avatar || '../img/creators-avatars/creator-1.jpg',
      poster: rawItem.poster || '',
      video: finalVid,
      catbox_id: catboxId,
      startTime: rawItem.startTime || 0.2,
      likes: rawItem.likes || (12400 + (((creatorIdx - 1) * 4391) % 48000)),
      commentsCount: rawItem.commentsCount || rawItem.comments || (38 + (((creatorIdx - 1) * 19) % 210)),
      saves: rawItem.saves || rawItem.savesCount || 1420,
      shares: rawItem.shares || rawItem.sharesCount || 410,
      description: rawItem.description || rawItem.desc || rawItem.title || '',
    });
  }

  data.creator_context = contextType;
  data.creators = cleanCreators;

  if (cleanCreators.length > 0) {
    totalProductsWithCreators++;
    totalCreatorVideos += cleanCreators.length;
  }

  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

registry.stats = {
  total_unique_catbox_videos: Object.keys(registry.videos).length,
  total_desc_videos: totalDescVideos,
  total_creator_videos_slots: totalCreatorVideos,
  products_with_creators: totalProductsWithCreators,
  conflicts_count: registry.conflicts_detected.length,
};

fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2), 'utf8');

console.log('=== CATBOX REGISTRY & CRIADORES POR PRODUTO CONCLUÍDOS ===');
console.log('Produtos com criadores:', totalProductsWithCreators);
console.log('Total vídeos descrição Catbox:', totalDescVideos);
console.log('Total slots de criadores:', totalCreatorVideos);
console.log('Vídeos únicos Catbox registrados:', Object.keys(registry.videos).length);
console.log('Conflitos históricos detectados entre produtos:', registry.conflicts_detected.length);
