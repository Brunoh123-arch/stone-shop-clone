const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync, execSync } = require('child_process');
const { loadDraft, buildProductJsonFromDraft, formatBRLNum } = require('./draft-manager');

const ROOT = path.join(__dirname, '..', '..');

const BAD_AVATARS = new Set([
  'tt_avatar_5', 'tt_avatar_9', 'tt_avatar_11', 'tt_avatar_12', 'tt_avatar_13', 'tt_avatar_17', 'tt_avatar_19',
  'tt_avatar_29', 'tt_avatar_31', 'tt_avatar_37', 'tt_avatar_39', 'tt_avatar_43', 'tt_avatar_57',
  'tt_cdn_2', 'tt_cdn_3', 'tt_cdn_4', 'tt_cdn_5', 'tt_cdn_10', 'tt_cdn_13', 'tt_cdn_14', 'tt_cdn_15',
  'tt_cdn_19', 'tt_cdn_21', 'tt_cdn_22', 'tt_cdn_23', 'tt_cdn_27', 'tt_cdn_28', 'tt_cdn_30',
  'tt_cdn_34', 'tt_cdn_35', 'tt_cdn_41', 'tt_cdn_44', 'tt_cdn_45',
  'tt_cdn_51', 'tt_cdn_58', 'tt_cdn_66', 'tt_cdn_68', 'tt_cdn_69', 'tt_cdn_70',
]);

const CATEGORY_LABELS = {
  eletronicos: 'Celulares, TVs & Eletrônicos',
  cozinha: 'Eletrodomésticos & Cozinha',
  casa: 'Casa, Limpeza & Natal',
  infantil: 'Brinquedos & Infantil',
  moda: 'Moda, Bolsas & Calçados',
  beleza: 'Beleza, Cabelo & Perfumaria',
  auto: 'Automotivo & Ferramentas',
};

function fileMd5(absPath) {
  if (!fs.existsSync(absPath)) return '';
  return crypto.createHash('md5').update(fs.readFileSync(absPath)).digest('hex');
}

function collectVerifiedAvatarPool(gender = 'feminino') {
  const dirs = [
    path.join(ROOT, 'img', 'reviews-avatars', 'mulheres_validadas'),
    path.join(ROOT, 'img', 'reviews-avatars', 'mulheres_brasil'),
  ];
  const maleExtras = [
    path.join(ROOT, 'img', 'reviews-avatars', 'tiktok_cdn_real', 'tt_cdn_6.jpg'),
    path.join(ROOT, 'img', 'reviews-avatars', 'tiktok_cdn_real', 'tt_cdn_7.jpg'),
  ];

  const candidates = [];
  if (gender === 'masculino' || gender === 'unissex') {
    maleExtras.forEach((abs) => {
      if (fs.existsSync(abs)) candidates.push(abs);
    });
  }

  for (const dir of dirs) {
    if (!fs.existsSync(dir)) continue;
    for (const fn of fs.readdirSync(dir).sort()) {
      if (!/\.(jpg|jpeg|png|webp)$/i.test(fn)) continue;
      const base = path.basename(fn, path.extname(fn));
      if (BAD_AVATARS.has(base)) continue;
      candidates.push(path.join(dir, fn));
    }
  }

  const seenMd5 = new Set();
  const uniqueRelPaths = [];
  for (const abs of candidates) {
    const h = fileMd5(abs);
    if (!h || seenMd5.has(h)) continue;
    seenMd5.add(h);
    const rel = '../' + path.relative(ROOT, abs).replace(/\\/g, '/');
    uniqueRelPaths.push({ rel, abs, md5: h });
  }
  return uniqueRelPaths;
}

function allocateVerifiedAvatars(productJson, gender = 'feminino') {
  const pool = collectVerifiedAvatarPool(gender);
  const usedMd5 = new Set();
  let cursor = 0;

  const nextFromPool = () => {
    while (cursor < pool.length) {
      const item = pool[cursor++];
      if (!usedMd5.has(item.md5)) {
        usedMd5.add(item.md5);
        return item.rel;
      }
    }
    return '../img/reviews-avatars/mulheres_validadas/mulher_10.jpg';
  };

  // First reserve creators' avatars so reviews never collide with creators
  const creators = (productJson.creators || []).map((c) => {
    const cleanRel = String(c.avatar || '').split('?')[0].replace(/^(\.\.\/|\.\/|\/)+/, '');
    const abs = path.join(ROOT, cleanRel);
    const base = path.basename(cleanRel, path.extname(cleanRel));
    if (cleanRel && fs.existsSync(abs) && !BAD_AVATARS.has(base) && !cleanRel.includes('mulher_01.jpg')) {
      const h = fileMd5(abs);
      if (h && !usedMd5.has(h)) {
        usedMd5.add(h);
        return { ...c, avatar: '../' + cleanRel };
      }
    }
    return { ...c, avatar: nextFromPool() };
  });

  const reviews = (productJson.reviews || []).map((r) => {
    const cleanRel = String(r.avatar || '').split('?')[0].replace(/^(\.\.\/|\.\/|\/)+/, '');
    const abs = path.join(ROOT, cleanRel);
    const base = path.basename(cleanRel, path.extname(cleanRel));
    if (
      cleanRel &&
      fs.existsSync(abs) &&
      !BAD_AVATARS.has(base) &&
      !cleanRel.includes('reviews-avatars/unique') &&
      !cleanRel.includes('reviews-avatars/curated') &&
      !cleanRel.includes('mulher_01.jpg')
    ) {
      const h = fileMd5(abs);
      if (h && !usedMd5.has(h)) {
        usedMd5.add(h);
        return { ...r, avatar: '../' + cleanRel };
      }
    }
    return { ...r, avatar: nextFromPool() };
  });

  return {
    ...productJson,
    creators,
    reviews,
  };
}

function escapeAttr(str) {
  return String(str || '')
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function promoteMediaFile(srcRef, destRelFromRoot, copiedFiles) {
  const cleanSrc = String(srcRef || '').split('?')[0];
  if (!cleanSrc || /^https?:\/\//i.test(cleanSrc)) return srcRef;

  let srcAbs;
  if (cleanSrc.startsWith('/.studio-drafts/')) {
    srcAbs = path.join(ROOT, cleanSrc.replace(/^\/+/, ''));
  } else {
    srcAbs = path.join(ROOT, cleanSrc.replace(/^(\.\.\/|\.\/|\/)+/, ''));
  }

  if (!fs.existsSync(srcAbs)) return srcRef;

  const destAbs = path.join(ROOT, destRelFromRoot);
  if (path.resolve(srcAbs) === path.resolve(destAbs)) {
    return '../' + destRelFromRoot.replace(/\\/g, '/');
  }

  fs.mkdirSync(path.dirname(destAbs), { recursive: true });
  fs.copyFileSync(srcAbs, destAbs);
  copiedFiles.push(destAbs);
  return '../' + destRelFromRoot.replace(/\\/g, '/');
}

function buildHomeCardHtml(prodJson, categoryLabel) {
  const id = prodJson.id;
  const title = prodJson.product_title;
  const searchSlug = title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
  const soldNum = String(prodJson.sold_count || '4820').replace(/\D/g, '') || '4820';
  const thumbRel = String((prodJson.slider_imgs[0] && prodJson.slider_imgs[0].src) || 'logo.png').replace(/^(\.\.\/|\/)+/, '');
  const priceStr = formatBRLNum(prodJson.produto_atual.preco);

  return `<!-- PRODUTO ${id} -->
<a class="product-card-rec" data-cat="${escapeAttr(categoryLabel)}" data-id="${id}" data-nome="${escapeAttr(searchSlug)}" data-vendas="${soldNum}" href="pages/produto-${id}.html" style="text-decoration: none; color: inherit;">
<div class="card-inner-box">
<img alt="${escapeAttr(title)}" class="card-thumb-img" loading="lazy" referrerpolicy="no-referrer" src="${escapeAttr(thumbRel)}"/>
<div class="card-details-col">
<div class="card-top-info">
<h3 class="product-name"><span class="tt-list-bf-tag">Black Friday</span>${escapeAttr(title)}</h3>
<div class="tt-list-promo-row"><span class="tt-list-coupon-pill"><svg aria-hidden="true" viewBox="0 0 667 534" width="12" height="10" style="flex-shrink:0;"><path fill="#d60643" d="M666.666 166.667C640.145 166.667 614.71 177.203 595.956 195.956C577.202 214.71 566.666 240.145 566.666 266.667C566.666 293.189 577.202 318.624 595.956 337.378C614.71 356.131 640.145 366.667 666.666 366.667V466.667C666.666 503.486 636.819 533.334 600 533.334H466.666V470.601C466.666 452.191 451.742 437.267 433.333 437.267C414.924 437.267 400 452.191 400 470.601V533.334H66.666C29.847 533.334 0 503.486 0 466.667V366.666C55.428 366.576 100.333 266.167 100.333 266.167C100.333 210.718 55.428 165.758 0 165.668V66.667C0 29.848 29.847 0 66.666 0H400V62.733C400 81.143 414.924 96.067 433.333 96.067C451.742 96.067 466.666 81.143 466.666 62.733V0H600C636.819 0 666.666 29.848 666.666 66.667V166.667ZM466.666 156.867C466.666 138.457 451.742 123.533 433.333 123.533C414.924 123.533 400 138.457 400 156.867V219.601C400 238.01 414.924 252.934 433.333 252.934C451.742 252.934 466.666 238.01 466.666 219.601V156.867ZM466.666 313.733C466.666 295.324 451.742 280.4 433.333 280.4C414.924 280.4 400 295.324 400 313.733V376.467C400 394.876 414.924 409.801 433.333 409.801C451.742 409.801 466.666 394.876 466.666 376.467V313.733Z"/></svg><span>Desconto Black Friday</span></span></div>
<div class="card-badges-row">
<span class="badge-frete-gratis">Frete grátis</span>
<span class="related-discount" style="background: #fff0f2; color: #fe2c55; border: 1px solid #ffd8e0; font-size: 9px; font-weight: 700; padding: 0.5px 3px; border-radius: 2px; line-height: 1.2;">${escapeAttr(prodJson.discount_badge)}</span>
</div>
</div>
<div class="card-rating-row"><span class="star-yellow">★</span> <span class="rating-num">${escapeAttr(prodJson.rating_score)}</span> <span class="rating-pipe">|</span> <span class="sales-count-txt">${soldNum} vendidos</span></div>
<div class="card-bottom-action-row">
<div class="price-stack-col">
<div class="price-current-txt"><span class="currency">R$</span> ${priceStr}</div>
<div class="price-old-txt">${escapeAttr(prodJson.price_original)}</div>
</div>
<div aria-label="Adicionar ao carrinho" class="btn-cart-circle"><svg fill="none" height="15" stroke="#111" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24" width="15"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg></div>
</div>
</div>
</div>
</a>`;
}

function updateCatalogFiles(prodJson, categoryKey) {
  const id = prodJson.id;
  const categoryLabel = CATEGORY_LABELS[categoryKey] || CATEGORY_LABELS.casa;

  // 1. data/produtos/index.js
  const idxJsPath = path.join(ROOT, 'data', 'produtos', 'index.js');
  let idxJs = fs.readFileSync(idxJsPath, 'utf8');
  const regLine = `  '${id}': () => require('./produto-${id}.json'),`;
  if (!new RegExp(`'${id}'\\s*:`).test(idxJs)) {
    idxJs = idxJs.replace(/\}\s*;?\s*$/, `${regLine}\n};\n`);
    fs.writeFileSync(idxJsPath, idxJs, 'utf8');
  }

  // 2. js/catalogo.js
  const catJsPath = path.join(ROOT, 'js', 'catalogo.js');
  let catJs = fs.readFileSync(catJsPath, 'utf8');
  const origClean = String(prodJson.price_original || '').replace(/^R\$\s*/, '');
  const descNum = Number(String(prodJson.discount_badge || '').replace(/\D/g, '')) || 75;
  const soldNum = Number(String(prodJson.sold_count || '').replace(/\D/g, '')) || 4820;
  const catEntry = `  {id:${id},nome:${JSON.stringify(prodJson.product_title)},preco:${prodJson.produto_atual.preco},precoOrig:${JSON.stringify(origClean)},desc:${descNum},vendidos:${soldNum},img:${JSON.stringify(prodJson.slider_imgs[0].src)}},`;
  catJs = catJs.replace(new RegExp(`^\\s*\\{id:${id},.*\\r?\\n`, 'm'), '');
  catJs = catJs.replace('const CATALOGO_PRODUTOS = [', `const CATALOGO_PRODUTOS = [\n${catEntry}`);
  fs.writeFileSync(catJsPath, catJs, 'utf8');

  // 3. index.html (#recommended-grid + #categorias-section count)
  const homePath = path.join(ROOT, 'index.html');
  let homeHtml = fs.readFileSync(homePath, 'utf8');
  const existingCardRe = new RegExp(`<!-- PRODUTO ${id} -->[\\s\\S]*?<\\/a>\\s*`, 'i');
  const wasAlreadyOnHome = existingCardRe.test(homeHtml);
  homeHtml = homeHtml.replace(existingCardRe, '');
  const cardHtml = buildHomeCardHtml(prodJson, categoryLabel);
  homeHtml = homeHtml.replace(
    /(<div id="recommended-grid"[^>]*>)/i,
    `$1\n${cardHtml}`
  );
  if (!wasAlreadyOnHome) {
    const escapedCat = categoryLabel.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const catCountRe = new RegExp(`(filterByCategory\\('${escapedCat}'\\)[\\s\\S]{0,650}?<span>)(\\d+)(<\\/span>)`, 'i');
    homeHtml = homeHtml.replace(catCountRe, (_, p1, num, p3) => `${p1}${Number(num) + 1}${p3}`);
  }
  fs.writeFileSync(homePath, homeHtml, 'utf8');

  // 4. data/admin-catalogo-360.json
  const admPath = path.join(ROOT, 'data', 'admin-catalogo-360.json');
  if (fs.existsSync(admPath)) {
    try {
      const adm = JSON.parse(fs.readFileSync(admPath, 'utf8'));
      const cleanRel = (p) => String(p || '').replace(/^(\.\.\/|\/)+/, '');
      const slug = prodJson.product_title
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-+|-+$/g, '')
        .slice(0, 32);

      const newEntry = {
        id,
        title: prodJson.product_title,
        slug,
        category: categoryLabel,
        is_new_bf: true,
        preco: prodJson.produto_atual.preco,
        preco_antigo: prodJson.produto_atual.preco_antigo,
        price_original_str: prodJson.price_original,
        discount_badge: prodJson.discount_badge,
        discount_pct: descNum,
        installment_text: prodJson.installment_text,
        sold_count: prodJson.sold_count,
        rating_score: String(prodJson.rating_score).replace('.', ','),
        img: cleanRel(prodJson.slider_imgs[0].src),
        slides: prodJson.slider_imgs.map((s) => ({ src: cleanRel(s.src), alt: s.alt })),
        variacoes: prodJson.produto_atual.variacoes,
        video: {
          src: prodJson.video.src,
          tagged_src: `${prodJson.video.src}#prod=${id}&slot=descricao&slug=prod${id}`,
          poster: cleanRel(prodJson.video.poster),
          duration: prodJson.video.duration || '0:20',
          catbox_id: prodJson.video.catbox_id,
        },
        creators_count: prodJson.creators.length,
        creators: prodJson.creators.map((c, ci) => ({
          name: c.name,
          username: c.username,
          avatar: cleanRel(c.avatar),
          poster: cleanRel(c.poster),
          video: c.video,
          tagged_video: `${c.video}#prod=${id}&slot=criador_${ci + 1}&slug=prod${id}`,
          catbox_id: c.catbox_id,
          likes: c.likes,
          description: c.description,
        })),
        details: prodJson.details,
        description_html: prodJson.description_html,
        size_guide_html: prodJson.size_guide_html || '',
        reviews_count: prodJson.reviews.length,
        reviews_photos_count: prodJson.reviews.reduce((acc, r) => acc + ((r.photos || []).length), 0),
        reviews: prodJson.reviews.map((r) => ({
          name: r.name,
          avatar: cleanRel(r.avatar),
          stars: r.stars,
          date_line: r.date_line,
          variation: r.variation,
          comment: r.comment,
          photos: (r.photos || []).map(cleanRel),
        })),
        health_score: 96,
        has_catbox_conflict: false,
        alerts: [],
      };

      adm.products = [newEntry, ...(adm.products || []).filter((p) => Number(p.id) !== id)];
      adm.total_products = adm.products.length;
      adm.generated_at = new Date().toISOString();
      fs.writeFileSync(admPath, JSON.stringify(adm), 'utf8');
    } catch (e) {}
  }
}

async function publishDraft(draftId, options = {}) {
  const draft = loadDraft(draftId);
  if (!draft) {
    return { ok: false, productId: 0, errors: [`Rascunho ${draftId} não encontrado.`] };
  }

  const id = Number(draft.targetId);
  const stamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const trackedPaths = [
    path.join(ROOT, 'data', 'produtos', 'index.js'),
    path.join(ROOT, 'js', 'catalogo.js'),
    path.join(ROOT, 'index.html'),
    path.join(ROOT, 'data', 'admin-catalogo-360.json'),
  ];

  const snapshots = new Map();
  for (const p of trackedPaths) {
    if (fs.existsSync(p)) snapshots.set(p, fs.readFileSync(p, 'utf8'));
  }
  const prodJsonPath = path.join(ROOT, 'data', 'produtos', `produto-${id}.json`);
  const prevProdJson = fs.existsSync(prodJsonPath) ? fs.readFileSync(prodJsonPath, 'utf8') : null;
  const copiedFiles = [];

  try {
    let prodJson = buildProductJsonFromDraft(draft);

    // Promote slides
    prodJson.slider_imgs = prodJson.slider_imgs.map((s, idx) => {
      const ext = path.extname(String(s.src).split('?')[0]) || '.webp';
      const rel = `img/studio-${id}-slide-${idx + 1}${ext}`;
      return { ...s, src: promoteMediaFile(s.src, rel, copiedFiles) };
    });

    // Promote variations
    const vars = prodJson.produto_atual.variacoes || {};
    let vCounter = 0;
    for (const grp of Object.values(vars)) {
      grp.opcoes = (grp.opcoes || []).map((opt) => {
        if (typeof opt === 'object' && opt.imagem) {
          vCounter += 1;
          const ext = path.extname(String(opt.imagem).split('?')[0]) || '.webp';
          const rel = `img/studio-${id}-var-${vCounter}${ext}`;
          return { ...opt, imagem: promoteMediaFile(opt.imagem, rel, copiedFiles) };
        }
        return opt;
      });
    }
    prodJson.produto_atual.img = prodJson.slider_imgs[0].src;
    prodJson.produto_atual.imagens = prodJson.slider_imgs.map((s) => s.src);

    // Promote description video poster
    if (prodJson.video && prodJson.video.poster) {
      const ext = path.extname(String(prodJson.video.poster).split('?')[0]) || '.jpg';
      const rel = `img/posters-desc/poster-desc-${id}${ext}`;
      prodJson.video.poster = `${promoteMediaFile(prodJson.video.poster, rel, copiedFiles)}?v=${stamp}`;
    }

    // Promote creators posters & avatars
    prodJson.creators = (prodJson.creators || []).map((c, idx) => {
      const pExt = path.extname(String(c.poster).split('?')[0]) || '.jpg';
      const pRel = `videosprodutos/posters/poster-prod-${id}-c${idx + 1}${pExt}`;
      const promotedPoster = `${promoteMediaFile(c.poster, pRel, copiedFiles)}?v=${stamp}`;

      let promotedAv = c.avatar;
      if (String(c.avatar || '').startsWith('/.studio-drafts/')) {
        const aExt = path.extname(String(c.avatar).split('?')[0]) || '.jpg';
        const aRel = `img/avatars-studio/creator-${id}-c${idx + 1}${aExt}`;
        promotedAv = `${promoteMediaFile(c.avatar, aRel, copiedFiles)}?v=${stamp}`;
      }
      return { ...c, poster: promotedPoster, avatar: promotedAv };
    });

    // Promote buyer unboxing photos
    prodJson.reviews = (prodJson.reviews || []).map((r, rIdx) => {
      const newPhotos = (r.photos || []).map((ph, pIdx) => {
        const ext = path.extname(String(ph).split('?')[0]) || '.jpg';
        const rel = `img/review-${id}-b${rIdx + 1}-${pIdx + 1}${ext}`;
        return promoteMediaFile(ph, rel, copiedFiles);
      });
      return { ...r, photos: newPhotos };
    });

    // Allocate unique verified Brazilian avatars (0 BAD_AVATARS, 0 MD5 collisions)
    prodJson = allocateVerifiedAvatars(prodJson, draft.gender || 'feminino');

    // Write product JSON & update catalogs
    fs.writeFileSync(prodJsonPath, JSON.stringify(prodJson, null, 2), 'utf8');
    updateCatalogFiles(prodJson, draft.category || 'casa');

    // Run mandatory validator!
    let valStdout = '';
    try {
      valStdout = execFileSync(process.execPath, [path.join(ROOT, 'scripts', 'validar-modelo-unico.js')], {
        cwd: ROOT,
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'pipe'],
      });
    } catch (valErr) {
      const combined = `${valErr.stdout || ''}\n${valErr.stderr || ''}`;
      const errLines = combined
        .split(/\r?\n/)
        .filter((l) => l.trim().startsWith('- ') || l.includes(`produto-${id}:`))
        .map((l) => l.replace(/^\s*-\s*/, '').trim());

      // Atomic rollback!
      for (const [p, content] of snapshots.entries()) fs.writeFileSync(p, content, 'utf8');
      if (prevProdJson === null) {
        if (fs.existsSync(prodJsonPath)) fs.unlinkSync(prodJsonPath);
      } else {
        fs.writeFileSync(prodJsonPath, prevProdJson, 'utf8');
      }
      for (const cf of copiedFiles) {
        if (fs.existsSync(cf)) {
          try { fs.unlinkSync(cf); } catch (_) {}
        }
      }

      return {
        ok: false,
        productId: id,
        errors: errLines.length ? errLines : ['Falha no validar-modelo-unico.js'],
      };
    }

    // Clear Node require cache for local server.js live serving
    try {
      delete require.cache[require.resolve('../../data/produtos/index')];
      delete require.cache[require.resolve(`../../data/produtos/produto-${id}.json`)];
    } catch (_) {}

    const warnings = valStdout
      .split(/\r?\n/)
      .filter((l) => l.includes(`produto-${id}:`))
      .map((l) => l.replace(/^\s*-\s*/, '').trim());

    if (options.deploy) {
      const relCopied = copiedFiles.map((abs) => path.relative(ROOT, abs).replace(/\\/g, '/'));
      const stageTargets = [
        `data/produtos/produto-${id}.json`,
        'data/produtos/index.js',
        'js/catalogo.js',
        'index.html',
        'data/admin-catalogo-360.json',
        ...relCopied,
      ];
      execFileSync('git', ['add', '--', ...stageTargets], { cwd: ROOT, stdio: 'pipe' });
      execFileSync('git', ['commit', '-m', `feat(studio): publicar produto #${id} via Stone Studio`], { cwd: ROOT, stdio: 'pipe' });
      execSync('git pull --rebase --autostash origin main', { cwd: ROOT, stdio: 'pipe' });
      execSync('git push origin main', { cwd: ROOT, stdio: 'pipe' });
      const vcOut = execSync('npx vercel --prod --yes', { cwd: ROOT, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
      const depMatch = vcOut.match(/https:\/\/stoneshopclone-[a-z0-9]+-k7s-projects-[a-z0-9]+\.vercel\.app/i);
      if (depMatch) {
        execSync(`npx vercel alias set ${depMatch[0]} stoneshopclone.vercel.app`, { cwd: ROOT, stdio: 'pipe' });
      }
    }

    return {
      ok: true,
      productId: id,
      warnings,
      liveUrl: `https://stoneshopclone.vercel.app/produto-${id}?owner=1`,
      adsUrl: 'https://stoneshopclone.vercel.app/videos-ads',
    };
  } catch (err) {
    for (const [p, content] of snapshots.entries()) fs.writeFileSync(p, content, 'utf8');
    if (prevProdJson === null) {
      if (fs.existsSync(prodJsonPath)) fs.unlinkSync(prodJsonPath);
    } else {
      fs.writeFileSync(prodJsonPath, prevProdJson, 'utf8');
    }
    for (const cf of copiedFiles) {
      if (fs.existsSync(cf)) {
        try { fs.unlinkSync(cf); } catch (_) {}
      }
    }
    return { ok: false, productId: id, errors: [err.message || String(err)] };
  }
}

module.exports = {
  allocateVerifiedAvatars,
  publishDraft,
};
