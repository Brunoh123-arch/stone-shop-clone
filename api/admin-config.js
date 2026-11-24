// API Serverless: Configuração Global + Overrides de Produtos + Catbox Lock Registry (Stone Shop)
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { setProductOverride, getAllProductOverrides } = require('./_lib/store-state');

let configStore = {
  pix_mode: "gateway",
  pix_key: "financeiro@stoneshop.com.br",
  pix_beneficiario: "STONE SHOP OFICIAL LTDA",
  pix_cidade: "SAO PAULO",
  gateway_provider: "syncpayments",
  whatsapp_suporte: "5511987654321",
  oferta_timer_minutos: 30,
  pessoas_olhando_min: 34,
  pessoas_olhando_max: 68,
  cupom_texto: "Black Friday - 12 de nov – 3 de dez",
  cupom_valor: "R$ 30,00",
  cupom_porcentagem: 74,
  frete_gratis: true,
  prazo_entrega: "2 a 7 dias úteis",
  social_proof_popups: true,
  store_name: "Stone Shop",
  store_sales: "112.2K vendido(s)",
  store_response_rate: "95% responde em 24 horas",
  store_shipping_rate: "99% envios pontuais",
  tiktok_pixel_id: "DBD7ASBC77UF91061F1G",
  tiktok_access_token: "5d6d02037cf86209372b4d1748ed7eba24158030",
  tiktok_test_code: "TEST96518",
  meta_pixel_id: "",
  catbox_custom_locks: {},
  atualizado_em: new Date().toISOString()
};

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");

  if (req.method === "OPTIONS") return res.status(200).end();

  if (req.method === "POST") {
    let body = req.body;
    if (typeof body === "string") {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    }
    if (!body || typeof body !== "object") {
      return res.status(400).json({ success: false, error: "Invalid body" });
    }

    // 1. Salvar override individual de produto (preço, bump, ativo) NO SERVIDOR!
    if (body.action === "save_product_override" && body.productId) {
      const saved = setProductOverride(body.productId, body.patch || {});
      return res.status(200).json({ success: true, override: saved, overrides: getAllProductOverrides() });
    }

    // 2. Upload direto via servidor para a Catbox com trava SHA-256 por Produto (sem bloqueio CORS!)
    if (body.action === "upload_catbox_base64" && body.base64 && body.productId) {
      try {
        const pid = Number(body.productId);
        const slot = String(body.slot || "criador");
        const buf = Buffer.from(String(body.base64), "base64");
        const sha256 = crypto.createHash("sha256").update(buf).digest("hex");

        configStore.catbox_hashes = configStore.catbox_hashes || {};
        if (configStore.catbox_hashes[sha256] && configStore.catbox_hashes[sha256].owner_product_id !== pid) {
          const prev = configStore.catbox_hashes[sha256];
          return res.status(409).json({
            success: false,
            conflict: true,
            error: `Conflito bloqueado! Este exato arquivo MP4 já pertence ao Produto #${prev.owner_product_id} (${prev.tagged_url}).`,
          });
        }

        const safeName = `stoneshop_prod_${pid}_${slot}_${Date.now()}.mp4`;
        const form = new FormData();
        form.append("reqtype", "fileupload");
        form.append("fileToUpload", new Blob([buf], { type: "video/mp4" }), safeName);
        const upRes = await fetch("https://catbox.moe/user/api.php", { method: "POST", body: form });
        const rawTxt = (await upRes.text()).trim();
        if (!upRes.ok || !rawTxt.startsWith("https://files.catbox.moe/")) {
          return res.status(502).json({ success: false, error: `Falha Catbox: ${rawTxt}` });
        }

        const cleanBase = rawTxt.split("#")[0].split("?")[0].trim();
        const taggedUrl = `${cleanBase}#prod=${pid}&slot=${encodeURIComponent(slot)}`;
        const lockEntry = {
          catbox_id: cleanBase.split("/").pop(),
          base_url: cleanBase,
          tagged_url: taggedUrl,
          sha256,
          owner_product_id: pid,
          slot,
          locked_at: new Date().toISOString(),
        };
        configStore.catbox_custom_locks[cleanBase] = lockEntry;
        configStore.catbox_hashes[sha256] = lockEntry;
        return res.status(200).json({ success: true, lock: lockEntry });
      } catch (upErr) {
        return res.status(500).json({ success: false, error: upErr.message });
      }
    }

    // 3. Registrar e travar vínculo de vídeo Catbox a um produto específico
    if (body.action === "register_catbox_lock" && body.baseUrl && body.productId) {
      const cleanBase = String(body.baseUrl).split("#")[0].split("?")[0].trim();
      const pid = Number(body.productId);
      const existing = configStore.catbox_custom_locks[cleanBase];
      if (existing && existing.owner_product_id !== pid) {
        return res.status(409).json({
          success: false,
          conflict: true,
          error: `Conflito bloqueado! Este vídeo (${cleanBase}) já pertence ao Produto #${existing.owner_product_id}.`,
          owner: existing,
        });
      }
      const taggedUrl = `${cleanBase}#prod=${pid}&slot=${encodeURIComponent(body.slot || 'criador')}`;
      const lockEntry = {
        base_url: cleanBase,
        tagged_url: taggedUrl,
        owner_product_id: pid,
        slot: body.slot || "criador",
        locked_at: new Date().toISOString(),
      };
      configStore.catbox_custom_locks[cleanBase] = lockEntry;
      return res.status(200).json({ success: true, lock: lockEntry });
    }

    configStore = {
      ...configStore,
      ...body,
      atualizado_em: new Date().toISOString()
    };
    return res.status(200).json({ success: true, config: configStore, overrides: getAllProductOverrides() });
  }

  return res.status(200).json({
    success: true,
    config: configStore,
    overrides: getAllProductOverrides(),
  });
};
