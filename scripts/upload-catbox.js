#!/usr/bin/env node
/**
 * UPLOADER OFICIAL CATBOX COM TRAVA ANTI-CONFLITO POR PRODUTO (STONE SHOP)
 * Uso CLI:
 *   node scripts/upload-catbox.js --produto 104 --tipo descricao --arquivo caminho/video.mp4
 *   node scripts/upload-catbox.js --produto 104 --tipo criador --user "mari.looks" --arquivo caminho/video.mp4
 *
 * Garante que NENHUM vídeo suba sem vínculo explícito ao ID do produto,
 * carimba a URL com #prod=<ID>&slot=<tipo>&slug=<slug> e trava no data/catbox-registry.json.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.join(__dirname, '..');
const REGISTRY_PATH = path.join(ROOT, 'data', 'catbox-registry.json');
const PRODS_DIR = path.join(ROOT, 'data', 'produtos');

function slugifyShort(str) {
  return String(str || 'produto')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 28) || 'produto';
}

async function uploadToCatboxLocked({ productId, slot = 'criador', filePath, creatorUsername = '' }) {
  const pid = Number(productId);
  if (!pid || isNaN(pid)) {
    throw new Error('ID do produto (--produto <ID>) é OBRIGATÓRIO para subir vídeo na Catbox!');
  }
  if (!filePath || !fs.existsSync(filePath)) {
    throw new Error(`Arquivo de vídeo não encontrado: ${filePath}`);
  }

  const prodJsonPath = path.join(PRODS_DIR, `produto-${pid}.json`);
  if (!fs.existsSync(prodJsonPath)) {
    throw new Error(`produto-${pid}.json não existe em data/produtos/!`);
  }
  const prodData = JSON.parse(fs.readFileSync(prodJsonPath, 'utf8'));
  const slug = slugifyShort(prodData.product_title || prodData.title);

  const fileBuffer = fs.readFileSync(filePath);
  const sha256 = crypto.createHash('sha256').update(fileBuffer).digest('hex');

  const registry = fs.existsSync(REGISTRY_PATH)
    ? JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'))
    : { version: '1.0.0', videos: {}, hashes: {} };
  registry.hashes = registry.hashes || {};

  // TRAVA ANTI-CONFLITO POR HASH SHA-256 DO ARQUIVO MP4!
  if (registry.hashes[sha256] && registry.hashes[sha256].owner_product_id !== pid) {
    const prev = registry.hashes[sha256];
    throw new Error(
      `🚨 BLOQUEIO ANTI-CONFLITO: Este exato arquivo MP4 (SHA256 ${sha256.slice(0, 10)}) JÁ PERTENCE ao Produto #${prev.owner_product_id} (${prev.owner_product_title}) -> ${prev.tagged_url}! Proibido reaproveitar em outro produto.`
    );
  }

  // Se já foi enviado para este MESMO produto antes, retorna o link oficial sem duplicar upload
  if (registry.hashes[sha256] && registry.hashes[sha256].owner_product_id === pid) {
    return registry.hashes[sha256];
  }

  // Envia para Catbox com nome de arquivo já identificado por produto
  const safeUploadName = `stoneshop_prod_${pid}_${slot}_${Date.now()}.mp4`;
  const form = new FormData();
  form.append('reqtype', 'fileupload');
  form.append('fileToUpload', new Blob([fileBuffer], { type: 'video/mp4' }), safeUploadName);

  const resp = await fetch('https://catbox.moe/user/api.php', {
    method: 'POST',
    body: form,
  });

  const rawText = (await resp.text()).trim();
  if (!resp.ok || !rawText.startsWith('https://files.catbox.moe/')) {
    throw new Error(`Falha no upload Catbox (${resp.status}): ${rawText}`);
  }

  const baseUrl = rawText.split('#')[0].split('?')[0];
  const catboxId = path.basename(baseUrl);
  const taggedUrl = `${baseUrl}#prod=${pid}&slot=${encodeURIComponent(slot)}&slug=${slug}`;

  const entry = {
    catbox_id: catboxId,
    base_url: baseUrl,
    tagged_url: taggedUrl,
    sha256,
    owner_product_id: pid,
    owner_product_title: prodData.product_title,
    slot,
    creator_username: creatorUsername,
    uploaded_at: new Date().toISOString(),
  };

  registry.videos[baseUrl] = entry;
  registry.hashes[sha256] = entry;
  registry.updated_at = new Date().toISOString();
  fs.writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2), 'utf8');

  return entry;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const getArg = (flag) => {
    const idx = args.indexOf(flag);
    return idx !== -1 ? args[idx + 1] : null;
  };
  const productId = getArg('--produto') || getArg('-p');
  const slot = getArg('--tipo') || getArg('-t') || 'criador';
  const filePath = getArg('--arquivo') || getArg('-f');
  const creatorUsername = getArg('--user') || getArg('-u') || '';

  uploadToCatboxLocked({ productId, slot, filePath, creatorUsername })
    .then((entry) => {
      console.log('✅ Upload Catbox Registrado e Travado com Sucesso!');
      console.log(JSON.stringify(entry, null, 2));
    })
    .catch((err) => {
      console.error('❌ Erro:', err.message);
      process.exit(1);
    });
}

module.exports = { uploadToCatboxLocked };
