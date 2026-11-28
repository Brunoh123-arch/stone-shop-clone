const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { renderReviews } = require('../../api/_lib/render-produto');

const ROOT = path.join(__dirname, '..', '..');
const DRAFTS_ROOT = path.join(ROOT, '.studio-drafts');

const COMMERCIAL_WORD_RE = /(shop|store|loja|oficial|official|ofertas|achadinhos|outlet|magazine|brasil|brazil|tech)/gi;

function ensureDraftsRoot() {
  if (!fs.existsSync(DRAFTS_ROOT)) fs.mkdirSync(DRAFTS_ROOT, { recursive: true });
}

function getNextProductId() {
  const indexPath = path.join(ROOT, 'data', 'produtos', 'index.js');
  if (!fs.existsSync(indexPath)) return 160;
  const raw = fs.readFileSync(indexPath, 'utf8');
  const matches = Array.from(raw.matchAll(/'(\d+)'\s*:/g)).map((m) => Number(m[1]));
  const maxId = matches.length ? Math.max(...matches) : 159;
  return Math.max(maxId + 1, 160);
}

function formatBRLNum(num) {
  const n = Number(num || 0);
  const [intPart, decPart] = n.toFixed(2).split('.');
  const formattedInt = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return `${formattedInt},${decPart}`;
}

function splitPriceParts(pricePix) {
  const n = Math.max(1, Number(pricePix || 49.89));
  const [intRaw, decRaw] = n.toFixed(2).split('.');
  const formattedInt = intRaw.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  return {
    num: Number(n.toFixed(2)),
    price_int: formattedInt,
    price_cents: `,${decRaw}`,
  };
}

function computeSweetSpotPix(originalPrice) {
  const raw = Number(originalPrice || 0);
  if (!(raw > 0)) {
    return { pix: 49.89, orig: 239.9 };
  }
  let pix;
  if (raw <= 80) {
    pix = Math.min(37.89, Math.max(24.89, Math.floor(raw * 0.46) + 0.89));
  } else if (raw <= 180) {
    pix = Math.min(57.89, Math.max(47.89, Math.floor(raw * 0.36) + 0.89));
  } else if (raw <= 400) {
    pix = Math.min(119.9, Math.max(69.89, Math.floor(raw * 0.31) + 0.9));
  } else {
    pix = Math.min(297.9, Math.max(167.9, Math.floor(raw * 0.28) + 0.9));
  }
  pix = Number(pix.toFixed(2));
  const minOrig = Number((Math.ceil(pix * 3.6) + 0.9).toFixed(2));
  const orig = raw >= pix * 2.2 ? Number(raw.toFixed(2)) : minOrig;
  return { pix, orig };
}

function sanitizeVariationName(name) {
  return String(name || '')
    .replace(/\s*,\s*/g, '/ ')
    .replace(/\s*[|·•]+\s*/g, ' / ')
    .replace(/\s{2,}/g, ' ')
    .trim() || 'Padrão';
}

function sanitizeCompositeVariation(raw) {
  const parts = String(raw || '')
    .split(/\s*[·•|]\s*/)
    .map((seg) => sanitizeVariationName(seg))
    .filter(Boolean);
  return parts.join(' · ');
}

function sanitizeCreatorObj(c, idx = 0) {
  const fallbackNames = [
    ['Camila Rocha', 'camilarocha.vids'],
    ['Juliana Alves', 'ju.alves.casa'],
    ['Bruna Martins', 'brunamartins_real'],
    ['Fernanda Costa', 'fer.costa.dicas'],
    ['Letícia Souza', 'leticiasouza.dia'],
    ['Mariana Ribeiro', 'mari.ribeiro.rotina'],
    ['Amanda Lima', 'amandalima.real'],
    ['Patrícia Gomes', 'patygomes.rotina'],
    ['Renata Dias', 'renatadias.vids'],
    ['Vanessa Cardoso', 'vanessacardoso.eu'],
    ['Lucas Ferreira', 'lucasferreira.real'],
    ['Rafael Mendes', 'rafamendes.dia'],
  ];
  const fb = fallbackNames[idx % fallbackNames.length];
  let name = String((c && c.name) || fb[0]).replace(COMMERCIAL_WORD_RE, '').replace(/\s{2,}/g, ' ').trim();
  let username = String((c && c.username) || fb[1]).replace(/^@+/, '').replace(COMMERCIAL_WORD_RE, '').replace(/[^a-zA-Z0-9._]/g, '').trim();
  if (name.length < 3) name = fb[0];
  if (username.length < 4) username = `${fb[1]}${idx + 1}`;
  const descClean = String((c && c.description) || '')
    .replace(/R\$\s*[\d.,]+/gi, '')
    .replace(/shopee|mercado\s*livre|aliexpress/gi, '')
    .trim();
  return {
    id: (c && c.id) || `vid_${idx + 1}_${Date.now()}`,
    name,
    username,
    avatar: (c && c.avatar) || '../img/reviews-avatars/mulheres_validadas/mulher_01.jpg',
    poster: (c && c.poster) || '',
    video: (c && c.video) || '',
    stream_url: (c && c.stream_url) || (c && c.video) || '',
    catbox_id: (c && c.catbox_id) || '',
    catbox_ready: Boolean(c && (c.catbox_ready || /catbox\.moe\//i.test(c.video || ''))),
    startTime: Number((c && c.startTime) || 0),
    likes: (c && c.likes) || `${(idx + 2) * 1.3}K`.replace('.', ','),
    commentsCount: Number((c && c.commentsCount) || (42 + idx * 11)),
    saves: (c && c.saves) || String(180 + idx * 29),
    shares: (c && c.shares) || String(95 + idx * 17),
    description: descClean || 'Chegou certinho e a qualidade surpreendeu demais no dia a dia!',
  };
}

function sanitizeDescriptionHtml(rawHtml, title, details = []) {
  let clean = String(rawHtml || '')
    .replace(/R\$\s*[\d.,]+/gi, '')
    .replace(/\b\d+\s*%\s*OFF\b/gi, '')
    .replace(/\b(mercado\s*livre|shopee|aliexpress|shein|amazon)\b/gi, 'nossa loja')
    .trim();

  const plainLen = clean.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().length;
  if (plainLen >= 310) return clean;

  const detailItems = (Array.isArray(details) && details.length ? details : [
    { label: 'Acabamento', value: 'Alta durabilidade e revisão completa de fábrica' },
    { label: 'Envio', value: 'Pronta entrega no Brasil com código de rastreio' },
    { label: 'Garantia', value: 'Compra protegida com devolução gratuita' },
  ])
    .slice(0, 6)
    .map((d) => `<li><strong>${d.label}:</strong> ${d.value}</li>`)
    .join('');

  const safeTitle = String(title || 'Produto Oficial Stone Shop')
    .replace(/R\$\s*[\d.,]+/gi, '')
    .replace(/\b\d+\s*%\s*OFF\b/gi, '')
    .trim();

  const extraBlock = [
    `<p><strong>${safeTitle}</strong> foi desenvolvido para entregar praticidade imediata, excelente acabamento e resistência superior no uso diário. Cada unidade passa por conferência de qualidade antes do envio, garantindo que você receba exatamente o item anunciado com todos os componentes protegidos na embalagem.</p>`,
    `<p>Ideal tanto para uso próprio quanto para presentear com segurança, conta com design funcional, materiais selecionados de fácil conservação e excelente ergonomia. Acompanha suporte dedicado pós-compra e envio ágil com rastreamento atualizado em todas as etapas da entrega.</p>`,
    `<ul>${detailItems}</ul>`,
  ].join('\n');

  return clean ? `${clean}\n${extraBlock}` : extraBlock;
}

function inferCategory(title) {
  const t = String(title || '').toLowerCase();
  if (/vestido|camiseta|bermuda|sand[aá]lia|bolsa|sapato|t[eê]nis|cinta|pijama|conjunto|cal[cç]a|blusa|rel[oó]gio|colar|porta[- ]?joia/.test(t)) return 'moda';
  if (/maquiagem|escova secadora|modelador|chapinha|perfume|sobrancelha|beleza|skincare|secador/.test(t)) return 'beleza';
  if (/infantil|brinquedo|patinete|triciclo|c[aâ]mera infantil|carrinho|beb[eê]|girocar|boneca/.test(t)) return 'infantil';
  if (/panela|fritadeira|air fryer|fog[aã]o|liquidificador|batedeira|cozinha|pote|faca|churras/.test(t)) return 'cozinha';
  if (/tv|smartwatch|celular|galaxy|tablet|caixa de som|jbl|projetor|fone|gamer|arcade/.test(t)) return 'eletronicos';
  if (/pneu|automotivo|carro|lavadora de alta|aspirador de p[oó]|chave|ferramenta/.test(t)) return 'auto';
  return 'casa';
}

function getValidVariationSample(variations, idx = 0) {
  if (!variations || typeof variations !== 'object') return '';
  const groups = Object.values(variations).filter((g) => g && Array.isArray(g.opcoes) && g.opcoes.length > 0);
  if (!groups.length) return '';
  return groups
    .map((g, gIdx) => {
      const opt = g.opcoes[(idx + gIdx) % g.opcoes.length];
      return sanitizeVariationName(typeof opt === 'string' ? opt : opt.nome);
    })
    .join(' · ');
}

function deduplicateCreatorsByUsername(list, initialSeen = new Set()) {
  const seen = new Set(Array.from(initialSeen).map((u) => String(u || '').toLowerCase()));
  const out = [];
  for (const item of list || []) {
    if (!item) continue;
    const uname = String(item.username || '').trim().toLowerCase();
    if (uname && seen.has(uname)) continue;
    if (uname) seen.add(uname);
    out.push(item);
  }
  return out;
}

function normalizeVariations(variations, slides) {
  const safeSlides = Array.isArray(slides) ? slides : [];
  const defaultImg = (safeSlides[0] && safeSlides[0].src) || '/logo.png';
  if (!variations || typeof variations !== 'object' || !Object.keys(variations).length) {
    return {
      cor: {
        com_imagem: true,
        label: 'Modelo',
        opcoes: [{ nome: 'Padrão Oficial', imagem: defaultImg }],
      },
    };
  }
  const out = {};
  const globalUsedVarImgs = new Set();

  for (const [k, grp] of Object.entries(variations)) {
    if (!grp || !Array.isArray(grp.opcoes) || !grp.opcoes.length) continue;
    const wantsImg = Boolean(grp.com_imagem) || grp.opcoes.some((o) => o && typeof o === 'object' && o.imagem);
    if (!wantsImg) {
      out[k] = {
        com_imagem: false,
        label: String(grp.label || k),
        opcoes: grp.opcoes.map((o, idx) => sanitizeVariationName(typeof o === 'string' ? o : (o.nome || `Opção ${idx + 1}`))),
      };
      continue;
    }

    const mappedOpts = [];
    let hasCollision = false;

    grp.opcoes.forEach((o, idx) => {
      const cleanName = sanitizeVariationName(typeof o === 'string' ? o : (o.nome || `Opção ${idx + 1}`));
      let candidateImg = (typeof o === 'object' && o.imagem) ? String(o.imagem) : '';
      const cleanKey = (u) => String(u || '').split('?')[0].split('#')[0];

      if (!candidateImg || globalUsedVarImgs.has(cleanKey(candidateImg))) {
        const unusedSlide = safeSlides.find((s) => s && s.src && !globalUsedVarImgs.has(cleanKey(s.src)));
        candidateImg = unusedSlide ? unusedSlide.src : '';
      }

      if (!candidateImg || globalUsedVarImgs.has(cleanKey(candidateImg))) {
        hasCollision = true;
      } else {
        globalUsedVarImgs.add(cleanKey(candidateImg));
      }

      const opt = { nome: cleanName, imagem: candidateImg || defaultImg };
      if (typeof o === 'object' && Number(o.preco) > 0) opt.preco = Number(Number(o.preco).toFixed(2));
      if (typeof o === 'object' && o.precoOrig) opt.precoOrig = String(o.precoOrig);
      mappedOpts.push(opt);
    });

    if (hasCollision && mappedOpts.length > 1) {
      out[k] = {
        com_imagem: false,
        label: String(grp.label || k),
        opcoes: mappedOpts.map((o) => o.nome),
      };
    } else {
      out[k] = {
        com_imagem: true,
        label: String(grp.label || k),
        opcoes: mappedOpts,
      };
    }
  }
  return Object.keys(out).length ? out : {
    cor: { com_imagem: true, label: 'Modelo', opcoes: [{ nome: 'Padrão Oficial', imagem: defaultImg }] },
  };
}

function createDraft(init = {}) {
  ensureDraftsRoot();
  const draftId = init.draftId || `d_${Date.now()}_${crypto.randomBytes(3).toString('hex')}`;
  const draftDir = path.join(DRAFTS_ROOT, draftId);
  if (!fs.existsSync(draftDir)) fs.mkdirSync(draftDir, { recursive: true });

  const sweet = computeSweetSpotPix(init.price_original_num || 0);
  const pricePix = Number(init.price_pix) > 0 ? Number(Number(init.price_pix).toFixed(2)) : sweet.pix;
  const priceOrigNum = Number(init.price_original_num) > pricePix ? Number(Number(init.price_original_num).toFixed(2)) : sweet.orig;
  const title = String(init.product_title || 'Carregando produto...').trim();

  const slides = Array.isArray(init.slides) ? init.slides : [];
  const variations = normalizeVariations(init.variations, slides);

  const draft = {
    draftId,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    status: init.status || 'ready',
    source_urls: Array.isArray(init.source_urls) ? init.source_urls : [],
    targetId: Number(init.targetId) || getNextProductId(),
    category: init.category || inferCategory(title),
    gender: init.gender || 'feminino',
    is_apparel: Boolean(init.is_apparel),
    product_title: title,
    price_pix: pricePix,
    price_original_num: priceOrigNum,
    sold_num: Number(init.sold_num) || 4820,
    rating_score: String(init.rating_score || '4.9'),
    reviews_total_display: Number(init.reviews_total_display) || 348,
    slides,
    variations,
    details: Array.isArray(init.details) && init.details.length ? init.details : [
      { label: 'Envio', value: 'Pronta entrega Brasil com rastreio', hidden: false },
      { label: 'Garantia', value: '30 dias de proteção direta', hidden: false },
    ],
    size_guide_html: init.is_apparel ? String(init.size_guide_html || '') : '',
    description_html: sanitizeDescriptionHtml(init.description_html, title, init.details),
    video: init.video || null,
    creators: (Array.isArray(init.creators) ? init.creators : []).map((c, i) => sanitizeCreatorObj(c, i)),
    reviews: Array.isArray(init.reviews) ? init.reviews : [],
    reserve_videos: (Array.isArray(init.reserve_videos) ? init.reserve_videos : []).map((c, i) => sanitizeCreatorObj(c, i + 10)),
    reserve_unboxings: Array.isArray(init.reserve_unboxings) ? init.reserve_unboxings : [],
    reserve_reviews: Array.isArray(init.reserve_reviews) ? init.reserve_reviews : [],
  };

  return saveDraft(draft);
}

function getDraftPath(draftId) {
  const safeId = String(draftId || '').replace(/[^a-zA-Z0-9_-]/g, '');
  return path.join(DRAFTS_ROOT, safeId, 'draft.json');
}

function loadDraft(draftId) {
  const fp = getDraftPath(draftId);
  if (!fs.existsSync(fp)) return null;
  try {
    return JSON.parse(fs.readFileSync(fp, 'utf8'));
  } catch (e) {
    return null;
  }
}

function saveDraft(draft) {
  ensureDraftsRoot();
  const fp = getDraftPath(draft.draftId);
  const dir = path.dirname(fp);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  draft.updatedAt = new Date().toISOString();
  fs.writeFileSync(fp, JSON.stringify(draft, null, 2), 'utf8');
  return draft;
}

function listDrafts() {
  ensureDraftsRoot();
  return fs.readdirSync(DRAFTS_ROOT)
    .map((d) => loadDraft(d))
    .filter(Boolean)
    .sort((a, b) => String(b.updatedAt).localeCompare(String(a.updatedAt)))
    .slice(0, 15);
}

function popFromReserve(draftId, kind, count = 1) {
  const draft = loadDraft(draftId);
  if (!draft) throw new Error(`Draft ${draftId} not found`);
  const n = Math.max(1, Number(count) || 1);
  let added = [];
  let remaining = 0;

  if (kind === 'videos') {
    const pool = Array.isArray(draft.reserve_videos) ? draft.reserve_videos : [];
    const activeUsers = new Set((draft.creators || []).map((c) => String(c.username || '').toLowerCase()));
    const picked = [];
    const kept = [];
    for (const item of pool) {
      const sanitized = sanitizeCreatorObj(item, draft.creators.length + picked.length);
      const uname = sanitized.username.toLowerCase();
      if (picked.length < n && !activeUsers.has(uname)) {
        activeUsers.add(uname);
        picked.push(sanitized);
      } else if (!activeUsers.has(uname)) {
        kept.push(item);
      }
    }
    added = picked;
    draft.reserve_videos = kept;
    draft.creators.push(...added);
    remaining = kept.length;
  } else if (kind === 'unboxings') {
    const pool = Array.isArray(draft.reserve_unboxings) ? draft.reserve_unboxings : [];
    added = pool.splice(0, n);
    draft.reserve_unboxings = pool;
    // Insert right after existing photo reviews so unboxing cards stay at the top
    const withPhotos = draft.reviews.filter((r) => Array.isArray(r.photos) && r.photos.length > 0);
    const textOnly = draft.reviews.filter((r) => !Array.isArray(r.photos) || r.photos.length === 0);
    draft.reviews = [...withPhotos, ...added, ...textOnly];
    remaining = pool.length;
  } else if (kind === 'reviews') {
    const pool = Array.isArray(draft.reserve_reviews) ? draft.reserve_reviews : [];
    added = pool.splice(0, n);
    draft.reserve_reviews = pool;
    draft.reviews.push(...added);
    remaining = pool.length;
  }

  saveDraft(draft);
  const built = buildProductJsonFromDraft(draft);
  return { draft, added, remaining, built, livePatch: extractLivePatch(built) };
}

function extractLivePatch(built) {
  return {
    product_title: built.product_title,
    price_int: built.price_int,
    price_cents: built.price_cents,
    price_original: built.price_original,
    discount_badge: built.discount_badge,
    installment_text: built.installment_text,
    coupon_main: built.coupon_main,
    sold_num: parseInt(String(built.sold_count).replace(/\D/g, ''), 10) || 1240,
    rating_score: built.rating_score,
    rating_count: built.rating_count,
    reviews_header: built.reviews_header,
    description_html: built.description_html,
    slider_imgs: built.slider_imgs,
    reviews_cards_html: renderReviews(built.reviews),
    video: built.video,
    creators: built.creators,
    produto_atual: built.produto_atual,
  };
}

function applyDraftPatch(draftId, patch = {}) {
  const draft = loadDraft(draftId);
  if (!draft) throw new Error(`Draft ${draftId} not found`);

  if (patch.targetId !== undefined && Number(patch.targetId) >= 125) draft.targetId = Number(patch.targetId);
  if (patch.product_title !== undefined) draft.product_title = String(patch.product_title).trim() || draft.product_title;
  if (patch.price_pix !== undefined && Number(patch.price_pix) > 0) {
    draft.price_pix = Number(Number(patch.price_pix).toFixed(2));
    if (draft.price_original_num <= draft.price_pix * 1.25) {
      draft.price_original_num = Number((Math.ceil(draft.price_pix * 3.5) + 0.9).toFixed(2));
    }
  }
  if (patch.price_original_num !== undefined && Number(patch.price_original_num) > 0) {
    draft.price_original_num = Number(Number(patch.price_original_num).toFixed(2));
  }
  if (patch.sold_num !== undefined && Number(patch.sold_num) > 0) draft.sold_num = Math.round(Number(patch.sold_num));
  if (patch.rating_score !== undefined) draft.rating_score = String(patch.rating_score).replace(',', '.');
  if (patch.reviews_total_display !== undefined && Number(patch.reviews_total_display) > 0) {
    draft.reviews_total_display = Math.round(Number(patch.reviews_total_display));
  }
  if (patch.category !== undefined) draft.category = String(patch.category);
  if (patch.gender !== undefined) draft.gender = String(patch.gender);
  if (patch.is_apparel !== undefined) draft.is_apparel = Boolean(patch.is_apparel);
  if (patch.description_html !== undefined) {
    draft.description_html = sanitizeDescriptionHtml(patch.description_html, draft.product_title, draft.details);
  }
  if (Array.isArray(patch.slides)) draft.slides = patch.slides;
  if (patch.variations && typeof patch.variations === 'object') {
    draft.variations = normalizeVariations(patch.variations, draft.slides);
  }
  if (Array.isArray(patch.details)) draft.details = patch.details;
  if (patch.video !== undefined) draft.video = patch.video;
  if (Array.isArray(patch.creators)) draft.creators = patch.creators.map((c, i) => sanitizeCreatorObj(c, i));
  if (Array.isArray(patch.reviews)) draft.reviews = patch.reviews;

  // Quick 1-click curation actions
  if (patch.action === 'remove_slide' && typeof patch.index === 'number') {
    draft.slides.splice(patch.index, 1);
  } else if (patch.action === 'promote_slide' && typeof patch.index === 'number' && draft.slides[patch.index]) {
    const [picked] = draft.slides.splice(patch.index, 1);
    draft.slides.unshift(picked);
  } else if (patch.action === 'remove_creator' && typeof patch.index === 'number') {
    const [removed] = draft.creators.splice(patch.index, 1);
    if (removed) draft.reserve_videos.push(removed);
  } else if (patch.action === 'set_desc_video' && typeof patch.index === 'number' && draft.creators[patch.index]) {
    const [picked] = draft.creators.splice(patch.index, 1);
    if (draft.video && draft.video.src) {
      draft.creators.unshift(sanitizeCreatorObj({
        id: draft.video.id,
        video: draft.video.src,
        poster: draft.video.poster,
        catbox_id: draft.video.catbox_id,
      }, 0));
    }
    draft.video = {
      id: picked.id,
      src: picked.video,
      poster: picked.poster,
      duration: '0:22',
      catbox_id: picked.catbox_id || '',
    };
  } else if (patch.action === 'remove_review' && typeof patch.index === 'number') {
    const [removed] = draft.reviews.splice(patch.index, 1);
    if (removed) {
      if (Array.isArray(removed.photos) && removed.photos.length) draft.reserve_unboxings.push(removed);
      else draft.reserve_reviews.push(removed);
    }
  } else if (patch.action === 'add_custom_review' && patch.review) {
    draft.reviews.unshift({
      name: String(patch.review.name || 'M**a S**a'),
      avatar: patch.review.avatar || '../img/reviews-avatars/mulheres_validadas/mulher_01.jpg',
      stars: Number(patch.review.stars) || 5,
      date: patch.review.date || '27/11',
      variation: sanitizeCompositeVariation(patch.review.variation || getValidVariationSample(draft.variations, 0)),
      comment: String(patch.review.comment || 'Produto excelente, entrega super rápida!'),
      photos: Array.isArray(patch.review.photos) ? patch.review.photos : [],
    });
  }

  saveDraft(draft);
  const built = buildProductJsonFromDraft(draft);
  return { draft, built, livePatch: extractLivePatch(built) };
}

function buildProductJsonFromDraft(draft) {
  const id = Number(draft.targetId) || getNextProductId();
  const parts = splitPriceParts(draft.price_pix);
  const origNum = Math.max(parts.num + 10, Number(draft.price_original_num || parts.num * 3.5));
  const origStr = formatBRLNum(origNum);
  const pct = Math.min(90, Math.max(25, Math.round((1 - parts.num / origNum) * 100)));
  const savings = formatBRLNum(Math.max(1, origNum - parts.num));
  const val3x = (Math.floor((parts.num / 3) * 100) / 100).toFixed(2).replace('.', ',');

  const slides = (Array.isArray(draft.slides) && draft.slides.length ? draft.slides : [{ src: '/logo.png', alt: draft.product_title }])
    .map((s, idx) => ({
      src: s.src,
      alt: s.alt || `${draft.product_title} - Foto ${idx + 1}`,
    }));

  const normVars = normalizeVariations(draft.variations, slides);
  const validVarNames = new Set();
  Object.values(normVars).forEach((g) => {
    (g.opcoes || []).forEach((o) => {
      validVarNames.add(String(typeof o === 'string' ? o : o.nome).toLowerCase());
    });
  });

  const reviews = (Array.isArray(draft.reviews) ? draft.reviews : []).map((r, idx) => {
    let varStr = sanitizeCompositeVariation(r.variation || '');
    const segs = varStr.toLowerCase().split(/\s*[·•|]\s*/).filter(Boolean);
    const isValid = segs.length > 0 && segs.every((s) => validVarNames.has(s));
    if (!isValid) {
      varStr = getValidVariationSample(normVars, idx);
    }
    const date = r.date || '26/11';
    return {
      name: r.name || 'C**a S**a',
      avatar: r.avatar || '../img/reviews-avatars/mulheres_validadas/mulher_01.jpg',
      stars: Math.min(5, Math.max(4, Number(r.stars) || 5)),
      date,
      variation: varStr,
      date_line: [date, varStr].filter(Boolean).join(' · '),
      comment: String(r.comment || 'Produto excelente, chegou bem embalado e dentro do prazo!'),
      photos: Array.isArray(r.photos) ? r.photos : [],
    };
  });

  const totalCountNum = Math.max(reviews.length, Number(draft.reviews_total_display) || 328);
  const ratingScore = String(draft.rating_score || '4.9').replace(',', '.');

  let descVideo = draft.video;
  const rawCreatorsList = (Array.isArray(draft.creators) ? draft.creators : []).map((c, idx) => sanitizeCreatorObj(c, idx));
  const creatorsList = deduplicateCreatorsByUsername(rawCreatorsList);
  if ((!descVideo || !descVideo.src) && creatorsList.length > 1) {
    const first = creatorsList.shift();
    descVideo = {
      src: first.video,
      poster: first.poster,
      duration: '0:20',
      catbox_id: first.catbox_id || '',
    };
  }

  return {
    id,
    title: `${draft.product_title} - Stone Shop`,
    meta_description: `${draft.product_title} com envio rápido e compra garantida na Stone Shop.`,
    product_title: draft.product_title,
    slider_imgs: slides,
    discount_badge: `-${pct}%`,
    price_int: parts.price_int,
    price_cents: parts.price_cents,
    price_original: `R$ ${origStr}`,
    installment_text: `3x R$ ${val3x}`,
    installment_highlight: 'sem juros',
    coupon_main: `Economize R$ ${savings}`,
    coupon_bonus: 'Frete grátis',
    rating_score: ratingScore,
    rating_count: `(${totalCountNum})`,
    sold_count: `${Math.max(100, Number(draft.sold_num) || 4820)} vendidos on-line`,
    frete_original: 'R$ 24,90',
    reviews_header: `Avaliações dos clientes (${totalCountNum})`,
    reviews_avg: ratingScore,
    reviews,
    details: Array.isArray(draft.details) ? draft.details : [],
    video: descVideo || { src: '', poster: '', duration: '0:18', catbox_id: '' },
    size_guide_html: draft.is_apparel ? String(draft.size_guide_html || '') : '',
    description_html: sanitizeDescriptionHtml(draft.description_html, draft.product_title, draft.details),
    related: [],
    produto_atual: {
      id,
      nome: draft.product_title,
      preco: parts.num,
      price: `R$ ${formatBRLNum(parts.num)}`,
      preco_antigo: origNum,
      precoOrig: `R$ ${origStr}`,
      installmentText: `3x R$ ${val3x} sem juros`,
      shipping: 'Frete grátis',
      store: 'Stone Shop',
      rating: ratingScore,
      sales: `${Math.max(100, Number(draft.sold_num) || 4820)} vendidos on-line`,
      img: slides[0].src,
      imagens: slides.map((s) => s.src),
      variacoes: normVars,
    },
    extra_scripts: [],
    creator_context: draft.category || 'casa',
    creators: creatorsList,
  };
}

function applyDaemonPatch(draftId, body = {}) {
  const draft = loadDraft(draftId);
  if (!draft) return null;
  const op = body.op || '';

  if (op === 'extract_fast') {
    if (body.title) {
      draft.product_title = String(body.title).trim();
      draft.category = inferCategory(draft.product_title);
    }
    if (Number(body.price_original) > 0 && !draft.user_locked_price) {
      const sweet = computeSweetSpotPix(Number(body.price_original));
      draft.price_pix = sweet.pix;
      draft.price_original_num = sweet.orig;
    }
    if (Array.isArray(body.slides) && body.slides.length) draft.slides = body.slides;
    if (body.description_html) draft.description_html = sanitizeDescriptionHtml(body.description_html, draft.product_title, draft.details);
    draft.status = 'enriching';
  } else if (op === 'extract_full') {
    if (body.title) {
      draft.product_title = String(body.title).trim();
      draft.category = inferCategory(draft.product_title);
    }
    if (Number(body.price_original) > 0 && !draft.user_locked_price) {
      const sweet = computeSweetSpotPix(Number(body.price_original));
      draft.price_pix = sweet.pix;
      draft.price_original_num = sweet.orig;
    }
    if (Array.isArray(body.slides) && body.slides.length) draft.slides = body.slides;
    if (body.variations && Object.keys(body.variations).length) {
      draft.variations = normalizeVariations(body.variations, draft.slides);
    }
    if (Array.isArray(body.details) && body.details.length) draft.details = body.details;
    if (body.description_html) {
      draft.description_html = sanitizeDescriptionHtml(body.description_html, draft.product_title, draft.details);
    }
    if (Array.isArray(body.reviews) && body.reviews.length) draft.reviews = body.reviews;
    if (Array.isArray(body.reserve_unboxings)) draft.reserve_unboxings = body.reserve_unboxings;
    if (Array.isArray(body.reserve_reviews)) draft.reserve_reviews = body.reserve_reviews;
    draft.status = 'ready';
  } else if (op === 'videos_merge') {
    const incoming = (Array.isArray(body.videos) ? body.videos : []).map((v, i) => sanitizeCreatorObj(v, i));
    const existingIds = new Set();
    const existingUrls = new Set();
    const existingUsers = new Set();
    if (draft.video && draft.video.src) {
      if (draft.video.id) existingIds.add(draft.video.id);
      existingUrls.add(draft.video.src);
    }
    (draft.creators || []).forEach((c) => {
      if (c.id) existingIds.add(c.id);
      if (c.video) existingUrls.add(c.video);
      if (c.username) existingUsers.add(String(c.username).toLowerCase());
    });
    (draft.reserve_videos || []).forEach((c) => {
      if (c.id) existingIds.add(c.id);
      if (c.video) existingUrls.add(c.video);
      if (c.username) existingUsers.add(String(c.username).toLowerCase());
    });

    const fresh = [];
    for (const v of incoming) {
      const uname = String(v.username || '').toLowerCase();
      if (existingIds.has(v.id) || existingUrls.has(v.video) || (uname && existingUsers.has(uname))) continue;
      existingIds.add(v.id);
      existingUrls.add(v.video);
      if (uname) existingUsers.add(uname);
      fresh.push(v);
    }
    if (body.mode === 'urls') {
      draft.creators.push(...fresh);
    } else {
      if ((!draft.video || !draft.video.src) && fresh.length > 0) {
        const first = fresh.shift();
        draft.video = {
          id: first.id,
          src: first.video,
          poster: first.poster,
          duration: body.firstDuration || '0:20',
          catbox_id: first.catbox_id || '',
        };
      }
      while (draft.creators.length < 9 && fresh.length > 0) {
        draft.creators.push(fresh.shift());
      }
      draft.reserve_videos.push(...fresh);
    }
  } else if (op === 'video_catbox_done') {
    const vidId = body.videoId;
    if (draft.video && draft.video.id === vidId) {
      draft.video.src = body.catboxUrl;
      draft.video.catbox_id = body.catboxId || '';
      if (body.poster) draft.video.poster = body.poster;
    }
    for (const arr of [draft.creators, draft.reserve_videos]) {
      for (const item of arr || []) {
        if (item.id === vidId) {
          item.video = body.catboxUrl;
          item.catbox_id = body.catboxId || '';
          item.catbox_ready = true;
          if (body.poster) item.poster = body.poster;
          if (body.avatar) item.avatar = body.avatar;
        }
      }
    }
  }

  saveDraft(draft);
  const built = buildProductJsonFromDraft(draft);
  return { draft, built, livePatch: extractLivePatch(built) };
}

module.exports = {
  DRAFTS_ROOT,
  getNextProductId,
  formatBRLNum,
  computeSweetSpotPix,
  sanitizeVariationName,
  sanitizeCompositeVariation,
  sanitizeCreatorObj,
  sanitizeDescriptionHtml,
  inferCategory,
  createDraft,
  loadDraft,
  saveDraft,
  listDrafts,
  popFromReserve,
  applyDraftPatch,
  applyDaemonPatch,
  buildProductJsonFromDraft,
};
